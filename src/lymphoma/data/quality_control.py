"""Quality checks for PET/CT studies and segmentation masks."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path

import nibabel as nib
import numpy as np
from nibabel.spatialimages import SpatialImage


@dataclass(frozen=True)
class Study:
    """Paths and identifiers for one study."""

    study_id: str
    patient_id: str
    pet_path: Path | None
    ct_path: Path | None
    mask_path: Path | None


@dataclass
class QCResult:
    """Study and reasons it should be excluded."""

    study: Study
    reasons: list[str] = field(default_factory=list)


def repository_root() -> Path:
    """Return the repository root based on this module's location."""
    return Path(__file__).resolve().parents[3]


def _is_file(path: Path | None) -> bool:
    return path is not None and path.is_file()


def check_pairing(pet_path: Path | None, ct_path: Path | None) -> bool:
    """Return whether both PET and CT files exist."""
    return _is_file(pet_path) and _is_file(ct_path)


def _pairing_issues(study: Study) -> list[str]:
    reasons = []
    if not _is_file(study.pet_path):
        reasons.append("Missing PET")
    if not _is_file(study.ct_path):
        reasons.append("Missing CT")
    return reasons


def _load_image(path: Path, modality: str) -> tuple[SpatialImage | None, str | None]:
    try:
        image = nib.load(str(path))
    except Exception as error:
        return None, f"Unreadable {modality}: {error}"
    return image, None


def _spacing(image: SpatialImage) -> np.ndarray:
    if len(image.shape) < 3 or len(image.header.get_zooms()) < 3:
        raise ValueError("image must have at least three dimensions")
    return np.asarray(image.header.get_zooms()[:3], dtype=float)


def _geometry_issues(pet_path: Path, ct_path: Path) -> list[str]:
    pet, pet_error = _load_image(pet_path, "PET")
    ct, ct_error = _load_image(ct_path, "CT")
    errors = [error for error in (pet_error, ct_error) if error is not None]
    if errors:
        return errors
    assert pet is not None and ct is not None

    try:
        pet_spacing = _spacing(pet)
        ct_spacing = _spacing(ct)
        pet_orientation = nib.aff2axcodes(pet.affine)
        ct_orientation = nib.aff2axcodes(ct.affine)
    except (ValueError, TypeError, np.linalg.LinAlgError) as error:
        return [f"Invalid image geometry: {error}"]

    reasons = []
    if pet_orientation != ct_orientation:
        reasons.append("Orientation mismatch")
    if not np.allclose(pet_spacing, ct_spacing, rtol=1e-3, atol=1e-3):
        reasons.append("Spacing mismatch")
    if pet.shape[:3] != ct.shape[:3]:
        reasons.append("Shape mismatch")
    if not np.allclose(pet.affine, ct.affine, rtol=1e-5, atol=1e-3):
        reasons.append("Affine mismatch")
    return reasons


def check_geometry(pet_path: Path, ct_path: Path) -> bool:
    """Return whether PET and CT orientation, spacing, and affine are compatible."""
    if not _is_file(pet_path) or not _is_file(ct_path):
        return False
    return not _geometry_issues(pet_path, ct_path)


def _mask_issue(mask_path: Path | None) -> str | None:
    if not _is_file(mask_path):
        return "Missing mask"
    assert mask_path is not None
    image, error = _load_image(mask_path, "mask")
    if error is not None:
        return error
    assert image is not None
    try:
        if not np.any(np.asanyarray(image.dataobj) > 0):
            return "Empty mask"
    except Exception as error:
        return f"Unreadable mask: {error}"
    return None


def check_mask(mask_path: Path | None) -> bool:
    """Return whether the mask can be loaded and contains at least one positive voxel."""
    return _mask_issue(mask_path) is None


def check_study(study: Study) -> QCResult:
    """Run all applicable checks for a study and collect exclusion reasons."""
    reasons = _pairing_issues(study)
    if not reasons and study.pet_path is not None and study.ct_path is not None:
        reasons.extend(_geometry_issues(study.pet_path, study.ct_path))
    mask_issue = _mask_issue(study.mask_path)
    if mask_issue is not None:
        reasons.append(mask_issue)
    return QCResult(study=study, reasons=reasons)


