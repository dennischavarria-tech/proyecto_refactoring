import os
import json
import time
from datetime import datetime

# Variables globales
METADATA_FILE = "metadata.json"
metadata = {}

def load_metadata():
    """Carga metadatos"""
    global metadata
    
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

def save_metadata():
    """Guarda metadatos"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

def add_metadata(key, value):
    """Agrega metadato"""
    metadata[key] = {
        "value": value,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_metadata()

def remove_metadata(key):
    """Elimina metadato"""
    if key in metadata:
        del metadata[key]
        save_metadata()
        return True
    return False

def get_metadata(key):
    """Obtiene metadato"""
    return metadata.get(key)

def get_metadata_value(key):
    """Obtiene valor de metadato"""
    if key in metadata:
        return metadata[key].get("value")
    return None

def set_metadata(key, value):
    """Establece metadato"""
    if key in metadata:
        metadata[key]["value"] = value
        metadata[key]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        metadata[key] = {
            "value": value,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    save_metadata()

def get_all_metadata():
    """Obtiene todos los metadatos"""
    return metadata.copy()

def search_metadata(query):
    """Busca metadatos"""
    results = {}
    query_lower = query.lower()
    
    for key, value in metadata.items():
        if query_lower in key.lower():
            results[key] = value
    
    return results

def clear_metadata():
    """Limpia metadatos"""
    global metadata
    metadata = {}
    save_metadata()

def get_metadata_stats():
    """Obtiene estadísticas de metadatos"""
    stats = {
        "total": len(metadata),
        "by_type": {}
    }
    
    for key, value in metadata.items():
        value_type = type(value.get("value")).__name__
        stats["by_type"][value_type] = stats["by_type"].get(value_type, 0) + 1
    
    return stats

def export_metadata(filename):
    """Exporta metadatos"""
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def import_metadata(filename):
    """Importa metadatos"""
    global metadata
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            metadata = json.load(f)
        save_metadata()
        return True
    return False

def validate_metadata():
    """Valida integridad de metadatos"""
    errors = []
    
    for key, value in metadata.items():
        if "value" not in value:
            errors.append("Metadata " + key + " missing value")
        if "created" not in value:
            errors.append("Metadata " + key + " missing created")
    
    return errors

def backup_metadata():
    """Crea backup de metadatos"""
    backup_name = "metadata_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_metadata(backup_name)
    return backup_name

def restore_metadata(backup_name):
    """Restaura metadatos desde backup"""
    return import_metadata(backup_name)

def get_metadata_summary():
    """Obtiene resumen de metadatos"""
    return {
        "total": len(metadata),
        "keys": list(metadata.keys())
    }

def update_metadata(key, updates):
    """Actualiza metadato"""
    if key in metadata:
        metadata[key].update(updates)
        metadata[key]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_metadata()
        return True
    return False

def get_metadata_by_pattern(pattern):
    """Obtiene metadatos por patrón"""
    results = {}
    
    for key, value in metadata.items():
        if pattern in key:
            results[key] = value
    
    return results

# Cargar metadatos al importar
load_metadata()
