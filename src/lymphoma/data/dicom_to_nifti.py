"""Convert DICOM series referenced by lymphoma manifests to NIfTI."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from collections.abc import Iterable, Iterator

LOGGER = logging.getLogger(__name__)
REQUIRED_COLUMNS = ("Subject ID", "Study UID", "File Location")
OUTPUT_COLUMNS = ("pet_path", "ct_path", "mask_path", "nifti_conversion_error")
MODALITY_PATH = {
    "pet": "pet_path",
    "ct": "ct_path",
    "mask": "mask_path",
}


def repository_root() -> Path:
    """Return repository root based on this module's location."""
    return Path(__file__).resolve().parents[3]


def _safe_name(value: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value.strip()).strip(" .")
    if not safe or safe in {".", ".."}:
        raise ValueError(f"Value cannot be used as a path component: {value!r}")
    return safe


def _resolve_location(value: str, manifest_path: Path) -> Path:
    location = Path(value.strip())
    if location.is_absolute():
        return location
    root_relative = repository_root() / location
    if root_relative.exists():
        return root_relative
    return manifest_path.parent / location


def _read_manifest(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing:
            raise ValueError(
                f"Manifest is missing required columns: {', '.join(missing)}"
            )
        return list(reader), columns


def _manifest_series(
    selected_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]] | None,
    manifest_path: Path,
) -> dict[tuple[str, str], list[tuple[Path, dict[str, str]]]]:
    """Find all DICOM series for each selected patient/study."""
    selected_keys = {
        (row["Subject ID"].strip(), row["Study UID"].strip())
        for row in selected_rows
    }
    all_rows = selected_rows
    if source_rows is not None:
        all_rows = [
            row
            for row in source_rows
            if (row["Subject ID"].strip(), row["Study UID"].strip()) in selected_keys
        ]

    grouped: dict[tuple[str, str], list[tuple[Path, dict[str, str]]]] = defaultdict(list)
    seen_locations: set[tuple[str, str, str]] = set()
    for row in all_rows:
        patient_id = row["Subject ID"].strip()
        study_uid = row["Study UID"].strip()
        location_value = row["File Location"].strip()
        if not patient_id or not study_uid or not location_value:
            continue
        key = (patient_id, study_uid)
        location_key = (patient_id, study_uid, location_value)
        if location_key in seen_locations:
            continue
        seen_locations.add(location_key)
        grouped[key].append((_resolve_location(location_value, manifest_path), row))
    return grouped


def _sidecar_for_nifti(nifti_path: Path) -> Path:
    if nifti_path.name.lower().endswith(".nii.gz"):
        return nifti_path.with_name(nifti_path.name[:-7] + ".json")
    return nifti_path.with_suffix(".json")


def _read_sidecar(nifti_path: Path) -> dict[str, object]:
    sidecar = _sidecar_for_nifti(nifti_path)
    try:
        with sidecar.open(encoding="utf-8") as file:
            metadata = json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}
    return metadata if isinstance(metadata, dict) else {}


def _classify_series(
    metadata: dict[str, object],
    manifest_row: dict[str, str],
) -> str | None:
    """Classify a converted series as PET, CT, or segmentation."""
    sidecar_values = [
        str(value)
        for value in (
            metadata.get("Modality"),
            metadata.get("SOPClassName"),
            metadata.get("SeriesDescription"),
            metadata.get("ProtocolName"),
        )
        if value
    ]
    modality = _classify_values(sidecar_values)
    if modality is not None:
        return modality

    manifest_values = [
        str(value)
        for value in (
            manifest_row.get("Modality"),
            manifest_row.get("SOP Class Name"),
            manifest_row.get("Series Description"),
        )
        if value
    ]
    return _classify_values(manifest_values)


def _classify_values(values: list[str]) -> str | None:
    joined = " ".join(values).casefold()
    if any(token in joined for token in ("segmentation", "seg storage")):
        return "mask"

    modalities = {value.strip().upper() for value in values}
    if "SEG" in modalities:
        return "mask"
    if "PT" in modalities or "PET" in modalities:
        return "pet"
    if "CT" in modalities:
        return "ct"

    for text in values:
        tokens = set(re.findall(r"[a-z0-9]+", text.casefold()))
        if tokens.intersection({"pet", "pt", "suv"}):
            return "pet"
        if "ct" in tokens:
            return "ct"
    return None


def _convert_directory(
    dcm2niix: str,
    dicom_directory: Path,
    output_directory: Path,
) -> list[Path]:
    if not dicom_directory.is_dir():
        raise FileNotFoundError(
            f"DICOM File Location is not a directory: {dicom_directory}"
        )
    output_directory.mkdir(parents=True, exist_ok=True)
    command = [
        dcm2niix,
        "-z",
        "y",
        "-b",
        "y",
        "-f",
        "%p_%s",
        "-o",
        str(output_directory),
        str(dicom_directory),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"dcm2niix failed for {dicom_directory} "
            f"(exit {completed.returncode}): {detail}"
        )
    return sorted(output_directory.glob("*.nii.gz")) + sorted(
        output_directory.glob("*.nii")
    )


