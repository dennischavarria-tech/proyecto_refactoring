---
name: tecnoideas-testing
description: "Genera pruebas unitarias, de integracion y mocks utilizando pytest. Cubre comportamiento, casos limite, manejo de errores y escenarios negativos siguiendo buenas practicas de testing automatizado."
license: MIT
compatibility: opencode
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
metadata:
  author: Custom
  version: "1.0.0"
  domain: testing
  triggers: pytest, unit test, integration test, testing, test coverage, mocks, fixtures
  role: specialist
  scope: edit
  output-format: report
  related-skills: tecnoideas-api-integration, code-reviewer, test-master
---

# TecnoIdeas Testing

Ingeniero que escribe y mantiene tests pytest: unitarios, de integracion, mocks y cobertura.

## Cuando Usar Este Skill

- Crear tests unitarios o de integracion nuevos
- Mockear APIs externas o dependencias del sistema
- Disenar fixtures y datos de prueba
- Parametrizar casos limite
- Auditar o aumentar cobertura con `pytest-cov`
- Reparar tests rotos o flaky

## Preparacion (antes de escribir tests)

1. **Baseline** — Ejecutar la suite existente para saber el estado real (ej. `python -m pytest -q`).
2. **Descubrir convenciones** — Localizar: carpeta/estructura de tests (`tests/`, `test/`), `conftest.py` y fixtures compartidas, estilo de nombrado, mocks ya en uso y dependencias de testing en el manifest (`requirements.txt`, `pyproject.toml`). Reproducir esas convenciones en los tests nuevos.
3. **Comando de cobertura** — Verificar si hay plugin configurado (ej. `pytest-cov`) y el comando para medirlo.

## Flujo de Trabajo

1. **Disenar** — Casos: happy path, casos limite, errores, negativos. **Checkpoint:** listar los casos antes de escribir el test.
2. **Estructura** — Colocar el archivo donde va (unit vs integration), nombre `test_<modulo>.py`, clases `Test*`, metodos `test_*`.
3. **Implementar** — Arrange-Act-Assert; fixtures en `conftest.py` si se reutilizan; mocks para todo lo externo.
4. **Verificar** — Ejecutar el archivo nuevo, luego la suite completa; revisar cobertura del modulo tocado.
5. **Reportar** — Tests agregados, casos cubiertos, cobertura antes/despues.

## Guia de Referencia

| Tema | Referencia | Cargar Cuando |
|------|-----------|---------------|
| Estructura y fixtures | `references/pytest-structure.md` | Creando archivos/fixtures/parametrize |
| Mocking | `references/mocking-strategies.md` | Mockeando APIs, env o servicios |
| Cobertura y calidad | `references/coverage-and-quality.md` | Midiendo o mejorando cobertura |

## Restricciones

### DEBE HACER
- AAA (Arrange-Act-Assert) con un unico comportamiento por test
- Nombres de test que describan escenario + resultado
- Mockear toda red y dependencias de entorno con `monkeypatch`
- Fixtures reutilizables en `conftest.py`
- Asserts sobre comportamiento observable, no sobre implementacion interna
- Suite completa en verde antes de terminar

### NO DEBE HACER
- Tests que llamen a APIs reales
- Hardcodear API keys reales en fixtures
- `sleep()` como sincronizacion ni dependencia de orden entre tests
- Mockear el propio codigo bajo test
- Borrar o reducir assertions para hacer pasar la suite

## Template de Salida

1. **Cobertura inicial** — Resultado baseline
2. **Tests agregados** — Archivo, clases, casos (escenario → assertion)
3. **Mocks usados** — Que se sustituyo y como
4. **Cobertura final** — % antes/despues del modulo tocado
5. **Suite** — Comando y resultado en verde
6. **Huecos** — Comportamientos todavia sin cubrir

## Conocimiento

pytest, fixtures, parametrize, monkeypatch, unittest.mock / pytest-mock, AAA, test doubles (stub/mock/fake), cobertura, test pyramid, flaky tests.