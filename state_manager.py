import os
import json
import time
from datetime import datetime

# Variables globales
STATE_FILE = "app_state.json"
DEFAULT_STATE = {
    "current_user": None,
    "favorites": [],
    "history": [],
    "search_results": [],
    "current_movie": None,
    "current_series": None,
    "ui_state": {
        "current_menu": "main",
        "selected_index": 0,
        "scroll_position": 0
    },
    "session": {
        "start_time": None,
        "last_activity": None,
        "total_searches": 0,
        "total_views": 0
    }
}

app_state = {}

def load_state():
    """Carga estado de la aplicación"""
    global app_state
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            app_state = json.load(f)
    else:
        app_state = DEFAULT_STATE.copy()
        app_state["session"]["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_state()

def save_state():
    """Guarda estado de la aplicación"""
    with open(STATE_FILE, 'w') as f:
        json.dump(app_state, f, indent=4)

def get_state(key):
    """Obtiene valor del estado"""
    return app_state.get(key)

def set_state(key, value):
    """Establece valor del estado"""
    app_state[key] = value
    save_state()

def update_state(updates):
    """Actualiza múltiples valores del estado"""
    app_state.update(updates)
    save_state()

def reset_state():
    """Resetea estado de la aplicación"""
    global app_state
    app_state = DEFAULT_STATE.copy()
    app_state["session"]["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state()

def clear_state():
    """Limpia estado temporal"""
    app_state["search_results"] = []
    app_state["current_movie"] = None
    app_state["current_series"] = None
    save_state()

def add_to_favorites(movie):
    """Agrega película a favoritas"""
    if "favorites" not in app_state:
        app_state["favorites"] = []
    
    # Verificar duplicados
    exists = False
    for fav in app_state["favorites"]:
        if fav.get("Title") == movie.get("Title"):
            exists = True
            break
    
    if not exists:
        app_state["favorites"].append(movie)
        save_state()
        return True
    return False

def remove_from_favorites(title):
    """Elimina película de favoritas"""
    if "favorites" not in app_state:
        return False
    
    for i in range(len(app_state["favorites"])):
        if app_state["favorites"][i].get("Title") == title:
            app_state["favorites"].pop(i)
            save_state()
            return True
    return False

def get_favorites():
    """Obtiene favoritas"""
    return app_state.get("favorites", [])

def add_to_history(item):
    """Agrega al historial"""
    if "history" not in app_state:
        app_state["history"] = []
    
    item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app_state["history"].append(item)
    save_state()

def clear_history():
    """Limpia historial"""
    app_state["history"] = []
    save_state()

def get_history():
    """Obtiene historial"""
    return app_state.get("history", [])

def set_current_user(user):
    """Establece usuario actual"""
    app_state["current_user"] = user
    save_state()

def get_current_user():
    """Obtiene usuario actual"""
    return app_state.get("current_user")

def logout():
    """Cierra sesión"""
    app_state["current_user"] = None
    save_state()

def update_session_stats(searches=None, views=None):
    """Actualiza estadísticas de sesión"""
    if "session" not in app_state:
        app_state["session"] = {}
    
    if searches is not None:
        app_state["session"]["total_searches"] = app_state["session"].get("total_searches", 0) + searches
    
    if views is not None:
        app_state["session"]["total_views"] = app_state["session"].get("total_views", 0) + views
    
    app_state["session"]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state()

def get_session_stats():
    """Obtiene estadísticas de sesión"""
    return app_state.get("session", {})

def set_ui_state(key, value):
    """Establece estado de UI"""
    if "ui_state" not in app_state:
        app_state["ui_state"] = {}
    
    app_state["ui_state"][key] = value
    save_state()

def get_ui_state(key):
    """Obtiene estado de UI"""
    return app_state.get("ui_state", {}).get(key)

def export_state(filename):
    """Exporta estado"""
    with open(filename, 'w') as f:
        json.dump(app_state, f, indent=4)

def import_state(filename):
    """Importa estado"""
    global app_state
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            app_state = json.load(f)
        save_state()
        return True
    return False

def validate_state():
    """Valida estado de la aplicación"""
    errors = []
    
    required_keys = ["favorites", "history", "session"]
    for key in required_keys:
        if key not in app_state:
            errors.append("Missing state key: " + key)
    
    if "session" in app_state:
        session = app_state["session"]
        if "start_time" not in session:
            errors.append("Missing session start_time")
    
    return errors

def get_state_summary():
    """Obtiene resumen del estado"""
    return {
        "total_favorites": len(app_state.get("favorites", [])),
        "total_history": len(app_state.get("history", [])),
        "current_user": app_state.get("current_user"),
        "session_stats": app_state.get("session", {})
    }

def backup_state():
    """Crea backup del estado"""
    backup_name = "state_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_state(backup_name)
    return backup_name

def restore_state(backup_name):
    """Restaura estado desde backup"""
    return import_state(backup_name)

# Cargar estado al importar
load_state()
