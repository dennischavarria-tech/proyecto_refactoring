from unittest.mock import Mock

import pytest
import requests

from exceptions import APIConnectionError, InvalidInputError
from api.omdb import OmdbApiClient
from models.movie import Movie


class TestOmdbApiClientSearch:
    def test_buscar_pelicula_success(self, mock_omdb_client, mock_requests_get, sample_movie_data):
        mock_requests_get(status_code=200, json_data=sample_movie_data)
        result = mock_omdb_client.buscar_pelicula("Inception")
        assert result is not None
        assert result.title == "Inception"

    def test_buscar_pelicula_not_found(self, mock_omdb_client, mock_requests_get):
        error_response = {"Response": "False", "Error": "Movie not found!"}
        mock_requests_get(status_code=200, json_data=error_response)
        result = mock_omdb_client.buscar_pelicula("Nonexistent")
        assert result is None

    def test_buscar_pelicula_http_error(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(status_code=500, json_data={})
        with pytest.raises(APIConnectionError) as exc_info:
            mock_omdb_client.buscar_pelicula("Inception")
        assert "500" in str(exc_info.value)

    def test_buscar_pelicula_timeout(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.Timeout("Connection timed out"))
        with pytest.raises(APIConnectionError) as exc_info:
            mock_omdb_client.buscar_pelicula("Inception")
        assert "Error de conexion" in str(exc_info.value)

    def test_buscar_pelicula_connection_error(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.ConnectionError("Failed to connect"))
        with pytest.raises(APIConnectionError) as exc_info:
            mock_omdb_client.buscar_pelicula("Inception")
        assert "Error de conexion" in str(exc_info.value)

    def test_buscar_pelicula_invalid_api_key(self, mock_env_vars, monkeypatch):
        monkeypatch.setenv("OMDB_API_KEY", "")
        from constants import API_KEYS
        API_KEYS["omdb"] = ""
        client = OmdbApiClient()
        with pytest.raises(InvalidInputError) as exc_info:
            client.buscar_pelicula("Inception")
        assert "API key" in str(exc_info.value)

    def test_buscar_pelicula_invalid_title(self, mock_omdb_client, mock_requests_get):
        with pytest.raises(InvalidInputError):
            mock_omdb_client.buscar_pelicula("")


class TestOmdbApiClientSearchByActor:
    def test_buscar_peliculas_por_actor_success(self, mock_omdb_client, mock_requests_get, sample_movie_data):
        search_response = {
            "Response": "True",
            "Search": [
                {"Title": "Inception", "Year": "2010", "imdbID": "tt1375666"},
            ],
        }
        mock_requests_get(status_code=200, json_data=search_response)
        mock_omdb_client._make_request = Mock(side_effect=[search_response, sample_movie_data])
        result = mock_omdb_client.buscar_peliculas_por_actor("Leonardo DiCaprio")
        assert isinstance(result, list)

    def test_buscar_peliculas_por_actor_empty(self, mock_omdb_client, mock_requests_get):
        empty_response = {"Response": "False", "Error": "No results"}
        mock_requests_get(status_code=200, json_data=empty_response)
        result = mock_omdb_client.buscar_peliculas_por_actor("Unknown Actor")
        assert result == []

    def test_buscar_peliculas_por_actor_invalid_name(self, mock_omdb_client):
        with pytest.raises(InvalidInputError):
            mock_omdb_client.buscar_peliculas_por_actor("")


class TestOmdbApiClientPopularMovies:
    def test_obtener_peliculas_populares(self, mock_omdb_client):
        result = mock_omdb_client.obtener_peliculas_populares()
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(m, Movie) for m in result)


class TestOmdbApiClientSearchByGenre:
    def test_buscar_peliculas_por_genero_accion(self, mock_omdb_client):
        result = mock_omdb_client.buscar_peliculas_por_genero("accion")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_buscar_peliculas_por_genero_comedia(self, mock_omdb_client):
        result = mock_omdb_client.buscar_peliculas_por_genero("comedia")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_buscar_peliculas_por_genero_unknown(self, mock_omdb_client):
        result = mock_omdb_client.buscar_peliculas_por_genero("unknown")
        assert isinstance(result, list)
        assert len(result) > 0


class TestOmdbApiClientValidation:
    def test_validate_api_key_missing_raises_error(self, mock_env_vars, monkeypatch):
        monkeypatch.setenv("OMDB_API_KEY", "")
        from constants import API_KEYS
        API_KEYS["omdb"] = ""
        client = OmdbApiClient()
        with pytest.raises(InvalidInputError) as exc_info:
            client._validate_api_key()
        assert "API key" in str(exc_info.value)

    def test_validate_api_key_present(self, mock_omdb_client):
        mock_omdb_client._validate_api_key()

    def test_make_request_success(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(status_code=200, json_data={"test": "data"})
        result = mock_omdb_client._make_request("http://test.com", {"param": "value"})
        assert result == {"test": "data"}

    def test_make_request_http_error(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(status_code=404, json_data={})
        with pytest.raises(APIConnectionError) as exc_info:
            mock_omdb_client._make_request("http://test.com")
        assert "404" in str(exc_info.value)

    def test_make_request_network_error(self, mock_omdb_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.RequestException("Network error"))
        with pytest.raises(APIConnectionError):
            mock_omdb_client._make_request("http://test.com")
