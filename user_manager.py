import os
import json
import time
from datetime import datetime

# Variables globales
USER_FILE = "users.json"
current_user = None

users = []

def load_users():
    """Carga usuarios"""
    global users
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = []

def save_users():
    """Guarda usuarios"""
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def create_user(username, password, email=None):
    """Crea usuario"""
    # Verificar si existe
    for user in users:
        if user["username"] == username:
            return False, "Usuario ya existe"
    
    new_user = {
        "username": username,
        "password": password,  # No hasheada (mala práctica)
        "email": email,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": None,
        "preferences": {
            "theme": "dark",
            "language": "es",
            "notifications": True
        }
    }
    
    users.append(new_user)
    save_users()
    return True, "Usuario creado"

def authenticate_user(username, password):
    """Autentica usuario"""
    global current_user
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            current_user = user
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_users()
            return True, user
    
    return False, "Credenciales inválidas"

def logout_user():
    """Cierra sesión"""
    global current_user
    current_user = None

def get_current_user():
    """Obtiene usuario actual"""
    return current_user

def update_user(username, updates):
    """Actualiza usuario"""
    for user in users:
        if user["username"] == username:
            user.update(updates)
            save_users()
            return True
    return False

def delete_user(username):
    """Elimina usuario"""
    global users
    
    for i in range(len(users)):
        if users[i]["username"] == username:
            users.pop(i)
            save_users()
            return True
    return False

def get_user(username):
    """Obtiene usuario por nombre"""
    for user in users:
        if user["username"] == username:
            return user
    return None

def get_all_users():
    """Obtiene todos los usuarios"""
    return users.copy()

def search_users(query):
    """Busca usuarios"""
    results = []
    query_lower = query.lower()
    
    for user in users:
        if query_lower in user["username"].lower():
            results.append(user)
    
    return results

def get_users_count():
    """Obtiene número de usuarios"""
    return len(users)

def update_user_preferences(username, preferences):
    """Actualiza preferencias de usuario"""
    for user in users:
        if user["username"] == username:
            user["preferences"].update(preferences)
            save_users()
            return True
    return False

def get_user_preferences(username):
    """Obtiene preferencias de usuario"""
    user = get_user(username)
    if user:
        return user.get("preferences", {})
    return {}

def export_users(filename):
    """Exporta usuarios"""
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)

def import_users(filename):
    """Importa usuarios"""
    global users
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        for user in imported:
            if not any(u["username"] == user["username"] for u in users):
                users.append(user)
        
        save_users()
        return True
    return False

def validate_user(username, password):
    """Valida usuario"""
    errors = []
    
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    
    if len(password) < 6:
        errors.append("Password must be at least 6 characters")
    
    return errors

def get_user_stats():
    """Obtiene estadísticas de usuarios"""
    stats = {
        "total": len(users),
        "active": 0,
        "inactive": 0
    }
    
    for user in users:
        if user.get("last_login"):
            stats["active"] += 1
        else:
            stats["inactive"] += 1
    
    return stats

def backup_users():
    """Crea backup de usuarios"""
    backup_name = "users_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_users(backup_name)
    return backup_name

def restore_users(backup_name):
    """Restaura usuarios desde backup"""
    return import_users(backup_name)

def validate_users_integrity():
    """Valida integridad de usuarios"""
    errors = []
    
    for i, user in enumerate(users):
        if "username" not in user:
            errors.append("User " + str(i) + " missing username")
        if "password" not in user:
            errors.append("User " + str(i) + " missing password")
    
    return errors

# Cargar usuarios al importar
load_users()
