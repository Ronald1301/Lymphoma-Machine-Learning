# AGENTS.md

Guía para agentes de código (Codex y similares) que trabajen en este repositorio.
Equipo 9 · Universidad de La Habana · Proyecto de Machine Learning.

## Proyecto

**Optimización de la detección y evaluación de lesiones en linfomas mediante PET/CT.**
Segmentación 3D de lesiones de linfoma en FDG-PET/CT, con evaluación a nivel de vóxel, de lesión y de paciente (TMTV).

Documentos de referencia (en `docs/`, léelos antes de proponer cambios de diseño):
- `plan_experimental.md`: diseño experimental (la fuente de verdad técnica).
- `gaps_y_oportunidades.md`: hipótesis H1–H4.
- `referencias/estado_del_arte.md` y `tabla_comparativa.md`: referencias verificadas.
- `roadmap_pipeline.md` e `issues_tareas.md`: tareas T01–T55, fases 0–7, responsables.

## Equipo

Ronald (jefe del equipo), Agustin, Dylan y Abel. No hay roles fijos: todos trabajan en todas las fases.
Cada tarea tiene un identificador `Txx` y un responsable en `issues_tareas.md`. Trabaja solo en la tarea que te asignen y no toques módulos de otra tarea sin avisar.

## Entorno

- Máquina de desarrollo: laptop con **CPU** (Windows 11, Ryzen AI 7 350, 32 GB). **No hay GPU local.**
- Entrenamientos largos: Kaggle/Colab (T4/P100), 6–10 h por corrida. El código debe poder **reanudar desde checkpoint**.
- La NPU solo se usa vía ONNX/Vitis AI y **nunca se afirma aceleración sin medirla**.
- Python 3.10+, PyTorch, MONAI, nibabel/SimpleITK, scikit-learn, scipy, pandas. Versiones fijadas en `requirements.txt`.
- Los scripts deben funcionar en Windows (rutas con `pathlib`, sin comandos solo de Linux).

## Estructura del repositorio

```
docs/                 estado del arte, plan, informe
configs/              un YAML por experimento
data/                 NO se sube a git (raw/, processed/, splits/)
src/lymphoma/{data,models,training,evaluation,deploy}/
scripts/              utilidades de línea de comandos
notebooks/            runners finos para Kaggle/Colab, sin lógica
results/              métricas, figuras y logs pequeños (CSV/JSON)
tests/                pytest
```

## Comandos

```bash
pip install -r requirements.txt
pytest -q                                   # debe pasar antes de cada PR
python scripts/create_issues.py --dry-run   # validar el reparto de tareas (no toca GitHub)
```

## Reglas del proyecto (no negociables)

1. **Split por paciente**, nunca por estudio ni por corte. Se congela una vez (`data/splits/splits.json`, semilla 42) y no se cambia.
2. **El test se usa una sola vez**, al final (T36). Nunca para elegir hiperparámetros, umbral ni postprocesado.
3. **Ningún número escrito a mano** en el informe: todo sale de archivos en `results/` generados por script.
4. **No se comparan Dice de datasets distintos** como si fueran equivalentes.
5. Con menos de 120 pacientes: 5-fold CV + hold-out de test. Con 120 o más: 70/15/15.
6. Con menos de 20 pacientes en test, los resultados son **exploratorios** (estimaciones con IC, sin sobreinterpretar p).
7. Semilla fija 42 (`set_seed()` compartida). Las semillas adicionales son 43.
8. La aumentación de desalineación se aplica **solo a la CT**, nunca a PET ni a la máscara.

## Convenciones técnicas

- Preprocesado: PET a SUV, `log1p` y escalado robusto; CT recortada a [-1000, 1000] HU y escalada a [-1, 1]; resample a 3 mm isotrópico. Guardar el SUV original aparte para las métricas.
- Modelo base: SegResNet compacto (MONAI), parches 96³ (80³ si no cabe), loss 0,5 Dice + 0,5 BCE con logits, AdamW (lr 1e-4, wd 1e-5), inferencia sliding-window con overlap 0,5.
- Métricas: Dice, FPV y FNV en mL; sensibilidad por lesión (componentes 26-conectadas, IoU > 0,10) y FP por paciente, por tamaño (<1, 1–10, >10 mL); TMTV con Bland-Altman e ICC(A,1).
- Estadística: Wilcoxon pareado, bootstrap por paciente y corrección de Holm; reportar tamaño de efecto e IC95%.
- Contratos de interfaz entre módulos: ver `docs/contratos.md` (`manifest.csv`, `splits.json`, volúmenes procesados, predicciones NIfTI, CSV de métricas por paciente, YAML por experimento). No los cambies sin acuerdo del equipo.

## Estilo de código

- Funciones pequeñas con tipos y docstring breve. Sin lógica en notebooks.
- Todo parámetro experimental va en `configs/*.yaml`, no en el código.
- Cada módulo nuevo lleva su test en `tests/` (transforms, split, métricas, matching de lesiones, inferencia). Los casos de prueba de métricas se construyen a mano.
- No subir datos, checkpoints ni archivos `*.nii.gz`, `*.pt`, `*.onnx` pesados. Respeta el `.gitignore`.

## Flujo de trabajo en git

- Ramas `feat/<tema>`. Nada de push directo a `main`.
- Un PR por tarea, con el id en el título (`[T17] Modelo SegResNet`) y enlazado al issue.
- Cada PR lo revisa el siguiente en el anillo Ronald → Agustin → Dylan → Abel → Ronald.
- Definition of Done: código en `main` vía PR revisado, tests pasando, salida documentada (archivo en `results/` o sección en `docs/`) e issue cerrado con enlace al PR.

## Qué no hacer

- No inventar resultados, referencias ni métricas. Si algo no se pudo medir, dilo.
- No afirmar mejora de rendimiento en NPU sin medición real.
- No excluir órganos de forma rígida en el postprocesado; las reglas deben ser auditables.
- No ejecutar descargas masivas de datos ni entrenamientos largos en la laptop sin confirmarlo con el equipo.
- No modificar `data/splits/splits.json` una vez congelado.
