import torch

from lymphoma.data.augmentations import augment_volumes


def _bounding_box(mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    coordinates = torch.nonzero(mask[0], as_tuple=False)
    return coordinates.min(dim=0).values, coordinates.max(dim=0).values


def _center_of_mass(mask: torch.Tensor) -> torch.Tensor:
    return torch.nonzero(mask[0], as_tuple=False).float().mean(dim=0)


def test_rotation_preserves_alignment_and_mask_labels() -> None:
    torch.manual_seed(42)
    mask = torch.zeros((1, 64, 64, 64), dtype=torch.uint8)
    mask[0, 12:22, 23:35, 34:40] = 1
    pet = mask.float()
    ct = mask.float() * 2
    original_center = _center_of_mass(mask)

    pet_aug, ct_aug, mask_aug = augment_volumes(
        pet,
        ct,
        mask,
        flip_probability=0,
        rotation_probability=1,
        rotation_degrees=15,
        pet_scale_range=(1, 1),
        noise_std=0,
    )

    assert pet_aug.shape == ct_aug.shape == mask_aug.shape == (1, 64, 64, 64)
    assert mask_aug.dtype in (
        torch.uint8,
        torch.int8,
        torch.int16,
        torch.int32,
        torch.int64,
    )
    assert set(mask_aug.unique().tolist()) <= {0, 1}
    assert not torch.allclose(_center_of_mass(mask_aug), original_center)

    mask_min, mask_max = _bounding_box(mask_aug)
    image_min, image_max = _bounding_box(ct_aug > 1)
    assert torch.all(torch.abs(mask_min - image_min) <= 1)
    assert torch.all(torch.abs(mask_max - image_max) <= 1)


def test_intensity_augmentations_leave_mask_unchanged() -> None:
    pet = torch.ones((1, 64, 64, 64))
    ct = torch.full_like(pet, 2)
    mask = torch.zeros_like(pet, dtype=torch.uint8)
    mask[0, 20:30, 20:30, 20:30] = 1

    pet_aug, ct_aug, mask_aug = augment_volumes(
        pet,
        ct,
        mask,
        flip_probability=0,
        rotation_probability=0,
        pet_scale_range=(1.1, 1.1),
        noise_std=0.01,
    )

    assert torch.equal(mask_aug, mask)
    assert not torch.equal(pet_aug, pet)
    assert not torch.equal(ct_aug, ct)
