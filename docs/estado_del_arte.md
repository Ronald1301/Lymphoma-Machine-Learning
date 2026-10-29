# Estado del arte: detección y evaluación de lesiones de linfoma mediante FDG-PET/CT e inteligencia artificial

## Resumen ejecutivo

El FDG-PET/CT es el estándar funcional para estadificación y respuesta en los linfomas ávidos por FDG. Lugano y Deauville consolidaron la lectura visual, pero la cuantificación de carga tumoral —en especial el volumen metabólico tumoral total (TMTV)— aporta información pronóstica aún no incorporada uniformemente a la práctica. La segmentación manual o semiautomática varía entre métodos, software y lectores. Los umbrales absolutos, sobre todo SUV ≥ 4, ofrecen mayor reproducibilidad que los porcentajes del SUVmax, aunque no hay equivalencia entre protocolos. En aprendizaje profundo, 3D U-Net, nnU-Net y SegResNet dominan la evidencia; transformers y modelos fundacionales no han demostrado ventaja consistente en PET/CT de linfoma. autoPET mostró que los ensambles 3D y el preentrenamiento multimodal mejoran el rendimiento, pero autoPET III confirmó que la generalización a combinaciones inéditas de trazador y centro sigue abierta. La validación externa, las lesiones pequeñas, los falsos positivos fisiológicos y la calibración de incertidumbre importan más que diferencias marginales de Dice. Para un proyecto de siete días y cómputo limitado, la opción defendible es un baseline 3D compacto, evaluación por vóxel, lesión y paciente, y una mejora validada por ablación.

## 1. Introducción clínica

### 1.1 Linfomas y papel del FDG-PET/CT

El linfoma de Hodgkin clásico, el linfoma difuso de células B grandes (DLBCL) y el linfoma folicular representan escenarios biológicos y terapéuticos distintos, pero los tres suelen ser ávidos por FDG. El FDG-PET/CT integra metabolismo y anatomía: detecta enfermedad ganglionar y extranodal, orienta la biopsia, establece extensión basal, mide respuesta temprana y documenta respuesta al final del tratamiento [1–3]. En DLBCL y Hodgkin, esta sensibilidad funcional supera a la TC aislada para lesiones viables; en folicular, el PET/CT también identifica transformación sospechosa y carga tumoral, aunque la historia natural indolente modifica el significado pronóstico [1,2,5].

Lugano reemplazó la dependencia de la suma de diámetros por una evaluación adaptada a la avidez por FDG. En enfermedad ávida, la respuesta se interpreta con la escala Deauville de cinco puntos, comparando la captación tumoral con mediastino e hígado [1,2]. Una puntuación 1–3 suele equivaler a respuesta metabólica completa en el contexto terapéutico estándar; 4–5 exige interpretar intensidad, cambio respecto al basal y aparición de lesiones. El ensayo RATHL demostró que el PET interino puede guiar de-escalada en Hodgkin avanzado, pero esa evidencia no convierte cualquier clasificador automático de Deauville en una herramienta para cambiar tratamiento sin validación prospectiva [4].

### 1.2 Biomarcadores cuantitativos

Los índices más utilizados son:

- **SUVmax:** máximo voxelar dentro de una lesión. Es simple, pero representa un único vóxel y depende de reconstrucción, tiempo de captación y ruido [3].
- **SUVmean:** promedio dentro de una segmentación; resulta más estable, aunque depende directamente del contorno.
- **MTV/TMTV:** volumen metabólicamente activo por lesión y suma por paciente. TMTV aproxima carga tumoral global [5–8].
- **TLG:** producto de MTV y SUVmean, por lesión o total. Combina volumen e intensidad, pero hereda los errores de ambos.
- **Dmax:** distancia máxima entre dos lesiones; mide diseminación espacial y aporta información distinta de TMTV [9].
- **Heterogeneidad/radiómica:** texturas, formas y descriptores de distribución. Pueden capturar fenotipos no resumidos por SUV o volumen, pero son sensibles al tamaño, discretización, reconstrucción y segmentación.

