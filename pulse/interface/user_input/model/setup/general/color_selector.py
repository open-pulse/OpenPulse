from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from pathlib import Path

from pulse.interface.formatters.icons import *

class PickColorInput(QColorDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title = kwargs.get("title", "")

        self._load_icon()
        self._config_window()
        self._initialize()
        self.exec()

    def _load_icon(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setFixedSize(QSize(540, 410))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(self.icon) 
        self.setWindowTitle(self.title)
    
    def _initialize(self):
        self.color = [] 
        self.complete = False  
        self.colorSelected.connect(self.confirm_color)   

    def confirm_color(self):
        color = self.currentColor().getRgb()
        self.complete = True
        self.color = list(color[0:3])
        self.close()
     
    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()