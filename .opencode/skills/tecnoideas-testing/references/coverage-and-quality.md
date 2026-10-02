# Cobertura y Calidad de Tests

## Comandos

```bash
pytest -q                                            # suite
pytest -q --cov=. --cov-report=term-missing          # cobertura con huecos (si hay pytest-cov)
pytest -q --cov=. --cov-report=html                  # reporte HTML
pytest -q --cov=. --cov-fail-under=80                # gate opcional
```

## Leer el reporte

- Columna `missing`: lineas **no** ejecutadas → candidatas a test nuevo.
- Distinguir: logica de negocio (obligatorio cubrir) vs `if __name__ == "__main__"` / prints decorativos (bajo valor).
- Cobertura alta no es meta: un 90% de asserts debiles no vale mas que 60% con asserts de comportamiento.

## Prioridad de cobertura (tipica)

1. Logica de negocio / servicios — decisiones, reglas, cache
2. Modelos y parsers — campos ausentes, payloads invalidos, casos de "no encontrado"
3. Validaciones — entradas invalidas, limites
4. Clientes de red — timeouts, HTTP != 200, JSON invalido (todo mockeado)
5. Utilidades y helpers — casos de error y ramas no obvias

## Que cubrir en cada modulo nuevo

| Tipo de funcion | Casos minimos |
|-----------------|---------------|
| Validacion | valido, invalido, limite superior/inferior, vacio |
| Busqueda API | exito, no encontrado (`None`), error de red |
| Cache | primero consulta, segundo usa cache (sin nueva llamada) |
| Coleccion (add/remove) | agregar, duplicado, eliminar existente, eliminar inexistente |
| Parser | payload completo, campo faltante, payload de error |

## Calidad de asserts

```python
# DEBIL: solo comprueba que no exploto
assert service.search("x") is not None

# FUERTE: comprueba el contrato
result = service.search("x")
assert result.id == "1"
assert result.name == "Item"
client.search.assert_called_once_with("x")
```

## Tests flaky: causas comunes

- Orden dependiente entre tests (estado global compartido) → aislar con fixtures.
- Red real → siempre mockear.
- Fechas/horas reales → fijar o mockear.
- `sleep()` real → mockear.

## Antes de dar por terminado

```bash
pytest -q
```

- [ ] Suite completa en verde
- [ ] Tests nuevos corren solos: `pytest tests/<archivo> -q`
- [ ] Sin llamadas a la red real
- [ ] Cobertura del modulo tocado sin lineas criticas en `missing`
