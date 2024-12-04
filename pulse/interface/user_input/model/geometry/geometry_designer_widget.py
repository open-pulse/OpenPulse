from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QFrame, QPushButton, QLabel, QStackedWidget, QAction, QSlider, QSpinBox, QCheckBox
from PyQt5 import uic

from vtkmodules.vtkRenderingCore import vtkCoordinate
from vtkmodules.vtkCommonDataModel import vtkRecti

import re
from itertools import chain
from numbers import Number
import numpy as np
import math

from molde.stylesheets import set_qproperty
from molde.utils import TreeInfo

from pulse import app, UI_DIR
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.setup.cross_section.cross_section_widget import CrossSectionWidget
from pulse.interface.user_input.model.setup.material.set_material_input_simplified import SetMaterialSimplified
from pulse.interface.viewer_3d.render_widgets._model_info_text import material_info_text
from pulse.interface.viewer_3d.render_widgets import GeometryRenderWidget
from pulse.editor.structures import (
    Point,
    Pipe,
    Bend,
    Beam,
)

from pulse.interface.user_input.model.geometry.options import (
    StructureOptions,
    PipeOptions,
    FlangeOptions,
    ReducerOptions,
    TBeamOptions,
    IBeamOptions,
    CBeamOptions,
    CircularBeamOptions,
    RectangularBeamOptions,
    ExpansionJointOptions,
    ValveOptions,
    ArcBendOptions,
    PointOptions,
)


