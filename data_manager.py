import json
import os
import csv
from datetime import datetime

# Variables globales
DATA_DIR = "data"
BACKUP_DIR = "backups"
DATA_FILE = os.path.join(DATA_DIR, "datos.json")
BACKUP_FILE = os.path.join(BACKUP_DIR, "backup_{}.json")

def init_data_dir():
    """Inicializa directorios de datos"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def load_data():
    """Carga datos desde archivo"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"peliculas": [], "series": [], "favoritas": [], "historial": []}

def save_data(data):
    """Guarda datos a archivo"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_movie(movie_data):
    """Agrega película"""
    data = load_data()
    data["peliculas"].append(movie_data)
    save_data(data)

def add_series(series_data):
    """Agrega serie"""
    data = load_data()
    data["series"].append(series_data)
    save_data(data)

def add_favorite(favorite_data):
    """Agrega favorita"""
    data = load_data()
    data["favoritas"].append(favorite_data)
    save_data(data)

def remove_favorite(title):
    """Elimina favorita"""
    data = load_data()
    new_favorites = []
    for fav in data["favoritas"]:
        if fav.get("titulo") != title and fav.get("Title") != title:
            new_favorites.append(fav)
    data["favoritas"] = new_favorites
    save_data(data)

def add_to_history(history_data):
    """Agrega al historial"""
    data = load_data()
    history_data["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["historial"].append(history_data)
    save_data(data)

def clear_history():
    """Limpia historial"""
    data = load_data()
    data["historial"] = []
    save_data(data)

def get_all_movies():
    """Obtiene todas las películas"""
    data = load_data()
    return data.get("peliculas", [])

def get_all_series():
    """Obtiene todas las series"""
    data = load_data()
    return data.get("series", [])

def get_all_favorites():
    """Obtiene todas las favoritas"""
    data = load_data()
    return data.get("favoritas", [])

def get_history():
    """Obtiene historial"""
    data = load_data()
    return data.get("historial", [])

def search_movies(query):
    """Busca películas por título"""
    movies = get_all_movies()
    results = []
    query_lower = query.lower()
    
    for movie in movies:
        title = movie.get("titulo", movie.get("Title", "")).lower()
        if query_lower in title:
            results.append(movie)
    
    return results

def search_series(query):
    """Busca series por nombre"""
    series = get_all_series()
    results = []
    query_lower = query.lower()
    
    for s in series:
        name = s.get("nombre", s.get("name", "")).lower()
        if query_lower in name:
            results.append(s)
    
    return results

def create_backup():
    """Crea backup de datos"""
    data = load_data()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = BACKUP_FILE.format(timestamp)
    
    with open(backup_filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return backup_filename

def restore_backup(backup_file):
    """Restaura backup"""
    if os.path.exists(backup_file):
        with open(backup_file, 'r') as f:
            data = json.load(f)
        save_data(data)
        return True
    return False

def list_backups():
    """Lista backups disponibles"""
    backups = []
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            if filename.endswith(".json"):
                backups.append(filename)
    return backups

def export_to_csv(filename):
    """Exporta datos a CSV"""
    data = load_data()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Encabezados
        writer.writerow(["Tipo", "Título", "Año", "Rating", "Género"])
        
        # Películas
        for movie in data.get("peliculas", []):
            writer.writerow([
                "Película",
                movie.get("titulo", movie.get("Title", "")),
                movie.get("anio", movie.get("Year", "")),
                movie.get("rating", movie.get("imdbRating", "")),
                movie.get("genero", movie.get("Genre", ""))
            ])
        
        # Series
        for series in data.get("series", []):
            writer.writerow([
                "Serie",
                series.get("nombre", series.get("name", "")),
                "",
                series.get("rating", ""),
                series.get("genero", "")
            ])

def import_from_csv(filename):
    """Importa datos desde CSV"""
    data = load_data()
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row["Tipo"] == "Película":
                movie = {
                    "titulo": row["Título"],
                    "anio": row["Año"],
                    "rating": row["Rating"],
                    "genero": row["Género"]
                }
                data["peliculas"].append(movie)
            elif row["Tipo"] == "Serie":
                series = {
                    "nombre": row["Título"],
                    "rating": row["Rating"],
                    "genero": row["Género"]
                }
                data["series"].append(series)
    
    save_data(data)

def get_stats():
    """Obtiene estadísticas de datos"""
    data = load_data()
    
    return {
        "total_peliculas": len(data.get("peliculas", [])),
        "total_series": len(data.get("series", [])),
        "total_favoritas": len(data.get("favoritas", [])),
        "total_historial": len(data.get("historial", []))
    }

def clear_all_data():
    """Limpia todos los datos"""
    data = {
        "peliculas": [],
        "series": [],
        "favoritas": [],
        "historial": []
    }
    save_data(data)

def delete_data_file():
    """Elimina archivo de datos"""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

def get_data_size():
    """Obtiene tamaño del archivo de datos"""
    if os.path.exists(DATA_FILE):
        return os.path.getsize(DATA_FILE)
    return 0

def validate_data():
    """Valida integridad de datos"""
    data = load_data()
    errors = []
    
    required_keys = ["peliculas", "series", "favoritas", "historial"]
    for key in required_keys:
        if key not in data:
            errors.append("Falta clave: " + key)
        elif not isinstance(data[key], list):
            errors.append("Clave " + key + " no es lista")
    
    return errors

# Inicializar directorios
init_data_dir()
