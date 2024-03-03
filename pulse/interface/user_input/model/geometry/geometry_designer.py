from PyQt5.QtWidgets import QPushButton, QStackedWidget, QTabWidget, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.geometry.add_widget import AddStructuresWidget
from pulse.interface.user_input.model.geometry.edit_bend_widget import EditBendWidget
from pulse.interface.user_input.model.geometry.edit_point_widget import EditPointWidget
from pulse.interface.user_input.model.geometry.edit_pipe_widget import EditPipeWidget
from pulse.tools.utils import get_new_path
from pulse import app, UI_DIR

from opps.model import Pipe, Bend

import os
import numpy as np

def get_data(data):
    return list(np.round(data, 6))

class OPPGeometryDesignerInput(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)

        uic.loadUi(UI_DIR / "model/geometry/geometry_designer_tabs.ui", self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

        self._define_qt_variables()
        self._create_layout()
        self._create_connections()
        self.setContentsMargins(2,2,2,2)

    def _define_qt_variables(self):
        self.pushButton_cancel: QPushButton
        self.pushButton_finalize: QPushButton
        self.edit_stack: QStackedWidget
        self.tab_widget: QTabWidget       
        self.add_tab: QWidget
        self.edit_tab: QWidget
        self.empty_widget: QWidget

    def _create_layout(self):

        self.add_widget = AddStructuresWidget(self.geometry_widget)
        self.edit_pipe_widget = EditPipeWidget(self.geometry_widget)
        self.edit_bend_widget = EditBendWidget(self.geometry_widget)
        self.edit_point_widget = EditPointWidget(self.geometry_widget)

        self.add_tab.layout().addWidget(self.add_widget)
        self.edit_stack.addWidget(self.edit_pipe_widget)
        self.edit_stack.addWidget(self.edit_bend_widget)
        self.edit_stack.addWidget(self.edit_point_widget)

    def _create_connections(self):
        self.geometry_widget.selection_changed.connect(self.selection_callback)
        self.pushButton_cancel.clicked.connect(self.close_callback)
        self.pushButton_finalize.clicked.connect(self.process_geometry_callback)

    def selection_callback(self):

        editor = self.geometry_widget.editor

        if editor.selected_structures:
            self.structures_selection_callback()
        elif editor.selected_points:
            self.edit_stack.setCurrentWidget(self.edit_point_widget)
        else:
            self.edit_stack.setCurrentWidget(self.empty_widget)

        self.edit_stack.currentWidget().update()

    def structures_selection_callback(self):

        editor = self.geometry_widget.editor
        structure, *_ = editor.selected_structures

        if isinstance(structure, Pipe):
            self.edit_stack.setCurrentWidget(self.edit_pipe_widget)
        elif isinstance(structure, Bend):
            self.edit_stack.setCurrentWidget(self.edit_bend_widget)
        else:
            self.edit_stack.setCurrentWidget(self.empty_widget)

    def process_geometry_callback(self):
        self.geometry_widget.unstage_structure()
        self.export_files()
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.action_front_view_callback()

    def export_files(self):
        self.export_entity_file()
        self.export_cad_file()

    def export_cad_file(self):
        pipeline = app().geometry_toolbox.pipeline
        geometry_filename = "geometry_pipeline.step"
        geometry_path = self.get_file_path_inside_project_directory(geometry_filename)
        geometry_filename = os.path.basename(geometry_path)
        geometry_filename = ""

        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(self.add_widget.length_unit)
        geometry_handler.set_pipeline(pipeline)
        self.project.preprocessor.set_geometry_handler(geometry_handler)

        self.file.modify_project_attributes(length_unit = self.add_widget.length_unit,
                                            element_size = 0.01, 
                                            geometry_tolerance = 1e-6)

        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_widget.initial_project_action(True)
        self.complete = True

    def export_entity_file(self):
       
        tag = 1
        points_info = dict()
        section_info = dict()
        element_type_info = dict()
        material_info = dict()
        pipeline = app().geometry_toolbox.pipeline

        for structure in pipeline.structures:
            
            build_data = self.get_segment_build_info(structure)

            if build_data is not None:
                points_info[tag] = build_data
            
            if isinstance(structure, Bend) and structure.is_colapsed():               
                continue

            if "cross_section_info" in structure.extra_info.keys():
                section_info[tag] = structure.extra_info["cross_section_info"]
            
            if "material_info" in structure.extra_info.keys():
                material_info[tag] = structure.extra_info["material_info"]
            
            if "structural_element_type" in structure.extra_info.keys():
                element_type_info[tag] = structure.extra_info["structural_element_type"]

            tag += 1

        if os.path.exists(self.file._entity_path):
            os.remove(self.file._entity_path)

        self.file.create_entity_file(section_info.keys())
        for tag, coords in points_info.items():
            self.file.add_segment_build_data_in_file(tag, coords)

        for tag, section in section_info.items():
            self.file.add_cross_section_segment_in_file(tag, section)

        for tag, e_type in element_type_info.items():
            self.file.modify_structural_element_type_in_file(tag, e_type)

        for tag, material_id in material_info.items():
            self.file.add_material_segment_in_file(tag, material_id)

    def get_segment_build_info(self, structure):
        if isinstance(structure, Bend):
            start_coords = get_data(structure.start.coords())
            end_coords = get_data(structure.end.coords())
            corner_coords = get_data(structure.corner.coords())
            curvature = structure.curvature
            return [start_coords, corner_coords, end_coords, curvature]

        elif isinstance(structure, Pipe):
            start_coords = get_data(structure.start.coords())
            end_coords = get_data(structure.end.coords())
            return [start_coords, end_coords]
        else:
            return None

    def get_file_path_inside_project_directory(self, filename):
        return get_new_path(self.file._project_path, filename)

    def close_callback(self):
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()
        app().main_window.action_front_view_callback()