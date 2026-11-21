"""PET SUV conversion and robust intensity preprocessing."""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]
FLUORINE_18_HALF_LIFE_SECONDS = 6586.2


def _validated_pet_data(pet_data: NDArray[np.generic]) -> FloatArray:
    data = np.asarray(pet_data, dtype=np.float64)
    if data.ndim != 3:
        raise ValueError(f"PET data must be 3D; got {data.ndim} dimensions.")
    if not np.all(np.isfinite(data)):
        raise ValueError("PET data must contain only finite values.")
    return data


def convert_to_suv(
    pet_data: NDArray[np.generic],
    patient_weight_kg: float,
    injected_dose_bq: float,
    *,
    elapsed_seconds: float = 0.0,
    half_life_seconds: float = FLUORINE_18_HALF_LIFE_SECONDS,
) -> FloatArray:
    """Convert Bq/mL to body-weight SUV using dose decayed to scan time.

    The input activity concentration is assumed to be referenced to scan time;
    injected dose is assumed to be recorded at injection time.
    """
    data = _validated_pet_data(pet_data)
    if np.any(data < 0):
        raise ValueError("Raw PET activity must be non-negative.")
    if not np.isfinite(patient_weight_kg) or patient_weight_kg <= 0:
        raise ValueError("Patient weight must be a positive finite value in kg.")
    if not np.isfinite(injected_dose_bq) or injected_dose_bq <= 0:
        raise ValueError("Injected dose must be a positive finite value in Bq.")
    if not np.isfinite(elapsed_seconds) or elapsed_seconds < 0:
        raise ValueError("Elapsed time must be a non-negative finite value in seconds.")
    if not np.isfinite(half_life_seconds) or half_life_seconds <= 0:
        raise ValueError("Half-life must be a positive finite value in seconds.")

    dose_at_scan = injected_dose_bq * np.exp(
        -np.log(2) * elapsed_seconds / half_life_seconds
    )
    if not np.isfinite(dose_at_scan) or dose_at_scan <= 0:
        raise ValueError("Injected dose decayed to an invalid value at scan time.")
    weight_grams = patient_weight_kg * 1000
    with np.errstate(over="ignore", invalid="ignore"):
        suv_data = data * weight_grams / dose_at_scan
    if not np.all(np.isfinite(suv_data)):
        raise ValueError("SUV conversion produced non-finite values.")
    return suv_data


def apply_log1p(suv_data: NDArray[np.generic]) -> FloatArray:
    """Apply log1p to finite, non-negative SUV values."""
    data = _validated_pet_data(suv_data)
    if np.any(data < 0):
        raise ValueError("SUV values must be non-negative for log1p preprocessing.")
    return np.log1p(data)


def robust_scale(
    data: NDArray[np.generic],
    lower_percentile: float = 1.0,
    upper_percentile: float = 99.0,
) -> FloatArray:
    """Clip data to percentile bounds and scale it to [0, 1]."""
    values = _validated_pet_data(data)
    if (
        not np.isfinite(lower_percentile)
        or not np.isfinite(upper_percentile)
        or lower_percentile < 0
        or upper_percentile > 100
        or lower_percentile >= upper_percentile
    ):
        raise ValueError("Percentiles must satisfy 0 <= lower < upper <= 100.")

    lower, upper = np.percentile(values, [lower_percentile, upper_percentile])
    if upper <= lower:
        return np.zeros_like(values)
    clipped = np.clip(values, lower, upper)
    return (clipped - lower) / (upper - lower)


def _load_nifti(input_path: Path):
    try:
        import nibabel as nib
    except ImportError as error:
        raise ImportError("PET NIfTI preprocessing requires nibabel.") from error
    image = nib.load(str(input_path))
    data = np.asanyarray(image.dataobj)
    return nib, image, data


def _save_nifti(data: FloatArray, reference_image, output_path: Path) -> None:
    import nibabel as nib

    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = reference_image.header.copy()
    header.set_data_dtype(np.float32)
    image = nib.Nifti1Image(
        data.astype(np.float32),
        affine=reference_image.affine,
        header=header,
    )
    nib.save(image, str(output_path))


def preprocess_pet(
    input_path: Path,
    pet_output_path: Path,
    suv_output_path: Path,
    *,
    is_suv: bool,
    patient_weight_kg: float | None = None,
    injected_dose_bq: float | None = None,
    elapsed_seconds: float = 0.0,
    half_life_seconds: float = FLUORINE_18_HALF_LIFE_SECONDS,
    lower_percentile: float = 1.0,
    upper_percentile: float = 99.0,
) -> tuple[Path, Path]:
    """Save original SUV and log1p/robust-scaled PET NIfTI volumes."""
    input_path = Path(input_path)
    nib, source_image, source_data = _load_nifti(input_path)
    source_data = _validated_pet_data(source_data)

    if is_suv:
        suv_data = source_data
    else:
        if patient_weight_kg is None or injected_dose_bq is None:
            raise ValueError(
                "Raw PET conversion requires patient_weight_kg and injected_dose_bq."
            )
        suv_data = convert_to_suv(
            source_data,
            patient_weight_kg,
            injected_dose_bq,
            elapsed_seconds=elapsed_seconds,
            half_life_seconds=half_life_seconds,
        )

    pet_data = robust_scale(
        apply_log1p(suv_data),
        lower_percentile=lower_percentile,
        upper_percentile=upper_percentile,
    )
    pet_output_path = Path(pet_output_path)
    suv_output_path = Path(suv_output_path)
    _save_nifti(suv_data, source_image, suv_output_path)
    _save_nifti(pet_data, source_image, pet_output_path)
    return pet_output_path, suv_output_path


def main() -> None:
    """Run PET preprocessing from the command line or demonstrate it on dummy data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="Input PET NIfTI path")
    parser.add_argument("--pet-output", type=Path, help="Output normalized PET NIfTI")
    parser.add_argument("--suv-output", type=Path, help="Output original SUV NIfTI")
    parser.add_argument(
        "--is-suv",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Declare input already in SUV units (default: true)",
    )
    parser.add_argument("--patient-weight-kg", type=float)
    parser.add_argument("--injected-dose-bq", type=float)
    parser.add_argument("--elapsed-seconds", type=float, default=0.0)
    parser.add_argument(
        "--half-life-seconds",
        type=float,
        default=FLUORINE_18_HALF_LIFE_SECONDS,
    )
    args = parser.parse_args()

    if args.input is None:
        import nibabel as nib

        with tempfile.TemporaryDirectory() as temp_dir:
            demo_dir = Path(temp_dir)
            input_path = demo_dir / "dummy_pet.nii.gz"
            nib.save(
                nib.Nifti1Image(np.ones((8, 8, 8), dtype=np.float32), np.eye(4)),
                str(input_path),
            )
            outputs = preprocess_pet(
                input_path,
                demo_dir / "pet.nii.gz",
                demo_dir / "suv.nii.gz",
                is_suv=True,
            )
            print(f"Dummy outputs: {outputs[0]} and {outputs[1]}")
        return

    if args.pet_output is None or args.suv_output is None:
        parser.error("--pet-output and --suv-output are required when input is provided.")
    outputs = preprocess_pet(
        args.input,
        args.pet_output,
        args.suv_output,
        is_suv=args.is_suv,
        patient_weight_kg=args.patient_weight_kg,
        injected_dose_bq=args.injected_dose_bq,
        elapsed_seconds=args.elapsed_seconds,
        half_life_seconds=args.half_life_seconds,
    )
    print(f"Preprocessed PET: {outputs[0]}")
    print(f"Original SUV: {outputs[1]}")


if __name__ == "__main__":
    main()
