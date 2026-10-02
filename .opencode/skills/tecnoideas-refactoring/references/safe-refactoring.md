# Refactorizacion Segura

Protocolo para cambiar codigo sin romper comportamiento. En los ejemplos, `$TEST` = comando de tests del proyecto (ej. `python -m pytest -q`); identificarlo antes de empezar.

## 1. Aislamiento y baseline

```bash
git status                                   # working tree limpio
git checkout -b refactor/<categoria>         # rama dedicada a la sesion
$TEST                                        # suite en verde antes de empezar
$TEST --cov=. --cov-report=term-missing      # cobertura inicial (opcional, si hay plugin)
```

- Si el baseline falla: **no refactorizar**. Reportar los tests rotos y esperar instrucciones.
- Commit del estado limpio si el working tree no lo esta: el diff de refactorizacion debe ser legible por separado.

## 2. Dividir en lotes

Un lote = una categoria del catalogo en un archivo (o un grupo cohesionado de archivos).

- Tamano maximo recomendado: ~100 lineas de diff o 3 responsabilidades.
- Si el lote crece: partirlo (por ejemplo, solo firmas primero, despues cuerpos).
- **Verificar tras cada lote, nunca al final de todo.**

```
lote → pytest → verde → commit corto → siguiente lote
              → rojo → revertir lote → partirlo mas pequeno
```

## 3. Revertir un lote fallido

```bash
git checkout -- <archivo>      # descartar solo lo tocado en el lote
git diff                       # confirmar que no quedan restos
$TEST                          # volver al verde
```

Reintentar con un cambio mas pequeno. Un lote revertido no se "arregla" ensuciando el diff.

## 4. Verificacion por categoria

| Categoria | Verificacion extra |
|-----------|--------------------|
| f-strings / imports | Grep de ocurrencias restantes = 0 en el alcance |
| Type hints | `python -c "import <modulo>"` + ejecutar tests del modulo |
| Excepciones | Tests de los flujos de error afectados |
| Dataclasses / DI | Suite completa (unit + integration) |
| Globales | grep de `global` en call sites = 0 y suite completa |

Comandos utiles (adaptar al proyecto):

```bash
python -m py_compile <archivo.py>    # sintaxis rapida
$TEST                                # gate obligatorio
python -m mypy .                     # solo si mypy esta configurado en el proyecto
```

## 5. Comportamiento inmutable

- Mismos mensajes en stdout/UI (el lote de estilo no cambia textos).
- Mismos retornos: `None`, listas vacias o las mismas excepciones en los mismos casos.
- Mismas claves de JSON/dict en la frontera de red y archivos.
- Firmas publicas: no renombrar; si es imprescindible, actualizar todos los call sites en el mismo lote:

```bash
grep -rn "nombre_viejo" --include="*.py" .
```

- Preservar el logger y el nivel de log existentes (`logging.getLogger(__name__)` o equivalente).

## 6. Checkpoint final

```bash
$TEST
git diff --stat
```

Reportar con `report-template.md`: baseline, practicas eliminadas (`archivo:linea`), archivos modificados, resultado final de tests y pendientes.

## 7. Que NO es refactorizacion

- Cambiar una respuesta de API, un flujo de UI o un mensaje al usuario.
- Anadir una feature "de paso".
- Reescribir un modulo entero sin tests intermedios.
- Ignorar un test que falla porque "ya estaba mal".
- Arreglar estilo de archivos fuera del alcance acordado.

Si el cambio exige alterar comportamiento: **parar y preguntar al usuario** antes de continuar.
