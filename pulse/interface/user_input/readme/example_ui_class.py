from PyQt5.QtWidgets import QDialog, QCheckBox, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np


window_title_1 = "Error"
window_title_2 = "Warning"

class NomeDaClasse(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "nome_do_ui_path.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # Defina as variáveis do Qt
        # QLineEdit
        self.lineEdit : QLineEdit
        # QPushButton
        self.pushButton : QPushButton

    def _create_connections(self):
        # Crie as conexões
        self.pushButton.clicked.connect(self.pushButton_callback)

    def _config_widgets(self):
        # Configure os widgets, caso necessário
        self.pushButton.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")

    def pushButton_callback(self):
        print("O botão foi acionado!")