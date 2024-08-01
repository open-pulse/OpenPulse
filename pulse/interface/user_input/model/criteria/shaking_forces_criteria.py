from PyQt5.QtWidgets import QDialog, QCheckBox, QFileDialog, QLabel, QLineEdit, QPushButton, QTableWidget, QTabWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.tools.utils import get_new_path

import os

window_title_1 = "Error"
window_title_2 = "Warning"

class ShakingForcesCriteriaInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "criterias/shaking_forces_criteria_widget.ui"
        uic.loadUi(ui_path, self)
        
        self.project = app().project
        self.opv = app().main_window.opv_widget
        app().main_window.input_ui.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        # self._config_widgets()

        # while self.keep_window_open:
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_force_Fx : QCheckBox
        self.checkBox_force_Fy : QCheckBox
        self.checkBox_force_Fz : QCheckBox
        self.checkBox_resultant_force : QCheckBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.process_shaking_forces_for_selected_lines)
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_entities = app().main_window.selected_entities
        if selected_entities:
            text = ", ".join([str(i) for i in selected_entities])
            self.lineEdit_selection_id.setText(text)

    def process_shaking_forces_for_selected_lines(self):
        print("pushButton pressed")
        pass