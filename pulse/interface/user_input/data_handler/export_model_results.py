from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse import UI_DIR
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class ExportModelResults(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "data_handler/export_model_results.ui", self)

        self._config_window()
        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Import data to compare")

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.search_icon = QIcon(get_icons_path('searchFile.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))
        self.setWindowIcon(self.pulse_icon)

    def _reset_variables(self):
        self.userPath = os.path.expanduser('~')
        self.save_path = ""
        self.data = dict()

    def _define_qt_variables(self):
        # QLabel
        self.label_data_information = self.findChild(QLabel, 'label_data_information')
        # QLineEdit
        self.lineEdit_file_name = self.findChild(QLineEdit, 'lineEdit_file_name')
        self.lineEdit_save_results_path = self.findChild(QLineEdit, 'lineEdit_save_results_path')
        # QPushButton
        self.pushButton_choose_folder_export = self.findChild(QPushButton, 'pushButton_choose_folder_export')
        self.pushButton_export_results = self.findChild(QPushButton, 'pushButton_export_results')
        self.pushButton_reset_filename = self.findChild(QPushButton, 'pushButton_reset_filename')
        self.pushButton_choose_folder_export.setIcon(self.search_icon)
        self.pushButton_reset_filename.setIcon(self.update_icon)

    def _create_connections(self):
        self.pushButton_choose_folder_export.clicked.connect(self._choose_path_export_results)
        self.pushButton_export_results.clicked.connect(self._export_results)
        self.pushButton_reset_filename.clicked.connect(self._reset_file_name)

    def _reset_file_name(self):
        self.lineEdit_file_name.setText("")
        self.lineEdit_file_name.setFocus()

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
                PrintMessageInput([title, message, window_title])
                return
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the results."
            PrintMessageInput([title, message, window_title])
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
        PrintMessageInput([title, message, window_title])
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._export_results()
        elif event.key() == Qt.Key_Escape:
            self.close()