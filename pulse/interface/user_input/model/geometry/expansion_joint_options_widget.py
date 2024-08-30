from copy import deepcopy
import warnings

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from opps.model import ExpansionJoint

from pulse import app, UI_DIR
from pulse.interface.utils import set_qt_property
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import ExpansionJointInput


class ExpansionJointOptionsWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        ui_path = UI_DIR / "model/geometry/expansion_joint_option_widget.ui"
        uic.loadUi(ui_path, self)

        self.pipeline = app().project.pipeline
        self.structure_type = ExpansionJoint
        self.add_function = self.pipeline.add_expansion_joint
        self.attach_function = self.pipeline.connect_expansion_joints
        self.expansion_joint_info = None

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):
        self.set_section_button.setProperty("warning", True)
        self.style().polish(self.set_section_button)

    def _define_qt_variables(self):
        self.set_section_button: QPushButton

    def _create_connections(self):
        self.set_section_button.clicked.connect(self.define_expansion_joint_parameters)

    def get_parameters(self) -> dict:
        if self.expansion_joint_info is None:
            return

        kwargs = dict()
        kwargs["diameter"] = self.expansion_joint_info["effective_diameter"]
        kwargs["thickness"] = 0
        kwargs["extra_info"] = dict(
            structural_element_type = "expansion_joint",
            expansion_joint_info = deepcopy(self.expansion_joint_info),
        )
        return kwargs

    def define_expansion_joint_parameters(self):

        app().main_window.close_dialogs()
        expansion_joint_input = app().main_window.input_ui.add_expansion_joint()
        app().main_window.set_input_widget(None)

        if not expansion_joint_input.complete:
            self.expansion_joint_info = None
            return

        self.expansion_joint_info = expansion_joint_input.expansion_joint_info
        set_qt_property(self.set_section_button, warning=False)
        self.edited.emit()
