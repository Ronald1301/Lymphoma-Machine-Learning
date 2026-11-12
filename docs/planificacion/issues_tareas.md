# Tareas del proyecto (issues de GitHub)

**Proyecto:** Optimización de la detección y evaluación de lesiones en linfomas mediante PET/CT  
**Equipo:** 4 personas (Ronald, Agustin, Dylan, Abel), sin roles fijos · **Cierre interno:** 20 dic 2026 · **Colchón:** 21-31 dic

Este documento y `scripts/create_issues.py` salen de la misma fuente: las 55 tareas son idénticas en ambos.

## Cómo trabajamos

No hay roles fijos. El trabajo se agrupa por **componente** (lo que estamos construyendo), y cada componente se reparte entre los cuatro:

1. **Todos en todas las fases.** Cada fase tiene tareas obligatorias de Ronald, Agustin, Dylan y Abel.
2. **Todos en todos los componentes.** Cada persona escribe una parte de los datos, del modelo, de las métricas y del despliegue.
3. **Todos entrenan.** Ronald el baseline PET+CT, Abel el PET-only, Agustin la variante con desalineación y Dylan la semilla adicional del baseline; Ronald y Dylan escriben juntos la loss y el bucle (T18). Además todos corren el smoke test en su cuenta (T24). El prior anatómico (T34-T35) es opcional.
4. **Revisión en anillo.** Cada PR lo revisa el siguiente en la lista Ronald→Agustin→Dylan→Abel→Ronald. Así todos conocen el código de todos.
5. **Coordinación rotativa.** Cada semana coordina una persona: mantiene el tablero, convoca el daily de 10 min, desbloquea issues sin avance en 48 h y hace merge de PRs aprobados. Rota Ronald→Agustin→Dylan→Abel.
6. **Tareas de todos** (marcadas con `*` en las tablas): decisiones y trabajos que hacemos todos (cuentas, partición, smoke test, tests, verificación cruzada, entrega).

## Quién trabaja en qué: por componente

| Componente | Ronald | Agustin | Dylan | Abel |
|---|---|---|---|---|
| **Base** | T01, T05*, T06, T23* | T02, T05*, T23* | T03, T04, T05*, T23* | T05*, T23* |
| **Datos** | T10* | T10*, T11 | T07, T10*, T13 | T08, T09, T10*, T12, T14 |
| **Modelo** | T17, T18, T34 | T29 | T15, T18, T19 | T16 |
| **Entrenamiento** | T24*, T25 | T24*, T30 | T24*, T31 | T24*, T26, T35 |
| **Evaluación** | T22, T27, T28, T32, T36, T42 | T20, T21, T37, T38 | T39 | T33, T40, T41 |
| **Despliegue** | T46 | T45 | T43, T47 | T44 |
| **Informe** | T50, T52, T54*, T55* | T48, T49, T54*, T55* | T51, T54*, T55* | T53, T54*, T55* |

`*` = tarea de todos. Las tareas opcionales (T34, T35, T47) no cuentan para el reparto obligatorio.

## Quién trabaja en qué: por fase

| Fase | Ronald | Agustin | Dylan | Abel |
|---|---|---|---|---|
| **0 · Arranque** | T01, T05*, T06 | T02, T05* | T03, T04, T05* | T05* |
| **1 · Datos** | T10* | T10*, T11 | T07, T10*, T13 | T08, T09, T10*, T12, T14 |
| **2 · Código base** | T17, T18, T22, T23* | T20, T21, T23* | T15, T18, T19, T23* | T16, T23* |
| **3 · Baselines** | T24*, T25, T27, T28 | T24* | T24* | T24*, T26 |
| **4 · Mejoras** | T32, T34 | T29, T30 | T31 | T33, T35 |
| **5 · Evaluación** | T36, T42 | T37, T38 | T39 | T40, T41 |
| **6 · Despliegue** | T46 | T45 | T43, T47 | T44 |
| **7 · Informe y entrega** | T50, T52, T54*, T55* | T48, T49, T54*, T55* | T51, T54*, T55* | T53, T54*, T55* |

## Calendario por fases

| Fase | Nombre | Inicio | Fecha límite (milestone) | Objetivo |
|---|---|---|---|---|
| 0 | Arranque | 2026-11-02 | **2026-11-08** | Repo, entorno, convenciones, contratos de interfaz y alcance confirmado. |
| 1 | Datos | 2026-11-09 | **2026-11-22** | Split por paciente congelado y 10 casos preprocesados verificados visualmente. |
| 2 | Código base | 2026-11-09 | **2026-11-22** | Loader, modelo, loss, inferencia y métricas con tests pasando. |
| 3 | Baselines | 2026-11-23 | **2026-12-01** | Baseline PET+CT y comparador PET-only entrenados; umbral y postprocesado congelados. |
| 4 | Mejoras | 2026-12-02 | **2026-12-08** | Variante con desalineación entrenada, semilla adicional y script de estadística listo. |
| 5 | Evaluación | 2026-12-09 | **2026-12-13** | Test ejecutado una sola vez; métricas, estadística y análisis de errores listos. |
| 6 | Despliegue | 2026-12-09 | **2026-12-15** | ONNX validado, benchmark CPU y documentación; NPU solo si se mide. |
| 7 | Informe y entrega | 2026-11-09 | **2026-12-20** | Informe verificado, repo reproducible y presentación lista. Colchón: 21-31 dic. |

> La fase 7 arranca temprano (semana 2) porque el estado del arte ya está escrito; las secciones del informe se redactan cuando cada parte queda lista. Las fases 1 y 2 van en paralelo; las fases 5 y 6 también.

## Plan semana a semana

