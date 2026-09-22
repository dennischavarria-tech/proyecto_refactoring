from typing import Any, Dict, List, Optional

import requests

from constants import API_URLS
from exceptions import APIConnectionError, InvalidInputError
from logger import get_logger
from models.series import Series
from validators import validate_series_name, sanitize_input

_logger = get_logger(__name__)


class TvmazeApiClient:
    def __init__(self, timeout: int = 30, debug: bool = False) -> None:
        self._base_url: str = API_URLS["tvmaze"]
        self._timeout: int = timeout
        self._debug: bool = debug

    def _make_request(self, url: str, params: Optional[Dict[str, str]] = None) -> Any:
        _logger.debug("Haciendo request a %s", url)

        try:
            response = requests.get(url, params=params, timeout=self._timeout)
        except requests.RequestException as e:
            _logger.error("Error de conexion: %s", e)
            raise APIConnectionError(url=url, details=str(e)) from e

        _logger.debug("Status code: %s", response.status_code)

        if response.status_code != 200:
            _logger.warning("Respuesta no exitosa: HTTP %s de %s", response.status_code, url)
            raise APIConnectionError(url=url, status_code=response.status_code)

        return response.json()

    def buscar_series(self, nombre: str) -> List[Series]:
        nombre_validado = validate_series_name(nombre)
        nombre_sanitizado = sanitize_input(nombre_validado)

        params = {"q": nombre_sanitizado}
        data = self._make_request(f"{self._base_url}/search/shows", params)

        series_list: List[Series] = []
        for item in data:
            series = Series.from_tvmaze_dict(item)
            if series:
                series_list.append(series)
        return series_list

    def obtener_detalles_serie(self, id_serie: int) -> Series:
        if not isinstance(id_serie, int) or id_serie <= 0:
            raise InvalidInputError("id_serie", str(id_serie), "El ID de la serie debe ser un entero positivo")

        data = self._make_request(f"{self._base_url}/shows/{id_serie}")
        return Series.from_tvmaze_show(data)
