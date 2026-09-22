import sys
from typing import Dict

from api.omdb import OmdbApiClient
from api.tvmaze import TvmazeApiClient
from constants import DEFAULT_CONFIG
from exceptions import BaseAppError
from logger import get_logger
from services.movie_service import MovieService
from services.series_service import SeriesService
from ui.display import Display
from ui.menu import Menu

_logger = get_logger(__name__)


def _build_config() -> Dict:
    return dict(DEFAULT_CONFIG)


def main() -> None:
    config = _build_config()

    omdb_api = OmdbApiClient(
        timeout=config["timeout"],
        debug=config["debug"],
    )
    tvmaze_api = TvmazeApiClient(
        timeout=config["timeout"],
        debug=config["debug"],
    )

    movie_service = MovieService(omdb_api)
    series_service = SeriesService(tvmaze_api)

    display = Display()
    menu = Menu(movie_service, series_service, display, config)

    try:
        menu.menu_principal()
    except KeyboardInterrupt:
        _logger.info("Programa interrumpido por el usuario")
        sys.exit(0)
    except BaseAppError as e:
        _logger.error("Error de aplicacion: %s", e)
        sys.exit(1)
    except (OSError, ValueError, KeyError) as e:
        _logger.exception("Error inesperado: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