| Semana | Fechas | Fases | Coordina | Ronald | Agustin | Dylan | Abel | Todos |
|---|---|---|---|---|---|---|---|---|
| 1 | 2-8 nov | 0 | Ronald | T01, T06 | T02 | T03, T04 | - | T05 |
| 2 | 9-15 nov | 1, 2, 7 | Agustin | T17, T18 | T20, T48 | T07, T15, T18 | T08, T09, T16 | T10 |
| 3 | 16-22 nov | 1, 2, 7 | Dylan | T22 | T11, T21 | T13, T19 | T12, T14 | T23 |
| 4 | 23 nov - 1 dic | 3, 4 | Abel | T25, T27, T28 | T29 | T31 | T26 | T24 |
| 5 | 2-8 dic | 4, 7 | Ronald | T32, T34 (opc.) | T30, T49 | T31* | T33, T35 (opc.) | - |
| 6 | 9-13 dic | 5, 6 | Agustin | T36, T46 | T37, T38, T45 | T39, T43 | T40, T41, T44 | - |
| 7 | 14-20 dic | 6, 7 | Dylan | T42, T50, T52 | - | T47 (opc.), T51 | T53 | T54, T55 |
| Colchón | 21-31 dic | - | Abel | Correcciones, ensayo y entrega | - | - | - | - |

`*` = continúa de la semana anterior.

**Si el calendario se aprieta, se recorta en este orden:** T47 (INT8/NPU) → T34-T35 (prior anatómico) → T31 (semilla adicional). No se recortan: split por paciente, test una sola vez, PET-only, métricas por lesión y TMTV, ni el smoke test de todos.

**Exámenes y otras entregas:** este calendario no los conoce. Si hay semanas con parciales, muevan las fases 3-4 (donde el cómputo es la limitación) y no las de escritura.

## Tareas logísticas y técnicas por persona

Las tareas **logísticas** (repo, entorno, contratos, convenciones, profesor, descarga, caché, documentación, reproducibilidad) se reparten parejo; las **técnicas** son el resto. Las 6 tareas de todos suman la misma parte a cada uno.

| Persona | Logísticas | Técnicas |
|---|---|---|
| Ronald | T01, T06, T46, T52 | T17, T18, T22, T25, T27, T28, T32, T34 (opc.), T36, T42, T50 |
| Agustin | T02, T48 | T11, T20, T21, T29, T30, T37, T38, T45, T49 |
| Dylan | T03, T04, T07 | T13, T15, T18, T19, T31, T39, T43, T47 (opc.), T51 |
| Abel | T14, T53 | T08, T09, T12, T16, T26, T33, T35 (opc.), T40, T41, T44 |

## Carga estimada por persona

| Persona | Tareas | Logísticas (h) | Técnicas (h) | De todos (h) | **Total obligatorio (h)** | Opcionales (h) |
|---|---:|---:|---:|---:|---:|---:|
| Ronald | 21 | 17 | 78 | 11 | **106** | 16 |
| Agustin | 17 | 16 | 88 | 11 | **115** | 0 |
| Dylan | 18 | 22 | 80 | 11 | **113** | 16 |
| Abel | 18 | 16 | 88 | 11 | **115** | 16 |

Esfuerzo: S ≈ 3 h, M ≈ 8 h, L ≈ 16 h (incluye esperas de entrenamiento). Es una estimación gruesa solo para balancear. Las tareas de todos reparten las horas por igual y las de varios responsables también. No incluye el tiempo semanal de coordinación (~2 h).

## Resumen de tareas

