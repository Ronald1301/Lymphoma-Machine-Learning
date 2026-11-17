# Estado de accesos y preparación de datos (T05)

**Estado:** parcial; no cerrar T05 hasta completar las verificaciones del equipo.
**Última actualización:** 2026-11-16.
**Fuente:** Ronald reportó acceso a Kaggle para los cuatro integrantes. Abel aportó en el comentario de T05 sus pruebas de GPU y velocidad; son datos reportados, no comprobados independientemente en este repositorio.

## Cuentas de cómputo

| Integrante | Cuenta Kaggle | GPU habilitada verificada | Cuota disponible anotada | Colab |
|---|---|---|---|---|
| Ronald | Disponible (reportado por Ronald) | GPU no seleccionable; `torch.cuda.is_available()` dio `False` (reportado por Ronald, 2026-11-16) | Pendiente | No sabe; no hace falta si Kaggle funciona |
| Agustin | Reportada como disponible | Pendiente | Pendiente | Sin verificar |
| Dylan | Reportada como disponible | Pendiente | Pendiente | Sin verificar |
| Abel | Reportada como disponible | Kaggle T4 x2 reportada; activación no verificada aquí | 30 h/semana reportadas | Colab T4 reportada; cuota variable |

Abel reportó estas mediciones desde entornos cloud: Kaggle 1166.67 Mbit/s de descarga y 145.58 Mbit/s de subida; Colab 63.15 Mbit/s de descarga y 0.25 Mbit/s de subida. Reportó Kaggle con T4 x2 y 30 horas semanales, y Colab con T4 y cuota variable. Son valores del comentario, no una transferencia medida desde TCIA; la velocidad y cuota deben tratarse como provisionales. La cuota gratuita puede variar por cuenta y fecha. Cada integrante debe abrir un notebook de Kaggle, seleccionar una GPU en *Settings/Accelerator* y comprobar que el runtime la detecta. Registrar luego la cuota o límite que muestre Kaggle. Colab es otra plataforma de notebooks en la nube; no hace falta asumir que el equipo ya tiene acceso con GPU.

No registrar contraseñas, tokens ni claves API aquí.

## Verificación de Ronald

El acceso a la cuenta Kaggle está reportado. La verificación de GPU y cuota queda pendiente hasta que la opción GPU pueda seleccionarse y PyTorch detecte el dispositivo. No pude observar la sesión personal desde aquí porque el navegador no está disponible en esta sesión; los pasos para resolverlo constan en el resultado de prueba siguiente.
## Resultado de la prueba de Ronald

El 2026-11-16, Ronald reportó que Kaggle no le permite seleccionar GPU y que la celda devolvió `CUDA disponible: False`. Esto confirma que la sesión actual está corriendo sin GPU; no confirma por sí solo la causa ni la cuota disponible. El estado de verificación telefónica de la cuenta aún no está confirmado.

### Pasos de diagnóstico

1. Abre https://www.kaggle.com/settings y revisa el estado de verificación de teléfono de tu cuenta. Kaggle indica que la verificación telefónica es requisito para acceso a GPU; no compartas el número ni códigos SMS aquí.
2. Si no está verificada, completa tú mismo el proceso de Kaggle. Luego vuelve al notebook y recarga o inicia una sesión nueva.
3. En el notebook, abre **Settings → Accelerator → GPU**. Si la opción aparece activa, selecciónala y espera a que la sesión reinicie. Kaggle advierte que la disponibilidad puede estar limitada o en cola.
4. Vuelve a ejecutar esta celda. Solo registra GPU disponible si `CUDA disponible` da `True` y aparece el nombre del dispositivo:

```python
import torch

print("CUDA disponible:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("Cantidad de GPU:", torch.cuda.device_count())
```
5. Consulta la cuota desde la configuración/uso del notebook, la página de notebooks o tu perfil. Anota exactamente el valor que muestre Kaggle.
6. Si tu teléfono ya está verificado y GPU sigue deshabilitada, revisa la cuota restante y vuelve a probar más tarde. Si continúa, contacta al soporte de Kaggle; no intentes evadir la verificación.

