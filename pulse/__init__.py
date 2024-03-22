import pkg_resources

# copying the version from pyproject.toml
__version__ = pkg_resources.get_distribution('pulse').version
__release_date__ = 'Apr 30th 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path

OPEN_PULSE_DIR = Path(__file__).parent
UI_DIR = OPEN_PULSE_DIR / "interface/ui_files/"
SYMBOLS_DIR = OPEN_PULSE_DIR / "interface/data/symbols/"

print(f"{SYMBOLS_DIR = }")

def app() -> "Application":
    return QApplication.instance()