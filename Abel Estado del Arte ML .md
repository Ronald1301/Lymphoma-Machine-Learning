# Optimización de detección y evaluación de lesiones en linfomas mediante PET/CT

Nota sobre la nomenclatura: el tema original consigna “PCT”; en la literatura científica sobre linfomas, la modalidad de imagen que integra tomografía por emisión de positrones y tomografía computarizada se denomina PET/CT. Se adopta esta denominación por corresponder al estándar terminológico del campo.

---

## 1. Introducción y delimitación del problema

La PET/CT con 18F-FDG constituye la modalidad de referencia para la estadificación y evaluación de respuesta en la mayoría de los linfomas FDG-ávidos, incluyendo el linfoma de Hodgkin (LH), el linfoma folicular (LF) y el linfoma difuso de células B grandes (DLBCL) . En este contexto, la optimización de la detección y evaluación de lesiones se articula en torno a un problema central identificado de manera consistente en la literatura reciente: la segmentación precisa y automatizada de las lesiones tumorales constituye el cuello de botella que impide la adopción generalizada de biomarcadores cuantitativos como el volumen tumoral metabólico total (TMTV) .

El valor pronóstico del TMTV está ampliamente validado en múltiples subtipos de linfoma. Sin embargo, su cálculo requiere delimitar cada lesión hipermetabólica en imágenes de cuerpo entero, tarea que en la práctica clínica se realiza de forma manual o semiautomática, con alta variabilidad interobservador y elevado costo temporal . La literatura de los últimos cinco años documenta tres líneas de trabajo convergentes para resolver este problema: el desarrollo de arquitecturas de aprendizaje profundo para segmentación automatizada, la validación pronóstica de métricas volumétricas en cohortes amplias, y la exploración de características radiómicas que trascienden el volumen tumoral. A continuación se presenta el estado actual de cada línea, con sus referencias y el balance entre lo consolidado y lo pendiente.

---

## 2. Segmentación automatizada de lesiones: el estado de la técnica

### 2.1 Arquitecturas dominantes y su rendimiento

Los métodos de deep learning basados en arquitecturas U-Net y sus variantes se han consolidado como el enfoque dominante para la segmentación de lesiones linfomatosas en PET/CT. Una revisión sistemática reciente que sintetizó 53 estudios originales de los últimos cinco años clasificó las aplicaciones de inteligencia artificial en PET/CT de linfomas en tres módulos: segmentación y cuantificación automatizada (n=22), diagnóstico diferencial y subtipificación (n=11), y predicción de respuesta y pronóstico (n=24) . El predominio del módulo de segmentación confirma su carácter habilitante para los demás.

Jiang et al. demostraron que un modelo de red neuronal convolucional completamente convolucional con arquitectura 3D U-Net segmenta con precisión lesiones linfomatosas en PET de pacientes con DLBCL . Sin embargo, la misma revisión señala una limitación persistente: los métodos de segmentación basados en IA exhiben precisión deficiente en lesiones linfomatosas de pequeño tamaño . Para abordar esta deficiencia, se han propuesto mejoras arquitectónicas específicas. Izadi et al. integraron U-Net con DenseNet y una función de pérdida Tversky, logrando reducir la pérdida de red para lesiones muy pequeñas y mejorar la precisión y robustez de la segmentación en LH . Wang et al. propusieron una red con regularización de desplazamiento previo (PSR-Net) para mejorar el rendimiento en conjuntos de datos con grave desequilibrio de clases .

### 2.2 Validación en conjuntos de datos de referencia

Un estudio de validación publicado en 2026 en el Journal of Nuclear Medicine evaluó un modelo de IA sobre un conjunto de datos de referencia público de PET/CT de linfoma. Los resultados mostraron que en el 83% de los casos (50/60), el TMTV derivado por IA coincidió con el TMTV de referencia, valor cercano al 87% de concordancia reportado entre el TMTV de referencia final y los lectores expertos que participaron en la construcción del propio benchmark . En 4 casos adicionales, la segmentación de IA se desvió de la referencia pero coincidió con al menos uno de los lectores expertos. Los autores señalan que el conjunto de datos estaba deliberadamente enriquecido con casos complejos, lo que hace particularmente alentadores los resultados, y que el modelo fue entrenado con 1.500 estudios PET/CT de múltiples hospitales . No obstante, los propios autores advierten que la validación se realizó únicamente sobre estudios basales y que se requiere validación externa en otros contextos clínicos (estadificación, evaluación de respuesta) .

