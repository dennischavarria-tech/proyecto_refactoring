import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_DIR: str = "logs"
LOG_FILE: str = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE: str = os.path.join(LOG_DIR, "error.log")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
MAX_BYTES: int = 10 * 1024 * 1024
BACKUP_COUNT: int = 5

_initialized: bool = False


def _ensure_log_dir() -> None:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def _setup_logging() -> None:
    global _initialized
    if _initialized:
        return

    _ensure_log_dir()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

    error_handler = RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    _initialized = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    _setup_logging()
    return logging.getLogger(name)


def log_debug(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).debug(message)


def log_info(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).info(message)


def log_warning(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).warning(message)


def log_error(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).error(message)


def log_exception(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).exception(message)


def log_critical(message: str, logger_name: Optional[str] = None) -> None:
    get_logger(logger_name).critical(message)