La evidencia multicéntrica respalda el valor pronóstico de TMTV en folicular, Hodgkin y DLBCL [5,6,10–12]. El corte de 510 cm³ en folicular fue útil en un análisis agrupado, pero no debe tratarse como constante biológica: los puntos de corte cambian con población, método y software [5,7,11]. El International Metabolic Prognostic Index propuso tratar MTV como variable continua junto con edad y estadio, una solución metodológicamente más estable que dicotomizarlo [12]. Dmax puede mejorar la estratificación porque separa carga y dispersión [9]. La interpretación crítica es que TMTV es un biomarcador pronóstico robusto a nivel de asociación, pero su utilidad clínica depende de reproducibilidad, calibración y decisiones terapéuticas demostradas.

## 2. Datasets y benchmarks

### 2.1 Recursos públicos y acceso real

| Recurso | Tamaño verificado | Población / trazador | Anotación | Acceso/licencia | Limitación principal |
|---|---:|---|---|---|---|
| FDG-PET-CT-Lesions / autoPET | 1.014 estudios; 501 casos con melanoma, linfoma o NSCLC y 513 controles negativos | FDG, cuerpo entero | Lesiones manuales | TCIA; condiciones de la colección | Un centro y un escáner para la cohorte original; no identifica por sí solo un split público exclusivo de linfoma [13,42] |
| autoPET III | 1.014 FDG + 597 PSMA para desarrollo; test de 200 estudios | FDG y PSMA, dos centros de desarrollo y combinaciones centro-trazador inéditas | Lesiones manuales; test oculto | Grand Challenge / publicación del reto | No es específico de linfoma; el test final no se descarga [22] |
| Benchmark internacional TMTV | 60 estudios basales: 20 folicular, 20 Hodgkin, 20 DLBCL | FDG | 12 expertos; 3–4 lectores por caso; SUV4 | Dataset público usado para validación | Enriquecido en casos difíciles; pequeño para entrenar [15,18] |
| HECKTOR 2022 | 524 casos para tarea de segmentación y 356 de prueba, según la página oficial | Cáncer de cabeza y cuello, FDG | GTV primario y ganglionar | Grand Challenge; registro | No es linfoma; útil para transferencia y evaluación multicéntrica, no para conclusiones clínicas de linfoma [24,47,48] |
| CALGB 50303 PET substudy | 158 pacientes elegibles | DLBCL, FDG | Revisión central en ensayo clínico | Publicación abierta | No se verificó un repositorio público descargable de imágenes; no debe anunciarse como dataset abierto [14] |
| RECOMIA | Plataforma, no cohorte única | Varias modalidades y trazadores | Depende del proyecto | Acceso investigador autenticado | Es infraestructura de análisis, no dataset descargable [41] |

El descriptor de FDG-PET-CT-Lesions documenta 1.014 estudios de cuerpo entero y aclara una confusión recurrente: 900 pacientes no equivalen a 900 estudios; algunos pacientes tienen más de un examen [13]. La colección es adecuada para aprender captación tumoral general, pero mezcla indicaciones y su distribución no representa de forma pura Hodgkin, DLBCL o folicular. Un split debe realizarse por paciente, no por estudio, para impedir fuga longitudinal.

autoPET I/II establecieron una prueba oculta de segmentación oncológica; el análisis publicado de autoPET mostró predominio de 3D U-Net y beneficio de ensambles [21]. autoPET III elevó la dificultad al combinar FDG y PSMA y evaluar pares trazador-centro no vistos. Participaron 17 equipos con 27 algoritmos; el mejor método alcanzó Dice medio 0,66, FNV 3,18 mL y FPV 2,78 mL en las cuatro condiciones del test [22]. Estas cifras no deben compararse con Dice de tests preliminares o con cohortes de linfoma, porque cambian trazadores, instituciones y prevalencia.

El benchmark internacional de 60 casos es especialmente valioso para cuantificación: el TMTV final cubrió 8–2.288 cm³ y 52/60 casos mostraron acuerdo entre lectores dentro de ±10% o ±10 cm³ [15]. La captación esplénica difusa y la exclusión de captación fisiológica explicaron buena parte de los desacuerdos. Su validación con una red 3D mostró concordancia con el rango experto en 50/60 casos, pero ese resultado no sustituye una evaluación amplia de sensibilidad por lesión [18].

### 2.2 Taxonomía de métodos

