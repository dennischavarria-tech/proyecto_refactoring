# Patron de Cliente HTTP

Estructura estandar para el modulo de clientes HTTP de un proyecto Python.

## Esqueleto

```python
import os
from typing import Any, Dict, Optional

import requests

_logger = logging.getLogger(__name__)


class NuevaApiClient:
    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30,
                 session: Optional[requests.Session] = None) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._timeout = timeout
        self._session = session or requests.Session()

    def _validate_api_key(self) -> None:
        if not self._api_key:
            _logger.error("API key no configurada")
            raise InvalidInputError("api_key", "", "Configure NUEVA_API_KEY en el entorno")

    def _make_request(self, url: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        _logger.debug("Haciendo request a %s", url)
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.RequestException as e:
            _logger.error("Error de conexion: %s", e)
            raise APIConnectionError(url=url, details=str(e)) from e

        if response.status_code != 200:
            _logger.warning("Respuesta no exitosa: HTTP %s de %s", response.status_code, url)
            raise APIConnectionError(url=url, status_code=response.status_code)

        return response.json()
```

(Adaptar `InvalidInputError`/`APIConnectionError` al manejo de errores tipado del proyecto; si no existe, crear excepciones propias subclaseando la base del proyecto o `Exception`.)

## Reglas

- URLs y keys salen de configuracion/entorno (`.env`, `config.py`, `settings`), nunca hardcodeadas.
- Timeout siempre explicito; sin `timeout` la llamada puede colgarse indefinidamente.
- El cliente no contiene logica de negocio: solo HTTP + parseo basico.
- El cliente no importa servicios ni UI; la dependencia va al reves (DI): el servicio recibe el cliente por constructor.
- `session` inyectable para poder mockear/aislar en tests.
- Un modulo/clase por API externa.

## Checklist antes de cerrar

- [ ] Timeout en todas las llamadas
- [ ] Errores de red → excepcion tipada del proyecto con `from e`
- [ ] API key validada antes del request y ausente de logs
- [ ] Servicio recibe el cliente por constructor
- [ ] Suite de tests en verde
