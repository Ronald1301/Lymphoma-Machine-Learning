# Guía de tareas de Ronald

Esta guía resume las tareas asignadas a Ronald, las dependencias que las desbloquean y qué puedes preparar mientras esperas. La fuente de verdad del reparto es [`issues_tareas.md`](issues_tareas.md); respeta también los contratos de [`docs/contratos.md`](../contratos.md) y el diseño de [`plan_experimental.md`](../metodologia/plan_experimental.md).

## Cómo funciona el ciclo de PR

Los usernames se contrastaron con la lista de colaboradores de GitHub y con la actividad del repositorio:

| Autor | Revisor requerido | Username confirmado |
|---|---|---|
| Ronald | Agustín | `agustin030902` |
| Agustín | Dylan | `Dylan2108` |
| Dylan | Abel | `amircalabel` |
| Abel | Ronald | `Ronald1301` |

1. Crea una rama `feat/<tema>` desde `main` y un PR por tarea.
2. Usa commits en inglés con `type(Txx): short description` y un título de PR `[Txx] ...`.
3. El workflow `PR review cycle` solicita al siguiente integrante del anillo. El check `review-cycle` falla hasta que ese reviewer apruebe el último commit; una aprobación anterior no basta después de un nuevo push.
4. La protección de `main` exige PR, una aprobación y conversaciones resueltas. El check `review-cycle` verifica que la aprobación sea de la persona correcta.
5. El coordinador semanal fusiona después de la aprobación correcta y de que pasen los checks. La aprobación se puede imponer técnicamente; quién pulsa «Merge» no se puede seleccionar dinámicamente por autor en la protección actual del repositorio personal, así que esa parte sigue siendo norma del equipo.

### Estado de instalación

El PR de configuración se abre desde una rama y se solicita a Agustín. No lo aprobaré ni fusionaré en nombre del revisor. El check nuevo solo se puede añadir a los checks obligatorios de `main` después de que Agustín apruebe y fusione ese PR: el workflow debe estar en la rama predeterminada para servir de requisito estable. La protección básica de PR y aprobación puede activarse antes. Una vez integrado, se agrega `review-cycle` a los checks obligatorios y se vuelve a verificar la regla.

## Tareas asignadas

«Depende de» lista las dependencias directas del plan. «Por qué esperar» explica qué salida hace falta; «mientras tanto» indica trabajo útil que no cambia decisiones prematuramente.