```mermaid
flowchart TD
    A[PET/CT de cuerpo entero] --> B{Método}
    B --> C[Clásico / semiautomático]
    B --> D[Aprendizaje profundo]
    B --> E[Modelo fundacional / promptable]
    C --> C1[SUV fijo: 2.5 o 4.0]
    C --> C2[Porcentaje de SUVmax]
    C --> C3[Referencia hepática / PERCIST]
    D --> D1[3D U-Net / SegResNet]
    D --> D2[nnU-Net / ResEncL]
    D --> D3[DynUNet / SwinUNETR]
    D --> D4[Cascada y ensamble]
    E --> E1[MedSAM 2D]
    E --> E2[SAM-Med3D / MedSAM2]
    D1 --> F[Máscara de lesiones]
    D2 --> F
    D3 --> F
    D4 --> F
    C1 --> F
    C2 --> F
    C3 --> F
    E1 --> F
    E2 --> F
    F --> G[TMTV, TLG, lesiones, Dmax, estadio]
```

## 3. Métodos de segmentación y detección

### 3.1 Umbrales y métodos semiautomáticos

Los umbrales absolutos SUV 2,5 y SUV 4,0 son transparentes y rápidos. En cohortes antiguas de DLBCL, SUV 2,5 mostró buen rendimiento pronóstico y concordancia entre observadores [7,8]. Sin embargo, el consenso reciente favorece SUV ≥ 4,0 con volumen lesional mínimo de 3 cm³ para TMTV basal, porque reduce inclusión fisiológica y facilita reproducibilidad multicéntrica [15–17]. En 1.960 pacientes de ensayos LYSA, SUV4 y 41% SUVmax tuvieron asociación pronóstica comparable, aunque la correlación de los volúmenes fue mayor en DLBCL que en folicular o Hodgkin [17].

El umbral relativo de 41% SUVmax se adapta a la intensidad de cada lesión, pero puede infrasegmentar lesiones heterogéneas y cambia al variar la definición de SUVmax. También requiere más interacción y presenta mayor variación entre implementaciones [7,15,16]. La normalización respecto al hígado conecta con PERCIST y Deauville; automatizar hígado y pool mediastínico puede estandarizar referencias, pero una referencia estable no elimina la necesidad de revisar captación fisiológica [40].

Ningún umbral resuelve por sí solo cerebro, corazón, riñones, sistema urinario, músculo activado, inflamación o grasa parda. Los sistemas semiautomáticos eficaces combinan preselección sensible y corrección humana. Esto explica por qué la concordancia de TMTV puede ser alta aunque las máscaras voxel a voxel no coincidan exactamente.

### 3.2 Redes convolucionales 3D

3D U-Net sigue siendo el patrón práctico porque conserva contexto volumétrico y permite inferencia por parches. MONAI ofrece implementaciones reproducibles de UNet, SegResNet, DynUNet y SwinUNETR [27]. nnU-Net automatiza resampling, tamaño de parche, normalización y configuración de entrenamiento; su fortaleza no es una capa novedosa sino adaptar el pipeline al dataset [25]. Los presets ResEnc amplían la capacidad del encoder, y ResEncL se ha propuesto como nuevo baseline fuerte, pero su costo excede una GPU gratuita típica [26].

El estudio comparativo específico de linfoma entrenó UNet, SegResNet, DynUNet y SwinUNETR sobre 611 casos de varias cohortes. En el test externo de 145 casos, SegResNet obtuvo Dice mediana 0,68 y FPV mediana 21,46 mL, evidencia directa de las dificultades fuera de distribución [19,46]. En ese trabajo, SwinUNETR no superó de forma consistente a la CNN. Esta comparación contradice la suposición de que un transformer mejora automáticamente la segmentación 3D. UNETR y SwinUNETR siguen siendo arquitecturas relevantes, pero su evidencia fundacional procede sobre todo de MRI, no de PET/CT de linfoma [28,29].

TMTV-Net utilizó una cascada: ensamble multirresolución de 3D U-Net seguido de una red refinadora que recibe PET, CT y probabilidades. Se desarrolló con 900 estudios y se probó externamente en 518 estudios de linfoma de varios centros [20]. Su escala y evaluación clínica son fortalezas; su complejidad y licencia restringida a investigación dificultan reproducibilidad y despliegue.