Kaggle documenta la selección de GPU en **Settings → Accelerator** y que la sesión se reinicia al cambiarla. Su guía también señala límites y monitorización de la cuota. Fuentes: https://www.kaggle.com/docs/notebooks, https://www.kaggle.com/docs/efficient-gpu-usage y la nota de Kaggle Staff sobre verificación de teléfono: https://www.kaggle.com/discussions/product-feedback/751699.
## Coordinación propuesta para T05 (pendiente de validar con el equipo)

- Kaggle será la plataforma principal; Colab queda como alternativa, sin exigir que todos lo configuren.
- No se descargará la colección completa de AutoPET (418.95 GB).
- Dylan, responsable de T07, coordinará una muestra manejable de 40–80 pacientes de la versión desidentificada o presentará una fuente alternativa. Antes de llamarla muestra de linfoma, se verificará el diagnóstico con los metadatos; la colección mezcla varios cánceres y controles.
- El equipo decidirá dónde quedarán los datos para que no haya descargas duplicadas. Una prueba de velocidad dentro de Kaggle/Colab no sustituye medir la descarga real de TCIA.

## Colección de imágenes

**AutoPET** es el nombre del reto/proyecto; **FDG-PET-CT-Lesions** es el nombre de su colección de imágenes en TCIA. TCIA significa *The Cancer Imaging Archive*, un archivo que publica colecciones de imágenes médicas. La colección contiene estudios FDG-PET/CT con segmentaciones; combina linfoma, melanoma y cáncer de pulmón, además de controles negativos. No es exclusivamente una cohorte de linfoma, por lo que la fase 1 debe filtrar y documentar diagnósticos y exclusiones.

- Página oficial de la colección: https://www.cancerimagingarchive.net/collection/fdg-pet-ct-lesions/
- Página del dataset AutoPET: https://autopet.grand-challenge.org/Dataset/
- Instrucciones oficiales de descarga de TCIA: https://www.cancerimagingarchive.net/downloading-tcia-images/
- TCIA indica actualmente **418.95 GB** para la versión *Images - Defaced* (desidentificada, CC BY 4.0) y **418.85 GB** para las imágenes originales, sujetas a la política de acceso controlado de NIH. Preferir la versión desidentificada para este trabajo, verificando las condiciones vigentes en la página antes de descargar.
- TCIA utiliza TCIA Data Retriever y un manifiesto para descargar la colección. El equipo indicó que no descargará la colección completa por su tamaño. No se inicia ninguna descarga desde este registro. Si se conserva AutoPET, hay que elegir y aprobar una muestra manejable (T07 contempla 40–80 pacientes) o definir dónde se alojarán los datos para acceso remoto.

## Tamaño y tiempo de descarga

Tamaño publicado para *Images - Defaced*: aproximadamente 418.95 GB. El tiempo real no se puede estimar sin medir la velocidad disponible en la conexión que hará la descarga. Como referencia teórica, suponiendo una velocidad sostenida y GB decimales, sin contar pausas ni sobrecarga:

| Velocidad sostenida | Tiempo aproximado para 418.95 GB |
|---:|---:|
| Kaggle (medición reportada: 1166.67 Mbps) | ~48 min |
| Colab (medición reportada: 63.15 Mbps) | ~14.7 h |
| 10 Mbps | 93 h |
| 50 Mbps | 18.6 h |
| 100 Mbps | 9.3 h |

Las filas de Kaggle y Colab son extrapolaciones teóricas de la prueba de red reportada por Abel; no miden el trayecto ni los límites de TCIA. El tiempo real de descarga del conjunto sigue sin conocerse. Como el equipo descarta descargar la colección completa, debe acordar si T07 usará una muestra estratificada de 40–80 pacientes o una fuente alternativa.

## Pendiente para completar T05

- [ ] Cada integrante verifica que su GPU de Kaggle se activa en una sesión y anota la cuota disponible.
- [ ] Probar en equipo la página oficial y obtener el manifiesto de la versión desidentificada de TCIA. La colección existe y el enlace oficial está confirmado, pero no consta una prueba de descarga por un integrante.
- [ ] Si se elige una muestra, medir el tiempo de descarga de esa muestra desde la conexión que efectivamente la descargará.
- [ ] Acordar si se usa AutoPET con muestra o se cambia de fuente; quién prepara los datos, dónde se almacenarán y cómo se compartirán sin duplicar descargas.
