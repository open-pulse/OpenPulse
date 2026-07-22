import logging
from typing import Literal

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QToolBar, QWidget

from pulse import app
from pulse.interface.formatters.icons import Icon
from pulse.interface.user_input.analysis.harmonic_analysis_setup_input import HarmonicAnalysisSetupInput
from pulse.interface.user_input.analysis.modal_analysis_input import ModalAnalysisInput
from pulse.interface.user_input.analysis.static_analysis_input import StaticAnalysisInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.model import AnalysisID

AnalysisType = Literal[
    "",
    "Harmonic",
    "Modal"
    "Static",
]

PhysicalDomain = Literal[
    "",
    "Structural",
    "Acoustic",
    "Coupled",
]


"""

|-----------------------------------------------------------|
|                  Analysis ID mapping                      |
|-----------------------------------------------------------|
|    0 - Structural - Modal analysis                        |
|    1 - Structural - Harmonic analysis                     |
|    2 - Acoustic - Modal analysis (convetional FE 1D)      |
|    3 - Acoustic - Harmonic analysis (FETM)                |
|    4 - Coupled - Harmonic analysis                        |
|    5 - Structural - Static analysis                       |
|-----------------------------------------------------------|

"""

class AnalysisToolbar(QToolBar):

    enable_pushbutons = Signal()
    domain_changed = Signal()

    def __init__(self):
        super().__init__()

        self._config_widgets()
        self._configure_appearance()
        self._configure_layout()
        self._create_connections()
        self._load_analysis_types()

        self.setWindowTitle("Analysis toolbar")

    def _config_widgets(self):
        
        # load icons
        self.configure_analysis_icon = Icon(":/icons/common/settings.png")
        self.run_analysis_icon = Icon(":/icons/common/go_next.png")
        self.reset_solution_icon = Icon(":/icons/common/reset_icon.png")

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_physical_domain = QComboBox()
        #
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_physical_domain.setFixedSize(100, 28)

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.run_analysis_action = QAction(self.run_analysis_icon, "Run Analysis", self)
        self.configure_analysis_action = QAction(self.configure_analysis_icon, "Analysis Setup", self)
        self.reset_solution_action = QAction(self.reset_solution_icon, "Reset Solution", self)
        #
        self.configure_analysis_action.setToolTip("Configure the analysis")
        self.run_analysis_action.setToolTip("Run the analysis")
        self.reset_solution_action.setToolTip("Reset Solution")
        self.run_analysis_action.setDisabled(True)
        self.reset_solution_action.setEnabled(True)

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        font = QFont()
        font.setPointSize(10)

        widgets = list()
        for widget in [QComboBox, QLabel, QPushButton]:
            widgets += self.findChildren(widget)

        for widget in widgets:
            widget.setFont(font)
        
    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addSeparator()
        self.addWidget(self.label_analysis_type)
        self.addWidget(self.combo_box_analysis_type)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_analysis_domain)
        self.addWidget(self.combo_box_physical_domain)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addAction(self.configure_analysis_action)
        self.addWidget(self.get_spacer())
        self.addAction(self.run_analysis_action)
        self.addWidget(self.get_spacer())
        self.addAction(self.reset_solution_action)
        #
        self.adjustSize()

    def _create_connections(self):
        #
        self.combo_box_analysis_type.currentTextChanged.connect(self.analysis_type_callback)
        self.combo_box_physical_domain.currentTextChanged.connect(self.check_analysis_setup_callback)
        #
        self.configure_analysis_action.triggered.connect(self.configure_analysis_callback)
        self.reset_solution_action.triggered.connect(self.project_solution_data_reset)
        self.run_analysis_action.triggered.connect(self.run_analysis_callback)
        #
        self.enable_pushbutons.connect(self.check_analysis_setup_callback)
        self.enable_pushbutons.connect(self.set_pushbutton_reset_solution_enabled)

    def _load_analysis_types(self):

        self.combo_box_analysis_type.clear()
        for analysis_type in ["Harmonic", "Modal", "Static"]:
            self.combo_box_analysis_type.addItem(analysis_type)

        self.combo_box_physical_domain.clear()
        for physical_domain in ["Structural", "Acoustic", "Coupled"]:
            self.combo_box_physical_domain.addItem(physical_domain)

        # default setup
        self.combo_box_analysis_type.setCurrentText("Harmonic")
        self.combo_box_physical_domain.setCurrentText("Structural")

    def update_analysis_combo_boxes(self, block_signals: bool = False):

        if block_signals:
            self.combo_box_analysis_type.blockSignals(block_signals)
            self.combo_box_physical_domain.blockSignals(block_signals)

        analysis_type, physical_domain = app().project.get_analysis_type_and_physical_domain()

        if analysis_type == "harmonic":
            self.combo_box_analysis_type.setCurrentIndex(0)
        elif analysis_type == "modal":
            self.combo_box_analysis_type.setCurrentIndex(1)
        elif analysis_type == "static":
            self.combo_box_analysis_type.setCurrentIndex(2)

        if physical_domain == "structural":
            self.combo_box_physical_domain.setCurrentIndex(0)
        elif physical_domain == "acoustic":
            self.combo_box_physical_domain.setCurrentIndex(1)
        elif physical_domain == "coupled":
            self.combo_box_physical_domain.setCurrentIndex(2)

        if block_signals:
            self.combo_box_analysis_type.blockSignals(False)
            self.combo_box_physical_domain.blockSignals(False)

    def set_pushbutton_run_analysis_enabled(self, enable: bool = True):
        self.run_analysis_action.setEnabled(enable)

    def set_pushbutton_reset_solution_enabled(self):
        self.reset_solution_action.setEnabled(True)

    def get_current_analysis_id(self):

        analysis_type = self.combo_box_analysis_type.currentText()
        physical_domain = self.combo_box_physical_domain.currentText()

        if analysis_type == "Harmonic":
            if physical_domain == "Structural":
                return AnalysisID.STRUCTURAL_HARMONIC
            elif physical_domain == "Acoustic":
                return AnalysisID.ACOUSTIC_HARMONIC
            else:
                return AnalysisID.COUPLED_HARMONIC

        elif analysis_type == "Modal":
            if physical_domain == "Structural":
                return AnalysisID.STRUCTURAL_MODAL
            else:
                return AnalysisID.ACOUSTIC_MODAL
            
        elif analysis_type == "Static":
            if physical_domain == "Structural":
                return AnalysisID.STRUCTURAL_STATIC

        return AnalysisID.NO_ANALYSIS

    def check_analysis_setup_callback(self):
        # app().main_window.update_symbols()
        # app().main_window.update_info_text()
        current_analysis_id = self.get_current_analysis_id()
        valid_setup = app().project.is_there_a_valid_analysis_setup(current_analysis_id=current_analysis_id)
        self.set_pushbutton_run_analysis_enabled(valid_setup)
        self.domain_changed.emit()

    def analysis_type_callback(self):

        self.combo_box_physical_domain.blockSignals(True)

        if self.combo_box_analysis_type.currentIndex() == 0:
            available_domains = ["Structural", "Acoustic", "Coupled"]
        elif self.combo_box_analysis_type.currentIndex() == 1:
            available_domains = ["Structural", "Acoustic"]
        elif self.combo_box_analysis_type.currentIndex() == 2:
            available_domains = ["Structural"]
        else:
            available_domains = list()

        self.combo_box_physical_domain.clear()
        self.combo_box_physical_domain.addItems(available_domains)

        self.update_run_analysis_button()
        self.combo_box_physical_domain.blockSignals(False)
        self.check_analysis_setup_callback()

    def run_analysis_callback(self):
        # reset the existing project solution data
        app().main_window.reset_solution()
        if app().project.run_analysis():
            return

        self.post_processing_analysis()

    def post_processing_analysis(self):
        logging.info("Post-processing results... [10/100]")
        app().main_window.update_results_workspace_button_accessibility()
        
        logging.info("Post-processing results... [50/100]")
        app().main_window.use_results_workspace()
        app().main_window.results_widget.show_empty()
        app().main_window.results_viewer_widget.bottom_widget.hide()
        
        logging.info("Post-processing results... [95/100]")
        app().main_window.results_viewer_widget.results_viewer_items._update_items()
        self.set_pushbutton_reset_solution_enabled()

    def update_run_analysis_button(self):

        analysis_type = self.combo_box_analysis_type.currentText()
        domain = self.combo_box_physical_domain.currentText()

        new_analysis_ids = list()
        analysis_id = app().project.analysis_id

        if analysis_type == "Harmonic":
            if domain == "Structural":
                new_analysis_ids = [AnalysisID.STRUCTURAL_HARMONIC]
            elif domain == "Acoustic":
                new_analysis_ids = [AnalysisID.ACOUSTIC_HARMONIC]
            else:
                new_analysis_ids = [AnalysisID.COUPLED_HARMONIC]

        elif analysis_type == "Modal":
            if domain == "Structural":
                new_analysis_ids = [AnalysisID.STRUCTURAL_MODAL]
            else:
                new_analysis_ids = [AnalysisID.ACOUSTIC_MODAL]

        elif analysis_type == "Static":
            if domain == "Structural":
                new_analysis_ids = [AnalysisID.STRUCTURAL_STATIC]

        if analysis_id in new_analysis_ids:
            self.run_analysis_action.setEnabled(True)
            return

        self.run_analysis_action.setEnabled(False)

    def load_analysis_settings(self):

        self.run_analysis_action.setEnabled(False)

        analysis_id = app().project.analysis_id
        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            self.combo_box_analysis_type.setCurrentIndex(0)
        elif analysis_id in [AnalysisID.STRUCTURAL_MODAL, AnalysisID.ACOUSTIC_MODAL]:
            self.combo_box_analysis_type.setCurrentIndex(1)
        elif analysis_id == AnalysisID.STRUCTURAL_STATIC:
            self.combo_box_analysis_type.setCurrentIndex(2)

        if analysis_id in[AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.STRUCTURAL_MODAL, AnalysisID.STRUCTURAL_STATIC]:
            self.combo_box_physical_domain.setCurrentIndex(0)
        elif analysis_id in [AnalysisID.ACOUSTIC_MODAL, AnalysisID.ACOUSTIC_HARMONIC]:
            self.combo_box_physical_domain.setCurrentIndex(1)
        elif analysis_id in [AnalysisID.COUPLED_HARMONIC]:
            self.combo_box_physical_domain.setCurrentIndex(2)

        setup_complete = app().project.is_analysis_setup_complete()
        self.run_analysis_action.setEnabled(setup_complete)

    def project_solution_data_reset(self):

        title = "Removal of project solution data"
        message = "Would you like to delete all solution data from this project? "
        tool_tip = "Be aware, this process cannot be undone."

        buttons_config = {
            "left_button_label": "Cancel", 
            "right_button_label": "Delete all",
            "right_toolTip" : tool_tip
            }

        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config, window_title="OpenPulse")
        if read._cancel:
            return

        if not read._continue:
            return

        app().main_window.reset_solution()

    def configure_analysis_callback(self):

        analysis_type : AnalysisType = self.combo_box_analysis_type.currentText()
        physical_domain : PhysicalDomain = self.combo_box_physical_domain.currentText()

        if analysis_type == "Harmonic":
            if physical_domain == "Structural":
                self.harmonic_structural()
            elif physical_domain == "Acoustic":
                self.harmonic_acoustic()
            else:
                self.harmonic_coupled()

        elif analysis_type == "Modal":
            if physical_domain == "Structural":
                self.modal_structural()
            elif physical_domain == "Acoustic":
                self.modal_acoustic()

        elif analysis_type == "Static":
            if physical_domain == "Structural":
                self.static_analysis()

    def harmonic_structural(self):

        harmonic = HarmonicAnalysisSetupInput(AnalysisID.STRUCTURAL_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis_callback()
            # app().main_window.update_symbols()

    def harmonic_acoustic(self):

        harmonic = HarmonicAnalysisSetupInput(AnalysisID.ACOUSTIC_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis_callback()
    
    def harmonic_coupled(self):

        harmonic = HarmonicAnalysisSetupInput(AnalysisID.COUPLED_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis_callback()

    def modal_structural(self):
        modal = ModalAnalysisInput(AnalysisID.STRUCTURAL_MODAL)

        if modal.setup_defined:
            self.run_analysis_action.setEnabled(True)
            self.final_actions()

        app().project.model.frequencies = None

        if modal.proceed_solution:
            self.run_analysis_callback()

    def modal_acoustic(self):
        modal = ModalAnalysisInput(AnalysisID.ACOUSTIC_MODAL)

        if modal.setup_defined:
            self.run_analysis_action.setEnabled(True)
            self.final_actions()

        app().project.model.frequencies = None

        if modal.proceed_solution:
            self.run_analysis_callback()

    def static_analysis(self):

        static = StaticAnalysisInput()

        if static.setup_defined:
            self.run_analysis_action.setEnabled(True)
            self.final_actions()

        if not static.proceed_solution:
            return

        self.run_analysis_callback()

    def final_actions(self):
        app().main_window.reset_solution()
        # app().project.create_solver()
        self.update_run_analysis_button()
        #
        analysis_setup = app().project.model.analysis_setup
        app().project.file.write_analysis_setup_in_file(analysis_setup)

    def update_analysis_setup(self, analysis_setup: dict):

        keys_to_ignore = list(analysis_setup.keys())
        analysis_setup = app().project.model.analysis_setup

        if isinstance(analysis_setup, dict):
            for key, value in analysis_setup.items():
                if key in keys_to_ignore:
                    continue

                analysis_setup[key] = value

        app().project.model.set_analysis_setup(analysis_setup)
