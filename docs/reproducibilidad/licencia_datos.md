# Licencia y condiciones de uso de los datos (T07)

Fuente principal: colección **FDG-PET-CT-Lesions** (reto autoPET), vía **TCIA / IDC**.

## Por qué no FDAT

El zip NIfTI de FDAT (`fdat.uni-tuebingen.de`, DOI `10.57754/FDAT.8f14a-pf846`) es la
misma colección ya convertida, pero el dominio lleva días inaccesible desde la red del
equipo (timeout de TCP, 2026-11-21). **T07 usa TCIA/IDC**, que responde y publica la
versión *Images - Defaced* en abierto. Si FDAT vuelve, se puede reevaluar como fuente
NIfTI alternativa; no bloquea el proyecto.

## Colección

| Campo | Valor |
|---|---|
| Nombre | FDG-PET-CT-Lesions |
| DOI (imágenes TCIA) | [10.7937/gkr0-xv29](https://doi.org/10.7937/gkr0-xv29) |
| Artículo de referencia | Gatidis & Küstner et al., *Sci Data* 9, 601 (2022). [10.1038/s41597-022-01718-3](https://doi.org/10.1038/s41597-022-01718-3) |
| Página TCIA | <https://www.cancerimagingarchive.net/collection/fdg-pet-ct-lesions/> |
| Espejo IDC (descarga T07) | <https://portal.imaging.datacommons.cancer.gov/collections/fdg_pet_ct_lesions> |
| Licencia de imágenes (Defaced) | **CC BY 4.0** |
| Licencia clínica (CSV) | CC BY 4.0 |
| Tamaño colección completa (DICOM) | ~419 GB (1.014 estudios, 900 pacientes) |

IDC aloja la versión *defaced* de TCIA bajo CC BY 4.0; las imágenes originales sin
defacing siguen bajo control de acceso de NIH. **Descargamos solo Defaced/IDC.**

## Citación obligatoria

Si usamos estos datos en el informe o en cualquier entrega, citamos:

> Gatidis S, Küstner T. *A whole-body FDG-PET/CT dataset with manually annotated tumor lesions (FDG-PET-CT-Lesions)* [Dataset]. The Cancer Imaging Archive, 2022. DOI: 10.7937/gkr0-xv29.

## Condiciones relevantes para el proyecto

- **Atribución (BY):** citar DOI y autores en informe, póster y código que publique resultados derivados.
- **Compartir derivados:** CC BY 4.0 permite compartir y adaptar con atribución; mantener la misma licencia en imágenes derivadas que se redistribuyan fuera del equipo.
- **Datos en el repo:** los DICOM y NIfTI **no** se suben a git (`.gitignore` incluye `*.nii.gz`, `*.nii` y `/data/`).
- **Compartir con el equipo:** la muestra se publica como **dataset privado de Hugging Face** (criterio de aceptación de T07: Kaggle, Drive u otro medio privado) para no repetir la descarga. El repo privado se comparte añadiendo al equipo en *Settings → Members*.
- **Dataset T07:** <https://huggingface.co/datasets/lymphoma-ml-uh/fdg-pet-ct-lesions> (privado, bajo la organización del equipo; contiene `raw/` con los 5 NIfTI por estudio, `manifest.csv` y `sample_ids.csv`). Si se cambia el `HF_REPO_ID`, actualizar este enlace.
- **Metadatos clínicos:** `Clinical-Metadata-FDG-PET_CT-Lesions.csv` (CC BY 4.0) procede de TCIA; se usa para diagnóstico y fechas.

## Qué descarga T07

- **Fuente:** IDC (`idc-index`), colección `fdg_pet_ct_lesions`, modalidades `PT`, `CT` y `SEG`.
- **Alcance:** muestra estratificada de 60 pacientes (semilla 42, `data/sample_ids.csv`): 48 linfoma y 12 negativos. Melanoma y cáncer de pulmón no se descargan porque el plan experimental entrena solo con linfoma y los negativos se reservan para medir falsos positivos.
- **Formato:** DICOM → conversión a NIfTI con el script oficial `lab-midas/TCIA_processing` (`tcia_dicom_to_nifti.py`) para obtener `SUV.nii.gz`, `CTres.nii.gz` y `SEG.nii.gz` (estructura del contrato).
- **Salidas versionadas:** `data/sample_ids.csv`, `data/manifest.csv`, scripts y notebook. Nunca imágenes.

## Contacto / dudas

Condiciones vigentes en las páginas oficiales enlazadas arriba. Ante cualquier uso
fuera del alcance académico del curso, consultar con el equipo y con las condiciones
de TCIA/IDC.
