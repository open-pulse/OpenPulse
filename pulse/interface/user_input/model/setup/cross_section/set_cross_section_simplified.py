from PySide6.QtWidgets import QDialog, QComboBox, QFrame, QGridLayout, QLineEdit, QPushButton, QScrollArea
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class SetCrossSectionSimplified(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/cross_section/set_cross_section_simplified.ui"
        load_ui(ui_path, self)

        self.main_window = app().main_window
        self.main_window.set_input_widget(self)

        self.project = app().main_window.project
        self.model = app().main_window.project.model
        self.properties = app().main_window.project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        # while self.keep_window_open:
        #     self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Configure the cross-section")

    def _initialize(self):
        self.selected_column = None
        self.complete = False
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type : QComboBox

        # # QFrame
        self.frame_main_widget : QFrame

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # QLineEdit

        # QScrollArea
        self.scrollArea_cross_section : QScrollArea
        self.scrollArea_cross_section.setLayout(self.grid_layout)
        self._add_cross_section_widget()
        # self.frame_main_widget.adjustSize()
        # self.scrollArea_cross_section.adjustSize()

        # # QPushButton
        self.pushButton_confirm_beam = self.cross_section_widget.pushButton_confirm_beam
        self.pushButton_confirm_pipe = self.cross_section_widget.pushButton_confirm_pipe

    def _create_connections(self):
        self.pushButton_confirm_beam.clicked.connect(self.attribute_callback)
        self.pushButton_confirm_pipe.clicked.connect(self.attribute_callback)

    def _add_cross_section_widget(self):
        self.cross_section_widget = CrossSectionWidget(dialog=self)
        self.grid_layout.addWidget(self.cross_section_widget)

    def attribute_callback(self):
        self.complete = True
        self.close()