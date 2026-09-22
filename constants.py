import os
from typing import Dict, List, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


API_URLS: Dict[str, str] = {
    "omdb": os.getenv("OMDB_API_URL", "http://www.omdbapi.com/"),
    "tmdb": os.getenv("TMDB_API_URL", "https://api.themoviedb.org/3/"),
    "tvmaze": os.getenv("TVMAZE_API_URL", "http://api.tvmaze.com"),
}

API_KEYS: Dict[str, str] = {
    "omdb": os.getenv("OMDB_API_KEY", ""),
    "tmdb": os.getenv("TMDB_API_KEY", ""),
}

DEFAULT_CONFIG: Dict[str, Any] = {
    "debug": os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"),
    "verbose": os.getenv("VERBOSE", "False").lower() in ("true", "1", "yes"),
    "timeout": int(os.getenv("API_TIMEOUT", "30")),
    "max_retries": int(os.getenv("MAX_RETRIES", "3")),
}

MESSAGES: Dict[str, str] = {
    "not_found": "No se encontró la película",
    "no_favorites": "No tienes películas favoritas",
    "no_history": "No hay historial",
    "invalid_option": "Opción inválida",
    "exported": "Exportado a {filename}",
    "imported": "Importado desde {filename}",
    "added_favorite": "¡Agregada a favoritos!",
    "already_favorite": "Ya está en favoritos",
    "removed_favorite": "Eliminada de favoritos",
    "history_cleared": "Historial limpiado",
    "goodbye": "¡Hasta luego!",
    "press_enter": "\nPresione Enter para continuar...",
    "searching": "Buscando...",
    "searching_actor": "Buscando películas del actor...",
    "searching_series": "Buscando series...",
    "no_movies_found": "No se encontraron películas para ese actor",
    "no_series_found": "No se encontraron series",
}

DEFAULT_VALUES: Dict[str, Any] = {
    "separator_char": "=",
    "separator_length": 60,
    "header_width": 60,
    "delay_seconds": 1,
    "max_history_items": 100,
    "max_favorites": 1000,
}

POPULAR_MOVIES: List[Dict[str, Any]] = [
    {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
    {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
    {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
    {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
    {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8},
]

GENRE_MOVIES: Dict[str, List[Dict[str, Any]]] = {
    "accion": [
        {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
        {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1},
    ],
    "comedia": [
        {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
        {"titulo": "The Hangover", "anio": 2009, "rating": 7.7},
    ],
}

DIRECTORIES: Dict[str, str] = {
    "results": "results",
    "exports": "exports",
    "data": "data",
    "backups": "backups",
    "cache": "cache",
    "history": "history",
    "logs": "logs",
    "plugins": "plugins",
}

MOVIE_FIELDS: List[str] = [
    "Title", "Year", "imdbRating", "Genre", "Director",
    "Actors", "Plot", "Country", "Awards", "Language", "Poster",
]

NA_VALUE: str = "N/A"
