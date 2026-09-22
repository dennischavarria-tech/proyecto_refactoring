from exceptions.base import BaseAppError


class InvalidInputError(BaseAppError):
    def __init__(self, field: str, value: str = "", details: str = "") -> None:
        self.field = field
        self.value = value
        message = f"Entrada invalida para el campo: {field}"
        if value:
            message += f" (valor: {value})"
        super().__init__(message=message, details=details)
