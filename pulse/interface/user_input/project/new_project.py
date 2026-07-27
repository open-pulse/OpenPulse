import os
from copy import deepcopy
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import app
from pulse.interface.ui_generated.project.new_project_input_ui import NewProjectInput_UI
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.data_classes.project_setup_data_classes import ImportType, MesherSetup, ProjectSetup

window_title = "Error"

class NewProjectInput(NewProjectInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.project = app().main_window.project
        self.preprocessor = app().project.model.preprocessor

        self._config_window()
        self._initialize()
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
        index_type = self.comboBox_start_project.currentIndex()
        self.pushButton_import_geometry.setEnabled(index_type == ImportType.CAD_FILE)

    def import_geometry(self):

        self.hide()
        last_geometry_file = app().main_window.config.get_last_folder_for("geometry_folder")

        if last_geometry_file is None:
            suggested_path = str(Path().home())
        else:
            suggested_path = last_geometry_file

        extensions = ["iges", "igs", "step", "stp"]
        geometry_path = FileDialogService.open_file(extensions, last_folder=suggested_path)

        if geometry_path is None:
            return
        
        self.lineEdit_geometry_path.setText(str(geometry_path))
        app().main_window.config.write_last_folder_path_in_file("geometry_folder", geometry_path)

    def check_project_inputs(self):
        
        if self.comboBox_start_project.currentIndex() == ImportType.CAD_FILE:
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
            app().main_window.reset_temporary_folder()
            self.project.model.properties._reset_variables()
            self.project.reset_project(reset_all=True)

            project_setup = self.create_project_setup()

            app().project.model.set_project_setup(project_setup)
            app().project.file.modify_project_attributes(project_setup)

            if self.comboBox_start_project.currentIndex() == ImportType.BUILT_IN:
                app().project.model.mesh._create_gmsh_geometry()
            else:
                self.project.model.process_geometry_and_mesh()

        except Exception as error_log:

            app().project.model.mesh.set_mesher_setup(MesherSetup())
            app().main_window.reset_temporary_folder()
            app().project.model.mesh._create_gmsh_geometry()

            window_title = "Error"
            title = "Error while creating new project"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            
            return True

    def create_project_setup(self) -> ProjectSetup:

        self.length_unit = self.comboBox_length_unit.currentText().replace(" ", "")
        import_type = self.comboBox_start_project.currentIndex()

        mesh_setup = MesherSetup(self.element_size, self.geometry_tolerance, self.length_unit)
        project_setup = ProjectSetup(import_type, mesher_setup=mesh_setup)

        if import_type == ImportType.CAD_FILE:
            geometry_path_source = self.lineEdit_geometry_path.text()
            geometry_filename = os.path.basename(geometry_path_source)
        else:
            geometry_filename = ""
            geometry_path_source = ""

        project_setup.geometry_filename = geometry_filename
        project_setup.geometry_path_source = geometry_path_source

        app().project.file.write_project_setup_in_file(project_setup.as_dict())

        if import_type == ImportType.CAD_FILE:
            project_setup.geometry_path_internal = app().project.file.read_geometry_from_file()

        return project_setup

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
        app().main_window.update_status_bar_info()

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