from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QToolBar, QWidget
from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import  QIcon, QFont

from pulse import app, UI_DIR, ICON_DIR
from pulse.model import AnalysisID
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from pulse.interface.user_input.analysis.harmonic_analysis_setup_input import HarmonicAnalysisSetupInput
from pulse.interface.user_input.analysis.modal_analysis_input import ModalAnalysisInput
from pulse.interface.user_input.analysis.static_analysis_input import StaticAnalysisInput

import logging
from typing import Literal
from time import time

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
|                  Analysis ID codification                 |
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

    def __init__(self):
        super().__init__()

        self._define_qt_variables()
        self._create_connections()

        self._configure_layout()
        self._configure_appearance()
        self._config_widgets()
        self._load_analysis_types()

        self.setWindowTitle("Analysis toolbar")

    def _define_qt_variables(self):

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_physical_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.pushButton_run_analysis = QPushButton(self)
        self.pushButton_configure_analysis = QPushButton(self)
        self.pushButton_reset_solution = QPushButton(self)

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)

        font = QFont()
        font.setPointSize(10)

        widgets = list()
        for widget in [QComboBox, QLabel, QPushButton]:
            widgets += self.findChildren(widget)

        for widget in widgets:
            widget.setFont(font)
        
        self.setStyleSheet(
            """
            QToolBar {
                border-style: solid;
                border-width: 1px;
                border-color: #888888;
            }
            """
        )

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
        self.addWidget(self.pushButton_configure_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_run_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_reset_solution)
        #
        self.adjustSize()

    def _config_widgets(self):
        
        # load icons
        self.settings_icon = QIcon(str(ICON_DIR / "common/settings.png"))
        self.solution_icon = QIcon(str(ICON_DIR / "common/go_next.png"))
        self.reset_icon = QIcon(str(ICON_DIR / "common/reset_icon.png"))

        # QComboBox
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_physical_domain.setFixedSize(100, 28)

        # QPushButton
        self.pushButton_configure_analysis.setFixedSize(50, 30)
        self.pushButton_configure_analysis.setIcon(self.settings_icon)
        self.pushButton_configure_analysis.setIconSize(QSize(20, 20))
        self.pushButton_configure_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_configure_analysis.setToolTip("Configure the analysis")

        self.pushButton_run_analysis.setFixedSize(50, 30)
        self.pushButton_run_analysis.setIcon(self.solution_icon)
        self.pushButton_run_analysis.setIconSize(QSize(20, 20))
        self.pushButton_run_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_run_analysis.setToolTip("Run the analysis")
        self.pushButton_run_analysis.setDisabled(True)

        self.pushButton_reset_solution.setFixedSize(50, 30)
        self.pushButton_reset_solution.setIcon(self.reset_icon)
        self.pushButton_reset_solution.setIconSize(QSize(20, 20))
        self.pushButton_reset_solution.setCursor(Qt.PointingHandCursor)
        self.pushButton_reset_solution.setToolTip("Reset Solution")
        self.pushButton_reset_solution.setDisabled(True)
    
    def _create_connections(self):
        #
        # self.combo_box_analysis_type.currentIndexChanged.connect(self.analysis_type_callback)
        # self.combo_box_physical_domain.currentIndexChanged.connect(self.physical_domain_callback)
        #
        # self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)
        # self.pushButton_configure_analysis.clicked.connect(self.configure_analysis_callback)
        #
        self.combo_box_analysis_type.currentTextChanged.connect(self.analysis_type_callback)
        self.combo_box_physical_domain.currentTextChanged.connect(self.check_analysis_setup_callback)
        #
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis)
        self.pushButton_reset_solution.clicked.connect(self.project_solution_data_reset)
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        #
        self.enable_pushbutons.connect(self.check_analysis_setup_callback)
        self.enable_pushbutons.connect(self.set_pushbutton_reset_solution_enabled)
        #
        # self.analysis_type_callback()

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
        self.pushButton_run_analysis.setEnabled(enable)

    def set_pushbutton_reset_solution_enabled(self):
        self.pushButton_reset_solution.setEnabled(True)

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

    def run_analysis(self):
        app().project.run_analysis()
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
            self.pushButton_run_analysis.setEnabled(True)
            return

        self.pushButton_run_analysis.setEnabled(False)

    def load_analysis_settings(self):

        self.pushButton_run_analysis.setEnabled(False)

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
        self.pushButton_run_analysis.setEnabled(setup_complete)

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

        self.reset_solution()

    def reset_solution(self):
        app().project.reset_solutions()
        app().project.file.remove_results_data_from_project_file()

        self.pushButton_reset_solution.setDisabled(True)
        app().main_window.project_data_modified = True
        app().main_window.use_model_setup_workspace()
        app().main_window.update_results_workspace_button_accessibility()

    def configure_analysis(self):

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

        harmonic = HarmonicAnalysisSetupInput(analysis_id=AnalysisID.STRUCTURAL_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
            # app().main_window.update_symbols()

    def harmonic_acoustic(self):

        harmonic = HarmonicAnalysisSetupInput(analysis_id=AnalysisID.ACOUSTIC_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()
    
    def harmonic_coupled(self):

        harmonic = HarmonicAnalysisSetupInput(analysis_id=AnalysisID.COUPLED_HARMONIC)

        if harmonic.setup_defined:
            self.final_actions()

        if harmonic.solve_analysis:
            self.run_analysis()

    def modal_structural(self):
        modal = ModalAnalysisInput()

        if modal.modes_number is None:
            return

        if modal.setup_defined:
            app().project.set_analysis_setup(modal.analysis_setup)
            self.pushButton_run_analysis.setEnabled(True)
            self.final_actions()

        app().project.model.frequencies = None

        if modal.proceed_solution:
            self.run_analysis()

    def modal_acoustic(self):
        modal = ModalAnalysisInput()

        if modal.modes_number is None:
            return

        if modal.setup_defined:
            app().project.set_analysis_setup(modal.analysis_setup)
            self.pushButton_run_analysis.setEnabled(True)
            self.final_actions()

        app().project.model.frequencies = None

        if modal.proceed_solution:
            self.run_analysis()

    def static_analysis(self):

        static = StaticAnalysisInput()

        if static.setup_defined:
            self.pushButton_run_analysis.setEnabled(True)
            self.final_actions()

        if not static.proceed_solution:
            return

        app().project.run_analysis()

    def final_actions(self):
        self.reset_solution()
        # app().project.create_solver()
        self.update_run_analysis_button()
        app().project.file.write_analysis_setup_in_file(app().project.analysis_setup)

    def update_analysis_setup(self, analysis_setup: dict):

        keys_to_ignore = list(analysis_setup.keys())
        if isinstance(app().project.analysis_setup, dict):
            for key, value in app().project.analysis_setup.items():
                if key in keys_to_ignore:
                    continue
                analysis_setup[key] = value

        app().project.set_analysis_setup(analysis_setup)