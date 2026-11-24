"""Selección de muestra estratificada por diagnóstico (T07)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from lymphoma.data.manifest import (
    ensure_unique_study_ids,
    normalize_diagnosis,
    study_id_from_file_location,
)

DEFAULT_SEED = 42
DEFAULT_N = 60

# Reparto objetivo de la muestra (T07): solo linfoma y controles negativos.
# Melanoma y lung_cancer no se descargan: T08 solo necesita excluirlos si
# aparecieran, y el plan experimental entrena exclusivamente con linfoma.
DEFAULT_FRACTIONS: dict[str, float] = {
    "lymphoma": 0.80,
    "negative": 0.20,
}

REQUIRED_COLUMNS = ("Subject ID", "Study Date", "diagnosis", "File Location")

SAMPLE_COLUMNS = ("patient_id", "study_id", "diagnosis", "date")


def load_metadata(path: Path) -> pd.DataFrame:
    """Carga el CSV clínico conservando identificadores como texto."""
    data = pd.read_csv(path, dtype={"Subject ID": "string", "Study UID": "string"})
    missing = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {path}: {', '.join(sorted(missing))}")
    return data


def baseline_studies(data: pd.DataFrame) -> pd.DataFrame:
    """Un estudio baseline (fecha más antigua) por paciente con diagnóstico."""
    frame = data.copy()
    frame["patient_id"] = frame["Subject ID"].astype("string").str.strip()
    frame["diagnosis_norm"] = frame["diagnosis"].map(normalize_diagnosis)
    frame["study_date"] = pd.to_datetime(frame["Study Date"], errors="coerce")
    frame = frame[frame["patient_id"].notna() & frame["patient_id"].ne("")]
    frame = frame[frame["diagnosis_norm"].ne("")]
    frame = frame.sort_values(
        ["patient_id", "study_date"], ascending=[True, True], na_position="last"
    )
    with_date = frame[frame["study_date"].notna()]
    picked = with_date.groupby("patient_id", sort=False).head(1)
    return picked.reset_index(drop=True)


def stratified_sample(
    studies: pd.DataFrame,
    n: int,
    fractions: dict[str, float],
    seed: int,
) -> pd.DataFrame:
    """Muestreo estratificado por ``diagnosis_norm`` con semilla fija."""
    rng = np.random.default_rng(seed)
    total_frac = sum(fractions.values())
    if total_frac <= 0:
        raise ValueError("Las fracciones deben sumar > 0")
    norms = {k: v / total_frac for k, v in fractions.items()}

    counts = studies["diagnosis_norm"].value_counts().to_dict()
    quotas: dict[str, int] = {}
    assigned = 0
    for label, frac in norms.items():
        want = int(round(n * frac))
        avail = int(counts.get(label, 0))
        take = min(want, avail)
        quotas[label] = take
        assigned += take

    while assigned < n:
        remaining = [
            label for label in norms if counts.get(label, 0) > quotas.get(label, 0)
        ]
        if not remaining:
            break
        label = max(remaining, key=lambda k: counts.get(k, 0) - quotas.get(k, 0))
        quotas[label] = quotas.get(label, 0) + 1
        assigned += 1

    while assigned > n:
        over = [k for k, v in quotas.items() if v > 0]
        if not over:
            break
        label = max(over, key=lambda k: quotas[k])
        quotas[label] -= 1
        assigned -= 1

    parts: list[pd.DataFrame] = []
    for label, k in quotas.items():
        if k <= 0:
            continue
        group = studies[studies["diagnosis_norm"] == label]
        idx = rng.choice(len(group), size=k, replace=False)
        parts.append(group.iloc[sorted(idx)])
    if not parts:
        raise ValueError("La muestra quedó vacía; revisa metadata y fracciones.")
    sample = pd.concat(parts, ignore_index=True)
    return sample.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def to_sample_ids(studies: pd.DataFrame) -> pd.DataFrame:
    """Convierte baseline studies al formato ``data/sample_ids.csv``."""
    rows: list[dict[str, object]] = []
    for _, row in studies.iterrows():
        patient_id = str(row["patient_id"])
        study_id = study_id_from_file_location(patient_id, row.get("File Location"))
        date = row["study_date"]
        date_str = "" if pd.isna(date) else pd.Timestamp(date).strftime("%Y-%m-%d")
        rows.append(
            {
                "patient_id": patient_id,
                "study_id": study_id,
                "diagnosis": row["diagnosis_norm"],
                "date": date_str,
            }
        )
    unique = ensure_unique_study_ids(rows)
    for rec, sid in zip(rows, unique):
        rec["study_id"] = sid
    return pd.DataFrame(rows, columns=list(SAMPLE_COLUMNS))


def select_sample(
    metadata_path: Path,
    n: int = DEFAULT_N,
    seed: int = DEFAULT_SEED,
    fractions: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Pipeline completo: metadata → baseline por paciente → muestra estratificada."""
    data = load_metadata(metadata_path)
    studies = baseline_studies(data)
    sample = stratified_sample(studies, n, fractions or DEFAULT_FRACTIONS, seed)
    return to_sample_ids(sample)
