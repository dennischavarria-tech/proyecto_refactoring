from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Movie:
    title: str
    year: str
    imdb_rating: str
    genre: str
    director: str
    actors: str
    plot: str
    country: str
    awards: str
    language: str = ""
    poster: str = ""

    @classmethod
    def from_omdb_dict(cls, data: Dict[str, Any]) -> Optional["Movie"]:
        if data.get("Response") != "True":
            return None

        return cls(
            title=data.get("Title", ""),
            year=data.get("Year", ""),
            imdb_rating=data.get("imdbRating", ""),
            genre=data.get("Genre", ""),
            director=data.get("Director", ""),
            actors=data.get("Actors", ""),
            plot=data.get("Plot", ""),
            country=data.get("Country", ""),
            awards=data.get("Awards", ""),
            language=data.get("Language", ""),
            poster=data.get("Poster", ""),
        )

    @classmethod
    def from_local_dict(cls, data: Dict[str, Any]) -> "Movie":
        return cls(
            title=data.get("titulo", data.get("Title", "")),
            year=str(data.get("anio", data.get("Year", ""))),
            imdb_rating=str(data.get("rating", data.get("imdbRating", ""))),
            genre=data.get("genero", data.get("Genre", "")),
            director=data.get("director", data.get("Director", "")),
            actors=data.get("actores", data.get("Actors", "")),
            plot=data.get("trama", data.get("Plot", "")),
            country=data.get("pais", data.get("Country", "")),
            awards=data.get("premios", data.get("Awards", "")),
            language=data.get("idioma", data.get("Language", "")),
            poster=data.get("poster", data.get("Poster", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Title": self.title,
            "Year": self.year,
            "imdbRating": self.imdb_rating,
            "Genre": self.genre,
            "Director": self.director,
            "Actors": self.actors,
            "Plot": self.plot,
            "Country": self.country,
            "Awards": self.awards,
            "Language": self.language,
            "Poster": self.poster,
        }

    def to_local_dict(self) -> Dict[str, Any]:
        return {
            "titulo": self.title,
            "anio": self.year,
            "rating": self.imdb_rating,
        }
