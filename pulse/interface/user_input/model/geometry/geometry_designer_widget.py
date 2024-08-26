from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QStackedWidget, QAction, QSlider, QSpinBox
from PyQt5 import uic
import re
from numbers import Number
import numpy as np
import math
from copy import deepcopy
from opps.model import Point, Pipe, Bend, Flange, ExpansionJoint, Valve, Reducer, IBeam, CBeam, TBeam, CircularBeam, RectangularBeam, Beam
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget

from pulse import app, UI_DIR
from molde.utils import TreeInfo
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.geometry.edit_pipe_widget import EditPipeWidget
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.interface.user_input.model.setup.material.material_widget import MaterialInputs

from pulse.interface.user_input.model.geometry.pipe_options_widget import PipeOptionsWidget
from pulse.interface.user_input.model.geometry.reducer_options_widget import ReducerOptionsWidget
from pulse.interface.user_input.model.geometry.flange_options_widget import FlangeOptionsWidget
from pulse.interface.user_input.model.geometry.valve_options_widget import ValveOptionsWidget
from pulse.interface.user_input.model.geometry.expansion_joint_options_widget import ExpansionJointOptionsWidget
from pulse.interface.user_input.model.geometry.rectangular_beam_options_widget import RectangularBeamOptionsWidget
from pulse.interface.user_input.model.geometry.circular_beam_options_widget import CircularBeamOptionsWidget
from pulse.interface.user_input.model.geometry.t_beam_options_widget import TBeamOptionsWidget
from pulse.interface.user_input.model.geometry.i_beam_options_widget import IBeamOptionsWidget
from pulse.interface.user_input.model.geometry.c_beam_options_widget import CBeamOptionsWidget


