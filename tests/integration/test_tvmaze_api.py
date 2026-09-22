from unittest.mock import Mock

import pytest
import requests

from exceptions import APIConnectionError, InvalidInputError
from api.tvmaze import TvmazeApiClient
from models.series import Series


class TestTvmazeApiClientSearch:
    def test_buscar_series_success(self, mock_tvmaze_client, mock_requests_get, sample_series_data):
        mock_requests_get(status_code=200, json_data=[sample_series_data])
        result = mock_tvmaze_client.buscar_series("Breaking Bad")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == "Breaking Bad"

    def test_buscar_series_empty_results(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(status_code=200, json_data=[])
        result = mock_tvmaze_client.buscar_series("Nonexistent Show")
        assert result == []

    def test_buscar_series_http_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(status_code=500, json_data={})
        with pytest.raises(APIConnectionError) as exc_info:
            mock_tvmaze_client.buscar_series("Breaking Bad")
        assert "500" in str(exc_info.value)

    def test_buscar_series_timeout(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.Timeout("Connection timed out"))
        with pytest.raises(APIConnectionError) as exc_info:
            mock_tvmaze_client.buscar_series("Breaking Bad")
        assert "Error de conexion" in str(exc_info.value)

    def test_buscar_series_invalid_name(self, mock_tvmaze_client):
        with pytest.raises(InvalidInputError):
            mock_tvmaze_client.buscar_series("")


class TestTvmazeApiClientDetails:
    def test_obtener_detalles_success(self, mock_tvmaze_client, mock_requests_get, sample_series_data):
        show_data = sample_series_data["show"]
        mock_requests_get(status_code=200, json_data=show_data)
        result = mock_tvmaze_client.obtener_detalles_serie(1)
        assert result is not None
        assert result.name == "Breaking Bad"
        assert result.id == 1

    def test_obtener_detalles_invalid_id(self, mock_tvmaze_client):
        with pytest.raises(InvalidInputError) as exc_info:
            mock_tvmaze_client.obtener_detalles_serie(0)
        assert "entero positivo" in str(exc_info.value)

    def test_obtener_detalles_negative_id(self, mock_tvmaze_client):
        with pytest.raises(InvalidInputError):
            mock_tvmaze_client.obtener_detalles_serie(-1)

    def test_obtener_detalles_non_integer_id(self, mock_tvmaze_client):
        with pytest.raises(InvalidInputError):
            mock_tvmaze_client.obtener_detalles_serie("abc")


class TestTvmazeApiClientConnectionErrors:
    def test_connection_error_raises_api_connection_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.ConnectionError("Failed to connect"))
        with pytest.raises(APIConnectionError) as exc_info:
            mock_tvmaze_client.buscar_series("Breaking Bad")
        assert "Error de conexion" in str(exc_info.value)

    def test_http_error_raises_api_connection_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(status_code=404, json_data={})
        with pytest.raises(APIConnectionError) as exc_info:
            mock_tvmaze_client.buscar_series("Breaking Bad")
        assert "404" in str(exc_info.value)


class TestTvmazeApiClientMakeRequest:
    def test_make_request_success(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(status_code=200, json_data={"test": "data"})
        result = mock_tvmaze_client._make_request("http://test.com", {"param": "value"})
        assert result == {"test": "data"}

    def test_make_request_http_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(status_code=500, json_data={})
        with pytest.raises(APIConnectionError) as exc_info:
            mock_tvmaze_client._make_request("http://test.com")
        assert "500" in str(exc_info.value)

    def test_make_request_network_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.RequestException("Network error"))
        with pytest.raises(APIConnectionError):
            mock_tvmaze_client._make_request("http://test.com")

    def test_make_request_timeout_error(self, mock_tvmaze_client, mock_requests_get):
        mock_requests_get(raise_exception=requests.Timeout("Timeout"))
        with pytest.raises(APIConnectionError):
            mock_tvmaze_client._make_request("http://test.com")
