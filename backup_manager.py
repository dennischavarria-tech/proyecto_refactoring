import os
import json
import time
from datetime import datetime

# Variables globales
BACKUP_DIR = "backups"
MAX_BACKUPS = 10

def init_backup_dir():
    """Inicializa directorio de backups"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_backup(data, backup_name=None):
    """Crea backup de datos"""
    if backup_name is None:
        backup_name = "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    with open(backup_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Limpiar backups antiguos
    cleanup_old_backups()
    
    return backup_path

def restore_backup(backup_name):
    """Restaura backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if os.path.exists(backup_path):
        with open(backup_path, 'r') as f:
            return json.load(f)
    
    return None

def list_backups():
    """Lista backups disponibles"""
    backups = []
    
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(BACKUP_DIR, filename)
                stat = os.stat(filepath)
                backups.append({
                    "name": filename,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                })
    
    return sorted(backups, key=lambda x: x["created"], reverse=True)

def delete_backup(backup_name):
    """Elimina backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if os.path.exists(backup_path):
        os.remove(backup_path)
        return True
    
    return False

def cleanup_old_backups():
    """Limpia backups antiguos"""
    backups = list_backups()
    
    if len(backups) > MAX_BACKUPS:
        for backup in backups[MAX_BACKUPS:]:
            delete_backup(backup["name"])

def get_backup_info(backup_name):
    """Obtiene información de backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if os.path.exists(backup_path):
        stat = os.stat(backup_path)
        return {
            "name": backup_name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return None

def backup_exists(backup_name):
    """Verifica si existe backup"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    return os.path.exists(backup_path)

def get_total_backup_size():
    """Obtiene tamaño total de backups"""
    total_size = 0
    
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    
    return total_size

def export_backup(backup_name, export_path):
    """Exporta backup a ubicación externa"""
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if os.path.exists(backup_path):
        with open(backup_path, 'r') as f:
            data = json.load(f)
        
        with open(export_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    
    return False

def import_backup(import_path, backup_name=None):
    """Importa backup desde ubicación externa"""
    if os.path.exists(import_path):
        with open(import_path, 'r') as f:
            data = json.load(f)
        
        if backup_name is None:
            backup_name = "imported_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
        
        return create_backup(data, backup_name)
    
    return None

# Inicializar directorio
init_backup_dir()
