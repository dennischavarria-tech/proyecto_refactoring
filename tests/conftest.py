import json
import os
import sys
from unittest.mock import Mock

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.omdb import OmdbApiClient
from api.tvmaze import TvmazeApiClient
from models.movie import Movie
from models.series import Series
from services.movie_service import MovieService
from services.series_service import SeriesService


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "test_api_key")
    monkeypatch.setenv("TMDB_API_KEY", "test_tmdb_key")
    monkeypatch.setenv("OMDB_API_URL", "http://test.omdbapi.com/")
    monkeypatch.setenv("TVMAZE_API_URL", "http://test.tvmaze.com")


@pytest.fixture
def sample_movie_data():
    return {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Genre": "Action, Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
        "Plot": "A thief who steals corporate secrets through dream-sharing technology.",
        "Country": "USA",
        "Awards": "Won 4 Oscars",
        "Language": "English",
        "Poster": "http://example.com/poster.jpg",
    }


@pytest.fixture
def sample_movie():
    return Movie(
        title="Inception",
        year="2010",
        imdb_rating="8.8",
        genre="Action, Sci-Fi",
        director="Christopher Nolan",
        actors="Leonardo DiCaprio",
        plot="A thief who steals corporate secrets.",
        country="USA",
        awards="Won 4 Oscars",
        language="English",
        poster="http://example.com/poster.jpg",
    )


@pytest.fixture
def sample_series_data():
    return {
        "show": {
            "id": 1,
            "name": "Breaking Bad",
            "language": "English",
            "genres": ["Drama", "Crime"],
            "rating": {"average": 9.5},
            "status": "Ended",
            "premiered": "2008-01-20",
            "ended": "2013-09-29",
            "runtime": 60,
            "summary": "A high school chemistry teacher turned meth producer.",
        }
    }


@pytest.fixture
def sample_series():
    return Series(
        id=1,
        name="Breaking Bad",
        language="English",
        genres=["Drama", "Crime"],
        rating=9.5,
        status="Ended",
        premiered="2008-01-20",
        ended="2013-09-29",
        runtime=60,
        summary="A high school chemistry teacher turned meth producer.",
    )


@pytest.fixture
def mock_omdb_client(mock_env_vars):
    client = OmdbApiClient(timeout=30, debug=False)
    client._api_key = "test_api_key"
    return client


@pytest.fixture
def mock_tvmaze_client(mock_env_vars):
    client = TvmazeApiClient(timeout=30, debug=False)
    return client


@pytest.fixture
def movie_service(mock_omdb_client):
    return MovieService(mock_omdb_client)


@pytest.fixture
def series_service(mock_tvmaze_client):
    return SeriesService(mock_tvmaze_client)


@pytest.fixture
def mock_requests_get(monkeypatch):
    def _mock_response(status_code=200, json_data=None, raise_exception=None):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data or {}

        if raise_exception:
            def side_effect(*args, **kwargs):
                raise raise_exception
            monkeypatch.setattr("requests.get", side_effect)
        else:
            monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

        return mock_response

    return _mock_response


@pytest.fixture
def mock_json_file(tmp_path):
    def _create_file(data, filename="test.json"):
        file_path = tmp_path / filename
        file_path.write_text(json.dumps(data))
        return str(file_path)

    return _create_file
