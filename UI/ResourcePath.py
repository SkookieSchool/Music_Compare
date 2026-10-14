import sys
from pathlib import Path


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).resolve().parent

    return str(Path(base_path) / relative_path)