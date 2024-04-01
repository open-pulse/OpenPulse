from PyQt5.QtWidgets import QCheckBox, QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pathlib import Path

class ResetProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/reset_project.ui"
        uic.loadUi(ui_path, self)

        self.project = app().main_window.project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_windows()
        self._create_connections()
        self._define_qt_variables()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_windows(self):    
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # QCheckBox
        self.reset_fluids_checkbox : QCheckBox
        self.reset_materials_checkbox : QCheckBox
        self.reset_acoustic_model_checkbox : QCheckBox
        self.reset_structural_model_checkbox : QCheckBox
        self.reset_analysis_setup_checkbox : QCheckBox
        # QPushButton
        self.cancel_button : QPushButton
        self.reset_project_button : QPushButton
        warning_message = "Warning: this process will be irreversible once the button has been pressed."
        self.reset_project_button.setToolTip(warning_message)

    def _create_connections(self):
        self.reset_project_button.clicked.connect(self.project_resetting_callback)
        self.cancel_button.clicked.connect(self.close)

    def get_reset_config(self):
        reset_config = {"reset_fluids" : self.reset_fluids_checkbox.isChecked(),
                        "reset_materials" : self.reset_materials_checkbox.isChecked(),
                        "reset_acoustic_model" : self.reset_acoustic_model_checkbox.isChecked(),
                        "reset_structural_model" : self.reset_structural_model_checkbox.isChecked(),
                        "reset_analysis_setup" : self.reset_analysis_setup_checkbox.isChecked()}
        return reset_config

    def project_resetting_callback(self):
        self.close()
        reset_config = self.get_reset_config()
        self.project.reset_project(**reset_config)
        self.opv.opvRenderer.plot()
        self.opv.plot_mesh()
        self.print_final_message()
    
    def print_final_message(self):
        window_title = "Warning"
        title = "Project resetting complete"
        message = "The current project setup and project data "
        message += "has been reset to default values."
        PrintMessageInput([window_title, title, message], auto_close=True)