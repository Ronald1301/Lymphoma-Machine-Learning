<!-- Título del PR: [Txx] Nombre de la tarea -->

## Qué cambia

-

## Cómo se probó

- [ ] `pytest -q` pasa en local
- [ ] No aplica (explicar por qué)

## Issue relacionado

- `Closes #<número>` si la tarea queda completa; `Refs #<número>` para un avance parcial.

## Definition of Done

- [ ] El código cumple los contratos de `docs/contratos.md`
- [ ] Cada módulo nuevo tiene su test en `tests/`
- [ ] La salida está documentada (archivo en `results/` o sección en `docs/`)
- [ ] No se suben datos, checkpoints ni archivos `*.nii.gz`, `*.pt` u `*.onnx`
- [ ] Ningún parámetro experimental está escrito en el código (va en `configs/*.yaml`)
- [ ] Revisor asignado según el anillo Ronald → Agustin → Dylan → Abel → Ronald
