# fmt: off

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
from pathlib import Path


class ImportGeometry():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window

        self._initialize()
        self.import_geometry()

    def _initialize(self):
        self.complete = False

    def import_geometry(self):

        last_path = app().config.get_last_folder_for("geometry_folder")
        if last_path is None:
            last_path = str(Path().home())

        geometry_path, check = app().main_window.file_dialog.get_open_file_name(
                                                                                'Import geometry file', 
                                                                                last_path, 
                                                                                'Files (*.iges *.igs *.step *.stp)'
                                                                                )

        if not check:
            return

        app().main_window.config.write_last_folder_path_in_file("geometry_folder", geometry_path)

        filename = os.path.basename(geometry_path)
        app().project.file.modify_project_attributes(import_type = 0, geometry_filename = filename)

        self.save_geometry_and_load_project(geometry_path)

    def save_geometry_and_load_project(self, geometry_path: str):
        #
        project_setup = app().project.file.read_project_setup_from_file()
        mesher_setup = project_setup["mesher_setup"]
        #
        app().project.file.write_project_setup_in_file(mesher_setup, geometry_path = geometry_path)
        mesher_setup["geometry_path"] = app().project.file.read_geometry_from_file()
        #
        app().project.reset(reset_all = True)
        app().project.loader.load_project_data()
        app().project.model.mesh.set_mesher_setup(mesher_setup = mesher_setup)
        #
        app().project.process_geometry_and_mesh()
        app().project.loader.load_mesh_dependent_properties()
        app().project.model.preprocessor.check_disconnected_lines()
        #
        app().main_window.use_model_setup_workspace()
        app().main_window.update_plots()
        self.complete = True

# fmt: on