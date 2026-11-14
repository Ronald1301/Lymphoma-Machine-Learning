"""Utilidades compartidas por todos los módulos."""

import random
import numpy as np
import torch

DEFAULT_SEED = 42

def set_seed(seed: int = DEFAULT_SEED) -> None:
    """Fija la semilla de Python, NumPy y PyTorch (CPU y GPU).

    No fuerza algoritmos deterministas en cuDNN, así que en GPU puede quedar
    una variación
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)