### 3.3 Fusión PET/CT, cascadas y aumentación

La **fusión temprana** concatena PET y CT como canales. Es simple y domina autoPET, pero obliga a la red a tolerar resoluciones, ruido y posibles desalineaciones distintas [21,22]. La **fusión tardía** usa encoders independientes y combina características o decisiones; separa estadísticas de modalidad, pero incrementa parámetros y exige más datos. Una estrategia intermedia usa PET para sensibilidad metabólica, CT para anatomía y una rama o prior anatómico para suprimir órganos fisiológicos.

Las cascadas clasifican cortes o regiones, detectan candidatos y después segmentan. Reducen el espacio de búsqueda y falsos positivos, pero un fallo en la primera etapa es irrecuperable. Para cuerpo entero, una alternativa más segura es un primer modelo sensible y un segundo refinador que preserve candidatos con incertidumbre.

El ganador model-centric de autoPET III combinó nnU-Net ResEncL, aumentación explícita de desalineación PET/CT, preentrenamiento multimodal en CT/MR/PET y supervisión auxiliar de órganos [23]. Reportó Dice 68,40 en su evaluación, frente a 57,61 del nnU-Net por defecto y 65,31 de ResEncL sin las mejoras. Estas cifras pertenecen al estudio de la solución y no son equivalentes al 0,66 agregado del test oficial [22,23]. El mecanismo es clínicamente plausible: desplazar una modalidad durante entrenamiento reduce dependencia de registro perfecto, mientras el aprendizaje anatómico ayuda a distinguir tumor de captación fisiológica.

### 3.4 Modelos fundacionales y priors anatómicos

TotalSegmentator segmenta 104 estructuras en CT y puede generar máscaras de cerebro, corazón, riñones, vejiga y otros órganos para postprocesado o como canales auxiliares [30]. Su evidencia es CT, no captación tumoral en PET. Por tanto, debe describirse como prior anatómico, no como segmentador de linfoma.

MedSAM fue entrenado con más de 1,5 millones de pares imagen-máscara y múltiples modalidades [31]. SAM-Med3D y MedSAM2 extienden la idea al volumen y seguimiento [32,33]. Estos modelos son útiles para anotación asistida y adaptación con pocos casos, pero la evidencia disponible no demuestra que superen a nnU-Net o SegResNet en segmentación automática de lesiones FDG de cuerpo entero. Los prompts, memoria y coste de inferencia también complican un pipeline completamente automático. La oportunidad realista es usarlos para acelerar corrección humana o preanotación, no sustituir de inmediato el baseline especializado.

### 3.5 Pipeline típico de desarrollo y evaluación

```mermaid
flowchart LR
    A[DICOM / NIfTI PET+CT] --> B[Conversión SUV y control geométrico]
    B --> C[Resampling y normalización]
    C --> D[Split por paciente]
    D --> E[Entrenamiento 3D por parches]
    E --> F[Sliding-window inference]
    F --> G[Mapa de probabilidad]
    G --> H[Postprocesado auditable]
    H --> I[Máscara y lesiones conectadas]
    I --> J[Dice, FPV, FNV]
    I --> K[Sensibilidad por lesión y FP/paciente]
    I --> L[TMTV, Bland-Altman e ICC]
    J --> M[Análisis de errores]
    K --> M
    L --> M
    M --> N[Calibración, exportación ONNX y reporte]
```

La separación entre postprocesado y métricas permite auditar qué candidatos fueron eliminados. El split debe preceder cualquier ajuste estadístico o selección de hiperparámetros para evitar fuga.

## 4. Evaluación y métricas

### 4.1 Tres niveles de evaluación

Una evaluación clínica no puede reducirse a Dice.

1. **Vóxel/volumen:** Dice, FPV y FNV. Dice mide solapamiento relativo; FPV y FNV expresan mililitros añadidos u omitidos y son más interpretables cuando la carga varía varios órdenes de magnitud.
2. **Lesión:** sensibilidad por lesión, falsos positivos por paciente y distribución por tamaño. Una lesión puede considerarse detectada por intersección no vacía, IoU mínimo o fracción de solapamiento; el criterio debe declararse. El estudio de 611 casos mostró que conclusiones clínicas cambian según el criterio de matching [19].
3. **Paciente/biomarcador:** error absoluto y relativo de TMTV, sesgo y límites de acuerdo de Bland–Altman, ICC con intervalo de confianza y concordancia de estratos de riesgo.