class GeometryDesignerWidget(QWidget):
    def __init__(self, render_widget: EditorRenderWidget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/geometry_designer_widget.ui"
        uic.loadUi(ui_path, self)

        self.render_widget = render_widget

        self.project = app().project
        self.pipeline = self.project.pipeline

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self._initialize()

    def _define_qt_variables(self):
        self.unit_combobox: QComboBox
        self.structure_combobox: QComboBox

        self.set_material_button: QPushButton
        self.set_fluid_button: QPushButton

        self.x_line_edit: QLineEdit
        self.y_line_edit: QLineEdit
        self.z_line_edit: QLineEdit

        self.sizes_coords_label: QLabel
        self.dx_label: QLabel
        self.dy_label: QLabel
        self.dz_label: QLabel

        self.division_combobox: QComboBox
        self.division_slider: QSlider
        self.cancel_division_button: QPushButton
        self.apply_division_button: QPushButton
        self.division_amount_spinbox: QSpinBox
        self.division_slider_label: QLabel

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
        self.cross_section_widget = CrossSectionWidget()

        self.pipe_options_widget = PipeOptionsWidget(self)
        self.reducer_options_widget = ReducerOptionsWidget(self)
        self.flange_options_widget = FlangeOptionsWidget(self)
        self.valve_options_widget = ValveOptionsWidget(self)
        self.expansion_joint_options_widget = ExpansionJointOptionsWidget(self)
        self.rectangular_beam_options_widget = RectangularBeamOptionsWidget(self)
        self.circular_beam_options_widget = CircularBeamOptionsWidget(self)
        self.t_beam_options_widget = TBeamOptionsWidget(self)
        self.i_beam_options_widget = IBeamOptionsWidget(self)
        self.c_beam_options_widget = CBeamOptionsWidget(self)

        self.options_stack_widget.addWidget(self.pipe_options_widget)
        self.options_stack_widget.addWidget(self.reducer_options_widget)
        self.options_stack_widget.addWidget(self.flange_options_widget)
        self.options_stack_widget.addWidget(self.valve_options_widget)
        self.options_stack_widget.addWidget(self.expansion_joint_options_widget)
        self.options_stack_widget.addWidget(self.rectangular_beam_options_widget)
        self.options_stack_widget.addWidget(self.circular_beam_options_widget)
        self.options_stack_widget.addWidget(self.t_beam_options_widget)
        self.options_stack_widget.addWidget(self.i_beam_options_widget)
        self.options_stack_widget.addWidget(self.c_beam_options_widget)

        self.material_widget = MaterialInputs(self)
        self.material_widget.hide()

    def _create_connections(self):
        self.render_widget.selection_changed.connect(self.selection_callback)
        self.select_all_action.triggered.connect(self.select_all_callback)

        self.unit_combobox.currentTextChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_type_changed_callback)
        self.set_material_button.clicked.connect(self.show_material_widget_callback)
        self.set_fluid_button.clicked.connect(self.show_fluid_widget_callback)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material_callback)

        self.x_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.y_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.z_line_edit.textEdited.connect(self.xyz_changed_callback)

        self.x_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)
        self.y_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)
        self.z_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)

        self.division_combobox.currentTextChanged.connect(self.division_type_changed_callback)
        self.division_slider.valueChanged.connect(self.division_slider_callback)
        self.division_amount_spinbox.textChanged.connect(self.division_amount_spinbox_callback)
        self.cancel_division_button.clicked.connect(self.cancel_division_callback)
        self.apply_division_button.clicked.connect(self.apply_division_callback)

        self.pipe_options_widget.edited.connect(self.options_changed_callback)
        self.reducer_options_widget.edited.connect(self.options_changed_callback)
        self.flange_options_widget.edited.connect(self.options_changed_callback)
        self.valve_options_widget.edited.connect(self.options_changed_callback)
        self.expansion_joint_options_widget.edited.connect(self.options_changed_callback)
        self.rectangular_beam_options_widget.edited.connect(self.options_changed_callback)
        self.circular_beam_options_widget.edited.connect(self.options_changed_callback)
        self.t_beam_options_widget.edited.connect(self.options_changed_callback)
        self.i_beam_options_widget.edited.connect(self.options_changed_callback)
        self.c_beam_options_widget.edited.connect(self.options_changed_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)

        self.cancel_button.clicked.connect(self.cancel_callback)
        self.finalize_button.clicked.connect(self.finalize_callback)

    def _initialize(self):
        self.current_structure_type = None
        self.current_material_info = None
        self._cached_sections = dict()

        self.unity_changed_callback("meter")
        self.structure_type_changed_callback("pipe")
        self.division_type_changed_callback("single division")

    def selection_callback(self):
        if issubclass(self.current_structure_type, Point):
            self._set_xyz_to_selected_point()

        if not self.pipeline.selected_structures:
            self.cancel_division_callback()

        self._update_permissions()
        self._update_information_text()

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
            self.options_stack_widget.setCurrentWidget(self.pipe_options_widget)

        elif issubclass(self.current_structure_type, Reducer):
            self.options_stack_widget.setCurrentWidget(self.reducer_options_widget)

        elif issubclass(self.current_structure_type, Flange):
            self.options_stack_widget.setCurrentWidget(self.flange_options_widget)

        elif issubclass(self.current_structure_type, Valve):
            self.options_stack_widget.setCurrentWidget(self.valve_options_widget)

        elif issubclass(self.current_structure_type, ExpansionJoint):
            self.options_stack_widget.setCurrentWidget(self.expansion_joint_options_widget)

        elif issubclass(self.current_structure_type, RectangularBeam):
            self.options_stack_widget.setCurrentWidget(self.rectangular_beam_options_widget)

        elif issubclass(self.current_structure_type, CircularBeam):
            self.options_stack_widget.setCurrentWidget(self.circular_beam_options_widget)

        elif issubclass(self.current_structure_type, TBeam):
            self.options_stack_widget.setCurrentWidget(self.t_beam_options_widget)

        elif issubclass(self.current_structure_type, IBeam):
            self.options_stack_widget.setCurrentWidget(self.i_beam_options_widget)

        elif issubclass(self.current_structure_type, CBeam):
            self.options_stack_widget.setCurrentWidget(self.c_beam_options_widget)

        elif issubclass(self.current_structure_type, Point):
            self._show_deltas_mode(False)
            self.pipeline.dismiss()
            self.pipeline.clear_structure_selection()
            self._set_xyz_to_selected_point()
            self.render_widget.update_plot(reset_camera=False)

        if not issubclass(self.current_structure_type, Point):
            self.xyz_changed_callback()

        self._update_permissions()
        self._update_information_text()
        self.x_line_edit.setFocus()

    def show_material_widget_callback(self):
        self.material_widget._initialize()
        self.material_widget._add_icon_and_title()
        self.material_widget.load_data_from_materials_library()
        self.material_widget.setVisible(True)

    def show_fluid_widget_callback(self):
        pass 

    def options_changed_callback(self):
        self._update_permissions()
        self.xyz_changed_callback()
        self.render_widget.update_plot(reset_camera=False)

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
        except TypeError:
            return

        if issubclass(self.current_structure_type, Point):
            self._xyz_point_callback(xyz)
        else:
            self._xyz_structure_callback(xyz)

        self._update_permissions()

    def xyz_apply_evaluation_callback(self):
        self.x_line_edit.blockSignals(True)
        self.y_line_edit.blockSignals(True)
        self.z_line_edit.blockSignals(True)

        dx = self._eval_number(self.x_line_edit.text())
        dy = self._eval_number(self.y_line_edit.text())
        dz = self._eval_number(self.z_line_edit.text())

        if dx is not None:
            self.x_line_edit.setText(str(dx))

        if dy is not None:
            self.y_line_edit.setText(str(dy))

        if dz is not None:
            self.z_line_edit.setText(str(dz))

        self.x_line_edit.blockSignals(False)
        self.y_line_edit.blockSignals(False)
        self.z_line_edit.blockSignals(False)

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
        self.division_amount_spinbox.setValue(value)

    def division_amount_spinbox_callback(self, value):
        value = int(value)
        division_type = self.division_combobox.currentText().lower()
        self.pipeline.dismiss()

        if division_type == "single division":
            self.pipeline.preview_divide_structures(value / 100)

        elif division_type == "multiple division":
            self.pipeline.preview_divide_structures_evenly(value)

        self.division_slider.blockSignals(True)
        self.division_slider.setValue(value)
        self.division_slider.blockSignals(False)

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

    def delete_selection_callback(self):
        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self._reset_xyz()
        self._update_permissions()
        self.render_widget.update_plot(reset_camera=False)

    def attach_selection_callback(self):
        current_widget = self.options_stack_widget.currentWidget()
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()

        if not callable(current_widget.add_function):
            return

        kwargs = self._get_parameters()
        if kwargs is None:
            return

        current_widget.attach_function(**kwargs)
        self.render_widget.update_plot(reset_camera=True)
        self._reset_xyz()
        self._update_permissions()

    def add_structure_callback(self):
        self.pipeline.commit()
        self.render_widget.update_plot(reset_camera=False)
        self._reset_xyz()

    def cancel_callback(self):
        app().main_window.update_plots()
        app().main_window.use_structural_setup_workspace()

    def finalize_callback(self):
        self.pipeline.dismiss()

        geometry_handler = GeometryHandler()
        geometry_handler.set_pipeline(self.pipeline)
        geometry_handler.set_length_unit(self.length_unit)
        geometry_handler.export_model_data_file()

        app().pulse_file.modify_project_attributes(
                                                                length_unit = self.length_unit,
                                                                element_size = 0.01, 
                                                                geometry_tolerance = 1e-6,
                                                                import_type = 1,
                                                              )

        self._load_project()

        app().main_window.update_plots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.plot_lines_with_cross_sections()
        self.render_widget.set_info_text("")

    def showEvent(self, event):
        self._update_permissions()

    def _eval_number(self, expression: str):
        '''
        We should avoid at all cost to run
        eval on our code due to safety reasons.

        I am trying my best to avoid any leaks, 
        because this functionality is pretty cool.
        '''
        global_context = {"__builtins__" : None}
        local_context = {
            "sqrt": math.sqrt,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
        }

        if not expression:
            return None

        try:
            result = eval(expression, global_context, local_context)
        except Exception:
            return None

        if isinstance(result, Number):
            return result
        else:
            return None

    def _get_xyz(self):
        '''
        If you find some concerning problem with eval
        please remove everyting and use the previous 
        version of this code:

        dx = float(self.x_line_edit.text() or 0)
        dy = float(self.y_line_edit.text() or 0)
        dz = float(self.z_line_edit.text() or 0)
        return dx, dy, dz
        '''

        dx = self._eval_number(self.x_line_edit.text())
        dy = self._eval_number(self.y_line_edit.text())
        dz = self._eval_number(self.z_line_edit.text())

        dx = dx if dx is not None else 0
        dy = dy if dy is not None else 0
        dz = dz if dz is not None else 0

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
            self.pipeline.add_isolated_point(xyz)

        self.render_widget.update_plot(reset_camera=True)

    def _xyz_structure_callback(self, xyz):
        current_widget = self.options_stack_widget.currentWidget()
        self.pipeline.dismiss()
        self.pipeline.clear_structure_selection()

        if xyz == (0, 0, 0):
            self.render_widget.update_plot(reset_camera=False)
            return

        if not callable(current_widget.add_function):
            return

        kwargs = self._get_parameters()
        if kwargs is None:
            return

        current_widget.add_function(xyz, **kwargs)
        self.render_widget.update_plot(reset_camera=True)
    
    def _get_parameters(self) -> dict | None:
        current_widget = self.options_stack_widget.currentWidget()
        kwargs = current_widget.get_parameters()
        if kwargs is None:
            return
        kwargs["extra_info"]["material_info"] = self.current_material_info
        return kwargs

    def _update_section_of_selected_structures(self):
        kwargs = self._get_parameters()
        if kwargs is None:
            return

        for structure in self.pipeline.selected_structures:
            if issubclass(self.current_structure_type, Pipe):
                _type = Pipe | Bend
            else:
                _type = self.current_structure_type

            if not isinstance(structure, _type):
                continue

            for k, v in kwargs.items():
                setattr(structure, k, v)
    
    def _update_material_of_selected_structures(self):
        for structure in self.pipeline.selected_structures:
            structure.extra_info["material_info"] =  self.current_material_info

    def _unit_abreviation(self, unit):
        if self.length_unit == "meter":
            return "m"

        elif self.length_unit == "milimeter":
            return "mm"

        elif self.length_unit == "inch":
            return "in"

        else:
            return

    def _structure_name_to_class(self, structure_name: str):
        structures = {
            "point": Point,
            "pipe": Pipe,
            "flange": Flange,
            "valve": Valve,
            "expansion joint": ExpansionJoint,
            "reducer": Reducer,
            "circular beam": CircularBeam,
            "rectangular beam": RectangularBeam,
            "i-beam": IBeam,
            "t-beam": TBeam,
            "c-beam": CBeam,
        }  # it is a bit cringe, but very understandable and compact
        return structures.get(structure_name)

    def _update_information_text(self):
        current_widget = self.options_stack_widget.currentWidget()
        cross_section_info = getattr(current_widget, "cross_section_info", None)

        section_label = ""
        section_parameters = ""
        if cross_section_info is not None:
            section_label = cross_section_info["section_type_label"]
            section_parameters = cross_section_info["section_parameters"]

        material_id = ""
        material = None
        if self.current_material_info is not None:
            material_id = self.current_material_info
            material = self.material_widget.library_materials[material_id]

        message = "Active configuration\n\n"

        if cross_section_info is not None:
            if section_label == "Reducer":
                message += f"Section type: {section_label} (variable)\n"
            elif section_label  == "Pipe":
                message += f"Section type: {section_label} (constant)\n"    
            else:
                message += f"Section type: {section_label}\n"
            message += f"Section data: {section_parameters}\n\n"

        if material is not None:
            message += f"Material name: {material.name}\n"
            message += f"Material id: {material.identifier}\n"
            message += f"Elasticity modulus: {material.elasticity_modulus}\n"
            message += f"Poisson ratio: {material.poisson_ratio}\n"
            message += f"Density: {material.density}\n\n"

        if len(self.pipeline.selected_points) == 2:
            a = self.pipeline.selected_points[0].coords()
            b = self.pipeline.selected_points[1].coords()
            dx, dy, dz = np.round(np.abs(a - b), 6)
            distance = np.round(np.linalg.norm(a - b), 6)

            unit = self._unit_abreviation(self.length_unit)
            tree = TreeInfo("Distance:")
            tree.add_item("Total", distance, unit)
            tree.add_item("dx", dx, unit)
            tree.add_item("dy", dy, unit)
            tree.add_item("dz", dz, unit)
            message += str(tree) + "\n\n"

        self.render_widget.set_info_text(message)

    def _update_permissions(self):
        current_widget = self.options_stack_widget.currentWidget()
        cross_section_info = getattr(current_widget, "cross_section_info", None)
        expansion_joint_info = getattr(current_widget, "expansion_joint_info", None)

        # usefull variables
        have_selection = bool(self.pipeline.selected_points or self.pipeline.selected_structures)
        have_staged = bool(self.pipeline.staged_points or self.pipeline.staged_structures)
        widget_configured = (cross_section_info is not None) or (expansion_joint_info is not None)
        multiple_points_selected = len(self.pipeline.selected_points) >= 1
        is_point = issubclass(self.current_structure_type, Point)
        is_beam = issubclass(self.current_structure_type, Beam)

        self.set_material_button.setDisabled(is_point)
        self.set_fluid_button.setDisabled(is_beam or is_point)

        self.add_button.setDisabled(not have_staged)
        self.delete_button.setDisabled(not (have_selection or have_staged))
        self.attach_button.setDisabled(
            is_point
            or not widget_configured
            or not multiple_points_selected
        )

        disable_xyz = (not is_point and not widget_configured)
        self.x_line_edit.setDisabled(disable_xyz)
        self.y_line_edit.setDisabled(disable_xyz)
        self.z_line_edit.setDisabled(disable_xyz)

    def _load_project(self):
        app().loader.load_project_data()
        self.project.initial_load_project_actions()
        app().loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        self.complete = True