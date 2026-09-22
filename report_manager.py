import os
import json
import time
from datetime import datetime

# Variables globales
REPORT_FILE = "reports.json"
reports = []

def load_reports():
    """Carga reportes"""
    global reports
    
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'r') as f:
            reports = json.load(f)
    else:
        reports = []

def save_reports():
    """Guarda reportes"""
    with open(REPORT_FILE, 'w') as f:
        json.dump(reports, f, indent=4)

def create_report(report_info):
    """Crea reporte"""
    report = {
        "id": len(reports) + 1,
        "title": report_info.get("title", "Sin título"),
        "type": report_info.get("type", "general"),
        "content": report_info.get("content", ""),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "generated": False,
        "file_path": None
    }
    reports.append(report)
    save_reports()
    return report["id"]

def delete_report(report_id):
    """Elimina reporte"""
    for i in range(len(reports)):
        if reports[i]["id"] == report_id:
            reports.pop(i)
            save_reports()
            return True
    return False

def update_report(report_id, updates):
    """Actualiza reporte"""
    for report in reports:
        if report["id"] == report_id:
            report.update(updates)
            save_reports()
            return True
    return False

def get_report(report_id):
    """Obtiene reporte"""
    for report in reports:
        if report["id"] == report_id:
            return report
    return None

def get_all_reports():
    """Obtiene todos los reportes"""
    return reports.copy()

def get_reports_by_type(report_type):
    """Obtiene reportes por tipo"""
    filtered = []
    for report in reports:
        if report.get("type") == report_type:
            filtered.append(report)
    return filtered

def search_reports(query):
    """Busca reportes"""
    results = []
    query_lower = query.lower()
    
    for report in reports:
        if query_lower in report.get("title", "").lower():
            results.append(report)
    
    return results

def generate_report(report_id):
    """Genera reporte"""
    for report in reports:
        if report["id"] == report_id:
            report["generated"] = True
            report["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_reports()
            return True
    return False

def clear_reports():
    """Limpia reportes"""
    global reports
    reports = []
    save_reports()

def get_report_stats():
    """Obtiene estadísticas de reportes"""
    stats = {
        "total": len(reports),
        "generated": 0,
        "pending": 0,
        "by_type": {}
    }
    
    for report in reports:
        if report.get("generated"):
            stats["generated"] += 1
        else:
            stats["pending"] += 1
        
        report_type = report.get("type", "unknown")
        stats["by_type"][report_type] = stats["by_type"].get(report_type, 0) + 1
    
    return stats

def export_reports(filename):
    """Exporta reportes"""
    with open(filename, 'w') as f:
        json.dump(reports, f, indent=4)

def import_reports(filename):
    """Importa reportes"""
    global reports
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reports = json.load(f)
        save_reports()
        return True
    return False

def validate_reports():
    """Valida integridad de reportes"""
    errors = []
    
    for i, report in enumerate(reports):
        if "id" not in report:
            errors.append("Report " + str(i) + " missing id")
        if "title" not in report:
            errors.append("Report " + str(i) + " missing title")
    
    return errors

def backup_reports():
    """Crea backup de reportes"""
    backup_name = "reports_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    export_reports(backup_name)
    return backup_name

def restore_reports(backup_name):
    """Restaura reportes desde backup"""
    return import_reports(backup_name)

def get_reports_summary():
    """Obtiene resumen de reportes"""
    return {
        "total": len(reports),
        "generated_count": len([r for r in reports if r.get("generated")]),
        "types": list(set(r.get("type", "") for r in reports if r.get("type")))
    }

# Cargar reportes al importar
load_reports()
