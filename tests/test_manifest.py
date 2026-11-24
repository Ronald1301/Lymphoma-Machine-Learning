"""Tests del manifiesto T07 con casos construidos a mano."""

from __future__ import annotations

from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
import pytest

from lymphoma.data.manifest import (
    MANIFEST_COLUMNS,
    build_manifest,
    count_lesions,
    derive_study_id,
    ensure_unique_study_ids,
    normalize_diagnosis,
    study_id_from_file_location,
    tmtv_ml,
    write_manifest,
)


def test_normalize_diagnosis_vocabulary():
    assert normalize_diagnosis("LYMPHOMA") == "lymphoma"
    assert normalize_diagnosis("Melanoma") == "melanoma"
    assert normalize_diagnosis("LUNG_CANCER") == "lung_cancer"
    assert normalize_diagnosis("lung cancer") == "lung_cancer"
    assert normalize_diagnosis("NEGATIVE") == "negative"
    assert normalize_diagnosis("") == ""
    assert normalize_diagnosis(None) == ""


def test_count_lesions_two_separate_cubes():
    mask = np.zeros((20, 20, 20), dtype=np.uint8)
    mask[2:5, 2:5, 2:5] = 1
    mask[12:15, 12:15, 12:15] = 1
    assert count_lesions(mask) == 2


def test_count_lesions_diagonal_is_one_with_26_connectivity():
    # Dos vóxeles solo en esquina compartida: 26-conectados → 1 componente.
    mask = np.zeros((5, 5, 5), dtype=np.uint8)
    mask[1, 1, 1] = 1
    mask[2, 2, 2] = 1
    assert count_lesions(mask) == 1


def test_count_lesions_face_neighbors_one_component():
    mask = np.zeros((6, 6, 6), dtype=np.uint8)
    mask[1:3, 1:3, 1:3] = 1
    mask[3:5, 1:3, 1:3] = 1  # comparte cara con el primero
    assert count_lesions(mask) == 1


def test_count_lesions_empty_is_zero():
    assert count_lesions(np.zeros((4, 4, 4), dtype=np.uint8)) == 0


def test_tmtv_ml_uses_voxel_volume():
    # 1000 vóxeles de 3 mm isotrópicos = 1000 * 0.027 mL = 27 mL
    mask = np.ones((10, 10, 10), dtype=np.uint8)
    assert tmtv_ml(mask, (3.0, 3.0, 3.0)) == pytest.approx(27.0)


def test_tmtv_ml_empty_mask_is_zero():
    assert tmtv_ml(np.zeros((3, 3, 3)), (3.0, 3.0, 3.0)) == 0.0


def test_tmtv_ml_rejects_bad_spacing():
    with pytest.raises(ValueError):
        tmtv_ml(np.ones((2, 2, 2)), (3.0, 3.0))


def test_derive_study_id_uses_trailing_number():
    patient = "PETCT_0011f3deaf"
    folder = "03-23-2003-NA-PET-CT Ganzkoerper  primaer mit KM-10445"
    assert derive_study_id(patient, folder) == "PETCT_0011f3deaf_10445"


def test_derive_study_id_without_digits_keeps_folder():
    assert derive_study_id("PETCT_abc", "StudyA") == "PETCT_abc_StudyA"


def test_study_id_from_file_location():
    loc = (
        "./FDG-PET-CT-Lesions/PETCT_0011f3deaf/"
        "03-23-2003-NA-PET-CT Ganzkoerper  primaer mit KM-10445/"
        "7.000000-PET corr.-19181"
    )
    assert (
        study_id_from_file_location("PETCT_0011f3deaf", loc)
        == "PETCT_0011f3deaf_10445"
    )


def test_ensure_unique_study_ids_appends_suffix():
    rows = [
        {"study_id": "P_1"},
        {"study_id": "P_1"},
        {"study_id": "P_2"},
    ]
    assert ensure_unique_study_ids(rows) == ["P_1", "P_1_01", "P_2"]


