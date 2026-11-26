"""Comprueba que el entorno coincide con las versiones fijadas (T02).

Uso:
    uv run python scripts/check_env.py           # solo muestra el resultado
    uv run python scripts/check_env.py --save    # además lo guarda en results/env/env_<plataforma>.json
"""

import sys

from lymphoma.env_check import main

if __name__ == "__main__":
    sys.exit(main())
