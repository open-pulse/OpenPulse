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
ICON_DIR = OPEN_PULSE_DIR / "interface/data/icons/"
QSS_DIR = OPEN_PULSE_DIR / "interface/data/qss_files/"
UI_DIR = OPEN_PULSE_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = OPEN_PULSE_DIR / "interface/data/symbols/"
   
USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_pulse"
TEMP_PROJECT_FILE = str(TEMP_PROJECT_DIR / "tmp.pulse") 

def app() -> "Application":
    return QApplication.instance()