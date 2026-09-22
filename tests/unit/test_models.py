import pytest

from models.movie import Movie
from models.series import Series


class TestMovieModel:
    def test_movie_creation(self, sample_movie):
        assert sample_movie.title == "Inception"
        assert sample_movie.year == "2010"
        assert sample_movie.imdb_rating == "8.8"
        assert sample_movie.genre == "Action, Sci-Fi"
        assert sample_movie.director == "Christopher Nolan"

    def test_movie_from_omdb_dict_success(self, sample_movie_data):
        movie = Movie.from_omdb_dict(sample_movie_data)
        assert movie is not None
        assert movie.title == "Inception"
        assert movie.year == "2010"
        assert movie.imdb_rating == "8.8"
        assert movie.genre == "Action, Sci-Fi"

    def test_movie_from_omdb_dict_error_response(self):
        data = {"Response": "False", "Error": "Movie not found!"}
        movie = Movie.from_omdb_dict(data)
        assert movie is None

    def test_movie_from_omdb_dict_missing_fields(self):
        data = {"Response": "True", "Title": "Test"}
        movie = Movie.from_omdb_dict(data)
        assert movie is not None
        assert movie.title == "Test"
        assert movie.year == ""
        assert movie.imdb_rating == ""

    def test_movie_from_local_dict(self):
        data = {
            "titulo": "The Matrix",
            "anio": "1999",
            "rating": "8.7",
            "genero": "Action",
            "director": "Wachowskis",
            "actores": "Keanu Reeves",
            "trama": "A computer hacker learns about the true nature of reality.",
            "pais": "USA",
            "premios": "Won 4 Oscars",
            "idioma": "English",
            "poster": "http://example.com/matrix.jpg",
        }
        movie = Movie.from_local_dict(data)
        assert movie.title == "The Matrix"
        assert movie.year == "1999"
        assert movie.imdb_rating == "8.7"

    def test_movie_to_dict(self, sample_movie):
        movie_dict = sample_movie.to_dict()
        assert movie_dict["Title"] == "Inception"
        assert movie_dict["Year"] == "2010"
        assert movie_dict["imdbRating"] == "8.8"
        assert "Genre" in movie_dict
        assert "Director" in movie_dict

    def test_movie_to_local_dict(self, sample_movie):
        local_dict = sample_movie.to_local_dict()
        assert local_dict["titulo"] == "Inception"
        assert local_dict["anio"] == "2010"
        assert local_dict["rating"] == "8.8"

    def test_movie_default_values(self):
        movie = Movie(
            title="Test",
            year="2020",
            imdb_rating="7.0",
            genre="Drama",
            director="Test Director",
            actors="Test Actor",
            plot="Test plot",
            country="USA",
            awards="None",
        )
        assert movie.language == ""
        assert movie.poster == ""


class TestSeriesModel:
    def test_series_creation(self, sample_series):
        assert sample_series.name == "Breaking Bad"
        assert sample_series.id == 1
        assert sample_series.language == "English"
        assert sample_series.genres == ["Drama", "Crime"]
        assert sample_series.rating == 9.5

    def test_series_from_tvmaze_dict_success(self, sample_series_data):
        series = Series.from_tvmaze_dict(sample_series_data)
        assert series is not None
        assert series.name == "Breaking Bad"
        assert series.id == 1
        assert series.rating == 9.5

    def test_series_from_tvmaze_dict_missing_id(self):
        data = {"show": {"name": "Test Show"}}
        series = Series.from_tvmaze_dict(data)
        assert series is None

    def test_series_from_tvmaze_dict_empty_show(self):
        data = {"show": None}
        series = Series.from_tvmaze_dict(data)
        assert series is None

    def test_series_from_tvmaze_show(self, sample_series_data):
        show_data = sample_series_data["show"]
        series = Series.from_tvmaze_show(show_data)
        assert series.name == "Breaking Bad"
        assert series.id == 1
        assert series.status == "Ended"

    def test_series_to_dict(self, sample_series):
        series_dict = sample_series.to_dict()
        assert "show" in series_dict
        assert series_dict["show"]["id"] == 1
        assert series_dict["show"]["name"] == "Breaking Bad"
        assert series_dict["show"]["rating"]["average"] == 9.5

    def test_series_with_none_rating(self):
        data = {
            "show": {
                "id": 2,
                "name": "Test Show",
                "language": "English",
                "genres": [],
                "rating": None,
                "status": "Running",
                "premiered": "2020-01-01",
                "ended": "",
                "runtime": None,
                "summary": "",
            }
        }
        series = Series.from_tvmaze_dict(data)
        assert series is not None
        assert series.rating is None
        assert series.runtime is None