Para dos máscaras binarias, Dice = 2TP/(2TP+FP+FN). No debe promediarse sin informar casos negativos: un paciente sin lesión plantea la convención 1 si predicción y referencia están vacías, pero ese valor puede inflar el promedio. Conviene reportar negativos por separado con tasa de falsos positivos.

FPV y FNV deben calcularse con el volumen voxelar físico, no con conteo bruto de vóxeles. La sensibilidad por lesión requiere matching uno-a-uno o reglas explícitas para lesiones fusionadas y fragmentadas. Se recomienda presentar resultados por tamaño (<1 mL, 1–10 mL, >10 mL, por ejemplo), localización y subtipo.

### 4.2 Fiabilidad frente a lectores

El benchmark de 60 casos define una referencia de consenso y un margen clínico de ±10% o ±10 cm³ para TMTV [15]. Bland–Altman revela sesgo dependiente de carga que un ICC alto puede ocultar. El ICC mide ordenamiento y acuerdo global, pero puede parecer excelente cuando el rango de TMTV es enorme. Deben presentarse ambos.

Comparar un modelo con una sola máscara no estima incertidumbre del ground truth. Cuando existan varias lecturas, el modelo debe contrastarse con cada lector y con consenso. La pregunta correcta es si el error del sistema cae dentro de la variación interlector, no si reproduce exactamente una máscara arbitraria [15,18].

## 5. Generalización, robustez y fiabilidad

### 5.1 Cambio de dominio

Las fuentes principales de shift son escáner y reconstrucción, dosis, tiempo postinyección, resolución, centro, población, trazador y prevalencia. El Dice mediano 0,68 y la FPV mediana 21,46 mL del test externo de 145 casos en el estudio de linfoma muestran que la evaluación fuera de distribución sigue siendo exigente [19]. autoPET III muestra un problema más fuerte: la combinación nueva de centro y trazador produce sobreestimación sistemática incluso cuando cada componente se vio por separado [22].

La validación externa debe estar separada por institución y paciente. Una partición aleatoria de estudios del mismo centro mide interpolación, no generalización clínica. La normalización de SUV y CT, resampling homogéneo y aumentación de desalineación son mitigaciones razonables, pero no sustituyen un test externo.

### 5.2 Falsos positivos y lesiones pequeñas

Cerebro, miocardio, hígado, bazo, riñón, uréteres y vejiga concentran actividad fisiológica; inflamación, granulomas y brown fat añaden captación benigna. Los priors anatómicos permiten enmascarar o penalizar parte de esos órganos, pero una exclusión rígida puede borrar enfermedad extranodal real. Debe preferirse un prior suave o una regla revisable.

Las lesiones pequeñas sufren efecto de volumen parcial y tienen pocos vóxeles, de modo que una traslación mínima reduce Dice de forma desproporcionada. Por eso se requieren sensibilidad por lesión y curvas según tamaño. Un modelo puede acertar TMTV total dominado por masas grandes y omitir lesiones pequeñas clínicamente relevantes.

### 5.3 Incertidumbre, calibración y explicabilidad

La literatura revisada informa poco sobre calibración. Ensembles y test-time augmentation generan dispersión, pero esa dispersión no es automáticamente una probabilidad calibrada. Deben evaluarse Expected Calibration Error o Brier score a nivel de candidato, curvas precisión–recobrado y cobertura–riesgo para abstención. Una salida útil marca casos que requieren revisión, especialmente captación esplénica difusa, región urinaria o discrepancia PET/CT.

La explicabilidad en segmentación debe ser espacial y causal: mapa de probabilidad, candidatos eliminados por postprocesado y contribución de PET frente a CT. Los mapas de atención no prueban razonamiento clínico. La auditoría por subgrupos debe incluir subtipo, centro, sexo, edad, carga tumoral y tamaño de lesión cuando los metadatos estén disponibles.

## 6. Eficiencia y despliegue

