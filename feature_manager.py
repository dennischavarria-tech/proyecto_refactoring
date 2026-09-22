import os
import json
import time
from datetime import datetime

# Variables globales
FEATURE_FILE = "features.json"
features = {}

def load_features():
    """Carga funcionalidades"""
    global features
    
    if os.path.exists(FEATURE_FILE):
        with open(FEATURE_FILE, 'r') as f:
            features = json.load(f)
    else:
        features = {}

def save_features():
    """Guarda funcionalidades"""
    with open(FEATURE_FILE, 'w') as f:
        json.dump(features, f, indent=4)

def add_feature(name, feature_info=None):
    """Agrega funcionalidad"""
    if feature_info is None:
        feature_info = {}
    
    features[name] = {
        "name": name,
        "enabled": True,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": feature_info.get("description", ""),
        "version": feature_info.get("version", "1.0.0"),
        "config": feature_info.get("config", {})
    }
    save_features()

def remove_feature(name):
    """Elimina funcionalidad"""
    if name in features:
        del features[name]
        save_features()
        return True
    return False

def enable_feature(name):
    """Habilita funcionalidad"""
    if name in features:
        features[name]["enabled"] = True
        save_features()
        return True
    return False

def disable_feature(name):
    """Deshabilita funcionalidad"""
    if name in features:
        features[name]["enabled"] = False
        save_features()
        return True
    return False

def get_feature(name):
    """Obtiene funcionalidad"""
    return features.get(name)

def get_all_features():
    """Obtiene todas las funcionalidades"""
    return features.copy()

def get_enabled_features():
    """Obtiene funcionalidades habilitadas"""
    enabled = {}
    for name, feature in features.items():
        if feature["enabled"]:
            enabled[name] = feature
    return enabled

def get_disabled_features():
    """Obtiene funcionalidades deshabilitadas"""
    disabled = {}
    for name, feature in features.items():
        if not feature["enabled"]:
            disabled[name] = feature
    return disabled

def search_features(query):
    """Busca funcionalidades"""
    results = {}
    query_lower = query.lower()
    
    for name, feature in features.items():
        if query_lower in name.lower() or query_lower in feature.get("description", "").lower():
            results[name] = feature
    
    return results

def update_feature(name, updates):
    """Actualiza funcionalidad"""
    if name in features:
        features[name].update(updates)
        save_features()
        return True
    return False

def get_feature_config(name):
    """Obtiene configuración de funcionalidad"""
    feature = features.get(name)
    if feature:
        return feature.get("config", {})
    return {}

def set_feature_config(name, config):
    """Establece configuración de funcionalidad"""
    if name in features:
        features[name]["config"] = config
        save_features()
        return True
    return False

def clear_features():
    """Limpia funcionalidades"""
    global features
    features = {}
    save_features()

def get_feature_stats():
    """Obtiene estadísticas de funcionalidades"""
    stats = {
        "total": len(features),
        "enabled": 0,
        "disabled": 0
    }
    
    for feature in features.values():
        if feature["enabled"]:
            stats["enabled"] += 1
        else:
            stats["disabled"] += 1
    
    return stats

def export_features(filename):
    """Exporta funcionalidades"""
    with open(filename, 'w') as f:
        json.dump(features, f, indent=4)

def import_features(filename):
    """Importa funcionalidades"""
    global features
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            features = json.load(f)
        save_features()
        return True
    return False

def validate_features():
    """Valida integridad de funcionalidades"""
    errors = []
    
    for name, feature in features.items():
        if "name" not in feature:
            errors.append("Feature " + name + " missing name")
        if "enabled" not in feature:
            errors.append("Feature " + name + " missing enabled")
    
    return errors

def backup_features():
    """Crea backup de funcionalidades"""
    backup_name = "features_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_features(backup_name)
    return backup_name

def restore_features(backup_name):
    """Restaura funcionalidades desde backup"""
    return import_features(backup_name)

def get_features_summary():
    """Obtiene resumen de funcionalidades"""
    return {
        "total": len(features),
        "enabled_count": len(get_enabled_features()),
        "names": list(features.keys())
    }

# Cargar funcionalidades al importar
load_features()
