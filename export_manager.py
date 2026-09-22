import os
import json
import csv
from datetime import datetime

# Variables globales
EXPORT_DIR = "exports"
IMPORT_DIR = "imports"

def init_dirs():
    """Inicializa directorios"""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    if not os.path.exists(IMPORT_DIR):
        os.makedirs(IMPORT_DIR)

def export_to_json(data, filename):
    """Exporta datos a JSON"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filepath

def import_from_json(filename):
    """Importa datos desde JSON"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    return None

def export_to_csv(data, filename):
    """Exporta datos a CSV"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            return filepath
    
    return None

def import_from_csv(filename):
    """Importa datos desde CSV"""
    filepath = os.path.join(EXPORT_DIR, filename)
    data = []
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    
    return data

def export_to_txt(data, filename):
    """Exporta datos a TXT"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    with open(filepath, 'w') as f:
        if isinstance(data, list):
            for item in data:
                f.write(str(item) + "\n")
        else:
            f.write(str(data))
    
    return filepath

def import_from_txt(filename):
    """Importa datos desde TXT"""
    filepath = os.path.join(EXPORT_DIR, filename)
    data = []
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                data.append(line.strip())
    
    return data

def list_exports():
    """Lista archivos de exportación"""
    files = []
    
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    "name": filename,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                })
    
    return files

def delete_export(filename):
    """Elimina archivo de exportación"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    
    return False

def get_export_info(filename):
    """Obtiene información de exportación"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    if os.path.exists(filepath):
        stat = os.stat(filepath)
        return {
            "name": filename,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return None

def copy_export(filename, destination):
    """Copia exportación a otra ubicación"""
    source_path = os.path.join(EXPORT_DIR, filename)
    dest_path = os.path.join(destination, filename)
    
    if os.path.exists(source_path):
        import shutil
        shutil.copy2(source_path, dest_path)
        return True
    
    return False

def move_export(filename, destination):
    """Mueve exportación a otra ubicación"""
    source_path = os.path.join(EXPORT_DIR, filename)
    dest_path = os.path.join(destination, filename)
    
    if os.path.exists(source_path):
        import shutil
        shutil.move(source_path, dest_path)
        return True
    
    return False

def create_backup(backup_name=None):
    """Crea backup de todas las exportaciones"""
    if backup_name is None:
        backup_name = "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    
    backup_path = os.path.join(EXPORT_DIR, backup_name)
    all_exports = {}
    
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as f:
                    all_exports[filename] = f.read()
    
    with open(backup_path, 'w') as f:
        json.dump(all_exports, f, indent=4)
    
    return backup_path

def restore_backup(backup_name):
    """Restaura backup de exportaciones"""
    backup_path = os.path.join(EXPORT_DIR, backup_name)
    
    if os.path.exists(backup_path):
        with open(backup_path, 'r') as f:
            all_exports = json.load(f)
        
        for filename, content in all_exports.items():
            filepath = os.path.join(EXPORT_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        return True
    
    return False

def get_total_export_size():
    """Obtiene tamaño total de exportaciones"""
    total_size = 0
    
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    
    return total_size

def export_data_report(data, filename):
    """Exporta reporte de datos"""
    filepath = os.path.join(EXPORT_DIR, filename)
    
    with open(filepath, 'w') as f:
        f.write("REPORTE DE DATOS\n")
        f.write("=" * 50 + "\n")
        f.write("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 50 + "\n\n")
        
        if isinstance(data, dict):
            for key, value in data.items():
                f.write(key.upper() + ":\n")
                f.write("-" * 30 + "\n")
                if isinstance(value, list):
                    for item in value:
                        f.write("  - " + str(item) + "\n")
                else:
                    f.write("  " + str(value) + "\n")
                f.write("\n")
        else:
            f.write(str(data) + "\n")
    
    return filepath

# Inicializar directorios
init_dirs()
