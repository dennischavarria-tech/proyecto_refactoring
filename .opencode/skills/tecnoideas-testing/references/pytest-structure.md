# Estructura pytest y Fixtures

## Distribucion de archivos

Estructura tipica (adaptar a la del proyecto):

```
tests/
  conftest.py          # fixtures compartidos (NO importar tests entre si)
  unit/                # rapidos, sin red, sin disco
    test_<modulo>.py
  integration/         # cruzan fronteras (BD, APIs) siempre mockeadas/fakeadas
    test_<flujo>.py
```

Convenciones:
- Archivo: `test_<modulo>.py` espejando el modulo de origen.
- Clase: `Test<Modulo>`; metodo: `test_<escenario>_<condicion>_<resultado>`.
- Un comportamiento observable por test.

## Arrange-Act-Assert

```python
def test_add_to_cart_returns_true(cart_service, sample_item):
    # Arrange
    # Act
    result = cart_service.add(sample_item)
    # Assert
    assert result is True
    assert cart_service.items() == [sample_item]
```

Evitar logica (ifs, loops) dentro de los tests: si la rama es compleja, el test debe ser parametrizado.

## Fixtures

Reglas:
- Reutilizable por 2+ tests → `conftest.py` (el mas cercano en la jerarquia).
- Solo para un test → fixture local en el archivo.
- Las fixtures de datos devuelven objetos puros; no hacen IO.

```python
@pytest.fixture
def order_service(mock_env_vars):
    client = ApiClient(base_url="http://test.local", api_key="test_key", timeout=5)
    return OrderService(api_client=client)
```

Fixture con `monkeypatch` para entorno:

```python
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_key")
    monkeypatch.setenv("API_URL", "http://test.local/")
```

`monkeypatch` se deshace solo al terminar el test: no limpies manualmente env vars con `os.environ.pop`.

## Parametrize

```python
@pytest.mark.parametrize("value,expected", [
    ("", False),
    ("   ", False),
    ("valid", True),
    ("x" * 500, False),
])
def test_validate_input(value, expected):
    assert validate_input(value) is expected
```

Usar parametrize para: casos limite, tablas de equivalencia, formatos de entrada invalidos.

## Orden y aislamiento

- Cada test debe poder ejecutarse solo: `pytest tests/unit/test_<modulo>.py -q`.
- Sin dependencia de estado entre tests (nada de "el test 3 asume que el 2 dejo estado").
- Estado compartido solo via fixtures con scope documentado (`scope="module"` si es caro).

## Comandos

```bash
pytest -q                                  # suite completa
pytest tests/unit/test_<modulo>.py -q      # un archivo
pytest -k "<patron>" -q                    # por nombre
pytest -x -q                               # parar en el primer fallo
pytest -k integration -q                   # solo integracion
```
