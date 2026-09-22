import os
import json
import time
from datetime import datetime

# Variables globales
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "app_name": "Movie Explorer",
    "version": "1.0.0",
    "author": "Student",
    "theme": "dark",
    "language": "es",
    "api_timeout": 30,
    "max_results": 10,
    "cache_enabled": True,
    "debug_mode": True,
    "verbose_output": True,
    "auto_save": True,
    "backup_enabled": True,
    "max_backups": 10,
    "log_level": "DEBUG",
    "date_format": "%Y-%m-%d",
    "time_format": "%H:%M:%S",
    "datetime_format": "%Y-%m-%d %H:%M:%S"
}

current_settings = {}

def load_settings():
    """Carga configuración"""
    global current_settings
    
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            current_settings = json.load(f)
    else:
        current_settings = DEFAULT_SETTINGS.copy()
        save_settings()

def save_settings():
    """Guarda configuración"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(current_settings, f, indent=4)

def get_setting(key):
    """Obtiene configuración"""
    return current_settings.get(key)

def set_setting(key, value):
    """Establece configuración"""
    current_settings[key] = value
    save_settings()

def reset_settings():
    """Resetea configuración"""
    global current_settings
    current_settings = DEFAULT_SETTINGS.copy()
    save_settings()

def get_all_settings():
    """Obtiene todas las configuraciones"""
    return current_settings.copy()

def update_settings(new_settings):
    """Actualiza múltiples configuraciones"""
    current_settings.update(new_settings)
    save_settings()

def delete_setting(key):
    """Elimina configuración"""
    if key in current_settings:
        del current_settings[key]
        save_settings()
        return True
    return False

def export_settings(filename):
    """Exporta configuración"""
    with open(filename, 'w') as f:
        json.dump(current_settings, f, indent=4)

def import_settings(filename):
    """Importa configuración"""
    global current_settings
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            current_settings = json.load(f)
        save_settings()
        return True
    return False

def validate_settings():
    """Valida configuración"""
    errors = []
    
    required_keys = ["app_name", "version", "api_timeout", "max_results"]
    for key in required_keys:
        if key not in current_settings:
            errors.append("Missing setting: " + key)
    
    if "api_timeout" in current_settings:
        if not isinstance(current_settings["api_timeout"], int):
            errors.append("api_timeout must be integer")
        elif current_settings["api_timeout"] <= 0:
            errors.append("api_timeout must be positive")
    
    if "max_results" in current_settings:
        if not isinstance(current_settings["max_results"], int):
            errors.append("max_results must be integer")
        elif current_settings["max_results"] <= 0:
            errors.append("max_results must be positive")
    
    return errors

def print_settings():
    """Imprime configuración"""
    print("=" * 50)
    print("CONFIGURACIÓN ACTUAL")
    print("=" * 50)
    
    for key, value in current_settings.items():
        print(key + ": " + str(value))
    
    print("=" * 50)

def get_setting_type(key):
    """Obtiene tipo de configuración"""
    value = current_settings.get(key)
    if value is None:
        return "None"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    else:
        return "unknown"

def copy_settings():
    """Copia configuración"""
    return current_settings.copy()

def merge_settings(other_settings):
    """Merge configuraciones"""
    current_settings.update(other_settings)
    save_settings()

def get_settings_summary():
    """Obtiene resumen de configuración"""
    return {
        "total_settings": len(current_settings),
        "setting_keys": list(current_settings.keys()),
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def backup_settings():
    """Crea backup de configuración"""
    backup_name = "settings_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_settings(backup_name)
    return backup_name

def restore_settings(backup_name):
    """Restaura configuración desde backup"""
    return import_settings(backup_name)

# Cargar configuración al importar
load_settings()
