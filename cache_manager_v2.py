import os
import json
import time
from datetime import datetime

# Variables globales
CACHE_DIR = "cache"
CACHE_INDEX_FILE = os.path.join(CACHE_DIR, "cache_index.json")
CACHE_EXPIRY_HOURS = 24

cache_index = {}

def init_cache():
    """Inicializa directorio de caché"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    load_cache_index()

def load_cache_index():
    """Carga índice de caché"""
    global cache_index
    
    if os.path.exists(CACHE_INDEX_FILE):
        with open(CACHE_INDEX_FILE, 'r') as f:
            cache_index = json.load(f)
    else:
        cache_index = {}

def save_cache_index():
    """Guarda índice de caché"""
    with open(CACHE_INDEX_FILE, 'w') as f:
        json.dump(cache_index, f, indent=4)

def get_cache_key(query, api_name):
    """Genera clave de caché"""
    return api_name + "_" + query.replace(" ", "_").lower() + ".json"

def save_to_cache(key, data):
    """Guarda datos en caché"""
    cache_file = os.path.join(CACHE_DIR, key)
    
    cache_entry = {
        "data": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires": (datetime.now().timestamp() + CACHE_EXPIRY_HOURS * 3600)
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_entry, f, indent=4)
    
    cache_index[key] = {
        "file": cache_file,
        "created": cache_entry["timestamp"],
        "expires": cache_entry["expires"]
    }
    save_cache_index()

def get_from_cache(key):
    """Obtiene datos de caché"""
    cache_file = os.path.join(CACHE_DIR, key)
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_entry = json.load(f)
        
        # Verificar expiración
        if datetime.now().timestamp() < cache_entry["expires"]:
            return cache_entry["data"]
        else:
            remove_from_cache(key)
    
    return None

def remove_from_cache(key):
    """Elimina entrada de caché"""
    cache_file = os.path.join(CACHE_DIR, key)
    
    if os.path.exists(cache_file):
        os.remove(cache_file)
    
    if key in cache_index:
        del cache_index[key]
        save_cache_index()

def clear_cache():
    """Limpia toda la caché"""
    global cache_index
    
    if os.path.exists(CACHE_DIR):
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
    
    cache_index = {}
    save_cache_index()

def cleanup_expired_cache():
    """Limpia entradas expiradas"""
    keys_to_remove = []
    
    for key, info in cache_index.items():
        if datetime.now().timestamp() > info["expires"]:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        remove_from_cache(key)

def cache_exists(key):
    """Verifica si existe entrada en caché"""
    cache_file = os.path.join(CACHE_DIR, key)
    return os.path.exists(cache_file)

def get_cache_size():
    """Obtiene tamaño total de caché"""
    total_size = 0
    
    if os.path.exists(CACHE_DIR):
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    
    return total_size

def get_cache_stats():
    """Obtiene estadísticas de caché"""
    total_entries = len(cache_index)
    expired_entries = 0
    valid_entries = 0
    
    for key, info in cache_index.items():
        if datetime.now().timestamp() > info["expires"]:
            expired_entries += 1
        else:
            valid_entries += 1
    
    return {
        "total": total_entries,
        "valid": valid_entries,
        "expired": expired_entries,
        "size_bytes": get_cache_size()
    }

def export_cache(filename):
    """Exporta caché completa"""
    export_data = {}
    
    for key, info in cache_index.items():
        cache_file = os.path.join(CACHE_DIR, key)
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                export_data[key] = json.load(f)
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=4)

def import_cache(filename):
    """Importa caché desde archivo"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported_data = json.load(f)
        
        for key, cache_entry in imported_data.items():
            save_to_cache(key, cache_entry["data"])

def list_cache_entries():
    """Lista entradas de caché"""
    entries = []
    
    for key, info in cache_index.items():
        entries.append({
            "key": key,
            "created": info["created"],
            "expires": datetime.fromtimestamp(info["expires"]).strftime("%Y-%m-%d %H:%M:%S"),
            "expired": datetime.now().timestamp() > info["expires"]
        })
    
    return entries

def get_cache_entry_info(key):
    """Obtiene información de entrada de caché"""
    if key in cache_index:
        info = cache_index[key]
        return {
            "key": key,
            "created": info["created"],
            "expires": datetime.fromtimestamp(info["expires"]).strftime("%Y-%m-%d %H:%M:%S"),
            "expired": datetime.now().timestamp() > info["expires"]
        }
    return None

def update_cache_expiry(key, hours):
    """Actualiza expiración de entrada"""
    cache_file = os.path.join(CACHE_DIR, key)
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_entry = json.load(f)
        
        cache_entry["expires"] = datetime.now().timestamp() + hours * 3600
        
        with open(cache_file, 'w') as f:
            json.dump(cache_entry, f, indent=4)
        
        cache_index[key]["expires"] = cache_entry["expires"]
        save_cache_index()
        return True
    
    return False

def get_cache_usage():
    """Obtiene uso de caché por tipo"""
    usage = {}
    
    for key in cache_index.keys():
        parts = key.split("_", 1)
        if len(parts) > 0:
            api_name = parts[0]
            usage[api_name] = usage.get(api_name, 0) + 1
    
    return usage

# Inicializar caché al importar
init_cache()
