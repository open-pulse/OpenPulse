__version__ = '2.0.0'
__release_date__ = 'Apr 30th 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path

OPEN_PULSE_DIR = Path(__file__).parent
UI_DIR = OPEN_PULSE_DIR / "interface/ui_files/"

def app() -> "Application":
    return QApplication.instance()