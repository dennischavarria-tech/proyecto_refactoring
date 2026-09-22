import os
import json
import time
from datetime import datetime

# Variables globales
HISTORY_DIR = "history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "search_history.json")
MAX_HISTORY = 100

search_history = []

def init_history():
    """Inicializa historial"""
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    load_history()

def load_history():
    """Carga historial"""
    global search_history
    
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            search_history = json.load(f)
    else:
        search_history = []

def save_history():
    """Guarda historial"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(search_history, f, indent=4)

def add_search(query, results_count, search_type="movie"):
    """Agrega búsqueda al historial"""
    entry = {
        "query": query,
        "results_count": results_count,
        "search_type": search_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    search_history.insert(0, entry)
    
    # Mantener límite
    if len(search_history) > MAX_HISTORY:
        search_history = search_history[:MAX_HISTORY]
    
    save_history()

def get_history():
    """Obtiene historial"""
    return search_history.copy()

def clear_history():
    """Limpia historial"""
    global search_history
    search_history = []
    save_history()

def search_history_by_query(query):
    """Busca en historial por consulta"""
    results = []
    query_lower = query.lower()
    
    for entry in search_history:
        if query_lower in entry["query"].lower():
            results.append(entry)
    
    return results

def search_history_by_type(search_type):
    """Busca en historial por tipo"""
    results = []
    
    for entry in search_history:
        if entry["search_type"] == search_type:
            results.append(entry)
    
    return results

def search_history_by_date(date_str):
    """Busca en historial por fecha"""
    results = []
    
    for entry in search_history:
        if date_str in entry["timestamp"]:
            results.append(entry)
    
    return results

def get_recent_searches(count=10):
    """Obtiene búsquedas recientes"""
    return search_history[:count]

def get_popular_searches(count=10):
    """Obtiene búsquedas más populares"""
    query_count = {}
    
    for entry in search_history:
        query = entry["query"]
        query_count[query] = query_count.get(query, 0) + 1
    
    sorted_queries = sorted(query_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_queries[:count]

def get_search_stats():
    """Obtiene estadísticas de búsqueda"""
    stats = {
        "total_searches": len(search_history),
        "by_type": {},
        "by_date": {},
        "avg_results": 0
    }
    
    total_results = 0
    
    for entry in search_history:
        search_type = entry["search_type"]
        stats["by_type"][search_type] = stats["by_type"].get(search_type, 0) + 1
        
        date = entry["timestamp"].split(" ")[0]
        stats["by_date"][date] = stats["by_date"].get(date, 0) + 1
        
        total_results += entry["results_count"]
    
    if len(search_history) > 0:
        stats["avg_results"] = total_results / len(search_history)
    
    return stats

def export_history(filename):
    """Exporta historial"""
    with open(filename, 'w') as f:
        json.dump(search_history, f, indent=4)

def import_history(filename):
    """Importa historial"""
    global search_history
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported_history = json.load(f)
        
        search_history = imported_history + search_history
        
        # Mantener límite
        if len(search_history) > MAX_HISTORY:
            search_history = search_history[:MAX_HISTORY]
        
        save_history()
        return True
    return False

def delete_search(index):
    """Elimina búsqueda por índice"""
    if 0 <= index < len(search_history):
        search_history.pop(index)
        save_history()
        return True
    return False

def update_search(index, updates):
    """Actualiza búsqueda"""
    if 0 <= index < len(search_history):
        search_history[index].update(updates)
        save_history()
        return True
    return False

def get_history_size():
    """Obtiene tamaño del historial"""
    return len(search_history)

def backup_history():
    """Crea backup del historial"""
    backup_name = "history_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_history(backup_name)
    return backup_name

def restore_history(backup_name):
    """Restaura historial desde backup"""
    return import_history(backup_name)

def validate_history():
    """Valida integridad del historial"""
    errors = []
    
    for i, entry in enumerate(search_history):
        if "query" not in entry:
            errors.append("Entry " + str(i) + " missing query")
        if "timestamp" not in entry:
            errors.append("Entry " + str(i) + " missing timestamp")
        if "search_type" not in entry:
            errors.append("Entry " + str(i) + " missing search_type")
    
    return errors

# Inicializar historial al importar
init_history()
