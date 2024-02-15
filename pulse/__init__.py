__version__ = '2.0.0'
__release_date__ = 'Apr 30th 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path


UI_DIR = Path('pulse/interface/ui_files/')


def app() -> "Application":
    return QApplication.instance()
