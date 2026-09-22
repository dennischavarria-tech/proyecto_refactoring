import json
import os

# Variables globales de configuración
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "app_name": "Mi App de Películas",
    "version": "1.0.0",
    "author": "Estudiante",
    "api_timeout": 30,
    "max_results": 10,
    "cache_enabled": True,
    "debug_mode": True,
    "log_file": "app.log",
    "data_dir": "data",
    "backup_dir": "backups"
}

# Configuración actual (global)
current_config = {}

def load_config():
    """Carga configuración sin manejo de errores"""
    global current_config
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            current_config = json.load(f)
    else:
        current_config = DEFAULT_CONFIG.copy()
        save_config()

def save_config():
    """Guarda configuración"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(current_config, f, indent=4)

def get_config(key):
    """Obtiene valor de configuración sin validación"""
    return current_config[key]

def set_config(key, value):
    """Establece valor de configuración"""
    current_config[key] = value
    save_config()

def reset_config():
    """Resetea configuración"""
    global current_config
    current_config = DEFAULT_CONFIG.copy()
    save_config()

def export_config(filename):
    """Exporta configuración"""
    with open(filename, 'w') as f:
        json.dump(current_config, f, indent=4)

def import_config(filename):
    """Importa configuración sin validación"""
    global current_config
    with open(filename, 'r') as f:
        current_config = json.load(f)

def print_config():
    """Imprime configuración"""
    for key, value in current_config.items():
        print(key + ": " + str(value))

def validate_config():
    """Valida configuración (pero no hace nada con los errores)"""
    errors = []
    
    if "api_timeout" not in current_config:
        errors.append("Falta api_timeout")
    
    if "max_results" not in current_config:
        errors.append("Falta max_results")
    
    if len(errors) > 0:
        print("Hay errores en la configuración:")
        for error in errors:
            print("- " + error)
    
    return len(errors) == 0

# Inicializar configuración
load_config()
