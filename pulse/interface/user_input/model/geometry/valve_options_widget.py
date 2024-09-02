from copy import deepcopy
import warnings

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from opps.model import Valve

from pulse import app, UI_DIR
from pulse.interface.utils import set_qt_property
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.interface.user_input.model.setup.structural.valves_input import ValvesInput


class ValveOptionsWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        ui_path = UI_DIR / "model/geometry/only_section_option_widget.ui"
        uic.loadUi(ui_path, self)

        self.pipeline = app().project.pipeline
        self.structure_type = Valve
        self.add_function = self.pipeline.add_valve
        self.attach_function = self.pipeline.connect_valves
        self.valve_info = None

        self._initialize()
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):
        self.set_section_button.setProperty("warning", True)
        self.style().polish(self.set_section_button)

    def _define_qt_variables(self):
        self.set_section_button: QPushButton

    def _create_connections(self):
        self.set_section_button.clicked.connect(self.define_valve_parameters)

    def get_parameters(self) -> dict:
        if self.valve_info is None:
            return

        kwargs = dict()
        kwargs["diameter"] = self.valve_info.get("valve_effective_diameter", 0)
        kwargs["thickness"] = 0
        kwargs["extra_info"] = dict(
            structural_element_type = "valve",
            cross_section_info = {"section_type_label" : "Valve"},
            valve_info = deepcopy(self.valve_info),
        )
        return kwargs

    def define_valve_parameters(self):

        app().main_window.close_dialogs()
        valve_input = ValvesInput(render_type="geometry")
        app().main_window.set_input_widget(None)

        if not valve_input.complete:
            self.valve_info = None
            return

        self.valve_info = valve_input.valve_info
        set_qt_property(self.set_section_button, warning=False)
        self.edited.emit()
