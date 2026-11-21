"""Joint PET/CT/segmentation augmentations for aligned 3D volumes."""

from __future__ import annotations

import torch
import torchio as tio
from torch import Tensor


def build_augmentation_transform(
    *,
    flip_probability: float = 0.5,
    rotation_degrees: float = 15.0,
    rotation_probability: float = 0.5,
    pet_scale_range: tuple[float, float] = (0.9, 1.1),
    noise_std: float = 0.01,
) -> tio.Compose:
    """Create joint spatial and modality-specific intensity augmentations."""
    return tio.Compose(
        [
            tio.RandomFlip(
                axes=(0, 1, 2),
                flip_probability=flip_probability,
            ),
            tio.RandomAffine(
                scales=1,
                degrees=rotation_degrees,
                translation=0,
                image_interpolation="linear",
                label_interpolation="nearest",
                p=rotation_probability,
            ),
            tio.RandomMultiply(
                multiplication_range=pet_scale_range,
                include=("pet",),
            ),
            tio.RandomNoise(
                mean=0,
                std=(0, noise_std),
                include=("pet", "ct"),
            ),
        ]
    )


def augment_volumes(
    pet: Tensor,
    ct: Tensor,
    mask: Tensor,
    *,
    flip_probability: float = 0.5,
    rotation_degrees: float = 15.0,
    rotation_probability: float = 0.5,
    pet_scale_range: tuple[float, float] = (0.9, 1.1),
    noise_std: float = 0.01,
) -> tuple[Tensor, Tensor, Tensor]:
    """Augment aligned [C, D, H, W] PET, CT, and mask tensors together."""
    if pet.ndim != 4 or pet.shape != ct.shape or pet.shape != mask.shape:
        raise ValueError("PET, CT, and mask must have the same [C, D, H, W] shape.")

    subject = tio.Subject(
        pet=tio.ScalarImage(tensor=pet.clone()),
        ct=tio.ScalarImage(tensor=ct.clone()),
        mask=tio.LabelMap(tensor=mask.clone()),
    )
    transformed = build_augmentation_transform(
        flip_probability=flip_probability,
        rotation_degrees=rotation_degrees,
        rotation_probability=rotation_probability,
        pet_scale_range=pet_scale_range,
        noise_std=noise_std,
    )(subject)
    return transformed.pet.data, transformed.ct.data, transformed.mask.data
