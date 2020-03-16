from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDirModel, QTreeView, QToolBar, QSplitter, QFrame, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit, QDialog, QDialogButtonBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from PyQt5 import uic

class CrossInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/cross.ui', self)
        self.exec_()
        
        # self.setWindowTitle("Set Cross Section")
        
        # QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.buttonBox)
        # self.setLayout(self.layout)
        