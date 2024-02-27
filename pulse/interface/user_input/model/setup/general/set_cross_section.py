from PyQt5.QtWidgets import QDialog, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np
import configparser
import matplotlib.pyplot as plt

from pulse import UI_DIR
from pulse.interface.user_input.model.setup.general.cross_section_inputs import CrossSectionWidget
from pulse.interface.user_input.model.setup.structural.get_standard_cross_section import GetStandardCrossSection
from pulse.preprocessing.cross_section import CrossSection, get_beam_section_properties, get_points_to_plot_section
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse.tools.utils import *

window_title = "ERROR MESSAGE"

class SetCrossSectionInput(QDialog):
    def __init__(   self, project, opv, 
                    pipe_to_beam = False,
                    beam_to_pipe = False,
                    lines_to_update_cross_section = [], 
                    elements_to_update_cross_section = [],
                    *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "model/setup/general/set_cross_section.ui", self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.input_widget = CrossSectionWidget()

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_id = self.opv.getListPickedLines()
        self.elements_id = self.opv.getListPickedElements()

        self.project = project
        self.preprocessor = project.preprocessor
        self.file = project.file
        self.before_run = project.get_pre_solution_model_checks()
        # self.preprocessor.get_nodes_and_elements_with_expansion()

        self.structural_elements = self.project.preprocessor.structural_elements
        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity

        self.pipe_to_beam = pipe_to_beam
        self.beam_to_pipe = beam_to_pipe
        self.lines_to_update_cross_section = lines_to_update_cross_section
        self.elements_to_update_cross_section = elements_to_update_cross_section
        self.remove_expansion_joint_tables_files = True

        self.section_id_by_lines = None
        self.section_id_by_elements = None
        self.section_type = None
        self.section_parameters = None
        self.section_info = None
        self._element_type = None
        self._section_parameters = None

        self.complete = False
        self.stop = False
        self.flip = False
 
        self.currentTab = 0
        self.list_elements = []
        self.section_data_lines = {}
        self.section_data_elements = {}

        self.define_qt_variables()
        self.create_connections()
        self.load_existing_sections()
        self.initial_condition()
        self.update_QDialog_info()       
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.confirm_pipe()
            if self.tabWidget_general.currentIndex() == 1:
                self.confirm_beam()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def define_qt_variables(self):

        # QFrame
        self.main_frame = self.findChild(QFrame, 'main_frame')

        # QGridLayout
        self.grid_layout = self.main_frame.layout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.input_widget)

        # QLabel
        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        
        # QLineEdit
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_ID.setEnabled(True)

        # QPushButton
        self.pushButton_confirm_pipe = self.findChild(QPushButton, 'pushButton_confirm_pipe')
        self.pushButton_confirm_beam = self.findChild(QPushButton, 'pushButton_confirm_beam')
        self.pushButton_flip_element_ids_initial = self.findChild(QPushButton, 'pushButton_flip_element_ids_initial')
        self.pushButton_flip_element_ids_final = self.findChild(QPushButton, 'pushButton_flip_element_ids_final')
        self.pushButton_load_section_info = self.findChild(QPushButton, "pushButton_load_section_info")
        self.pushButton_plot_pipe_cross_section = self.findChild(QPushButton, 'pushButton_plot_pipe_cross_section')
        self.pushButton_plot_beam_cross_section = self.findChild(QPushButton, 'pushButton_plot_beam_cross_section')
        self.pushButton_select_standard_section = self.findChild(QPushButton, 'pushButton_select_standard_section')
        self.pushButton_select_standard_section_initial = self.findChild(QPushButton, 'pushButton_select_standard_section_initial')
        self.pushButton_select_standard_section_final = self.findChild(QPushButton, 'pushButton_select_standard_section_final')
        self.pushButton_check_if_section_is_normalized = self.findChild(QPushButton, 'pushButton_check_if_section_is_normalized')

        # QRadioButton
        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_pipe_section = self.findChild(QTabWidget, 'tabWidget_pipe_section')
        self.tabWidget_beam_section = self.findChild(QTabWidget, 'tabWidget_beam_section')
        self.tabWidget_sections_data = self.findChild(QTabWidget, 'tabWidget_sections_data')

        # QWidget
        self.tab_pipe = self.tabWidget_general.findChild(QWidget, "tab_pipe")
        self.tab_beam = self.tabWidget_general.findChild(QWidget, "tab_beam")
        self.tab_straight_pipe_section = self.tabWidget_pipe_section.findChild(QWidget, "tab_straight_pipe_section")
        self.tab_variable_pipe_section = self.tabWidget_pipe_section.findChild(QWidget, "tab_variable_pipe_section")
        self.tab_rectangular_section = self.tabWidget_beam_section.findChild(QWidget, "tab_rectangular_section")
        self.tab_circular_section = self.tabWidget_beam_section.findChild(QWidget, "tab_circular_section")
        self.tab_C_section = self.tabWidget_beam_section.findChild(QWidget, "tab_C_section")
        self.tab_I_section = self.tabWidget_beam_section.findChild(QWidget, "tab_I_section")
        self.tab_T_section = self.tabWidget_beam_section.findChild(QWidget, "tab_T_section")
        self.tab_generic_section = self.tabWidget_beam_section.findChild(QWidget, "tab_generic_section")
        self.tab_attributed_by_lines = self.tabWidget_sections_data.findChild(QWidget, 'tab_attributed_by_lines')
        self.tab_attributed_by_elements = self.tabWidget_sections_data.findChild(QWidget, 'tab_attributed_by_elements')
        
        # QTabWidget
        self.tab_sections =  self.tabWidget_general.findChild(QTabWidget, 'tab_sections')

        # QTreeWidget
        self.treeWidget_sections_parameters_by_lines = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_lines')
        self.treeWidget_sections_parameters_by_elements = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_elements')  
            
    def create_connections(self):

        self.lineEdit_selected_ID.editingFinished.connect(self.update_highlights)

        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)
                
        self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe)
        self.pushButton_confirm_beam.clicked.connect(self.confirm_beam)
        self.pushButton_flip_element_ids_initial.clicked.connect(self.flip_element_ids)
        self.pushButton_flip_element_ids_final.clicked.connect(self.flip_element_ids)

        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        self.tabWidget_pipe_section.currentChanged.connect(self.tabEvent_pipe)

        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_elements.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_element)
        self.treeWidget_sections_parameters_by_elements.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_element)
        self.pushButton_load_section_info.clicked.connect(self.load_section_info)
        self.pushButton_load_section_info.setDisabled(True)

    def load_existing_sections(self):
        """
        """
        # self.config_treeWidget()
        self.section_id_data_lines = {}
        self.section_id_data_elements = {}
        self.treeWidget_sections_parameters_by_lines.clear()
        self.treeWidget_sections_parameters_by_elements.clear()
        self.section_data_lines, self.section_data_elements = self.file.get_cross_sections_from_file()

        if len(self.section_data_elements) == 0 and len(self.section_data_lines) == 0:
            self.tabWidget_general.removeTab(2)
        elif len(self.section_data_lines) == 0:
            self.tabWidget_sections_data.removeTab(0)
        elif len(self.section_data_elements) == 0:
            self.tabWidget_sections_data.removeTab(1)

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_lines.items():
            self.section_id_data_lines[section_id] = [tag_type, tags]
            str_parameters = str(section_parameters)[1:-1]
            new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_elements.items():
            self.section_id_data_elements[section_id] = [tag_type, tags]
            str_parameters = str(section_parameters)[1:-1]
            new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_sections_parameters_by_elements.addTopLevelItem(new)

    def initial_condition(self):
        """
        """
        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentWidget(self.tab_beam)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentWidget(self.tab_pipe)
            self.tabWidget_general.setTabEnabled(1, False)
        
        if self.lines_to_update_cross_section != []:
            self.label_selected_id.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_to_update_cross_section)

        elif self.elements_to_update_cross_section != []:
            self.label_selected_id.setText("Elements IDs:")
            self.radioButton_selected_elements.setChecked(True)
            self.write_ids(self.elements_to_update_cross_section)  

    def update_QDialog_info(self):

        if len(self.lines_id) > 0:   
            self.input_widget.reset_all_input_texts()
            self.selection = self.dict_tag_to_entity[self.lines_id[0]]
            element_type = self.selection.structural_element_type
            if element_type is None:
                for element_id in self.preprocessor.line_to_elements[self.lines_id[0]]:
                    element = self.structural_elements[element_id]
                    element_type = element.element_type
                    if element_type in ["pipe_1", "beam_1"]:
                        break
            _variable_cross_section_data = self.selection.variable_cross_section_data

        elif len(self.elements_id) > 0:   
            self.input_widget.reset_all_input_texts()
            self.selection = self.structural_elements[self.elements_id[0]]
            element_type = self.selection.element_type
            _variable_cross_section_data = None
        else:
            return

        if _variable_cross_section_data is None:
            if self.selection.cross_section is not None:
                cross = self.selection.cross_section
                self.section_label = cross.section_info["section_type_label"]
                self.section_parameters = cross.section_info["section_parameters"]
                        
                if element_type == 'pipe_1':
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                    self.tabWidget_pipe_section.setCurrentWidget(self.tab_straight_pipe_section)
                                
                elif element_type in ['beam_1']:
                    self.tabWidget_general.setCurrentWidget(self.tab_beam)

                self.update_section_entries()

        else:

            if element_type == 'pipe_1':
                self.tabWidget_general.setCurrentIndex(0)
                if self.selection.variable_cross_section_data:
                    self.tabWidget_pipe_section.setCurrentIndex(1)
                    self.update_section_entries(variable_section=True)
            elif element_type in ['beam_1']:
                self.tabWidget_general.setCurrentWidget(self.tab_beam)

        self.update_tabs()
        self.update_line_and_element_ids()

    def on_click_treeWidget_section_parameters_by_line(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_lines = int(key)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                self.pushButton_load_section_info.setDisabled(False)
                [self._element_type, self._section_parameters, *args] = self.section_data_lines[int(key)]

    def on_doubleClick_treeWidget_section_parameters_by_line(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_lines = int(key)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                [self._element_type, self._section_parameters, *args] = self.section_data_lines[int(key)]
                self.load_section_info()

    def on_click_treeWidget_section_parameters_by_element(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_elements = int(key)
        if key != "":
            if int(key) in self.section_data_elements.keys():
                self.pushButton_load_section_info.setDisabled(False)
                [self._element_type, self._section_parameters, *args] = self.section_data_elements[int(key)]

    def on_doubleClick_treeWidget_section_parameters_by_element(self, item):
        self.input_widget.reset_all_input_texts()
        key = item.text(0)
        self.section_id_by_elements = int(key)
        if key != "":
            if int(key) in self.section_data_elements.keys():
                [self._element_type, self._section_parameters, *args] = self.section_data_elements[int(key)]
                self.load_section_info()

    def load_section_info(self):
        """
        """
        self.input_widget.reset_all_input_texts()
        if self._element_type is not None:
            if self._element_type == "pipe_1":

                if len(self._section_parameters) == 6:
                    for index, lineEdit in enumerate(self.input_widget.list_straight_pipe_entries):
                        lineEdit.setText(str(self._section_parameters[index]))
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                    self.tabWidget_pipe_section.setCurrentWidget(self.tab_straight_pipe_section)

                elif len(self._section_parameters) == 10:
                    for index, lineEdit in enumerate(self.input_widget.list_variable_pipe_entries):
                        lineEdit.setText(str(self._section_parameters[index]))
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                    self.tabWidget_pipe_section.setCurrentWidget(self.tab_variable_pipe_section)
            
            elif "beam_1" in self._element_type:
                
                section_type = self._element_type.split("beam_1 - ")[1]
                self.tabWidget_general.setCurrentWidget(self.tab_beam)
                
                if section_type == "Rectangular section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_rectangular_section)
                    [base, height, base_in, height_in, offset_y, offset_z] = self._section_parameters
                    self.section_type = 1
                    self.input_widget.lineEdit_base_rectangular_section.setText(str(base))
                    self.input_widget.lineEdit_height_rectangular_section.setText(str(height))
                    self.input_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
                    if base_in != 0 and height_in != 0:
                        self.input_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 

                if section_type == "Circular section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_circular_section)
                    [outside_diameter_beam, thickness, offset_y, offset_z] = self._section_parameters
                    self.section_type = 2
                    self.input_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
                    self.input_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
                    if thickness != 0:
                        self.input_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))

                if section_type == "C-section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_C_section)
                    [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 3
                    self.input_widget.lineEdit_height_C_section.setText(str(h))
                    self.input_widget.lineEdit_w1_C_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_C_section.setText(str(tw))
                    self.input_widget.lineEdit_w2_C_section.setText(str(w2))
                    self.input_widget.lineEdit_t1_C_section.setText(str(t1))   
                    self.input_widget.lineEdit_t2_C_section.setText(str(t2))
                    self.input_widget.lineEdit_offsety_C_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_C_section.setText(str(offset_z))  

                if section_type == "I-section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_I_section)
                    [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 4
                    self.input_widget.lineEdit_height_I_section.setText(str(h))
                    self.input_widget.lineEdit_w1_I_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_I_section.setText(str(tw))
                    self.input_widget.lineEdit_w2_I_section.setText(str(w2))
                    self.input_widget.lineEdit_t1_I_section.setText(str(t1))   
                    self.input_widget.lineEdit_t2_I_section.setText(str(t2))
                    self.input_widget.lineEdit_offsety_I_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_I_section.setText(str(offset_z))

                if section_type == "T-section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_T_section)
                    [h, w1, t1, tw, offset_y, offset_z] = self._section_parameters
                    self.section_type = 5
                    self.input_widget.lineEdit_height_T_section.setText(str(h))
                    self.input_widget.lineEdit_w1_T_section.setText(str(w1))
                    self.input_widget.lineEdit_tw_T_section.setText(str(tw))
                    self.input_widget.lineEdit_t1_T_section.setText(str(t1))
                    self.input_widget.lineEdit_offsety_T_section.setText(str(offset_y))
                    self.input_widget.lineEdit_offsetz_T_section.setText(str(offset_z))

                if section_type == "Generic section":
                    self.tabWidget_beam_section.setCurrentWidget(self.tab_generic_section)
        
        if self.section_id_by_lines in self.section_id_data_lines.keys():
            [tag_type, tags] = self.section_id_data_lines[self.section_id_by_lines]
            str_tags = str(tags)
            if tag_type == "line ids":
                self.radioButton_selected_lines.setChecked(True)                
                self.opv.opvRenderer.highlight_lines(tags)
                if len(self._section_parameters) == 10:
                    if len(tags) == 1:
                        line_elements = self.project.preprocessor.line_to_elements[tags[0]]
                        self.input_widget.lineEdit_element_id_initial.setText(str(line_elements[0]))
                        self.input_widget.lineEdit_element_id_final.setText(str(line_elements[-1]))
        
        if self.section_id_by_elements in self.section_id_data_elements.keys():
            [tag_type, tags] = self.section_id_data_elements[self.section_id_by_elements]
            str_tags = str(tags)
            if tag_type == "element ids":
                self.radioButton_selected_elements.setChecked(True)
                self.opv.opvRenderer.highlight_elements(tags)

        self.lineEdit_selected_ID.setText(str_tags[1:-1])
        
        self.section_id_by_lines = None
        self.section_id_by_elements = None
        self._element_type = None
        self._section_parameters = None

    def config_treeWidget(self):

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)

        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,120)
        self.treeWidget_sections_parameters_by_lines.setFont(font)
        # self.treeWidget_sections_parameters_by_lines.setFont(1, font)
        # self.treeWidget_sections_parameters_by_lines.setFont(2, font)
        # self.treeWidget_sections_parameters_by_lines.setColumnWidth(2,20)

        self.treeWidget_sections_parameters_by_elements.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_elements.setColumnWidth(1,120)
        self.treeWidget_sections_parameters_by_elements.setFont(font)
        # self.treeWidget_sections_parameters_by_elements.setFont(1, font)
        # self.treeWidget_sections_parameters_by_elements.setFont(2, font)
        # self.treeWidget_sections_parameters_by_elements.setColumnWidth(2,20)


    def check_variable_section_pipe(self):
        
        self.input_widget.get_variable_section_pipe_parameters()
        variable_parameters = self.input_widget.variable_parameters
        
        self.project.set_variable_cross_section_by_line(self.lines_typed[0], variable_parameters)
        # self.project.add_cross_sections_expansion_joints_valves_in_file(self.list_elements)
        self.project.set_structural_element_type_by_lines(self.lines_typed[0], self.element_type)
        self.file.modify_variable_cross_section_in_file(self.lines_typed[0], variable_parameters)
        # self.project.set_variable_cross_section_by_line(self.lines_typed[0], variable_parameters)
        self.project._set_variable_cross_section_to_selected_line(self.lines_typed[0], variable_parameters)
        self.project.reset_number_sections_by_line(self.lines_typed[0])
        self.actions_to_finalize()

    def update_section_entries(self, variable_section=False):
        """
        """
        if variable_section:

            self.update_variable_section_element_ids()   
            data = self.selection.variable_cross_section_data

            for index, lineEdit in enumerate(self.list_pipe_section_entries[6:-2]):
                lineEdit.setText(str(data[index]))
            
            return
        
        if self.section_label == 'Pipe section':

            outside_diameter = self.section_parameters["outer_diameter"]
            thickness = self.section_parameters["thickness"]
            offset_y = self.section_parameters["offset_y"] 
            offset_z = self.section_parameters["offset_z"]
            insulation_thickness = self.section_parameters["insulation_thickness"]
            insulation_density = self.section_parameters["insulation_density"]

            self.section_type = 0
            self.input_widget.lineEdit_outside_diameter.setText(str(outside_diameter))
            self.input_widget.lineEdit_wall_thickness.setText(str(thickness))
            if offset_y != 0:
                self.input_widget.lineEdit_offset_y.setText(str(offset_y))
            if offset_z != 0:
                self.input_widget.lineEdit_offset_z.setText(str(offset_z))
            if insulation_density != 0:
                self.input_widget.lineEdit_insulation_density.setText(str(insulation_density))
            if insulation_thickness != 0:
                self.input_widget.lineEdit_insulation_thickness.setText(str(insulation_thickness))

        elif self.section_label == 'Rectangular section':
            [base, height, base_in, height_in, offset_y, offset_z] = self.section_parameters
            self.section_type = 1
            self.input_widget.lineEdit_base_rectangular_section.setText(str(base))
            self.input_widget.lineEdit_height_rectangular_section.setText(str(height))
            self.input_widget.lineEdit_offsety_rectangular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
            if base_in != 0 and height_in != 0:
                self.input_widget.lineEdit_wall_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 
        
        elif self.section_label == 'Circular section':
            [outside_diameter_beam, thickness, offset_y, offset_z] = self.section_parameters
            self.section_type = 2
            self.input_widget.lineEdit_outside_diameter_circular_section.setText(str(outside_diameter_beam))
            self.input_widget.lineEdit_offsety_circular_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_circular_section.setText(str(offset_z))
            if thickness != 0:
                self.input_widget.lineEdit_wall_thickness_circular_section.setText(str(thickness))
        
        elif self.section_label == 'C-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 3
            self.input_widget.lineEdit_height_C_section.setText(str(h))
            self.input_widget.lineEdit_w1_C_section.setText(str(w1))
            self.input_widget.lineEdit_tw_C_section.setText(str(tw))
            self.input_widget.lineEdit_w2_C_section.setText(str(w2))
            self.input_widget.lineEdit_t1_C_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_C_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_C_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_C_section.setText(str(offset_z))             
        
        elif self.section_label == 'I-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 4
            self.input_widget.lineEdit_height_I_section.setText(str(h))
            self.input_widget.lineEdit_w1_I_section.setText(str(w1))
            self.input_widget.lineEdit_tw_I_section.setText(str(tw))
            self.input_widget.lineEdit_w2_I_section.setText(str(w2))
            self.input_widget.lineEdit_t1_I_section.setText(str(t1))   
            self.input_widget.lineEdit_t2_I_section.setText(str(t2))
            self.input_widget.lineEdit_offsety_I_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_I_section.setText(str(offset_z))
        
        elif self.section_label == 'T-section':
            [h, w1, t1, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 5
            self.input_widget.lineEdit_height_T_section.setText(str(h))
            self.input_widget.lineEdit_w1_T_section.setText(str(w1))
            self.input_widget.lineEdit_tw_T_section.setText(str(tw))
            self.input_widget.lineEdit_t1_T_section.setText(str(t1))
            self.input_widget.lineEdit_offsety_T_section.setText(str(offset_y))
            self.input_widget.lineEdit_offsetz_T_section.setText(str(offset_z))  

    def update_variable_section_element_ids(self):
        """
        """
        if len(self.lines_id) > 0:
            line_id = self.lines_id[0]
            # entity = self.dict_tag_to_entity[line_id]
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_pipe_section.setCurrentIndex(1)
            if len(self.lines_id) == 1:
                self.list_elements = self.project.preprocessor.line_to_elements[line_id]
                self.input_widget.lineEdit_element_id_initial.setText(str(self.list_elements[0]))
                self.input_widget.lineEdit_element_id_final.setText(str(self.list_elements[-1]))
    
    def update_tabs(self):
        """
        """
        if self.tabWidget_general.currentIndex() == 0:
            if self.tabWidget_pipe_section.currentIndex() == 1:
                return
       
        if self.section_type == 0:
            self.tabWidget_pipe_section.setCurrentWidget(self.tab_straight_pipe_section)
            return

        beam_tabs = [   self.tab_rectangular_section, 
                        self.tab_circular_section, 
                        self.tab_C_section, 
                        self.tab_I_section, 
                        self.tab_T_section,
                        self.tab_generic_section  ]

        for i in range(6):
            if i+1 == self.section_type:
                # self.tabWidget_beam_section.setTabEnabled(i, True)
                self.tabWidget_beam_section.setCurrentWidget(beam_tabs[i])
            # else:
                # self.tabWidget_beam_section.setTabEnabled(i, False)

    def update(self):
        """
        """
        self.lines_id = self.opv.getListPickedLines()
        self.elements_id = self.opv.getListPickedElements()
        self.update_QDialog_info()

    def update_line_and_element_ids(self):
        """
        """
        if self.lines_id != []:
            self.label_selected_id.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_id)
            
        elif self.elements_id != []:
            self.label_selected_id.setText("Elements IDs:")
            self.radioButton_selected_elements.setChecked(True)
            self.write_ids(self.elements_id)
            
        else:
            if self.tabWidget_general.currentIndex() == 0:
                if self.tabWidget_pipe_section.currentIndex() == 1:
                    self.lineEdit_selected_ID.setText("")
                    return
            self.label_selected_id.setText("Lines IDs:")
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all_lines.setChecked(True)

    def update_highlights(self):
        """
        """
        lineEdit = self.lineEdit_selected_ID.text()
        if lineEdit != "":
            if self.radioButton_selected_lines.isChecked():
                _stop, _lines_typed = self.before_run.check_input_LineID(lineEdit)
                if _stop:
                    return
                self.opv.opvRenderer.highlight_lines(_lines_typed)
            if self.radioButton_selected_elements.isChecked():
                _stop, _elements_typed = self.before_run.check_input_ElementID(lineEdit)
                if _stop:
                    return
                self.opv.opvRenderer.highlight_elements(_elements_typed) 

    def flip_element_ids(self):
        self.flip = not self.flip
        temp_initial = self.input_widget.lineEdit_element_id_initial.text()
        temp_final = self.input_widget.lineEdit_element_id_final.text()
        self.input_widget.lineEdit_element_id_initial.setText(temp_final)
        self.input_widget.lineEdit_element_id_final.setText(temp_initial)

    def radioButtonEvent(self):

        self.lineEdit_selected_ID.setEnabled(True)
        self.lineEdit_selected_ID.setText("")

        if self.radioButton_all_lines.isChecked():
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)

        elif self.radioButton_selected_lines.isChecked():
            self.label_selected_id.setText("Lines IDs:")
            # if self.lines_id != []:
            #     self.write_ids(self.lines_id)
                    
        elif self.radioButton_selected_elements.isChecked():
            self.label_selected_id.setText("Elements IDs:")
            # if self.elements_id != []:
            #     self.write_ids(self.elements_id)
        
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)
    
    def tabEvent_cross_section(self):
        """
        """
        if self.tabWidget_general.currentIndex() == 0:
            if self.tabWidget_pipe_section.currentIndex() == 1:
                self.tabEvent_pipe()
            for i in range(2):
                self.tabWidget_pipe_section.setTabEnabled(i, True)
        else:
            self.set_disable_radioButtons(False)
            for i in range(6):
                self.tabWidget_beam_section.setTabEnabled(i, True)

    def tabEvent_pipe(self):
        """
        """
        if self.tabWidget_pipe_section.currentIndex() == 0:
            self.pushButton_plot_pipe_cross_section.setDisabled(False)
            self.set_disable_radioButtons(False)
        if self.tabWidget_pipe_section.currentIndex() == 1:
            self.pushButton_plot_pipe_cross_section.setDisabled(True)
            self.radioButton_selected_lines.setChecked(True)
            self.radioButton_selected_elements.setDisabled(True)
            self.radioButton_all_lines.setDisabled(True)
            self.update_variable_section_element_ids()

    def set_disable_radioButtons(self, _bool):
        self.radioButton_selected_lines.setDisabled(_bool)
        self.radioButton_selected_elements.setDisabled(_bool)
        self.radioButton_all_lines.setDisabled(_bool)

    def actions_to_finalize(self):
        plt.close()
        self.complete = True
        self.opv.updateEntityRadius()
        self.opv.changePlotToEntitiesWithCrossSection()
        self.close()

    def check_straight_pipe(self, plot=False):

        self.input_widget.get_straight_pipe_parameters()

        self.section_label = self.input_widget.section_label
        self.section_parameters = self.input_widget.section_parameters
        self.section_properties = self.input_widget.section_properties
        self.pipe_section_info = self.input_widget.pipe_section_info

        if plot:
            return
        
        self.cross_section = CrossSection(pipe_section_info=self.pipe_section_info)

        self.set_cross_sections()
        self.actions_to_finalize()

    def confirm_pipe(self):
        
        self.element_type = 'pipe_1'

        if self.radioButton_selected_elements.isChecked():

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
            if self.stop:
                return

        elif self.radioButton_selected_lines.isChecked():

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True 

        if self.tabWidget_pipe_section.currentIndex() == 0:
            self.check_straight_pipe()

        elif self.tabWidget_pipe_section.currentIndex() == 1:
            self.check_variable_section_pipe()

    def confirm_beam(self):
        self.element_type = 'beam_1'
        self.check_beam()

    def check_beam(self):

        if self.radioButton_selected_lines.isChecked():
            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True        
        
        elif self.radioButton_all_lines.isChecked():
            self.lines_typed = self.preprocessor.all_lines

        if self.tabWidget_general.currentIndex() == 1:

            if self.input_widget.get_beam_section_parameters():
                return
            
            self.section_label = self.input_widget.section_label
            self.section_parameters = self.input_widget.section_parameters
            self.section_properties = self.input_widget.section_properties

            self.beam_section_info = {  "section_type_label" : self.section_label,
                                        "section_parameters" : self.section_parameters,
                                        "section_properties" : self.section_properties  }
       
            self.cross_section = CrossSection(beam_section_info=self.beam_section_info)
            self.set_cross_sections()
            self.project.set_capped_end_by_lines(self.lines_typed, False)
            self.project.set_structural_element_wall_formulation_by_lines(self.lines_typed, None)

        self.actions_to_finalize()

    def set_cross_sections(self):

        if self.radioButton_selected_lines.isChecked():
            if self.remove_expansion_joint_tables_files:
                self.process_expansion_joint_table_files_removal(self.lines_typed)
            for line_id in self.lines_typed:
                self.project.reset_number_sections_by_line(line_id)
            self.project.add_valve_by_line(line_id, None, reset_cross=False)
            self.project._set_expansion_joint_to_selected_lines(self.lines_typed, None)
                
            self.project.set_cross_section_by_line(self.lines_typed, self.cross_section)
            self.project.set_structural_element_type_by_lines(self.lines_typed, self.element_type)
            
            if len(self.lines_typed) < 20:
                print("[Set Cross-section] - defined at the {} lines".format(self.lines_typed))
            else:
                print("[Set Cross-section] - defined at {} selected lines".format(len(self.lines_typed)))

        elif self.radioButton_selected_elements.isChecked():
            self.project.set_cross_section_by_elements(self.elements_typed, self.cross_section)
            self.project.add_cross_sections_expansion_joints_valves_in_file(self.elements_typed)
            # self.preprocessor.set_structural_element_type_by_element(self.elements_typed, self.element_type)
            
            if len(self.elements_typed) < 20:
                print("[Set Cross-section] - defined at the {} elements".format(self.elements_typed))
            else:
                print("[Set Cross-section] - defined at {} selected elements".format(len(self.elements_typed)))

        else:
            line_ids = self.preprocessor.all_lines
            if self.remove_expansion_joint_tables_files:
                self.process_expansion_joint_table_files_removal(line_ids)
            self.project.add_valve_by_line(line_ids, None, reset_cross=False)
            self.project._set_expansion_joint_to_selected_lines(line_ids, None)

            self.project.set_cross_section_by_line(line_ids, self.cross_section)
            self.project.set_structural_element_type_to_all(self.element_type)
            
            print("[Set Cross-section] - defined at all lines") 
        
        self.preprocessor.add_lids_to_variable_cross_sections()

    def process_expansion_joint_table_files_removal(self, list_line_ids):

        config = configparser.ConfigParser()
        config.read(self.project.file._entity_path)
        sections = config.sections()

        for section in sections:
            if "-" in section:
                line_id = int(section.split("-")[0])
            else:
                line_id = int(section)

            if line_id in list_line_ids:
                if "expansion joint stiffness" in config[section].keys():
                    str_joint_stiffness = config[section]['expansion joint stiffness']
                    _, joint_table_names, _ = self.project.file._get_expansion_joint_stiffness_from_string(str_joint_stiffness)
                    if joint_table_names is not None:
                        for table_name in joint_table_names:
                            self.project.remove_structural_table_files_from_folder(table_name, "expansion_joints_files")