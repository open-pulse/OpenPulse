from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

from copy import deepcopy
import warnings

from opps.model import Bend
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from pulse.interface.user_input.model.setup.cross_section.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.material.material_widget import MaterialInputs

from pulse import app, UI_DIR


class EditPipeWidget(QWidget):
    edited = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/edit_pipe_widget.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.pipeline = app().project.pipeline

        self.bending_factor = 0
        self.user_defined_bending_radius = 0
        self.current_cross_section_info = None

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        
        self.bending_options_changed_callback("long radius")

    def _define_qt_variables(self):
        self.bending_options_combobox: QComboBox
        self.bending_radius_line_edit: QLineEdit

        self.set_section_button: QPushButton
        self.set_material_button: QPushButton
        self.set_fluid_button: QPushButton
    
    def _create_layout(self):
        self.cross_section_widget = CrossSectionWidget(self)
        self.material_widget = MaterialInputs(self)

        self.cross_section_widget.hide()
        self.material_widget.hide()

    def _create_connections(self):
        self.bending_options_combobox.currentTextChanged.connect(self.bending_options_changed_callback)
        self.bending_radius_line_edit.textEdited.connect(self.bending_radius_changed_callback)

        self.set_section_button.clicked.connect(self.show_cross_section_widget_callback)
        # self.set_material_button.clicked.connect(self.show_material_widget_callback)
        # self.set_fluid_button.clicked.connect(self.show_fluid_widget_callback)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section_callback)


    def show_cross_section_widget_callback(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     
        self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
        self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
        self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        self.cross_section_widget.setVisible(True)

    def define_cross_section_callback(self):
        if self.cross_section_widget.get_constant_pipe_parameters():
            return
        self.current_cross_section_info = self.cross_section_widget.pipe_section_info
        self.cross_section_widget.hide()

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

        self._apply_to_selection()
        self.edited.emit()

    def bending_radius_changed_callback(self, text: str):
        try:
            self.user_defined_bending_radius = float(text)

        except ValueError:
            self.user_defined_bending_radius = 0

        else:
            self._apply_to_selection()
            self.edited.emit()

    def _apply_to_selection(self):
        for bend in self.pipeline.selected_structures:
            if not isinstance(bend, Bend):
                continue
            bend.curvature = self.get_bending_radius(bend.diameter)
        self.pipeline.recalculate_curvatures()

    def _get_selected_curvature(self):
        last_curvature = None

        for bend in self.pipeline.selected_structures:
            if not isinstance(bend, Bend):
                continue

            if last_curvature is None:
                last_curvature = bend.curvature

            elif bend.curvature != last_curvature:
                return None

        return last_curvature
            
