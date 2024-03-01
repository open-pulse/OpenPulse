from PyQt5.QtWidgets import QDialog, QFrame, QComboBox, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.tools.utils import get_new_path

import os
from pathlib import Path


class ExportGeometry(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/project/export_geometry_file.ui")
        uic.loadUi(ui_path, self)
        
        self.main_window = app().main_window
        self.opv = self.main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = self.main_window.project
        self.file = self.project.file
        self.config = self.main_window.config

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_qt_actions()
        self.update_project_directory()
        self.exec()

    def _initialize(self):

        self.complete = False
        self.folder_path = ""

        user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # QFrame
        self.frame_filename = self.findChild(QFrame, 'frame_filename')
        self.frame_directory = self.findChild(QFrame, 'frame_directory')
        # QLineEdit
        self.lineEdit_geometry_filename = self.findChild(QLineEdit, 'lineEdit_geometry_filename')
        self.lineEdit_directory_to_export = self.findChild(QLineEdit, 'lineEdit_directory_to_export')
        self.lineEdit_geometry_filename.setClearButtonEnabled(True)
        self.lineEdit_geometry_filename.setPlaceholderText("< Insert a filename >")
        self.lineEdit_directory_to_export.setText(self.desktop_path)
        # self.focus_lineEdit_geometry_filename_if_blank()
        # QPushButton
        self.pushButton_search_folder = self.findChild(QPushButton, 'pushButton_search_folder')
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_export = self.findChild(QPushButton, 'pushButton_export')

    def _create_qt_actions(self):
        self.clickable(self.lineEdit_geometry_filename).connect(self.lineEdit_clicked)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_export.clicked.connect(self.export_geometry)
        self.pushButton_search_folder.clicked.connect(self.search_folder)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_clicked(self):
        pass

    def check_inputs(self):
        window_title = "Error"
        if self.lineEdit_geometry_filename.text() == "":
            self.lineEdit_geometry_filename.setFocus()
            title = 'Empty project name'
            message = "Please, inform a valid project name to continue."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        
        if self.lineEdit_directory_to_export.text() == "":
            title = 'None project folder selected'
            message = "Please, select a folder where the project data are going to be stored."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True

        # if not os.path.exists(self.project_directory):
        #     os.mkdir(self.project_directory)

    def focus_lineEdit_geometry_filename_if_blank(self):
        if self.lineEdit_geometry_filename.text() == "":
            self.lineEdit_geometry_filename.setFocus()

    def update_project_directory(self):
        if self.folder_path != "":
            self.lineEdit_directory_to_export.setText(str(self.folder_path))
        else:
            self.folder_path = self.desktop_path

    def search_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the cad file', self.desktop_path)
        self.update_project_directory()

    def export_geometry(self):

        if self.check_inputs():
            return

        build_data = self.file.load_segment_build_data_from_file()
        self.geometry_handler = GeometryHandler()
        pipeline = self.geometry_handler.process_pipeline(build_data)
        self.geometry_handler.set_length_unit(self.file.length_unit)
        self.geometry_handler.set_pipeline(pipeline)

        filename = self.lineEdit_geometry_filename.text() + ".step"
        path = get_new_path(self.folder_path, filename)
        self.geometry_handler.export_cad_file(path)
        self.close()
        self.print_user_message()

    def print_user_message(self):
        window_title = "OpenPulse"
        title = "Geometry exported"
        message = "The geometry file has been exported."
        PrintMessageInput([window_title, title, message], auto_close=True)