El baseline oficial de autoPET documenta nnU-Net 3D full-resolution con 16 GB de VRAM, 1.000 épocas y validación cruzada de cinco folds; el baseline MONAI usa parches 128×128×32, batch 12 y 800 épocas [47]. Esos presupuestos exceden lo razonable para una semana en Colab/Kaggle si se repiten completos. Un proyecto académico debe reducir parches, canales, folds y épocas con early stopping, y reservar un único test.

ONNX permite separar entrenamiento PyTorch e inferencia [45]. ONNX Runtime ofrece cuantización dinámica y estática INT8 con formatos QDQ/QOperator, pero la cuantización no es sin pérdida y debe revalidarse, especialmente en lesiones pequeñas [43]. Ryzen AI recomienda opset 17, modelos INT8 o BF16 y partición automática entre NPU y CPU en Windows [44]. No se encontró evidencia primaria de un 3D U-Net PET/CT completo ejecutándose de extremo a extremo en esa NPU. Operadores 3D no soportados pueden caer a CPU, por lo que exportar correctamente no demuestra aceleración.

Una ruta prudente es: exportar con forma de parche fija, comparar PyTorch CPU con ONNX Runtime CPU, cuantizar solo después de verificar Dice/TMTV y probar el Vitis AI Execution Provider como experimento opcional. Deben medirse latencia por volumen, memoria pico y fracción de operadores asignados a NPU.

## 7. Tabla comparativa resumida

> Las métricas de filas distintas no son comparables directamente: cambian cohortes, trazadores, splits, prevalencia y definición de lesión.

| Estudio | Tarea / entrada | Arquitectura | Validación | Resultado contextualizado | Limitación |
|---|---|---|---|---|---|
| Ahamed et al. [19] | Lesiones de linfoma, PET+CT | UNet, SegResNet, DynUNet, SwinUNETR | 611 casos; test externo 145 | SegResNet: Dice mediana 0,68 y FPV 21,46 mL en test externo | Cohortes retrospectivas; rendimiento fuera de distribución |
| TMTV-Net [20] | TMTV de linfoma, PET+CT | Cascada y ensamble 3D U-Net | 518 externos multicéntricos | Evalúa Dice, TMTV y revisión médica | Pipeline pesado; licencia de investigación |
| autoPET [21] | Lesiones oncológicas FDG, PET+CT | Predominio 3D U-Net; ensamble | Test privado 150, dos centros | Ensamble superior a modelos individuales | Mezcla tumores; test oculto |
| autoPET III [22] | FDG+PSMA, PET+CT | 27 algoritmos, mayoría nnU-Net | 200 casos, 4 condiciones | Top: Dice 0,66, FNV 3,18 mL, FPV 2,78 mL | Generalización composicional no resuelta |
| LesionTracer/DKFZ [23] | autoPET III | nnU-Net ResEncL + pretraining + órganos + misalignment | Challenge | Dice 68,40 en evaluación del paper | No comparar directamente con ranking final |
| Benchmark IA TMTV [18] | Linfoma, PET+CT | 3D U-Net | Benchmark 60, múltiples lectores | Dentro de ±10% o ±10 cm³ en 50/60 | Dataset pequeño y difícil |
| AutoLugano [34] | Segmentación + regiones + estadio | 3D nnU-Net + TotalSegmentator + reglas | Externa 67 | Accuracy 85,07% limitado/avanzado | Preprint; externa pequeña |
| Hasanabadi et al. [35] | Estadio, PET radiomics | ML con rasgos nodales/extranodales | Multicéntrica, n=241 | AUC externa 0,87 | Retrospectivo |
| Li et al. [36] | Estadio, MIP PET/CT | DL multivista 2D | 5-fold, n=227 | AUC 0,942 | Sin test institucional independiente |
| Jiang et al. [37] | Pronóstico DLBCL, PET | VGG19 + DenseNet121 | 3 centros, n=684 | C-index PFS externo 0,760 | Asociación retrospectiva, no impacto clínico |

## 8. Brechas y oportunidades

