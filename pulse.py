import sys
from PyQt5 import Qt

from pulse.uix.mainWindow import MainWindow

def init():
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
init()