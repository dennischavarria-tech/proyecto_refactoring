import os
import json
import time
from datetime import datetime

# Variables globales
STATS_FILE = "app_stats.json"
stats = {}

def load_stats():
    """Carga estadísticas"""
    global stats
    
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
    else:
        stats = {
            "searches": {"total": 0, "by_type": {}, "by_date": {}},
            "views": {"total": 0, "by_type": {}, "by_date": {}},
            "favorites": {"total": 0, "by_date": {}},
            "sessions": {"total": 0, "total_time": 0},
            "errors": {"total": 0, "by_type": {}}
        }

def save_stats():
    """Guarda estadísticas"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def increment_search(search_type="movie"):
    """Incrementa contador de búsquedas"""
    stats["searches"]["total"] = stats["searches"].get("total", 0) + 1
    
    by_type = stats["searches"].get("by_type", {})
    by_type[search_type] = by_type.get(search_type, 0) + 1
    stats["searches"]["by_type"] = by_type
    
    today = datetime.now().strftime("%Y-%m-%d")
    by_date = stats["searches"].get("by_date", {})
    by_date[today] = by_date.get(today, 0) + 1
    stats["searches"]["by_date"] = by_date
    
    save_stats()

def increment_view(view_type="movie"):
    """Incrementa contador de vistas"""
    stats["views"]["total"] = stats["views"].get("total", 0) + 1
    
    by_type = stats["views"].get("by_type", {})
    by_type[view_type] = by_type.get(view_type, 0) + 1
    stats["views"]["by_type"] = by_type
    
    today = datetime.now().strftime("%Y-%m-%d")
    by_date = stats["views"].get("by_date", {})
    by_date[today] = by_date.get(today, 0) + 1
    stats["views"]["by_date"] = by_date
    
    save_stats()

def increment_favorite():
    """Incrementa contador de favoritas"""
    stats["favorites"]["total"] = stats["favorites"].get("total", 0) + 1
    
    today = datetime.now().strftime("%Y-%m-%d")
    by_date = stats["favorites"].get("by_date", {})
    by_date[today] = by_date.get(today, 0) + 1
    stats["favorites"]["by_date"] = by_date
    
    save_stats()

def increment_session(duration=0):
    """Incrementa contador de sesiones"""
    stats["sessions"]["total"] = stats["sessions"].get("total", 0) + 1
    stats["sessions"]["total_time"] = stats["sessions"].get("total_time", 0) + duration
    save_stats()

def increment_error(error_type="unknown"):
    """Incrementa contador de errores"""
    stats["errors"]["total"] = stats["errors"].get("total", 0) + 1
    
    by_type = stats["errors"].get("by_type", {})
    by_type[error_type] = by_type.get(error_type, 0) + 1
    stats["errors"]["by_type"] = by_type
    
    save_stats()

def get_stats():
    """Obtiene todas las estadísticas"""
    return stats.copy()

def get_search_stats():
    """Obtiene estadísticas de búsquedas"""
    return stats.get("searches", {})

def get_view_stats():
    """Obtiene estadísticas de vistas"""
    return stats.get("views", {})

def get_favorite_stats():
    """Obtiene estadísticas de favoritas"""
    return stats.get("favorites", {})

def get_session_stats():
    """Obtiene estadísticas de sesiones"""
    return stats.get("sessions", {})

def get_error_stats():
    """Obtiene estadísticas de errores"""
    return stats.get("errors", {})

def reset_stats():
    """Resetea estadísticas"""
    global stats
    stats = {
        "searches": {"total": 0, "by_type": {}, "by_date": {}},
        "views": {"total": 0, "by_type": {}, "by_date": {}},
        "favorites": {"total": 0, "by_date": {}},
        "sessions": {"total": 0, "total_time": 0},
        "errors": {"total": 0, "by_type": {}}
    }
    save_stats()

def export_stats(filename):
    """Exporta estadísticas"""
    with open(filename, 'w') as f:
        json.dump(stats, f, indent=4)

def import_stats(filename):
    """Importa estadísticas"""
    global stats
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            stats = json.load(f)
        save_stats()
        return True
    return False

def get_stats_summary():
    """Obtiene resumen de estadísticas"""
    return {
        "total_searches": stats.get("searches", {}).get("total", 0),
        "total_views": stats.get("views", {}).get("total", 0),
        "total_favorites": stats.get("favorites", {}).get("total", 0),
        "total_sessions": stats.get("sessions", {}).get("total", 0),
        "total_errors": stats.get("errors", {}).get("total", 0)
    }

def print_stats():
    """Imprime estadísticas"""
    print("=" * 60)
    print("ESTADÍSTICAS DE LA APLICACIÓN")
    print("=" * 60)
    
    summary = get_stats_summary()
    print("Búsquedas totales: " + str(summary["total_searches"]))
    print("Vistas totales: " + str(summary["total_views"]))
    print("Favoritas totales: " + str(summary["total_favorites"]))
    print("Sesiones totales: " + str(summary["total_sessions"]))
    print("Errores totales: " + str(summary["total_errors"]))
    
    print("\nBúsquedas por tipo:")
    for search_type, count in stats.get("searches", {}).get("by_type", {}).items():
        print("  " + search_type + ": " + str(count))
    
    print("\nVistas por tipo:")
    for view_type, count in stats.get("views", {}).get("by_type", {}).items():
        print("  " + view_type + ": " + str(count))
    
    print("=" * 60)

def validate_stats():
    """Valida integridad de estadísticas"""
    errors = []
    
    required_keys = ["searches", "views", "favorites", "sessions", "errors"]
    for key in required_keys:
        if key not in stats:
            errors.append("Missing stats key: " + key)
    
    return errors

def backup_stats():
    """Crea backup de estadísticas"""
    backup_name = "stats_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_stats(backup_name)
    return backup_name

def restore_stats(backup_name):
    """Restaura estadísticas desde backup"""
    return import_stats(backup_name)

# Cargar estadísticas al importar
load_stats()
