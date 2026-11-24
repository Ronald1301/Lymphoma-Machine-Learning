"""Tests del muestreo estratificado (T07) con metadata sintética."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from lymphoma.data.sample import (
    baseline_studies,
    select_sample,
    stratified_sample,
    to_sample_ids,
)


def _metadata_frame() -> pd.DataFrame:
    rows = []
    for diagnosis in ["LYMPHOMA", "MELANOMA", "LUNG_CANCER", "NEGATIVE"]:
        for j in range(10):
            patient = f"PETCT_{diagnosis[:3]}{j:02d}"
            year = 2000 + j
            rows.append(
                {
                    "Subject ID": patient,
                    "Study UID": f"uid-{patient}-1",
                    "Study Date": f"{year}-01-01",
                    "diagnosis": diagnosis,
                    "File Location": (
                        f"./FDG-PET-CT-Lesions/{patient}/"
                        f"{year}-01-01-NA-study-{1000 + j}/series-1"
                    ),
                }
            )
            rows.append(
                {
                    "Subject ID": patient,
                    "Study UID": f"uid-{patient}-2",
                    "Study Date": f"{year + 5}-06-15",
                    "diagnosis": diagnosis,
                    "File Location": (
                        f"./FDG-PET-CT-Lesions/{patient}/"
                        f"{year + 5}-06-15-NA-study-{2000 + j}/series-2"
                    ),
                }
            )
    return pd.DataFrame(rows)


def test_baseline_studies_one_row_per_patient():
    studies = baseline_studies(_metadata_frame())
    assert len(studies) == 40
    assert studies["patient_id"].is_unique
    first = studies[studies["patient_id"] == "PETCT_LYM00"].iloc[0]
    assert pd.Timestamp(first["study_date"]).year == 2000


def test_stratified_sample_respects_seed_and_counts():
    studies = baseline_studies(_metadata_frame())
    fractions = {
        "lymphoma": 0.40,
        "melanoma": 0.20,
        "lung_cancer": 0.20,
        "negative": 0.20,
    }
    a = stratified_sample(studies, 16, fractions, seed=42)
    b = stratified_sample(studies, 16, fractions, seed=42)
    assert a["patient_id"].tolist() == b["patient_id"].tolist()
    counts = a["diagnosis_norm"].value_counts().to_dict()
    assert counts["lymphoma"] == 6
    assert sum(counts.values()) == 16


def test_to_sample_ids_columns_and_study_id():
    studies = baseline_studies(_metadata_frame()).head(3)
    sample = to_sample_ids(studies)
    assert list(sample.columns) == ["patient_id", "study_id", "diagnosis", "date"]
    assert sample["study_id"].str.contains("_").all()
    assert sample["study_id"].is_unique
    assert sample["date"].str.match(r"\d{4}-\d{2}-\d{2}").all()


def test_select_sample_from_csv(tmp_path: Path):
    path = tmp_path / "meta.csv"
    _metadata_frame().to_csv(path, index=False)
    sample = select_sample(path, n=10, seed=42)
    assert len(sample) == 10
    counts = sample["diagnosis"].value_counts().to_dict()
    assert counts == {"lymphoma": 8, "negative": 2}
