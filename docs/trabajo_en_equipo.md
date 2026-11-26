# Trabajo en equipo

Convenciones mínimas para que los cuatro integrantes no se pisen y para que todos conozcan todo el código. Tarea: T04 (#6). Las reglas técnicas del proyecto están en `AGENTS.md`; este documento cubre cómo se coordina el trabajo.

## Ramas

- Una rama por tarea, con el nombre `feat/<tema>` (por ejemplo, `feat/contracts`).
- **Nadie hace push directo a `main`.** La protección de rama exige que todo cambio entre por PR y tenga una aprobación; la Action del ciclo valida además quién debe aprobarlo.
- Antes de empezar una tarea, actualizar `main` (`git pull`) y crear la rama desde ahí.

## Commits

Mensajes en inglés, en minúsculas y en imperativo, con el identificador de la tarea:

```
type(Txx): short description
```

Tipos habituales: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`. Ejemplo: `feat(T01): create repository structure and gitignore`.

## Pull requests

- **Un PR por tarea.** Título: `[Txx] Nombre de la tarea`.
- La plantilla pide «Qué cambia», «Cómo se probó» e «Issue relacionado». Usa `Closes #<número>` solo cuando la tarea esté completa; para avances parciales, usa `Refs #<número>`.
- La plantilla de `.github/pull_request_template.md` se carga sola al abrir el PR.
- `uv run pytest -q` debe pasar antes de pedir revisión.

## Revisión cruzada

Cada PR lo revisa el siguiente integrante del anillo:

```
Ronald → Agustin → Dylan → Abel → Ronald
```

| Autor del PR | Revisor |
|---|---|
| Ronald | Agustin |
| Agustin | Dylan |
| Dylan | Abel |
| Abel | Ronald |

- Los usernames verificados en GitHub son: Ronald `Ronald1301`, Agustín `agustin030902`, Dylan `Dylan2108` y Abel `amircalabel`.
- `.github/workflows/pr-review-cycle.yml` solicita al siguiente integrante del anillo y exige su aprobación del último commit para PR dirigidos a `main`. No aprueba PRs ni los fusiona.
- La protección de `main` requiere PR, una aprobación, aprobación posterior al último push, conversaciones resueltas y sin force-push ni eliminación.
- El coordinador semanal fusiona después de la aprobación correcta y de que pasen los checks. GitHub protege el requisito de aprobación; quién pulsa «Merge» no se puede seleccionar dinámicamente por autor en este repositorio personal, así que esa parte sigue siendo una regla del equipo.
- Las tareas que piden el acuerdo de todos (por ejemplo, T03 y T10) necesitan la confirmación de los cuatro en el PR o en el issue.
- El revisor comprueba que el código cumple los contratos de `docs/contratos.md`, que los tests pasan y que no se suben datos ni checkpoints.

### Puesta en marcha de la protección

La regla de `main` se configura primero para exigir PR y una aprobación. El check `review-cycle` se añade a los checks obligatorios después de que el PR que instala este workflow sea aprobado y fusionado; GitHub no puede ejecutar como política estable un workflow que todavía no está en la rama predeterminada. Hasta entonces, el PR de instalación debe ser aprobado por Agustín y su autor no debe aprobarlo ni fusionarlo.

## Definition of Done

Una tarea está terminada cuando:

1. El código está en `main` a través de un PR revisado.
2. Los tests pasan.
3. La salida está documentada (archivo en `results/` o sección en `docs/`).
4. El issue está cerrado, con enlace al PR.

## Coordinador semanal

El coordinador rota cada semana, según el plan de `docs/planificacion/issues_tareas.md`:

| Semana | Fechas | Fases | Coordina |
|---|---|---|---|
| 1 | 2–8 nov | 0 | Ronald |
| 2 | 9–15 nov | 1, 2, 7 | Agustin |
| 3 | 16–22 nov | 1, 2, 7 | Dylan |
| 4 | 23 nov – 1 dic | 3, 4 | Abel |
| 5 | 2–8 dic | 4, 7 | Ronald |
| 6 | 9–13 dic | 5, 6 | Agustin |
| 7 | 14–20 dic | 6, 7 | Dylan |
| Colchón | 21–31 dic | — | Abel |

Funciones del coordinador durante su semana (propuesta, a confirmar por el equipo):

- Revisar el estado de los issues de la semana y avisar de las tareas bloqueadas o con retraso.
- Comprobar que cada PR abierto tiene revisor y que las revisiones no se quedan paradas.
- Convocar la reunión de integración al cerrar las fases 1, 3 y 5, para verificar que las salidas cumplen los contratos.
- Dejar un resumen breve al final de la semana: qué se cerró, qué queda pendiente y qué decisiones se tomaron.

El coordinador no reasigna tareas por su cuenta: los cambios de responsable se acuerdan con el jefe del equipo (Ronald).

## Reproducibilidad

- Todo script o entrenamiento llama a `set_seed()` (`src/lymphoma/utils.py`) al empezar. La semilla por defecto es 42; las semillas adicionales usan 43.
- Los parámetros experimentales van en `configs/*.yaml`, no en el código.
