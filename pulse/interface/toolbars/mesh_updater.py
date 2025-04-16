from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class MeshUpdater:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()

    def _initialize(self):

        self.element_size = 0.01
        self.geometry_tolerance = 1e-6
        self.non_mapped_bcs = list()

        self.complete = False
        self.create = False
        self.stop = False
        self.t0 = 0

    def set_project_attributes(self, element_size, geometry_tolerance):

        self.element_size = element_size
        self.geometry_tolerance = geometry_tolerance

        app().project.file.modify_project_attributes(
                                                    element_size = element_size, 
                                                    geometry_tolerance = geometry_tolerance
                                                    )

    def get_mesh_attributes_from_project_file(self):

        if app().project.file is None:
            return None, None

        project_setup = app().project.file.read_project_setup_from_file()
        if project_setup is None:
            return None, None

        element_size = None
        geometry_tolerance = None

        if "mesher_setup" in project_setup.keys():

            mesh_setup = project_setup["mesher_setup"]
            keys = mesh_setup.keys()

            if 'element_size' in keys:
                element_size = mesh_setup['element_size']

            if 'geometry_tolerance' in keys:
                geometry_tolerance = mesh_setup['geometry_tolerance']

        return element_size, geometry_tolerance

    def process_mesh_and_load_project(self):

        if app().project.file.check_pipeline_data():
            self.current_element_size, self.current_geometry_tolerance = self.get_mesh_attributes_from_project_file()
            # app().project.file.modify_project_attributes(element_size=self.element_size, geometry_tolerance=self.geometry_tolerance)
            app().project.loader.load_mesh_setup_from_file()
            app().project.initial_load_project_actions()
            app().project.loader.load_project_data()
            app().project.loader.load_mesh_dependent_properties()
            app().main_window.initial_project_action(True)
            app().main_window.update_plots()  
            self.complete = True

    def undo_mesh_actions(self):

        self.t0 = time()

        element_size = self.current_element_size
        geometry_tolerance = self.current_geometry_tolerance

        self.set_project_attributes(element_size, geometry_tolerance)

        app().main_window.mesh_toolbar.lineEdit_element_size.setText(str(element_size))
        app().main_window.mesh_toolbar.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))

        app().project.loader.load_mesh_setup_from_file()
        app().project.initial_load_project_actions()
        app().project.loader.load_project_data()
        app().project.loader.load_mesh_dependent_properties()
        app().main_window.update_plots()