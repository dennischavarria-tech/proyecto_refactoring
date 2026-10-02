---
name: tecnoideas-refactoring
description: "Refactoriza codigo Python eliminando malas practicas, deuda tecnica y code smells manteniendo el comportamiento existente. Aplica refactorizaciones incrementales, verificables y seguras mediante la suite de pruebas disponible del proyecto. Utilizar para clean code, technical debt, code smells, type hints, dependency injection, dataclasses, eliminacion de duplicacion y mejoras de mantenibilidad."
license: MIT
compatibility: opencode
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
metadata:
  author: Custom
  version: "1.0.0"
  domain: code-quality
  triggers: refactoring, clean code, technical debt, code smells, maintainability, type hints, dependency injection, dry, solid
  role: specialist
  scope: edit
  output-format: report
  related-skills: code-reviewer, architecture-designer, test-master, legacy-modernizer
---

# TecnoIdeas Refactoring

Ingeniero senior que elimina malas practicas del codigo Python manteniendo el comportamiento identico y verificando cada cambio con la suite de tests del proyecto.

## Cuando Usar Este Skill

- Eliminar variables globales y `global` statements
- Reemplazar wildcard imports por imports especificos
- Convertir concatenacion de strings a f-strings
- Agregar type hints a funciones
- Eliminar codigo duplicado
- Reemplazar `except:`/`except Exception` genericos por excepciones especificas
- Convertir dicts de datos a dataclasses
- Introducir inyeccion de dependencias
- Separar responsabilidades en modulos

## Preparacion (antes de tocar codigo)

1. **Entender el proyecto** — Identificar: lenguaje/version, gestor de dependencias, **comando de tests** (ej. `python -m pytest`, `python -m unittest`, `npm test`) y linter/formatter configurado. Si hay linter/formatter, no discutir estilo: usarlo.
2. **Baseline** — Ejecutar la suite completa. Si ya falla, detenerse y reportarlo: no refactorizar sobre tests rojos.
3. **Rama** — Trabajar en una rama/commits separados para que el diff de refactorizacion sea revisable por separado.

## Flujo de Trabajo

1. **Deteccion** — Buscar el patron con Grep (comandos en el catalogo). Listar ocurrencias como `archivo:linea`.
2. **Priorizacion** — Una categoria de malas practica por vez, en lotes pequenos (~100 lineas de diff).
3. **Refactorizar** — Aplicar el patron antes/despues del catalogo; comportamiento publico identico.
4. **Verificar** — Suite de tests tras cada lote; si falla, revertir el lote y partirlo mas pequeno.
5. **Reportar** — Entregar el reporte con el template de cierre.

## Guia de Referencia

| Tema | Referencia | Cargar Cuando |
|------|-----------|---------------|
| Catalogo de malas practicas | `references/bad-practices-catalog.md` | Detectando o aplicando cada patron |
| Refactorizacion segura | `references/safe-refactoring.md` | Antes de editar, resolviendo tests rotos, dividiendo lotes |
| Reporte de cierre | `references/report-template.md` | Escribiendo el resumen final de la sesion |

## Restricciones

### DEBE HACER
- Suite en verde antes del primer cambio y tras cada lote
- Cambiar una categoria a la vez, en lotes pequenos con git diff legible
- Preservar mensajes, retornos, claves de JSON y firmas publicas
- Reutilizar las convenciones del proyecto (manejo de errores, logging, estilo de modulos)
- Actualizar todos los call sites al renombrar o mover algo

### NO DEBE HACER
- Cambiar comportamiento observable del programa
- Editar o borrar tests para hacer pasar la suite
- Introducir dependencias nuevas sin pedir permiso
- Refactorizar archivos fuera del alcance acordado
- Hacer un refactor grande sin verificacion intermedia

Si un cambio exige alterar comportamiento: parar y preguntar al usuario.