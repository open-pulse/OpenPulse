from PyQt5.QtWidgets import QComboBox, QLabel, QFileDialog, QPushButton, QSlider, QSpinBox, QToolBar, QWidget
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtGui import  QIcon

from pulse import app, UI_DIR, ICON_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse.interface.user_input.analysis.structural.structural_harmonic_analysis import StructuralHarmonicAnalysisInput
from pulse.interface.user_input.analysis.coupled.coupled_harmonic_analysis import CoupledHarmonicAnalysisInput
from pulse.interface.user_input.analysis.structural.structural_modal_analysis import StructuralModalAnalysisInput
from pulse.interface.user_input.analysis.acoustic.acoustic_modal_analysis import AcousticModalAnalysisInput
from pulse.interface.user_input.analysis.structural.static_analysis_input import StaticAnalysisInput

from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class AnalysisToolbar(QToolBar):
    def __init__(self):
        super().__init__()

        self._initialize()
        self._load_icons()
        self._define_qt_variables()
        self._load_analysis_options()
        self.update_domain_callback()
        self._config_widgets()
        self._create_connections()
        self._configure_layout()
        self._configure_appearance()

    def _initialize(self):
        self.animating = False

    def _load_icons(self):
        self.settings_icon = QIcon(str(ICON_DIR / "common/settings.png"))
        self.solution_icon = QIcon(str(ICON_DIR / "common/go_next.png"))

    def _define_qt_variables(self):

        # QComboBox
        self.combo_box_analysis_type = QComboBox()
        self.combo_box_analysis_domain = QComboBox()

        # QLabel
        self.label_analysis_type = QLabel("Analysis type:")
        self.label_analysis_domain = QLabel("Physical domain:")

        # QPushButton
        self.pushButton_run_analysis = QPushButton(self)
        self.pushButton_configure_analysis = QPushButton(self)

    def _load_analysis_options(self):
        self.combo_box_analysis_type.clear()
        for _type in [" Harmonic", " Modal", " Static"]:
            self.combo_box_analysis_type.addItem(_type)

    def update_domain_callback(self):

        if self.combo_box_analysis_type.currentIndex() == 0:
            available_domains = [" Structural", " Acoustic", " Coupled"]
        elif self.combo_box_analysis_type.currentIndex() == 1:
            available_domains = [" Structural", " Acoustic"]
        elif self.combo_box_analysis_type.currentIndex() == 2:
            available_domains = [" Structural"]
        else:
            available_domains = list()

        self.combo_box_analysis_domain.clear()
        for _domain in available_domains:
            self.combo_box_analysis_domain.addItem(_domain)

    def _config_widgets(self):

        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

        # QComboBox
        self.combo_box_analysis_type.setFixedHeight(26)
        self.combo_box_analysis_type.setFixedWidth(90)
        self.combo_box_analysis_domain.setFixedHeight(26)
        self.combo_box_analysis_domain.setFixedWidth(90)

        # QPushButton
        self.pushButton_configure_analysis.setFixedHeight(28)
        self.pushButton_configure_analysis.setFixedWidth(40)
        self.pushButton_configure_analysis.setIcon(self.settings_icon)
        self.pushButton_configure_analysis.setIconSize(QSize(20,20))
        self.pushButton_configure_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_configure_analysis.setToolTip("Configure the analysis")
        # self.pushButton_configure_analysis.setCheckable(True)

        self.pushButton_run_analysis.setFixedHeight(28)
        self.pushButton_run_analysis.setFixedWidth(40)
        self.pushButton_run_analysis.setIcon(self.solution_icon)
        self.pushButton_run_analysis.setIconSize(QSize(20,20))
        self.pushButton_run_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_run_analysis.setToolTip("Run the analysis")
        # self.pushButton_run_analysis.setCheckable(True)
        self.pushButton_run_analysis.setDisabled(True)

    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addWidget(self.label_analysis_type)
        self.addWidget(self.combo_box_analysis_type)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_analysis_domain)
        self.addWidget(self.combo_box_analysis_domain)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_configure_analysis)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_run_analysis)
        #
        self.adjustSize()

    def _configure_appearance(self):
        self.setMinimumHeight(32)
        self.setMovable(True)
        self.setFloatable(True)

    def _create_connections(self):
        #
        self.combo_box_analysis_type.currentIndexChanged.connect(self.update_domain_callback)
        #
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis_callback)

    def run_analysis_callback(self):
        app().main_window.input_ui.run_analysis()

    def configure_analysis_callback(self):

        self.complete = False

        analysis_type = self.combo_box_analysis_type.currentIndex()
        domain = self.combo_box_analysis_domain.currentIndex()

        if analysis_type == 0:
            if domain == 0:
                self.harmonic_structural()
            elif domain == 1:
                self.harmonic_acoustic()
            else:
                self.harmonic_coupled()

        elif analysis_type == 1:
            if domain == 0:
                self.modal_structural()
            else:
                self.modal_acoustic()

        elif analysis_type == 2:
            if domain == 0:
                self.static_analysis()

        else:
            pass

        if self.complete:
            self.actions_to_finalize()

    def harmonic_structural(self):

        select = StructuralHarmonicAnalysisInput()
        if select.index == -1:
            return

        self.method_id = select.index
        analysis_type = "Structural Harmonic Analysis"
        if self.method_id == 0:
            analysis_id = 0
            analysis_method = "Direct Method"
        else:
            analysis_id = 1
            analysis_method = "Mode Superposition Method"

        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def harmonic_acoustic(self):

        self.method_id = 0
        analysis_type = "Acoustic Harmonic Analysis"

        if self.method_id == 0:
            analysis_id = 3
            analysis_method = "Direct Method"
        else:
            return
    
        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def harmonic_coupled(self):

        coupled = CoupledHarmonicAnalysisInput()
        if coupled.index == -1:
            return

        self.method_id = coupled.index
        analysis_type = "Coupled Harmonic Analysis"
        if self.method_id == 0:
            analysis_id = 5
            analysis_method = "Direct Method"
        else:
            analysis_id = 6
            analysis_method = "Mode Superposition Method"

        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def modal_structural(self):

        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            return

        analysis_id = 2
        analysis_type = "Structural Modal Analysis"

        app().project.set_analysis_type(analysis_id, analysis_type, None)
        app().project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def modal_acoustic(self):

        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            return

        analysis_id = 4
        analysis_type = "Acoustic Modal Analysis"

        app().project.set_analysis_type(analysis_id, analysis_type, None)
        app().project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def static_analysis(self):

        static = StaticAnalysisInput()
        if not static.complete:
            return

        analysis_id = 7
        analysis_type = "Static Analysis"

        app().project.set_analysis_type(analysis_id, analysis_type, None)
        self.complete = static.complete
    
    def actions_to_finalize(self):

        analysis_id = app().project.analysis_id

        if analysis_id is None:
            return

        if analysis_id in [0, 1, 3, 5, 6, 7]:
            app().project.set_structural_solution(None)
            app().project.set_acoustic_solution(None)

        if analysis_id in [2, 4, 7]:
            app().project.model.frequencies = None
            app().project.update_project_analysis_setup_state(True)
            app().main_window.input_ui.run_analysis()

        else:
            app().main_window.input_ui.analysis_setup()

        setup_complete = app().project.analysis_setup_complete
        self.pushButton_run_analysis.setEnabled(setup_complete)