def _write_study(raw: Path, patient: str, study: str, lesion: bool) -> None:
    study_dir = raw / patient / study
    study_dir.mkdir(parents=True, exist_ok=True)
    shape = (8, 8, 8)
    affine = np.eye(4)
    affine[:3, :3] *= 3.0  # 3 mm
    for name in ("SUV.nii.gz", "CTres.nii.gz"):
        nib.save(nib.Nifti1Image(np.zeros(shape, dtype=np.float32), affine), str(study_dir / name))
    mask = np.zeros(shape, dtype=np.uint8)
    if lesion:
        mask[1:3, 1:3, 1:3] = 1
        mask[5:7, 5:7, 5:7] = 1
    nib.save(nib.Nifti1Image(mask, affine), str(study_dir / "SEG.nii.gz"))


def test_build_manifest_with_files(tmp_path: Path):
    raw = tmp_path / "data" / "raw"
    _write_study(raw, "PETCT_aaa", "study-10445", lesion=True)
    sample = pd.DataFrame(
        [
            {
                "patient_id": "PETCT_aaa",
                "study_id": "PETCT_aaa_10445",
                "diagnosis": "lymphoma",
                "date": "2003-03-23",
            }
        ]
    )
    frame = build_manifest(raw, sample, repo_root=tmp_path)
    assert list(frame.columns) == list(MANIFEST_COLUMNS)
    row = frame.iloc[0]
    assert row["patient_id"] == "PETCT_aaa"
    assert row["study_id"] == "PETCT_aaa_10445"
    assert row["diagnosis"] == "lymphoma"
    assert row["date"] == "2003-03-23"
    assert row["pet_path"].endswith("SUV.nii.gz")
    assert row["pet_path"].startswith("data/raw/")
    assert "/" in row["pet_path"] and "\\" not in row["pet_path"]
    assert row["ct_path"].endswith("CTres.nii.gz")
    assert row["mask_path"].endswith("SEG.nii.gz")
    assert bool(row["suv_available"]) is True
    assert int(row["n_lesions"]) == 2
    assert float(row["tmtv_ml"]) == pytest.approx(2 * 8 * 0.027)
    assert bool(row["include"]) is True
    assert row["exclude_reason"] == ""


def test_build_manifest_missing_files_leaves_metrics_empty(tmp_path: Path):
    sample = pd.DataFrame(
        [
            {
                "patient_id": "PETCT_missing",
                "study_id": "PETCT_missing_1",
                "diagnosis": "negative",
                "date": "2020-01-01",
            }
        ]
    )
    frame = build_manifest(tmp_path / "nope", sample, repo_root=tmp_path)
    row = frame.iloc[0]
    assert row["pet_path"] == ""
    assert row["n_lesions"] == ""
    assert row["tmtv_ml"] == ""
    assert bool(row["suv_available"]) is False


def test_write_manifest_boolean_format(tmp_path: Path):
    frame = pd.DataFrame(
        [
            {
                "patient_id": "p",
                "study_id": "p_1",
                "diagnosis": "lymphoma",
                "date": "2001-01-01",
                "pet_path": "",
                "ct_path": "",
                "mask_path": "",
                "suv_available": True,
                "n_lesions": 0,
                "tmtv_ml": 0.0,
                "include": True,
                "exclude_reason": "",
            },
            {
                "patient_id": "q",
                "study_id": "q_1",
                "diagnosis": "melanoma",
                "date": "",
                "pet_path": "",
                "ct_path": "",
                "mask_path": "",
                "suv_available": False,
                "n_lesions": "",
                "tmtv_ml": "",
                "include": False,
                "exclude_reason": "missing",
            },
        ],
        columns=list(MANIFEST_COLUMNS),
    )
    out = tmp_path / "manifest.csv"
    write_manifest(frame, out)
    text = out.read_text(encoding="utf-8")
    assert ",true," in text or text.count("true") >= 2
    assert "false" in text
    reread = pd.read_csv(out, dtype=str)
    assert list(reread.columns) == list(MANIFEST_COLUMNS)
