from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QAction
from PyQt5 import uic
import re
import numpy as np
import warnings
from copy import deepcopy
from opps.model import Point, Pipe, Flange, ExpansionJoint, Valve, Reducer, IBeam, CBeam, TBeam, CircularBeam, RectangularBeam, Beam
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget

from pulse import app, UI_DIR
from pulse.interface.viewer_3d.text_templates import TreeInfo
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

        self.select_all_action: QAction
        self.addAction(self.select_all_action)
    
    def _create_layout(self):
        self.edit_pipe_widget = EditPipeWidget(self)
        self.options_stack_widget.addWidget(self.edit_pipe_widget)

        self.cross_section_widget = CrossSectionWidget(self)
        self.material_widget = MaterialInputs(self)

        self.cross_section_widget.hide()
        self.material_widget.hide()

    def _create_connections(self):
        self.render_widget.selection_changed.connect(self.selection_callback)
        self.select_all_action.triggered.connect(self.select_all_callback)

        self.unit_combobox.currentTextChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_type_changed_callback)
        
        self.set_section_button.clicked.connect(self.show_cross_section_widget_callback)
        self.set_material_button.clicked.connect(self.show_material_widget_callback)
        self.set_fluid_button.clicked.connect(self.show_fluid_widget_callback)

        self.x_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.y_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.z_line_edit.textEdited.connect(self.xyz_changed_callback)

        self.edit_pipe_widget.edited.connect(self.pipe_editor_changed_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)

        self.cancel_button.clicked.connect(self.cancel_callback)
        self.finalize_button.clicked.connect(self.finalize_callback)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section_callback)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section_callback)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material_callback)

    def _initialize(self):
        self.current_structure_type = None
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
        if issubclass(self.current_structure_type, Point):
            self._set_xyz_to_selected_point()
        self._update_information_text()
        self._update_permissions()

    def select_all_callback(self):
        self.pipeline.select_points(self.pipeline.points)
        self.pipeline.select_structures(self.pipeline.structures)
        self.render_widget.update_selection()

    def unity_changed_callback(self, text: str):
        self.length_unit = text.lower().strip()
        unit_label_text = self._unit_abreviation(self.length_unit)

        if unit_label_text is None:
            return

        # Automatically replace every label in the format [m] or [mm] or [in]
        unit_pattern = re.compile(r"\[(m|mm|in)\]")
        for label in self.findChildren(QLabel):
            if unit_pattern.match(label.text()) is not None:
                label.setText(unit_label_text)

    def structure_type_changed_callback(self, structure_name: str):
        # the previous value before this change
        if (self.current_structure_type is not None) and issubclass(self.current_structure_type, Point):
            self._reset_xyz()

        structure_name = structure_name.lower().strip()
        self.current_structure_type = self._structure_name_to_class(structure_name)    

        self.options_stack_widget.setCurrentWidget(self.empty_widget)
        self._show_deltas_mode(True)

        if issubclass(self.current_structure_type, Pipe):
            self.options_stack_widget.setCurrentWidget(self.edit_pipe_widget)

        elif issubclass(self.current_structure_type, Point):
            self._show_deltas_mode(False)

        key = self.current_structure_type
        # temporary until these structures are properly represented
        if issubclass(self.current_structure_type, (Pipe, Valve, Flange, ExpansionJoint)):
            key = Pipe

        # Try to get the same cross section used before
        self.current_cross_section_info = self._cached_sections.get(key)

        self._update_permissions()
        self._update_information_text()

        if issubclass(self.current_structure_type, Point):
            self.pipeline.dismiss()
            self.pipeline.clear_structure_selection()
            self._set_xyz_to_selected_point()
            self.render_widget.update_plot(reset_camera=False)
        else:
            self.xyz_changed_callback()

        self.x_line_edit.setFocus()

    def show_cross_section_widget_callback(self):
        self.cross_section_widget._add_icon_and_title()
        self.cross_section_widget.set_inputs_to_geometry_creator()     
        self.cross_section_widget.hide_all_tabs()     

        # Configure visible cross section tabs
        # temporary configuration until the specific configurations are implemented
        if issubclass(self.current_structure_type, (Pipe, Flange, Valve, ExpansionJoint)):
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(0, True)
            self.cross_section_widget.lineEdit_outside_diameter.setFocus()
        
        elif issubclass(self.current_structure_type, Reducer):
            self.cross_section_widget.tabWidget_general.setTabVisible(0, True)
            self.cross_section_widget.tabWidget_pipe_section.setTabVisible(1, True)
            self.cross_section_widget.lineEdit_outside_diameter_initial.setFocus()

        elif issubclass(self.current_structure_type, RectangularBeam):
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(0, True)
            self.cross_section_widget.lineEdit_base_rectangular_section.setFocus()

        elif issubclass(self.current_structure_type, CircularBeam):
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(1, True)
            self.cross_section_widget.lineEdit_outside_diameter_circular_section.setFocus()

        elif issubclass(self.current_structure_type, CBeam):
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(2, True)
            self.cross_section_widget.lineEdit_height_C_section.setFocus()

        elif issubclass(self.current_structure_type, IBeam):
            self.cross_section_widget.tabWidget_general.setTabVisible(1, True)
            self.cross_section_widget.tabWidget_beam_section.setTabVisible(3, True)
            self.cross_section_widget.lineEdit_height_I_section.setFocus()

        elif issubclass(self.current_structure_type, TBeam):
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
        if issubclass(self.current_structure_type, Pipe):
            if self.cross_section_widget.get_constant_pipe_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.pipe_section_info

        elif issubclass(self.current_structure_type, Reducer):
            if self.cross_section_widget.get_variable_section_pipe_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.pipe_section_info

        elif issubclass(self.current_structure_type, Beam):
            if self.cross_section_widget.get_beam_section_parameters():
                return
            self.current_cross_section_info = self.cross_section_widget.beam_section_info

        else:
            return

        key = self.current_structure_type
        # temporary until these structures are properly represented
        if issubclass(self.current_structure_type, (Pipe, Valve, Flange, ExpansionJoint)):
            key = Pipe

        self._cached_sections[key] = self.current_cross_section_info

        self.cross_section_widget.hide()
        self._update_section_of_selected_structures()
        self._update_permissions()
        self._update_information_text()
        self.x_line_edit.setFocus()
        self.xyz_changed_callback()

    def define_material_callback(self):
        self.current_material_info = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self._update_material_of_selected_structures()
        self._update_permissions()
        self._update_information_text()
        self.render_widget.update_plot(reset_camera=False)

    def xyz_changed_callback(self):
        try:
            xyz = self._get_xyz()
        except ValueError:
            return

        if issubclass(self.current_structure_type, Point):
            self._xyz_point_callback(xyz)
        else:
            self._xyz_structure_callback(xyz)

        self._update_permissions()
    
    def pipe_editor_changed_callback(self):
        self.render_widget.update_plot(reset_camera=False)
        self._update_permissions()

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_xyz()

    def attach_selection_callback(self):
        self.pipeline.dismiss()
        _, attach_function, kwargs = self._get_current_structure_functions()
        attach_function(**kwargs)
        self.pipeline.commit()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_xyz()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_xyz()

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

        self._load_project()

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

    def _get_xyz(self):
        dx = float(self.x_line_edit.text() or 0)
        dy = float(self.y_line_edit.text() or 0)
        dz = float(self.z_line_edit.text() or 0)
        return dx, dy, dz

    def _set_xyz(self, x, y, z):
        self.x_line_edit.setText(str(x))
        self.y_line_edit.setText(str(y))
        self.z_line_edit.setText(str(z))

    def _reset_xyz(self):
        self._set_xyz("", "", "")
    
    def _set_xyz_to_selected_point(self):
        if len(self.pipeline.selected_points) != 1:
            return

        x, y, z = np.round(self.pipeline.selected_points[0].coords(), 6)
        self._set_xyz(x, y, z)

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

    def _xyz_point_callback(self, xyz):
        if len(self.pipeline.selected_points) == 1:
            # Edit selected point
            self.pipeline.selected_points[0].set_coords(*xyz)
            self.pipeline.recalculate_curvatures()
        else:
            # Create new point
            self.pipeline.dismiss()
            self.pipeline.clear_selection()
            add_function, _, kwargs = self._get_current_structure_functions()
            add_function(xyz, **kwargs)

        self.render_widget.update_plot(reset_camera=True)

    def _xyz_structure_callback(self, xyz):
        if self.current_cross_section_info is None:
            return 
        
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()

        if xyz == (0, 0, 0):
            self.render_widget.update_plot(reset_camera=False)
            return

        add_function, _, kwargs = self._get_current_structure_functions()
        add_function(xyz, **kwargs)
        self.render_widget.update_plot(reset_camera=True)

    def _update_section_of_selected_structures(self):
        _, _, kwargs = self._get_current_structure_functions()

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, self.current_structure_type):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)
    
    def _update_material_of_selected_structures(self):
        for structure in self.pipeline.selected_structures:
            structure.extra_info["material_info"] =  self.current_material_info

    def _unit_abreviation(self, unit):
        if self.length_unit == "meter":
            return "[m]"

        elif self.length_unit == "milimeter":
            return "[mm]"

        elif self.length_unit == "inch":
            return "[in]"

        else:
            return

    def _structure_name_to_class(self, structure_name: str):
        if structure_name == "point":
            return Point
        
        elif structure_name == "pipe":
            return Pipe

        elif structure_name == "flange":
            return Flange

        elif structure_name == "valve":
            return Valve

        elif structure_name == "expansion joint":
            return ExpansionJoint

        elif structure_name == "reducer":
            return Reducer

        elif structure_name == "circular beam":
            return CircularBeam

        elif structure_name == "rectangular beam":
            return RectangularBeam

        elif structure_name == "i-beam":
            return IBeam

        elif structure_name == "t-beam":
            return TBeam

        elif structure_name == "c-beam":
            return CBeam

    def _get_current_structure_functions(self):
        add_function = None
        attach_function = None
        kwargs = dict()

        if issubclass(self.current_structure_type, Point):
            add_function = self.pipeline.add_isolated_point
            return add_function, attach_function, kwargs

        # all other structures need a cross section defined
        if self.current_cross_section_info is None:
            return add_function, attach_function, kwargs

        parameters = self.current_cross_section_info["section_parameters"]
        kwargs["extra_info"] = dict(
            cross_section_info = deepcopy(self.current_cross_section_info),
            material_info = self.current_material_info
        )
        
        if issubclass(self.current_structure_type, Pipe):
            add_function = self.pipeline.add_bent_pipe
            attach_function = self.pipeline.connect_bent_pipes
            _curvature_radius = self.edit_pipe_widget.get_bending_radius(parameters[0])
            kwargs["curvature_radius"] = _curvature_radius
            kwargs["diameter"] = parameters[0]
            kwargs["thickness"] = parameters[1]
            kwargs["extra_info"]["structural_element_type"] = "pipe_1"

        elif issubclass(self.current_structure_type, Flange):
            add_function = self.pipeline.add_flange
            attach_function = self.pipeline.connect_flanges
            kwargs["diameter"] = parameters[0]
            kwargs["thickness"] = parameters[1]
            kwargs["extra_info"]["structural_element_type"] = "pipe_1"
            # add remaining valve info here

        elif issubclass(self.current_structure_type, Valve):
            add_function = self.pipeline.add_valve
            attach_function = self.pipeline.connect_valves
            kwargs["diameter"] = parameters[0]
            kwargs["thickness"] = parameters[1]
            kwargs["extra_info"]["structural_element_type"] = "pipe_1"
            # add remaining valve info here

        elif issubclass(self.current_structure_type, ExpansionJoint):
            add_function = self.pipeline.add_expansion_joint
            attach_function = self.pipeline.connect_expansion_joints
            kwargs["diameter"] = parameters[0]
            kwargs["thickness"] = parameters[1]
            kwargs["extra_info"]["structural_element_type"] = "pipe_1"
            # add remaining valve info here

        elif issubclass(self.current_structure_type, Reducer):
            add_function = self.pipeline.add_reducer_eccentric
            attach_function = self.pipeline.connect_reducer_eccentrics
            kwargs["initial_diameter"] = parameters[0]
            kwargs["final_diameter"] = parameters[4]
            kwargs["thickness"] = parameters[1]
            kwargs["initial_offset_y"] = -parameters[2]
            kwargs["initial_offset_z"] = parameters[3]
            kwargs["final_offset_y"] = -parameters[6]
            kwargs["final_offset_z"] = parameters[7]
            kwargs["extra_info"]["structural_element_type"] = "pipe_1"

        elif issubclass(self.current_structure_type, CircularBeam):
            add_function = self.pipeline.add_circular_beam
            attach_function = self.pipeline.connect_circular_beams
            kwargs["diameter"] = parameters[0]
            kwargs["thickness"] = parameters[1]
            kwargs["extra_info"]["structural_element_type"] = "beam_1"

        elif issubclass(self.current_structure_type, RectangularBeam):
            add_function = self.pipeline.add_rectangular_beam
            attach_function = self.pipeline.connect_rectangular_beams
            kwargs["width"] = parameters[0]
            kwargs["height"] = parameters[1]
            kwargs["thickness"] = (parameters[0] - parameters[2]) / 2
            kwargs["extra_info"]["structural_element_type"] = "beam_1"

        elif issubclass(self.current_structure_type, IBeam):
            add_function = self.pipeline.add_i_beam
            attach_function = self.pipeline.connect_i_beams
            kwargs["height"] = parameters[0]
            kwargs["width_1"] = parameters[1]
            kwargs["width_2"] = parameters[3]
            kwargs["thickness_1"] = parameters[2]
            kwargs["thickness_2"] = parameters[4]
            kwargs["thickness_3"] = parameters[5]
            kwargs["extra_info"]["structural_element_type"] = "beam_1"

        elif issubclass(self.current_structure_type, TBeam):
            add_function = self.pipeline.add_t_beam
            attach_function = self.pipeline.connect_t_beams
            kwargs["height"] = parameters[0]
            kwargs["width"] = parameters[1]
            kwargs["thickness_1"] = parameters[2]
            kwargs["thickness_2"] = parameters[3]
            kwargs["extra_info"]["structural_element_type"] = "beam_1"

        elif issubclass(self.current_structure_type, CBeam):
            add_function = self.pipeline.add_c_beam
            attach_function = self.pipeline.connect_c_beams
            kwargs["height"] = parameters[0]
            kwargs["width_1"] = parameters[1]
            kwargs["width_2"] = parameters[3]
            kwargs["thickness_1"] = parameters[2]
            kwargs["thickness_2"] = parameters[4]
            kwargs["thickness_3"] = parameters[5]
            kwargs["extra_info"]["structural_element_type"] = "beam_1"
    
        return add_function, attach_function, kwargs

    def _update_information_text(self):
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

        if len(self.pipeline.selected_points) == 2:
            a = self.pipeline.selected_points[0].coords()
            b = self.pipeline.selected_points[1].coords()
            dx, dy, dz = np.round(np.abs(a - b), 6)
            distance = np.round(np.linalg.norm(a - b), 6)

            unit = self._unit_abreviation(self.length_unit)
            tree = TreeInfo("Distance:")
            tree.add_item("Total", distance, unit)
            tree.add_item("ΔX", dx, unit)
            tree.add_item("ΔY", dy, unit)
            tree.add_item("ΔZ", dz, unit)
            message += str(tree) + "\n\n"

        self.render_widget.set_info_text(message)

    def _update_permissions(self):
        # usefull variables
        have_selection = bool(self.pipeline.selected_points or self.pipeline.selected_structures)
        have_staged = bool(self.pipeline.staged_points or self.pipeline.staged_structures)
        have_cross_section = self.current_cross_section_info is not None
        multiple_points_selected = len(self.pipeline.selected_points) >= 1
        is_point = issubclass(self.current_structure_type, Point)
        is_beam = issubclass(self.current_structure_type, Beam)

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
