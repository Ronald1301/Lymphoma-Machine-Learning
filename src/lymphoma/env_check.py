"""Comprobación del entorno: versiones instaladas frente a las fijadas (T02).

Lee las dependencias fijadas con ``==`` en ``pyproject.toml`` y la versión de
Python de ``.python-version``, las compara con lo instalado y, si hay GPU,
ejecuta una prueba mínima de CUDA (detecta el fallo "no kernel image" de la
P100 con ruedas de torch sin sm_60). Lo usa ``scripts/check_env.py``.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "pyproject.toml"
PYTHON_VERSION_FILE = REPO_ROOT / ".python-version"
RESULTS_ENV_DIR = REPO_ROOT / "results" / "env"


def normalize_name(name: str) -> str:
    """Normaliza un nombre de paquete según PEP 503 (``SimpleITK`` -> ``simpleitk``)."""
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_pins(requirements: list[str]) -> dict[str, str]:
    """Convierte ``["torch==2.11.0", ...]`` en ``{"torch": "2.11.0", ...}``.

    Lanza ``ValueError`` si alguna dependencia no está fijada con ``==``.
    """
    pins: dict[str, str] = {}
    for requirement in requirements:
        spec = requirement.split(";", 1)[0].strip()
        name, sep, version = spec.partition("==")
        if not sep or not version.strip():
            raise ValueError(f"Dependencia sin versión fijada con '==': {requirement!r}")
        name = name.split("[", 1)[0].strip()
        pins[normalize_name(name)] = version.strip()
    return pins


def read_pins(pyproject: Path = PYPROJECT) -> dict[str, str]:
    """Lee las dependencias de ``[project.dependencies]`` de un ``pyproject.toml``."""
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return parse_pins(list(data["project"]["dependencies"]))


def installed_versions(names: list[str]) -> dict[str, str | None]:
    """Devuelve la versión instalada de cada paquete, o ``None`` si falta."""
    versions: dict[str, str | None] = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def _public_version(version: str) -> str:
    """Quita la etiqueta local de una versión (``2.11.0+cu126`` -> ``2.11.0``)."""
    return version.split("+", 1)[0]


def compare_pins(installed: dict[str, str | None], pinned: dict[str, str]) -> list[str]:
    """Lista las diferencias entre lo instalado y lo fijado.

    Ignora la etiqueta local (``+cu126``, ``+cpu``): la variante CPU/CUDA de
    torch depende de la plataforma, pero el número de versión debe coincidir.
    """
    problems: list[str] = []
    for name, expected in sorted(pinned.items()):
        found = installed.get(name)
        if found is None:
            problems.append(f"{name}: no está instalado (fijado {expected})")
        elif _public_version(found) != _public_version(expected):
            problems.append(f"{name}: instalado {found}, fijado {expected}")
    return problems


def check_python(actual: str, expected: str) -> list[str]:
    """Exige la misma versión mayor.menor de Python; el parche solo se registra."""
    if actual.split(".")[:2] != expected.split(".")[:2]:
        return [f"python: instalado {actual}, fijado {expected}"]
    return []


def detect_platform() -> str:
    """Identifica dónde corre: ``kaggle``, ``colab``, ``windows``, ``macos`` o ``linux``."""
    if "KAGGLE_KERNEL_RUN_TYPE" in os.environ:
        return "kaggle"
    if "COLAB_RELEASE_TAG" in os.environ:
        return "colab"
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def evidence_path(platform_name: str, results_dir: Path) -> Path:
    """Ruta del JSON de evidencia: ``<results_dir>/env_<plataforma>.json``."""
    return results_dir / f"env_{platform_name}.json"


def git_commit(repo_root: Path = REPO_ROOT) -> str | None:
    """Commit actual del repositorio, o ``None`` si git no está disponible."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def gpu_smoke_test() -> str:
    """Ejecuta suma y backward en CUDA; devuelve ``"ok"`` o el error."""
    import torch

    try:
        x = torch.ones(8, 8, device="cuda", requires_grad=True)
        (x * 2.0).sum().backward()
        torch.cuda.synchronize()
        if x.grad is None or not torch.allclose(x.grad, torch.full_like(x, 2.0)):
            return "error: gradiente incorrecto"
    except Exception as exc:  # cualquier fallo de CUDA se informa, no interrumpe el chequeo
        return f"error: {type(exc).__name__}: {exc}"
    return "ok"


def torch_info() -> dict[str, Any]:
    """Versión de torch, build de CUDA y, si hay GPU, su nombre y la prueba mínima."""
    import torch

    info: dict[str, Any] = {
        "version": torch.__version__,
        "cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "mps_available": torch.backends.mps.is_available(),
    }
    if info["cuda_available"]:
        major, minor = torch.cuda.get_device_capability(0)
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["compute_capability"] = f"sm_{major}{minor}"
        info["arch_list"] = torch.cuda.get_arch_list()
        info["gpu_smoke_test"] = gpu_smoke_test()
    return info


def collect_env(
    pyproject: Path = PYPROJECT, python_version_file: Path = PYTHON_VERSION_FILE
) -> dict[str, Any]:
    """Reúne el estado del entorno y la lista de problemas encontrados."""
    pins = read_pins(pyproject)
    installed = installed_versions(list(pins))
    expected_python = python_version_file.read_text(encoding="utf-8").strip()
    actual_python = platform.python_version()

    problems = check_python(actual_python, expected_python)
    problems += compare_pins(installed, pins)
    torch_details = torch_info() if installed.get("torch") else None
    if torch_details and torch_details.get("gpu_smoke_test", "ok") != "ok":
        problems.append(f"gpu: {torch_details['gpu_smoke_test']}")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform": detect_platform(),
        "os": platform.platform(),
        "machine": platform.machine(),
        "python": actual_python,
        "python_pinned": expected_python,
        "git_commit": git_commit(),
        "packages": installed,
        "pinned": pins,
        "torch": torch_details,
        "problems": problems,
    }


def print_summary(env: dict[str, Any]) -> None:
    """Imprime un resumen legible del entorno."""
    print(f"Plataforma: {env['platform']} ({env['os']})")
    print(f"Python:     {env['python']} (fijado {env['python_pinned']})")
    for name, version in env["packages"].items():
        print(f"  {name:<14} {version}")
    torch_details = env["torch"] or {}
    if torch_details.get("cuda_available"):
        print(
            f"GPU:        {torch_details['gpu_name']} ({torch_details['compute_capability']}), "
            f"CUDA {torch_details['cuda_build']}, prueba: {torch_details['gpu_smoke_test']}"
        )
    else:
        print("GPU:        no disponible (CPU)")
    if env["problems"]:
        print("PROBLEMAS:")
        for problem in env["problems"]:
            print(f"  - {problem}")
    else:
        print("OK: el entorno coincide con las versiones fijadas.")


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de ``scripts/check_env.py``. Devuelve 1 si hay problemas."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--save",
        action="store_true",
        help="guarda el resultado en results/env/env_<plataforma>.json (la plataforma se detecta sola)",
    )
    args = parser.parse_args(argv)

    env = collect_env()
    print_summary(env)
    if args.save:
        out = evidence_path(env["platform"], RESULTS_ENV_DIR)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(env, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Guardado en {out}")
    return 1 if env["problems"] else 0
