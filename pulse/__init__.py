__version__ = '1.0.2'
__release_date__ = 'Oct 19th 2022'

from PyQt5.QtWidgets import QApplication


def app() -> "Application":
    return QApplication.instance()
