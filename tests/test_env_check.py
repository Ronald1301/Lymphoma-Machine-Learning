import json

import pytest

from lymphoma import env_check
from lymphoma.env_check import (
    PYPROJECT,
    check_python,
    collect_env,
    compare_pins,
    evidence_path,
    parse_pins,
    read_pins,
)


def test_parse_pins_normalizes_names_and_markers():
    pins = parse_pins(["SimpleITK==2.5.7", "scikit_learn==1.9.1", "torch==2.11.0 ; sys_platform == 'linux'"])
    assert pins == {"simpleitk": "2.5.7", "scikit-learn": "1.9.1", "torch": "2.11.0"}


@pytest.mark.parametrize("requirement", ["numpy", "numpy>=2.0", "numpy~=2.5", "numpy=="])
def test_parse_pins_rejects_unpinned(requirement):
    with pytest.raises(ValueError):
        parse_pins([requirement])


def test_compare_pins_equal_versions():
    assert compare_pins({"monai": "1.6.1"}, {"monai": "1.6.1"}) == []


def test_compare_pins_ignores_local_label():
    assert compare_pins({"torch": "2.11.0+cu126"}, {"torch": "2.11.0"}) == []


def test_compare_pins_detects_different_version():
    problems = compare_pins({"torch": "2.10.0+cu128"}, {"torch": "2.11.0"})
    assert problems == ["torch: instalado 2.10.0+cu128, fijado 2.11.0"]


def test_compare_pins_detects_missing_package():
    problems = compare_pins({"monai": None}, {"monai": "1.6.1"})
    assert problems == ["monai: no está instalado (fijado 1.6.1)"]


@pytest.mark.parametrize(
    ("actual", "expected", "n_problems"),
    [("3.12.16", "3.12.16", 0), ("3.12.9", "3.12.16", 0), ("3.13.1", "3.12.16", 1), ("3.11.9", "3.12.16", 1)],
)
def test_check_python_compares_major_minor(actual, expected, n_problems):
    assert len(check_python(actual, expected)) == n_problems


def test_repo_dependencies_are_all_pinned():
    pins = read_pins(PYPROJECT)
    assert {"torch", "monai", "nibabel", "simpleitk", "scikit-learn", "scipy", "pandas"} <= set(pins)


def test_installed_environment_matches_pins():
    env = collect_env()
    assert env["problems"] == []
    assert env["torch"]["version"].startswith(env["pinned"]["torch"])


def test_evidence_path_uses_platform_name(tmp_path):
    assert evidence_path("windows", tmp_path) == tmp_path / "env_windows.json"


def test_save_names_file_after_detected_platform(tmp_path, monkeypatch):
    monkeypatch.setattr(env_check, "RESULTS_ENV_DIR", tmp_path)
    monkeypatch.setattr(env_check, "detect_platform", lambda: "kaggle")
    env_check.main(["--save"])
    assert [f.name for f in tmp_path.iterdir()] == ["env_kaggle.json"]
    saved = json.loads((tmp_path / "env_kaggle.json").read_text(encoding="utf-8"))
    assert saved["platform"] == "kaggle"
