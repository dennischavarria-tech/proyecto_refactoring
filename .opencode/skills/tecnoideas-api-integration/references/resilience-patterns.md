# Patrones de Resiliencia

Aplicar solo donde el caso de uso lo justifique; no todo request necesita reintentos. En los ejemplos, `APIConnectionError` es un ejemplo: usar la excepcion tipada de red/HTTP que defina el proyecto.

## 1. Timeout

```python
# MAL: sin timeout, la request puede colgarse
requests.get(url)

# BIEN: timeout por defecto del client (conexion + lectura)
requests.get(url, timeout=(5, 30))
```

Definir un timeout por defecto en el cliente (p. ej. 30s de conexion/lectura) y reutilizarlo en todas las llamadas.

## 2. Reintentos con backoff exponencial

Solo para operaciones **idempotentes** (GET), nunca para POST/PUT.

```python
import time
from typing import Callable, TypeVar

import requests

T = TypeVar("T")

def retry_with_backoff(
    fn: Callable[[], T],
    retries: int = 3,
    base_delay: float = 0.5,
    retry_on: tuple = (requests.Timeout, requests.ConnectionError),
) -> T:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            return fn()
        except retry_on as exc:
            last_exc = exc
            delay = base_delay * (2 ** attempt)
            _logger.warning("Intento %s falló, reintentando en %.1fs: %s", attempt + 1, delay, exc)
            time.sleep(delay)
    raise APIConnectionError(url="n/a", details=str(last_exc)) from last_exc
```

- Respuesta HTTP 4xx/5xx **no** se reintenta igual: 4xx es error del cliente (no cambia con retry); 429 y 5xx pueden reintentarse con limite.
- Siempre con tope de reintentos y delay creciente.

## 3. Rate limiting (429)

```python
if response.status_code == 429:
    retry_after = int(response.headers.get("Retry-After", 5))
    _logger.warning("Rate limit alcanzado, esperando %ss", retry_after)
    time.sleep(retry_after)
    raise APIConnectionError(url=url, status_code=429)
```

Registrar el fallo y dejar que el caller decida; no dormir dentro del client si bloquea la UI.

## 4. Cache de respuestas

Patron recomendado:

- Clave normalizada: `f"{endpoint}:{query.lower().strip()}"`.
- TTL corto (minutos) para datos que cambian poco.
- Cache **dentro del servicio**, no del cliente HTTP (asi el cliente sigue siendo stateless y testeable).

## 5. Circuit breaker (solo si hay fallos recurrentes)

Si una API se cae seguido: tras N fallos consecutivos, fallar rapido durante M segundos en vez de golpear la API en cada request. Implementarlo como wrapper alrededor de `_make_request`, no dentro de cada endpoint.

## Decision rapida

| Situacion | Aplicar |
|-----------|---------|
| GET simple, uso interactivo | Timeout + log |
| API inestable o red movil | Timeout + retry con backoff (2-3 intentos) |
| Endpoints caros / multiples llamadas | Cache con TTL |
| Muchos usuarios / 429 frecuentes | Rate limit + Retry-After |
| Caida prolongada conocida | Circuit breaker |
