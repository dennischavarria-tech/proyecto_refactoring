import json
from typing import Dict, Optional

from constants import MESSAGES
from exceptions import BaseAppError, InvalidInputError
from logger import get_logger
from services.movie_service import MovieService
from services.series_service import SeriesService
from ui.display import Display
from validators import (
    validate_menu_option,
    validate_movie_title,
    validate_actor_name,
    validate_series_name,
    validate_filename,
    validate_timeout,
    sanitize_input,
)

_logger = get_logger(__name__)


class Menu:
    def __init__(
        self,
        movie_service: MovieService,
        series_service: SeriesService,
        display: Display,
        config: Optional[Dict] = None,
    ) -> None:
        self._movie_service = movie_service
        self._series_service = series_service
        self._display = display
        self._config = config or {"debug": True, "verbose": True, "timeout": 30}

    def menu_principal(self) -> None:
        while True:
            self._display.clear_screen()
            self._display.print_header("SISTEMA DE PELÍCULAS Y SERIES")
            print("1. Buscar película por título")
            print("2. Buscar por actor")
            print("3. Buscar series")
            print("4. Ver películas populares")
            print("5. Buscar por género")
            print("6. Ver favoritos")
            print("7. Ver historial")
            print("8. Ver estadísticas")
            print("9. Exportar datos")
            print("10. Importar datos")
            print("11. Configuración")
            print("12. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self._funcion_buscar_pelicula()
            elif opcion == "2":
                self._funcion_buscar_actor()
            elif opcion == "3":
                self._funcion_buscar_series()
            elif opcion == "4":
                self._funcion_peliculas_populares()
            elif opcion == "5":
                self._funcion_buscar_por_genero()
            elif opcion == "6":
                self._funcion_ver_favoritos()
            elif opcion == "7":
                self._funcion_ver_historial()
            elif opcion == "8":
                self._funcion_estadisticas()
            elif opcion == "9":
                self._funcion_exportar()
            elif opcion == "10":
                self._funcion_importar()
            elif opcion == "11":
                self._funcion_configuracion()
            elif opcion == "12":
                print(MESSAGES["goodbye"])
                break
            else:
                print(MESSAGES["invalid_option"])
                self._display.delay(1)

    def _funcion_buscar_pelicula(self) -> None:
        titulo = input("Ingrese el título de la película: ")
        try:
            titulo_validado = validate_movie_title(titulo)
            print(MESSAGES["searching"])
            self._display.delay(1)

            movie = self._movie_service.buscar_pelicula(titulo_validado)
            self._display.mostrar_pelicula(movie)

            if movie is not None:
                self._movie_service.agregar_al_historial(movie)
                opcion = input("\n¿Agregar a favoritos? (s/n): ")
                if opcion.lower() == "s":
                    if self._movie_service.agregar_a_favoritas(movie):
                        print(MESSAGES["added_favorite"])
                    else:
                        print(MESSAGES["already_favorite"])
        except InvalidInputError as e:
            _logger.warning("Entrada invalida: %s", e)
            print(f"Error: {e.message}")
        except BaseAppError as e:
            _logger.error("Error de aplicacion: %s", e)
            print(f"Error: {e.message}")

        input(MESSAGES["press_enter"])

    def _funcion_buscar_actor(self) -> None:
        actor = input("Ingrese el nombre del actor: ")
        try:
            actor_validado = validate_actor_name(actor)
            print(MESSAGES["searching_actor"])

            movies = self._movie_service.buscar_peliculas_por_actor(actor_validado)

            if len(movies) > 0:
                self._display.mostrar_lista_peliculas(movies)

                opcion = input("\nSeleccione una película para ver detalles (0 para volver): ")
                if opcion.isdigit():
                    indice = int(opcion) - 1
                    if 0 <= indice < len(movies):
                        detalles = self._movie_service.buscar_pelicula(movies[indice].title)
                        self._display.mostrar_pelicula(detalles)
            else:
                print(MESSAGES["no_movies_found"])
        except InvalidInputError as e:
            _logger.warning("Entrada invalida: %s", e)
            print(f"Error: {e.message}")
        except BaseAppError as e:
            _logger.error("Error de aplicacion: %s", e)
            print(f"Error: {e.message}")

        input(MESSAGES["press_enter"])

    def _funcion_buscar_series(self) -> None:
        nombre = input("Ingrese el nombre de la serie: ")
        try:
            nombre_validado = validate_series_name(nombre)
            print(MESSAGES["searching_series"])

            series_list = self._series_service.buscar_series(nombre_validado)

            if len(series_list) > 0:
                self._display.mostrar_lista_series(series_list)

                opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
                if opcion.isdigit():
                    indice = int(opcion) - 1
                    if 0 <= indice < len(series_list):
                        detalles = self._series_service.obtener_detalles(series_list[indice].id)
                        self._display.mostrar_serie(detalles)
            else:
                print(MESSAGES["no_series_found"])
        except InvalidInputError as e:
            _logger.warning("Entrada invalida: %s", e)
            print(f"Error: {e.message}")
        except BaseAppError as e:
            _logger.error("Error de aplicacion: %s", e)
            print(f"Error: {e.message}")

        input(MESSAGES["press_enter"])

    def _funcion_peliculas_populares(self) -> None:
        self._display.print_header("PELÍCULAS POPULARES")
        movies = self._movie_service.obtener_peliculas_populares()
        self._display.mostrar_lista_peliculas(movies)
        input(MESSAGES["press_enter"])

    def _funcion_buscar_por_genero(self) -> None:
        print("Géneros disponibles: acción, comedia")
        genero = input("Ingrese el género: ")
        print(MESSAGES["searching"])

        movies = self._movie_service.buscar_peliculas_por_genero(genero)
        self._display.mostrar_lista_peliculas(movies)

        input(MESSAGES["press_enter"])

    def _funcion_ver_favoritos(self) -> None:
        self._display.print_header("MIS FAVORITOS")
        favorites = self._movie_service.obtener_favoritas()
        if len(favorites) > 0:
            self._display.mostrar_favoritas(favorites)

            opcion = input("\n¿Desea eliminar alguna? (número o Enter para volver): ")
            if opcion.isdigit():
                indice = int(opcion) - 1
                if 0 <= indice < len(favorites):
                    titulo = favorites[indice].title
                    if self._movie_service.eliminar_de_favoritas(titulo):
                        print(MESSAGES["removed_favorite"])
        else:
            print(MESSAGES["no_favorites"])

        input(MESSAGES["press_enter"])

    def _funcion_ver_historial(self) -> None:
        self._display.print_header("HISTORIAL DE BÚSQUEDAS")
        history = self._movie_service.obtener_historial()
        if len(history) > 0:
            self._display.mostrar_historial(history)

            opcion = input("\n¿Limpiar historial? (s/n): ")
            if opcion.lower() == "s":
                self._movie_service.limpiar_historial()
                print(MESSAGES["history_cleared"])
        else:
            print(MESSAGES["no_history"])

        input(MESSAGES["press_enter"])

    def _funcion_estadisticas(self) -> None:
        self._display.print_header("ESTADÍSTICAS")
        stats = self._movie_service.obtener_estadisticas()
        print(f"Total favoritas: {stats['total_favoritas']}")
        print(f"Total historial: {stats['total_historial']}")
        input(MESSAGES["press_enter"])

    def _funcion_exportar(self) -> None:
        nombre = input("Nombre del archivo (sin extensión): ")
        try:
            nombre_validado = validate_filename(nombre)
            self._movie_service.exportar_a_json(f"{nombre_validado}.json")
        except InvalidInputError as e:
            _logger.warning("Entrada invalida: %s", e)
            print(f"Error: {e.message}")
        except BaseAppError as e:
            _logger.error("Error de aplicacion: %s", e)
            print(f"Error: {e.message}")
        input(MESSAGES["press_enter"])

    def _funcion_importar(self) -> None:
        nombre = input("Nombre del archivo (sin extensión): ")
        try:
            nombre_validado = validate_filename(nombre)
            self._movie_service.importar_de_json(f"{nombre_validado}.json")
        except InvalidInputError as e:
            _logger.warning("Entrada invalida: %s", e)
            print(f"Error: {e.message}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error al importar archivo")
        except BaseAppError as e:
            _logger.error("Error de aplicacion: %s", e)
            print(f"Error: {e.message}")
        input(MESSAGES["press_enter"])

    def _funcion_configuracion(self) -> None:
        self._display.print_header("CONFIGURACIÓN")
        print(f"1. Debug: {self._config['debug']}")
        print(f"2. Verbose: {self._config['verbose']}")
        print(f"3. Timeout: {self._config['timeout']}")

        opcion = input("\nSeleccione opción a cambiar (0 para volver): ")
        if opcion == "1":
            self._config["debug"] = not self._config["debug"]
            print(f"Debug ahora es: {self._config['debug']}")
        elif opcion == "2":
            self._config["verbose"] = not self._config["verbose"]
            print(f"Verbose ahora es: {self._config['verbose']}")
        elif opcion == "3":
            try:
                timeout_input = input("Nuevo timeout: ")
                self._config["timeout"] = validate_timeout(timeout_input)
                print(f"Timeout ahora es: {self._config['timeout']}")
            except InvalidInputError as e:
                _logger.warning("Entrada invalida: %s", e)
                print(f"Error: {e.message}")

        input(MESSAGES["press_enter"])
