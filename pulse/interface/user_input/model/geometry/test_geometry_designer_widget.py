from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5 import uic
import re
import warnings

from opps.model import Pipeline
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget

from pulse import app, UI_DIR
from pulse.interface.user_input.model.geometry.test_edit_pipe_widget import EditPipeWidget
from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs


class GeometryDesignerWidget(QWidget):
    def __init__(self, render_widget: EditorRenderWidget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/test_geometry_designer_widget.ui"
        uic.loadUi(ui_path, self)

        self.render_widget = render_widget

        self.project = app().project
        self.pipeline = self.project.pipeline
        self.file = self.project.file

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

        self.options_stack_widget: QStackedWidget
        self.empty_widget: QWidget

        self.add_button: QPushButton
        self.attach_button: QPushButton
        self.delete_button: QPushButton

        self.cancel_button: QPushButton
        self.finalize_button: QPushButton
    
    def _create_layout(self):
        self.edit_pipe_widget = EditPipeWidget(self)
        self.options_stack_widget.addWidget(self.edit_pipe_widget)

        self.cross_section_widget = CrossSectionWidget(self)
        self.material_widget = MaterialInputs(self)

        self.cross_section_widget.hide()
        self.material_widget.hide()

    def _create_connections(self):
        self.render_widget.selection_changed.connect(self.selection_callback)

        self.unit_combobox.currentTextChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_type_changed_callback)
        
        self.set_section_button.clicked.connect(self.show_cross_section_widget_callback)
        self.set_material_button.clicked.connect(self.show_material_widget_callback)
        self.set_fluid_button.clicked.connect(self.show_fluid_widget_callback)

        self.x_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.y_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.z_line_edit.textEdited.connect(self.xyz_changed_callback)

        self.edit_pipe_widget.edited.connect(self.xyz_changed_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)

        self.cancel_button.clicked.connect(self.cancel_callback)
        self.finalize_button.clicked.connect(self.finalize_callback)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section_callback)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section_callback)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material_callback)

    def _initial_configuration(self):
        self.current_material_info = None
        self.current_cross_section_info = None
        self._cached_sections = dict()

        self.set_section_button.setProperty("warning", True)
        self.set_material_button.setProperty("warning", False)
        self.set_fluid_button.setProperty("warning", False)

        self.style().polish(self.set_section_button)
        self.style().polish(self.set_material_button)
        self.style().polish(self.set_fluid_button)

        self.unity_changed_callback("meter")
        self.structure_type_changed_callback("pipe")

    def selection_callback(self):
        if len(self.pipeline.selected_points) > 1:
            self.attach_button.setEnabled(True)
        else:
            self.attach_button.setDisabled(True)

        has_selection = self.pipeline.selected_points or self.pipeline.selected_structures
        has_staged = self.pipeline.staged_points or self.pipeline.staged_structures
        if has_selection or has_staged:
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setDisabled(True)
        
        if has_staged:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setDisabled(True)

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
        self.structure_type = structure_type.lower().strip()
        self.options_stack_widget.setCurrentWidget(self.empty_widget)
        self._show_deltas_mode(True)

        if self.structure_type == "pipe":
            self.options_stack_widget.setCurrentWidget(self.edit_pipe_widget)

        elif self.structure_type == "point":
            self._show_deltas_mode(False)

        # Try to get the same cross section used before
        self.current_cross_section_info = self._cached_sections.get(self.structure_type)

        self._update_permissions()
        self._update_segment_information_text()
        self.xyz_changed_callback()
        self.x_line_edit.setFocus()

    def show_cross_section_widget_callback(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     

        # Configure visible cross section tabs
        if self.structure_type in ["pipe", "flange", "valve", "expansion_joint"]:
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
            self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        
        elif self.structure_type == "reducer":
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(1, True)
            self.cross_section_widget.lineEdit_outside_diameter_initial.setFocus()

        elif self.structure_type == "rectangular beam":
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(0, True)
            self.cross_section_widget.lineEdit_base_rectangular_section.setFocus()

        elif self.structure_type == "circular beam":
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(1, True)
            self.cross_section_widget.lineEdit_outside_diameter_circular_section.setFocus()

        elif self.structure_type == "c-beam":
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(2, True)
            self.cross_section_widget.lineEdit_height_C_section.setFocus()

        elif self.structure_type == "i-beam":
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(3, True)
            self.cross_section_widget.lineEdit_height_I_section.setFocus()

        elif self.structure_type == "t-beam":
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(4, True)
            self.cross_section_widget.lineEdit_height_T_section.setFocus()

        else:
            return

        self.cross_section_widget.setVisible(True)

    def show_material_widget_callback(self):
        self.material_widget._initialize()
        self.material_widget._add_icon_and_title()
        self.material_widget.load_data_from_materials_library()
        self.material_widget.setVisible(True)

    def show_fluid_widget_callback(self):
        pass 

    def define_cross_section_callback(self):
        beam_structure_types = [
            "circular beam",
            "rectangular beam",
            "i-beam",
            "t-beam",
            "c-beam"
        ]

        if self.structure_type == "pipe":
            if self.cross_section_widget.get_constant_pipe_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.pipe_section_info

        elif self.structure_type == "reducer":
            if self.cross_section_widget.get_variable_section_pipe_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.pipe_section_info

        elif self.structure_type in beam_structure_types:
            if self.cross_section_widget.get_beam_section_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.beam_section_info

        else:
            return

        self._cached_sections[self.structure_type] = self.current_cross_section_info

        self.cross_section_widget.hide()
        self._update_permissions()
        self._update_segment_information_text()
        self.xyz_changed_callback()

    def define_material_callback(self):
        self.current_material_info = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self._update_permissions()
        self._update_segment_information_text()

    def xyz_changed_callback(self):
        if self.current_cross_section_info is None:
            return

        try:
            deltas = self._get_deltas()
        except ValueError:
            return
        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        if deltas == (0, 0, 0):
            return self.render_widget.update_plot()
        
        self._create_current_structure(deltas)
        self.add_button.setEnabled(True)
        self.render_widget.update_plot()

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.render_widget.update_plot()
        self._reset_deltas()

    def attach_selection_callback(self):
        self.pipeline.dismiss()
        self._attach_current_structure()
        self.pipeline.commit()
        self.render_widget.update_plot()
        self._reset_deltas()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot()
        self._reset_deltas()

    def cancel_callback(self):
        pass

    def finalize_callback(self):
        pass

    def widget_appears_callback(self):
        self.attach_button.setDisabled(True)
        self.delete_button.setDisabled(True)
        self.add_button.setDisabled(True)

        self.x_line_edit.setDisabled(True)
        self.y_line_edit.setDisabled(True)
        self.z_line_edit.setDisabled(True)

    def widget_disappears_callback(self):
        pass

    def _get_deltas(self):
        dx = float(self.x_line_edit.text() or 0)
        dy = float(self.y_line_edit.text() or 0)
        dz = float(self.z_line_edit.text() or 0)
        return dx, dy, dz

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
    
    def _create_current_structure(self, xyz):
        parameters = self.current_cross_section_info["section_parameters"]

        if self.structure_type == "pipe":
            curvature_radius = self.edit_pipe_widget.get_bending_radius(parameters[0])
            self.pipeline.add_bent_pipe(xyz, curvature_radius, diameter = parameters[0], thickness = parameters[1])

        elif self.structure_type == "point":
            self.pipeline.add_point(xyz)

        elif self.structure_type == "reducer":
            self.pipeline.add_reducer_eccentric(
                xyz, 
                initial_diameter = parameters[0],
                final_diameter = parameters[4],
                offset_y = parameters[6],
                offset_z = parameters[7],
                thickness = parameters[1]
            )
        
        elif self.structure_type == "flange":
            self.pipeline.add_flange(xyz)

        elif self.structure_type == "valve":
            self.pipeline.add_valve(xyz)

        elif self.structure_type == "expansion joint":
            self.pipeline.add_expansion_joint(xyz)

        elif self.structure_type == "circular beam":
            self.pipeline.add_circular_beam(
                xyz,
                diameter = parameters[0], 
                thickness = parameters[1]
            )

        elif self.structure_type == "rectangular beam":
            self.pipeline.add_rectangular_beam(
                xyz,
                width = parameters[0],
                height = parameters[1],
                thickness = parameters[2]
            )

        elif self.structure_type == "i-beam":
            self.pipeline.add_i_beam(
                xyz,
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
            )

        elif self.structure_type == "t-beam":
            self.pipeline.add_t_beam(
                xyz,
                height = parameters[0],
                width = parameters[1],
                thickness_1 = parameters[2],
                thickness_2 = parameters[3],
            )

        elif self.structure_type == "c-beam":
            self.pipeline.add_c_beam(
                xyz,
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
            )

        else:
            warnings.warn(f'Structure "{self.structure_type}" not available.')

    def _attach_current_structure(self):
        parameters = self.current_cross_section_info["section_parameters"]

        if self.structure_type == "pipe":
            curvature_radius = self.edit_pipe_widget.get_bending_radius(parameters[0])
            self.pipeline.connect_bent_pipes(curvature_radius, diameter = parameters[0], thickness = parameters[1])

        elif self.structure_type == "reducer":
            self.pipeline.connect_reducer_eccentrics(
                initial_diameter = parameters[0],
                final_diameter = parameters[4],
                offset_y = parameters[6],
                offset_z = parameters[7],
                thickness = parameters[1]
            )

        elif self.structure_type == "flange":
            self.pipeline.connect_flanges()

        elif self.structure_type == "valve":
            self.pipeline.connect_valves()

        elif self.structure_type == "expansion joint":
            self.pipeline.connect_expansion_joints()

        elif self.structure_type == "circular beam":
            self.pipeline.connect_circular_beams(
                diameter = parameters[0], 
                thickness = parameters[1]
            )

        elif self.structure_type == "rectangular beam":
            self.pipeline.connect_rectangular_beams(
                width = parameters[0],
                height = parameters[1],
                thickness = parameters[2]
            )

        elif self.structure_type == "i-beam":
            self.pipeline.connect_i_beams(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
            )

        elif self.structure_type == "t-beam":
            self.pipeline.connect_t_beams(
                height = parameters[0],
                width = parameters[1],
                thickness_1 = parameters[2],
                thickness_2 = parameters[3],
            )

        elif self.structure_type == "c-beam":
            self.pipeline.connect_c_beams(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
            )

        else:
            warnings.warn(f'Structure "{self.structure_type}" not available to attach.')

    def _update_segment_information_text(self):
        section_label = ""
        section_parameters = ""
        if self.current_cross_section_info is not None:
            section_label = self.current_cross_section_info["section_type_label"]
            section_parameters = self.current_cross_section_info["section_parameters"]

        material_id = ""
        material_data = None
        if self.current_material_info is not None:
            material_id = self.current_material_info
            material_data = self.file.get_material_properties(material_id)

        message = "Active configuration\n\n"

        if self.current_cross_section_info is not None:
            if section_label == "Pipe section":
                if len(section_parameters) == 6:
                    message += f"Section type: {section_label} (constant)\n"
                else:
                    message += f"Section type: {section_label} (variable)\n"
            else:
                message += f"Section type: {section_label}\n"
            message += f"Section data: {section_parameters}\n\n"

        if material_data is not None:
            message += f"Material name: {material_data[0]}\n"
            message += f"Material data: {material_data[1:]}\n\n"

        self.render_widget.set_info_text(message)

    def _update_permissions(self):
        hide_cross_section = (self.structure_type in ["point"])
        hide_material = (self.structure_type in ["point"])
        hide_fluid = ("beam" in self.structure_type)

        self.set_section_button.setDisabled(hide_cross_section)
        self.set_material_button.setDisabled(hide_material)
        self.set_fluid_button.setDisabled(hide_fluid)

        missing_cross_section = (self.current_cross_section_info is None
                                 and not hide_cross_section)
        self.x_line_edit.setDisabled(missing_cross_section)
        self.y_line_edit.setDisabled(missing_cross_section)
        self.z_line_edit.setDisabled(missing_cross_section)
        self.set_section_button.setProperty("warning", missing_cross_section)
        self.style().polish(self.set_section_button)
