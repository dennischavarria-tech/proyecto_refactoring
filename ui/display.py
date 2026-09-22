import os
import time
from typing import List, Optional

from constants import MESSAGES, NA_VALUE
from models.movie import Movie
from models.series import Series


class Display:
    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def print_separator(self) -> None:
        print("=" * 60)

    def print_header(self, text: str) -> None:
        self.print_separator()
        print(text.upper().center(60))
        self.print_separator()

    def delay(self, seconds: float) -> None:
        time.sleep(seconds)

    def mostrar_pelicula(self, movie: Optional[Movie]) -> None:
        self.print_separator()
        if movie is None:
            print(MESSAGES["not_found"])
            return

        print(f"Título: {movie.title}")
        print(f"Año: {movie.year}")
        print(f"Rating IMDB: {movie.imdb_rating}")
        print(f"Género: {movie.genre}")
        print(f"Director: {movie.director}")
        print(f"Actores: {movie.actors}")
        print(f"Trama: {movie.plot}")
        print(f"País: {movie.country}")
        print(f"Premios: {movie.awards}")
        self.print_separator()

    def mostrar_serie(self, series: Series) -> None:
        self.print_separator()
        print(f"Nombre: {series.name}")
        print(f"Idioma: {series.language}")
        print(f"Géneros: {series.genres}")
        print(f"Rating: {series.rating if series.rating is not None else NA_VALUE}")
        print(f"Estado: {series.status}")
        print(f"Estreno: {series.premiered}")
        print(f"Final: {series.ended}")
        print(f"Episodios: {series.runtime if series.runtime is not None else NA_VALUE}")
        summary = series.summary
        if len(summary) > 200:
            summary = summary[:200] + "..."
        print(f"Resumen: {summary}")
        self.print_separator()

    def mostrar_lista_peliculas(self, movies: List[Movie]) -> None:
        for i, movie in enumerate(movies):
            print(f"{i + 1}. {movie.title} ({movie.year}) - {movie.imdb_rating}")

    def mostrar_lista_series(self, series_list: List[Series]) -> None:
        for i, series in enumerate(series_list):
            print(f"{i + 1}. {series.name} ({series.status})")

    def mostrar_favoritas(self, movies: List[Movie]) -> None:
        for i, movie in enumerate(movies):
            print(f"{i + 1}. {movie.title}")

    def mostrar_historial(self, items: List[dict]) -> None:
        for i, item in enumerate(items):
            print(f"{i + 1}. {item['titulo']}")