def _record_path(value: str, csv_path: Path) -> Path | None:
    if not value.strip():
        return None
    path = Path(value.strip())
    if path.is_absolute():
        return path
    root_relative = repository_root() / path
    if root_relative.exists():
        return root_relative
    return csv_path.parent / path


def _load_csv(path: Path) -> list[Study]:
    studies = []
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"pet_path", "ct_path", "mask_path"}
        missing = required.difference(reader.fieldnames or ())
        if missing:
            columns = ", ".join(sorted(missing))
            raise ValueError(f"CSV is missing required columns: {columns}")
        for index, row in enumerate(reader, start=1):
            study_id = (row.get("study_id") or "").strip() or f"study-{index}"
            patient_id = (row.get("patient_id") or "").strip()
            studies.append(
                Study(
                    study_id=study_id,
                    patient_id=patient_id,
                    pet_path=_record_path(row.get("pet_path") or "", path),
                    ct_path=_record_path(row.get("ct_path") or "", path),
                    mask_path=_record_path(row.get("mask_path") or "", path),
                )
            )
    return studies


def _load_directory(directory: Path) -> list[Study]:
    aliases = {
        "pet": "pet_path",
        "suv": "pet_path",
        "ct": "ct_path",
        "ctres": "ct_path",
        "seg": "mask_path",
        "mask": "mask_path",
    }
    preferred = {
        "pet_path": ("suv", "pet"),
        "ct_path": ("ctres", "ct"),
        "mask_path": ("seg", "mask"),
    }
    by_folder: dict[Path, dict[str, list[tuple[str, Path]]]] = {}
    for path in sorted((*directory.rglob("*.nii"), *directory.rglob("*.nii.gz"))):
        name = path.name.lower()
        stem = name[:-7] if name.endswith(".nii.gz") else name[:-4]
        field_name = aliases.get(stem)
        if field_name is not None:
            by_folder.setdefault(path.parent, {}).setdefault(field_name, []).append(
                (stem, path)
            )

    studies = []
    for folder, candidates in sorted(by_folder.items()):
        paths = {}
        for field_name, options in preferred.items():
            available = candidates.get(field_name, [])
            paths[field_name] = next(
                (
                    file_path
                    for alias in options
                    for stem, file_path in available
                    if stem == alias
                ),
                None,
            )
        studies.append(
            Study(
                study_id=folder.name,
                patient_id=folder.parent.name,
                pet_path=paths["pet_path"],
                ct_path=paths["ct_path"],
                mask_path=paths["mask_path"],
            )
        )
    return studies


def load_studies(input_path: Path) -> list[Study]:
    """Load studies from a CSV manifest or a tree of per-study NIfTI folders."""
    if input_path.is_file():
        if input_path.suffix.lower() != ".csv":
            raise ValueError(f"Input file must be a CSV manifest: {input_path}")
        return _load_csv(input_path)
    if input_path.is_dir():
        return _load_directory(input_path)
    raise FileNotFoundError(f"Input path does not exist: {input_path}")


def generate_report(results: list[QCResult], output_path: Path) -> Path:
    """Write a Markdown report listing studies excluded by QC."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    discarded = [result for result in results if result.reasons]
    lines = [
        "# Quality control report",
        "",
        f"Studies checked: {len(results)}",
        f"Studies discarded: {len(discarded)}",
        "",
    ]
    if not discarded:
        lines.append("No studies were discarded.")
    else:
        lines.extend(
            [
                "| Patient | Study | Reasons |",
                "| --- | --- | --- |",
            ]
        )
        for result in discarded:
            patient_id = result.study.patient_id.replace("|", r"\|") or "Unknown"
            study_id = result.study.study_id.replace("|", r"\|")
            reasons = "; ".join(result.reasons).replace("|", r"\|")
            lines.append(f"| {patient_id} | {study_id} | {reasons} |")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    """Run QC for an input manifest or directory and write its report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        type=Path,
        help="CSV manifest or directory containing per-study NIfTI folders",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository_root() / "results" / "qc_report.md",
        help="Markdown report path (default: results/qc_report.md)",
    )
    args = parser.parse_args()

    results = [check_study(study) for study in load_studies(args.input)]
    report_path = generate_report(results, args.output)
    discarded = sum(bool(result.reasons) for result in results)
    print(f"Checked {len(results)} studies; discarded {discarded}.")
    print(f"QC report written to {report_path}")


if __name__ == "__main__":
    main()
