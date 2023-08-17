from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from pathlib import Path

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

class PickColorInput(QColorDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 

        self.color = [] 
        self.complete = False  
        self.colorSelected.connect(self.confirm_color)   
        self.configWindow()
        self.exec()
        
    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def confirm_color(self):
        color = self.currentColor().getRgb()
        self.complete = True
        self.color = list(color[0:3])
        self.close()

    def configWindow(self):
        self.setWindowTitle("Get color")
        self.setMinimumSize(QSize(540, 410))
        self.setMaximumSize(QSize(540, 410))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)
        # self.setGeometry(QRect(400, 400, 400, 400))