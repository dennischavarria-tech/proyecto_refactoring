from exceptions.base import BaseAppError


class MovieNotFoundError(BaseAppError):
    def __init__(self, titulo: str) -> None:
        super().__init__(
            message=f"No se encontro la pelicula: {titulo}",
            details=f"Titulo buscado: {titulo}",
        )
        self.titulo = titulo


class SeriesNotFoundError(BaseAppError):
    def __init__(self, nombre: str) -> None:
        super().__init__(
            message=f"No se encontro la serie: {nombre}",
            details=f"Nombre buscado: {nombre}",
        )
        self.nombre = nombre
