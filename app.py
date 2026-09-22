import json
import os
import random
import sys
import time
from typing import Any, Dict, List, Optional

import requests

from constants import API_KEYS, API_URLS, MESSAGES, NA_VALUE, POPULAR_MOVIES
from exceptions import BaseAppError, InvalidInputError
from logger import get_logger
from validators import validate_movie_title, validate_actor_name, validate_series_name, sanitize_input

_logger = get_logger(__name__)


API_KEY: str = API_KEYS["omdb"]
OMDB_BASE_URL: str = API_URLS["omdb"]
TVMAZE_BASE_URL: str = API_URLS["tvmaze"]
CACHE: Dict[str, Any] = {}
USUARIO_ACTUAL: Optional[str] = None
PELICULAS_FAVORITAS: List[Dict[str, Any]] = []
HISTORIAL: List[str] = []


def print_sep() -> None:
    print("=" * 50)


def print_header(text: str) -> None:
    print_sep()
    print(text.upper())
    print_sep()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def delay(seconds: float) -> None:
    time.sleep(seconds)


def buscar_pelicula_omdb(titulo: str) -> Optional[Dict[str, Any]]:
    global CACHE
    titulo_validado = validate_movie_title(titulo)
    titulo_sanitizado = sanitize_input(titulo_validado)
    
    if titulo_sanitizado in CACHE:
        _logger.debug("Usando cache para: %s", titulo_sanitizado)
        return CACHE[titulo_sanitizado]

    params = {"t": titulo_sanitizado, "apikey": API_KEY}
    response = requests.get(OMDB_BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        CACHE[titulo_sanitizado] = data
        return data
    return None


def buscar_series_tvmaze(nombre: str) -> List[Dict[str, Any]]:
    global CACHE
    nombre_validado = validate_series_name(nombre)
    nombre_sanitizado = sanitize_input(nombre_validado)
    cache_key = f"series_{nombre_sanitizado}"
    if cache_key in CACHE:
        _logger.debug("Usando cache de series para: %s", nombre_sanitizado)
        return CACHE[cache_key]

    params = {"q": nombre_sanitizado}
    response = requests.get(f"{TVMAZE_BASE_URL}/search/shows", params=params)
    data = response.json()

    CACHE[cache_key] = data
    return data


def obtener_detalles_serie_tvmaze(id_serie: int) -> Dict[str, Any]:
    url = f"{TVMAZE_BASE_URL}/shows/{id_serie}"
    response = requests.get(url)
    return response.json()


def buscar_peliculas_por_actor(nombre_actor: str) -> List[Dict[str, Any]]:
    actor_validado = validate_actor_name(nombre_actor)
    actor_sanitizado = sanitize_input(actor_validado)
    params = {"s": actor_sanitizado, "type": "movie", "apikey": API_KEY}
    response = requests.get(OMDB_BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data.get("Search", [])
    return []


def obtener_peliculas_populares() -> List[Dict[str, Any]]:
    return list(POPULAR_MOVIES)


def mostrar_pelicula(pelicula: Optional[Dict[str, Any]]) -> None:
    print_sep()
    if pelicula is None:
        print(MESSAGES["not_found"])
        return

    print(f"Título: {pelicula.get('Title', NA_VALUE)}")
    print(f"Año: {pelicula.get('Year', NA_VALUE)}")
    print(f"Rating: {pelicula.get('imdbRating', NA_VALUE)}")
    print(f"Género: {pelicula.get('Genre', NA_VALUE)}")
    print(f"Director: {pelicula.get('Director', NA_VALUE)}")
    print(f"Trama: {pelicula.get('Plot', NA_VALUE)}")
    print_sep()


def mostrar_serie(serie: Dict[str, Any]) -> None:
    print_sep()
    show = serie.get("show", serie)
    print(f"Nombre: {show.get('name', NA_VALUE)}")
    print(f"Idioma: {show.get('language', NA_VALUE)}")
    print(f"Géneros: {show.get('genres', [])}")
    print(f"Rating: {show.get('rating', {}).get('average', NA_VALUE)}")
    print(f"Estado: {show.get('status', NA_VALUE)}")
    print_sep()


def mostrar_lista_peliculas(peliculas: List[Dict[str, Any]]) -> None:
    for i, pelicula in enumerate(peliculas):
        titulo = pelicula.get("titulo", pelicula.get("Title", "Sin título"))
        print(f"{i + 1}. {titulo}")


def menu_principal() -> None:
    while True:
        clear_screen()
        print_header("SISTEMA DE PELÍCULAS")
        print("1. Buscar película por título")
        print("2. Buscar por actor")
        print("3. Buscar series")
        print("4. Ver películas populares")
        print("5. Ver favoritos")
        print("6. Ver historial")
        print("7. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            funcion_buscar_pelicula()
        elif opcion == "2":
            funcion_buscar_actor()
        elif opcion == "3":
            funcion_buscar_series()
        elif opcion == "4":
            funcion_peliculas_populares()
        elif opcion == "5":
            funcion_ver_favoritos()
        elif opcion == "6":
            funcion_ver_historial()
        elif opcion == "7":
            print(MESSAGES["goodbye"])
            break
        else:
            print(MESSAGES["invalid_option"])
            delay(1)


def funcion_buscar_pelicula() -> None:
    titulo = input("Ingrese el título de la película: ")
    print(MESSAGES["searching"])
    delay(1)

    pelicula = buscar_pelicula_omdb(titulo)
    mostrar_pelicula(pelicula)

    if pelicula:
        HISTORIAL.append(pelicula.get("Title"))
        opcion = input("\n¿Agregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            PELICULAS_FAVORITAS.append(pelicula)
            print(MESSAGES["added_favorite"])

    input(MESSAGES["press_enter"])


def funcion_buscar_actor() -> None:
    actor = input("Ingrese el nombre del actor: ")
    print(MESSAGES["searching_actor"])

    peliculas = buscar_peliculas_por_actor(actor)

    if len(peliculas) > 0:
        for i, pelicula in enumerate(peliculas):
            print(f"{i + 1}. {pelicula.get('Title', '')} ({pelicula.get('Year', '')})")

        opcion = input("\nSeleccione una película para ver detalles (0 para volver): ")
        if opcion.isdigit() and int(opcion) > 0:
            indice = int(opcion) - 1
            if indice < len(peliculas):
                detalles = buscar_pelicula_omdb(peliculas[indice].get("Title"))
                mostrar_pelicula(detalles)
    else:
        print(MESSAGES["no_movies_found"])

    input(MESSAGES["press_enter"])


def funcion_buscar_series() -> None:
    nombre = input("Ingrese el nombre de la serie: ")
    print(MESSAGES["searching_series"])

    series = buscar_series_tvmaze(nombre)

    if len(series) > 0:
        for i, serie in enumerate(series):
            show = serie.get("show", {})
            print(f"{i + 1}. {show.get('name', '')} ({show.get('status', '')})")

        opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
        if opcion.isdigit() and int(opcion) > 0:
            indice = int(opcion) - 1
            if indice < len(series):
                id_serie = series[indice].get("show", {}).get("id")
                detalles = obtener_detalles_serie_tvmaze(id_serie)
                mostrar_serie(detalles)
    else:
        print(MESSAGES["no_series_found"])

    input(MESSAGES["press_enter"])


def funcion_peliculas_populares() -> None:
    print_header("PELÍCULAS POPULARES")
    peliculas = obtener_peliculas_populares()
    mostrar_lista_peliculas(peliculas)
    input(MESSAGES["press_enter"])


def funcion_ver_favoritos() -> None:
    print_header("MIS FAVORITOS")
    if len(PELICULAS_FAVORITAS) > 0:
        for i, pelicula in enumerate(PELICULAS_FAVORITAS):
            print(f"{i + 1}. {pelicula.get('Title', '')}")
    else:
        print(MESSAGES["no_favorites"])
    input(MESSAGES["press_enter"])


def funcion_ver_historial() -> None:
    print_header("HISTORIAL DE BÚSQUEDAS")
    if len(HISTORIAL) > 0:
        for i, item in enumerate(HISTORIAL):
            print(f"{i + 1}. {item}")
    else:
        print(MESSAGES["no_history"])
    input(MESSAGES["press_enter"])


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        _logger.info("Programa interrumpido por el usuario")
        sys.exit(0)
    except BaseAppError as e:
        _logger.error("Error de aplicacion: %s", e)
        sys.exit(1)
    except (OSError, ValueError, KeyError) as e:
        _logger.exception("Error inesperado: %s", e)
        sys.exit(1)
