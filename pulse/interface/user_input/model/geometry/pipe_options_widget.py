from copy import deepcopy
import warnings

from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QSlider, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from opps.model import Pipe, Bend

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.cross_section.cross_section_inputs import CrossSectionWidget


class PipeOptionsWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        ui_path = UI_DIR / "model/geometry/pipe_option_widget.ui"
        uic.loadUi(ui_path, self)

        self.pipeline = app().project.pipeline
        self.render_widget = app().main_window.geometry_widget

        self.structure_type = Pipe
        self.add_function = self.pipeline.add_bent_pipe
        self.attach_function = self.pipeline.connect_bent_pipes
        self.cross_section_info = None
        self.user_defined_bending_radius = 0

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self._initialize()

    def _define_qt_variables(self):
        self.bending_options_combobox: QComboBox
        self.bending_radius_line_edit: QLineEdit

        self.division_combobox: QComboBox
        self.division_slider: QSlider
        self.cancel_division_button: QPushButton
        self.apply_division_button: QPushButton
        self.division_amount_label: QLabel
        self.division_slider_label: QLabel

        self.set_section_button: QPushButton
        self.cross_section_widget = CrossSectionWidget(self)

    def _create_layout(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.cross_section_widget.hide()

    def _create_connections(self):
        self.bending_options_combobox.currentTextChanged.connect(self.bending_options_changed_callback)
        self.bending_radius_line_edit.textEdited.connect(self.bending_radius_changed_callback)
        self.set_section_button.clicked.connect(self.show_cross_section_widget_callback)
        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section_callback)

        self.division_combobox.currentTextChanged.connect(self.division_type_changed_callback)
        self.division_slider.valueChanged.connect(self.division_slider_callback)
        self.cancel_division_button.clicked.connect(self.cancel_division_callback)
        self.apply_division_button.clicked.connect(self.apply_division_callback)

    def _initialize(self):
        self.bending_options_changed_callback("long radius")
        self.division_type_changed_callback("single division")
        self.set_section_button.setProperty("warning", True)
        self.style().polish(self.set_section_button)

    def get_parameters(self) -> dict:
        if self.cross_section_info is None:
            return

        parameters = self.cross_section_info.get("section_parameters")
        if parameters is None:
            return

        kwargs = dict()
        kwargs["diameter"] = parameters[0]
        kwargs["thickness"] = parameters[1]
        kwargs["curvature_radius"] = 0.3
        kwargs["extra_info"] = dict(
            structural_element_type = "pipe_1",
            cross_section_info = deepcopy(self.cross_section_info),
        )
        return kwargs

    def show_cross_section_widget_callback(self):
        self.cross_section_widget.show()

    def define_cross_section_callback(self):
        if self.cross_section_widget.get_constant_pipe_parameters():
            return
        self.cross_section_info = self.cross_section_widget.pipe_section_info
        self.cross_section_widget.hide()
        self.set_section_button.setProperty("warning", False)
        self.style().polish(self.set_section_button)
        self.edited.emit()

    def get_bending_radius(self, diameter):
        if (self.bending_option == "long radius") or (self.bending_option == "short radius"):
            return self.bending_factor * diameter

        elif self.bending_option == "user-defined":
            return self.user_defined_bending_radius

        else:
            return 0

    def bending_options_changed_callback(self, text: str):
        self.bending_factor = 0
        self.bending_option = text.lower().strip()
        self.bending_radius_line_edit.setDisabled(True)

        if self.bending_option == "long radius":
            self.bending_factor = 1.5
            self.bending_radius_line_edit.setText("1.5 * D")

        elif self.bending_option == "short radius":
            self.bending_factor = 1
            self.bending_radius_line_edit.setText("1.0 * D")

        elif self.bending_option == "user-defined":
            r = str(round(self.user_defined_bending_radius, 4))
            self.bending_radius_line_edit.setText(r)
            self.bending_radius_line_edit.setDisabled(False)
            self.bending_radius_line_edit.setFocus()

        elif self.bending_option == "disabled":
            self.bending_factor = 0
            self.bending_radius_line_edit.setText("disabled")

        else:
            warnings.warn(f'Bending option "{self.bending_option}" not available.')

        self._apply_bending_radius_to_selection()
        self.edited.emit()

    def bending_radius_changed_callback(self, text: str):
        try:
            self.user_defined_bending_radius = float(text)

        except ValueError:
            self.user_defined_bending_radius = 0

        else:
            self._apply_bending_radius_to_selection()
            self.edited.emit()

    def division_type_changed_callback(self, text: str):
        division_type = text.lower()

        if division_type == "single division":
            self.division_slider.setMinimum(0)
            self.division_slider.setMaximum(100)
            self.division_slider.setValue(50)
            self.division_slider_label.setText("Position")

        elif division_type == "multiple division":
            self.division_slider.setMinimum(1)
            self.division_slider.setMaximum(10)
            self.division_slider.setValue(1)
            self.division_slider_label.setText("Divisions")

    def division_slider_callback(self, value):
        division_type = self.division_combobox.currentText().lower()
        self.pipeline.dismiss()

        if division_type == "single division":
            self.pipeline.preview_divide_structures(value / 100)
            self.division_amount_label.setText(f"[{value} %]")

        elif division_type == "multiple division":
            self.pipeline.preview_divide_structures_evenly(value)
            self.division_amount_label.setText(f"[{value}]")

        self.render_widget.update_plot(reset_camera=False)
    
    def cancel_division_callback(self):
        self.pipeline.dismiss()
        self.render_widget.update_plot(reset_camera=False)

    def apply_division_callback(self):
        self.pipeline.dismiss()
        value = self.division_slider.value()
        division_type = self.division_combobox.currentText().lower()

        if division_type == "single division":
            self.pipeline.divide_structures(value / 100)

        elif division_type == "multiple division":
            self.pipeline.divide_structures_evenly(value)

        self.pipeline.clear_structure_selection()
        self.render_widget.update_plot(reset_camera=False)

    def _apply_bending_radius_to_selection(self):
        for bend in self.pipeline.selected_structures:
            if not isinstance(bend, Bend):
                continue
            bend.curvature = self.get_bending_radius(bend.diameter)
        self.pipeline.recalculate_curvatures()
