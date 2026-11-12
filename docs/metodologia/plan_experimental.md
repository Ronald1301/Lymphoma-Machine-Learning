# Plan de implementación provisional

> **Propuesta preliminar.** Este plan es provisional y está sujeto a revisión en la siguiente fase del proyecto. El plazo, el hardware, la cohorte de entrenamiento y las mejoras propuestas se confirmarán con el profesor y el equipo antes de empezar la implementación.

## 1. Objetivo y alcance

Desarrollar y evaluar un baseline 3D para segmentación binaria de lesiones de linfoma en FDG-PET/CT basal, con una mejora principal de robustez y una mejora opcional. El resultado debe ser reproducible en una laptop Windows 11 con AMD Ryzen AI 7 350 y 32 GB de RAM para desarrollo, usando Kaggle o Colab para entrenamiento.

**No incluido:** predicción de respuesta o pronóstico. No se verificó un dataset público adecuado con pares longitudinales y etiquetas clínicas.

## 2. Datos

### 2.1 Cohorte

- Fuente principal: FDG-PET-CT-Lesions/autoPET [13,42].
- Seleccionar únicamente estudios identificados como linfoma según metadatos disponibles.
- Usar estudios basales cuando pueda verificarse temporalidad.
- Excluir estudios corruptos, sin PET/CT pareados o con geometría irrecuperable; conservar un registro de exclusión.

### 2.2 Partición

- Agrupar por paciente antes de dividir.
- Split sugerido: 70% entrenamiento, 15% validación, 15% test.
- Estratificar, si los metadatos lo permiten, por presencia de lesión y cuantiles de TMTV.
- Fijar semilla y guardar listas de identificadores.
- No usar el test hasta congelar arquitectura, umbral y postprocesado.

Si el número de pacientes de linfoma es menor de 120, usar 5-fold cross-validation para desarrollo y conservar un test externo o hold-out mínimo; si no existe cohorte externa, declarar la limitación.

## 3. Preprocesado

1. Convertir DICOM/NIfTI preservando orientación y espaciado.
2. Convertir PET a SUV cuando los metadatos lo permitan; si el dataset ya ofrece SUV, verificar distribución.
3. Recortar CT a [-1.000, 1.000] HU y escalar a [-1,1].
4. Para PET, aplicar `log1p(SUV)` y escalado robusto por percentiles; guardar SUV original para métricas.
5. Resamplear PET, CT y máscara a 2,0–3,0 mm isotrópicos. Empezar en 3 mm para ahorrar VRAM.
6. Recortar cuerpo y entrenar con parches centrados en lesión y parches negativos.
7. Cachear volúmenes preprocesados para no repetir SimpleITK en cada época.

## 4. Modelos

### 4.1 Baseline obligatorio

**SegResNet compacto de MONAI**:

- 2 canales: PET + CT.
- `init_filters=16` (subir a 24 solo si cabe).
- 4 niveles, deep supervision opcional desactivada inicialmente.
- Parches iniciales de 96×96×96 a 3 mm; bajar a 80³ si falta VRAM.
- Loss: 0,5 Dice + 0,5 BCE con logits.
- AdamW, LR 1e-4, weight decay 1e-5.
- Mixed precision en GPU.
- Sliding-window inference con overlap 0,5.

**Comparador mínimo:** PET-only con la misma arquitectura y presupuesto. Esta ablación demuestra el valor de CT sin confundirlo con mayor capacidad.

### 4.2 Mejora 1: aumentación de desalineación

Durante entrenamiento, aplicar aleatoriamente a CT —no a PET/máscara— una traslación de ±2–6 voxels y rotación pequeña de ±3°. Mantener 50% de muestras alineadas. Evaluar en:

- Test limpio.
- Test con shift sintético leve.
- Test con shift sintético moderado.

Hipótesis: menor degradación de Dice/FNV bajo shift, con pérdida no significativa en test limpio [23].

### 4.3 Mejora 2 opcional: prior anatómico