def _copy_nifti(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = destination.with_name(f".{destination.name}.tmp")
    try:
        shutil.copyfile(source, temporary_path)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _stored_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _convert_study(
    key: tuple[str, str],
    series: list[tuple[Path, dict[str, str]]],
    output_root: Path,
    repository: Path,
    dcm2niix: str,
) -> tuple[dict[str, str], str]:
    patient_id, study_uid = key
    subject_directory = output_root / _safe_name(patient_id)
    output_names = {
        "pet": f"{_safe_name(study_uid)}_PET.nii.gz",
        "ct": f"{_safe_name(study_uid)}_CT.nii.gz",
        "mask": f"{_safe_name(study_uid)}_mask.nii.gz",
    }
    selected: dict[str, list[Path]] = {"pet": [], "ct": [], "mask": []}
    errors = []

    with tempfile.TemporaryDirectory(prefix="dicom_to_nifti_") as temporary_name:
        temporary_root = Path(temporary_name)
        for index, (dicom_directory, manifest_row) in enumerate(series):
            try:
                converted = _convert_directory(
                    dcm2niix,
                    dicom_directory,
                    temporary_root / f"series_{index:04d}",
                )
                if not converted:
                    errors.append(f"No NIfTI generated from {dicom_directory}")
                for nifti_path in converted:
                    modality = _classify_series(
                        _read_sidecar(nifti_path),
                        manifest_row,
                    )
                    if modality is None:
                        errors.append(
                            f"Could not identify modality for {nifti_path.name}"
                        )
                    else:
                        selected[modality].append(nifti_path)
            except (OSError, RuntimeError) as error:
                errors.append(str(error))

        output_paths: dict[str, str] = {}
        for modality, candidates in selected.items():
            path_column = MODALITY_PATH[modality]
            if not candidates:
                errors.append(f"Missing converted {modality.upper()} series")
                output_paths[path_column] = ""
                continue
            if len(candidates) > 1:
                errors.append(
                    f"Multiple converted {modality.upper()} series; "
                    "select the intended series before preprocessing"
                )
                output_paths[path_column] = ""
                continue
            destination = subject_directory / output_names[modality]
            _copy_nifti(candidates[0], destination)
            output_paths[path_column] = _stored_path(destination, repository)

    return output_paths, "; ".join(errors)


def _iter_progress(items: Iterable[tuple[str, str]]) -> Iterator[tuple[str, str]]:
    try:
        from tqdm.auto import tqdm
    except ImportError:
        yield from items
    else:
        yield from tqdm(items, desc="Converting studies", unit="study")


def convert_manifest(
    manifest_path: Path,
    output_manifest: Path,
    output_root: Path,
    *,
    source_manifest: Path | None = None,
    dcm2niix: str = "dcm2niix",
) -> tuple[int, int]:
    """Convert each selected study and save a manifest with NIfTI paths."""
    manifest_path = Path(manifest_path)
    output_manifest = Path(output_manifest)
    output_root = Path(output_root)
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest does not exist: {manifest_path}")

    selected_rows, input_columns = _read_manifest(manifest_path)
    for row in selected_rows:
        if not row["Subject ID"].strip() or not row["Study UID"].strip():
            raise ValueError("Manifest contains an empty Subject ID or Study UID.")

    source_rows = None
    if source_manifest is not None:
        source_manifest = Path(source_manifest)
        if source_manifest.is_file():
            source_rows, _ = _read_manifest(source_manifest)
        elif source_manifest != manifest_path:
            raise FileNotFoundError(f"Source manifest does not exist: {source_manifest}")

    series_by_study = _manifest_series(
        selected_rows,
        source_rows,
        source_manifest if source_rows is not None else manifest_path,
    )
    grouped_selected: dict[tuple[str, str], dict[str, str]] = {}
    for row in selected_rows:
        key = (row["Subject ID"].strip(), row["Study UID"].strip())
        grouped_selected.setdefault(key, row)

    output_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    successful = 0
    for key in _iter_progress(list(grouped_selected)):
        base_row = dict(grouped_selected[key])
        series = series_by_study.get(key, [])
        if not series:
            paths = {column: "" for column in OUTPUT_COLUMNS[:3]}
            error = "No DICOM File Location found for this study"
        else:
            paths, error = _convert_study(
                key,
                series,
                output_root,
                repository_root(),
                dcm2niix,
            )
        base_row.update(paths)
        base_row["nifti_conversion_error"] = error
        if not error:
            successful += 1
        results.append(base_row)

    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    output_columns = list(input_columns)
    for column in OUTPUT_COLUMNS:
        if column not in output_columns:
            output_columns.append(column)
    with tempfile.NamedTemporaryFile(
        mode="w",
        newline="",
        encoding="utf-8",
        prefix=f".{output_manifest.name}.",
        suffix=".tmp",
        dir=output_manifest.parent,
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
        writer = csv.DictWriter(
            temporary_file,
            fieldnames=output_columns,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(results)
    try:
        os.replace(temporary_path, output_manifest)
    finally:
        temporary_path.unlink(missing_ok=True)
    return successful, len(results) - successful


def main() -> None:
    """Parse input/output paths and run DICOM-to-NIfTI conversion."""
    root = repository_root()
    default_source_manifest = (
        root / "results" / "Clinical-Metadata-FDG-PET_CT-Lesions.csv"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=root / "results" / "manifest_lymphoma.csv",
        help="Filtered lymphoma manifest.",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=default_source_manifest if default_source_manifest.is_file() else None,
        help=(
            "Optional full series-level manifest used to find PET, CT, and SEG series "
            "for selected studies."
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=root / "data" / "nifti",
        help="Directory for converted NIfTI files.",
    )
    parser.add_argument(
        "--output-manifest",
        type=Path,
        default=root / "results" / "manifest_lymphoma_nifti.csv",
        help="Destination manifest path.",
    )
    parser.add_argument(
        "--dcm2niix",
        default="dcm2niix",
        help="Path to the dcm2niix executable.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        successful, failed = convert_manifest(
            args.manifest,
            args.output_manifest,
            args.output_root,
            source_manifest=args.source_manifest,
            dcm2niix=args.dcm2niix,
        )
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
    LOGGER.info(
        "Conversion complete: %d studies with all modalities, %d studies with errors.",
        successful,
        failed,
    )
    LOGGER.info("Updated manifest saved to %s", args.output_manifest)


if __name__ == "__main__":
    main()
