"""Generate slice-by-slice visual QC images from processed NPZ volumes."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np


def load_volume(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load aligned CT, PET, and mask arrays from one NPZ cache."""
    with np.load(path, allow_pickle=False) as archive:
        missing = {"ct", "pet", "mask"}.difference(archive.files)
        if missing:
            raise ValueError(f"{path} is missing arrays: {', '.join(sorted(missing))}")
        ct, pet, mask = (np.asarray(archive[key]) for key in ("ct", "pet", "mask"))

    if ct.ndim != 3 or pet.ndim != 3 or mask.ndim != 3:
        raise ValueError(f"{path} must contain three-dimensional arrays.")
    if ct.shape != pet.shape or ct.shape != mask.shape:
        raise ValueError(f"{path} CT, PET, and mask arrays must have matching shapes.")
    return ct, pet, mask


def select_axial_slice(mask: np.ndarray) -> int:
    """Return the axial slice with the largest positive mask area."""
    if mask.ndim != 3:
        raise ValueError("Mask must be a three-dimensional array.")
    areas = np.count_nonzero(mask > 0, axis=(0, 1))
    if not np.any(areas):
        return mask.shape[2] // 2
    return int(np.argmax(areas))


def visualize_file(input_path: Path, output_dir: Path) -> Path:
    """Render CT, PET, and CT/mask overlay for one NPZ file."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError(
            "Visual QC requires matplotlib; install it in the project environment."
        ) from error

    ct, pet, mask = load_volume(input_path)
    slice_index = select_axial_slice(mask)
    ct_slice = ct[:, :, slice_index].T
    pet_slice = pet[:, :, slice_index].T
    mask_slice = mask[:, :, slice_index].T

    figure, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    axes[0].imshow(ct_slice, cmap="gray", origin="lower")
    axes[0].set_title("CT")
    axes[1].imshow(pet_slice, cmap="magma", origin="lower")
    axes[1].set_title("PET")
    axes[2].imshow(ct_slice, cmap="gray", origin="lower")
    if np.any(mask_slice > 0):
        mask_overlay = np.ma.masked_where(mask_slice <= 0, mask_slice > 0)
        axes[2].imshow(
            mask_overlay,
            cmap="Reds",
            alpha=0.5,
            origin="lower",
            vmin=0,
            vmax=1,
        )
    axes[2].set_title("CT + Mask")
    for axis in axes:
        axis.set_axis_off()
    figure.suptitle(f"{input_path.stem} — axial slice {slice_index}")

    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    output_path = output_dir / f"visual_qc_{input_path.stem}.png"
    try:
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
    finally:
        plt.close(figure)
    return output_path


def main() -> None:
    """Generate visual QC PNGs for all NPZ caches in the input directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input_dir",
        type=Path,
        default=Path("data/processed/"),
        help="Directory containing per-study NPZ caches.",
    )
    args = parser.parse_args()
    if not args.input_dir.is_dir():
        parser.error(f"Input directory does not exist: {args.input_dir}")

    input_files = sorted(
        path
        for path in args.input_dir.iterdir()
        if path.is_file() and path.suffix.casefold() == ".npz"
    )
    if not input_files:
        parser.error(f"No .npz cache files found in {args.input_dir}")

    output_dir = Path("results") / "visual_qc"
    failures = 0
    for input_path in input_files:
        try:
            output_path = visualize_file(input_path, output_dir)
        except (OSError, ValueError, KeyError, ImportError) as error:
            failures += 1
            print(f"Failed {input_path}: {error}")
            continue
        print(f"Saved {output_path}")
    if failures:
        raise SystemExit(f"Visual QC failed for {failures} of {len(input_files)} files.")


if __name__ == "__main__":
    main()
