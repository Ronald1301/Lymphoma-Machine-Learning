"""Genera ``data/manifest.csv`` desde ``data/raw/`` y la muestra (T07).

Uso:
    uv run python scripts/build_manifest.py \
        --raw-dir data/raw \
        --sample data/sample_ids.csv \
        --output data/manifest.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from lymphoma.data.manifest import build_manifest, write_manifest

DEFAULT_RAW = Path("data/raw")
DEFAULT_SAMPLE = Path("data/sample_ids.csv")
DEFAULT_OUTPUT = Path("data/manifest.csv")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Raíz del repo para las rutas relativas del manifiesto",
    )
    args = parser.parse_args(argv)

    if not args.sample.is_file():
        print(f"No existe la muestra {args.sample}", file=sys.stderr)
        return 1
    if not args.raw_dir.is_dir():
        print(
            f"Aviso: no existe {args.raw_dir}; las rutas quedarán vacías",
            file=sys.stderr,
        )

    sample = pd.read_csv(args.sample, dtype=str).fillna("")
    frame = build_manifest(args.raw_dir, sample, repo_root=args.repo_root)
    write_manifest(frame, args.output)

    n_paths = int((frame["mask_path"] != "").sum())
    print(
        f"Escrito {args.output}: {len(frame)} filas, "
        f"{n_paths} con máscara encontrada"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
