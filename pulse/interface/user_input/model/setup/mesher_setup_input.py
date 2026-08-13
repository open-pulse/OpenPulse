import logging

from PySide6.QtCore import Qt

from pulse import app
from pulse.interface import warning_title
from pulse.interface.ui_generated.model.setup.mesh.mesher_setup_input_ui import MesherSetupInput_UI
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.utils.interface_utils import check_inputs
from pulse.interface.user_input.project.print_message import PrintMessageInput


class MesherSetupInput(MesherSetupInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._configure_window()
        self._configure_validators()
        self._create_connections()
        self.exec()

    @property
    def mesh(self):
        return app().project.model.mesh

    def _configure_window(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint
        )
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse")
        self.setWindowIcon(app().main_window.pulse_icon)

    def _initialize(self):
        self.lineEdit_element_size.setFocus()
        self.cache_save_path = app().project.save_path
        self.cache_element_size = self.mesh.mesher_setup.element_size
        self.cache_geometry_tolerance = self.mesh.mesher_setup.geometry_tolerance

    def _configure_validators(self):
        self.lineEdit_element_size.setValidator(StrictDoubleValidator(1e-8, 1e6, 8))
        self.lineEdit_geometry_tolerance.setValidator(StrictDoubleValidator(1e-12, 10, 8))

    def _create_connections(self):
        #
        self.pushbutton_cancel.clicked.connect(self.close)
        self.pushbutton_apply.clicked.connect(self.generate_mesh_callback)
        self.pushbutton_apply_and_close.clicked.connect(lambda: self.generate_mesh_callback(close_window=True))
        #
        self.load_project_mesh_settings()

    def load_project_mesh_settings(self):

        mesher_setup = self.mesh.mesher_setup
        element_size = mesher_setup.element_size
        geometry_tolerance = mesher_setup.geometry_tolerance
 
        if isinstance(element_size, float):
            self.lineEdit_element_size.setText(str(element_size))

        if isinstance(geometry_tolerance, float):
            self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))

    def has_mesh_configuration_changed(self):
        if self.lineEdit_element_size.text() == "":
            return False

        if self.lineEdit_geometry_tolerance.text() == "":
            return False

        new_element_size = float(self.lineEdit_element_size.text())
        new_geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        
        mesher_setup = self.mesh.mesher_setup
        current_element_size = mesher_setup.element_size
        current_geometry_tolerance = mesher_setup.geometry_tolerance

        return (new_element_size != current_element_size) or (new_geometry_tolerance != current_geometry_tolerance)

    def generate_mesh_callback(self, close_window: bool = False):

        element_size = check_inputs(self.lineEdit_element_size, "'Element size'")
        if element_size is None:
            self.lineEdit_element_size.setFocus()
            return

        geometry_tolerance = check_inputs(self.lineEdit_geometry_tolerance, "'Geometry tolerance'")
        if geometry_tolerance is None:
            self.lineEdit_geometry_tolerance.setFocus()
            return

        if not self.has_mesh_configuration_changed():
            self.hide()
            title = "The same mesh configuration was detected"
            message = "You are trying to generate a mesh without changing its configuration, and as a result, the mesh will not "
            message += "be updated. In order to modify the current mesh state, you should change the current configuration."
            PrintMessageInput([warning_title, title, message])
            self.show()
            return

        app().main_window.reset_solution()

        def generate_mesh():
            logging.info("Setting project attributes... [25%]")
            project_setup = app().project.project_setup
            mesher_setup = project_setup.mesher_setup
            mesher_setup.element_size = element_size
            mesher_setup.geometry_tolerance = geometry_tolerance
            app().project.set_project_setup(project_setup)
            app().project.file.modify_project_attributes(project_setup)

            logging.info("Processing the mesh... [75%]")
            self.process_mesh_and_load_project()

            # TODO: remove as soon as possible
            app().main_window.action_results_workspace.setDisabled(True)

            logging.info("The mesh was successfully generated. [100%]")

        self.hide()
        LoadingWindow(generate_mesh, parent=self).run()
        self.show()

        if close_window:
            self.close()

    def process_mesh_and_load_project(self):

        if not app().project.file.check_pipeline_data():
            return

        app().project.loader.load_project_setup_from_file()
        app().project.initial_load_project_actions()
        app().project.loader.load_project_data()
        app().project.loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        app().main_window.update_plots()
        app().main_window.update_status_bar_info()

        app().project.save_path = self.cache_save_path

    def undo_mesh_actions(self):
        project_setup = app().project.project_setup
        mesher_setup = project_setup.mesher_setup
        mesher_setup.element_size = self.cache_element_size
        mesher_setup.geometry_tolerance = self.cache_geometry_tolerance
        app().project.set_project_setup(project_setup)
        app().project.file.modify_project_attributes(project_setup)
        app().project.loader.load_project_setup_from_file()
        app().project.initial_load_project_actions()
        app().project.loader.load_project_data()
        app().project.loader.load_mesh_dependent_properties()
        app().main_window.update_plots()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_mesh_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

        return super().keyPressEvent(event)