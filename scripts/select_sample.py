"""CLI: selecciona la muestra estratificada de T07.

Uso:
    uv run python scripts/select_sample.py \
        --metadata results/Clinical-Metadata-FDG-PET_CT-Lesions.csv \
        --output data/sample_ids.csv \
        --n 60
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lymphoma.data.sample import DEFAULT_N, DEFAULT_SEED, select_sample

DEFAULT_METADATA = Path("results/Clinical-Metadata-FDG-PET_CT-Lesions.csv")
DEFAULT_OUTPUT = Path("data/sample_ids.csv")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args(argv)

    if not args.metadata.is_file():
        print(f"No existe {args.metadata}", file=sys.stderr)
        return 1

    sample = select_sample(args.metadata, n=args.n, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(args.output, index=False, encoding="utf-8")
    counts = sample["diagnosis"].value_counts().to_dict()
    print(f"Escrito {args.output} con {len(sample)} estudios: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
