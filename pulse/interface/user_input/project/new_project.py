from PyQt5.QtWidgets import QComboBox, QDialog, QFrame, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

import os
from time import time

window_title = "Error"

class NewProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/new_project_input2.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().main_window.project
        self.preprocessor = app().project.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):
        self.stop = False
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("New project")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_length_unit : QComboBox
        self.comboBox_start_project : QComboBox

        # QFrame
        self.frame_geometry_file : QFrame
        self.frame_element_size : QFrame
        self.frame_geometry_tolerance : QFrame

        # QLabel
        self.label_element_size : QLabel
        self.label_geometry_tolerance : QLabel

        # QLineEdit
        self.lineEdit_geometry_path : QLineEdit
        self.lineEdit_element_size : QLineEdit
        self.lineEdit_geometry_tolerance : QLineEdit

        # QPushButton
        self.pushButton_import_geometry : QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_start_project : QPushButton

    def _create_connections(self):
        #
        self.comboBox_start_project.currentIndexChanged.connect(self.update_available_inputs)
        self.comboBox_length_unit.currentIndexChanged.connect(self.update_unit_length_event)
        #
        self.pushButton_start_project.clicked.connect(self.start_project)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_import_geometry.clicked.connect(self.import_geometry)
        self.update_available_inputs()

    def update_unit_length_event(self):

        unit = self.comboBox_length_unit.currentText().replace(" ", "")

        if unit == "millimeter":
            label = "mm"
        elif unit == "inch":
            label = "in"
        else:
            label = "m"

        self.label_element_size.setText(f"Element size: [{label}]")
        self.label_geometry_tolerance.setText(f"Geometry tolerance: [{label}]")

    def update_available_inputs(self):
        index = self.comboBox_start_project.currentIndex()
        if index == 0:
            self.pushButton_import_geometry.setDisabled(False)
        elif index == 1:
            self.pushButton_import_geometry.setDisabled(True)

    def import_geometry(self):

        last_geometry_file = app().main_window.config.get_last_folder_for("geometry folder")

        if last_geometry_file is None:
            suggested_path = str(Path().home())
        else:
            suggested_path = last_geometry_file

        geometry_path, check = QFileDialog.getOpenFileName(
                                                            None, 
                                                            'Open file', 
                                                            suggested_path, 
                                                            'Files (*.iges *.igs *.step *.stp)'
                                                            )

        if check:
            self.lineEdit_geometry_path.setText(geometry_path)
            app().main_window.config.write_last_folder_path_in_file("geometry folder", geometry_path)

    def check_project_inputs(self):
        
        if self.comboBox_start_project.currentIndex() == 0:
            if self.lineEdit_geometry_path.text() == "":
                title = 'Empty geometry at selection'
                message = "Please, select a valid *.iges or *.step format geometry to continue."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True
        
        if self.lineEdit_element_size.text() == "":
            title = 'Empty element size'
            message = "Please, inform a valid input to the element size."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        else:
            try:
                self.element_size = float(self.lineEdit_element_size.text())
            except Exception:
                title = 'Invalid element size'
                message = "Please, inform a valid input to the element size."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True

        if self.lineEdit_geometry_tolerance.text() == "":
            title = 'Empty geometry tolerance'
            message = "Please, inform a valid input to the geometry tolerance."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        else:
            try:
                self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
            except Exception:
                title = 'Invalid geometry tolerance'
                message = "Please, inform a valid input to the geometry tolerance."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True

    def create_project(self):

        try:

            import_type = self.comboBox_start_project.currentIndex()
            self.create_project_file(import_type)

            self.project.reset(reset_all=True)
            app().project.model.mesh.set_mesher_setup(mesh_setup=self.setup_data)

            if import_type == 1:
                app().project.model.mesh._create_gmsh_geometry()
            else:
                self.project.process_geometry_and_mesh()

        except Exception as error_log:

            window_title = "Error"
            title = "Error while creating new project"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            
            return True

    def create_project_file(self, import_type : int):

        self.length_unit = self.comboBox_length_unit.currentText().replace(" ", "")

        self.setup_data = { 
                            "length unit" : self.length_unit,
                            "element size" : self.element_size,
                            "geometry tolerance" : self.geometry_tolerance,
                            "import type" : import_type,
                           }

        geometry_path = ""
        self.geometry_filename = ""

        if import_type == 0:
            geometry_path = self.lineEdit_geometry_path.text()
            self.geometry_filename = os.path.basename(geometry_path)
            self.setup_data["geometry filename"] = self.geometry_filename

        app().pulse_file.write_project_setup_in_file(
                                                                    self.setup_data,
                                                                    geometry_path = geometry_path
                                                                )
        
        # self.project.set_project_setup(self.setup_data)
        
        if import_type == 0:
            self.setup_data["geometry path"] = app().pulse_file.read_geometry_from_file()

    def start_project(self):
        t0 = time()

        if self.check_project_inputs():
            return

        if self.stop:
            self.project.time_to_load_or_create_project = 0
            return
   
        if self.create_project():
            return
        
        app().main_window._update_recent_projects()
        app().main_window.set_window_title("New project (*)")
        
        if self.comboBox_start_project.currentIndex() == 1:
            app().main_window.action_plot_geometry_editor_callback()
        
        else:
            app().main_window.use_structural_setup_workspace()
        
        app().main_window.update_plots()

        self.project.time_to_load_or_create_project = time() - t0
        self.complete = True
        
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.start_project()
        elif event.key() == Qt.Key_Escape:
            self.close()