| Tarea | Issue | Alcance de Ronald | Depende de | Por qué esperar / qué puedes hacer mientras tanto |
|---|---:|---|---|---|
| T01 | #1 | Crear estructura y `.gitignore` | — | Ya está integrada en `main`; no repetirla. |
| T05 | #2 | Parte de todos: verificar cómputo y acceso a datos | — | Tu Kaggle no deja seleccionar GPU y `CUDA` dio `False`. Verifica teléfono y cuota; no marques GPU operativa hasta que PyTorch detecte una. El equipo debe acordar muestra y almacenamiento. |
| T06 | #3 | Confirmar alcance, hipótesis, fecha y formato con el profesor | — | El borrador existe, pero falta respuesta. Puedes preparar el resumen para validar; no cierres T06 ni presentes principios de enero como fecha confirmada. |
| T10 | #17 | Decisión compartida del split; Ronald coordina | T08 | Espera el conteo de pacientes con linfoma, no el número de estudios. Prepara la reunión: <120 pacientes, 5-fold CV + hold-out; ≥120, 70/15/15. Si test <20, declarar exploratorio. |
| T17 | #13 | SegResNet PET+CT y PET-only | T15 | El DataLoader define forma y contrato de entrada. Revisa la arquitectura mientras tanto; implementa con interfaz estable. |
| T18 | #18 | Loss, validación y mejor checkpoint, con Dylan | T17 | La loss necesita logits y salida del modelo. Coordina reparto: Ronald loss/selección, Dylan loop/checkpoint/logging. |
| T22 | #15 | Métricas de TMTV | T20 | Espera las métricas voxelarias para integrar formatos. Puedes preparar casos manuales de volumen, Bland–Altman e ICC. |
| T23 | #25 | Tests/CI de tus módulos y parte de todos | T16, T19, T20, T21, T22 | Integra cuando existan transforms, inferencia y métricas. Mientras, planifica casos sintéticos; no marques CI completa. |
| T24 | #28 | Smoke test en Kaggle con todos | T14, T18 | Requiere casos procesados y loop que guarde/reanude. Habilita tu GPU; mientras, revisa el runner sin lanzar entrenamiento. |
| T25 | #31 | Entrenar baseline PET+CT | T24 | Espera smoke test, caché accesible y criterio de checkpoint fijado. Requiere GPU; prepara config y reanudación, no entrenes en CPU. |
| T27 | #34 | Analizar validación PET+CT vs PET-only | T25, T26 | Espera ambos modelos y predicciones de validación. Usa solo validación, nunca test para elegir parámetros. |
| T28 | #35 | Revisar falsos positivos y congelar umbral/postprocesado | T25, T26 | Necesita predicciones de ambos baselines en validación. Prepara la revisión; no fijes umbral con test. |
| T32 | #26 | Generar perturbaciones sintéticas | T19 | Espera interfaz de inferencia. El shift afecta solo CT; puedes revisar niveles y casos de prueba. |
| T34 *(opcional)* | #29 | Precalcular prior anatómico | T14 | Requiere volúmenes procesados y solo se hace si hay tiempo; prioriza la ruta principal. |
| T36 | #39 | Congelar configuración y usar test una sola vez | T28, T30 | Espera postprocesado congelado y variante de desalineación. Prepara hashes y coordinación; no abras test antes. |
| T42 | #48 | Cerrar H1–H4 con evidencia | T38, T40, T41 | Espera robustez, estadística y análisis de errores. Puedes preparar la tabla sin veredictos. |
| T46 | #49 | Documentar despliegue | T44 | Espera benchmark medido; prepara el formato, no inventes latencias. |
| T50 | #38 | Escribir sección de modelo/entrenamiento | T18, T25 | Espera loss, config y logs reales. Puedes redactar metodología cualitativa; las cifras salen de artefactos. |
| T52 | #53 | Limitaciones y trabajo futuro | T42 | Espera el cierre de hipótesis para delimitar afirmaciones. Puedes bosquejar limitaciones conocidas. |
| T54 | #54 | Revisión cruzada del informe | T51, T52 | Espera resultados de Dylan y tu sección de limitaciones. Prepara lista de cotejo de citas y cifras. |
| T55 | #55 | Entrega/presentación con todos | T54 | Espera revisión final. Reúne materiales, pero no etiquetes ni declares entrega antes del visto bueno. |

## Qué hacer ahora en fase 1

Tu tarea propia de fase 1 es T10, compartida. También eres revisor de T08 y T09.

1. Coordina si Dylan prepara una muestra de 40–80 pacientes o propone otra fuente. No se descargará AutoPET completo; hay que filtrar diagnósticos y acordar almacenamiento compartido.
2. Agustín es responsable de T02, prerequisito de T07. Confirma que complete `requirements.txt` con versiones fijadas y el entorno de Windows/Kaggle.
3. Dylan prepara T07 y `manifest.csv`; Abel filtra linfoma y hace QC (T08/T09). Tú revisas exclusiones, geometría y máscaras.
4. Cuando Abel entregue pacientes únicos, lidera T10 y registra conteo, esquema de split y acuerdo sobre folds/épocas en `docs/decisiones.md`.
5. Agustín implementa y congela T11 por paciente, con semilla 42. Abel/Dylan avanzan PET/CT (T12/T13) tras QC; Abel prepara caché y revisión visual de 10 casos (T14).

No crees ni congeles `data/splits/splits.json` antes del manifiesto filtrado y la decisión T10. El objetivo de fase 1 es un split congelado y 10 casos preprocesados y revisados visualmente.
