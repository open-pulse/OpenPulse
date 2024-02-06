from PyQt5.QtWidgets import QComboBox, QWidget, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from data.user_input.model.geometry.cross_section_inputs import CrossSectionInputs
from data.user_input.model.setup.general.material_input_new import MaterialInputs
from data.user_input.project.print_message_input import PrintMessageInput

# from opps.io.cad_file.cad_handler import CADHandler
from pulse.interface.cad_handler import CADHandler
from pulse import app


class AddStructuresWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(Path('data/user_input/ui_files/Model/geometry/add_widget.ui'), self)

        self.geometry_widget = geometry_widget
        self.project = app().project
        self.file = self.project.file

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

    def _reset_variables(self):
        self.complete = False
        self.cross_section_info = None
        self.bending_radius = 0
        self.bending_factor = 0
        self.segment_information = dict()

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_segment_id: QComboBox
        self.comboBox_length_unit: QComboBox
        self.comboBox_section_type: QComboBox
        self.comboBox_bending_type: QComboBox

        # QFrame
        self.information_frame: QFrame

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)

        self.cross_section_widget = CrossSectionInputs()
        self.material_widget = MaterialInputs(app().main_window)

        # QLabel
        self.label_unit_delta_x: QLabel
        self.label_unit_delta_y: QLabel
        self.label_unit_delta_z: QLabel
        self.label_unit_diameter: QLabel
        self.label_unit_bending_radius: QLabel

        # QLineEdit
        self.lineEdit_delta_x: QLineEdit
        self.lineEdit_delta_y: QLineEdit
        self.lineEdit_delta_z: QLineEdit
        self.lineEdit_bending_radius: QLineEdit
        self.lineEdit_section_diameter: QLineEdit
        self.create_list_of_unit_labels()
        
        # QPushButton
        self.pushButton_set_cross_section: QPushButton
        self.pushButton_set_material: QPushButton
        self.pushButton_create_segment: QPushButton
        self.pushButton_finalize: QPushButton
        self.pushButton_delete_segment: QPushButton

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
        # self.textEdit_segment_information.setText("Apenas para testar...\ne ver se consigo configurar corretamente.")
        # self.textEdit_segment_information.setVisible(False)

    def _create_connections(self):
        self.comboBox_length_unit.currentIndexChanged.connect(self.update_legth_units)
        self.comboBox_bending_type.currentIndexChanged.connect(self.update_bending_type)
        self.update_legth_units()
        self.update_bending_type()

        self.lineEdit_delta_x.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_y.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_delta_z.textEdited.connect(self.coords_modified_callback)
        self.lineEdit_bending_radius.textEdited.connect(self.coords_modified_callback)

        self.pushButton_create_segment.clicked.connect(self.create_segment_callback)
        self.pushButton_set_cross_section.clicked.connect(self.show_cross_section_widget)
        self.pushButton_set_material.clicked.connect(self.show_material_widget)
        self.pushButton_finalize.clicked.connect(self.process_geometry_callback)
        self.pushButton_delete_segment.clicked.connect(self.delete_segment)

        self.cross_section_widget.pushButton_confirm_pipe.clicked.connect(self.define_cross_section)
        self.cross_section_widget.pushButton_confirm_beam.clicked.connect(self.define_cross_section)
        self.material_widget.pushButton_attribute_material.clicked.connect(self.define_material)

    def show_cross_section_widget(self):
        # self.right_frame.setVisible(True)
        self.cross_section_widget.setVisible(True)
        # self.right_frame.adjustSize()
        # self.setFixedWidth(1000)
        #
        section_type = self.comboBox_section_type.currentIndex()
        self.cross_section_widget.set_inputs_to_geometry_creator(section_type=section_type)            
        # self.alternate_cross_section_button_label()

    def show_material_widget(self):
        # self.right_frame.setVisible(True)
        self.material_widget.reset()
        self.material_widget.load_data_from_materials_library()
        self.material_widget.setVisible(True)
        # self.right_frame.adjustSize()
        # self.setFixedWidth(1000)
        #        
        # self.alternate_material_button_label()

    def create_list_of_unit_labels(self):
        self.unit_labels = []
        self.unit_labels.append(self.label_unit_delta_x)
        self.unit_labels.append(self.label_unit_delta_y)
        self.unit_labels.append(self.label_unit_delta_z)
        self.unit_labels.append(self.label_unit_diameter)
        self.unit_labels.append(self.label_unit_bending_radius)

    def update_legth_units(self):
        index = self.comboBox_length_unit.currentIndex()
        if index == 0:
            self.length_unit = "m"
        elif index == 1:
            self.length_unit = "mm"
        else:
            self.length_unit = "in"
        #
        for _label in self.unit_labels:
            _label.setText(f"[{self.length_unit}]")

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
            if self.bending_factor:
                bend_pipe = True
            else:
                bend_pipe = False
            self.geometry_widget.stage_pipe_deltas(dx, dy, dz, bend_pipe)
        except ValueError:
            pass

    def create_segment_callback(self):
        self.propagate_section()
        dx, dy, dz = self.get_segment_deltas()
        if (dx, dy, dz) == (0, 0, 0):
            return
        self.geometry_widget.commit_structure()
        self.add_segment_information_to_file()
        self.update_segment_tag()
        self.reset_deltas()

    def propagate_section(self):
        if not self.cross_section_widget.isVisible():
            if self.cross_section_info is not None:
                tag = self.get_current_segment_tag()
                self.segment_information[tag] = self.cross_section_info

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

    def add_segment_information_to_file(self):
        return
        lines = list(self.segment_information.keys())
        self.file.create_segment_file(lines)
        tag = self.get_current_segment_tag()
        self.file.add_cross_section_segment_in_file(tag, self.segment_information[tag])

    def update_segment_tag(self):
        tag = self.get_segment_tag()
        self.segment_information[tag] = dict()
        self.comboBox_segment_id.clear()
        for key in self.segment_information.keys():
            text = f" Segment-{key}"
            self.comboBox_segment_id.addItem(text)
            self.comboBox_segment_id.setCurrentText(text)

    def get_current_segment_tag(self):
        return 0
        tag = self.comboBox_segment_id.currentText().split("Segment-")[1]
        return int(tag)

    def define_cross_section(self):

        # self.cross_section_info = None
        # tag = self.get_current_segment_tag()

        if self.cross_section_widget.tabWidget_general.currentIndex() == 0:
            if self.cross_section_widget.tabWidget_pipe_section.currentIndex() == 0:
                self.cross_section_widget.get_straight_pipe_parameters()
                self.cross_section_info = { "section label" : "pipe (constant)",
                                            "section parameters" : self.cross_section_widget.section_parameters  }
                diameter = self.cross_section_widget.section_parameters["outer_diameter"]
                self.geometry_widget.update_default_diameter(diameter)
                self.lineEdit_section_diameter.setText(str(diameter))
            else:
                self.cross_section_widget.get_variable_section_pipe_parameters()
                self.cross_section_info = { "section label" : "pipe (variable)",
                                            "section parameters" : self.cross_section_widget.variable_parameters  }
        else:
            self.cross_section_widget.get_beam_section_parameters()
            self.cross_section_info = { "section label" : "beam",
                                        "beam section type" : self.cross_section_widget.section_label,
                                        "section parameters" : self.cross_section_widget.section_parameters  }
        
        # self.segment_information[tag] = self.cross_section_info
        self.cross_section_widget.setVisible(False)
        # self.reset_appearance_to_default()
        # self.alternate_cross_section_button_label()

    def define_material(self):
        # temporary
        tag = self.get_current_segment_tag()
        aux = self.segment_information[tag]
        material_tag = self.material_widget.get_selected_material_id()
        if material_tag is not None:
            aux["material id"] = material_tag 
        #
        self.segment_information[tag] = aux
        self.material_widget.setVisible(True)
        self.reset_appearance_to_default()
        self.alternate_material_button_label()

    def delete_segment(self):
        pass

    def process_geometry_callback(self):
        self.geometry_widget.show_passive_points = True
        self.geometry_widget.unstage_structure()
        self.export_cad_file()
        app().update()
        app().main_window.opv_widget.updatePlots()
        app().main_window.use_structural_setup_workspace()

    def export_cad_file(self):
        exporter = CADHandler()
        pipeline = app().geometry_toolbox.pipeline
        geometry_filename = "geometry_pipeline.step"
        geometry_path = self.file.get_file_path_inside_project_directory(geometry_filename)
        exporter.save(geometry_path, pipeline)

        if os.path.exists(self.file._entity_path):
            os.remove(self.file._entity_path)

        geometry_filename = os.path.basename(geometry_path)
        # self.project.edit_project_geometry(geometry_filename)
        self.file.update_project_attributes(element_size = 0.01, 
                                            geometry_tolerance = 1e-6,
                                            geometry_filename=geometry_filename)

        self.project.initial_load_project_actions(self.file.project_ini_file_path)
        self.project.load_project_files()
        self.complete = True