### 2.3 Balance de esta línea

La segmentación automatizada mediante IA existe y ha alcanzado un grado de madurez técnica considerable, con valores de concordancia cercanos a los de lectores humanos expertos en conjuntos de datos de referencia. Sin embargo, no constituye una tecnología resuelta: las deficiencias en lesiones pequeñas persisten, la validación se ha realizado mayoritariamente sobre datos de un solo tipo (estudios basales) y la generalización a diferentes escáneres, protocolos y subtipos de linfoma requiere confirmación adicional .

---

## 3. Cuantificación volumétrica metabólica: validación pronóstica del TMTV

### 3.1 Linfoma folicular

Un metaanálisis publicado en 2025 evaluó el valor pronóstico del TMTV basal en linfoma folicular de alta carga tumoral, incluyendo 11 estudios con 2.631 pacientes. Un TMTV elevado se asoció significativamente con peor supervivencia libre de progresión (HR agrupado = 1,91; IC 95%: 1,59–2,29), peor supervivencia global (HR = 1,78; IC 95%: 1,33–2,37) y mayor riesgo de progresión dentro de 24 meses (OR = 3,72; IC 95%: 2,22–6,23). El punto de corte más validado fue >510 cm³. En análisis multivariados, el TMTV permaneció independiente de índices clínicos como FLIPI y PRIMA-PI. La combinación de TMTV con β2-microglobulina estratificó a los pacientes en grupos de riesgo con supervivencia global a 5 años que osciló entre 96,1% y 73,7% . Los autores concluyen que el TMTV basal es un biomarcador pronóstico reproducible e independiente, pero que la validación prospectiva y la estandarización metodológica son cruciales para una implementación más amplia .

Un segundo metaanálisis, con 16 estudios y 2.313 pacientes, confirmó que tanto el volumen tumoral metabólico (MTV) como la glucólisis lesional total (TLG) son predictores independientes robustos de SLP y SG en LF. El TLG mostró un rendimiento pronóstico incluso superior al MTV (HR para SG = 9,71; IC 95%: 3,47–27,20), mientras que el SUVmax tuvo utilidad predictiva limitada: se asoció con SLP (HR = 2,14) pero no con SG . Los autores señalan que la validación de puntos de corte estandarizados y la incorporación de biomarcadores moleculares son necesarias para mejorar la precisión pronóstica .

### 3.2 Linfoma de Hodgkin

Una revisión publicada en Clinical and Translational Imaging (2022) sobre TMTV basal en LH clásico, que incluyó 26 estudios, concluyó que un TMTV elevado en PET/CT basal se asocia con peor SLP y SG en enfermedad en estadio temprano, y predice fallo terapéutico tras trasplante autólogo en enfermedad recaída/refractaria. Sin embargo, en enfermedad avanzada tratada con eBEACOPP no se encontró asociación estadísticamente significativa entre TMTV elevado y reducción de SLP o SG. Los autores señalan que no existe acuerdo sobre cuál es el mejor método de segmentación del TMTV, aunque independientemente del método elegido, este puede predecir el pronóstico con precisión comparable .

### 3.3 DLBCL: PET interino y el papel del criterio de interpretación

