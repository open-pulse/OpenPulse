from PySide6.QtWidgets import QComboBox, QDialog, QFrame, QFileDialog, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

import os
from pathlib import Path
from time import time

window_title = "Error"

class NewProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/new_project_input2.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)
        self.project = app().main_window.project
        self.preprocessor = app().project.model.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.stop = False
        self.complete = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

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
        #
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

        self.hide()
        last_geometry_file = app().main_window.config.get_last_folder_for("geometry_folder")

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

            app().main_window.config.write_last_folder_path_in_file("geometry_folder", geometry_path)

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

            mesher_setup = self.create_project_file()

            self.project.reset(reset_all = True)
            app().project.model.mesh.set_mesher_setup(mesher_setup = mesher_setup)

            if self.comboBox_start_project.currentIndex() == 1:
                app().project.model.mesh._create_gmsh_geometry()
            else:
                self.project.process_geometry_and_mesh()

        except Exception as error_log:

            app().project.model.mesh.set_mesher_setup()
            app().main_window.reset_temporary_folder()
            app().project.model.mesh._create_gmsh_geometry()

            window_title = "Error"
            title = "Error while creating new project"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            
            return True

    def create_project_file(self):

        self.length_unit = self.comboBox_length_unit.currentText().replace(" ", "")
        import_type = self.comboBox_start_project.currentIndex()

        setup_data = { 
                      "length_unit" : self.length_unit,
                      "element_size" : self.element_size,
                      "geometry_tolerance" : self.geometry_tolerance,
                      "import_type" : import_type,
                      }

        geometry_path = ""
        self.geometry_filename = ""

        if import_type == 0:
            geometry_path = self.lineEdit_geometry_path.text()
            self.geometry_filename = os.path.basename(geometry_path)
            setup_data["geometry_filename"] = self.geometry_filename

        app().project.file.write_project_setup_in_file(setup_data, geometry_path = geometry_path)
        
        if import_type == 0:
            setup_data["geometry_path"] = app().project.file.read_geometry_from_file()

        return setup_data

    def start_project(self):

        self.hide()

        if self.check_project_inputs():
            return

        if self.stop:
            return

        if self.create_project():
            return
        
        app().main_window._update_recent_projects()
        app().main_window.set_window_title("New project (*)")
        
        if self.comboBox_start_project.currentIndex() == 1:
            app().main_window.action_plot_geometry_editor_callback()
        
        else:
            app().main_window.use_model_setup_workspace()

        app().main_window.update_plots()

        self.complete = True

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.start_project()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)