class GeometryDesignerWidget(QWidget):
    def __init__(self, render_widget: GeometryRenderWidget, parent=None):
        super().__init__(parent)

        ui_path = UI_DIR / "model/geometry/geometry_designer_widget.ui"
        uic.loadUi(ui_path, self)

        self.render_widget = render_widget
        self.modified = False

        self.project = app().project
        self.pipeline = self.project.pipeline

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self._initialize()

    def _define_qt_variables(self):

        # QAction
        self.select_all_action: QAction
        self.addAction(self.select_all_action)

        # QComboBox
        self.unit_combobox: QComboBox
        self.structure_combobox: QComboBox
        self.division_combobox: QComboBox
        self.bending_options_combobox: QComboBox
        self.deltas_combobox: QComboBox
        self.selected_point_combo_box: QComboBox
        self.distance_axis_combo_box: QComboBox

        # QFrame
        self.frame_bending_options: QFrame
        self.frame_bounding_box_sizes: QFrame
        self.frame_division_options: QFrame
        self.create_structure_frame: QFrame

        # QPushButton
        self.add_button: QPushButton
        self.apply_division_button: QPushButton
        self.attach_button: QPushButton
        self.cancel_button: QPushButton
        self.cancel_division_button: QPushButton
        self.delete_button: QPushButton
        self.finalize_button: QPushButton
        self.configure_button: QPushButton
        self.set_material_button: QPushButton

        # QLineEdit
        self.x_line_edit: QLineEdit
        self.y_line_edit: QLineEdit
        self.z_line_edit: QLineEdit
        self.unity_x_label: QLineEdit
        self.unity_y_label: QLineEdit
        self.unity_z_label: QLineEdit
        self.bending_radius_line_edit: QLineEdit
        self.deltas_line_edit: QLineEdit
        self.distance_value_line_edit: QLineEdit

        # QLabel
        self.dx_label: QLabel
        self.dy_label: QLabel
        self.dz_label: QLabel

        self.division_slider_label: QLabel
        self.position_slider_label: QLabel
        self.sizes_coords_label: QLabel

        # QSlider
        self.division_slider: QSlider
        self.position_slider: QSlider

        # QSpinBox
        self.division_amount_spinbox: QSpinBox
        self.position_spinbox: QSpinBox

        # QStackedWidget
        self.options_stack_widget: QStackedWidget

        # QWidget
        self.empty_widget: QWidget

    def _create_layout(self):
        self.cross_section_widget = CrossSectionWidget(self)
        self.material_widget = SetMaterialSimplified()

        # Add your newly implemented StructureOptions here 
        structure_option_types: list[type[StructureOptions]] = [
            PipeOptions,
            ArcBendOptions,
            FlangeOptions,
            ReducerOptions,
            RectangularBeamOptions,
            CircularBeamOptions,
            TBeamOptions,
            IBeamOptions,
            CBeamOptions,
            ExpansionJointOptions,
            ValveOptions,
            PointOptions,
        ]

        # Initialize the StructureOptions classes
        self.structure_options: dict[str, StructureOptions] = {
            option.name(): option(self) for option in structure_option_types
        }

        # Add the names to the combobox
        self.structure_combobox.clear()
        for name in self.structure_options.keys():
            self.structure_combobox.addItem(name)

    def _create_connections(self):
        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.cross_section_confirm_callback)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.cross_section_confirm_callback)

        self.render_widget.selection_changed.connect(self.selection_callback)
        self.select_all_action.triggered.connect(self.select_all_callback)

        self.unit_combobox.currentTextChanged.connect(self.unity_changed_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_type_changed_callback)
        self.set_material_button.clicked.connect(self.show_material_widget_callback)
        self.configure_button.clicked.connect(self.configure_structure_callback)
        self.material_widget.material_widget.pushButton_attribute.clicked.connect(self.define_material_callback)

        self.x_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.y_line_edit.textEdited.connect(self.xyz_changed_callback)
        self.z_line_edit.textEdited.connect(self.xyz_changed_callback)

        self.x_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)
        self.y_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)
        self.z_line_edit.editingFinished.connect(self.xyz_apply_evaluation_callback)

        self.bending_options_combobox.currentIndexChanged.connect(self.bending_options_changed_callback)
        self.bending_radius_line_edit.textChanged.connect(self.bending_options_changed_callback)

        self.division_combobox.currentTextChanged.connect(self.division_type_changed_callback)
        self.division_slider.valueChanged.connect(self.division_slider_callback)
        self.division_amount_spinbox.textChanged.connect(self.preview_divisions_callback)
        self.position_slider.valueChanged.connect(self.position_slider_callback)
        self.position_spinbox.textChanged.connect(self.preview_divisions_callback)

        self.distance_value_line_edit.textChanged.connect(self.preview_divisions_callback)
        self.distance_axis_combo_box.currentIndexChanged.connect(self.preview_divisions_callback)        
        self.selected_point_combo_box.currentIndexChanged.connect(self.preview_divisions_callback)        

        self.cancel_division_button.clicked.connect(self.cancel_division_callback)
        self.apply_division_button.clicked.connect(self.apply_division_callback)

        self.add_button.clicked.connect(self.add_structure_callback)
        self.attach_button.clicked.connect(self.attach_selection_callback)
        self.delete_button.clicked.connect(self.delete_selection_callback)

        self.cancel_button.clicked.connect(self.cancel_callback)
        self.finalize_button.clicked.connect(self.finalize_callback)

    def _initialize(self):
        self.current_options: StructureOptions | None = None
        self.current_structure_type = None
        self.current_material_info = None

        self.unity_changed_callback("meter")
        self.structure_type_changed_callback(PipeOptions.name())
        self.division_type_changed_callback()

    def selection_callback(self):
        if issubclass(self.current_structure_type, Point):
            self._set_xyz_to_selected_point()

        if not self.pipeline.selected_structures:
            self.pipeline.main_editor.remove_collapsed_bends()
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
                label.setText(f"[{unit_label_text}]")

    def structure_type_changed_callback(self, structure_name: str):        
        # If the previous option was PointOptions reset xyz
        if isinstance(self.current_options, PointOptions):
            self._reset_xyz()

        # Update the current object based on the name
        self.current_options = self.structure_options[structure_name]
        self.current_structure_type = self.current_options.structure_type

        # Only pipes need to bend
        if isinstance(self.current_options, PipeOptions):
            self.frame_bending_options.setEnabled(True)
        else:
            self.frame_bending_options.setEnabled(False)

        # Structures that can be divided
        if issubclass(self.current_options.structure_type, Pipe | Beam):
            self.frame_division_options.setEnabled(True)
        else:
            self.frame_division_options.setEnabled(False)
        
        # Points specific configuration
        if isinstance(self.current_options, PointOptions):
            self._show_deltas_mode(False)
            self._set_xyz_to_selected_point()
        else:
            self._show_deltas_mode(True)
            self.xyz_changed_callback()

        self._update_permissions()
        self._update_information_text()
        self.x_line_edit.setFocus()

    def set_bound_box_sizes_widgets_enabled(self, key: bool):
        self.x_line_edit.setEnabled(key)
        self.y_line_edit.setEnabled(key)
        self.z_line_edit.setEnabled(key)

    def show_material_widget_callback(self):
        self.material_widget.material_widget.load_data_from_materials_library()
        self.material_widget.exec()

    def options_changed_callback(self):
        self._update_permissions()
        self.xyz_changed_callback()
        self.render_widget.update_plot(reset_camera=False)

    def define_material_callback(self):
        self.current_material_info = self.material_widget.material_widget.get_selected_material_id()
        self.material_widget.close()
        self._update_material_of_selected_structures()
        self._update_permissions()
        self._update_information_text()
        self.render_widget.update_plot(reset_camera=False)

    def configure_structure_callback(self):
        self.current_options.configure_structure()
        self._update_permissions()
        self._update_information_text()
        self.xyz_changed_callback()
        self.render_widget.update_plot(reset_camera=False)

    def cross_section_confirm_callback(self):
        self.cross_section_widget.complete = True
        self.cross_section_widget.close()

    def update_bending_radius_visibility(self):

        index = self.bending_options_combobox.currentIndex()
        if index == 2:
            self.bending_radius_line_edit.setEnabled(True)
            if self.bending_radius_line_edit.text() in ["1.5*D", "1.0*D"]:
                self.bending_radius_line_edit.setText("")

        else:

            self.bending_radius_line_edit.blockSignals(True)
            self.bending_radius_line_edit.setEnabled(False)
            d = self.get_pipe_diameter()

            if index == 0:
                if d is None:
                    self.bending_radius_line_edit.setText("1.5*D")
                else:
                    bending_radius = 1.5 * d
                    self.bending_radius_line_edit.setText(str(round(bending_radius, 6)))

            elif index == 1:
                if d is None:
                    self.bending_radius_line_edit.setText("1.0*D")
                else:
                    bending_radius = 1.0 * d
                    self.bending_radius_line_edit.setText(str(round(bending_radius, 6)))

            else:
                self.bending_radius_line_edit.setText("")

            self.bending_radius_line_edit.blockSignals(False)

    def get_pipe_diameter(self):

        try:
            section_parameters = self.cross_section_widget.pipe_section_info["section_parameters"]
            diameter = section_parameters[0]
        except:
            return None

        return diameter

    def bending_options_changed_callback(self):
        if self.pipeline.selected_structures:
            self._update_bending_radius_of_selected_structures()
            self.update_bending_radius_visibility()
            self._update_permissions()
            self.render_widget.update_plot(reset_camera=False)
        else:
            self.xyz_changed_callback()

    def xyz_changed_callback(self):
        try:
            self.update_bending_radius_visibility()
            xyz = self._get_xyz()
        except ValueError:
            return
        except TypeError:
            return

        self.current_options.xyz_callback(xyz)
        self._update_permissions()
        self.render_widget.update_plot(reset_camera=False)
        self.update_zoom_to_fit_new_points()
        self.render_widget.update()

    def update_zoom_to_fit_new_points(self):
        renderer = self.render_widget.renderer
        coordinate = vtkCoordinate()
        coordinate.SetCoordinateSystemToWorld()

        w, h = renderer.GetSize()
        x0, y0 = 0, 0
        x1, y1 = w, h
        need_to_fit = False

        for point in chain(self.pipeline.staged_points, self.pipeline.selected_points):
            coordinate.SetValue(*point)
            view_x, view_y = coordinate.GetComputedViewportValue(renderer)

            if not renderer.IsInViewport(view_x, view_y):
                x0 = min(x0, view_x)
                x1 = max(x1, view_x)
                y0 = min(y0, view_y)
                y1 = max(y1, view_y)
                need_to_fit = True
            
        if not need_to_fit:
            return
        
        dx = (x1 + x0 - w) / 2
        dy = (y1 + y0 - h) / 2
        self.move_viewport(dx, dy)

        rect = vtkRecti(x0, y0, x1-x0, y1-y0)
        renderer.ZoomToBoxUsingViewAngle(rect)
    
    def move_viewport(self, dx, dy):
        renderer = self.render_widget.renderer
        camera = renderer.GetActiveCamera()
        width, heigth = renderer.GetSize()

        if camera.GetParallelProjection():
            view_height = 2 * camera.GetParallelScale()
        else:
            correction = camera.GetDistance()
            view_height = 2 * correction * np.tan(0.5 * camera.GetViewAngle() / 57.296)
        scale = view_height / heigth

        focal_point = np.array(camera.GetFocalPoint())
        camera_position = np.array(camera.GetPosition())
        camera_up = np.array(camera.GetViewUp())
        camera_in = np.array(camera.GetDirectionOfProjection())
        camera_right = np.cross(camera_in, camera_up)

        camera_displacement = scale * (camera_right * dx + camera_up * dy)
        camera.SetPosition(camera_position + camera_displacement)
        camera.SetFocalPoint(focal_point + camera_displacement)

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
    
    def adjust_stack_widget_height(self):
        height = self.options_stack_widget.currentWidget().sizeHint().height()
        self.options_stack_widget.setFixedHeight(height)

    def division_type_changed_callback(self):

        index = self.division_combobox.currentIndex()

        if index == 0:
            self.options_stack_widget.setCurrentIndex(0)
            self.position_slider.setMinimum(0)
            self.position_slider.setMaximum(100)
            self.position_slider.setValue(50)

        elif index == 1:
            self.options_stack_widget.setCurrentIndex(1)
            self.division_slider.setMinimum(1)
            self.division_slider.setMaximum(10)
            self.division_slider.setValue(1)

        elif index == 2:
            self.options_stack_widget.setCurrentIndex(2)

        else:
            return

        self.adjust_stack_widget_height()

    def division_slider_callback(self, value):
        self.division_amount_spinbox.setValue(value)

    def position_slider_callback(self, value):
        self.position_spinbox.setValue(value)

    def preview_divisions_callback(self, value):
        
        self.pipeline.dismiss()
        index = self.division_combobox.currentIndex()

        if index == 0:
            value = int(value)
            self.pipeline.preview_divide_structures(value / 100)

            self.position_slider.blockSignals(True)
            self.position_slider.setValue(value)
            self.position_slider.blockSignals(False)


        elif index == 1:
            value = int(value)
            self.pipeline.preview_divide_structures_evenly(value)

            self.division_slider.blockSignals(True)
            self.division_slider.setValue(value)
            self.division_slider.blockSignals(False)
        
        elif index == 2:

            if self.selected_point_combo_box.currentIndex():
                selected_point = "end_point"
            else:
                selected_point = "start_point"

            division_data = [None, None, None, None]
            direction_index = self.distance_axis_combo_box.currentIndex()

            value = self._eval_number(self.distance_value_line_edit.text())

            if value is None:
                return

            if value < 0:
                value = abs(value)
                self.distance_value_line_edit.blockSignals(True)
                self.distance_value_line_edit.setText(str(value))
                self.distance_value_line_edit.blockSignals(False)

            division_data[direction_index] = value

            self.pipeline.preview_divided_structures_by_distance_from_point(selected_point, division_data)

        self.render_widget.update_plot(reset_camera=False)

    def cancel_division_callback(self):
        self.pipeline.dismiss()
        self.render_widget.update_plot(reset_camera=False)

    def apply_division_callback(self):

        self.pipeline.dismiss()
        index = self.division_combobox.currentIndex()

        if index == 0:
            value = self.position_slider.value()
            self.pipeline.divide_structures(value / 100)

        elif index == 1:
            value = self.division_slider.value()
            self.pipeline.divide_structures_evenly(value)
        
        elif index == 2:

            if self.selected_point_combo_box.currentIndex():
                selected_point = "end_point"
            else:
                selected_point = "start_point"

            division_data = [None, None, None, None]
            direction_index = self.distance_axis_combo_box.currentIndex()

            value = self._eval_number(self.distance_value_line_edit.text())

            if value is None:
                return

            if value < 0:
                value = abs(value)
                self.distance_value_line_edit.blockSignals(True)
                self.distance_value_line_edit.setText(str(value))
                self.distance_value_line_edit.blockSignals(False)

            division_data[direction_index] = value

            self.pipeline.divide_structures_by_distance_from_point(selected_point, division_data)

        self.pipeline.clear_structure_selection()
        self.render_widget.update_plot(reset_camera=False)
        self.modified = True
        self._update_permissions()

    def delete_selection_callback(self):
        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, Point):
                tag = structure.tag
                if tag != -1:
                    app().project.model.properties._remove_line(tag)

        self.pipeline.dismiss()
        self.pipeline.delete_selection()
        self.modified = True

        self._reset_xyz()
        self._update_permissions()
        self.render_widget.update_plot(reset_camera=False)

    def attach_selection_callback(self):
        self.current_options.attach_callback()
        self.pipeline.commit()
        self._update_permissions()
        self.render_widget.update_plot(reset_camera=True)
        self.modified = True
        self._reset_xyz()
        self._update_permissions()

    def add_structure_callback(self):
        if (self.pipeline.selected_structures) and not (self.pipeline.staged_structures):
            self.current_options.replace_selection()
        else:
            self.pipeline.commit()
            if self.current_structure_type == Point:
                self.pipeline.clear_point_selection()

        self.render_widget.update_plot(reset_camera=False)
        self.modified = True
        self._reset_xyz()
        self._update_permissions()

    def cancel_callback(self):
        app().main_window.update_plots()
        app().main_window.use_model_setup_workspace()

    def finalize_callback(self):
        self.modified = False
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
        app().main_window.use_model_setup_workspace()
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

        expression = expression.replace(",", ".")

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
            self._reset_xyz()
            return

        x, y, z = np.round(self.pipeline.selected_points[0].coords(), 6)
        self._set_xyz(x, y, z)

    def _show_deltas_mode(self, boolean):
        if boolean:
            x_text = "Length Δx:"
            y_text = "Length Δy:"
            z_text = "Length Δz:"
            self.sizes_coords_label.setText("Bounding Box Sizes")

        else:
            x_text = "Coordinate x:"
            y_text = "Coordinate y:"
            z_text = "Coordinate z:"
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

    def _update_material_of_selected_structures(self):
        for structure in self.pipeline.selected_structures:
            structure.extra_info["material_info"] =  self.current_material_info

    def _update_bending_radius_of_selected_structures(self):
        if not isinstance(self.current_options, PipeOptions):
            return

        for structure in self.pipeline.selected_structures:
            if not isinstance(structure, Bend):
                continue
            
            pipe_options: PipeOptions = self.structure_options[PipeOptions.name()]
            bending_radius = pipe_options._get_bending_radius(structure.diameter)
            structure.curvature_radius = bending_radius

        self.pipeline.recalculate_curvatures()

    def _unit_abreviation(self, unit):
        if self.length_unit == "meter":
            return "m"

        elif self.length_unit == "milimeter":
            return "mm"

        elif self.length_unit == "inch":
            return "in"

        else:
            return

    def _update_information_text(self):
        cross_section_info = getattr(self.current_options, "cross_section_info", None)

        section_label = ""
        section_parameters = ""
        if cross_section_info:
            section_label = cross_section_info["section_type_label"]
            section_parameters = cross_section_info["section_parameters"]

        material_id = ""
        material = None
        if self.current_material_info is not None:
            material_id = self.current_material_info
            material = self.material_widget.material_widget.library_materials[material_id]

        message = "Active configuration\n\n"

        if cross_section_info:
            if section_label == "Reducer":
                message += f"Section type: {section_label} (variable)\n"
            elif section_label  == "Pipe":
                message += f"Section type: {section_label} (constant)\n"    
            else:
                message += f"Section type: {section_label}\n"
            message += f"Section data: {section_parameters}\n\n"

        if material is not None:
            message += material_info_text(material)

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
        if self.current_options is None:
            return

        self.current_options.update_permissions()

        if self.modified:
            set_qproperty(self.finalize_button, warning=True, status="danger")
        else:
            set_qproperty(self.finalize_button, warning=False, status="default")

    def _load_project(self):
        app().loader.load_project_data()
        self.project.initial_load_project_actions()
        app().loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        self.complete = True
