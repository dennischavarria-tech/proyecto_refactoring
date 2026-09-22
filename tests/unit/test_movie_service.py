import json
import os
from unittest.mock import Mock, patch

import pytest

from models.movie import Movie
from services.movie_service import MovieService


class TestMovieServiceSearch:
    def test_buscar_pelicula_success(self, movie_service, mock_omdb_client, sample_movie):
        mock_omdb_client.buscar_pelicula = Mock(return_value=sample_movie)
        result = movie_service.buscar_pelicula("Inception")
        assert result is not None
        assert result.title == "Inception"
        mock_omdb_client.buscar_pelicula.assert_called_once_with("Inception")

    def test_buscar_pelicula_not_found(self, movie_service, mock_omdb_client):
        mock_omdb_client.buscar_pelicula = Mock(return_value=None)
        result = movie_service.buscar_pelicula("Nonexistent")
        assert result is None

    def test_buscar_pelicula_uses_cache(self, movie_service, mock_omdb_client, sample_movie):
        mock_omdb_client.buscar_pelicula = Mock(return_value=sample_movie)
        movie_service.buscar_pelicula("Inception")
        movie_service.buscar_pelicula("Inception")
        mock_omdb_client.buscar_pelicula.assert_called_once()

    def test_buscar_peliculas_por_actor_success(self, movie_service, mock_omdb_client, sample_movie):
        mock_omdb_client.buscar_peliculas_por_actor = Mock(return_value=[sample_movie])
        result = movie_service.buscar_peliculas_por_actor("Leonardo DiCaprio")
        assert len(result) == 1
        assert result[0].title == "Inception"

    def test_buscar_peliculas_por_actor_empty_results(self, movie_service, mock_omdb_client):
        mock_omdb_client.buscar_peliculas_por_actor = Mock(return_value=[])
        result = movie_service.buscar_peliculas_por_actor("Unknown Actor")
        assert result == []

    def test_obtener_peliculas_populares(self, movie_service, mock_omdb_client, sample_movie):
        mock_omdb_client.obtener_peliculas_populares = Mock(return_value=[sample_movie])
        result = movie_service.obtener_peliculas_populares()
        assert len(result) == 1

    def test_buscar_peliculas_por_genero_success(self, movie_service, mock_omdb_client, sample_movie):
        mock_omdb_client.buscar_peliculas_por_genero = Mock(return_value=[sample_movie])
        result = movie_service.buscar_peliculas_por_genero("accion")
        assert len(result) == 1


class TestMovieServiceFavorites:
    def test_agregar_a_favoritas_success(self, movie_service, sample_movie):
        result = movie_service.agregar_a_favoritas(sample_movie)
        assert result is True
        assert len(movie_service.obtener_favoritas()) == 1

    def test_agregar_a_favoritas_duplicate(self, movie_service, sample_movie):
        movie_service.agregar_a_favoritas(sample_movie)
        result = movie_service.agregar_a_favoritas(sample_movie)
        assert result is False
        assert len(movie_service.obtener_favoritas()) == 1

    def test_eliminar_de_favoritas_success(self, movie_service, sample_movie):
        movie_service.agregar_a_favoritas(sample_movie)
        result = movie_service.eliminar_de_favoritas("Inception")
        assert result is True
        assert len(movie_service.obtener_favoritas()) == 0

    def test_eliminar_de_favoritas_not_found(self, movie_service):
        result = movie_service.eliminar_de_favoritas("Nonexistent")
        assert result is False

    def test_obtener_favoritas_empty(self, movie_service):
        result = movie_service.obtener_favoritas()
        assert result == []

    def test_obtener_favoritas_multiple(self, movie_service):
        movie1 = Movie("Movie1", "2020", "7.0", "Action", "Dir1", "Act1", "Plot1", "USA", "None")
        movie2 = Movie("Movie2", "2021", "8.0", "Drama", "Dir2", "Act2", "Plot2", "USA", "None")
        movie_service.agregar_a_favoritas(movie1)
        movie_service.agregar_a_favoritas(movie2)
        result = movie_service.obtener_favoritas()
        assert len(result) == 2


class TestMovieServiceHistory:
    def test_agregar_al_historial(self, movie_service, sample_movie):
        movie_service.agregar_al_historial(sample_movie)
        history = movie_service.obtener_historial()
        assert len(history) == 1
        assert history[0]["titulo"] == "Inception"

    def test_limpiar_historial(self, movie_service, sample_movie):
        movie_service.agregar_al_historial(sample_movie)
        movie_service.limpiar_historial()
        history = movie_service.obtener_historial()
        assert history == []

    def test_obtener_historial_empty(self, movie_service):
        history = movie_service.obtener_historial()
        assert history == []

    def test_obtener_historial_multiple(self, movie_service, sample_movie):
        movie_service.agregar_al_historial(sample_movie)
        movie_service.agregar_al_historial(sample_movie)
        history = movie_service.obtener_historial()
        assert len(history) == 2


class TestMovieServiceStats:
    def test_obtener_estadisticas(self, movie_service, sample_movie):
        movie_service.agregar_a_favoritas(sample_movie)
        movie_service.agregar_al_historial(sample_movie)
        stats = movie_service.obtener_estadisticas()
        assert stats["total_favoritas"] == 1
        assert stats["total_historial"] == 1

    def test_obtener_estadisticas_empty(self, movie_service):
        stats = movie_service.obtener_estadisticas()
        assert stats["total_favoritas"] == 0
        assert stats["total_historial"] == 0


class TestMovieServiceImportExport:
    def test_exportar_a_json_success(self, movie_service, sample_movie, tmp_path):
        movie_service.agregar_a_favoritas(sample_movie)
        file_path = tmp_path / "export.json"
        movie_service.exportar_a_json(str(file_path))
        assert file_path.exists()
        with open(file_path) as f:
            data = json.load(f)
        assert "favoritas" in data
        assert "historial" in data
        assert "estadisticas" in data

    def test_importar_de_json_success(self, movie_service, sample_movie, tmp_path):
        movie_dict = sample_movie.to_dict()
        movie_dict["Response"] = "True"
        data = {
            "favoritas": [movie_dict],
            "historial": [{"titulo": "Inception", "fecha": "hoy"}],
        }
        file_path = tmp_path / "import.json"
        with open(file_path, "w") as f:
            json.dump(data, f)
        movie_service.importar_de_json(str(file_path))
        assert len(movie_service.obtener_favoritas()) == 1
        assert len(movie_service.obtener_historial()) == 1

    def test_importar_de_json_file_not_found(self, movie_service):
        with pytest.raises(FileNotFoundError):
            movie_service.importar_de_json("nonexistent.json")

    def test_importar_de_json_invalid_json(self, tmp_path, movie_service):
        file_path = tmp_path / "invalid.json"
        file_path.write_text("not valid json")
        with pytest.raises(json.JSONDecodeError):
            movie_service.importar_de_json(str(file_path))
