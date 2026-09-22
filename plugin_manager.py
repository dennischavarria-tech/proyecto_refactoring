import os
import json
import time
from datetime import datetime

# Variables globales
PLUGIN_DIR = "plugins"
PLUGIN_INDEX_FILE = os.path.join(PLUGIN_DIR, "plugins.json")
plugins = {}

def init_plugins():
    """Inicializa directorio de plugins"""
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)
    load_plugin_index()

def load_plugin_index():
    """Carga índice de plugins"""
    global plugins
    
    if os.path.exists(PLUGIN_INDEX_FILE):
        with open(PLUGIN_INDEX_FILE, 'r') as f:
            plugins = json.load(f)
    else:
        plugins = {}

def save_plugin_index():
    """Guarda índice de plugins"""
    with open(PLUGIN_INDEX_FILE, 'w') as f:
        json.dump(plugins, f, indent=4)

def register_plugin(name, plugin_info):
    """Registra plugin"""
    plugins[name] = {
        "name": name,
        "version": plugin_info.get("version", "1.0.0"),
        "author": plugin_info.get("author", "Unknown"),
        "description": plugin_info.get("description", ""),
        "enabled": True,
        "registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "config": plugin_info.get("config", {})
    }
    save_plugin_index()

def unregister_plugin(name):
    """Desregistra plugin"""
    if name in plugins:
        del plugins[name]
        save_plugin_index()
        return True
    return False

def enable_plugin(name):
    """Habilita plugin"""
    if name in plugins:
        plugins[name]["enabled"] = True
        save_plugin_index()
        return True
    return False

def disable_plugin(name):
    """Deshabilita plugin"""
    if name in plugins:
        plugins[name]["enabled"] = False
        save_plugin_index()
        return True
    return False

def get_plugin(name):
    """Obtiene plugin"""
    return plugins.get(name)

def get_all_plugins():
    """Obtiene todos los plugins"""
    return plugins.copy()

def get_enabled_plugins():
    """Obtiene plugins habilitados"""
    enabled = {}
    for name, plugin in plugins.items():
        if plugin["enabled"]:
            enabled[name] = plugin
    return enabled

def search_plugins(query):
    """Busca plugins"""
    results = {}
    query_lower = query.lower()
    
    for name, plugin in plugins.items():
        if query_lower in name.lower() or query_lower in plugin.get("description", "").lower():
            results[name] = plugin
    
    return results

def update_plugin(name, updates):
    """Actualiza plugin"""
    if name in plugins:
        plugins[name].update(updates)
        save_plugin_index()
        return True
    return False

def get_plugin_config(name):
    """Obtiene configuración de plugin"""
    plugin = plugins.get(name)
    if plugin:
        return plugin.get("config", {})
    return {}

def set_plugin_config(name, config):
    """Establece configuración de plugin"""
    if name in plugins:
        plugins[name]["config"] = config
        save_plugin_index()
        return True
    return False

def export_plugins(filename):
    """Exporta plugins"""
    with open(filename, 'w') as f:
        json.dump(plugins, f, indent=4)

def import_plugins(filename):
    """Importa plugins"""
    global plugins
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        plugins.update(imported)
        save_plugin_index()
        return True
    return False

def get_plugin_stats():
    """Obtiene estadísticas de plugins"""
    stats = {
        "total": len(plugins),
        "enabled": 0,
        "disabled": 0
    }
    
    for plugin in plugins.values():
        if plugin["enabled"]:
            stats["enabled"] += 1
        else:
            stats["disabled"] += 1
    
    return stats

def validate_plugins():
    """Valida plugins"""
    errors = []
    
    for name, plugin in plugins.items():
        if "name" not in plugin:
            errors.append("Plugin " + name + " missing name")
        if "version" not in plugin:
            errors.append("Plugin " + name + " missing version")
    
    return errors

def backup_plugins():
    """Crea backup de plugins"""
    backup_name = "plugins_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_plugins(backup_name)
    return backup_name

def restore_plugins(backup_name):
    """Restaura plugins desde backup"""
    return import_plugins(backup_name)

def get_plugins_summary():
    """Obtiene resumen de plugins"""
    return {
        "total": len(plugins),
        "names": list(plugins.keys()),
        "enabled_count": len(get_enabled_plugins())
    }

# Inicializar plugins al importar
init_plugins()
