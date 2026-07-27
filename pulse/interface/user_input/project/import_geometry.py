from copy import deepcopy
from pathlib import Path

from pulse import app
from pulse.interface import error_title
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.data_classes.project_setup_data_classes import ImportType, ProjectSetup
from pulse.utils.geometry_validator import format_validation_error, validate_geometry_file


class ImportGeometry:
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

        extensions = ["iges", "igs", "step", "stp"]
        geometry_path = FileDialogService.open_file(extensions, "Import geometry file", last_path)

        if geometry_path is None:
            return

        result = validate_geometry_file(geometry_path)
        if not result.is_valid:
            title = "Unsupported geometry entities"
            message = format_validation_error(result)
            PrintMessageInput(["Error", title, message])
            return

        app().main_window.config.write_last_folder_path_in_file("geometry_folder", geometry_path)

        project_setup = deepcopy(app().project.project_setup)
        project_setup.import_type = ImportType.CAD_FILE
        project_setup.geometry_filename = geometry_path.name

        original_setup_dict = app().project.file.read_project_setup_from_file()
        original_project_setup = deepcopy(app().project.project_setup)

        app().project.set_project_setup(project_setup)
        app().project.file.modify_project_attributes(project_setup)

        try:
            self.save_geometry_and_load_project(project_setup)
        except Exception as error_log:
            app().project.file.write_project_setup_in_file(original_setup_dict)
            app().project.set_project_setup(original_project_setup)
            title = "Error while importing geometry"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return

        app().main_window.use_model_setup_workspace()
        app().main_window.update_plots()
        app().main_window.update_status_bar_info()

        self.complete = True

    def save_geometry_and_load_project(self, project_setup: ProjectSetup):
        #
        app().project.reset(reset_all=True)
        app().project.loader.load_project_data()
        app().project.model.mesh.set_mesher_setup(project_setup.mesher_setup)
        #
        app().project.model.process_geometry_and_mesh()
        app().project.loader.load_mesh_dependent_properties()
        app().project.model.preprocessor.check_disconnected_lines()
