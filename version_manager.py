import os
import json
import time
from datetime import datetime

# Variables globales
VERSION_FILE = "version.json"
version_info = {}

def load_version():
    """Carga información de versión"""
    global version_info
    
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            version_info = json.load(f)
    else:
        version_info = {
            "current": "1.0.0",
            "history": [],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def save_version():
    """Guarda información de versión"""
    with open(VERSION_FILE, 'w') as f:
        json.dump(version_info, f, indent=4)

def get_current_version():
    """Obtiene versión actual"""
    return version_info.get("current", "1.0.0")

def set_version(version):
    """Establece versión"""
    old_version = version_info.get("current", "1.0.0")
    
    version_info["current"] = version
    version_info["history"].append({
        "from": old_version,
        "to": version,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    save_version()

def get_version_history():
    """Obtiene historial de versiones"""
    return version_info.get("history", [])

def increment_major():
    """Incrementa versión mayor"""
    current = get_current_version()
    parts = current.split(".")
    
    if len(parts) >= 3:
        major = int(parts[0]) + 1
        new_version = str(major) + ".0.0"
    else:
        new_version = "2.0.0"
    
    set_version(new_version)
    return new_version

def increment_minor():
    """Incrementa versión menor"""
    current = get_current_version()
    parts = current.split(".")
    
    if len(parts) >= 3:
        major = parts[0]
        minor = int(parts[1]) + 1
        new_version = major + "." + str(minor) + ".0"
    else:
        new_version = "1.1.0"
    
    set_version(new_version)
    return new_version

def increment_patch():
    """Incrementa versión parche"""
    current = get_current_version()
    parts = current.split(".")
    
    if len(parts) >= 3:
        major = parts[0]
        minor = parts[1]
        patch = int(parts[2]) + 1
        new_version = major + "." + minor + "." + str(patch)
    else:
        new_version = "1.0.1"
    
    set_version(new_version)
    return new_version

def compare_versions(version1, version2):
    """Compara versiones"""
    parts1 = version1.split(".")
    parts2 = version2.split(".")
    
    for i in range(max(len(parts1), len(parts2))):
        v1 = int(parts1[i]) if i < len(parts1) else 0
        v2 = int(parts2[i]) if i < len(parts2) else 0
        
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    
    return 0

def is_newer_version(version1, version2):
    """Verifica si version1 es más reciente que version2"""
    return compare_versions(version1, version2) > 0

def get_version_info():
    """Obtiene información completa de versión"""
    return version_info.copy()

def export_version(filename):
    """Exporta información de versión"""
    with open(filename, 'w') as f:
        json.dump(version_info, f, indent=4)

def import_version(filename):
    """Importa información de versión"""
    global version_info
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            version_info = json.load(f)
        save_version()
        return True
    return False

def validate_version():
    """Valida integridad de versión"""
    errors = []
    
    if "current" not in version_info:
        errors.append("Missing current version")
    
    if "history" not in version_info:
        errors.append("Missing version history")
    
    return errors

def backup_version():
    """Crea backup de versión"""
    backup_name = "version_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_version(backup_name)
    return backup_name

def restore_version(backup_name):
    """Restaura versión desde backup"""
    return import_version(backup_name)

def get_version_summary():
    """Obtiene resumen de versión"""
    return {
        "current": get_current_version(),
        "total_changes": len(get_version_history())
    }

# Cargar versión al importar
load_version()
