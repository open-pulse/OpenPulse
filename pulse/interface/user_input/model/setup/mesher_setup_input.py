import logging

from PySide6.QtCore import Qt

from pulse import app
from pulse.interface import warning_title
from pulse.interface.toolbars.mesh_updater import MeshUpdater
from pulse.interface.ui_generated.model.setup.mesh.mesher_setup_input_ui import MesherSetupInput_UI
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.utils.interface_utils import check_inputs
from pulse.interface.user_input.project.print_message import PrintMessageInput


class MesherSetupInput(MesherSetupInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.mesh_updater = MeshUpdater()

        self._configure_window()

        self._initialize()
        self._configure_validators()
        self._create_connections()

        self.exec()

    def _configure_window(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint
        )
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse")
        self.setWindowIcon(app().main_window.pulse_icon)

    def _initialize(self):
        self.element_size = None
        self.geometry_tolerance = None

    def _configure_validators(self):
        self.lineEdit_element_size.setValidator(StrictDoubleValidator(1e-8, 1e6, 8))
        self.lineEdit_geometry_tolerance.setValidator(StrictDoubleValidator(1e-12, 10, 8))

    def _create_connections(self):
        self.pushbutton_cancel.clicked.connect(self.close)
        self.pushbutton_apply.clicked.connect(self.generate_mesh_callback)
        self.pushbutton_apply_and_close.clicked.connect(lambda: self.generate_mesh_callback(close_window=True))
        #
        self.load_project_mesh_settings()

    def load_project_mesh_settings(self):
        element_size, geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

        if isinstance(element_size, float):
            self.lineEdit_element_size.setText(str(element_size))

        if isinstance(geometry_tolerance, float):
            self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))

    def check_input_values(self):
        self.element_size = check_inputs(self.lineEdit_element_size, "'Element size'")
        if self.element_size is None:
            self.lineEdit_element_size.setFocus()
            return True

        self.geometry_tolerance = check_inputs(self.lineEdit_geometry_tolerance, "'Geometry tolerance'")
        if self.geometry_tolerance is None:
            self.lineEdit_geometry_tolerance.setFocus()
            return True

    def has_mesh_configuration_changed(self):
        if self.lineEdit_element_size.text() == "":
            return False

        if self.lineEdit_geometry_tolerance.text() == "":
            return False

        new_element_size = float(self.lineEdit_element_size.text())
        new_geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        current_element_size, current_geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

        return (new_element_size != current_element_size) or (new_geometry_tolerance != current_geometry_tolerance)

    def generate_mesh_callback(self, close_window: bool = False):

        if self.check_input_values():
            return

        if not self.has_mesh_configuration_changed():
            self.hide()
            title = "The same mesh configuration was detected"
            message = "You are trying to generate a mesh without changing its configuration, and as a result, the mesh will not "
            message += "be updated. In order to modify the current mesh state, you should change the current configuration."
            PrintMessageInput([warning_title, title, message])
            self.show()
            return

        def generate_mesh():
            logging.info("Setting project attributes... [25%]")
            self.mesh_updater.set_project_attributes(self.element_size, self.geometry_tolerance)

            logging.info("Processing the mesh... [75%]")
            self.mesh_updater.process_mesh_and_load_project()

            # TODO: remove as soon as possible
            app().main_window.action_results_workspace.setDisabled(True)

            logging.info("The mesh was successfully generated. [100%]")

        self.hide()
        LoadingWindow(generate_mesh, parent=self).run()
        self.show()

        if close_window:
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.generate_mesh_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

        return super().keyPressEvent(event)