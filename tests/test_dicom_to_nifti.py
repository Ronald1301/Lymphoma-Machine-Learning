import csv
import json
from pathlib import Path
from types import SimpleNamespace

import nibabel as nib
import numpy as np

from lymphoma.data import dicom_to_nifti


def _write_manifest(path, rows):
    columns = [
        "Subject ID",
        "Study UID",
        "File Location",
        "Modality",
        "Series Description",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def test_convert_manifest_groups_modalities_and_updates_paths(tmp_path, monkeypatch):
    subject_id = "patient-1"
    study_uid = "study-1"
    series = []
    for modality in ("PT", "CT", "SEG"):
        directory = tmp_path / "dicom" / modality
        directory.mkdir(parents=True)
        (directory / "image.dcm").touch()
        series.append(
            {
                "Subject ID": subject_id,
                "Study UID": study_uid,
                "File Location": str(directory),
                "Modality": modality,
                "Series Description": (
                    "Segmentation" if modality == "SEG" else modality
                ),
            }
        )

    def fake_run(command, **_kwargs):
        output_directory = tmp_path / command[command.index("-o") + 1]
        dicom_directory = tmp_path / command[-1]
        output_directory.mkdir(parents=True, exist_ok=True)
        nifti_path = output_directory / "converted.nii.gz"
        image = nib.Nifti1Image(np.ones((4, 4, 4), dtype=np.uint8), np.eye(4))
        nib.save(image, nifti_path)
        (output_directory / "converted.json").write_text(
            json.dumps({"Modality": dicom_directory.name}),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(dicom_to_nifti.subprocess, "run", fake_run)
    selected_manifest = tmp_path / "manifest_lymphoma.csv"
    source_manifest = tmp_path / "all_series.csv"
    output_manifest = tmp_path / "manifest_lymphoma_nifti.csv"
    _write_manifest(selected_manifest, [series[0]])
    _write_manifest(source_manifest, series)

    successful, failed = dicom_to_nifti.convert_manifest(
        selected_manifest,
        output_manifest,
        tmp_path / "data" / "nifti",
        source_manifest=source_manifest,
        dcm2niix="mock-dcm2niix",
    )

    assert (successful, failed) == (1, 0)
    with output_manifest.open(newline="", encoding="utf-8") as file:
        result = next(csv.DictReader(file))
    for column in ("pet_path", "ct_path", "mask_path"):
        assert Path(result[column]).is_file()
    assert result["Subject ID"] == subject_id
    assert result["Study UID"] == study_uid
    assert result["nifti_conversion_error"] == ""


def test_classification_uses_converted_sidecar_before_manifest_metadata():
    modality = dicom_to_nifti._classify_series(
        {"Modality": "CT"},
        {"Modality": "PT", "Series Description": "PET"},
    )

    assert modality == "ct"
