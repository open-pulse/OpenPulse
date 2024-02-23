from PyQt5.QtWidgets import QComboBox, QWidget, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.general.material_widget import MaterialInputs
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse.interface.cad_handler import CADHandler
from pulse.interface.gmsh_geometry_handler import GMSHGeometryHandler
from pulse import app, UI_DIR

from opps.model import Bend, Pipe
        
def get_data(data):
    return list(np.round(data, 6))

class AddStructuresWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "model/geometry/add_widget.ui", self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._update_permissions()

    def _initialize(self):
        self.complete = False
        self.cross_section_info = None
        self.current_material_index = None
        self.bending_radius = 0
        self.bending_factor = 0
        self.segment_information = dict()

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_length_unit: QComboBox
        self.comboBox_section_type: QComboBox
        self.comboBox_bending_type: QComboBox

        # QFrame
        self.information_frame: QFrame

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.cross_section_widget = CrossSectionWidget()
        self.material_widget = MaterialInputs(app().main_window)

        # QLabel
        self.label_unit_delta_x: QLabel
        self.label_unit_delta_y: QLabel
        self.label_unit_delta_z: QLabel
        self.label_unit_bending_radius: QLabel

        # QLineEdit
        self.lineEdit_delta_x: QLineEdit
        self.lineEdit_delta_y: QLineEdit
        self.lineEdit_delta_z: QLineEdit
        self.lineEdit_bending_radius: QLineEdit
        self.create_list_of_unit_labels()
        
        # QPushButton
        self.pushButton_set_cross_section: QPushButton
        self.pushButton_set_material: QPushButton
        self.pushButton_add_segment: QPushButton
        self.pushButton_finalize: QPushButton

        # self.pushButton_confirm_pipe: QPushButton
        # self.pushButton_confirm_beam: QPushButton
        # self.pushButton_set_material: QPushButton
        # self.pushButton_process_geometry.setIcon(self.export_icon)

        # QTabWidget
        # self.tabWidget_main: QTabWidget
        # self.tabWidget_general: QTabWidget
        # self.tabWidget_pipe_section: QTabWidget
        # self.tabWidget_beam_section: QTabWidget

        # QTextEdit
        self.textEdit_segment_information: QTextEdit
        self.textEdit_segment_information.setDisabled(True)

    def _create_connections(self):
        self.comboBox_length_unit.currentIndexChanged.connect(self.update_legth_units)
        self.comboBox_bending_type.currentIndexChanged.connect(self.update_bending_type)
        self.update_legth_units()
        self.update_bending_type()

        self.lineEdit_delta_x.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_y.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_z.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_bending_radius.textEdited.connect(self.coords_modified_callback)

        self.pushButton_add_segment.clicked.connect(self.create_segment_callback)
        self.pushButton_set_cross_section.clicked.connect(self.show_cross_section_widget)
        self.pushButton_set_material.clicked.connect(self.show_material_widget)
        self.pushButton_finalize.clicked.connect(self.process_geometry_callback)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material)

    def _update_permissions(self):
        enable_pipe = self.cross_section_info is not None

        self.lineEdit_delta_x.setEnabled(enable_pipe)
        self.lineEdit_delta_y.setEnabled(enable_pipe)
        self.lineEdit_delta_z.setEnabled(enable_pipe)

        if enable_pipe:
            self.lineEdit_delta_x.setPlaceholderText("")
            self.lineEdit_delta_y.setPlaceholderText("")
            self.lineEdit_delta_z.setPlaceholderText("")
        else:
            self.lineEdit_delta_x.setPlaceholderText("Cross-Section")
            self.lineEdit_delta_y.setPlaceholderText("was not")
            self.lineEdit_delta_z.setPlaceholderText("defined")

        pipeline = app().geometry_toolbox.pipeline
        enable_finalize = len(pipeline.structures) > 0
        self.pushButton_finalize.setEnabled(enable_finalize)

    def load_defined_unit(self):
        self.unit_of_length = self.file.length_unit
        if self.unit_of_length == "milimeter":
            self.comboBox_length_unit.setCurrentIndex(0)
        elif self.unit_of_length == "milimeter":
            self.comboBox_length_unit.setCurrentIndex(1)
        elif self.unit_of_length == "inch":
            self.comboBox_length_unit.setCurrentIndex(2)
        self.update_legth_units()

    def show_cross_section_widget(self):
        self.cross_section_widget.setVisible(True)
        section_type = self.comboBox_section_type.currentIndex()
        self.cross_section_widget.set_inputs_to_geometry_creator(section_type=section_type)            

    def show_material_widget(self):
        self.material_widget.reset()
        self.material_widget.load_data_from_materials_library()
        self.material_widget.setVisible(True)

    def create_list_of_unit_labels(self):
        self.unit_labels = list()
        self.unit_labels.append(self.label_unit_delta_x)
        self.unit_labels.append(self.label_unit_delta_y)
        self.unit_labels.append(self.label_unit_delta_z)
        self.unit_labels.append(self.label_unit_bending_radius)

    def update_legth_units(self):
        index = self.comboBox_length_unit.currentIndex()
        if index == 0:
            unit_label = "m"
            self.unit_of_length = "meter"
        elif index == 1:
            unit_label = "mm"
            self.unit_of_length = "milimeter"
        else:
            unit_label = "in"
            self.unit_of_length = "inch"
        #
        for _label in self.unit_labels:
            _label.setText(f"[{unit_label}]")

    def update_bending_type(self):
        self.bending_factor = 0
        self.lineEdit_bending_radius.setText("")
        self.lineEdit_bending_radius.setDisabled(True)
        index = self.comboBox_bending_type.currentIndex()
        if index == 0:
            self.bending_factor = 1.5
        elif index == 1:
            self.bending_factor = 1
        elif index == 2:
            self.lineEdit_bending_radius.setDisabled(False)
            self.lineEdit_bending_radius.setFocus()
        self.coords_modified_callback()

    def get_segment_deltas(self):
        dx = float(self.lineEdit_delta_x.text() or 0)
        dy = float(self.lineEdit_delta_y.text() or 0)
        dz = float(self.lineEdit_delta_z.text() or 0)
        return dx, dy, dz

    def coords_modified_callback(self):
        try:
            dx, dy, dz = self.get_segment_deltas()
        except ValueError:
            return

        # TODO: change this to pass the bend radius directly
        if self.bending_factor:
            bend_pipe = True
        else:
            bend_pipe = False
        self.geometry_widget.stage_pipe_deltas(dx, dy, dz, bend_pipe)

    def create_segment_callback(self):
        try:
            dx, dy, dz = self.get_segment_deltas()
        except ValueError:
            return

        if (dx, dy, dz) == (0, 0, 0):
            return

        # put usefull data inside the structures
        editor = app().geometry_toolbox.editor
        for structure in editor.staged_structures:
            structure.extra_info["cross_section_info"] = self.cross_section_info
            structure.extra_info["material_info"] = self.current_material_index

        self.geometry_widget.commit_structure()
        self.reset_deltas()
        self._update_permissions()

    def reset_deltas(self):
        self.lineEdit_delta_x.setText("")
        self.lineEdit_delta_y.setText("")
        self.lineEdit_delta_z.setText("")

    def get_segment_tag(self):
        tag = 1
        stop = False
        while not stop:
            if tag in self.segment_information.keys():
                tag += 1
            else:
                stop = True
        return tag

    def define_cross_section(self):
        is_pipe = (self.cross_section_widget.tabWidget_general.currentIndex() == 0)
        is_constant_section = (self.cross_section_widget.tabWidget_pipe_section.currentIndex() == 0)

        if is_pipe and is_constant_section:
            self.cross_section_widget.get_straight_pipe_parameters()
            section_parameters = list(self.cross_section_widget.section_parameters.values())
            self.cross_section_info = { "section label" : "pipe (constant)",
                                        "section parameters" : section_parameters }
            diameter = self.cross_section_widget.section_parameters["outer_diameter"]
            self.geometry_widget.update_default_diameter(diameter)

        elif is_pipe and not is_constant_section:
            self.cross_section_widget.get_variable_section_pipe_parameters()
            section_parameters =self.cross_section_widget.variable_parameters
            self.cross_section_info = { "section label" : "pipe (variable)",
                                        "section parameters" : section_parameters }

        else:  # is beam
            self.cross_section_widget.get_beam_section_parameters()
            section_label = self.cross_section_widget.section_label
            section_parameters = self.cross_section_widget.section_parameters
            self.cross_section_info = { "section label" : "beam",
                                        "beam section type" : section_label,
                                        "section parameters" : section_parameters }
        
        # just being consistent with the material name
        self.cross_section_widget.setVisible(False)
        self._update_permissions()
        self.update_segment_information_text()

    def define_material(self):
        self.current_material_index = self.material_widget.get_selected_material_id()
        self.material_widget.setVisible(False)
        self._update_permissions()
        self.update_segment_information_text()

    def update_segment_information_text(self):

        self.textEdit_segment_information.clear()
        
        section_label = ""
        section_parameters = ""
        if self.cross_section_info:
            section_label = self.cross_section_info["section label"]
            section_parameters = self.cross_section_info["section parameters"]

        material_id = ""
        material_data = None
        if self.current_material_index is not None:
            material_id = self.current_material_index
            material_data = self.file.get_material_properties(material_id)

        message = "SEGMENT INFORMATION\n\n"

        if self.cross_section_info:
            # message = "Cross-section info:\n"
            message += f"Section type: {section_label}\n"
            message += f"Section data: {section_parameters}\n\n"

        if material_data is not None:
            # message = "Material info:\n"
            message += f"Material name: {material_data[0]}\n"
            message += f"Material data: {material_data[1:]}\n\n"

        self.textEdit_segment_information.setText(message)

    def update_cross_section_info(self):
        self.textEdit_segment_information.setText("")

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
        geometry_path = self.file.get_file_path_inside_project_directory(geometry_filename)
        geometry_filename = os.path.basename(geometry_path)
        geometry_filename = ""

        # exporter = CADHandler()
        # exporter.save(geometry_path, pipeline, unit=self.unit_of_length)

        geometry_handler = GMSHGeometryHandler()
        geometry_handler.set_unit_of_length(self.unit_of_length)
        geometry_handler.set_pipeline(pipeline)
        self.project.preprocessor.set_geometry_handler(geometry_handler)

        self.file.update_project_attributes(length_unit = self.unit_of_length,
                                            element_size = 0.01, 
                                            geometry_tolerance = 1e-6)

        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        app().main_window.input_widget.initial_project_action(True)
        self.complete = True

    def export_entity_file(self):

        pipeline = app().geometry_toolbox.pipeline
        
        tag = 1
        points_info = dict()
        section_info = dict()
        material_info = dict()
        for structure in pipeline.structures:
            
            build_data = self.get_segment_build_info(structure)
            if build_data is not None:
                points_info[tag] = build_data
            
            if isinstance(structure, Bend) and structure.is_colapsed():               
                continue
            
            section_info[tag] = structure.extra_info["cross_section_info"]
            material_info[tag] = structure.extra_info["material_info"]
            tag += 1

        if os.path.exists(self.file._entity_path):
            os.remove(self.file._entity_path)

        self.file.create_entity_file(section_info.keys())
        for tag, coords in points_info.items():
            self.file.add_segment_build_data_in_file(tag, coords)

        for tag, section in section_info.items():
            self.file.add_cross_section_segment_in_file(tag, section)

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