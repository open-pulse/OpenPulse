# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.interface.application import Application

from PySide6.QtWidgets import QApplication
from molde import Color
from pathlib import Path

__version__ = "2.0.11"
__release_date__ = 'Jul 2026'

VERSION = __version__
RELEASE_DATE = __release_date__

OPEN_PULSE_DIR = Path(__file__).parent
ICON_DIR = OPEN_PULSE_DIR / "interface/data/icons/"
QSS_DIR = OPEN_PULSE_DIR / "interface/data/qss_files/"
UI_DIR = OPEN_PULSE_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = OPEN_PULSE_DIR / "interface/data/symbols/"
EXAMPLES_DIR = OPEN_PULSE_DIR / "interface/data/examples/"
FONT_DIR = OPEN_PULSE_DIR / "interface/data/fonts/"
   
USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_pulse"

LIGHT_ICON_COLOR = Color("#0051A2")
DARK_ICON_COLOR = Color("#84AAFF")

def app() -> "Application":
    '''
    Returns the instance of the current application.
    '''
    return QApplication.instance()
