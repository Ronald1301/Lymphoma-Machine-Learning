"""Preprocess QC-passing lymphoma studies into per-study compressed caches."""

from __future__ import annotations

import argparse
import csv
import logging
import os
from dataclasses import dataclass
from pathlib import Path
import re
import tempfile
from collections.abc import Iterable, Iterator

import nibabel as nib
import numpy as np

LOGGER = logging.getLogger(__name__)
MODALITY_PATH_COLUMNS = {
    "pet_path": ("pet_path", "PET Path", "PET_path"),
    "ct_path": ("ct_path", "CT Path", "CT_path"),
    "mask_path": ("mask_path", "Mask Path", "SEG Path", "SEG_path"),
}
IDENTIFIER_COLUMNS = {
    "subject_id": ("Subject ID", "patient_id", "Patient ID"),
    "study_id": ("Study UID", "study_id", "Study ID"),
}


@dataclass(frozen=True)
class CacheStudy:
    """Image paths and identifiers for a manifest study."""

    study_id: str
    patient_id: str
    pet_path: Path | None
    ct_path: Path | None
    mask_path: Path | None


def repository_root() -> Path:
    """Return repository root from this module's location."""
    return Path(__file__).resolve().parents[3]


def _column(row: dict[str, str], aliases: tuple[str, ...]) -> str:
    """Get a non-empty CSV value, matching column names case-insensitively."""
    normalized = {key.strip().casefold(): value for key, value in row.items() if key}
    for alias in aliases:
        value = normalized.get(alias.casefold(), "")
        if value and value.strip():
            return value.strip()
    return ""


def _resolve_path(value: str, manifest_path: Path) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    root_relative = repository_root() / path
    if root_relative.exists():
        return root_relative
    return manifest_path.parent / path


