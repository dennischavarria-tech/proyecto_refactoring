# Validacion de Respuestas

Regla central: **el resto de la app nunca ve un `dict` crudo de la API**. Se parsea en la frontera (cliente HTTP) y se devuelve un modelo tipado.

## Flujo

```
HTTP → JSON dict → validar → modelo tipado (dataclass/clase) → logica de negocio → UI
```

## Patron: mapeo en el modelo

```python
@dataclass
class Item:
    id: str
    name: str
    rating: str = ""

    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> Optional["Item"]:
        if data.get("status") != "ok":
            return None
        return cls(
            id=str(data.get("id", "")),
            name=data.get("name", ""),
            rating=str(data.get("rating", "")),
        )
```

- Respuesta invalida / no encontrada → `None` (o excepcion, segun el contrato del servicio).
- `.get(..., default)` con default seguro: un campo ausente no debe lanzar `KeyError` en runtime.
- Claves del JSON solo viven dentro de `from_api_dict`; el resto del codigo usa `item.name`.

## Validacion de entrada del usuario antes del request

Validar y sanitizar la entrada **antes** de llamar a la API, para no gastar requests con basura:

```python
def get_item(self, item_id: str) -> Optional[Item]:
    item_id = validate_id(item_id)        # valida formato/longitud
    item_id = sanitize_input(item_id)     # limpia entradas hostiles
    ...
```

Usar el modulo de validacion/validators que tenga el proyecto; si no existe, crear funciones puras de validacion que lancen la excepcion tipada de entrada invalida.

## Manejo de errores HTTP

| Caso | Accion |
|------|--------|
| Timeout / connection error | Excepcion tipada de fallo de red con `from e` |
| HTTP != 200 | Excepcion tipada con `status_code` |
| JSON invalido (`ValueError`) | Excepcion tipada con detalle, o subclase nueva |
| "No encontrado" en el payload | Devolver `None` (no encontrado no es error) |
| Faltan campos obligatorios | Default seguro en el modelo o `None` |

Si el proyecto tiene jerarquia de excepciones propias, anadir la categoria que falte ahi y exportarla en el paquete de errores:

```python
class APIParseError(BaseAppError):
    def __init__(self, url: str, details: str = "") -> None:
        super().__init__(f"Respuesta invalida de {url}: {details}")
        self.url = url
```

## Errores que jamas deben filtrarse al usuario

- API keys, tokens, headers de autenticacion
- Tracebacks completos de `requests`
- Bodies JSON enteros (loguear longitud o resumen, no el contenido en prod)

Loguear con el logger del modulo (`logging.getLogger(__name__)`) en nivel `warning`/`error`; el usuario ve un mensaje de la excepcion ya redactado.

## Checklist antes de cerrar

- [ ] Todo endpoint devuelve modelo tipado o `None`, nunca `dict`
- [ ] Campos ausentes no revientan con `KeyError`
- [ ] Errores de red/HTTP tipados con `from e`
- [ ] Entrada validada antes del request
- [ ] Sin secretos en logs ni mensajes de error
