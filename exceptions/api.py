from exceptions.base import BaseAppError


class APIConnectionError(BaseAppError):
    def __init__(self, url: str, status_code: int = 0, details: str = "") -> None:
        self.url = url
        self.status_code = status_code
        message = f"Error de conexion con la API: {url}"
        if status_code:
            message += f" (HTTP {status_code})"
        super().__init__(message=message, details=details)
