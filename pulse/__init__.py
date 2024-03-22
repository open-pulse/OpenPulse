# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.application import Application

import pkg_resources

# copying the version from pyproject.toml
__version__ = pkg_resources.get_distribution('pulse').version
__release_date__ = 'Apr 30th 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path

OPEN_PULSE_DIR = Path(__file__).parent
UI_DIR = OPEN_PULSE_DIR / "interface/ui_files/"
SYMBOLS_DIR = OPEN_PULSE_DIR / "interface/data/symbols/"

def app() -> "Application":
    return QApplication.instance()