1. **Generalización específica de linfoma.** autoPET es grande, pero no sustituye una cohorte externa con subtipo, centro y protocolo distintos [13,19,22].
2. **Detección y cuantificación conjunta.** Optimizar Dice global puede ocultar falsos negativos pequeños y error de TMTV. La evaluación debe ser multiescala y clínica [15,18,19].
3. **Captación fisiológica.** Supervisión anatómica y priors CT son prometedores, pero deben permitir enfermedad extranodal y cuantificar errores por órgano [23,30].
4. **Desalineación PET/CT.** Es frecuente y pocas publicaciones la modelan explícitamente. La aumentación de desplazamiento es barata y verificable mediante ablación [23].
5. **Subtipos infrarrepresentados.** DLBCL domina la literatura de radiómica y pronóstico; Hodgkin y folicular tienen menos validación externa automatizada [38,39,49].
6. **Incertidumbre y abstención.** Falta calibración prospectiva y definición de cuándo el sistema debe remitir un caso a revisión.
7. **Despliegue medido, no supuesto.** ONNX y NPU son compatibles a nivel de herramientas, pero faltan benchmarks PET/CT 3D en Ryzen AI [42–44].
8. **De segmentación a decisión.** AutoLugano demuestra viabilidad técnica, pero todavía se necesita validación prospectiva de estadio, respuesta y cambio de manejo [34–36].

Estas brechas justifican un proyecto enfocado en segmentación basal de linfoma con evaluación por lesión y TMTV, no en predicción de respuesta clínica sin etiquetas longitudinales.

## 9. Conclusiones

La evidencia establecida por múltiples estudios es que FDG-PET/CT estructura el estadiaje y la respuesta en linfoma, y que TMTV añade valor pronóstico [1–6,10–12]. También está establecido que la segmentación y el software alteran los valores absolutos; SUV4 ofrece una ruta de estandarización, no una verdad única [7,15–17].

Un solo estudio multicéntrico o challenge no demuestra generalización universal. El rendimiento del estudio de 611 casos en su conjunto externo y el reto composicional de autoPET III indican que el principal problema es robustez, no escoger entre variantes cercanas de arquitectura [19,22]. Para una entrega académica en siete días, la contribución defendible es un pipeline reproducible con split por paciente, baseline 3D compacto, una o dos mejoras motivadas, y evaluación de Dice, FPV/FNV, sensibilidad por lesión, FP/paciente y acuerdo de TMTV. Predicción de Deauville o respuesta debe quedar como extensión condicionada a datos adecuados.

## Referencias

La información bibliográfica completa y los identificadores verificables están en `referencias.bib`.

