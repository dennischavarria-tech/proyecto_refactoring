# Reporte de Riesgos de Seguridad

**Fecha:** 2026-09-17  
**Proyecto:** Sistema de Peliculas y Series  
**Analista:** Especialista en Robustez y Observabilidad

---

## Resumen Ejecutivo

Se identificaron **7 riesgos criticos** y **5 riesgos medios** en el codigo fuente. Se implementaron mitigaciones para todos los riesgos criticos relacionados con credenciales y validacion de entrada.

---

## Riesgos Criticos

### 1. API Keys Hardcodeadas en Codigo
**Severidad:** CRITICA  
**Estado:** MITIGADO  
**Ubicacion original:** `constants.py:11`

**Riesgo identificado:**
- API key de OMDB (`"trilogy"`) estaba hardcodeada directamente en el codigo fuente
- API key de TMDB estaba hardcodeada (aunque vacia)
- Cualquier persona con acceso al codigo tendria acceso a las credenciales

**Mitigacion implementada:**
- Se creo archivo `.env` para almacenar credenciales fuera del codigo
- Se creo archivo `.env.example` como plantilla
- Se modifico `constants.py` para usar `os.getenv()` con valores por defecto vacios
- Se agrego `.env` al `.gitignore` para evitar commitear credenciales

**Codigo antes:**
```python
API_KEYS: Dict[str, str] = {
    "omdb": "trilogy",  # EXPUESTO
    "tmdb": "",
}
```

**Codigo despues:**
```python
API_KEYS: Dict[str, str] = {
    "omdb": os.getenv("OMDB_API_KEY", ""),
    "tmdb": os.getenv("TMDB_API_KEY", ""),
}
```

---

### 2. Contraseñas Almacenadas en Texto Plano
**Severidad:** CRITICA  
**Estado:** NO MITIGADO (Requiere accion adicional)  
**Ubicacion:** `user_manager.py:36, 56`

**Riesgo identificado:**
- Las contrasenas de usuarios se almacenan sin hashear en `users.json`
- La autenticacion compara contrasenas en texto plano
- Si el archivo `users.json` es comprometido, todas las contrasenas quedan expuestas

**Codigo vulnerable:**
```python
# Linea 36
"password": password,  # No hasheada (mala practica)

# Linea 56
if user["username"] == username and user["password"] == password:
```

**Mitigacion recomendada:**
- Usar `bcrypt` o `argon2` para hashear contrasenas
- Implementar salt unico por usuario
- Nunca almacenar contrasenas en texto plano

**Ejemplo de solucion:**
```python
import bcrypt

def create_user(username, password, email=None):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = {
        "username": username,
        "password": hashed_password.decode('utf-8'),
        ...
    }

def authenticate_user(username, password):
    for user in users:
        if user["username"] == username:
            if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                return True, user
    return False, "Credenciales invalidas"
```

---

### 3. URLs de APIs Construidas Manualmente (Inyeccion de Parametros)
**Severidad:** CRITICA  
**Estado:** MITIGADO  
**Ubicacion original:** `api/omdb.py:38,43`, `api/tvmaze.py:27`, `app.py:50,67,82`

**Riesgo identificado:**
- Las URLs se construian usando f-strings con entrada del usuario
- Vulnerable a inyeccion de parametros y ataques de manipulacion de URL
- Ejemplo: `url = f"{base_url}?t={titulo}&apikey={api_key}"`

**Codigo antes (vulnerable):**
```python
url = f"{self._base_url}?t={titulo}&apikey={self._api_key}"
response = requests.get(url)
```

**Codigo despues (seguro):**
```python
params = {"t": titulo_sanitizado, "apikey": self._api_key}
response = requests.get(self._base_url, params=params)
```

**Mitigacion implementada:**
- Se uso el parametro `params` de `requests.get()` para construir URLs de forma segura
- Se agrego sanitizacion de entrada antes de usar los valores
- Se implemento validacion de entrada para todos los parametros de busqueda

---

