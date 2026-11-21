import csv

import nibabel as nib
import numpy as np

from lymphoma.data.quality_control import (
    QCResult,
    Study,
    check_geometry,
    check_mask,
    check_pairing,
    generate_report,
    load_studies,
)


def _save_nifti(path, data, affine=None):
    image = nib.Nifti1Image(data, np.eye(4) if affine is None else affine)
    nib.save(image, str(path))
    return path


def test_check_pairing_fails_when_either_image_is_missing(tmp_path):
    pet_path = _save_nifti(tmp_path / "pet.nii.gz", np.ones((8, 8, 8)))
    ct_path = _save_nifti(tmp_path / "ct.nii.gz", np.ones((8, 8, 8)))

    assert check_pairing(pet_path, ct_path)
    assert not check_pairing(tmp_path / "missing_pet.nii.gz", ct_path)
    assert not check_pairing(pet_path, tmp_path / "missing_ct.nii.gz")


def test_check_geometry_flags_different_spacing(tmp_path):
    pet_affine = np.eye(4)
    ct_affine = np.diag([2, 1, 1, 1])
    pet_path = _save_nifti(tmp_path / "pet.nii.gz", np.ones((8, 8, 8)), pet_affine)
    ct_path = _save_nifti(tmp_path / "ct.nii.gz", np.ones((8, 8, 8)), ct_affine)

    assert not check_geometry(pet_path, ct_path)


def test_check_geometry_flags_different_orientation(tmp_path):
    pet_affine = np.eye(4)
    ct_affine = np.diag([-1, 1, 1, 1])
    pet_path = _save_nifti(tmp_path / "pet.nii.gz", np.ones((8, 8, 8)), pet_affine)
    ct_path = _save_nifti(tmp_path / "ct.nii.gz", np.ones((8, 8, 8)), ct_affine)

    assert not check_geometry(pet_path, ct_path)


def test_check_mask_rejects_empty_and_accepts_nonempty_masks(tmp_path):
    empty_path = _save_nifti(tmp_path / "empty.nii.gz", np.zeros((8, 8, 8)))
    nonempty_data = np.zeros((8, 8, 8))
    nonempty_data[3, 4, 5] = 1
    nonempty_path = _save_nifti(tmp_path / "nonempty.nii.gz", nonempty_data)

    assert not check_mask(empty_path)
    assert check_mask(nonempty_path)
    assert not check_mask(tmp_path / "missing_mask.nii.gz")


def test_check_mask_rejects_corrupted_file(tmp_path):
    corrupted_path = tmp_path / "corrupted.nii.gz"
    corrupted_path.write_bytes(b"not a NIfTI image")

    assert not check_mask(corrupted_path)


def test_generate_report_includes_exclusion_reasons(tmp_path):
    study = Study("study-1", "patient-1", None, None, None)
    report_path = tmp_path / "results" / "qc_report.md"

    generate_report([QCResult(study, ["Missing PET", "Empty mask"])], report_path)

    report = report_path.read_text(encoding="utf-8")
    assert report_path.is_file()
    assert "study-1" in report
    assert "Missing PET" in report
    assert "Empty mask" in report


def test_load_studies_from_csv_manifest(tmp_path):
    manifest_path = tmp_path / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["patient_id", "study_id", "pet_path", "ct_path", "mask_path"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "patient_id": "patient-1",
                "study_id": "study-1",
                "pet_path": "pet.nii.gz",
                "ct_path": "ct.nii.gz",
                "mask_path": "mask.nii.gz",
            }
        )

    study = load_studies(manifest_path)[0]

    assert study.study_id == "study-1"
    assert study.pet_path == tmp_path / "pet.nii.gz"
    assert study.ct_path == tmp_path / "ct.nii.gz"
    assert study.mask_path == tmp_path / "mask.nii.gz"


def test_load_studies_from_per_study_directory(tmp_path):
    study_dir = tmp_path / "patient-1" / "study-1"
    study_dir.mkdir(parents=True)
    pet_path = _save_nifti(study_dir / "SUV.nii.gz", np.ones((8, 8, 8)))
    ct_path = _save_nifti(study_dir / "CTres.nii.gz", np.ones((8, 8, 8)))
    mask_path = _save_nifti(study_dir / "SEG.nii.gz", np.ones((8, 8, 8)))

    study = load_studies(tmp_path)[0]

    assert study.study_id == "study-1"
    assert study.patient_id == "patient-1"
    assert study.pet_path == pet_path
    assert study.ct_path == ct_path
    assert study.mask_path == mask_path
