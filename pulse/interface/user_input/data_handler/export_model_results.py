from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse import UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput


class ExportModelResults(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "data_handler/export_model_results.ui"
        uic.loadUi(ui_path, self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

    def _load_icons(self):
        self.pulse_icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.userPath = os.path.expanduser('~')
        self.save_path = ""
        self.data = dict()

    def _define_qt_variables(self):
        # QLabel
        self.label_data_information : QLabel
        # QLineEdit
        self.lineEdit_file_name : QLineEdit
        self.lineEdit_save_results_path : QLineEdit
        # QPushButton
        self.pushButton_choose_folder_export : QPushButton
        self.pushButton_export_results : QPushButton

    def _create_connections(self):
        self.pushButton_choose_folder_export.clicked.connect(self._choose_path_export_results)
        self.pushButton_export_results.clicked.connect(self._export_results)

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _set_data_to_export(self, data):
        self.data = data
        if len(data) > 0:
            self._load_data_information()
            self.exec()

    def _load_data_information(self):
        if "data_information" in self.data.keys():
            text = "Data information: "
            text += self.data["data_information"]
            self.label_data_information.setText(text)
            self.lineEdit_file_name.setFocus()

    def _choose_path_export_results(self):
        
        if self.save_path == "":
            _path = self.userPath
        else:
            _path = self.save_path

        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', _path)
        self.save_name = os.path.basename(self.save_path)
        self.lineEdit_save_results_path.setText(str(self.save_path))

    def _export_results(self):
        window_title = "ERROR MESSAGE"
        if self.lineEdit_file_name.text() != "":
            if self.save_path == "":
                title = "None folder selected"
                message = "Plese, choose a folder before trying export the results."
                PrintMessageInput([window_title, title, message])
                return
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the results."
            PrintMessageInput([window_title, title, message])
            return

        file_name = self.lineEdit_file_name.text() + ".dat"
        self.export_path = os.path.join(self.save_path, file_name)
        
        if "x_data" in self.data.keys():
            x_data = self.data["x_data"]
        if "y_data" in self.data.keys():
            y_data = self.data["y_data"]
        if "unit" in self.data.keys():
            unit = self.data["unit"]
        
        header = ("Frequency[Hz], Real part [{}], Imaginary part [{}], Absolute [{}]").format(unit, unit, unit)
        data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T      
   
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        
        window_title = "Warning"
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([window_title, title, message], auto_close=True)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._export_results()
        elif event.key() == Qt.Key_Escape:
            self.close()