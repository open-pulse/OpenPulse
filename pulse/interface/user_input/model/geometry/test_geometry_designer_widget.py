from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QTabWidget
from PyQt5 import uic
import re
import warnings
from copy import deepcopy

from opps.model import Pipeline, Pipe, Flange, ExpansionJoint, Valve, ReducerEccentric, IBeam, CBeam, TBeam, CircularBeam, RectangularBeam, Beam
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler
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
        self._initialize()
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

    def _initialize(self):
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
        self._update_permissions()

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

        key = self.structure_type
        if self.structure_type in ["pipe", "valve", "flange", "expansion joint"]:
            key = "pipe"

        # Try to get the same cross section used before
        self.current_cross_section_info = self._cached_sections.get(key)

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

        key = self.structure_type
        if self.structure_type in ["pipe", "valve", "flange", "expansion joint"]:
            key = "pipe"

        self._cached_sections[key] = self.current_cross_section_info

        self.cross_section_widget.hide()
        self._update_section_of_selected_structures()
        self._update_permissions()
        self._update_segment_information_text()
        self.xyz_changed_callback()

    def define_material_callback(self):
        self.current_material_info = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self._update_permissions()
        self._update_segment_information_text()

    def xyz_changed_callback(self):
        have_cross_section = self.current_cross_section_info is not None
        needs_cross_section = self.structure_type != "point"

        if needs_cross_section and not have_cross_section:
            return 

        try:
            deltas = self._get_deltas()
        except ValueError:
            return

        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()
        if (self.structure_type != "point") and (deltas == (0, 0, 0)):
            return self.render_widget.update_plot(reset_camera=False)

        self.pipeline.dismiss()
        self._create_current_structure(deltas)
        self._update_permissions()
        self.render_widget.update_plot(reset_camera=True)

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_deltas()

    def attach_selection_callback(self):
        self.pipeline.dismiss()
        self._attach_current_structure()
        self.pipeline.commit()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_deltas()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_deltas()

    def cancel_callback(self):
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.action_front_view_callback()

    def finalize_callback(self):
        self.pipeline.dismiss()

        geometry_handler = GeometryHandler()
        geometry_handler.set_pipeline(self.pipeline)
        geometry_handler.set_length_unit(self.length_unit)
        geometry_handler.export_entity_file()

        self.file.modify_project_attributes(
            length_unit = self.length_unit,
            element_size = 0.01, 
            geometry_tolerance = 1e-6,
            import_type = 1,
        )

        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.plot_entities_with_cross_section()
        app().main_window.action_front_view_callback()
        self.render_widget.set_info_text("")

    def widget_appears_callback(self):
        self._update_permissions()

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
        if self.structure_type == "point":
            self.pipeline.clear_point_selection()
            self.pipeline.add_isolated_point(xyz)
            return

        parameters = self.current_cross_section_info["section_parameters"]
        extra_info = dict(
            cross_section_info = deepcopy(self.current_cross_section_info),
            material_info = self.current_material_info
        )

        if self.structure_type == "pipe":
            extra_info["structural_element_type"] = "pipe_1"
            curvature_radius = self.edit_pipe_widget.get_bending_radius(parameters[0])
            self.pipeline.add_bent_pipe(
                xyz,
                curvature_radius,
                diameter = parameters[0],
                thickness = parameters[1],
                extra_info=extra_info
            )

        elif self.structure_type == "point":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.add_point(xyz)

        elif self.structure_type == "reducer":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.add_reducer_eccentric(
                xyz, 
                initial_diameter = parameters[0],
                final_diameter = parameters[4],
                offset_y = parameters[6],
                offset_z = parameters[7],
                thickness = parameters[1],
                extra_info=extra_info,
            )
        
        elif self.structure_type == "flange":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.add_flange(xyz, extra_info=extra_info)

        elif self.structure_type == "valve":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.add_valve(xyz, extra_info=extra_info)

        elif self.structure_type == "expansion joint":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.add_expansion_joint(xyz, extra_info=extra_info)

        elif self.structure_type == "circular beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.add_circular_beam(
                xyz,
                diameter = parameters[0], 
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "rectangular beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.add_rectangular_beam(
                xyz,
                width = parameters[0],
                height = parameters[1],
                thickness = parameters[2],
                extra_info=extra_info,
            )

        elif self.structure_type == "i-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.add_i_beam(
                xyz,
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )

        elif self.structure_type == "t-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.add_t_beam(
                xyz,
                height = parameters[0],
                width = parameters[1],
                thickness_1 = parameters[2],
                thickness_2 = parameters[3],
                extra_info=extra_info,
            )

        elif self.structure_type == "c-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.add_c_beam(
                xyz,
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )

    def _attach_current_structure(self):
        parameters = self.current_cross_section_info["section_parameters"]
        extra_info = dict(
            cross_section_info = deepcopy(self.current_cross_section_info),
            material_info = self.current_material_info
        )

        if self.structure_type == "pipe":
            extra_info["structural_element_type"] = "pipe_1"
            curvature_radius = self.edit_pipe_widget.get_bending_radius(parameters[0])
            self.pipeline.connect_bent_pipes(
                curvature_radius,
                diameter = parameters[0],
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "reducer":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.connect_reducer_eccentrics(
                initial_diameter = parameters[0],
                final_diameter = parameters[4],
                offset_y = parameters[6],
                offset_z = parameters[7],
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "flange":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.connect_flanges(extra_info=extra_info)

        elif self.structure_type == "valve":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.connect_valves(extra_info=extra_info)

        elif self.structure_type == "expansion joint":
            extra_info["structural_element_type"] = "pipe_1"
            self.pipeline.connect_expansion_joints(extra_info=extra_info)

        elif self.structure_type == "circular beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.connect_circular_beams(
                diameter = parameters[0], 
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "rectangular beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.connect_rectangular_beams(
                width = parameters[0],
                height = parameters[1],
                thickness = parameters[2],
                extra_info=extra_info,
            )

        elif self.structure_type == "i-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.connect_i_beams(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )

        elif self.structure_type == "t-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.connect_t_beams(
                height = parameters[0],
                width = parameters[1],
                thickness_1 = parameters[2],
                thickness_2 = parameters[3],
                extra_info=extra_info,
            )

        elif self.structure_type == "c-beam":
            extra_info["structural_element_type"] = "beam_1"
            self.pipeline.connect_c_beams(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )

    def _update_section_of_selected_structures(self):
        parameters = self.current_cross_section_info["section_parameters"]
        extra_info = dict(
            cross_section_info = deepcopy(self.current_cross_section_info),
            material_info = self.current_material_info
        )

        if self.structure_type in ["pipe", "valve", "flange", "expansion joints"]:
            valid_type = Pipe | Valve | Flange | ExpansionJoint
            extra_info["structural_element_type"] = "pipe_1"
            kwargs = dict(
                diameter = parameters[0], 
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "reducer":
            valid_type = ReducerEccentric
            extra_info["structural_element_type"] = "pipe_1"
            kwargs = dict(
                initial_diameter = parameters[0],
                final_diameter = parameters[4],
                offset_y = parameters[6],
                offset_z = parameters[7],
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "circular beam":
            valid_type = CircularBeam
            extra_info["structural_element_type"] = "beam_1"
            kwargs = dict(
                diameter = parameters[0], 
                thickness = parameters[1],
                extra_info=extra_info,
            )

        elif self.structure_type == "rectangular beam":
            valid_type = RectangularBeam
            extra_info["structural_element_type"] = "beam_1"
            kwargs = dict(
                width = parameters[0],
                height = parameters[1],
                thickness = parameters[2],
                extra_info=extra_info,
            )

        elif self.structure_type == "i-beam":
            valid_type = IBeam
            extra_info["structural_element_type"] = "beam_1"
            kwargs = dict(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )

        elif self.structure_type == "t-beam":
            valid_type = TBeam
            extra_info["structural_element_type"] = "beam_1"
            kwargs = dict(
                height = parameters[0],
                width = parameters[1],
                thickness_1 = parameters[2],
                thickness_2 = parameters[3],
                extra_info=extra_info,
            )

        elif self.structure_type == "c-beam":
            valid_type = CBeam
            extra_info["structural_element_type"] = "beam_1"
            kwargs = dict(
                height = parameters[0],
                width_1 = parameters[1],
                width_2 = parameters[3],
                thickness_1 = parameters[2],
                thickness_2 = parameters[4],
                thickness_3 = parameters[5],
                extra_info=extra_info,
            )
        
        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, valid_type):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)

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
        # usefull variables
        have_selection = bool(self.pipeline.selected_points or self.pipeline.selected_structures)
        have_staged = bool(self.pipeline.staged_points or self.pipeline.staged_structures)
        have_cross_section = self.current_cross_section_info is not None
        multiple_points_selected = len(self.pipeline.selected_points) >= 1
        is_point = self.structure_type == "point"
        is_beam = ("beam" in self.structure_type) 

        self.set_section_button.setDisabled(is_point)
        self.set_material_button.setDisabled(is_point)
        self.set_fluid_button.setDisabled(is_beam or is_point)

        self.add_button.setDisabled(not have_staged)
        self.delete_button.setDisabled(not (have_selection or have_staged))
        self.attach_button.setDisabled(
            is_point
            or not have_cross_section
            or not multiple_points_selected
        )

        enable_xyz = (not is_point and not have_cross_section)
        self.x_line_edit.setDisabled(enable_xyz)
        self.y_line_edit.setDisabled(enable_xyz)
        self.z_line_edit.setDisabled(enable_xyz)
        self.set_section_button.setProperty("warning", enable_xyz)
        self.style().polish(self.set_section_button)

    def _load_project(self):
        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_widget.initial_project_action(True)
        self.complete = True
