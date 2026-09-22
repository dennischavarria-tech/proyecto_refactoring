from unittest.mock import Mock

import pytest

from models.series import Series
from services.series_service import SeriesService


class TestSeriesServiceSearch:
    def test_buscar_series_success(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        result = series_service.buscar_series("Breaking Bad")
        assert len(result) == 1
        assert result[0].name == "Breaking Bad"
        mock_tvmaze_client.buscar_series.assert_called_once_with("Breaking Bad")

    def test_buscar_series_uses_cache(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        series_service.buscar_series("Breaking Bad")
        series_service.buscar_series("Breaking Bad")
        mock_tvmaze_client.buscar_series.assert_called_once()

    def test_buscar_series_empty_results(self, series_service, mock_tvmaze_client):
        mock_tvmaze_client.buscar_series = Mock(return_value=[])
        result = series_service.buscar_series("Nonexistent Show")
        assert result == []

    def test_buscar_series_multiple_results(self, series_service, mock_tvmaze_client):
        series1 = Series(1, "Show1", "English", ["Drama"], 8.0, "Ended", "2020-01-01", "2020-12-31", 60, "Summary1")
        series2 = Series(2, "Show2", "English", ["Comedy"], 7.5, "Running", "2021-01-01", "", 30, "Summary2")
        mock_tvmaze_client.buscar_series = Mock(return_value=[series1, series2])
        result = series_service.buscar_series("Show")
        assert len(result) == 2


class TestSeriesServiceDetails:
    def test_obtener_detalles_success(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.obtener_detalles_serie = Mock(return_value=sample_series)
        result = series_service.obtener_detalles(1)
        assert result is not None
        assert result.name == "Breaking Bad"
        assert result.id == 1
        mock_tvmaze_client.obtener_detalles_serie.assert_called_once_with(1)


class TestSeriesServiceCache:
    def test_cache_key_generation(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        series_service.buscar_series("Breaking Bad")
        assert "series_Breaking Bad" in series_service._cache

    def test_cache_hit(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        series_service.buscar_series("Breaking Bad")
        series_service.buscar_series("Breaking Bad")
        assert mock_tvmaze_client.buscar_series.call_count == 1

    def test_cache_miss(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        series_service.buscar_series("Breaking Bad")
        series_service.buscar_series("The Wire")
        assert mock_tvmaze_client.buscar_series.call_count == 2

    def test_cache_different_queries(self, series_service, mock_tvmaze_client, sample_series):
        mock_tvmaze_client.buscar_series = Mock(return_value=[sample_series])
        series_service.buscar_series("Show1")
        series_service.buscar_series("Show2")
        series_service.buscar_series("Show3")
        assert mock_tvmaze_client.buscar_series.call_count == 3
        assert len(series_service._cache) == 3
