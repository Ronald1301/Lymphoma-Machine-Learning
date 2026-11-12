# Brechas y oportunidades

## Tesis

El proyecto se justifica mejor como un estudio de **segmentación basal de lesiones de linfoma en FDG-PET/CT con evaluación clínica multiescala**, no como un predictor de respuesta. La razón es empírica: existen máscaras públicas y benchmarks para segmentación/TMTV, pero no se verificó un dataset abierto que combine pares longitudinales pre/post, máscaras y etiquetas clínicas de respuesta Deauville/Lugano suficientemente grandes para entrenar y validar un predictor.

## Brechas prioritarias

### 1. Generalización específica de linfoma

El dataset autoPET aporta escala, pero mezcla melanoma, cáncer de pulmón y linfoma, y la cohorte original procede de un único centro/escáner. En el estudio específico de 611 casos, SegResNet obtuvo Dice mediana 0,68 y FPV mediana 21,46 mL en un test externo de 145 casos [19]. autoPET III confirma que ver un centro y un trazador por separado no garantiza rendimiento en su combinación inédita [22].

**Oportunidad:** entrenar en un subconjunto de linfoma con split estricto por paciente y reservar un conjunto externo o fuera de distribución. Si solo existe un centro, simular perturbaciones realistas y declarar que no equivalen a validación externa.

### 2. Dice no captura detección ni cuantificación

Una máscara puede obtener buen Dice por masas grandes y omitir lesiones pequeñas. También puede conservar TMTV global con errores espaciales compensados. El benchmark internacional muestra que la concordancia de TMTV y el acuerdo voxelar son preguntas distintas [15,18].

**Oportunidad:** reportar Dice, FPV, FNV, sensibilidad por lesión, falsos positivos por paciente y error de TMTV. Añadir Bland–Altman e ICC con intervalos de confianza.

### 3. Captación fisiológica y anatomía

Cerebro, corazón, hígado, bazo, riñones, uréteres y vejiga son fuentes recurrentes de falsos positivos. TotalSegmentator ofrece máscaras anatómicas en CT [30], mientras el ganador de autoPET III utilizó supervisión auxiliar de órganos [23]. Sin embargo, excluir órganos rígidamente puede borrar enfermedad extranodal.

**Oportunidad:** usar máscaras anatómicas como prior suave, feature auxiliar o postprocesado auditable. Medir FPV por región anatómica y documentar errores de exclusión.

### 4. Desalineación PET/CT

PET y CT pueden quedar desalineados por respiración, movimiento o adquisición secuencial. La fusión temprana suele asumir correspondencia perfecta. La aumentación de desalineación fue una de las técnicas del ganador model-centric de autoPET III [23].

**Oportunidad:** introducir desplazamientos/rotaciones pequeñas en una sola modalidad durante entrenamiento y realizar una ablación controlada. Es una mejora barata y directamente relacionada con robustez.

### 5. Lesiones pequeñas y efecto de volumen parcial

Lesiones pequeñas contienen pocos vóxeles y sufren pérdida de contraste. Dice es inestable en ese régimen, y la sensibilidad puede depender del criterio de matching.

**Oportunidad:** estratificar por volumen y reportar sensibilidad con un criterio explícito de intersección o IoU. Mantener una curva sensibilidad–FP/paciente en lugar de un solo umbral.

### 6. Incertidumbre sin calibración

Ensembles y test-time augmentation producen variación, pero la mayoría de estudios no demuestra calibración ni define abstención clínica.

**Oportunidad:** calibrar la probabilidad de candidatos en validación, medir Brier/ECE y evaluar cobertura–riesgo. Marcar casos con alta incertidumbre para revisión.

### 7. Predicción clínica con evidencia desigual

DLBCL domina la literatura de radiómica y pronóstico. Hodgkin y, sobre todo, folicular tienen menos validación externa automatizada [38,39]. Los estudios retrospectivos informan AUC/C-index, pero no prueban mejora de decisiones.

**Oportunidad:** limitar las conclusiones a cuantificación y preparar biomarcadores reproducibles para futuros estudios. La predicción de respuesta debe ser una fase posterior con datos longitudinales adecuados.

### 8. Eficiencia y NPU

ONNX Runtime y Ryzen AI permiten exportación, cuantización y partición NPU/CPU [43–45], pero no se encontró un benchmark publicado de un modelo 3D PET/CT completo en la NPU del Ryzen AI 7 350.

**Oportunidad:** medir una prueba de concepto: PyTorch CPU vs ONNX Runtime CPU, y NPU solo si los operadores se asignan realmente. Informar latencia, memoria, exactitud y porcentaje de fallback a CPU.

## Hipótesis defendibles para el proyecto

1. Un SegResNet 3D compacto con PET+CT supera un baseline PET-only en Dice y FNV sin aumentar excesivamente FPV.
2. La aumentación de desalineación reduce la degradación bajo shifts sintéticos PET/CT sin perjudicar significativamente el test limpio.
3. Un prior anatómico suave reduce FPV en órganos fisiológicos sin reducir sensibilidad de lesiones extranodales.
4. La mejora de Dice no garantiza mejor acuerdo de TMTV; ambas métricas deben analizarse por separado.

## Contribución propuesta

- Pipeline reproducible de preprocesado y split por paciente.
- Baseline público y realizable en GPU gratuita.
- Una mejora principal: aumentación de desalineación.
- Una segunda mejora opcional: prior anatómico simple.
- Evaluación a nivel de vóxel, lesión y paciente.
- Análisis de errores por tamaño y órgano.
- Exportación ONNX como demostración de despliegue, sin prometer aceleración NPU no medida.

## Riesgos de sobreafirmación que deben evitarse

- Llamar “dataset público” a CALGB 50303; se verificó la publicación, no la descarga de imágenes.
- Presentar TotalSegmentator o MedSAM como validados para tumor FDG de linfoma.
- Comparar Dice de autoPET III, del estudio de 611 casos y del benchmark TMTV como si compartieran test.
- Inferir beneficio clínico prospectivo a partir de una validación retrospectiva.
- Usar “respuesta” como sinónimo de segmentación basal o cambio de TMTV sin etiquetas clínicas.
