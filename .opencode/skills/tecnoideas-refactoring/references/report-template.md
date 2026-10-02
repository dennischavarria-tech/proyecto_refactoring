# Template de Reporte de Refactorizacion

Entregar este reporte al cerrar la sesion. Completar todas las secciones; si una no aplica, indicarlo explicitamente.

```markdown
# Reporte de Refactorizacion — <fecha>

## 1. Alcance
- Categoria(s) atacada(s): <ej. f-strings, type hints>
- Archivos incluidos: <lista>

## 2. Baseline
- Comando de tests: `<comando>` antes de cambios: **N passed** (verde/rojo)

## 3. Practicas eliminadas
| Practica | Ocurrencias | Ubicaciones |
|----------|-------------|-------------|
| concatenacion → f-strings | 12 | modulo_a.py:152-162, modulo_b.py:66 |

## 4. Archivos modificados
- `modulo_a.py` — 10 f-strings, sin cambios de firma
- `modulo_b.py` — 2 f-strings, extraccion de helper `validate_feature`

## 5. Verificacion
- Grep restante en alcance: 0 ocurrencias
- `<comando>` despues: **N passed**

## 6. Pendientes (fuera de alcance)
- N `global` en modulo_x.py, modulo_y.py
- type hints en modulo_z.py (N firmas sin `->`)

## 7. Riesgo
- Bajo | Medio | Alto — <justificacion en una frase>
```

## Reglas del reporte

- Siempre referencias `archivo:linea`, nunca "varios archivos".
- El resultado de la suite baseline y final es obligatorio; sin el, el lote no se da por terminado.
- Los pendientes se listan con recuento real (grep), no estimaciones.
- Si se revertio algun lote, mencionarlo en "Verificacion" con el motivo.