Si TotalSegmentator puede precomputarse dentro del plazo, crear canales binarios agregados para cerebro, corazón, riñones y vejiga, o una máscara de penalización suave. No excluir rígidamente órganos. Comparar:

- Baseline PET+CT.
- Baseline + prior anatómico.

Si el cómputo no alcanza, usar reglas simples de connected components y una máscara corporal; documentarlo como Plan B.

## 5. Muestreo y entrenamiento

- Parches positivos: 60%; negativos: 40%.
- Aumentaciones conjuntas: flips, rotaciones pequeñas, escala de intensidad PET, ruido gaussiano leve.
- Aumentación de desalineación solo en CT.
- 150–250 épocas máximas, con validación cada 2–5 épocas y early stopping de 25 validaciones.
- Entrenar una semilla por configuración durante selección. Repetir 3 semillas solo para baseline y mejora final si hay tiempo.
- Guardar mejor checkpoint por combinación de Dice + penalización de FPV/FNV, definida antes de entrenar.

## 6. Métricas

### 6.1 Vóxel/volumen

- Dice por paciente, mediana e IQR.
- FPV y FNV en mL.
- Precision y recall voxelar como secundarias.
- Casos negativos: reportar por separado tasa de cualquier FP y FPV/paciente.

### 6.2 Lesión

- Connected components 26-conectadas en referencia y predicción.
- Lesión detectada si existe intersección y `IoU > 0,10`; repetir sensibilidad con criterio de cualquier intersección como análisis de sensibilidad.
- Sensibilidad por lesión.
- FP por paciente.
- Resultados por volumen: <1 mL, 1–10 mL, >10 mL.

### 6.3 TMTV

- TMTV predicho y de referencia en mL.
- Error absoluto y relativo, mediana e IQR.
- Bland–Altman: sesgo medio y límites 95%.
- ICC(A,1) de acuerdo absoluto con IC95%.
- Correlación Spearman solo como complemento; no sustituye acuerdo.

## 7. Estadística

- Comparar configuraciones sobre los mismos pacientes.
- Dice/FPV/FNV/TMTV: Wilcoxon pareado si no hay normalidad; t pareado solo con justificación.
- Sensibilidad de lesión: bootstrap por paciente, no por lesión aislada, para respetar clustering.
- FP por paciente: bootstrap pareado o prueba de rangos.
- Intervalos de confianza: bootstrap de 1.000–2.000 réplicas por paciente.
- Corregir comparaciones múltiples con Holm para las dos mejoras y las métricas primarias.
- Reportar tamaño de efecto y diferencia con IC95%, no solo `p`.
- No realizar pruebas inferenciales si el test tiene menos de 20 pacientes; usar estimaciones con IC y declararlas exploratorias.

## 8. Presupuesto de cómputo

### Laptop CPU

- Inspección DICOM/NIfTI, QC y preprocesado de 3–10 casos.
- Tests unitarios de transforms y métricas.
- Inferencia de parches pequeños.
- Exportación ONNX y benchmark CPU.
- No entrenar volúmenes 3D completos.

### Kaggle/Colab GPU gratuita

Suposición conservadora: T4 o P100 con 16 GB y sesiones de 9–12 h.

| Trabajo | Estimación | VRAM objetivo |
|---|---:|---:|
| Preprocesado/caché | 1–3 h de CPU | RAM 12–24 GB |
| Smoke test 10–20 épocas | 0,5–1,5 h | 8–12 GB |
| Baseline PET+CT 150–250 épocas | 6–10 h | 10–15 GB |
| PET-only | 5–9 h | 8–14 GB |
| Mejora misalignment | 6–10 h | 10–15 GB |
| Prior anatómico opcional | 6–10 h + precomputado | 10–15 GB |
| Inferencia test + métricas | 0,5–2 h | 6–10 GB |

Las cifras son estimaciones de planificación, no resultados medidos. Si una época supera 3–4 minutos, reducir parches/steps y usar early stopping para caber en una sesión.

## 9. Exportación e inferencia

