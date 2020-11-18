import sys
import os
import platform
from PyQt5 import Qt, QtCore, QtWidgets

from pulse.uix.mainWindow import MainWindow

def init():
    #If are using Windows with HighDPI active, this'll set the scale to 100%
    #But the screen and text'll be blurry
    if platform.system() == "Windows":
        sys.argv.append("--platform")
        sys.argv.append("windows:dpiawareness=0")
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
init()