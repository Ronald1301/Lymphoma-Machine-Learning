"""Construcción de ``data/manifest.csv`` según el contrato de T03.

Una fila por estudio. Ver ``docs/contratos.md`` §1.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import nibabel as nib
import numpy as np
import pandas as pd
from scipy import ndimage

MANIFEST_COLUMNS: tuple[str, ...] = (
    "patient_id",
    "study_id",
    "diagnosis",
    "date",
    "pet_path",
    "ct_path",
    "mask_path",
    "suv_available",
    "n_lesions",
    "tmtv_ml",
    "include",
    "exclude_reason",
)

DIAGNOSIS_MAP: dict[str, str] = {
    "LYMPHOMA": "lymphoma",
    "MELANOMA": "melanoma",
    "LUNG_CANCER": "lung_cancer",
    "LUNG CANCER": "lung_cancer",
    "LUNG-CANCER": "lung_cancer",
    "NSCLC": "lung_cancer",
    "NEGATIVE": "negative",
}

# Conectividad 26 (regla del contrato para n_lesions).
_CONNECTIVITY_26 = np.ones((3, 3, 3), dtype=bool)


def normalize_diagnosis(raw: object) -> str:
    """Normaliza el diagnóstico de los metadatos al vocabulario del contrato."""
    if raw is None or (isinstance(raw, float) and np.isnan(raw)):
        return ""
    text = str(raw).strip()
    if not text:
        return ""
    key = text.upper().replace("-", "_").replace(" ", "_")
    if key in DIAGNOSIS_MAP:
        return DIAGNOSIS_MAP[key]
    key2 = text.upper().replace("-", " ")
    for source, target in DIAGNOSIS_MAP.items():
        if source.replace("_", " ") == key2:
            return target
    return text.lower()


def count_lesions(mask: np.ndarray) -> int:
    """Número de componentes 26-conectados del volumen binario."""
    binary = np.asarray(mask) != 0
    if not binary.any():
        return 0
    _labels, n = ndimage.label(binary, structure=_CONNECTIVITY_26)
    return int(n)


def tmtv_ml(mask: np.ndarray, spacing_mm: Iterable[float]) -> float:
    """Volumen de la máscara en mL a partir del espaciado de vóxel (mm)."""
    binary = np.asarray(mask) != 0
    spacing = tuple(float(s) for s in spacing_mm)
    if len(spacing) != 3:
        raise ValueError("spacing_mm debe tener 3 elementos (x, y, z)")
    voxel_ml = (spacing[0] * spacing[1] * spacing[2]) / 1000.0
    return float(binary.sum() * voxel_ml)


def derive_study_id(patient_id: str, study_folder: str) -> str:
    """``<patient_id>_<sufijo>``; el sufijo es el número final del nombre de carpeta.

    Si no hay número final, se usa el índice de fecha más tarde en
    ``ensure_unique_study_ids``.
    """
    digits = ""
    for ch in reversed(study_folder):
        if ch.isdigit():
            digits = ch + digits
        elif digits:
            break
    if not digits:
        return f"{patient_id}_{study_folder}"
    return f"{patient_id}_{digits}"


def ensure_unique_study_ids(rows: list[Mapping[str, object]]) -> list[str]:
    """Asigna sufijos ``_01``, ``_02``… si un ``study_id`` se repite."""
    seen: dict[str, int] = {}
    out: list[str] = []
    for row in rows:
        base = str(row["study_id"])
        if base not in seen:
            seen[base] = 0
            out.append(base)
            continue
        seen[base] += 1
        candidate = f"{base}_{seen[base]:02d}"
        while candidate in seen:
            seen[base] += 1
            candidate = f"{base}_{seen[base]:02d}"
        seen[candidate] = 0
        out.append(candidate)
    return out


def study_id_from_file_location(patient_id: str, file_location: object) -> str:
    """Deriva ``study_id`` desde ``File Location`` del CSV clínico de TCIA.

    Estructura típica:
    ``./FDG-PET-CT-Lesions/<patient_id>/<study_folder>/<series>``.
    """
    if file_location is None or (
        isinstance(file_location, float) and np.isnan(file_location)
    ):
        return patient_id
    parts = [
        p
        for p in str(file_location).replace("\\", "/").split("/")
        if p and p != "."
    ]
    # El penúltimo componente es la carpeta del estudio; el último, la serie.
    if len(parts) >= 3:
        return derive_study_id(patient_id, parts[-2])
    if len(parts) == 2:
        return derive_study_id(patient_id, parts[-1])
    return patient_id


def _rel_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _study_stats(mask_path: Path) -> tuple[int, float]:
    data = nib.load(str(mask_path))
    arr = np.asanyarray(data.dataobj)
    zooms = data.header.get_zooms()[:3]
    spacing = tuple(float(z) if float(z) > 0 else 1.0 for z in zooms)
    return count_lesions(arr), tmtv_ml(arr, spacing)


def build_manifest(
    raw_dir: Path,
    sample: pd.DataFrame,
    *,
    repo_root: Path | None = None,
) -> pd.DataFrame:
    """Une la muestra con los NIfTI bajo ``raw_dir`` y calcula métricas de la máscara.

    ``sample`` debe traer al menos ``patient_id``, ``study_id``, ``diagnosis`` y
    ``date``. Las rutas del manifiesto son relativas al repo con ``/``.
    """
    root = repo_root or Path.cwd()
    records: list[dict[str, object]] = []

    for _, row in sample.iterrows():
        patient_id = str(row["patient_id"])
        patient_dir = raw_dir / patient_id
        study_dir: Path | None = None
        if patient_dir.is_dir():
            candidates = sorted(p for p in patient_dir.iterdir() if p.is_dir())
            # Emparejar por sufijo de study_id si hay varias carpetas de estudio.
            suffix = str(row["study_id"]).removeprefix(f"{patient_id}_")
            for cand in candidates:
                if suffix and (cand.name.endswith(suffix) or suffix in cand.name):
                    study_dir = cand
                    break
            if study_dir is None and len(candidates) == 1:
                study_dir = candidates[0]
            elif study_dir is None and candidates:
                study_dir = candidates[0]

        suv: Path | None = None
        ctres: Path | None = None
        seg: Path | None = None
        if study_dir is not None:
            suv = study_dir / "SUV.nii.gz"
            ctres = study_dir / "CTres.nii.gz"
            seg = study_dir / "SEG.nii.gz"
            if not suv.is_file():
                pet = study_dir / "PET.nii.gz"
                suv = pet if pet.is_file() else None
            if not ctres.is_file():
                ct = study_dir / "CT.nii.gz"
                ctres = ct if ct.is_file() else None
            if not seg.is_file():
                seg = None

        n_lesions: object = ""
        tmtv: object = ""
        if seg is not None and seg.is_file():
            n_lesions, tmtv = _study_stats(seg)

        pet_path = _rel_posix(suv, root) if suv and suv.is_file() else ""
        ct_path = _rel_posix(ctres, root) if ctres and ctres.is_file() else ""
        mask_path = _rel_posix(seg, root) if seg and seg.is_file() else ""
        suv_available = bool(pet_path.endswith("SUV.nii.gz"))

        records.append(
            {
                "patient_id": patient_id,
                "study_id": str(row["study_id"]),
                "diagnosis": normalize_diagnosis(row.get("diagnosis", "")),
                "date": str(row.get("date", "") or ""),
                "pet_path": pet_path,
                "ct_path": ct_path,
                "mask_path": mask_path,
                "suv_available": suv_available,
                "n_lesions": n_lesions,
                "tmtv_ml": tmtv,
                "include": True,
                "exclude_reason": "",
            }
        )

    unique_ids = ensure_unique_study_ids(records)
    for rec, sid in zip(records, unique_ids):
        rec["study_id"] = sid

    frame = pd.DataFrame.from_records(records, columns=list(MANIFEST_COLUMNS))
    return frame


def write_manifest(frame: pd.DataFrame, path: Path) -> None:
    """Escribe el CSV UTF-8 con coma, booleanos ``true``/``false``."""
    out = frame.copy()
    for col in ("suv_available", "include"):
        if col in out.columns:
            out[col] = out[col].map(lambda v: "true" if bool(v) else "false")
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False, encoding="utf-8")