1. Exportar checkpoint final a ONNX con opset 17 y shape de parche fija [44,45].
2. Validar equivalencia numérica PyTorch vs ONNX Runtime CPU en 5–10 parches.
3. Ejecutar sliding-window en CPU y medir mediana/p95 por estudio y memoria pico.
4. Probar cuantización INT8 estática solo si existe calibración representativa [43].
5. Recalcular todas las métricas después de cuantizar.
6. Probar Vitis AI Execution Provider en Windows como extensión; registrar operadores enviados a NPU y fallback a CPU [44].

Criterio de aceptación de cuantización: descenso de Dice mediana <0,01, aumento de FNV <5% relativo y ausencia de pérdida desproporcionada en lesiones <1 mL. Si no se cumple, conservar FP32.

## 10. Tareas

### Datos y reproducibilidad

- Descargar una muestra y verificar licencias/metadatos.
- Construir manifiesto por paciente.
- Implementar preprocesado y QC.
- Congelar split.

**Salida:** 10 casos preprocesados y visualmente verificados.

### Baseline mínimo

- Implementar dataset/loader, loss y métricas.
- Overfit de 2–4 casos.
- Smoke test de 10–20 épocas en GPU.

**Criterio:** loss desciende y el modelo recupera lesiones del microconjunto.

### Baseline completo

- Entrenar PET+CT.
- Ajustar solo LR, parche o sampling si hay fallo evidente.
- Congelar checkpoint y umbral en validación.

### Ablación PET-only y análisis inicial

- Entrenar PET-only con mismo presupuesto.
- Comparar validación y revisar FP fisiológicos.

### Mejora principal

- Entrenar PET+CT con aumentación de desalineación.
- Ejecutar stress tests de shift.
- Solo si termina temprano, precomputar prior anatómico.

### Test y estadística

- Ejecutar inferencia una vez en test.
- Calcular métricas voxel/lesión/paciente.
- Bland–Altman, ICC, bootstrap y análisis por tamaño.
- Revisar 10 mejores y 10 peores casos.

### Despliegue y entrega

- Exportar ONNX.
- Benchmark CPU; NPU opcional.
- Completar tablas, figuras, limitaciones y manifest de reproducibilidad.
- Verificar que números del informe coincidan con archivos de resultados.

## 11. Riesgos y Plan B

| Riesgo | Señal temprana | Plan B |
|---|---|---|
| Descarga/datos demasiado grandes | La preparación de datos no termina | Trabajar con 40–80 pacientes estratificados y declarar estudio piloto |
| Pocos casos identificables como linfoma | Metadatos insuficientes | Usar cohorte oncológica general para preentrenar y evaluar solo casos de linfoma disponibles |
| OOM en T4 | Parche 96³ no cabe | 80³, `init_filters=12`, gradient accumulation |
| Entrenamiento >12 h | Época demasiado lenta | 150 épocas, menos samples/epoch, early stopping, una semilla |
| TotalSegmentator no cabe | Precomputado tarda >4 h | Omitir mejora 2; usar solo misalignment |
| FP fisiológicos altos | FPV dominada por vejiga/cerebro | Postprocesado auditable y análisis por órgano; no borrar rígidamente |
| ONNX falla por operadores | Export error o discrepancia | Exportar núcleo del modelo con shape fija; mantener PyTorch para sliding-window |
| NPU hace fallback completo | 0% de subgrafos en NPU | Reportar CPU ONNX; no afirmar aceleración NPU |
| Test demasiado pequeño | IC muy anchos | Presentar resultados exploratorios y bootstrap, sin sobreinterpretar p-values |

## 12. Criterios de finalización

- Split por paciente congelado y versionado.
- Baseline PET+CT y comparador PET-only completados.
- Mejora de desalineación evaluada en test limpio y perturbado.
- Dice, FPV, FNV, sensibilidad por lesión, FP/paciente y TMTV reportados.
- Bland–Altman e ICC incluidos.
- Errores por tamaño y captación fisiológica revisados.
- Exportación ONNX validada o fallo documentado.
- Ninguna afirmación de NPU sin medición real.
