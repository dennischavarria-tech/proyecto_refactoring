from typing import Dict, List, Optional

from api.tvmaze import TvmazeApiClient
from models.series import Series


class SeriesService:
    def __init__(self, api_client: TvmazeApiClient) -> None:
        self._api = api_client
        self._cache: Dict[str, List[Series]] = {}

    def buscar_series(self, nombre: str) -> List[Series]:
        cache_key = f"series_{nombre}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        series_list = self._api.buscar_series(nombre)
        self._cache[cache_key] = series_list
        return series_list

    def obtener_detalles(self, id_serie: int) -> Series:
        return self._api.obtener_detalles_serie(id_serie)
