import re
from typing import Any, Optional

from exceptions import InvalidInputError
from logger import get_logger

_logger = get_logger(__name__)

MAX_SEARCH_LENGTH = 200
MIN_SEARCH_LENGTH = 1
MAX_TITLE_LENGTH = 500
MAX_NAME_LENGTH = 200


def validate_menu_option(option: str, valid_options: list) -> str:
    if not option:
        raise InvalidInputError("menu_option", option, "La opcion no puede estar vacia")
    
    if option not in valid_options:
        raise InvalidInputError("menu_option", option, f"Opcion no valida. Opciones permitidas: {valid_options}")
    
    return option


def validate_search_query(query: str, field_name: str = "busqueda") -> str:
    if not query or not query.strip():
        raise InvalidInputError(field_name, query, "El campo de busqueda no puede estar vacio")
    
    query = query.strip()
    
    if len(query) < MIN_SEARCH_LENGTH:
        raise InvalidInputError(field_name, query, f"La busqueda debe tener al menos {MIN_SEARCH_LENGTH} caracter")
    
    if len(query) > MAX_SEARCH_LENGTH:
        raise InvalidInputError(field_name, query, f"La busqueda no puede exceder {MAX_SEARCH_LENGTH} caracteres")
    
    if not re.match(r"^[\w\s\-\.\,\&':!\(\)\[\]/\?]+$", query):
        raise InvalidInputError(field_name, query, "La busqueda contiene caracteres no permitidos")
    
    return query


def validate_movie_title(title: str) -> str:
    return validate_search_query(title, "titulo_pelicula")


def validate_actor_name(name: str) -> str:
    return validate_search_query(name, "nombre_actor")


def validate_series_name(name: str) -> str:
    return validate_search_query(name, "nombre_serie")


def validate_year(year: str) -> int:
    if not year or not year.strip():
        raise InvalidInputError("year", year, "El anio no puede estar vacio")
    
    year = year.strip()
    
    if not year.isdigit():
        raise InvalidInputError("year", year, "El anio debe ser un numero")
    
    year_int = int(year)
    
    if year_int < 1888 or year_int > 2100:
        raise InvalidInputError("year", year, "El anio debe estar entre 1888 y 2100")
    
    return year_int


def validate_timeout(timeout: str) -> int:
    if not timeout or not timeout.strip():
        raise InvalidInputError("timeout", timeout, "El timeout no puede estar vacio")
    
    timeout = timeout.strip()
    
    if not timeout.isdigit():
        raise InvalidInputError("timeout", timeout, "El timeout debe ser un numero")
    
    timeout_int = int(timeout)
    
    if timeout_int < 1 or timeout_int > 300:
        raise InvalidInputError("timeout", timeout, "El timeout debe estar entre 1 y 300 segundos")
    
    return timeout_int


def validate_api_url(url: str) -> str:
    if not url or not url.strip():
        raise InvalidInputError("api_url", url, "La URL de la API no puede estar vacia")
    
    url = url.strip()
    
    if not url.startswith(('http://', 'https://')):
        raise InvalidInputError("api_url", url, "La URL debe comenzar con http:// o https://")
    
    if len(url) > 500:
        raise InvalidInputError("api_url", url, "La URL no puede exceder 500 caracteres")
    
    return url


def validate_filename(filename: str) -> str:
    if not filename or not filename.strip():
        raise InvalidInputError("filename", filename, "El nombre del archivo no puede estar vacio")
    
    filename = filename.strip()
    
    if len(filename) > 255:
        raise InvalidInputError("filename", filename, "El nombre del archivo no puede exceder 255 caracteres")
    
    if not re.match(r'^[\w\-\.\s]+$', filename):
        raise InvalidInputError("filename", filename, "El nombre del archivo contiene caracteres no permitidos")
    
    dangerous_patterns = ['..', '/', '\\', '<', '>', ':', '|', '?', '*']
    for pattern in dangerous_patterns:
        if pattern in filename:
            raise InvalidInputError("filename", filename, f"El nombre del archivo no puede contener: {pattern}")
    
    return filename


def validate_positive_integer(value: str, field_name: str = "numero") -> int:
    if not value or not value.strip():
        raise InvalidInputError(field_name, value, f"{field_name} no puede estar vacio")
    
    value = value.strip()
    
    if not value.isdigit():
        raise InvalidInputError(field_name, value, f"{field_name} debe ser un numero entero")
    
    value_int = int(value)
    
    if value_int < 0:
        raise InvalidInputError(field_name, value, f"{field_name} debe ser un numero positivo")
    
    return value_int


def validate_non_empty_string(value: str, field_name: str = "campo") -> str:
    if not value or not value.strip():
        raise InvalidInputError(field_name, value, f"{field_name} no puede estar vacio")
    
    return value.strip()


def sanitize_input(value: str) -> str:
    if not value:
        return ""
    
    value = value.strip()
    
    value = re.sub(r'[<>"\']', '', value)
    
    return value
