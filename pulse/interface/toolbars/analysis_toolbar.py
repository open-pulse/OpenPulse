from PyQt5.QtWidgets import QComboBox, QLabel, QFileDialog, QPushButton, QSlider, QSpinBox, QToolBar, QWidget
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtGui import  QIcon

from pulse import app, UI_DIR, ICON_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput

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
        self.pushButton_configure_analysis.setCheckable(True)

        self.pushButton_run_analysis.setFixedHeight(28)
        self.pushButton_run_analysis.setFixedWidth(40)
        self.pushButton_run_analysis.setIcon(self.solution_icon)
        self.pushButton_run_analysis.setIconSize(QSize(20,20))
        self.pushButton_run_analysis.setCursor(Qt.PointingHandCursor)
        self.pushButton_run_analysis.setToolTip("Run the analysis")
        self.pushButton_run_analysis.setCheckable(True)
        self.pushButton_run_analysis.setDisabled(True)

    def _create_connections(self):
        #
        self.combo_box_analysis_type.currentIndexChanged.connect(self.update_domain_callback)
        #
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)
        self.pushButton_configure_analysis.clicked.connect(self.configure_analysis_callback)

    def run_analysis_callback(self):
        pass

    def configure_analysis_callback(self):
        pass

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