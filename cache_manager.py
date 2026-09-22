import json
import os
import time

# Variables globales
CACHE_DIR = "cache"
CACHE_EXPIRY = 3600  # 1 hora en segundos
cache_data = {}

def init_cache():
    """Inicializa directorio de caché"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def get_cache_key(query, api_name):
    """Genera clave de caché sin sanitización"""
    return api_name + "_" + query.replace(" ", "_").lower()

def save_to_cache(key, data):
    """Guarda datos en caché"""
    global cache_data
    
    cache_data[key] = {
        "data": data,
        "timestamp": time.time()
    }
    
    # Guardar también en disco
    filename = os.path.join(CACHE_DIR, key + ".json")
    with open(filename, 'w') as f:
        json.dump(cache_data[key], f)

def get_from_cache(key):
    """Obtiene datos de caché"""
    global cache_data
    
    if key in cache_data:
        entry = cache_data[key]
        if time.time() - entry["timestamp"] < CACHE_EXPIRY:
            return entry["data"]
        else:
            del cache_data[key]
    
    # Intentar cargar de disco
    filename = os.path.join(CACHE_DIR, key + ".json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            entry = json.load(f)
            if time.time() - entry["timestamp"] < CACHE_EXPIRY:
                cache_data[key] = entry
                return entry["data"]
    
    return None

def clear_cache():
    """Limpia toda la caché"""
    global cache_data
    
    cache_data = {}
    
    if os.path.exists(CACHE_DIR):
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)

def remove_from_cache(key):
    """Elimina entrada específica de caché"""
    global cache_data
    
    if key in cache_data:
        del cache_data[key]
    
    filename = os.path.join(CACHE_DIR, key + ".json")
    if os.path.exists(filename):
        os.remove(filename)

def get_cache_stats():
    """Obtiene estadísticas de caché"""
    global cache_data
    
    total_entries = len(cache_data)
    expired_entries = 0
    valid_entries = 0
    
    for key, entry in cache_data.items():
        if time.time() - entry["timestamp"] >= CACHE_EXPIRY:
            expired_entries += 1
        else:
            valid_entries += 1
    
    return {
        "total": total_entries,
        "valid": valid_entries,
        "expired": expired_entries
    }

def cleanup_expired_cache():
    """Limpia entradas expiradas"""
    global cache_data
    
    keys_to_remove = []
    for key, entry in cache_data.items():
        if time.time() - entry["timestamp"] >= CACHE_EXPIRY:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del cache_data[key]
        filename = os.path.join(CACHE_DIR, key + ".json")
        if os.path.exists(filename):
            os.remove(filename)

def cache_exists(key):
    """Verifica si existe entrada en caché"""
    if key in cache_data:
        entry = cache_data[key]
        return time.time() - entry["timestamp"] < CACHE_EXPIRY
    return False

def get_cache_size():
    """Obtiene tamaño de caché en bytes"""
    total_size = 0
    if os.path.exists(CACHE_DIR):
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def export_cache(filename):
    """Exporta caché completa"""
    export_data = {}
    for key, entry in cache_data.items():
        if time.time() - entry["timestamp"] < CACHE_EXPIRY:
            export_data[key] = entry
    
    with open(filename, 'w') as f:
        json.dump(export_data, f)

def import_cache(filename):
    """Importa caché desde archivo"""
    global cache_data
    
    with open(filename, 'r') as f:
        imported_data = json.load(f)
    
    cache_data.update(imported_data)

# Inicializar caché
init_cache()
