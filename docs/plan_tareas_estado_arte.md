# Plan de tareas para el estado del arte

**Objetivo:** producir una revisión crítica, verificable y reproducible sobre detección, segmentación y evaluación de lesiones de linfoma en FDG-PET/CT, con énfasis en 2022–2026 y un plan experimental realizable en siete días.

## Criterios de inclusión

- Fuentes primarias o páginas oficiales: PubMed/PMC, editoriales de revistas, arXiv, TCIA, Grand Challenge y repositorios oficiales.
- Referencias con título, autores, año, venue y DOI, PMID o arXiv ID comprobados abriendo la fuente.
- Mínimo 40 referencias; al menos 15 de 2024–2026 y al menos 10 específicas de linfoma.
- Toda cifra se conservará junto con su contexto experimental y fuente.
- Se excluirán referencias que no puedan verificarse o cuyos metadatos/resultados sean ambiguos.

## Paquetes de trabajo paralelos

1. **Clínica y biomarcadores:** Lugano, Deauville, MTV/TMTV/TLG, SUV, Dmax, heterogeneidad y evidencia pronóstica por subtipo.
2. **Segmentación clásica y fiabilidad:** umbrales, métodos semiautomáticos, variabilidad interobservador y benchmark TMTV de 60 casos.
3. **Deep learning y arquitecturas:** U-Net 3D, nnU-Net/ResEncL, SegResNet, DynUNet, SwinUNETR, transformers, cascadas y fusión PET/CT.
4. **Benchmarks y datasets:** autoPET I–III, HECKTOR, TCIA, CALGB 50303 y datasets públicos adicionales.
5. **Detección, métricas y robustez:** evaluación por vóxel/lesión/paciente, TMTV, cambio de dominio, incertidumbre, sesgos y explicabilidad.
6. **Más allá de segmentación:** AutoLugano, Deauville automático, radiómica y predicción de respuesta/pronóstico.
7. **Eficiencia y despliegue:** modelos ligeros, cuantización, ONNX, CPU/NPU y costos computacionales publicados.
8. **Tendencias 2024–2026:** modelos fundacionales, preentrenamiento multimodal, TotalSegmentator como prior y generalización multitrazador.

## Consolidación y control de calidad

1. Unificar registros bibliográficos y eliminar duplicados.
2. Abrir cada fuente seleccionada y cotejar metadatos, cohortes, particiones y cifras.
3. Construir `referencias.bib` y asignar claves estables.
4. Redactar `tabla_comparativa.csv` con un estudio por fila y contexto de cada métrica.
5. Redactar `estado_del_arte.md`, `gaps_y_oportunidades.md` y `plan_experimental.md`.
6. Ejecutar una segunda pasada cruzada: cada cita del texto debe existir en BibTeX; cada cifra debe coincidir con la fuente; cada referencia BibTeX debe estar citada o justificada.
7. Documentar explícitamente fuentes no verificables, datos no reportados y trabajos descartados.

## Criterio de finalización

Los cinco entregables solicitados existen en `docs/`, cumplen los mínimos bibliográficos, no contienen cifras sin contexto y pasan una auditoría final de citas, URLs, DOI/arXiv/PMID, CSV y coherencia interna.