| ID | Tarea | Fase | Componente | Tipo | Responsable | Revisor | Esf. | Depende de |
|---|---|---|---|---|---|---|---|---|
| T01 | Crear estructura del repositorio y .gitignore | 0 | Base | Logística | Ronald | Agustin | S | - |
| T02 | Entorno reproducible (laptop Windows y Kaggle/Colab) | 0 | Base | Logística | Agustin | Dylan | M | T01 |
| T03 | Acordar contratos de interfaz | 0 | Base | Logística | Dylan | Abel | S | T01 |
| T04 | Convenciones de trabajo, plantillas y revisión cruzada | 0 | Base | Logística | Dylan | Abel | S | T01 |
| T05 | Cuentas de cómputo y acceso a datos | 0 | Base | Logística | Todos | cruzada | M | - |
| T06 | Confirmar alcance y fecha de entrega con el profesor | 0 | Base | Logística | Ronald | Agustin | S | - |
| T07 | Descargar FDG-PET-CT-Lesions y construir manifest.csv | 1 | Datos | Logística | Dylan | Abel | L | T02, T05 |
| T08 | Filtrar estudios de linfoma y registrar exclusiones | 1 | Datos | Técnica | Abel | Ronald | M | T07 |
| T09 | QC de geometría y máscaras | 1 | Datos | Técnica | Abel | Ronald | M | T08 |
| T10 | Decidir esquema de partición según el número de pacientes | 1 | Datos | Técnica | Todos | cruzada | S | T08 |
| T11 | Implementar y congelar el split por paciente | 1 | Datos | Técnica | Agustin | Dylan | M | T09, T10 |
| T12 | Preprocesado de PET: SUV, log1p y escalado robusto | 1 | Datos | Técnica | Abel | Ronald | M | T09 |
| T13 | Preprocesado de CT y geometría: HU, resample a 3 mm y recorte de cuerpo | 1 | Datos | Técnica | Dylan | Abel | M | T09 |
| T14 | Caché de volúmenes y verificación visual de 10 casos | 1 | Datos | Logística | Abel | Ronald | M | T12, T13 |
| T15 | Dataset y DataLoader MONAI | 2 | Modelo | Técnica | Dylan | Abel | M | T03 |
| T16 | Aumentaciones conjuntas | 2 | Modelo | Técnica | Abel | Ronald | M | T15 |
| T17 | Modelo SegResNet compacto y variante PET-only | 2 | Modelo | Técnica | Ronald | Agustin | S | T15 |
| T18 | Loss y bucle de entrenamiento con reanudación | 2 | Modelo | Técnica | Ronald + Dylan | Abel | L | T17 |
| T19 | Inferencia sliding-window | 2 | Modelo | Técnica | Dylan | Abel | M | T17 |
| T20 | Métricas de vóxel | 2 | Evaluación | Técnica | Agustin | Dylan | M | T03 |
| T21 | Métricas de lesión | 2 | Evaluación | Técnica | Agustin | Dylan | L | T20 |
| T22 | Métricas de TMTV | 2 | Evaluación | Técnica | Ronald | Agustin | M | T20 |
| T23 | Tests unitarios y CI: cada persona testea lo que construyó | 2 | Base | Técnica | Todos | cruzada | M | T16, T19, T20, T21, T22 |
| T24 | Overfit de 2-4 casos y smoke test en las 4 cuentas | 3 | Entrenamiento | Técnica | Todos | cruzada | M | T14, T18 |
| T25 | Entrenar baseline PET+CT | 3 | Entrenamiento | Técnica | Ronald | Agustin | L | T24 |
| T26 | Entrenar comparador PET-only | 3 | Entrenamiento | Técnica | Abel | Ronald | L | T24 |
| T27 | Análisis inicial en validación: vóxel y lesión | 3 | Evaluación | Técnica | Ronald | Agustin | M | T25, T26 |
| T28 | Revisión de falsos positivos fisiológicos y congelar umbral/postprocesado | 3 | Evaluación | Técnica | Ronald | Agustin | M | T25, T26 |
| T29 | Implementar aumentación de desalineación (solo CT) | 4 | Modelo | Técnica | Agustin | Dylan | M | T16 |
| T30 | Entrenar variante con desalineación | 4 | Entrenamiento | Técnica | Agustin | Dylan | L | T25, T29 |
| T31 | Semilla adicional del baseline PET+CT (variabilidad entre semillas) | 4 | Entrenamiento | Técnica | Dylan | Abel | L | T24 |
| T32 | Generador de tests con desplazamiento sintético | 4 | Evaluación | Técnica | Ronald | Agustin | M | T19 |
| T33 | Script de estadística comparativa | 4 | Evaluación | Técnica | Abel | Ronald | M | T22 |
| T34 | Precalcular máscaras de TotalSegmentator *(opc.)* | 4 | Modelo | Técnica | Ronald | Agustin | L | T14 |
| T35 | Entrenar variante con prior anatómico *(opc.)* | 4 | Entrenamiento | Técnica | Abel | Ronald | L | T25, T34 |
| T36 | Congelar todo y ejecutar el test una sola vez | 5 | Evaluación | Técnica | Ronald | Agustin | M | T28, T30 |
| T37 | Métricas completas de vóxel y lesión en test | 5 | Evaluación | Técnica | Agustin | Dylan | M | T36 |
| T38 | Robustez bajo desplazamiento sintético | 5 | Evaluación | Técnica | Agustin | Dylan | M | T32, T36 |
| T39 | TMTV en test: Bland-Altman e ICC | 5 | Evaluación | Técnica | Dylan | Abel | M | T36 |
| T40 | Estadística comparativa sobre test | 5 | Evaluación | Técnica | Abel | Ronald | L | T31, T33, T37, T39 |
| T41 | Análisis de errores por tamaño y órgano | 5 | Evaluación | Técnica | Abel | Ronald | M | T37 |
| T42 | Cierre de hipótesis H1-H4 | 5 | Evaluación | Técnica | Ronald | Agustin | S | T38, T40, T41 |
| T43 | Exportar a ONNX y validar equivalencia | 6 | Despliegue | Técnica | Dylan | Abel | M | T36 |
| T44 | Benchmark de inferencia en CPU | 6 | Despliegue | Técnica | Abel | Ronald | M | T43 |
| T45 | Script de inferencia de demostración (ONNX → máscara + TMTV) | 6 | Despliegue | Técnica | Agustin | Dylan | M | T43 |
| T46 | Documentar despliegue | 6 | Despliegue | Logística | Ronald | Agustin | M | T44 |
| T47 | Cuantización INT8 y prueba en NPU *(opc.)* | 6 | Despliegue | Técnica | Dylan | Abel | L | T44 |
| T48 | Esqueleto del informe y adaptación del estado del arte | 7 | Informe | Logística | Agustin | Dylan | M | T03 |
| T49 | Sección de datos y preprocesado | 7 | Informe | Técnica | Agustin | Dylan | M | T11, T14 |
| T50 | Sección de modelo y entrenamiento | 7 | Informe | Técnica | Ronald | Agustin | M | T18, T25 |
| T51 | Sección de evaluación, resultados y figuras | 7 | Informe | Técnica | Dylan | Abel | L | T40, T41 |
| T52 | Limitaciones y trabajo futuro | 7 | Informe | Logística | Ronald | Agustin | S | T42 |
| T53 | Reproducibilidad desde cero | 7 | Informe | Logística | Abel | Ronald | M | T44, T45 |
| T54 | Verificación cruzada final del informe | 7 | Informe | Técnica | Todos | cruzada | M | T51, T52 |
| T55 | Entrega y presentación | 7 | Informe | Técnica | Todos | cruzada | M | T54 |

## Etiquetas y milestones

**Milestones:** `Fase 0 - Arranque`, `Fase 1 - Datos`, `Fase 2 - Código base`, `Fase 3 - Baselines`, `Fase 4 - Mejoras`, `Fase 5 - Evaluación`, `Fase 6 - Despliegue`, `Fase 7 - Informe y entrega`.

**Etiquetas:** `datos`, `modelado`, `evaluacion`, `estadistica`, `despliegue`, `redaccion`, `entrenamiento`, `calidad`, `decision`, `infra`, `setup`, `diseno`, `entrega`, `opcional`, `bloqueado`, `todos`, `logistica`, `fase-0`, `fase-1`, `fase-2`, `fase-3`, `fase-4`, `fase-5`, `fase-6`, `fase-7`, `Ronald`, `Agustin`, `Dylan`, `Abel`. Las etiquetas `Ronald`, `Agustin`, `Dylan` y `Abel` indican responsable y sirven para filtrar el tablero.

