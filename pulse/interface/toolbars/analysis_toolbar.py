from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QToolBar, QWidget
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtGui import  QIcon, QFont

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

"""
|--------------------------------------------------------------------|
|                    Analysis ID codification                        |
|--------------------------------------------------------------------|
|    0 - Structural - Harmonic analysis through direct method        |
|    1 - Structural - Harmonic analysis through mode superposition   |
|    2 - Structural - Modal analysis                                 |
|    3 - Acoustic - Harmonic analysis through direct method          |
|    4 - Acoustic - Modal analysis (convetional FE 1D)               |
|    5 - Coupled - Harmonic analysis through direct method           |
|    6 - Coupled - Harmonic analysis through mode superposition      |
|    7 - Structural - Static analysis (under development)            |
|--------------------------------------------------------------------|
"""

def decode_analysis(analysis_id):
    if analysis_id == 0:
        return

class AnalysisToolbar(QToolBar):
    def __init__(self):
        super().__init__()

        self._load_icons()
        self._define_qt_variables()
        self._configure_layout()
        self._configure_appearance()
        self._load_analysis_types()
        self._config_widgets()
        self._create_connections()

        self.setWindowTitle("Analysis toolbar")

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

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)

        user_preferences = app().main_window.config2.user_preferences

        font = QFont()
        font.setPointSize(user_preferences.interface_font_size)

        for widget in self.findChildren((QComboBox, QLabel, QPushButton)):
            widget.setFont(font)

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

    def _load_analysis_types(self):
        self.combo_box_analysis_type.clear()
        for _type in [" Harmonic", " Modal", " Static"]:
            self.combo_box_analysis_type.addItem(_type)

    def physical_domain_callback(self):
        self.update_run_analysis_button()

    def analysis_type_callback(self):

        if self.combo_box_analysis_type.currentIndex() == 0:
            available_domains = [" Structural", " Acoustic", " Coupled"]
        elif self.combo_box_analysis_type.currentIndex() == 1:
            available_domains = [" Structural", " Acoustic"]
        elif self.combo_box_analysis_type.currentIndex() == 2:
            available_domains = [" Structural"]
        else:
            available_domains = list()

        self.combo_box_analysis_domain.clear()
        self.combo_box_analysis_domain.blockSignals(True)

        for _domain in available_domains:
            self.combo_box_analysis_domain.addItem(_domain)

        self.update_run_analysis_button()
        self.combo_box_analysis_domain.blockSignals(False)

    def _config_widgets(self):

        # QComboBox
        self.combo_box_analysis_type.setFixedSize(100, 28)
        self.combo_box_analysis_domain.setFixedSize(100, 28)

        # QPushButton
        self.pushButton_configure_analysis.setFixedSize(50, 30)
        self.pushButton_configure_analysis.setIcon(self.settings_icon)
        self.pushButton_configure_analysis.setIconSize(QSize(20,20))
        self.pushButton_configure_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_configure_analysis.setToolTip("Configure the analysis")
        # self.pushButton_configure_analysis.setCheckable(True)

        self.pushButton_run_analysis.setFixedSize(50, 28)
        self.pushButton_run_analysis.setIcon(self.solution_icon)
        self.pushButton_run_analysis.setIconSize(QSize(20,20))
        self.pushButton_run_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_run_analysis.setToolTip("Run the analysis")
        # self.pushButton_run_analysis.setCheckable(True)
        self.pushButton_run_analysis.setDisabled(True)

    def _create_connections(self):
        #
        self.combo_box_analysis_type.currentIndexChanged.connect(self.analysis_type_callback)
        self.combo_box_analysis_domain.currentIndexChanged.connect(self.physical_domain_callback)
        #
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis_callback)
        #
        self.analysis_type_callback()

    def run_analysis_callback(self):
        app().project.run_analysis()

    def configure_analysis_callback(self):

        app().main_window.close_dialogs()

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

    def harmonic_structural(self):

        select = StructuralHarmonicAnalysisInput()
        if select.index == -1:
            return

        method_id = select.index

        if method_id == 0:
            analysis_id = 0
        else:
            analysis_id = 1

        app().project.set_analysis_id(analysis_id)

        app().project.reset_solution()
        if app().main_window.input_ui.analysis_setup():
            self.update_run_analysis_button()

    def harmonic_acoustic(self):

        method_id = 0

        if method_id == 0:
            analysis_id = 3
        else:
            return

        app().project.set_analysis_id(analysis_id)

        app().project.reset_solution()
        if app().main_window.input_ui.analysis_setup():
            self.update_run_analysis_button()

    def harmonic_coupled(self):

        coupled = CoupledHarmonicAnalysisInput()
        if coupled.index == -1:
            return

        method_id = coupled.index

        if method_id == 0:
            analysis_id = 5
        else:
            analysis_id = 6

        app().project.set_analysis_id(analysis_id)

        app().project.reset_solution()
        if app().main_window.input_ui.analysis_setup():
            self.update_run_analysis_button()

    def modal_structural(self):

        modal = StructuralModalAnalysisInput()

        if modal.setup_defined:
            self.update_run_analysis_button()

        if not modal.proceed_solution:
            return

        app().project.model.frequencies = None
        app().project.run_analysis()

    def modal_acoustic(self):

        modal = AcousticModalAnalysisInput()

        if modal.setup_defined:
            self.update_run_analysis_button()

        if not modal.proceed_solution:
            return
        
        app().project.model.frequencies = None
        app().project.run_analysis()

    def static_analysis(self):

        static = StaticAnalysisInput()

        if static.setup_defined:
            self.update_run_analysis_button()

        if not static.proceed_solution:
            return

        app().project.run_analysis()

    def update_run_analysis_button(self):

        analysis_type = self.combo_box_analysis_type.currentIndex()
        domain = self.combo_box_analysis_domain.currentIndex()

        new_analysis_ids = list()
        analysis_id = app().project.analysis_id

        if analysis_type == 0:
            if domain == 0:
                new_analysis_ids = [0, 1]
            elif domain == 1:
                new_analysis_ids = [3]
            else:
                new_analysis_ids = [5, 6]

        elif analysis_type == 1:
            if domain == 0:
                new_analysis_ids = [2]
            else:
                new_analysis_ids = [4]

        elif analysis_type == 2:
            if domain == 0:
                new_analysis_ids = [7]

        else:
            pass

        if analysis_id in new_analysis_ids:
            self.pushButton_run_analysis.setEnabled(True)
        else:
            self.pushButton_run_analysis.setEnabled(False)

    def load_analysis_settings(self):

        self.pushButton_run_analysis.setEnabled(False)

        analysis_id = app().project.analysis_id
        if analysis_id in [0, 1, 3, 5, 6]:
            self.combo_box_analysis_type.setCurrentIndex(0)
        elif analysis_id in [2, 4]:
            self.combo_box_analysis_type.setCurrentIndex(1)
        elif analysis_id == 7:
            self.combo_box_analysis_type.setCurrentIndex(2)

        if analysis_id in [0, 1, 2, 7]:
            self.combo_box_analysis_domain.setCurrentIndex(0)
        elif analysis_id in [3, 4]:
            self.combo_box_analysis_domain.setCurrentIndex(1)
        elif analysis_id in [5, 6]:
            self.combo_box_analysis_domain.setCurrentIndex(2)

        setup_complete = app().project.is_analysis_setup_complete()
        self.pushButton_run_analysis.setEnabled(setup_complete)