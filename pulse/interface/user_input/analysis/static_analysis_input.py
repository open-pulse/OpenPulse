from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.analysis.structural.static_analysis_ui import StaticAnalysis_UI
from pulse.model import AnalysisID


class StaticAnalysisInput(StaticAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self.project = app().project
        self.model = app().project.model
        
        self._config_window()
        self._initialize()

        self._create_connections()
        self._load_current_state()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.setup_defined = False
        self.proceed_solution = False

        # self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)
        self.gravity_vector = app().project.model.gravity_vector

    def _create_connections(self):
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)

    def _load_current_state(self):
        self.checkBox_self_weight_load.setChecked(app().project.model.weight_load)
        self.checkBox_internal_pressure_load.setChecked(app().project.model.internal_pressure_load)
        self.checkBox_external_nodal_loads.setChecked(app().project.model.external_nodal_loads)
        self.checkBox_distributed_element.setChecked(app().project.model.element_distributed_load)

    def enter_setup_callback(self):

        weight_load = self.checkBox_self_weight_load.isChecked()
        internal_pressure_load = self.checkBox_internal_pressure_load.isChecked()
        external_nodal_load = self.checkBox_external_nodal_loads.isChecked()
        distributed_load = self.checkBox_distributed_element.isChecked()

        analysis_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText().lower()

        analysis_setup = { 
            "analysis_id" : AnalysisID.STRUCTURAL_STATIC,
            "analysis_type" : "static",
            "analysis_domain" : analysis_domain,
            "weight_load" : weight_load,
            "internal_pressure_load" : internal_pressure_load,
            "external_pressure_load" : external_nodal_load,
            "distributed_load" : distributed_load
            }

        app().project.model.set_analysis_setup(analysis_setup)
        app().project.file.write_analysis_setup_in_file(analysis_setup)

        self.setup_defined = True
        self.close()

    def run_analysis_callback(self):
        self.enter_setup_callback()
        self.confirm()

    def confirm(self):
        self.proceed_solution = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()