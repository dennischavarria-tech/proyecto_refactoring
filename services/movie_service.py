import json
from typing import Any, Dict, List, Optional

from api.omdb import OmdbApiClient
from logger import get_logger
from models.movie import Movie

_logger = get_logger(__name__)


class MovieService:
    def __init__(self, api_client: OmdbApiClient) -> None:
        self._api = api_client
        self._cache: Dict[str, Movie] = {}
        self._favorites: List[Movie] = []
        self._history: List[Dict[str, str]] = []

    def buscar_pelicula(self, titulo: str) -> Optional[Movie]:
        if titulo in self._cache:
            return self._cache[titulo]

        movie = self._api.buscar_pelicula(titulo)
        if movie:
            self._cache[titulo] = movie
        return movie

    def buscar_peliculas_por_actor(self, actor: str) -> List[Movie]:
        return self._api.buscar_peliculas_por_actor(actor)

    def obtener_peliculas_populares(self) -> List[Movie]:
        return self._api.obtener_peliculas_populares()

    def buscar_peliculas_por_genero(self, genero: str) -> List[Movie]:
        return self._api.buscar_peliculas_por_genero(genero)

    def agregar_a_favoritas(self, movie: Movie) -> bool:
        existe = any(m.title == movie.title for m in self._favorites)
        if not existe:
            self._favorites.append(movie)
            return True
        return False

    def eliminar_de_favoritas(self, titulo: str) -> bool:
        for i, movie in enumerate(self._favorites):
            if movie.title == titulo:
                self._favorites.pop(i)
                return True
        return False

    def obtener_favoritas(self) -> List[Movie]:
        return list(self._favorites)

    def agregar_al_historial(self, movie: Movie) -> None:
        self._history.append({
            "titulo": movie.title,
            "fecha": "hoy",
        })

    def limpiar_historial(self) -> None:
        self._history = []

    def obtener_historial(self) -> List[Dict[str, str]]:
        return list(self._history)

    def obtener_estadisticas(self) -> Dict[str, int]:
        return {
            "total_favoritas": len(self._favorites),
            "total_historial": len(self._history),
        }

    def exportar_a_json(self, nombre_archivo: str) -> None:
        data = {
            "favoritas": [m.to_dict() for m in self._favorites],
            "historial": self._history,
            "estadisticas": self.obtener_estadisticas(),
        }

        with open(nombre_archivo, "w") as f:
            json.dump(data, f)

        _logger.info("Exportado a %s", nombre_archivo)

    def importar_de_json(self, nombre_archivo: str) -> None:
        with open(nombre_archivo, "r") as f:
            data = json.load(f)

        self._favorites = [
            Movie.from_omdb_dict(m) for m in data.get("favoritas", [])
        ]
        self._favorites = [m for m in self._favorites if m is not None]
        self._history = data.get("historial", [])

        _logger.info("Importado desde %s", nombre_archivo)
