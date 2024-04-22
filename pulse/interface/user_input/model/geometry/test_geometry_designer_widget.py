from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5 import uic
import re
from copy import deepcopy
import warnings

from opps.model import Pipeline
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler


class GeometryDesignerWidget(QWidget):
    def __init__(self, render_widget: EditorRenderWidget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/test_geometry_designer_widget.ui"
        uic.loadUi(ui_path, self)

        self.render_widget = render_widget
        self.geometry_handler = GeometryHandler()

        self.project = app().project
        self.pipeline = self.project.pipeline
        self.file = self.project.file

        # This dict is passed as argument for the current
        # creation function, either if it is a pipe, a bend,
        # an i-beam, a square beam, etc.
        # If the argument is useless to the current function,
        # like a diameter in a square beam, the argument
        # will be ignored, and no errors will be raised. 
        self.structure_kwargs = dict()
        self.add_structure_function = None
        self.attach_selection_function = None

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self._initial_configuration()
        self.setContentsMargins(2,2,2,2)

    def _define_qt_variables(self):
        self.unit_combobox: QComboBox
        self.structure_combobox: QComboBox

        self.set_section_button: QPushButton
        self.set_material_button: QPushButton
        self.set_fluid_button: QPushButton

        self.x_line_edit: QLineEdit
        self.y_line_edit: QLineEdit
        self.z_line_edit: QLineEdit

        self.sizes_coords_label: QLabel
        self.dx_label: QLabel
        self.dy_label: QLabel
        self.dz_label: QLabel

        self.bending_options_combobox: QComboBox
        self.bending_radius_line_edit: QLineEdit

        self.add_button: QPushButton
        self.attach_button: QPushButton
        self.delete_button: QPushButton
    
    def _create_layout(self):
        pass

    def _create_connections(self):
        self.render_widget.selection_changed.connect(self.selection_callback)

        self.unit_combobox.currentTextChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_type_changed_callback)
        
        self.set_section_button.clicked.connect(self.section_callback)
        self.set_material_button.clicked.connect(self.material_callback)
        self.set_fluid_button.clicked.connect(self.fluid_callback)

        self.x_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)
        self.y_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)
        self.z_line_edit.textEdited.connect(self.sizes_coordinates_changed_callback)

        self.bending_options_combobox.currentTextChanged.connect(self.bending_options_changed_callback)
        self.bending_radius_line_edit.textEdited.connect(self.bending_radius_changed_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)        

    def _initial_configuration(self):
        self.bending_options_changed_callback("long radius")
        self.unity_changed_callback("meter")
        self.structure_type_changed_callback("pipe")

        self.user_defined_bending_radius = 0
        self.set_section_button.setProperty("warning", True)
        self.set_material_button.setProperty("warning", True)
        self.set_fluid_button.setProperty("warning", True)

        self.style().polish(self.set_section_button)
        self.style().polish(self.set_material_button)
        self.style().polish(self.set_fluid_button)

    def selection_callback(self):
        pass

    def unity_changed_callback(self, text: str):
        self.length_unit = text.lower().strip()
        
        if self.length_unit == "meter":
            unit_label_text = "[m]"

        elif self.length_unit == "milimeter":
            unit_label_text = "[mm]"

        elif self.length_unit == "inch":
            unit_label_text = "[in]"

        else:
            return

        # Automatically replace every label in the format [m] or [mm] or [in]
        unit_pattern = re.compile(r"\[(m|mm|in)\]")
        for label in self.findChildren(QLabel):
            if unit_pattern.match(label.text()) is not None:
                label.setText(unit_label_text)

    def structure_type_changed_callback(self, structure_type: str):
        structure_type = structure_type.lower().strip()
        self._show_deltas_mode(True)

        if structure_type == "pipe":
            self.add_structure_function = self.pipeline.add_bent_pipe
            self.attach_selection_function = self.pipeline.connect_bent_pipes

        elif structure_type == "point":
            self.add_structure_function = self.pipeline.add_point
            self.attach_selection_function = None
            self._show_deltas_mode(False)

        elif structure_type == "flange":
            self.add_structure_function = self.pipeline.add_flange
            self.attach_selection_function = self.pipeline.connect_flanges

        elif structure_type == "valve":
            self.add_structure_function = self.pipeline.add_valve
            self.attach_selection_function = self.pipeline.connect_valves

        elif structure_type == "expansion joint":
            self.add_structure_function = self.pipeline.add_expansion_joint
            self.attach_selection_function = self.pipeline.connect_expansion_joints

        elif structure_type == "reducer":
            self.add_structure_function = self.pipeline.add_reducer_eccentric
            self.attach_selection_function = self.pipeline.connect_reducer_eccentrics

        elif structure_type == "circular beam":
            self.add_structure_function = self.pipeline.add_circular_beam
            self.attach_selection_function = self.pipeline.connect_circular_beams

        elif structure_type == "rectangular beam":
            self.add_structure_function = self.pipeline.add_rectangular_beam
            self.attach_selection_function = self.pipeline.connect_rectangular_beams

        elif structure_type == "i-beam":
            self.add_structure_function = self.pipeline.add_i_beam
            self.attach_selection_function = self.pipeline.connect_i_beams

        elif structure_type == "t-beam":
            self.add_structure_function = self.pipeline.add_t_beam
            self.attach_selection_function = self.pipeline.connect_t_beams

        elif structure_type == "c-beam":
            self.add_structure_function = self.pipeline.add_c_beam
            self.attach_selection_function = self.pipeline.connect_c_beams

        else:
            warnings.warn(f'Structure "{structure_type}" not available. Using pipe instead.')
            self.add_structure_function = self.pipeline.add_bent_pipe
            self.attach_selection_function = self.pipeline.connect_bent_pipes

        self.sizes_coordinates_changed_callback()
        self.x_line_edit.setFocus()

    def section_callback(self):
        self.set_section_button.setProperty("warning", False)
        self.style().polish(self.set_section_button)

    def material_callback(self):
        self.set_material_button.setProperty("warning", False)
        self.style().polish(self.set_material_button)

    def fluid_callback(self):
        self.set_fluid_button.setProperty("warning", False)
        self.style().polish(self.set_fluid_button)

    def sizes_coordinates_changed_callback(self):
        if not callable(self.add_structure_function):
            return

        try:
            deltas = self._get_deltas()
        except ValueError:
            return

        self.structure_kwargs["curvature_radius"] = self._get_radius()

        self.pipeline.dismiss()
        kwargs = deepcopy(self.structure_kwargs)
        self.add_structure_function(deltas, **kwargs)
        self.render_widget.update_plot()

    def bending_options_changed_callback(self, text: str):
        self.bending_option = text.lower().strip()
        self.bending_radius_line_edit.setDisabled(True)
        self.bending_factor = 0
    
        if self.bending_option == "long radius":
            self.bending_factor = 1.5
            self.bending_radius_line_edit.setText("1.5 * D")

        elif self.bending_option == "short radius":
            self.bending_factor = 1
            self.bending_radius_line_edit.setText("1.0 * D")

        elif self.bending_option == "user-defined":
            self.bending_radius_line_edit.setText("")
            self.bending_radius_line_edit.setDisabled(False)
            self.bending_radius_line_edit.setFocus()
        
        elif self.bending_option == "disabled":
            self.bending_factor = 0
            self.bending_radius_line_edit.setText("disabled")

        else:
            warnings.warn(f'Bending option "{self.bending_option}" not available.')

    def bending_radius_changed_callback(self, text: str):
        try:
            self.user_defined_bending_radius = float(text)
        except ValueError:
            self.user_defined_bending_radius = 0
        else:
            self.sizes_coordinates_changed_callback()

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.render_widget.update_plot()
        self._reset_deltas()

    def attach_selection_callback(self):
        self.pipeline.dismiss()
        if callable(self.attach_selection_function):
            kwargs = deepcopy(self.structure_kwargs)
            self.attach_selection_function(**kwargs)
        self.pipeline.commit()
        self.render_widget.update_plot()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot()
        self._reset_deltas()

    def _get_deltas(self):
        dx = float(self.x_line_edit.text() or 0)
        dy = float(self.y_line_edit.text() or 0)
        dz = float(self.z_line_edit.text() or 0)
        return dx, dy, dz

    def _get_radius(self):
        diameter = self.structure_kwargs.get("diameter", 0)

        if (self.bending_option == "long radius") or (self.bending_option == "short radius"):
            return self.bending_factor * diameter

        elif self.bending_option == "user-defined":
            return self.user_defined_bending_radius

        else:
            return 0

    def _reset_deltas(self):
        self.x_line_edit.setText("")
        self.y_line_edit.setText("")
        self.z_line_edit.setText("")

    def _show_deltas_mode(self, boolean):
        x_text = self.dx_label.text().removeprefix("Δ")
        y_text = self.dy_label.text().removeprefix("Δ")
        z_text = self.dz_label.text().removeprefix("Δ")

        if boolean:
            x_text = "Δ" + x_text
            y_text = "Δ" + y_text
            z_text = "Δ" + z_text
            self.sizes_coords_label.setText("Bounding Box Sizes")
        
        else:
            self.sizes_coords_label.setText("Coordinates")
        
        self.dx_label.setText(x_text)
        self.dy_label.setText(y_text)
        self.dz_label.setText(z_text)

    def _disable_finalize_button(self, boolean):
        pass