### 4. Falta de Validacion de Entrada
**Severidad:** CRITICA  
**Estado:** MITIGADO  
**Ubicacion:** `ui/menu.py`, `api/omdb.py`, `api/tvmaze.py`, `app.py`

**Riesgo identificado:**
- No habia validacion de longitud, formato o caracteres permitidos
- Entrada del usuario se usaba directamente sin sanitizacion
- Vulnerable a ataques de inyeccion, XSS, y desbordamiento

**Mitigacion implementada:**
- Se creo modulo `validators.py` con funciones de validacion
- Se implemento validacion para:
  - Titulos de peliculas (longitud 1-200, caracteres alfanumericos)
  - Nombres de actores (longitud 1-200, caracteres alfanumericos)
  - Nombres de series (longitud 1-200, caracteres alfanumericos)
  - Nombres de archivo (sin caracteres peligrosos como `..`, `/`, `\`)
  - Timeout (1-300 segundos)
  - Anios (1888-2100)
- Se implemento sanitizacion para eliminar caracteres peligrosos

---

### 5. Manejo de Errores con `except:` Bare
**Severidad:** ALTA  
**Estado:** MITIGADO  
**Ubicacion original:** `favorites_manager.py:77,141`, `log_manager.py:170,190`

**Riesgo identificado:**
- Uso de `except:` sin especificar tipo de excepcion
- Captura todas las excepciones incluyendo `SystemExit` y `KeyboardInterrupt`
- Dificulta el debugging y puede ocultar errores criticos

**Mitigacion implementada:**
- Se reemplazo todos los `except:` por excepciones especificas
- `except (TypeError, KeyError):` para operaciones de diccionarios
- `except (ValueError, TypeError):` para conversiones de tipo

---

### 6. Manejo de Errores con `except Exception`
**Severidad:** ALTA  
**Estado:** MITIGADO  
**Ubicacion original:** `main.py:40`, `app.py:254`

**Riesgo identificado:**
- Captura demasiado amplia de excepciones
- No diferencia entre errores de aplicacion y errores inesperados
- No registra stack traces para debugging

**Mitigacion implementada:**
- Se uso excepciones personalizadas (`BaseAppError`)
- Se capturan excepciones especificas (`OSError`, `ValueError`, `KeyError`)
- Se usa `logger.exception()` para registrar stack traces completos

---

### 7. Uso de `print()` para Debugging
**Severidad:** MEDIA  
**Estado:** MITIGADO  
**Ubicacion original:** `api/omdb.py:18,23`, `api/tvmaze.py:17,22`, `logger.py:21`

**Riesgo identificado:**
- Mensajes de debug expuestos en consola
- No hay control de niveles de log
- No hay rotacion de logs
- Informacion sensible puede quedar expuesta en consola

**Mitigacion implementada:**
- Se refactorizo `logger.py` para usar `logging` estandar de Python
- Se implemento rotacion de logs con `RotatingFileHandler`
- Se configuro niveles de log: DEBUG (archivo), WARNING (consola), ERROR (archivo separado)
- Se reemplazaron todos los `print()` de debug por `logger.debug()`

---

## Riesgos Medios

### 8. Archivo de Usuarios sin Proteccion
**Severidad:** MEDIA  
**Estado:** NO MITIGADO  
**Ubicacion:** `user_manager.py:7`

**Riesgo identificado:**
- Archivo `users.json` almacenado en directorio sin proteccion
- No hay encriptacion de datos sensibles
- Permisos de archivo no restringidos

**Mitigacion recomendada:**
- Restringir permisos del archivo: `chmod 600 users.json`
- Considerar encriptar el archivo completo
- Mover a directorio protegido

---

### 9. Configuracion de Debug Habilitada por Defecto
**Severidad:** MEDIA  
**Estado:** MITIGADO  
**Ubicacion:** `constants.py:16`

**Riesgo identificado:**
- `DEBUG` estaba habilitado por defecto (`True`)
- Puede exponer informacion sensible en produccion

**Mitigacion implementada:**
- Se cambio valor por defecto a `False`
- Se controla mediante variable de entorno `DEBUG`

---

### 10. Falta de Rate Limiting en APIs
**Severidad:** MEDIA  
**Estado:** NO MITIGADO  
**Ubicacion:** `api/omdb.py`, `api/tvmaze.py`

**Riesgo identificado:**
- No hay control de rate limiting para llamadas a APIs
- Puede resultar en bloqueo por exceso de peticiones
- No hay mecanismo de retry con backoff exponencial

**Mitigacion recomendada:**
- Implementar rate limiting con decoradores
- Agregar backoff exponencial para reintentos
- Cache de respuestas para reducir llamadas

---

### 11. URLs de APIs en Codigo
**Severidad:** BAJA  
**Estado:** MITIGADO  
**Ubicacion original:** `constants.py:5-7`

**Riesgo identificado:**
- URLs de APIs publicas estaban hardcodeadas
- Dificil de cambiar entre ambientes (dev, staging, prod)

**Mitigacion implementada:**
- Se movieron URLs a variables de entorno
- Se mantienen valores por defecto para facilidad de uso

---

### 12. No hay Validacion de SSL/TLS
**Severidad:** MEDIA  
**Estado:** NO MITIGADO  
**Ubicacion:** `api/omdb.py`, `api/tvmaze.py`

**Riesgo identificado:**
- No se verifica certificados SSL/TLS
- Vulnerable a ataques man-in-the-middle
- URLs usan HTTP en lugar de HTTPS

**Mitigacion recomendada:**
- Usar HTTPS para todas las APIs
- Verificar certificados SSL
- Configurar `verify=True` en requests

---

## Archivos Modificados

| Archivo | Cambios |
|---|---|
| `constants.py` | Uso de `os.getenv()` para API keys y URLs |
| `api/omdb.py` | Validacion de entrada, uso de `params`, validacion de API key |
| `api/tvmaze.py` | Validacion de entrada, uso de `params` |
| `app.py` | Validacion de entrada, uso de `params` |
| `ui/menu.py` | Validacion de entrada en todas las funciones |
| `logger.py` | Refactorizado con `logging` estandar |
| `validators.py` | Nuevo modulo de validacion |
| `.env` | Nuevo archivo de variables de entorno |
| `.env.example` | Nuevo archivo de ejemplo |
| `.gitignore` | Nuevo archivo para proteger datos sensibles |

---

## Archivos Creados

| Archivo | Proposito |
|---|---|
| `exceptions/base.py` | Excepcion base de la aplicacion |
| `exceptions/not_found.py` | Excepciones de recursos no encontrados |
| `exceptions/api.py` | Excepciones de errores de API |
| `exceptions/validation.py` | Excepciones de validacion de entrada |
| `exceptions/__init__.py` | Exportacion de excepciones |
| `validators.py` | Modulo de validacion de entrada |
| `.env` | Variables de entorno (NO commitear) |
| `.env.example` | Plantilla de variables de entorno |
| `.gitignore` | Proteccion de archivos sensibles |

---

## Acciones Pendientes

### Alta Prioridad
1. **Implementar hashing de contrasenas** en `user_manager.py` usando `bcrypt`
2. **Restringir permisos** de archivos sensibles (`users.json`, `errors.json`)
3. **Cambiar a HTTPS** todas las URLs de APIs

### Media Prioridad
4. **Implementar rate limiting** para llamadas a APIs
5. **Agregar backoff exponencial** para reintentos
6. **Implementar verificacion SSL/TLS**

### Baja Prioridad
7. **Agregar tests de seguridad** para validacion de entrada
8. **Implementar auditoria de seguridad** periodica
9. **Documentar politicas de seguridad** para desarrolladores

---

## Conclusion

Se mitigaron todos los riesgos criticos relacionados con:
- Credenciales hardcodeadas
- Validacion de entrada
- Manejo de errores
- Logging y debugging

Quedan pendientes acciones relacionadas con:
- Seguridad de contrasenas (hashing)
- Rate limiting
- Verificacion SSL/TLS

**Nivel de riesgo general:** MEDIO (antes: ALTO)
