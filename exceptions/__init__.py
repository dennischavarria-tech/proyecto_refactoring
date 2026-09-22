from exceptions.base import BaseAppError
from exceptions.not_found import MovieNotFoundError, SeriesNotFoundError
from exceptions.api import APIConnectionError
from exceptions.validation import InvalidInputError

__all__ = [
    "BaseAppError",
    "MovieNotFoundError",
    "SeriesNotFoundError",
    "APIConnectionError",
    "InvalidInputError",
]
