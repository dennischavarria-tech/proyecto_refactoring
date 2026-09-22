import os
import json
import time
from datetime import datetime

# Variables globales
CONFIG_FILE = "app_config.json"
DEFAULT_CONFIG = {
    "app": {
        "name": "Movie Explorer",
        "version": "1.0.0",
        "author": "Student",
        "description": "Aplicación de películas y series"
    },
    "api": {
        "omdb_key": "trilogy",
        "tvmaze_url": "http://api.tvmaze.com",
        "timeout": 30,
        "max_retries": 3
    },
    "ui": {
        "theme": "dark",
        "language": "es",
        "items_per_page": 10,
        "show_posters": True,
        "animations": True
    },
    "cache": {
        "enabled": True,
        "expiry_hours": 24,
        "max_size_mb": 100
    },
    "data": {
        "auto_save": True,
        "backup_enabled": True,
        "max_backups": 10
    },
    "logging": {
        "enabled": True,
        "level": "DEBUG",
        "file": "app.log",
        "max_size_mb": 10
    }
}

app_config = {}

def load_config():
    """Carga configuración"""
    global app_config
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            app_config = json.load(f)
    else:
        app_config = DEFAULT_CONFIG.copy()
        save_config()

def save_config():
    """Guarda configuración"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(app_config, f, indent=4)

def get_config(section, key=None):
    """Obtiene configuración"""
    if key is None:
        return app_config.get(section)
    return app_config.get(section, {}).get(key)

def set_config(section, key, value):
    """Establece configuración"""
    if section not in app_config:
        app_config[section] = {}
    app_config[section][key] = value
    save_config()

def get_all_config():
    """Obtiene toda la configuración"""
    return app_config.copy()

def update_config(updates):
    """Actualiza múltiples configuraciones"""
    for section, values in updates.items():
        if section not in app_config:
            app_config[section] = {}
        app_config[section].update(values)
    save_config()

def reset_config():
    """Resetea configuración"""
    global app_config
    app_config = DEFAULT_CONFIG.copy()
    save_config()

def delete_config(section, key=None):
    """Elimina configuración"""
    if key is None:
        if section in app_config:
            del app_config[section]
            save_config()
            return True
    else:
        if section in app_config and key in app_config[section]:
            del app_config[section][key]
            save_config()
            return True
    return False

def export_config(filename):
    """Exporta configuración"""
    with open(filename, 'w') as f:
        json.dump(app_config, f, indent=4)

def import_config(filename):
    """Importa configuración"""
    global app_config
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            app_config = json.load(f)
        save_config()
        return True
    return False

def validate_config():
    """Valida configuración"""
    errors = []
    
    required_sections = ["app", "api", "ui", "cache", "data", "logging"]
    for section in required_sections:
        if section not in app_config:
            errors.append("Missing section: " + section)
    
    if "api" in app_config:
        if "timeout" in app_config["api"]:
            if not isinstance(app_config["api"]["timeout"], int):
                errors.append("api.timeout must be integer")
    
    return errors

def print_config():
    """Imprime configuración"""
    print("=" * 60)
    print("CONFIGURACIÓN DE LA APLICACIÓN")
    print("=" * 60)
    
    for section, values in app_config.items():
        print("\n" + section.upper() + ":")
        print("-" * 40)
        if isinstance(values, dict):
            for key, value in values.items():
                print("  " + key + ": " + str(value))
        else:
            print("  " + str(values))
    
    print("\n" + "=" * 60)

def get_config_summary():
    """Obtiene resumen de configuración"""
    summary = {}
    
    for section, values in app_config.items():
        if isinstance(values, dict):
            summary[section] = len(values)
        else:
            summary[section] = 1
    
    return summary

def backup_config():
    """Crea backup de configuración"""
    backup_name = "config_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_config(backup_name)
    return backup_name

def restore_config(backup_name):
    """Restaura configuración desde backup"""
    return import_config(backup_name)

def merge_config(other_config):
    """Merge configuraciones"""
    for section, values in other_config.items():
        if section not in app_config:
            app_config[section] = {}
        if isinstance(values, dict):
            app_config[section].update(values)
        else:
            app_config[section] = values
    save_config()

def get_config_value(path):
    """Obtiene valor por ruta (ej: 'api.timeout')"""
    keys = path.split(".")
    value = app_config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    
    return value

def set_config_value(path, value):
    """Establece valor por ruta"""
    keys = path.split(".")
    config = app_config
    
    for key in keys[:-1]:
        if key not in config:
            config[key] = {}
        config = config[key]
    
    config[keys[-1]] = value
    save_config()

# Cargar configuración al importar
load_config()