Un metaanálisis actualizado publicado en 2026 evaluó el valor pronóstico del PET/CT interino en DLBCL, incluyendo 66 artículos con 9.335 pacientes. La tasa agrupada de respuesta metabólica completa fue 67,2%, con heterogeneidad extrema (I² = 92,45%). Para SLP, el HR agrupado de un PET interino positivo fue 3,05 (IC 95%: 2,63–3,54). Un hallazgo relevante para la optimización: al utilizar exclusivamente el umbral de Deauville score 5, el HR se elevó a 5,72 (IC 95%: 4,35–7,51), con heterogeneidad más moderada (I² = 40,7%). El ΔSUVmax mostró un efecto pronóstico más débil (HR = 1,83). Los escaneos realizados tras 4 ciclos mostraron un rendimiento ligeramente superior a los realizados tras 2 ciclos . Los autores concluyen que el PET interino, particularmente con el umbral DS 5, es un biomarcador sólido para identificar pacientes de alto riesgo .

### 3.4 Balance de esta línea

La cuantificación volumétrica metabólica existe y cuenta con validación pronóstica robusta en múltiples subtipos. El TMTV y el TLG han demostrado asociación independiente con desenlaces en LF, LH y DLBCL. Sin embargo, la heterogeneidad metodológica —particularmente en los métodos de segmentación y en los puntos de corte— y la falta de validación prospectiva limitan su traslación clínica generalizada . Un metaanálisis sobre parámetros PET/CT basales en LH y DLBCL encontró que, aunque el MTV mostró capacidad predictiva significativa en 17 de 19 estudios de DLBCL y 6 de 8 de LH, todos los estudios incluidos presentaron riesgo de sesgo global moderado o alto, y la mayoría eran retrospectivos, con potencia insuficiente y heterogéneos en su metodología .

---

## 4. Radiómica y modelos de predicción: más allá del volumen

La radiómica —extracción de características cuantitativas de la imagen más allá del volumen— representa el nivel de optimización que busca capturar la heterogeneidad tumoral. En el linfoma de Hodgkin, una revisión sistemática sobre radiómica basada en PET/CT encontró que, en 7 de 9 estudios, los modelos radiómicos o multimodales superaron a los modelos clínicos o volumétricos para predecir SLP y SG, con AUC entre 0,86 y 0,92. Dos estudios mostraron alta capacidad para identificar enfermedad refractaria primaria (AUC > 0,95). Un hallazgo relevante: la integración de múltiples lesiones incrementó la precisión predictiva en comparación con analizar una sola lesión diana .

En linfoma folicular, modelos radiómicos que combinaron TMTV con características de textura (medPCD, TVSR) alcanzaron mayor precisión predictiva que el TMTV solo . Un metaanálisis sobre valor diagnóstico de radiómica PET/CT en linfomas encontró que los modelos de deep learning (DL) superaron a los modelos de aprendizaje automático tradicional (TML), con cuatro estudios que utilizaron DL reportando precisión diagnóstica superior al 85% . Sin embargo, los mismos autores advierten que el DL requiere mayor cantidad de datos y la capacidad de generalización de los modelos en conjuntos de datos independientes sigue siendo deficiente .

Balance de esta línea

La radiómica existe como línea de investigación activa con resultados prometedores, pero no constituye una tecnología consolidada para uso clínico. La heterogeneidad metodológica, la falta de validación externa y la ausencia de armonización en la extracción de características son limitaciones reconocidas de manera consistente .

---

## 5. Tecnologías emergentes con impacto potencial

PET/CT de campo de visión axial largo (LAFOV). Un estudio pediátrico que comparó LAFOV con escáneres de campo de visión estándar (SAFOV), con la mitad de los pacientes diagnosticados de linfoma, encontró que LAFOV a 1 MBq/kg produjo calidad de imagen diagnóstica comparable a SAFOV, mientras que 2–3 MBq/kg proporcionaron rendimiento superior. Los autores concluyen que LAFOV permite reducir la dosis de radiación sin deteriorar la detección de lesiones . Esta tecnología existe comercialmente pero su adopción clínica rutinaria aún es limitada.

Trazadores alternativos y cinética extendida. La literatura sobre 18F-FDG con adquisición ultra-tardía (hasta 6 horas post-inyección) utilizando LAFOV sugiere que la cinética extendida podría ofrecer información adicional para diferenciar subtipos de linfoma, aunque se trata de estudios exploratorios de un solo centro con muestras pequeñas . El 18F-FLT ha mostrado capacidad para diferenciar tumor de inflamación en comparación con 18F-FDG, pero su uso se ve limitado en enfermedad ósea por alta captación fisiológica en médula ósea.

