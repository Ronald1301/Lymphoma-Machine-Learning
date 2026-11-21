# Instalar el entorno

Guía paso a paso (T02, #4). Elige tu plataforma y sigue los pasos en orden:

- **Laptop o PC (Windows, macOS o Linux):** comandos en la terminal. No se usa el notebook.
- **Nube (Kaggle o Colab):** el notebook `notebooks/setup_kaggle_colab.ipynb`. No se escribe ningún comando.

En todas, la comprobación final debe terminar con:

```
OK: el entorno coincide con las versiones fijadas.
```

- [Windows 11](#windows-11)
- [macOS](#macos)
- [Linux](#linux)
- [Kaggle](#kaggle)
- [Colab](#colab)
- [Uso diario](#uso-diario)
- [Añadir una dependencia](#añadir-una-dependencia)
- [Sin uv (con pip)](#sin-uv-con-pip)
- [Si algo falla](#si-algo-falla)

## Windows 11

Necesitas Git. Todos los comandos se escriben en **PowerShell**.

**1. Instala uv** (el programa que instala el entorno):

```powershell
winget install --id=astral-sh.uv -e
```

Si `winget` no existe, usa este comando en su lugar:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Cierra PowerShell, ábrela de nuevo** y comprueba que uv responde:

```powershell
uv --version
```

Debe mostrar `uv 0.13.8` o una versión mayor.

**3. Descarga el repositorio.** Si ya lo tienes, entra en su carpeta y ejecuta `git pull`.

```powershell
git clone https://github.com/Ronald1301/Lymphoma-Machine-Learning.git
cd Lymphoma-Machine-Learning
```

**4. Instala el entorno:**

```powershell
uv sync
```

La primera vez tarda unos minutos. Descarga Python 3.12 y todas las librerías en la carpeta `.venv`. No hace falta tener Python instalado.

**5. Comprueba que funciona:**

```powershell
uv run python -c "import monai, torch; print(monai.__version__, torch.__version__)"
uv run pytest -q
uv run python scripts/check_env.py --save
```

Debes ver:

- tras el primer comando: `1.6.1 2.11.0`;
- tras el segundo: una línea `N passed`, sin ningún `failed`;
- tras el tercero: `OK: el entorno coincide con las versiones fijadas.` y una línea `Guardado en …env_windows.json`. El script pone solo el nombre de la plataforma en el archivo.

Listo. Para trabajar a diario, ver [Uso diario](#uso-diario).

## macOS

**1. Instala uv:**

```bash
brew install uv
```

Sin Homebrew: `curl -LsSf https://astral.sh/uv/install.sh | sh` y abre una terminal nueva.

**2. Descarga el repositorio e instala el entorno:**

```bash
git clone https://github.com/Ronald1301/Lymphoma-Machine-Learning.git
cd Lymphoma-Machine-Learning
uv sync
```

**3. Comprueba que funciona:**

```bash
uv run python -c "import monai, torch; print(monai.__version__, torch.__version__)"
uv run pytest -q
uv run python scripts/check_env.py --save
```

Debes ver lo mismo que en el [paso 5 de Windows](#windows-11), pero el archivo guardado se llama `env_macos.json`.

## Linux

Solo para Linux x86_64, es decir, un PC normal. En Linux ARM (por ejemplo, una Raspberry Pi) `uv sync` falla, porque el lock no incluye esa plataforma.

**1. Instala uv** y abre una terminal nueva:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Descarga el repositorio e instala el entorno:**

```bash
git clone https://github.com/Ronald1301/Lymphoma-Machine-Learning.git
cd Lymphoma-Machine-Learning
uv sync
```

En Linux, torch se instala en su versión CUDA, la misma que en Kaggle y Colab. Son unos 3 GB de descarga. Si el PC no tiene GPU NVIDIA, funciona igual en CPU.

**3. Comprueba que funciona:**

```bash
uv run python -c "import monai, torch; print(monai.__version__, torch.__version__)"
uv run pytest -q
uv run python scripts/check_env.py --save
```

Debes ver lo mismo que en el [paso 5 de Windows](#windows-11), con dos diferencias: torch aparece como `2.11.0+cu126` y el archivo guardado se llama `env_linux.json`.

## Kaggle

**1. Crea el notebook.** Descarga [`notebooks/setup_kaggle_colab.ipynb`](../../notebooks/setup_kaggle_colab.ipynb) del repositorio. En Kaggle, ve a *Create → New Notebook*, después a *File → Import Notebook*, y sube ese archivo.

**2. Configura la sesión** en el panel derecho (*Session options*):

- *Accelerator*: `GPU T4 x2` o `GPU P100`.
- *Internet*: activado. Si no aparece la opción, la cuenta no está verificada por teléfono (ver T05).

**3. Ejecuta todas las celdas** con *Run All*. La celda de `uv sync` tarda unos minutos.

**4. Revisa la salida de la última celda.** Debe parecerse a esto:

```
monai 1.6.1 | torch 2.11.0+cu126 | CUDA True
...
GPU:        Tesla T4 (sm_75), CUDA 12.6, prueba: ok
OK: el entorno coincide con las versiones fijadas.
```

Con la P100 aparece `sm_60` en lugar de `sm_75`. Si sale `CUDA False`, la GPU no está activada: vuelve al paso 2.

**5. Guarda la evidencia.** Solo hace falta para cerrar T02. Descarga `Lymphoma-Machine-Learning/results/env/env_kaggle.json` desde el panel *Output* y súbelo al repo en `results/env/`.

Kaggle borra el entorno al cerrar la sesión, así que hay que repetir *Run All* al empezar cada sesión.

## Colab

**1. Abre el notebook** desde este enlace:
<https://colab.research.google.com/github/Ronald1301/Lymphoma-Machine-Learning/blob/main/notebooks/setup_kaggle_colab.ipynb>

Otra opción: *Archivo → Subir notebook* y elegir el archivo.

**2. Activa la GPU:** *Entorno de ejecución → Cambiar tipo de entorno de ejecución → T4 GPU*.

**3. Ejecuta todas las celdas:** *Entorno de ejecución → Ejecutar todas*.

**4. Revisa la salida de la última celda.** Debe ser como la del [paso 4 de Kaggle](#kaggle), con `Tesla T4`.

**5. Guarda la evidencia.** Solo hace falta para cerrar T02. Descarga `Lymphoma-Machine-Learning/results/env/env_colab.json` desde el panel *Archivos* (el icono de la carpeta) y súbelo al repo en `results/env/`.

Colab trae Python 3.13, pero eso no afecta: el notebook usa el Python 3.12 del entorno.

### Probar una rama que no está en `main`

En la primera celda de código, cambia `BRANCH = "main"` por el nombre de la rama, por ejemplo `BRANCH = "feat/02-reproducible-environment"`. La rama tiene que estar subida a GitHub. En el enlace de Colab, cambia también `main` por el nombre de la rama.

## Uso diario

| Quiero… | Comando |
|---|---|
| Ejecutar un script | `uv run python scripts/<script>.py` |
| Pasar los tests | `uv run pytest -q` |
| Actualizar el entorno después de un `git pull` | `uv sync` |
| Comprobar el entorno | `uv run python scripts/check_env.py` |
| Usar el entorno en VS Code | *Python: Select Interpreter* y elegir el de `.venv` |
| Entrenar en Kaggle/Colab | Copiar las celdas de código del notebook de setup y después lanzar `run(*UV, "run", "python", "scripts/train.py", "--config", "configs/<experimento>.yaml")` |

Con `uv run` no hace falta activar el entorno. Si prefieres activarlo, usa `.venv\Scripts\activate` en Windows o `source .venv/bin/activate` en macOS y Linux.

## Añadir una dependencia

1. Añádela con versión exacta (`==`). Si no lleva `==`, falla un test.

   ```bash
   uv add "paquete==X.Y.Z"
   ```

   Si solo se usa para desarrollar (tests, formato…): `uv add --dev "paquete==X.Y.Z"`.

2. Regenera `requirements.txt`:

   ```bash
   uv export --frozen --no-hashes --no-dev --no-emit-project -o requirements.txt
   ```

3. Pasa los tests: `uv run pytest -q`.

4. Sube `pyproject.toml`, `uv.lock` y `requirements.txt` juntos, en el mismo PR.

## Sin uv (con pip)

Úsalo solo si uv no funciona. Necesitas Python 3.12 instalado (en Windows: `py install 3.12` o el instalador de python.org).

**Windows:**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pip install pytest==9.2.0
```

**macOS y Linux:** igual, pero las dos primeras líneas son `python3.12 -m venv .venv` y `source .venv/bin/activate`.

**Linux:** añade siempre el índice de PyTorch al tercer comando. Sin él, pip no encuentra la versión `+cu126` de torch:

```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu126
```

No añadas ese índice en Windows ni en macOS. pip descargaría la versión CUDA de torch, que pesa varios GB.

## Si algo falla

| Problema | Qué hacer |
|---|---|
| `uv` no se reconoce como comando | Cierra la terminal y ábrela de nuevo. Si sigue igual, repite el paso 1. |
| `uv sync` falla al descargar | Revisa la conexión. `uv sync` necesita acceso a PyPI, a GitHub y, en Linux, a `download.pytorch.org`. Anota en el issue #4 qué dominio falla. |
| `check_env.py` muestra `PROBLEMAS` | Ejecuta `uv sync` y vuelve a comprobar. Lanza los scripts siempre con `uv run python`: solo `python` usa otro Python. |
| `no kernel image is available` en la P100 | El script está usando el torch de Kaggle en lugar del del entorno. Lánzalo con `uv run` desde la carpeta del repo. |
| `CUDA False` en Kaggle o Colab | La sesión no tiene GPU. Actívala (paso 2) y vuelve a ejecutar todo. |
| Kaggle no deja activar *Internet* | Verifica la cuenta con el teléfono (T05). Si no se puede, avisa al equipo: habrá que subir las librerías como Dataset de Kaggle. |
| Linux: `uv sync` dice que la plataforma no es compatible | Es un Linux ARM. El entorno solo cubre Linux x86_64: usa otro PC o trabaja en Kaggle o Colab. |
| macOS: `Bad CPU type in executable` | uv ha encontrado un Python viejo para Intel. Ejecuta `uv python install` y después `uv sync`. |
| PowerShell no deja ejecutar `.venv\Scripts\activate` | No hace falta activar el entorno. Usa `uv run`. |

## Referencia

| Archivo | Qué fija | ¿Se edita a mano? |
|---|---|---|
| `pyproject.toml` | Las dependencias directas, con `==` | No: se usa `uv add` |
| `uv.lock` | Todas las versiones, incluidas las indirectas, para Windows, macOS y Linux | No: lo genera uv |
| `.python-version` | Python 3.12.16 | No |
| `requirements.txt` | Lo mismo que `uv.lock`, para pip | No: se genera con `uv export` |

- **torch** tiene la misma versión (2.11.0) en todas las plataformas. Lo que cambia es la variante:
  - en Windows y macOS se usa la de CPU;
  - en Linux (incluidos Kaggle y Colab) se usa la `cu126`, que funciona en la T4 y en la P100. El torch que trae Kaggle no funciona en la P100 ([Kaggle/docker-python#1546](https://github.com/Kaggle/docker-python/issues/1546)).
- **No se usa Docker** por tres razones: Kaggle y Colab no permiten imágenes propias, Docker Hub bloquea las IPs de Cuba y, en Windows, el contenedor no tiene acceso a la NPU.
- **La NPU (T47)** usa el entorno que instala AMD (Ryzen AI), que va aparte de este.
