import json
import os
from typing import Any, Dict, Optional

from constants import DEFAULT_CONFIG


CONFIG_FILE: str = "config.json"

_config: Dict[str, Any] = {}


def _get_defaults() -> Dict[str, Any]:
    return {
        "app": {
            "name": "Mi App de Peliculas",
            "version": "1.0.0",
            "user": "Estudiante",
        },
        "api": {
            "timeout": DEFAULT_CONFIG["timeout"],
            "max_retries": DEFAULT_CONFIG["max_retries"],
        },
        "ui": {
            "theme": "dark",
            "language": "es",
            "items_per_page": 10,
        },
        "cache": {
            "enabled": True,
            "expiry_hours": 24,
            "max_size_mb": 100,
        },
        "logging": {
            "level": "DEBUG",
            "file": "app.log",
            "max_size_mb": 10,
        },
        "debug": DEFAULT_CONFIG["debug"],
        "verbose": DEFAULT_CONFIG["verbose"],
    }


def load_config() -> None:
    global _config
    defaults = _get_defaults()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                stored = json.load(f)
            _deep_merge(defaults, stored)
        except (json.JSONDecodeError, OSError):
            pass
    _config = defaults


def save_config() -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(_config, f, indent=4)


def get_config(key: str, default: Any = None) -> Any:
    keys = key.split(".")
    value: Any = _config
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default
    return value


def set_config(key: str, value: Any) -> None:
    keys = key.split(".")
    target: Any = _config
    for k in keys[:-1]:
        if k not in target or not isinstance(target[k], dict):
            target[k] = {}
        target = target[k]
    target[keys[-1]] = value


def reset_config() -> None:
    global _config
    _config = _get_defaults()
    save_config()


def get_all_config() -> Dict[str, Any]:
    return dict(_config)


def export_config(filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(_config, f, indent=4)


def import_config(filename: str) -> None:
    global _config
    with open(filename, "r") as f:
        _config = json.load(f)


def validate_config() -> bool:
    required_keys = ["app", "api", "ui", "cache", "logging"]
    return all(k in _config for k in required_keys)


def print_config() -> None:
    for section, values in _config.items():
        print(f"[{section}]")
        if isinstance(values, dict):
            for k, v in values.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {values}")
        print()


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


load_config()
