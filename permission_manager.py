import os
import json
import time
from datetime import datetime

# Variables globales
PERMISSION_FILE = "permissions.json"
permissions = {}

def load_permissions():
    """Carga permisos"""
    global permissions
    
    if os.path.exists(PERMISSION_FILE):
        with open(PERMISSION_FILE, 'r') as f:
            permissions = json.load(f)
    else:
        permissions = {}

def save_permissions():
    """Guarda permisos"""
    with open(PERMISSION_FILE, 'w') as f:
        json.dump(permissions, f, indent=4)

def add_permission(role, permission_list):
    """Agrega permisos a un rol"""
    permissions[role] = {
        "role": role,
        "permissions": permission_list,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_permissions()

def remove_permission(role):
    """Elimina permisos de un rol"""
    if role in permissions:
        del permissions[role]
        save_permissions()
        return True
    return False

def get_permission(role):
    """Obtiene permisos de un rol"""
    return permissions.get(role)

def get_all_permissions():
    """Obtiene todos los permisos"""
    return permissions.copy()

def add_role_permission(role, permission):
    """Agrega un permiso a un rol"""
    if role in permissions:
        if permission not in permissions[role]["permissions"]:
            permissions[role]["permissions"].append(permission)
            save_permissions()
            return True
    return False

def remove_role_permission(role, permission):
    """Elimina un permiso de un rol"""
    if role in permissions:
        if permission in permissions[role]["permissions"]:
            permissions[role]["permissions"].remove(permission)
            save_permissions()
            return True
    return False

def has_permission(role, permission):
    """Verifica si un rol tiene un permiso"""
    if role in permissions:
        return permission in permissions[role]["permissions"]
    return False

def get_roles_with_permission(permission):
    """Obtiene roles con un permiso específico"""
    roles = []
    
    for role, info in permissions.items():
        if permission in info["permissions"]:
            roles.append(role)
    
    return roles

def search_permissions(query):
    """Busca permisos"""
    results = {}
    query_lower = query.lower()
    
    for role, info in permissions.items():
        if query_lower in role.lower():
            results[role] = info
    
    return results

def clear_permissions():
    """Limpia permisos"""
    global permissions
    permissions = {}
    save_permissions()

def get_permission_stats():
    """Obtiene estadísticas de permisos"""
    stats = {
        "total_roles": len(permissions),
        "total_permissions": 0,
        "avg_permissions_per_role": 0
    }
    
    for info in permissions.values():
        stats["total_permissions"] += len(info.get("permissions", []))
    
    if len(permissions) > 0:
        stats["avg_permissions_per_role"] = stats["total_permissions"] / len(permissions)
    
    return stats

def export_permissions(filename):
    """Exporta permisos"""
    with open(filename, 'w') as f:
        json.dump(permissions, f, indent=4)

def import_permissions(filename):
    """Importa permisos"""
    global permissions
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            permissions = json.load(f)
        save_permissions()
        return True
    return False

def validate_permissions():
    """Valida integridad de permisos"""
    errors = []
    
    for role, info in permissions.items():
        if "role" not in info:
            errors.append("Role " + role + " missing role field")
        if "permissions" not in info:
            errors.append("Role " + role + " missing permissions")
    
    return errors

def backup_permissions():
    """Crea backup de permisos"""
    backup_name = "permissions_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_permissions(backup_name)
    return backup_name

def restore_permissions(backup_name):
    """Restaura permisos desde backup"""
    return import_permissions(backup_name)

def get_permissions_summary():
    """Obtiene resumen de permisos"""
    return {
        "total_roles": len(permissions),
        "roles": list(permissions.keys())
    }

# Cargar permisos al importar
load_permissions()
