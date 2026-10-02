# Estrategias de Mocking

Objetivo: tests rapidos y deterministas. **Ningun test toca la red real.**

## Que mockear

| Dependencia | Doble | Herramienta |
|-------------|-------|-------------|
| HTTP / clientes externos | Stub de respuesta | `monkeypatch` sobre el cliente o `Mock` del servicio |
| Env vars / configuracion | Fixture | `monkeypatch.setenv` |
| Archivos en disco | tmp dir | `tmp_path` |
| Reloj / fechas | Stub | `monkeypatch` de `time`/`datetime` |
| Servicios en tests de otra capa | Mock | `Mock()` inyectado por DI |

**No** mockear: el codigo propio bajo test, ni funciones que solo computan.

## Patron 1 — Mock del cliente via DI (preferido)

```python
from unittest.mock import Mock

def test_search_calls_client_once(service, mock_client, sample_result):
    # Arrange
    mock_client.search = Mock(return_value=[sample_result])
    # Act
    result = service.search("query")
    # Assert
    assert result == [sample_result]
    mock_client.search.assert_called_once_with("query")
```

Ventaja: no se instala nada de red; se verifica ademas **que se llamo** (interaccion).

## Patron 2 — `monkeypatch` del modulo HTTP

Fixture tipica en `conftest.py`:

```python
@pytest.fixture
def mock_http_get(monkeypatch):
    def _fake_get(url, params=None, timeout=None, **kwargs):
        resp = Mock()
        resp.status_code = 200
        resp.json.return_value = {"status": "ok", "id": "1", "name": "Item"}
        return resp
    monkeypatch.setattr("requests.get", _fake_get)
```

Usar cuando el test ejercita el cliente HTTP real sin salir a internet.

## Patron 3 — `pytest-mock` (`mocker`)

Da la misma API que `unittest.mock` con auto-limpieza:

```python
def test_timeout_raises(mocker):
    mocker.patch("requests.get", side_effect=requests.Timeout("slow"))
    client = ApiClient(timeout=1)
    with pytest.raises(ConnectionErrorTipada):
        client.get_item("1")
```

## Patron 4 — Respuestas de error

```python
def test_connection_error(mocker):
    mocker.patch("requests.get", side_effect=requests.ConnectionError("down"))
    with pytest.raises(ConnectionErrorTipada):
        ...

def test_http_500(mocker):
    resp = Mock(status_code=500)
    mocker.patch("requests.get", return_value=resp)
    with pytest.raises(ConnectionErrorTipada):
        ...
```

## Buenas practicas

- Mockear en el borde (`requests` o el cliente), no en el medio de la logica.
- `assert_called_once_with(...)` para validar argumentos; `assert_not_called()` para caminos que no deben ejecutar requests.
- `side_effect` para errores/estados; `return_value` para exito.
- No usar `time.sleep()` real: si hay backoff, mockear `time.sleep` o inyectar el sleep.
- Datos de respuesta realistas pero recortados: solo los campos que consume el test.
- Si el mock se vuelve enorme, es senal de que falta una fixture en `conftest.py`.
