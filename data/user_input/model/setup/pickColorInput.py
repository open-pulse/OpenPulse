import os
from os.path import basename
from PyQt5.QtWidgets import QDialog, QColorDialog, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QSize, QRect, QPoint, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

class PickColorInput(QColorDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)  
        self.color = [] 
        self.complete = False  
        self.colorSelected.connect(self.confirm_color)   
        self.configWindow()
        self.exec_()
        
    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def confirm_color(self):
        color = self.currentColor().getRgb()
        self.complete = True
        self.color = color[0:3] 
        self.close()

    def configWindow(self):
        self.setWindowTitle("Get color")
        self.setMinimumSize(QSize(540, 410))
        self.setMaximumSize(QSize(540, 410))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)
        # self.setGeometry(QRect(400, 400, 400, 400))