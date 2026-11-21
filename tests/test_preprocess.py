import nibabel as nib
import numpy as np

from lymphoma.data.preprocess import (
    apply_log1p,
    convert_to_suv,
    preprocess_pet,
    robust_scale,
)


def test_apply_log1p_returns_finite_values_for_skewed_pet():
    pet = np.ones((8, 8, 8), dtype=np.float32)
    pet[0, 0, 0] = 100_000

    transformed = apply_log1p(pet)

    assert np.isfinite(transformed).all()
    assert transformed[0, 0, 0] == np.log1p(100_000)
    assert transformed[1, 1, 1] == np.log1p(1)


def test_robust_scale_clips_percentile_outliers():
    values = np.arange(100, dtype=np.float64).reshape(10, 10, 1)
    values[0, 0, 0] = -1000
    values[-1, -1, 0] = 100_000

    scaled = robust_scale(values, lower_percentile=10, upper_percentile=90)

    assert np.isfinite(scaled).all()
    assert scaled.min() == 0
    assert scaled.max() == 1
    assert scaled[0, 0, 0] == 0
    assert scaled[-1, -1, 0] == 1
    assert np.all((scaled >= 0) & (scaled <= 1))


def test_convert_to_suv_uses_weight_and_decay_adjusted_dose():
    raw_pet = np.full((2, 2, 2), 100.0)

    suv = convert_to_suv(
        raw_pet,
        patient_weight_kg=70,
        injected_dose_bq=350_000_000,
        elapsed_seconds=60,
        half_life_seconds=120,
    )

    dose_at_scan = 350_000_000 * np.exp(-np.log(2) * 60 / 120)
    assert np.allclose(suv, 100 * 70_000 / dose_at_scan)


def test_preprocess_saves_original_suv_before_intensity_transforms(tmp_path):
    original_suv = np.ones((8, 8, 8), dtype=np.float32)
    original_suv[0, 0, 0] = 100_000
    affine = np.diag([2, 2, 2, 1])
    input_path = tmp_path / "source_pet.nii.gz"
    nib.save(nib.Nifti1Image(original_suv, affine), str(input_path))

    pet_path = tmp_path / "processed" / "pet.nii.gz"
    suv_path = tmp_path / "processed" / "suv.nii.gz"
    preprocess_pet(input_path, pet_path, suv_path, is_suv=True)

    saved_suv = nib.load(str(suv_path))
    saved_pet = nib.load(str(pet_path))
    assert np.array_equal(np.asanyarray(saved_suv.dataobj), original_suv)
    assert np.allclose(saved_suv.affine, affine)
    assert np.all((np.asanyarray(saved_pet.dataobj) >= 0) & (
        np.asanyarray(saved_pet.dataobj) <= 1
    ))


def test_preprocess_requires_conversion_metadata_for_raw_pet(tmp_path):
    input_path = tmp_path / "raw_pet.nii.gz"
    nib.save(nib.Nifti1Image(np.ones((4, 4, 4)), np.eye(4)), str(input_path))

    try:
        preprocess_pet(
            input_path,
            tmp_path / "pet.nii.gz",
            tmp_path / "suv.nii.gz",
            is_suv=False,
        )
    except ValueError as error:
        assert "patient_weight_kg and injected_dose_bq" in str(error)
    else:
        raise AssertionError("Raw PET without dose metadata should fail.")
