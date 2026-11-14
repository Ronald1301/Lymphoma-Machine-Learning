# Contratos de interfaz

Formatos de los archivos que se intercambian entre módulos. Sirven para que los cuatro integrantes trabajen en paralelo: cada módulo solo necesita que su entrada cumpla el contrato, sin importar quién la produjo.

Tarea: T03 (#5). Parte del borrador de `docs/planificacion/roadmap_pipeline.md` (sección "Contratos de interfaz") y lo concreta. Lo que este documento añade al borrador está marcado como **(propuesta)** y se confirma en la revisión del PR.

## Resumen

| Contrato | Ruta | Lo produce | Lo consume |
|---|---|---|---|
| [Manifiesto](#1-manifestcsv) | `data/manifest.csv`, `data/manifest_lymphoma.csv` | T07 (Dylan), T08–T09 (Abel) | T11, T12–T14, T15 |
| [Split](#2-splitsjson) | `data/splits/splits.json` | T11 (Agustin) | T15, T18, T19, T36 |
| [Volúmenes procesados](#3-volúmenes-procesados) | `data/processed/<study_id>/` | T12 (Abel), T13 (Dylan), T14 (Abel) | T15, T19, T20–T22 |
| [Predicciones](#4-predicciones) | `results/<exp>/pred/<study_id>.nii.gz` | T19 (Dylan) | T20–T22, T37–T41 |
| [Métricas por paciente](#5-métricas-por-paciente) | `results/<exp>/metrics_per_patient.csv` | T20–T21 (Agustin), T22 (Ronald) | T33, T40 (Abel), T51 |
| [Configuración](#6-configuración-por-experimento) | `configs/<exp>.yaml` | Quien lance el experimento | T15, T17–T19 |

## Convenciones comunes

- **Identificadores.**
  - `patient_id`: nombre de la carpeta del paciente en el dataset original (por ejemplo, `PETCT_0011f3deaf`).
  - `study_id`: identificador único del estudio, válido como nombre de archivo en Windows y Linux. **(propuesta)** `<patient_id>_<sufijo>`, donde el sufijo es el número final del nombre de la carpeta del estudio. Se verifica en T07 que es único; si no lo es, se usa un índice por fecha (`_01`, `_02`…).
  - Un paciente puede tener varios estudios. Todo lo que agrupa (split, bootstrap) usa `patient_id`; todo lo que nombra archivos usa `study_id`.
- **Rutas.** Siempre relativas a la raíz del repositorio, con `/` como separador. El código las abre con `pathlib`. Nunca rutas absolutas: deben funcionar igual en la laptop y en Kaggle/Colab.
- **CSV.** UTF-8, separador coma, primera fila de cabecera, punto decimal. Los booleanos son `true` / `false`. Un valor desconocido o no aplicable es una celda vacía.
- **Unidades.** Volúmenes en mL. SUV sin unidades. Espaciado en mm.
- **NIfTI.** Siempre `.nii.gz`. NIfTI no admite float16, así que los volúmenes reales van en float32.
- **Semilla.** 42 (regla 7 de `AGENTS.md`).

## 1. `manifest.csv`

Una fila por estudio. `data/manifest.csv` contiene todos los estudios descargados; `data/manifest_lymphoma.csv` tiene las mismas columnas y solo los estudios de linfoma, con `include` y `exclude_reason` actualizados por el filtrado (T08) y el control de calidad (T09).

| Columna | Tipo | Descripción |
|---|---|---|
| `patient_id` | texto | Identificador del paciente. |
| `study_id` | texto | Identificador único del estudio. |
| `diagnosis` | texto | `lymphoma`, `melanoma`, `lung_cancer` o `negative`. Se normaliza a partir de `fdg_metadata.csv` en T07. |
| `date` | fecha `AAAA-MM-DD` | Fecha del estudio tal como viene en los metadatos (anonimizada). Vacía si no se puede obtener. |
| `pet_path` | ruta | PET sin preprocesar. **(propuesta)** Apunta a `SUV.nii.gz` si existe; si no, a `PET.nii.gz`. |
| `ct_path` | ruta | CT sin preprocesar. **(propuesta)** Apunta a `CTres.nii.gz` (CT ya remuestreada a la geometría del PET). |
| `mask_path` | ruta | Máscara de referencia (`SEG.nii.gz`). |
| `suv_available` | booleano | `true` si `pet_path` ya está en SUV. |
| `n_lesions` | entero | Componentes conexas (conectividad 26) de la máscara de referencia a resolución original. 0 en estudios negativos. |
| `tmtv_ml` | decimal | Volumen de la máscara de referencia en mL, a resolución original. |
| `include` | booleano | `false` si el estudio se excluye del proyecto. |
| `exclude_reason` | texto | Motivo de la exclusión. Vacío si `include` es `true`. |

Ejemplo (valores ilustrativos):

```csv
patient_id,study_id,diagnosis,date,pet_path,ct_path,mask_path,suv_available,n_lesions,tmtv_ml,include,exclude_reason
PETCT_0011f3deaf,PETCT_0011f3deaf_10445,lymphoma,2003-03-23,data/raw/PETCT_0011f3deaf/.../SUV.nii.gz,data/raw/PETCT_0011f3deaf/.../CTres.nii.gz,data/raw/PETCT_0011f3deaf/.../SEG.nii.gz,true,7,312.4,true,
```

## 2. `splits.json`

Partición por **paciente**, nunca por estudio (regla 1). Se genera una vez con semilla 42 y no se modifica (reglas 1 y 2).

```json
{
  "seed": 42,
  "mode": "holdout",
  "train": ["PETCT_0011f3deaf", "PETCT_01140d52d8"],
  "val": ["PETCT_0117d7f11f"],
  "test": ["PETCT_0168a0a1c4"],
  "folds": {}
}
```

- `mode`: `holdout` (70/15/15, con 120 pacientes o más) o `5fold` (con menos de 120). Lo decide T10.
- `train`, `val`, `test`: listas de `patient_id`. Ningún paciente aparece en dos listas.
- **(propuesta)** En modo `5fold`, `test` contiene el hold-out de test; `train` y `val` quedan vacías, y `folds` tiene una entrada por fold:

```json
"folds": {
  "0": {"train": ["..."], "val": ["..."]},
  "1": {"train": ["..."], "val": ["..."]}
}
```

- Los estudios de cada conjunto se obtienen cruzando los `patient_id` con `manifest_lymphoma.csv` y quedándose con las filas con `include = true`.

## 3. Volúmenes procesados

Una carpeta por estudio:

```
data/processed/<study_id>/
├── pet.nii.gz    # entrada del modelo
├── ct.nii.gz     # entrada del modelo
├── mask.nii.gz   # referencia
├── suv.nii.gz    # SUV sin normalizar, para métricas
└── meta.json     # (propuesta) trazabilidad del preprocesado
```

| Archivo | Tipo | Contenido |
|---|---|---|
| `pet.nii.gz` | float32 | `log1p(SUV)` con escalado robusto por percentiles (T12). |
| `ct.nii.gz` | float32 | CT recortada a [-1000, 1000] HU y escalada a [-1, 1] (T13). |
| `mask.nii.gz` | uint8 | Máscara binaria de referencia: 0 fondo, 1 lesión. |
| `suv.nii.gz` | float32 | SUV original, sin `log1p` ni escalado. |

Los cuatro volúmenes de un estudio comparten **la misma rejilla**: misma forma, misma matriz afín, espaciado de 3 mm isotrópico y el mismo recorte del cuerpo.

- **Orientación:** **(propuesta)** RAS canónica (`nibabel.as_closest_canonical`).
- **Interpolación:** lineal para PET, CT y SUV; vecino más cercano para la máscara.
- **`meta.json` (propuesta):** forma y afín originales, caja del recorte del cuerpo en la rejilla de 3 mm, percentiles usados en el escalado del PET y versión del código. Permite auditar el preprocesado y llevar una predicción de vuelta a la geometría original si hiciera falta.

## 4. Predicciones

- **Ruta:** `results/<exp>/pred/<study_id>.nii.gz`, donde `<exp>` es el nombre del experimento (el del YAML).
- **Contenido:** máscara binaria uint8 (0 fondo, 1 lesión), ya umbralizada y postprocesada.
- **Geometría:** misma forma y matriz afín que `data/processed/<study_id>/mask.nii.gz`.
- **(propuesta) Probabilidades:** `results/<exp>/prob/<study_id>.nii.gz`, float32 en [0, 1], antes del umbral. Son opcionales; sirven para elegir el umbral en validación (T28).

Las predicciones no se suben a git (`*.nii.gz` está en `.gitignore`).

## 5. Métricas por paciente

`results/<exp>/metrics_per_patient.csv`, con una fila por estudio evaluado. Este archivo sí se sube a git.

| Columna | Tipo | Descripción |
|---|---|---|
| `study_id` | texto | Estudio evaluado. |
| `patient_id` | texto | **(propuesta)** Necesario para el bootstrap por paciente (T33). |
| `split` | texto | **(propuesta)** `val` o `test`. |
| `dice` | decimal | Dice entre predicción y referencia. Vacío si la referencia no tiene lesiones. |
| `fpv_ml` | decimal | Volumen de las componentes predichas que no tocan ninguna lesión de referencia. |
| `fnv_ml` | decimal | Volumen de las lesiones de referencia que no tocan ninguna predicción. |
| `n_lesions_ref` | entero | Lesiones en la referencia (componentes con conectividad 26). |
| `n_lesions_pred` | entero | Componentes en la predicción. |
| `tp_lesions` | entero | Lesiones de referencia detectadas (intersección e IoU > 0,10). |
| `fp_lesions` | entero | Componentes predichas que no corresponden a ninguna lesión de referencia. |
| `tmtv_ref_ml` | decimal | TMTV de referencia. |
| `tmtv_pred_ml` | decimal | TMTV predicho. |

- Los volúmenes se calculan con el volumen físico del vóxel (0,027 mL en la rejilla de 3 mm).
- Los estudios sin lesiones de referencia llevan `dice` vacío y se reportan aparte (T20).
- Las lesiones no detectadas son `n_lesions_ref - tp_lesions`.
- **(propuesta)** El desglose por tamaño de lesión (T21) va en un segundo archivo, `results/<exp>/metrics_per_lesion.csv`, con una fila por lesión de referencia: `study_id, lesion_id, volume_ml, size_bin, detected`. `size_bin` es `<1`, `1-10` o `>10`.

## 6. Configuración por experimento

Un YAML por experimento en `configs/`. Todo parámetro experimental va aquí y no en el código. Nombres previstos: `baseline_petct.yaml`, `baseline_petonly.yaml`, `misalign.yaml`, `anatomic_prior.yaml`.

**(propuesta)** Estructura común, con los valores del plan experimental:

```yaml
experiment: baseline_petct      # nombre único; da nombre a results/<exp>/ y checkpoints/<exp>/
seed: 42

data:
  manifest: data/manifest_lymphoma.csv
  splits: data/splits/splits.json
  processed_dir: data/processed
  fold: null                    # 0-4 en modo 5fold; null en holdout
  modalities: [pet, ct]         # [pet] en baseline_petonly

model:
  name: segresnet
  init_filters: 16
  in_channels: 2
  out_channels: 1

training:
  patch_size: [96, 96, 96]
  positive_ratio: 0.6
  batch_size: 2                 # provisional; se fija en T18
  max_epochs: 250
  val_every: 5
  early_stopping_patience: 25   # en validaciones
  optimizer: adamw
  lr: 1.0e-4
  weight_decay: 1.0e-5
  loss: {dice: 0.5, bce: 0.5}
  amp: true
  checkpoint_dir: checkpoints/baseline_petct
  resume: true

augmentation:
  misalign:
    enabled: false              # true en misalign.yaml; solo se aplica a la CT
    max_shift_voxels: 6
    max_rotation_deg: 3
    aligned_fraction: 0.5

inference:
  overlap: 0.5
  threshold: 0.5                # provisional; se congela en T28

output:
  results_dir: results/baseline_petct
```

Los cuatro YAML comparten estas claves. Una clave nueva se añade en todos, con su valor por defecto.

## Puntos abiertos

Decisiones que el borrador del roadmap no fija y que hay que cerrar en la revisión de este PR:

1. **`splits.json` y `.gitignore`.** T11 pide que `data/splits/splits.json` esté versionado en git, pero `.gitignore` excluye toda la carpeta `/data/`. Hace falta una excepción (`!/data/splits/`) o mover el archivo fuera de `data/`.
2. **Rejilla de evaluación.** Este documento propone calcular las métricas en la rejilla de 3 mm (predicción frente a `mask.nii.gz` procesada). La alternativa es llevar la predicción a la resolución original y comparar con `SEG.nii.gz`. La primera es más simple; la segunda evita que el remuestreo altere la referencia, sobre todo en lesiones pequeñas. `tmtv_ml` del manifiesto (resolución original) permite medir esa diferencia.
3. **`pet_path` y `ct_path`.** Confirmar que apuntan a `SUV.nii.gz` y `CTres.nii.gz`, y no a `PET.nii.gz` y `CT.nii.gz`.
4. **Formato de `study_id`.** Se confirma en T07, al ver los nombres reales de las carpetas.
5. **Evaluaciones con desplazamiento sintético (T32, T38).** Falta decidir dónde se guardan sus predicciones y métricas. Opción: un experimento por condición (`<exp>__shift_mild`, `<exp>__shift_moderate`).
6. **Valores provisionales del YAML:** `batch_size`, `max_epochs` y `threshold`.

## Cómo cambiar un contrato

Un contrato no se cambia sin acuerdo del equipo (`AGENTS.md`). Para cambiarlo: abrir un issue que explique el motivo, actualizar este documento en un PR y avisar a quienes producen y consumen ese formato.

## Aprobación

Cada integrante confirma la parte que va a producir:

- [ ] Ronald: métricas de TMTV, configuración del modelo y del entrenamiento.
- [ ] Agustin: `splits.json`, métricas de vóxel y de lesión.
- [ ] Dylan: `manifest.csv`, CT y geometría de los volúmenes procesados, predicciones.
- [ ] Abel: `manifest_lymphoma.csv`, PET de los volúmenes procesados, entradas de la estadística.
