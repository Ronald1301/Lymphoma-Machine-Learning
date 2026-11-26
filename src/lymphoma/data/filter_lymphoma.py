"""Filter the clinical metadata to one baseline lymphoma study per patient."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ("Subject ID", "Study UID", "Study Date", "diagnosis")
INPUT_FILENAME = "Clinical-Metadata-FDG-PET_CT-Lesions.csv"


def repository_root() -> Path:
    """Return the repository root based on this file's location."""
    return Path(__file__).resolve().parents[3]


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load metadata while preserving patient and study identifiers as text."""
    data = pd.read_csv(
        csv_path,
        dtype={"Subject ID": "string", "Study UID": "string"},
    )
    missing_columns = set(REQUIRED_COLUMNS).difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input CSV is missing required columns: {missing}")
    return data


def filter_lymphoma(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keep the oldest dated lymphoma study per patient and explain exclusions."""
    missing_columns = set(REQUIRED_COLUMNS).difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input data is missing required columns: {missing}")

    diagnosis = data["diagnosis"].astype("string").str.strip()
    is_lymphoma = diagnosis.str.upper().eq("LYMPHOMA").fillna(False)
    subject_id = data["Subject ID"].astype("string").str.strip()
    subject_id = subject_id.mask(subject_id.eq(""))
    study_date = pd.to_datetime(data["Study Date"], errors="coerce", utc=True)

    reasons = pd.Series(pd.NA, index=data.index, dtype="string")
    not_lymphoma = ~is_lymphoma
    diagnosis_label = diagnosis.fillna("").str.strip()
    reasons.loc[not_lymphoma] = diagnosis_label.loc[not_lymphoma].map(
        lambda value: (
            f"Not lymphoma (is {value})"
            if value
            else "Not lymphoma (missing diagnosis)"
        )
    )

    missing_subject = is_lymphoma & subject_id.isna()
    reasons.loc[missing_subject] = "Missing Subject ID; baseline cannot be determined"

    eligible = is_lymphoma & subject_id.notna()
    lymphoma_rows = data.loc[eligible]
    lymphoma_dates = study_date.loc[eligible]

    for _, patient_rows in lymphoma_rows.groupby(subject_id.loc[eligible], sort=False):
        patient_dates = lymphoma_dates.loc[patient_rows.index]
        undated_indices = patient_dates.index[patient_dates.isna()]
        reasons.loc[undated_indices] = (
            "Missing or invalid Study Date; baseline cannot be determined"
        )

        dated_indices = patient_dates.index[patient_dates.notna()]
        if len(dated_indices) == 0:
            continue

        earliest_date = patient_dates.loc[dated_indices].min()
        baseline_index = next(
            index
            for index in dated_indices
            if patient_dates.loc[index] == earliest_date
        )
        reasons.loc[dated_indices] = "Not baseline study"
        reasons.loc[baseline_index] = pd.NA

    included = data.loc[reasons.isna()].copy()
    excluded = data.loc[reasons.notna()].copy()
    excluded["exclusion_reason"] = reasons.loc[reasons.notna()]
    return included, excluded


def save_results(
    manifest: pd.DataFrame,
    exclusion_log: pd.DataFrame,
    results_dir: Path,
) -> tuple[Path, Path]:
    """Write the filtered manifest and exclusion log to the results directory."""
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = results_dir / "manifest_lymphoma.csv"
    exclusion_path = results_dir / "exclusion_log.csv"
    manifest.to_csv(manifest_path, index=False, encoding="utf-8")
    exclusion_log.to_csv(exclusion_path, index=False, encoding="utf-8")
    return manifest_path, exclusion_path


def parse_args() -> argparse.Namespace:
    """Parse optional input and output paths."""
    root = repository_root()
    parser = argparse.ArgumentParser(
        description="Keep the oldest lymphoma study for each patient."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "results" / INPUT_FILENAME,
        help=(
            "Metadata CSV path "
            f"(default: results/{INPUT_FILENAME}, relative to the repository root)"
        ),
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=root / "results",
        help="Directory for generated CSV files (default: repository results/).",
    )
    return parser.parse_args()


def main() -> None:
    """Run filtering, save outputs, and print patient and study counts."""
    args = parse_args()
    manifest, exclusion_log = filter_lymphoma(load_data(args.input))
    manifest_path, exclusion_path = save_results(
        manifest, exclusion_log, args.results_dir
    )

    patient_count = manifest["Subject ID"].nunique()
    study_count = manifest["Study UID"].nunique()
    print(f"Unique lymphoma patients (Subject ID): {patient_count}")
    print(f"Baseline lymphoma studies (unique Study UID): {study_count}")
    print(f"Manifest saved to: {manifest_path}")
    print(f"Exclusion log saved to: {exclusion_path}")


if __name__ == "__main__":
    main()
