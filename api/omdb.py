from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests

from constants import API_KEYS, API_URLS, GENRE_MOVIES, POPULAR_MOVIES
from exceptions import APIConnectionError, InvalidInputError
from logger import get_logger
from models.movie import Movie
from validators import validate_movie_title, validate_actor_name, sanitize_input

_logger = get_logger(__name__)


class OmdbApiClient:
    def __init__(self, timeout: int = 30, debug: bool = False) -> None:
        self._base_url: str = API_URLS["omdb"]
        self._api_key: str = API_KEYS["omdb"]
        self._timeout: int = timeout
        self._debug: bool = debug

    def _validate_api_key(self) -> None:
        if not self._api_key:
            _logger.error("OMDB API key no configurada")
            raise InvalidInputError("api_key", "", "La API key de OMDB no esta configurada. Configure OMDB_API_KEY en .env")

    def _make_request(self, url: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        _logger.debug("Haciendo request a %s", url)

        try:
            response = requests.get(url, params=params, timeout=self._timeout)
        except requests.RequestException as e:
            _logger.error("Error de conexion: %s", e)
            raise APIConnectionError(url=url, details=str(e)) from e

        _logger.debug("Status code: %s", response.status_code)

        if response.status_code != 200:
            _logger.warning("Respuesta no exitosa: HTTP %s de %s", response.status_code, url)
            raise APIConnectionError(url=url, status_code=response.status_code)

        return response.json()

    def _obtener_detalle(self, titulo: str) -> Optional[Movie]:
        self._validate_api_key()
        params = {"t": titulo, "apikey": self._api_key}
        data = self._make_request(self._base_url, params)
        return Movie.from_omdb_dict(data)

    def buscar_pelicula(self, titulo: str) -> Optional[Movie]:
        titulo_validado = validate_movie_title(titulo)
        titulo_sanitizado = sanitize_input(titulo_validado)
        return self._obtener_detalle(titulo_sanitizado)

    def buscar_peliculas_por_actor(self, actor: str) -> List[Movie]:
        actor_validado = validate_actor_name(actor)
        actor_sanitizado = sanitize_input(actor_validado)
        self._validate_api_key()

        params = {"s": actor_sanitizado, "type": "movie", "apikey": self._api_key}
        data = self._make_request(self._base_url, params)

        if data.get("Response") != "True":
            return []

        search_results = data.get("Search", [])
        movies: List[Movie] = []
        for item in search_results:
            titulo = item.get("Title", "")
            if not titulo:
                continue
            movie = self._obtener_detalle(titulo)
            if movie:
                movies.append(movie)
        return movies

    def obtener_peliculas_populares(self) -> List[Movie]:
        return [Movie.from_local_dict(m) for m in POPULAR_MOVIES]

    def buscar_peliculas_por_genero(self, genero: str) -> List[Movie]:
        genero_lower = genero.lower()
        if genero_lower == "accion":
            results = GENRE_MOVIES["accion"]
        elif genero_lower == "comedia":
            results = GENRE_MOVIES["comedia"]
        else:
            results = GENRE_MOVIES["accion"] + GENRE_MOVIES["comedia"]
        return [Movie.from_local_dict(m) for m in results]