[1] Cheson et al., Lugano Classification, *J Clin Oncol*, 2014.  
[2] Barrington et al., ICML Imaging Working Group, *J Clin Oncol*, 2014.  
[3] Boellaard et al., EANM FDG PET/CT guidelines v2.0, *Eur J Nucl Med Mol Imaging*, 2015.  
[4] Johnson et al., RATHL, *N Engl J Med*, 2016.  
[5] Meignan et al., TMTV in follicular lymphoma, *J Clin Oncol*, 2016.  
[6] Mikhaeel et al., baseline MTV and early response in DLBCL, *Eur J Nucl Med Mol Imaging*, 2016.  
[7] Ilyas et al., optimal baseline MTV method in DLBCL, *Eur J Nucl Med Mol Imaging*, 2018.  
[8] Guzmán Ortiz et al., MTV calculation methods in DLBCL, 2020.  
[9] Cottereau et al., PET dissemination features in DLBCL, *J Nucl Med*, 2020.  
[10] Durmo et al., baseline TMTV in advanced Hodgkin lymphoma, *Sci Rep*, 2021.  
[11] Meignan et al., TMTV review, *Br J Radiol*, 2021.  
[12] Mikhaeel et al., International Metabolic Prognostic Index, *J Clin Oncol*, 2022.  
[13] Gatidis et al., FDG-PET-CT-Lesions data descriptor, *Sci Data*, 2022.  
[14] Schöder et al., CALGB 50303 PET substudy, *Blood*, 2020.  
[15] Boellaard et al., international TMTV benchmark, *J Nucl Med*, 2024.  
[16] Barrington et al., clinical implementation of MTV, *J Nucl Med*, 2024.  
[17] Malmon et al., SUV4 in 1,960 lymphoma patients, *Eur J Nucl Med Mol Imaging*, 2025.  
[18] Sadik et al., AI validation on public TMTV benchmark, *J Nucl Med*, 2026.  
[19] Ahamed et al., comparative lymphoma segmentation framework, *Phys Med*, 2026 / arXiv:2311.09614.  
[20] Yousefirizi et al., TMTV-Net, *Eur J Nucl Med Mol Imaging*, 2024.  
[21] Gatidis et al., autoPET challenge results, *Nat Mach Intell*, 2024.  
[22] Dexl et al., autoPET III multitracer multicenter generalization, arXiv:2605.05775, 2026.  
[23] Rokuss et al., Hitchhiker's Guide / LesionTracer, arXiv:2409.09478, 2024.  
[24] Andrearczyk et al., HECKTOR 2022 overview, LNCS 13626, 2023.  
[25] Isensee et al., nnU-Net, *Nat Methods*, 2021.  
[26] Isensee et al., nnU-Net Revisited, arXiv:2404.09556, 2024.  
[27] Cardoso et al., MONAI, arXiv:2211.02701, 2022.  
[28] Hatamizadeh et al., UNETR, WACV, 2022.  
[29] Hatamizadeh et al., Swin UNETR, arXiv:2201.01266, 2022.  
[30] Wasserthal et al., TotalSegmentator, *Radiol AI*, 2023.  
[31] Ma et al., MedSAM, *Nat Commun*, 2024.  
[32] Wang et al., SAM-Med3D, arXiv:2310.15161, 2023.  
[33] Zhuo et al., MedSAM2, arXiv:2504.03600, 2025.  
[34] Pan et al., AutoLugano, arXiv:2512.07206, 2025.  
[35] Hasanabadi et al., automatic Lugano staging, *Nucl Med Commun*, 2025.  
[36] Li et al., multi-view automated lymphoma staging, *EJNMMI Res*, 2026.  
[37] Jiang et al., multicenter DLBCL prognostic imaging biomarker, *Eur J Nucl Med Mol Imaging*, 2023.  
[38] Driessen et al., PET radiomics in relapsed/refractory Hodgkin lymphoma, *Blood Adv*, 2023.  
[39] Mehrabi Nejad et al., AI PET outcome meta-analysis, *Eur J Radiol*, 2025.  
[40] Grossiord et al., automated Deauville references, 2018.  
[41] Trägårdh et al., RECOMIA, *EJNMMI Phys*, 2020.  
[42] The Cancer Imaging Archive, FDG-PET-CT-Lesions collection.  
[43] ONNX Runtime, quantization documentation.  
[44] AMD, Ryzen AI model compilation and deployment.  
[45] PyTorch, `torch.onnx` documentation.  
[46] Microsoft AI for Good Lab, `lymphoma-segmentation-dnn`.  
[47] autoPET challenge organizers, baseline repository.  
[48] HECKTOR organizers, HECKTOR 2022 data page.  
[49] Kanavos et al., systematic review of deep learning for lymphoma PET, *Cancers*, 2025.

## Informe de verificación y descartes

**Verificado:** se abrieron fuentes primarias o páginas oficiales para Lugano/Deauville, autoPET, autoPET III, el benchmark TMTV de 60 casos, TMTV-Net, el estudio de 611 casos, AutoLugano, estadiaje multivista, ONNX Runtime y Ryzen AI. Se comprobó que el benchmark contiene 20 casos de cada subtipo y que cada caso fue segmentado por 3–4 de 12 expertos; que autoPET III recibió 27 algoritmos de 17 equipos; y que CALGB 50303 describe una cohorte de ensayo, no un repositorio público de imágenes.

**No verificado o no reportado:** no se encontró un dataset público con pares longitudinales pre/post y etiquetas clínicas de respuesta Deauville/Lugano listo para entrenar un predictor. Tampoco se encontró un benchmark publicado de 3D U-Net PET/CT en la NPU Ryzen AI. Hardware y tiempo no reportados se dejan como “no reportado” en la tabla CSV.

**Descartado:** blogs, noticias, copias de ResearchGate cuando existía fuente primaria, métricas de tests preliminares presentadas como resultados finales, y referencias cuyo título/identificador no pudo confirmarse. TotalSegmentator, MedSAM y HECKTOR se conservan solo como evidencia de prior, transferencia o benchmark vecino; no se presentan como validación directa de linfoma.