**Definition of Done de cualquier issue:** código en `main` vía PR revisado por el revisor asignado, tests pasando, salida documentada (archivo en `results/` o sección en `docs/`) y issue cerrado con enlace al PR.

## Cómo usar el script

Requisitos: Python 3.10+, [GitHub CLI](https://cli.github.com) y haber ejecutado `gh auth login`. El repositorio debe existir ya en GitHub.

```bash
# 1) Ver qué crearía y validar el reparto, sin tocar GitHub
python scripts/create_issues.py --dry-run

# 2) Crear etiquetas, milestones e issues (desde dentro del clon del repo)
python scripts/create_issues.py --users "Ronald=usuario1,Agustin=usuario2,Dylan=usuario3,Abel=usuario4"

# 3) Contra otro repo
python scripts/create_issues.py --repo owner/nombre --users "Ronald=..,Agustin=..,Dylan=..,Abel=.."
```

- Es **idempotente**: si un issue con el mismo prefijo `[Txx]` ya existe, lo salta; si se corta a mitad, se vuelve a ejecutar.
- Las tareas de todos se asignan a las cuatro personas.
- Si un usuario no es colaborador del repo, el script crea el issue sin asignar y lo avisa.
- Las dependencias se escriben como `#número (Txx)` con el número real del issue en GitHub.
- Los `- [ ]` de cada issue se convierten en checklist con barra de progreso.

---

## Fase 0 - Arranque

**Milestone:** `Fase 0 - Arranque` · **Inicio:** 2026-11-02 · **Fecha límite:** 2026-11-08  
**Objetivo:** Repo, entorno, convenciones, contratos de interfaz y alcance confirmado.

### T01 · Crear estructura del repositorio y .gitignore

**Componente:** Base · **Tipo:** Logística · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-0` `setup` `logistica` `Ronald`  

Dejar el repo con la estructura acordada para que todos trabajen sobre el mismo esqueleto.

- [ ] Carpetas: docs/, configs/, src/lymphoma/{data,models,training,evaluation,deploy}/, scripts/, notebooks/, results/, tests/
- [ ] .gitignore excluye data/, checkpoints/, *.nii.gz, *.pt y *.onnx pesados
- [ ] README enlaza al roadmap y a las tareas

### T02 · Entorno reproducible (laptop Windows y Kaggle/Colab)

**Componente:** Base · **Tipo:** Logística · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-0` `setup` `infra` `logistica` `Agustin`  
**Depende de:** T01

Un entorno con versiones fijadas que funcione igual en las laptops y en Kaggle/Colab.

- [ ] requirements.txt o environment.yml con versiones fijadas (MONAI, PyTorch, nibabel/SimpleITK, scikit-learn, scipy, pandas)
- [ ] Instrucciones para Windows y celda de setup para Kaggle/Colab
- [ ] Prueba: python -c 'import monai, torch' funciona en una laptop y en Kaggle

### T03 · Acordar contratos de interfaz

**Componente:** Base · **Tipo:** Logística · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-0` `diseno` `logistica` `Dylan`  
**Depende de:** T01

Fijar los formatos de intercambio para que los cuatro trabajen en paralelo sin bloquearse.

- [ ] docs/contratos.md con: manifest.csv, splits.json (IDs de paciente), volúmenes procesados (3 mm, SUV original aparte), predicciones NIfTI, CSV de métricas por paciente y YAML por experimento
- [ ] Revisado y aprobado por los cuatro (cada uno confirma la parte que va a producir)

### T04 · Convenciones de trabajo, plantillas y revisión cruzada

**Componente:** Base · **Tipo:** Logística · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-0` `setup` `logistica` `Dylan`  
**Depende de:** T01

Reglas mínimas para no pisarse y para que todos conozcan todo el código.

- [ ] Plantillas de issue y de PR
- [ ] Ramas feat/<tema>; PR con revisión obligatoria del revisor asignado en el issue (el siguiente en la lista Ronald→Agustin→Dylan→Abel→Ronald); si el repo privado no permite proteger main, regla acordada de no hacer push directo
- [ ] Rotación semanal del coordinador documentada en docs/trabajo_en_equipo.md
- [ ] Utilidad set_seed() compartida con semilla 42

### T05 · Cuentas de cómputo y acceso a datos

**Componente:** Base · **Tipo:** Logística · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-0` `infra` `todos` `logistica`  

Cada integrante prepara su propio acceso a GPU gratuita y a los datos: los cuatro van a entrenar.

- [ ] Cuenta de Kaggle y/o Colab operativa con GPU habilitada (comprobar que la verificación de cuenta funciona desde su conexión)
- [ ] Acceso a TCIA / FDG-PET-CT-Lesions verificado
- [ ] Cuota semanal de GPU de cada cuenta anotada en el tablero
- [ ] Estimado el tamaño y el tiempo real de descarga con la conexión disponible

### T06 · Confirmar alcance y fecha de entrega con el profesor

**Componente:** Base · **Tipo:** Logística · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-0` `decision` `logistica` `Ronald`  

Validar el alcance antes de invertir cómputo.

- [ ] Validar objetivo (segmentación basal + evaluación multiescala), hipótesis H1-H4, fecha de entrega y formato del informe
- [ ] Respuesta registrada en docs/decisiones.md

---

## Fase 1 - Datos

**Milestone:** `Fase 1 - Datos` · **Inicio:** 2026-11-09 · **Fecha límite:** 2026-11-22  
**Objetivo:** Split por paciente congelado y 10 casos preprocesados verificados visualmente.

### T07 · Descargar FDG-PET-CT-Lesions y construir manifest.csv

**Componente:** Datos · **Tipo:** Logística · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-1` `datos` `logistica` `Dylan`  
**Depende de:** T02, T05

Obtener los datos y un manifiesto único con la lista de estudios.

- [ ] Descarga completa o de una muestra (si pesa demasiado: Plan B de 40-80 pacientes estratificados)
- [ ] manifest.csv con las columnas del contrato
- [ ] Licencia y condiciones de uso de la colección anotadas
- [ ] Datos compartidos con el equipo (dataset privado de Kaggle o Drive) para que nadie repita la descarga

### T08 · Filtrar estudios de linfoma y registrar exclusiones

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `Abel`  
**Depende de:** T07

Quedarse con los casos de linfoma y contar pacientes reales.

- [ ] Selección por diagnóstico en los metadatos
- [ ] Verificar temporalidad basal cuando sea posible
- [ ] Contar pacientes y estudios por separado (un paciente puede tener varios estudios)
- [ ] manifest_lymphoma.csv y registro de exclusiones con motivo

### T09 · QC de geometría y máscaras

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `calidad` `Abel`  
**Depende de:** T08

Detectar estudios inutilizables antes de entrenar.

- [ ] Verificar pares PET/CT, orientación, espaciado, máscaras vacías o corruptas
- [ ] results/qc_report.md con casos descartados y motivo

### T10 · Decidir esquema de partición según el número de pacientes

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-1` `decision` `todos`  
**Depende de:** T08

Reunión corta de los cuatro: el esquema depende de cuántos pacientes de linfoma haya de verdad.

- [ ] Menos de 120 pacientes: 5-fold CV para desarrollo + hold-out mínimo de test; 120 o más: 70/15/15
- [ ] Si se elige 5-fold: acordar cómo se reducen épocas/pasos y cómo se reparten los folds entre los cuatro
- [ ] Decisión documentada en docs/decisiones.md

### T11 · Implementar y congelar el split por paciente

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `Agustin`  
**Depende de:** T09, T10

Partición sin fuga, versionada. Desde aquí no se cambia.

- [ ] Agrupar por paciente antes de dividir; estratificar por presencia de lesión y cuantiles de TMTV si hay metadatos
- [ ] data/splits/splits.json con semilla 42, versionado en git
- [ ] Test unitario: ningún paciente aparece en dos conjuntos

### T12 · Preprocesado de PET: SUV, log1p y escalado robusto

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `Abel`  
**Depende de:** T09

Normalización de la modalidad metabólica.

- [ ] PET a SUV (o verificar el SUV existente) y guardar SUV original aparte para las métricas
- [ ] log1p(SUV) y escalado robusto por percentiles
- [ ] Función en src/lymphoma/data/preprocess.py con test unitario

### T13 · Preprocesado de CT y geometría: HU, resample a 3 mm y recorte de cuerpo

**Componente:** Datos · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `Dylan`  
**Depende de:** T09

Normalización anatómica y espacio común.

- [ ] CT recortado a [-1000, 1000] HU y escalado a [-1, 1]
- [ ] Resample de PET, CT y máscara a 3 mm isotrópico
- [ ] Recorte de cuerpo
- [ ] Función en src/lymphoma/data/preprocess.py con test unitario

### T14 · Caché de volúmenes y verificación visual de 10 casos

**Componente:** Datos · **Tipo:** Logística · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-1` `datos` `calidad` `logistica` `Abel`  
**Depende de:** T12, T13

Evitar repetir el preprocesado en cada sesión de GPU y comprobar que todo está bien alineado.

- [ ] Caché en data/processed/ con una corrida del pipeline completo
- [ ] 10 casos revisados visualmente (PET, CT y máscara superpuestos); cada integrante revisa 2-3 y deja su captura en el issue
- [ ] Caché subida a un dataset privado de Kaggle/Drive para usarla desde las sesiones de GPU de todos

---

## Fase 2 - Código base

**Milestone:** `Fase 2 - Código base` · **Inicio:** 2026-11-09 · **Fecha límite:** 2026-11-22  
**Objetivo:** Loader, modelo, loss, inferencia y métricas con tests pasando.

### T15 · Dataset y DataLoader MONAI

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `modelado` `Dylan`  
**Depende de:** T03

Cargar parches 3D desde splits.json y manifest.

- [ ] Muestreo de parches de 96³: 60% positivos, 40% negativos; opción de bajar a 80³
- [ ] Probado con 3-5 casos mientras Datos termina la caché

### T16 · Aumentaciones conjuntas

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `modelado` `Abel`  
**Depende de:** T15

Aumentaciones que mantienen PET, CT y máscara alineados.

- [ ] Flips, rotaciones pequeñas, escala de intensidad PET, ruido gaussiano leve
- [ ] Test unitario: PET, CT y máscara siguen alineados tras las transformaciones

### T17 · Modelo SegResNet compacto y variante PET-only

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-2` `modelado` `Ronald`  
**Depende de:** T15

Baseline y su ablación con la misma capacidad.

- [ ] init_filters=16, 4 niveles; variante de 2 canales (PET+CT) y de 1 canal (PET)
- [ ] Mismo número de parámetros salvo la capa de entrada

### T18 · Loss y bucle de entrenamiento con reanudación

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Ronald + Dylan · **Revisor:** Abel · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-2` `modelado` `entrenamiento` `Ronald` `Dylan`  
**Depende de:** T17

Entrenamiento robusto a cortes de sesión.

- [ ] Loss 0,5 Dice + 0,5 BCE con logits
- [ ] AdamW (LR 1e-4, weight decay 1e-5), mixed precision, validación cada 2-5 épocas, early stopping de 25 validaciones
- [ ] Criterio de mejor checkpoint (Dice + penalización FPV/FNV) definido y escrito ANTES de entrenar
- [ ] Checkpoint periódico y reanudación (las sesiones de Kaggle/Colab se cortan)

### T19 · Inferencia sliding-window

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `modelado` `evaluacion` `Dylan`  
**Depende de:** T17

Pasar de parches a estudios completos.

- [ ] Overlap 0,5; salida de probabilidad y máscara binaria
- [ ] Predicciones en NIfTI con la geometría de la referencia

### T20 · Métricas de vóxel

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `evaluacion` `Agustin`  
**Depende de:** T03

Dice, FPV y FNV correctos y probados.

- [ ] Dice, FPV y FNV en mL con el volumen físico del vóxel
- [ ] Casos negativos reportados aparte (tasa de cualquier FP y FPV por paciente)
- [ ] Tests con casos construidos a mano

### T21 · Métricas de lesión

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-2` `evaluacion` `Agustin`  
**Depende de:** T20

Detección por lesión con criterio declarado.

- [ ] Componentes conexas 26-conectadas en referencia y predicción
- [ ] Detectada si hay intersección e IoU > 0,10; variante con cualquier intersección como análisis de sensibilidad
- [ ] Sensibilidad por lesión, FP por paciente y desglose por volumen (<1 mL, 1-10 mL, >10 mL)
- [ ] Regla explícita para lesiones fusionadas o fragmentadas

### T22 · Métricas de TMTV

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `evaluacion` `estadistica` `Ronald`  
**Depende de:** T20

Acuerdo de TMTV frente a la referencia.

- [ ] TMTV predicho y de referencia; error absoluto y relativo
- [ ] Bland-Altman (sesgo y límites 95%) e ICC(A,1) con IC95%
- [ ] Spearman solo como complemento

### T23 · Tests unitarios y CI: cada persona testea lo que construyó

**Componente:** Base · **Tipo:** Técnica · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-2` `calidad` `todos`  
**Depende de:** T16, T19, T20, T21, T22

Red de seguridad antes de gastar horas de GPU.

- [ ] Cada integrante entrega los tests de sus módulos (transforms, split, métricas, matching de lesiones, inferencia)
- [ ] GitHub Actions corriendo pytest en cada PR

---

## Fase 3 - Baselines

**Milestone:** `Fase 3 - Baselines` · **Inicio:** 2026-11-23 · **Fecha límite:** 2026-12-01  
**Objetivo:** Baseline PET+CT y comparador PET-only entrenados; umbral y postprocesado congelados.

### T24 · Overfit de 2-4 casos y smoke test en las 4 cuentas

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-3` `entrenamiento` `todos`  
**Depende de:** T14, T18

Comprobar que el pipeline aprende y que funciona igual en las cuatro cuentas antes de gastar horas completas.

- [ ] Cada integrante corre 10-20 épocas en su propia cuenta de Kaggle/Colab y anota tiempo por época y VRAM
- [ ] La loss desciende y el modelo recupera las lesiones del microconjunto
- [ ] Si una época pasa de 3-4 min: reducir parche o pasos por época y acordar el cambio con todos

### T25 · Entrenar baseline PET+CT

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-3` `entrenamiento` `Ronald`  
**Depende de:** T24

Modelo de referencia del proyecto.

- [ ] configs/baseline_petct.yaml versionado
- [ ] 150-250 épocas máximas con early stopping, semilla 42
- [ ] Logs y mejor checkpoint guardados (fuera de git, con enlace en results/)

### T26 · Entrenar comparador PET-only

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-3` `entrenamiento` `Abel`  
**Depende de:** T24

Ablación que mide el valor de la CT, lanzada desde otra cuenta para repartir cuota de GPU.

- [ ] Mismo presupuesto de épocas, parche y semilla que el baseline PET+CT
- [ ] configs/baseline_petonly.yaml y logs guardados

### T27 · Análisis inicial en validación: vóxel y lesión

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-3` `evaluacion` `calidad` `Ronald`  
**Depende de:** T25, T26

Primera lectura de resultados, solo sobre validación.

- [ ] Dice, FPV, FNV, sensibilidad por lesión y FP/paciente de ambos modelos en validación (no test)
- [ ] Tabla comparativa PET+CT vs PET-only (insumo de H1)

### T28 · Revisión de falsos positivos fisiológicos y congelar umbral/postprocesado

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-3` `evaluacion` `calidad` `Ronald`  
**Depende de:** T25, T26

Entender los errores y fijar el postprocesado antes de tocar el test.

- [ ] Revisión de falsos positivos fisiológicos (cerebro, vejiga, riñones) con capturas
- [ ] Umbral y postprocesado del baseline congelados y documentados
- [ ] Cualquier regla de postprocesado es auditable (no borra órganos de forma rígida)

---

## Fase 4 - Mejoras

**Milestone:** `Fase 4 - Mejoras` · **Inicio:** 2026-12-02 · **Fecha límite:** 2026-12-08  
**Objetivo:** Variante con desalineación entrenada, semilla adicional y script de estadística listo.

### T29 · Implementar aumentación de desalineación (solo CT)

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-4` `modelado` `Agustin`  
**Depende de:** T16

Mejora principal de robustez.

- [ ] Traslación de ±2-6 vóxeles y rotación de ±3° aplicadas solo a CT, no a PET ni a la máscara
- [ ] 50% de las muestras alineadas
- [ ] Test unitario que confirma que PET y máscara no se mueven

### T30 · Entrenar variante con desalineación

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-4` `entrenamiento` `Agustin`  
**Depende de:** T25, T29

Misma configuración que el baseline salvo la aumentación.

- [ ] configs/misalign.yaml versionado
- [ ] Logs y checkpoint guardados

### T31 · Semilla adicional del baseline PET+CT (variabilidad entre semillas)

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-4` `entrenamiento` `Dylan`  
**Depende de:** T24

Estimar cuánto varía el resultado solo por la semilla, para no sobreinterpretar diferencias pequeñas. Si el cómputo falla, se recorta justo después de las tareas opcionales.

- [ ] Mismo config que T25 con semilla 43
- [ ] Logs y checkpoint guardados; resultados disponibles para T40

### T32 · Generador de tests con desplazamiento sintético

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-4` `evaluacion` `Ronald`  
**Depende de:** T19

Medir robustez de forma controlada.

- [ ] Versiones leve y moderada del test con la CT desplazada
- [ ] Baseline y variante se evalúan en test limpio, leve y moderado

### T33 · Script de estadística comparativa

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-4` `estadistica` `Abel`  
**Depende de:** T22

Dejar listo el análisis estadístico y probado con resultados de validación, para no improvisar con el test.

- [ ] Wilcoxon pareado (t pareado solo con justificación), bootstrap por paciente (1.000-2.000 réplicas), corrección de Holm
- [ ] Tamaño de efecto e IC95%, no solo p
- [ ] Probado con las predicciones de validación de T25/T26

### T34 · Precalcular máscaras de TotalSegmentator *(opcional)*

**Componente:** Modelo · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-4` `modelado` `opcional` `Ronald`  
**Depende de:** T14

Segunda mejora. Es de lo primero que se recorta si el calendario aprieta.

- [ ] Máscaras de cerebro, corazón, riñones y vejiga (si tarda más de 4 h, aplicar Plan B)
- [ ] Se usarán como canal auxiliar o penalización suave, nunca exclusión rígida

### T35 · Entrenar variante con prior anatómico *(opcional)*

**Componente:** Entrenamiento · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-4` `entrenamiento` `opcional` `Abel`  
**Depende de:** T25, T34

Comparar contra el baseline.

- [ ] configs/anatomic_prior.yaml versionado
- [ ] Logs y checkpoint guardados; comparación con el baseline en validación

---

## Fase 5 - Evaluación

**Milestone:** `Fase 5 - Evaluación` · **Inicio:** 2026-12-09 · **Fecha límite:** 2026-12-13  
**Objetivo:** Test ejecutado una sola vez; métricas, estadística y análisis de errores listos.

### T36 · Congelar todo y ejecutar el test una sola vez

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-5` `evaluacion` `decision` `Ronald`  
**Depende de:** T28, T30

Momento crítico de validez: el test se usa una vez. Los cuatro presentes (reunión corta).

- [ ] Confirmación escrita en el issue, firmada por los cuatro, de que arquitectura, umbral y postprocesado están congelados
- [ ] Inferencia en test de todas las variantes
- [ ] Predicciones y métricas guardadas en results/

### T37 · Métricas completas de vóxel y lesión en test

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-5` `evaluacion` `Agustin`  
**Depende de:** T36

Todas las métricas de vóxel y lesión sobre el test.

- [ ] Dice, FPV, FNV, sensibilidad por lesión, FP/paciente y desglose por tamaño
- [ ] CSV por paciente según el contrato

### T38 · Robustez bajo desplazamiento sintético

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-5` `evaluacion` `Agustin`  
**Depende de:** T32, T36

Evaluar H2: baseline y variante en test limpio, leve y moderado.

- [ ] Métricas en los tres escenarios
- [ ] Degradación relativa de Dice y FNV por modelo

### T39 · TMTV en test: Bland-Altman e ICC

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-5` `evaluacion` `estadistica` `Dylan`  
**Depende de:** T36

Evaluar H4 a nivel de paciente.

- [ ] TMTV predicho vs referencia, error absoluto y relativo
- [ ] Bland-Altman e ICC(A,1) con IC95% por modelo

### T40 · Estadística comparativa sobre test

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-5` `estadistica` `Abel`  
**Depende de:** T31, T33, T37, T39

Ejecutar el script de T33 con los resultados de test.

- [ ] Comparaciones pareadas con IC95%, tamaño de efecto y corrección de Holm
- [ ] Variabilidad entre semillas (T31) incluida
- [ ] Si el test tiene menos de 20 pacientes: solo estimaciones con IC, declaradas exploratorias

### T41 · Análisis de errores por tamaño y órgano

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-5` `evaluacion` `redaccion` `Abel`  
**Depende de:** T37

Entender por qué falla el modelo.

- [ ] 10 mejores y 10 peores casos con figuras
- [ ] Errores por tamaño de lesión y por órgano de captación fisiológica

### T42 · Cierre de hipótesis H1-H4

**Componente:** Evaluación · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-5` `redaccion` `Ronald`  
**Depende de:** T38, T40, T41

Decir con honestidad qué se confirmó y qué no.

- [ ] Tabla H1-H4: hipótesis, evidencia, confirmada/no confirmada/inconclusa
- [ ] Sin afirmaciones que el test no sostenga

---

## Fase 6 - Despliegue

**Milestone:** `Fase 6 - Despliegue` · **Inicio:** 2026-12-09 · **Fecha límite:** 2026-12-15  
**Objetivo:** ONNX validado, benchmark CPU y documentación; NPU solo si se mide.

### T43 · Exportar a ONNX y validar equivalencia

**Componente:** Despliegue · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-6` `despliegue` `Dylan`  
**Depende de:** T36

Exportación verificable del modelo final.

- [ ] Opset 17 y forma de parche fija
- [ ] Equivalencia numérica PyTorch vs ONNX Runtime CPU en 5-10 parches
- [ ] Si falla por operadores: exportar solo el núcleo y mantener sliding-window en PyTorch (Plan B)

### T44 · Benchmark de inferencia en CPU

**Componente:** Despliegue · **Tipo:** Técnica · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-6` `despliegue` `Abel`  
**Depende de:** T43

Costo real de inferencia en una laptop.

- [ ] Mediana y p95 de latencia por estudio y memoria pico
- [ ] Comparación PyTorch CPU vs ONNX Runtime CPU (Ryzen AI 7 350, 32 GB)

### T45 · Script de inferencia de demostración (ONNX → máscara + TMTV)

**Componente:** Despliegue · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-6` `despliegue` `Agustin`  
**Depende de:** T43

Una forma sencilla de usar el modelo final sobre un estudio nuevo.

- [ ] scripts/infer_demo.py: carga ONNX, corre sliding-window y guarda máscara NIfTI y TMTV
- [ ] Probado en un estudio del test y documentado en el README

### T46 · Documentar despliegue

**Componente:** Despliegue · **Tipo:** Logística · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-6` `despliegue` `redaccion` `logistica` `Ronald`  
**Depende de:** T44

Dejar por escrito lo medido, sin prometer lo que no se midió.

- [ ] docs/despliegue.md con tabla de latencia/memoria, equivalencia numérica y limitaciones
- [ ] Ninguna afirmación de NPU sin medición real

### T47 · Cuantización INT8 y prueba en NPU *(opcional)*

**Componente:** Despliegue · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-6` `despliegue` `opcional` `Dylan`  
**Depende de:** T44

Extensión. Solo se afirma lo que se mida.

- [ ] Cuantización estática con calibración representativa y recálculo de todas las métricas
- [ ] Aceptar solo si Dice mediana baja menos de 0,01, FNV sube menos de 5% relativo y no se pierden desproporcionadamente lesiones <1 mL
- [ ] Probar Vitis AI Execution Provider; registrar operadores en NPU y los que caen a CPU
- [ ] Si todo cae a CPU, reportarlo así y no afirmar aceleración

---

## Fase 7 - Informe y entrega

**Milestone:** `Fase 7 - Informe y entrega` · **Inicio:** 2026-11-09 · **Fecha límite:** 2026-12-20  
**Objetivo:** Informe verificado, repo reproducible y presentación lista. Colchón: 21-31 dic.

### T48 · Esqueleto del informe y adaptación del estado del arte

**Componente:** Informe · **Tipo:** Logística · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `redaccion` `logistica` `Agustin`  
**Depende de:** T03

Empezar a escribir temprano; el estado del arte ya está hecho.

- [ ] Estructura: introducción, estado del arte, datos, métodos, resultados, discusión, limitaciones, conclusiones
- [ ] docs/referencias/estado_del_arte.md adaptado al formato del informe sin perder las citas

### T49 · Sección de datos y preprocesado

**Componente:** Informe · **Tipo:** Técnica · **Responsable:** Agustin · **Revisor:** Dylan · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `redaccion` `Agustin`  
**Depende de:** T11, T14

Describir exactamente lo que se hizo con los datos.

- [ ] Cohorte, exclusiones, split, preprocesado y QC
- [ ] Cada decisión con su justificación

### T50 · Sección de modelo y entrenamiento

**Componente:** Informe · **Tipo:** Técnica · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `redaccion` `Ronald`  
**Depende de:** T18, T25

Describir exactamente cómo se construyó y entrenó el modelo.

- [ ] Arquitectura, loss, muestreo, aumentaciones, hiperparámetros y presupuesto de cómputo
- [ ] Cada decisión con su justificación

### T51 · Sección de evaluación, resultados y figuras

**Componente:** Informe · **Tipo:** Técnica · **Responsable:** Dylan · **Revisor:** Abel · **Esfuerzo:** L (~16 h)  
**Etiquetas:** `fase-7` `redaccion` `evaluacion` `Dylan`  
**Depende de:** T40, T41

Resultados trazables a archivos.

- [ ] Tablas y figuras generadas por script desde results/
- [ ] Ningún número copiado a mano

### T52 · Limitaciones y trabajo futuro

**Componente:** Informe · **Tipo:** Logística · **Responsable:** Ronald · **Revisor:** Agustin · **Esfuerzo:** S (~3 h)  
**Etiquetas:** `fase-7` `redaccion` `logistica` `Ronald`  
**Depende de:** T42

Honestidad metodológica.

- [ ] Un solo centro y un solo lector en la cohorte original; sin validación externa real
- [ ] Las perturbaciones sintéticas no equivalen a validación externa
- [ ] Predicción de respuesta como extensión condicionada a datos longitudinales
- [ ] Alcance real del resultado en NPU

### T53 · Reproducibilidad desde cero

**Componente:** Informe · **Tipo:** Logística · **Responsable:** Abel · **Revisor:** Ronald · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `calidad` `logistica` `Abel`  
**Depende de:** T44, T45

Que otra persona pueda repetirlo.

- [ ] README con pasos de principio a fin
- [ ] Manifest de reproducibilidad: versiones, semillas, hash de splits, configs usadas
- [ ] Se ejecuta desde cero en una máquina limpia siguiendo solo el README; cada fallo se reporta al responsable del módulo

### T54 · Verificación cruzada final del informe

**Componente:** Informe · **Tipo:** Técnica · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `calidad` `todos`  
**Depende de:** T51, T52

Cada persona verifica el trabajo de otra (anillo Ronald→Agustin→Dylan→Abel→Ronald).

- [ ] Cada cifra de la sección verificada coincide con su archivo de results/
- [ ] Cada integrante abre 3-4 referencias al azar de la sección que revisa y comprueba que dicen lo que se les atribuye
- [ ] Revisión del informe con /review del repo de skills de MatCom, si está instalado

### T55 · Entrega y presentación

**Componente:** Informe · **Tipo:** Técnica · **Responsable:** Todos · **Revisión:** cruzada · **Esfuerzo:** M (~8 h)  
**Etiquetas:** `fase-7` `entrega` `todos`  
**Depende de:** T54

Cierre del proyecto.

- [ ] Informe final y repo etiquetados v1.0
- [ ] Presentación preparada y ensayada
- [ ] Cada integrante puede defender cualquier parte del proyecto, no solo la suya

