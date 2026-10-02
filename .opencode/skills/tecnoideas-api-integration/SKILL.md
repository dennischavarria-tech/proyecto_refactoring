---
name: tecnoideas-api-integration
description: "Implementa integraciones robustas con APIs REST externas siguiendo buenas practicas de resiliencia, manejo de errores, configuracion, logging, validacion de respuestas y pruebas automatizadas. Utilizar cuando se consuman APIs externas, servicios HTTP, microservicios o integraciones de terceros."
license: MIT
compatibility: opencode
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
metadata:
  author: Custom
  version: "1.0.0"
  domain: integration
  triggers: api integration, rest api, http client, requests, external service, microservice, webhook, third party api
  role: specialist
  scope: edit
  output-format: report
  related-skills: tecnoideas-testing, code-reviewer, architecture-designer
---

# TecnoIdeas API Integration

Ingeniero que integra APIs REST externas con clientes robustos, errores tipados, validacion de respuestas y tests.

## Cuando Usar Este Skill

- Crear o refactorizar un cliente HTTP para una API externa
- Manejar timeouts, reintentos, rate limiting o errores de red
- Validar/mapear respuestas JSON a modelos tipados
- Conectar un servicio nuevo a una API de terceros
- Logging o cache de requests

## Preparacion (antes de tocar codigo)

1. **Contrato** — Definir: endpoint, metodo, autenticacion, rate limit, formato de respuesta y modo de fallo. **Checkpoint:** resumir el contrato en una frase antes de codificar.
2. **Convenciones del proyecto** — Localizar donde viven los clientes HTTP existentes, el manejo de errores tipado, la configuracion de secretos (`.env`/config) y el logger. Seguir esas mismas convenciones; si no existen, aplicar el patron de la referencia.
3. **Comando de tests** — Identificar como se ejecuta la suite (ej. `python -m pytest`) para verificar al final.

## Flujo de Trabajo

1. **Cliente** — Crear/refactorizar el cliente HTTP: timeout por defecto, params tipados, sin secretos en logs.
2. **Errores** — Mapear fallos de red/HTTP a una excepcion tipada del proyecto con `raise ... from e`.
3. **Validacion** — Parsear la respuesta a un modelo tipado (dataclass/clase); nunca devolver dicts crudos a la logica de negocio.
4. **Resiliencia** — Aplicar reintentos/backoff o cache solo donde el caso de uso lo justifique (ver referencia).
5. **Verificar** — Suite de tests (unit con mocks + integration) antes de cerrar.

## Guia de Referencia

| Tema | Referencia | Cargar Cuando |
|------|-----------|---------------|
| Patron de cliente | `references/client-pattern.md` | Creando o refactorizando un cliente HTTP |
| Resiliencia | `references/resilience-patterns.md` | Agregando timeouts, reintentos, rate limiting |
| Validacion de respuestas | `references/response-validation.md` | Parseando JSON, mapeando a modelos, manejando errores HTTP |

## Restricciones

### DEBE HACER
- Timeout explicito en toda llamada HTTP
- Errores de red/HTTP convertidos en excepciones tipadas del proyecto
- Secretos (API keys) solo via variables de entorno/config, nunca en logs ni en mensajes
- Respuestas mapeadas a modelos tipados
- Tests unitarios con mocks antes de tocar la red real

### NO DEBE HACER
- Llamadas HTTP sueltas fuera del modulo de clientes
- `except Exception: pass` o respuestas `None` silenciosas sin log
- Hardcodear URLs o keys dentro de la logica de negocio
- Compartir un session/cliente global mutable entre modulos

## Template de Salida

1. **Contrato** — API, endpoint, autenticacion
2. **Cambios** — Archivos creados/modificados con `archivo:linea`
3. **Errores y timeouts** — Como se propagan
4. **Validacion** — Modelo destino y caso invalido
5. **Verificacion** — Resultado de la suite de tests
6. **Pendientes** — Cache, reintentos o rate limit no implementados

## Conocimiento

HTTP/1.1, codigos de estado, idempotencia, backoff exponencial con jitter, circuit breaker, OpenAPI, DI, EAFP, PEP 8.