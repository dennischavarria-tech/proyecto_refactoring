import csv
import json
import os
import random
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, Union

from constants import DIRECTORIES, MOVIE_FIELDS, NA_VALUE


RESULTS_DIR: str = DIRECTORIES["results"]
EXPORT_DIR: str = DIRECTORIES["exports"]


def init_dirs() -> None:
    for d in (RESULTS_DIR, EXPORT_DIR):
        if not os.path.exists(d):
            os.makedirs(d)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_separator(char: str = "=", length: int = 60) -> None:
    print(char * length)


def print_header(text: str) -> None:
    print_separator()
    print(text.upper().center(60))
    print_separator()


def print_subheader(text: str) -> None:
    print_separator("-", 40)
    print(text.center(40))
    print_separator("-", 40)


def delay(seconds: float) -> None:
    time.sleep(seconds)


def get_user_input(prompt: str, input_type: Type = str) -> Any:
    while True:
        try:
            user_input = input(prompt)
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            return user_input
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")


def format_movie_display(movie: Optional[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("=" * 50)

    if movie is None:
        lines.append("No se encontró la película")
        lines.append("=" * 50)
        return "\n".join(lines)

    for field in MOVIE_FIELDS:
        label = field
        if field == "imdbRating":
            label = "Rating IMDB"
        lines.append(f"{label}: {movie.get(field, NA_VALUE)}")

    lines.append("=" * 50)
    return "\n".join(lines)


def format_series_display(series: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("=" * 50)

    show = series.get("show", series)

    lines.append(f"Nombre: {show.get('name', NA_VALUE)}")
    lines.append(f"Idioma: {show.get('language', NA_VALUE)}")
    lines.append(f"Géneros: {show.get('genres', [])}")
    lines.append(f"Rating: {show.get('rating', {}).get('average', NA_VALUE)}")
    lines.append(f"Estado: {show.get('status', NA_VALUE)}")
    lines.append(f"Estreno: {show.get('premiered', NA_VALUE)}")
    lines.append(f"Final: {show.get('ended', NA_VALUE)}")
    lines.append(f"Episodios: {show.get('runtime', NA_VALUE)}")

    summary = str(show.get("summary", NA_VALUE))
    if len(summary) > 200:
        summary = summary[:200] + "..."
    lines.append(f"Resumen: {summary}")

    lines.append("=" * 50)
    return "\n".join(lines)


def format_list_display(items: List[Dict[str, Any]], item_type: str = "pelicula") -> str:
    lines: List[str] = []

    if len(items) == 0:
        lines.append(f"No se encontraron {item_type}s")
        return "\n".join(lines)

    for i, item in enumerate(items):
        if "titulo" in item:
            lines.append(f"{i + 1}. {item['titulo']} ({item.get('anio', '')})")
        elif "Title" in item:
            lines.append(f"{i + 1}. {item['Title']} ({item.get('Year', NA_VALUE)})")
        elif "name" in item:
            lines.append(f"{i + 1}. {item['name']}")
        else:
            lines.append(f"{i + 1}. Elemento desconocido")

    return "\n".join(lines)


def save_results(results: Any, filename: str) -> str:
    filepath = os.path.join(RESULTS_DIR, filename)
    with open(filepath, "w") as f:
        if isinstance(results, list):
            for item in results:
                f.write(f"{item}\n")
        else:
            f.write(str(results))
    return filepath


def export_to_json(data: Any, filename: str) -> str:
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return filepath


def export_to_csv(data: Any, filename: str) -> str:
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, "w", newline="") as f:
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    return filepath


def create_menu(options: List[str]) -> None:
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Salir")


def handle_menu_choice(choice: int, handlers: Dict[int, Callable[[], None]]) -> bool:
    if choice in handlers:
        handlers[choice]()
        return True
    elif choice == 0:
        return False
    else:
        print("Opción inválida")
        return True


def generate_random_id() -> str:
    return str(random.randint(1000, 9999))


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def validate_email(email: str) -> bool:
    return "@" in email and "." in email


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_date(date_obj: Any) -> str:
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return str(date_obj)


def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def remove_duplicates(items: List[Any]) -> List[Any]:
    unique_items: List[Any] = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items


def sort_items(items: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    try:
        return sorted(items, key=lambda x: x.get(key, ""), reverse=reverse)
    except (TypeError, AttributeError):
        return items


def filter_items(items: List[Dict[str, Any]], key: str, value: Any) -> List[Dict[str, Any]]:
    return [item for item in items if item.get(key) == value]


init_dirs()
