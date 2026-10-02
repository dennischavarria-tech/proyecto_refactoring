# Catalogo de Malas Practicas

Cada entrada: severidad, comando de deteccion (Grep) y patron de refactorizacion aplicado a codigo Python.

## Resumen

| # | Practica | Severidad | Deteccion rapida |
|---|----------|-----------|------------------|
| 1 | Excepciones genericas | critica | `grep -rn "except:" --include="*.py" .` |
| 2 | Wildcard imports | mayor | `grep -rn "import \*" --include="*.py" .` |
| 3 | Concatenacion de strings | menor | `grep -rn '" + \|+ str(' --include="*.py" .` |
| 4 | Sin type hints | mayor | `grep -rn "def .*):$" --include="*.py" . \| grep -v "\->"` |
| 5 | Dicts como modelos | mayor | `grep -rn "Dict\[str, Any\]" --include="*.py" .` |
| 6 | Codigo duplicado | mayor | `grep -rn "def " --include="*.py" . \| awk -F: '{print $NF}' \| sort \| uniq -d` |
| 7 | Acoplamiento / falta de DI | mayor | `grep -rn "import requests" --include="*.py" .` |
| 8 | Responsabilidades mezcladas | mayor | `wc -l *.py \| sort -rn \| head` |
| 9 | Variables globales | mayor | `grep -rn "global " --include="*.py" . \| grep -v tests` |

Ejecutar los comandos antes de empezar para obtener el recuento real en el proyecto actual.

---

## 1. Excepciones genericas

**Severidad:** critica (oculta bugs, traga `KeyboardInterrupt`)
**Deteccion:**

```bash
grep -rn "except:" --include="*.py" .
grep -rn "except Exception" --include="*.py" .
```

**Antes:**

```python
try:
    data = requests.get(url, timeout=5).json()
except:
    return None
```

**Despues:**

```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
except (requests.Timeout, requests.ConnectionError) as exc:
    raise APIConnectionError(url=url, details=str(exc)) from exc
except ValueError as exc:
    raise APIConnectionError(url=url, details=f"JSON invalido: {exc}") from exc
```

Usar la jerarquia de excepciones del proyecto (subclase de `Exception` o de la base de errores propia); si falta una categoria de error, anadirla al modulo/paquete de excepciones y exportarla. Nunca `except: pass`.

---

## 2. Wildcard imports

**Severidad:** mayor (namespace contaminado, dependencias invisibles)
**Deteccion:**

```bash
grep -rn "import \*" --include="*.py" .
```

**Antes:**

```python
from utils import *
```

**Despues:**

```python
from utils import print_header, export_to_csv, clear_screen
```

Listar explicitamente solo los simbolos usados en el archivo.

---

## 3. Concatenacion de strings con `+`

**Severidad:** menor (legibilidad, errores con `str()`)
**Deteccion:**

```bash
grep -rn '" + \|+ str(' --include="*.py" .
```

**Antes:**

```python
validation_errors.append("Error " + str(i) + " missing id")
backup_name = "errors_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
```

**Despues:**

```python
validation_errors.append(f"Error {i} missing id")
backup_name = f"errors_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
```

Excepcion: repetir con `*` (`"=" * 50`) o unir listas con `+` es correcto, no tocar.

---

## 4. Funciones sin type hints

**Severidad:** mayor (contratos invisibles, sin ayuda de mypy/IDE)
**Deteccion:**

```bash
grep -rn "def [a-zA-Z_]*(.*)\s*:" --include="*.py" . | grep -v "\->"
```

**Antes:**

```python
def buscar(title, year=None):
```

**Despues:**

```python
def buscar(title: str, year: Optional[str] = None) -> Optional[Item]:
```

Leer la implementacion para deducir el tipo real; no adivinar. Anotar parametros y retorno; usar tipos ya importados en el archivo.

---

## 5. Dicts como modelos de datos

**Severidad:** mayor (typos de keys en runtime, sin autocompletado)
**Deteccion:**

```bash
grep -rn "Dict\[str, Any\]" --include="*.py" .
grep -rn '\.get("Title"\|\.get("title"' --include="*.py" .
```

**Antes:**

```python
def render(data: Dict[str, Any]) -> None:
    print(data["Title"], data["Year"])
```

**Despues:**

```python
@dataclass
class Item:
    title: str
    year: str

def render(item: Item) -> None:
    print(item.title, item.year)
```

Convertir en la frontera donde se recibe el JSON (respuesta de API, archivo, evento) mediante un `from_api_dict()` en el propio modelo; propagar el dataclass hacia adentro.

---

## 6. Codigo duplicado

**Severidad:** mayor (DRY, cambios en varios lugares)
**Deteccion:**

```bash
grep -rn "def " --include="*.py" . | awk -F: '{print $NF}' | sort | uniq -d
```

Comparar funciones con logica similar (clientes de dos APIs distintas, modulos `*_manager` repetidos). Duplicacion aceptada: tests y wrappers de una linea con distinto significado.

**Antes:** dos funciones identicas salvo un parametro.

**Despues:** una generica con parametro + dos wrappers de una linea, o helper compartido en el modulo de utilidades.

---

## 7. Acoplamiento a dependencias (falta de DI)

**Severidad:** mayor (tests lentos, imposible de mockear)
**Deteccion:**

```bash
grep -rn "import requests" --include="*.py" .
```

**Antes:**

```python
class OrderService:
    def search(self, query: str):
        resp = requests.get(HARD_CODED_URL, params={"apikey": os.environ["KEY"], ...})
```

**Despues:**

```python
class OrderService:
    def __init__(self, api_client: ApiClient) -> None:
        self._api_client = api_client
```

El HTTP vive en un modulo/clase de clientes; los servicios lo reciben por constructor; los tests inyectan mocks o stubs.

---

## 8. Responsabilidades mezcladas

**Severidad:** mayor (modulos que hacen IO + logica + presentacion)
**Deteccion:**

```bash
wc -l *.py | sort -rn | head
```

**Direccion de extraccion:** logica de negocio → capa de servicios, HTTP → clientes externos, estructuras de datos → modelos/DTOs, helpers puros → modulo de utilidades, errores → paquete de excepciones.
No extraer modulos de una sola funcion ni por menos de dos responsabilidades reales.

---

## 9. Variables globales

**Severidad:** mayor (estado oculto, acoplamiento, dificil de testear)
**Deteccion:**

```bash
grep -rn "global " --include="*.py" . | grep -v test
grep -rn "^[A-Z_][A-Z_0-9]* = \[\]\|^[A-Z_][A-Z_0-9]* = {}\|^[a-z_]* = \[\]\|^[a-z_]* = {}" --include="*.py" .
```

**Antes:**

```python
app_state = {}

def set_value(key, value):
    global app_state
    app_state[key] = value
```

**Despues:**

```python
class StateManager:
    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}

    def set_value(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get_value(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)
```

Alternativa menos invasiva si no se puede tocar todo el call site: mantener el estado como atributo de modulo **dentro** del manager y exponer funciones que no usen `global` en otros archivos (el `global` solo apunta al estado declarado en su propio modulo).

---

## Orden de Ataque

1. Excepciones genericas (critica)
2. Wildcard imports (rapido, bajo riesgo)
3. Concatenacion → f-strings (rapido, bajo riesgo)
4. Type hints (lectura de implementacion obligatoria)
5. Codigo duplicado → extraccion
6. Dicts → dataclasses
7. DI y extraccion de responsabilidades (mayor esfuerzo)
8. Variables globales (ultima: mas invasiva, toca muchos call sites)

Una categoria por lote, suite de tests tras cada lote (ver `safe-refactoring.md`).
