# Lymphoma-Machine-Learning

Proyecto de segmentación 3D de lesiones de linfoma en FDG-PET/CT y evaluación a nivel de vóxel, lesión y paciente (TMTV).

## Documentación del proyecto

- [Roadmap del pipeline](docs/planificacion/roadmap_pipeline.md): fases, flujo técnico, entregables y criterios de finalización.
- [Tareas del proyecto](docs/planificacion/issues_tareas.md): tareas T01–T55, responsables, dependencias y checklist.
- [Plan experimental](docs/metodologia/plan_experimental.md): diseño técnico y evaluación.
- [Brechas y oportunidades](docs/metodologia/gaps_y_oportunidades.md): hipótesis y motivación.
- [Estado del arte](docs/referencias/estado_del_arte.md).
- [Tabla comparativa](docs/referencias/tabla_comparativa.md) ([CSV](docs/referencias/tabla_comparativa.csv)).

## Instalación

1. Instala [uv](https://docs.astral.sh/uv/): `winget install --id=astral-sh.uv -e` en Windows, `brew install uv` en macOS o `curl -LsSf https://astral.sh/uv/install.sh | sh` en Linux.
2. En la carpeta del repositorio, ejecuta `uv sync`.
3. Comprueba la instalación con `uv run python scripts/check_env.py`. La última línea debe decir `OK: el entorno coincide con las versiones fijadas.`

Guía paso a paso para Windows, macOS, Linux, Kaggle y Colab: [Instalar el entorno](docs/reproducibilidad/entorno.md).

## Estructura del código

El código fuente vive en `src/lymphoma/`, organizado por datos, modelos, entrenamiento, evaluación y despliegue. Los parámetros experimentales se guardan en `configs/`; las utilidades de línea de comandos, en `scripts/`; y las pruebas, en `tests/`.

Los datos clínicos y los artefactos grandes de entrenamiento no se versionan. Consulta el roadmap y las tareas antes de iniciar una fase.
