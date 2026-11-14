import random
import numpy as np
import torch
from lymphoma.utils import DEFAULT_SEED, set_seed

def _draw() -> tuple[float, float, float]:
    return random.random(), float(np.random.rand()), float(torch.rand(1))

def test_set_seed_is_reproducible():
    set_seed()
    first = _draw()
    set_seed()
    assert _draw() == first

def test_set_seed_default_is_42():
    set_seed()
    first = _draw()
    set_seed(42)
    assert DEFAULT_SEED == 42
    assert _draw() == first

def test_different_seeds_give_different_values():
    set_seed(42)
    first = _draw()
    set_seed(43)
    assert _draw() != first