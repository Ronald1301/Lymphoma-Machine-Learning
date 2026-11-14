# Trabajo en equipo

Convenciones mínimas para que los cuatro integrantes no se pisen y para que todos conozcan todo el código. Tarea: T04 (#6). Las reglas técnicas del proyecto están en `AGENTS.md`; este documento cubre cómo se coordina el trabajo.

## Ramas

- Una rama por tarea, con el nombre `feat/<tema>` (por ejemplo, `feat/contracts`).
- **Nadie hace push directo a `main`.** La rama `main` no está protegida en GitHub, así que esta es una regla acordada por el equipo: todo cambio entra por pull request.
- Antes de empezar una tarea, actualizar `main` (`git pull`) y crear la rama desde ahí.

## Commits

Mensajes en inglés, en minúsculas y en imperativo, con el identificador de la tarea:

```
type(Txx): short description
```

Tipos habituales: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`. Ejemplo: `feat(T01): create repository structure and gitignore`.

## Pull requests

- **Un PR por tarea.** Título: `[Txx] Nombre de la tarea`.
- La descripción enlaza el issue con `Closes #<número del issue>`, para que se cierre al fusionar. El número es el del issue en GitHub, que no siempre coincide con el de la tarea.
- La plantilla de `.github/pull_request_template.md` se carga sola al abrir el PR.
- `pytest -q` debe pasar antes de pedir revisión.

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

- El revisor asignado de cada tarea figura en su issue.
- El PR se fusiona cuando el revisor asignado lo aprueba. El autor no fusiona su propio PR sin esa aprobación.
- Las tareas que piden el acuerdo de todos (por ejemplo, T03 y T10) necesitan la confirmación de los cuatro en el PR o en el issue.
- El revisor comprueba que el código cumple los contratos de `docs/contratos.md`, que los tests pasan y que no se suben datos ni checkpoints.

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
