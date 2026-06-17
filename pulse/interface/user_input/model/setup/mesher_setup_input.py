from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.formatters import icons
from pulse.interface.toolbars.mesh_updater import MeshUpdater
from pulse.interface.ui_generated.model.setup.mesh.mesher_setup_input_ui import MesherSetupInput_UI
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.utils.interface_utils import check_inputs


class MesherSetupInput(MesherSetupInput_UI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        
        self.project = app().main_window.project
        self.mesh_updater = MeshUpdater()

        self._initialize()
        self._configure_window()
        self._configure_validators()
        self._create_connections()

        self.exec()

    def _configure_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("OpenPulse")
        self.setWindowIcon(icons.get_openpulse_icon())
    
    def _initialize(self):
        self.get_mesh_attributes_from_project_file()

        self.element_size = float(self.lineEdit_element_size.text())
        self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
    
    def  _configure_validators(self):
        self.lineEdit_element_size.setValidator(StrictDoubleValidator(1e-8, 1e6, 8))
        self.lineEdit_geometry_tolerance.setValidator(StrictDoubleValidator(1e-12, 10, 8))

    def _create_connections(self):
        self.pushbutton_cancel.clicked.connect(self.close)
        self.pushbutton_apply.clicked.connect(self.generate_mesh_callback)
        self.pushbutton_apply_and_close.clicked.connect(self.generate_mesh_and_close)

        self.lineEdit_element_size.textChanged.connect(self.mesh_attributes_changed)
        self.lineEdit_geometry_tolerance.textChanged.connect(self.mesh_attributes_changed)
    
    def generate_mesh_callback(self):
        if self.check_input_values():
            return

        self.mesh_updater.set_project_attributes(self.element_size, self.geometry_tolerance)
        self.mesh_updater.process_mesh_and_load_project()
        self.mesh_attributes_changed()

        # TODO: remove as soon as possible
        app().main_window.action_results_workspace.setDisabled(True)
    
    def generate_mesh_and_close(self):
        self.generate_mesh_callback()
        self.close()
    
    def check_input_values(self):
        self.element_size = check_inputs(self.lineEdit_element_size, "'Element size'")
        if self.element_size is None:
            self.lineEdit_element_size.setFocus()
            return True
        
        self.geometry_tolerance = check_inputs(self.lineEdit_geometry_tolerance, "'Geometry tolerance'")
        if self.geometry_tolerance is None:
            self.lineEdit_geometry_tolerance.setFocus()
            return True
    
    def mesh_attributes_changed(self):
        current_element_size, current_geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

        try:
            _element_size = float(self.lineEdit_element_size.text())
            _geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except Exception:
            return
        
        if bool(_element_size) and bool(_geometry_tolerance):

            if _element_size != current_element_size:
                return

            if _geometry_tolerance != current_geometry_tolerance:
                return
    
    def get_mesh_attributes_from_project_file(self):
        element_size, geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

        if element_size is not None:
            self.lineEdit_element_size.setText(str(element_size))

        if geometry_tolerance is not None:
            self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
