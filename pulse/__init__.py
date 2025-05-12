# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.application import Application

from PySide6.QtWidgets import QApplication
from pathlib import Path

OPEN_PULSE_DIR = Path(__file__).parent
ICON_DIR = OPEN_PULSE_DIR / "interface/data/icons/"
QSS_DIR = OPEN_PULSE_DIR / "interface/data/qss_files/"
UI_DIR = OPEN_PULSE_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = OPEN_PULSE_DIR / "interface/data/symbols/"
EXAMPLES_DIR = OPEN_PULSE_DIR / "interface/data/examples/"
FONT_DIR = OPEN_PULSE_DIR / "interface/data/fonts/"
   
USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_pulse"
TEMP_PROJECT_FILE = str(TEMP_PROJECT_DIR / "tmp.pulse")

def app() -> "Application":
    '''
    Returns the instance of the current application.
    '''
    return QApplication.instance()

def version() -> str:
    '''
    Returns the version of the software available in pyproject.toml
    '''
    return "2.0.11"

def release_date() -> str:
    '''
    Returns a string containing the release date
    '''
    return 'Sep 30th 2024'