def _parse_bool(value: str, field: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Missing or invalid {field} value: {value!r}")


def _safe_cache_name(identifier: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", identifier.strip()).strip(" .")
    if not safe or safe in {".", ".."}:
        raise ValueError(
            f"Identifier cannot be used as a cache filename: {identifier!r}"
        )
    return safe


def _row_study(
    row: dict[str, str], manifest_path: Path, row_number: int
) -> tuple[CacheStudy, str]:
    subject_id = _column(row, IDENTIFIER_COLUMNS["subject_id"])
    study_id = _column(row, IDENTIFIER_COLUMNS["study_id"]) or subject_id
    if not subject_id:
        subject_id = study_id or f"study-{row_number}"
    if not study_id:
        study_id = subject_id

    pet_path = _resolve_path(
        _column(row, MODALITY_PATH_COLUMNS["pet_path"]), manifest_path
    )
    ct_path = _resolve_path(
        _column(row, MODALITY_PATH_COLUMNS["ct_path"]), manifest_path
    )
    mask_path = _resolve_path(
        _column(row, MODALITY_PATH_COLUMNS["mask_path"]), manifest_path
    )
    study = CacheStudy(
        study_id=study_id,
        patient_id=subject_id,
        pet_path=pet_path,
        ct_path=ct_path,
        mask_path=mask_path,
    )
    return study, _safe_cache_name(subject_id)


def _find_column(row: dict[str, str], *names: str) -> str:
    return _column(row, names)


def _ct_to_model_range(ct_data: np.ndarray) -> np.ndarray:
    """Clip CT in HU and scale to the project's [-1, 1] input range."""
    if ct_data.ndim != 3 or not np.all(np.isfinite(ct_data)):
        raise ValueError("CT must be a finite 3D volume.")
    clipped = np.clip(ct_data.astype(np.float32, copy=False), -1000, 1000)
    return (clipped / 1000).astype(np.float32, copy=False)


def _load_aligned_volumes(
    study: CacheStudy,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load CT and mask and ensure they occupy PET's exact voxel grid."""
    assert study.pet_path is not None
    assert study.ct_path is not None
    assert study.mask_path is not None
    pet_image = nib.load(str(study.pet_path))
    ct_image = nib.load(str(study.ct_path))
    mask_image = nib.load(str(study.mask_path))

    images = (pet_image, ct_image, mask_image)
    reference = pet_image
    for name, image in zip(("PET", "CT", "mask"), images, strict=True):
        if len(image.shape) != 3:
            raise ValueError(f"{name} must be a 3D image; got shape {image.shape}.")
        if image.shape != reference.shape or not np.allclose(
            image.affine, reference.affine, rtol=1e-5, atol=1e-3
        ):
            raise ValueError(f"{name} geometry does not match the PET grid.")

    ct_data = np.asanyarray(ct_image.dataobj)
    mask_data = np.asanyarray(mask_image.dataobj)
    if not np.all(np.isfinite(mask_data)):
        raise ValueError("Mask contains non-finite values.")
    if not np.any(mask_data > 0):
        raise ValueError("Empty mask.")
    return (
        _ct_to_model_range(ct_data),
        (mask_data > 0).astype(np.uint8),
        reference.affine.astype(np.float64),
        np.asarray(reference.header.get_zooms()[:3], dtype=np.float64),
    )


def _write_cache(
    cache_path: Path,
    pet_data: np.ndarray,
    suv_data: np.ndarray,
    ct_data: np.ndarray,
    mask_data: np.ndarray,
    affine: np.ndarray,
    spacing: np.ndarray,
    study: CacheStudy,
) -> None:
    """Write all study arrays to a temporary NPZ and atomically publish it."""
    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=".npz",
        prefix=f".{cache_path.stem}.",
        dir=cache_path.parent,
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
    try:
        np.savez_compressed(
            temporary_path,
            pet=np.asarray(pet_data, dtype=np.float32),
            suv=np.asarray(suv_data, dtype=np.float32),
            ct=np.asarray(ct_data, dtype=np.float32),
            mask=np.asarray(mask_data, dtype=np.uint8),
            affine=affine,
            spacing=spacing,
            patient_id=np.asarray(study.patient_id),
            study_id=np.asarray(study.study_id),
        )
        os.replace(temporary_path, cache_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _progress(
    iterable: Iterable[dict[str, str]], total: int
) -> Iterator[dict[str, str]]:
    try:
        from tqdm.auto import tqdm
    except ImportError:
        def display_progress() -> Iterator[dict[str, str]]:
            width = 24
            for index, item in enumerate(iterable, start=1):
                completed = min(width, round(width * index / max(total, 1)))
                bar = "#" * completed + "-" * (width - completed)
                print(
                    f"\rCaching studies: [{bar}] {index}/{total}",
                    end="\n" if index == total else "",
                    flush=True,
                )
                yield item

        return display_progress()
    return iter(tqdm(iterable, total=total, desc="Caching studies", unit="study"))


def _process_row(
    row: dict[str, str],
    row_number: int,
    manifest_path: Path,
    output_dir: Path,
) -> tuple[str, str | None]:
    study, cache_name = _row_study(row, manifest_path, row_number)
    cache_path = output_dir / f"{cache_name}.npz"
    include = _find_column(row, "include")
    if include and not _parse_bool(include, "include"):
        return "excluded", "Manifest include=false"
    if cache_path.is_file():
        return "cached", None

    from lymphoma.data.quality_control import check_study

    qc_result = check_study(study)
    if qc_result.reasons:
        reason = "; ".join(qc_result.reasons)
        LOGGER.warning("Skipping %s: %s", study.study_id, reason)
        return "skipped", reason

    try:
        from lymphoma.data.preprocess import preprocess_pet

        if study.pet_path is None:
            raise ValueError("Missing PET path.")
        suv_flag = _find_column(row, "suv_available", "SUV available")
        is_suv = _parse_bool(suv_flag, "suv_available")
        weight = _find_column(
            row, "patient_weight_kg", "weight_kg", "Patient Weight (kg)"
        )
        dose = _find_column(
            row, "injected_dose_bq", "dose_bq", "Injected Dose (Bq)"
        )
        elapsed = _find_column(row, "elapsed_seconds", "injection_to_scan_seconds")

        ct_data, mask_data, affine, spacing = _load_aligned_volumes(study)
        weight_kg = float(weight) if weight else None
        dose_bq = float(dose) if dose else None
        elapsed_seconds = float(elapsed) if elapsed else 0.0
        output_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=f".{cache_name}.", dir=output_dir
        ) as temporary_directory:
            temporary_dir = Path(temporary_directory)
            pet_path, suv_path = preprocess_pet(
                study.pet_path,
                temporary_dir / "pet.nii.gz",
                temporary_dir / "suv.nii.gz",
                is_suv=is_suv,
                patient_weight_kg=weight_kg,
                injected_dose_bq=dose_bq,
                elapsed_seconds=elapsed_seconds,
            )
            pet_data = np.asanyarray(nib.load(str(pet_path)).dataobj)
            suv_data = np.asanyarray(nib.load(str(suv_path)).dataobj)
            if pet_data.shape != ct_data.shape or suv_data.shape != ct_data.shape:
                raise ValueError(
                    "Preprocessed PET/SUV shape does not match CT and mask."
                )
            _write_cache(
                cache_path,
                pet_data,
                suv_data,
                ct_data,
                mask_data,
                affine,
                spacing,
                study,
            )
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        LOGGER.warning("Skipping %s: %s", study.study_id, error)
        return "skipped", str(error)
    return "created", None


def make_cache(manifest_path: Path, output_dir: Path) -> dict[str, int]:
    """Run QC and preprocess each manifest study unless its cache already exists."""
    manifest_path = Path(manifest_path)
    output_dir = Path(output_dir)
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest does not exist: {manifest_path}")

    with manifest_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required_groups = (
            MODALITY_PATH_COLUMNS["pet_path"],
            MODALITY_PATH_COLUMNS["ct_path"],
            MODALITY_PATH_COLUMNS["mask_path"],
        )
        columns = {name.casefold() for name in (reader.fieldnames or [])}
        missing_groups = [
            aliases[0]
            for aliases in required_groups
            if not any(alias.casefold() in columns for alias in aliases)
        ]
        if missing_groups:
            raise ValueError(
                "Manifest is missing image path columns: " + ", ".join(missing_groups)
            )
        rows = list(reader)

    output_dir.mkdir(parents=True, exist_ok=True)
    names = []
    for row_number, row in enumerate(rows, start=1):
        _, name = _row_study(row, manifest_path, row_number)
        names.append(name)
    if len(set(names)) != len(names):
        raise ValueError(
            "Manifest contains duplicate subject IDs; cache filenames collide."
        )

    counts = {"created": 0, "cached": 0, "skipped": 0, "excluded": 0}
    for row_number, row in enumerate(_progress(rows, len(rows)), start=1):
        status, reason = _process_row(row, row_number, manifest_path, output_dir)
        counts[status] += 1
        if status == "excluded":
            LOGGER.info("Excluding row %d: %s", row_number, reason)
    return counts


def main() -> None:
    """Parse paths and create the processed-volume cache."""
    parser = argparse.ArgumentParser(description=__doc__)
    root = repository_root()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=root / "data" / "manifest_lymphoma.csv",
        help="Filtered lymphoma CSV manifest.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "data" / "processed",
        help="Directory for per-subject NPZ caches.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    counts = make_cache(args.manifest, args.output_dir)
    LOGGER.info(
        "Cache complete: %(created)d created, %(cached)d already cached, "
        "%(skipped)d failed QC/processing, %(excluded)d excluded by manifest.",
        counts,
    )


if __name__ == "__main__":
    main()