---

## 6. Conclusión: ¿existe la tecnología? ¿Es mejorable?

La tecnología existe. La PET/CT con 18F-FDG es el estándar clínico para estadificación y evaluación de respuesta en linfomas FDG-ávidos, y los parámetros cuantitativos derivados (TMTV, MTV, TLG) han demostrado valor pronóstico independiente en múltiples subtipos y en metaanálisis que acumulan miles de pacientes . La segmentación automatizada mediante deep learning ha alcanzado un grado de concordancia con expertos humanos cercano al 83–87% en conjuntos de datos de referencia . Los modelos radiómicos añaden valor predictivo más allá del volumen en estudios preliminares .

La tecnología es mejorable, y la literatura identifica con precisión dónde. Las brechas reconocidas son: (a) la precisión de la segmentación automatizada en lesiones de pequeño tamaño, que sigue siendo deficiente ; (b) la falta de estandarización en los métodos de segmentación y en los puntos de corte del TMTV, que impide comparar resultados entre estudios y adoptar umbrales universalmente válidos ; (c) la escasez de validación externa y prospectiva de los modelos de IA y radiómicos, con la mayoría de los estudios siendo retrospectivos y con riesgo de sesgo moderado o alto ; y (d) la variabilidad en los criterios de interpretación del PET interino, donde el uso exclusivo del umbral DS 5 mejora sustancialmente el rendimiento pronóstico en comparación con otros umbrales .

El tema propuesto no plantea el desarrollo de una mejora específica sobre una tecnología existente, sino la optimización de la detección y evaluación mediante PET/CT. A la luz de la evidencia, esa optimización se materializa hoy en la interfaz entre la segmentación automatizada, la validación de biomarcadores volumétricos y la armonización metodológica. Las tecnologías existen; las brechas identificadas definen el espacio donde la investigación adicional es necesaria.

---

## Referencias

1. Total metabolic tumor volume as a prognostic biomarker in high-burden follicular lymphoma: A systematic review and meta-analysis. ScienceDirect, 2025. 
2. Baseline total metabolic tumor volume (TMTV) application in Hodgkin lymphoma: a review article. Clinical and Translational Imaging, 2022;10(3):273-284. 
3. The Prognostic Role of Interim [18F]FDG PET/CT in Diffuse Large B-Cell Lymphoma: An Updated Systematic Review and Meta-analysis. Clinical Lymphoma, Myeloma and Leukemia, 2026;26(8):491-510. 
4. Baseline PET/CT imaging parameters for prediction of treatment outcome in Hodgkin and diffuse large B cell lymphoma: a systematic review. OUCI (registro de artículo). 
5. Validation of an AI Method for Automated Lymphoma Metabolic Tumor Volume Segmentation Using a Public Benchmark PET/CT Dataset. Journal of Nuclear Medicine, 2026. 
6. Diagnostic Value of 18F-FDG PET/CT Radiomics in Lymphoma: A Systematic Review and Meta-Analysis. SAGE, 2025. 
7. FDG-PET/CT in children with malignant diseases - comparison of a long axial field of view scanner with a standard scanner. Europe PMC, 2026. 
8. Prognostic Value of 18F-FDG PET/CT Parameters at Baseline and End of Treatment in Follicular Lymphoma: A Systematic Review and Meta-analysis. ScienceDirect, 2025. 
9. Prognostic value of radiomics derived from 18F-FDG PET/CT in Hodgkin lymphoma: a systematic review. Revista Española de Medicina Nuclear e Imagen Molecular, 2026 (en prensa).
10. Artificial intelligence-based PET/CT analysis in lymphoma: segmentation, differential diagnosis, and prognostic stratification. Holistic Integrative Oncology, 2026. 
11. Exploring extended [18F]FDG kinetics in lymphoma with ultra-late LAFOV-PET/CT. European Journal of Nuclear Medicine and Molecular Imaging, 2026. 