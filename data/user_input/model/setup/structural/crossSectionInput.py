from pulse.preprocessing.entity import Entity
from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection, get_beam_section_properties, get_points_to_plot_section
from data.user_input.project.printMessageInput import PrintMessageInput
from pulse.utils import get_linear_distribution

import numpy as np
import matplotlib.pyplot as plt

window_title = "ERROR MESSAGE"

class CrossSectionInput(QDialog):
    def __init__(   self, project, opv, 
                    pipe_to_beam = False,
                    beam_to_pipe = False,
                    lines_to_update_cross_section = [], 
                    elements_to_update_cross_section = [],
                    *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/crossSectionInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()
        # self.preprocessor.get_nodes_and_elements_with_expansion()

        self.structural_elements = self.project.preprocessor.structural_elements
        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity

        self.pipe_to_beam = pipe_to_beam
        self.beam_to_pipe = beam_to_pipe
        self.lines_to_update_cross_section = lines_to_update_cross_section
        self.elements_to_update_cross_section = elements_to_update_cross_section
        self.remove_expansion_joint_tables_files = True

        self.section_type = None
        self.section_parameters = None
        self.section_info = None
        self.section_data = None
        self.complete = False
        self.stop = False
        self.flip = False
 
        self.currentTab = 0
        self.list_elements = []

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')
        self.lineEdit_selected_ID.setEnabled(True)

        self.lineEdit_outerDiameter = self.findChild(QLineEdit, 'lineEdit_outerDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')
        self.lineEdit_insulation_density = self.findChild(QLineEdit, 'lineEdit_insulation_density')
        self.lineEdit_insulation_thickness = self.findChild(QLineEdit, 'lineEdit_insulation_thickness')

        self.lineEdit_outerDiameter_initial = self.findChild(QLineEdit, 'lineEdit_outerDiameter_initial')
        self.lineEdit_thickness_initial = self.findChild(QLineEdit, 'lineEdit_thickness_initial')
        self.lineEdit_offset_y_initial = self.findChild(QLineEdit, 'lineEdit_offset_y_initial')
        self.lineEdit_offset_z_initial = self.findChild(QLineEdit, 'lineEdit_offset_z_initial')

        self.lineEdit_outerDiameter_final = self.findChild(QLineEdit, 'lineEdit_outerDiameter_final')
        self.lineEdit_thickness_final = self.findChild(QLineEdit, 'lineEdit_thickness_final')
        self.lineEdit_offset_y_final = self.findChild(QLineEdit, 'lineEdit_offset_y_final')
        self.lineEdit_offset_z_final = self.findChild(QLineEdit, 'lineEdit_offset_z_final')

        self.lineEdit_base_rectangular_section = self.findChild(QLineEdit, 'lineEdit_base_rectangular_section')
        self.lineEdit_height_rectangular_section = self.findChild(QLineEdit, 'lineEdit_height_rectangular_section')
        self.lineEdit_thickness_rectangular_section = self.findChild(QLineEdit, 'lineEdit_thickness_rectangular_section')
        self.lineEdit_offsety_rectangular_section = self.findChild(QLineEdit, 'lineEdit_offsety_rectangular_section')
        self.lineEdit_offsetz_rectangular_section = self.findChild(QLineEdit, 'lineEdit_offsetz_rectangular_section')

        self.lineEdit_outer_diameter_circular_section = self.findChild(QLineEdit, 'lineEdit_outer_diameter_circular_section')
        self.lineEdit_thickness_circular_section = self.findChild(QLineEdit, 'lineEdit_thickness_circular_section')
        self.lineEdit_offsety_circular_section = self.findChild(QLineEdit, 'lineEdit_offsety_circular_section')
        self.lineEdit_offsetz_circular_section = self.findChild(QLineEdit, 'lineEdit_offsetz_circular_section')

        self.lineEdit_height_C_section = self.findChild(QLineEdit, 'lineEdit_height_C_section')
        self.lineEdit_w1_C_section = self.findChild(QLineEdit, 'lineEdit_w1_C_section')
        self.lineEdit_t1_C_section = self.findChild(QLineEdit, 'lineEdit_t1_C_section')
        self.lineEdit_w2_C_section = self.findChild(QLineEdit, 'lineEdit_w2_C_section')
        self.lineEdit_t2_C_section = self.findChild(QLineEdit, 'lineEdit_t2_C_section')    
        self.lineEdit_tw_C_section = self.findChild(QLineEdit, 'lineEdit_tw_C_section')         
        self.lineEdit_offsety_C_section = self.findChild(QLineEdit, 'lineEdit_offsety_C_section')
        self.lineEdit_offsetz_C_section = self.findChild(QLineEdit, 'lineEdit_offsetz_C_section')

        self.lineEdit_height_I_section = self.findChild(QLineEdit, 'lineEdit_height_I_section')
        self.lineEdit_w1_I_section = self.findChild(QLineEdit, 'lineEdit_w1_I_section')
        self.lineEdit_t1_I_section = self.findChild(QLineEdit, 'lineEdit_t1_I_section')
        self.lineEdit_w2_I_section = self.findChild(QLineEdit, 'lineEdit_w2_I_section')
        self.lineEdit_t2_I_section = self.findChild(QLineEdit, 'lineEdit_t2_I_section')    
        self.lineEdit_tw_I_section = self.findChild(QLineEdit, 'lineEdit_tw_I_section') 
        self.lineEdit_offsety_I_section = self.findChild(QLineEdit, 'lineEdit_offsety_I_section')
        self.lineEdit_offsetz_I_section = self.findChild(QLineEdit, 'lineEdit_offsetz_I_section')

        self.lineEdit_height_T_section = self.findChild(QLineEdit, 'lineEdit_height_T_section')
        self.lineEdit_w1_T_section = self.findChild(QLineEdit, 'lineEdit_w1_T_section')
        self.lineEdit_t1_T_section = self.findChild(QLineEdit, 'lineEdit_t1_T_section')
        self.lineEdit_tw_T_section = self.findChild(QLineEdit, 'lineEdit_tw_T_section')  
        self.lineEdit_offsety_T_section = self.findChild(QLineEdit, 'lineEdit_offsety_T_section')
        self.lineEdit_offsetz_T_section = self.findChild(QLineEdit, 'lineEdit_offsetz_T_section')

        self.lineEdit_area = self.findChild(QLineEdit, 'lineEdit_area')
        self.lineEdit_Iyy = self.findChild(QLineEdit, 'lineEdit_Iyy')
        self.lineEdit_Izz = self.findChild(QLineEdit, 'lineEdit_Izz')
        self.lineEdit_Iyz = self.findChild(QLineEdit, 'lineEdit_Iyz')
        self.lineEdit_shear_coefficient = self.findChild(QLineEdit, 'lineEdit_shear_coefficient')

        self.lineEdit_element_id_initial = self.findChild(QLineEdit, 'lineEdit_element_id_initial')
        self.lineEdit_element_id_final = self.findChild(QLineEdit, 'lineEdit_element_id_final')

        self.lineEdit_outerDiameter_initial = self.findChild(QLineEdit, 'lineEdit_outerDiameter_initial')
        self.lineEdit_thickness_initial = self.findChild(QLineEdit, 'lineEdit_thickness_initial')
        self.lineEdit_offset_y_initial = self.findChild(QLineEdit, 'lineEdit_offset_y_initial')
        self.lineEdit_offset_z_initial = self.findChild(QLineEdit, 'lineEdit_offset_z_initial')

        self.lineEdit_outerDiameter_final = self.findChild(QLineEdit, 'lineEdit_outerDiameter_final')
        self.lineEdit_thickness_final = self.findChild(QLineEdit, 'lineEdit_thickness_final')
        self.lineEdit_offset_y_final = self.findChild(QLineEdit, 'lineEdit_offset_y_final')
        self.lineEdit_offset_z_final = self.findChild(QLineEdit, 'lineEdit_offset_z_final')

        self.lineEdit_insulation_thickness_variable_section = self.findChild(QLineEdit, 'lineEdit_insulation_thickness_variable_section')
        self.lineEdit_insulation_density_variable_section = self.findChild(QLineEdit, 'lineEdit_insulation_density_variable_section')

        self.create_lists_of_entries()

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()

        self.tabWidget_pipe_section = self.findChild(QTabWidget, 'tabWidget_pipe_section')
        self.tabWidget_pipe_section.currentChanged.connect(self.tabEvent_pipe)
        self.currentTab_pipe = self.tabWidget_pipe_section.currentIndex()

        self.tabWidget_beam_section = self.findChild(QTabWidget, 'tabWidget_beam_section')
        self.tabWidget_beam_section.currentChanged.connect(self.tabEvent_beam)
        self.currentTab_beam = self.tabWidget_beam_section.currentIndex()
        
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

        self.pushButton_confirm_pipe = self.findChild(QPushButton, 'pushButton_confirm_pipe')
        self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe)

        self.pushButton_confirm_beam = self.findChild(QPushButton, 'pushButton_confirm_beam')  
        self.pushButton_confirm_beam.clicked.connect(self.confirm_beam)

        # self.pushButton_confirm_generic_section_beam = self.findChild(QPushButton, 'pushButton_confirm_generic_section_beam')
        # self.pushButton_confirm_generic_section_beam.clicked.connect(self.confirm_beam)

        self.pushButton_plot_pipe_cross_section = self.findChild(QPushButton, 'pushButton_plot_pipe_cross_section')  
        self.pushButton_plot_pipe_cross_section.clicked.connect(self.plot_section)

        self.pushButton_plot_beam_cross_section = self.findChild(QPushButton, 'pushButton_plot_beam_cross_section')  
        self.pushButton_plot_beam_cross_section.clicked.connect(self.plot_section)

        self.pushButton_flip_element_ids = self.findChild(QPushButton, 'pushButton_flip_element_ids')
        self.pushButton_flip_element_ids.clicked.connect(self.flip_element_ids)

        self.comboBox_pipe = self.findChild(QComboBox, 'comboBox_pipe')
        # self.comboBox_pipe.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox_pipe.currentIndex()
                      
        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentWidget(self.tab_beam)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentWidget(self.tab_pipe)
            self.tabWidget_general.setTabEnabled(1, False)
        
        if self.lines_to_update_cross_section != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_to_update_cross_section)

        elif self.elements_to_update_cross_section != []:
            self.lineEdit_id_labels.setText("Elements IDs:")
            self.radioButton_selected_elements.setChecked(True)
            self.write_ids(self.elements_to_update_cross_section)  

        elif self.lines_id != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_id)
            
        elif self.elements_id != []:
            self.lineEdit_id_labels.setText("Elements IDs:")
            self.radioButton_selected_elements.setChecked(True)
            self.write_ids(self.elements_id)
                          
        else:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_all_lines.setChecked(True)  
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)
       
        self.update_QDialog_info()       
        self.exec_()

    def create_lists_of_entries(self):
        self.list_pipe_section_entries = [  self.lineEdit_outerDiameter,
                                            self.lineEdit_thickness,
                                            self.lineEdit_offset_y,
                                            self.lineEdit_offset_z,
                                            self.lineEdit_insulation_thickness,
                                            self.lineEdit_insulation_density,
                                            self.lineEdit_outerDiameter_initial,
                                            self.lineEdit_thickness_initial,
                                            self.lineEdit_offset_y_initial,
                                            self.lineEdit_offset_z_initial,
                                            self.lineEdit_outerDiameter_final,
                                            self.lineEdit_thickness_final,
                                            self.lineEdit_offset_y_final,
                                            self.lineEdit_offset_z_final,
                                            self.lineEdit_insulation_thickness_variable_section,
                                            self.lineEdit_insulation_density_variable_section  ] 

        self.list_beam_section_entries = [  self.lineEdit_base_rectangular_section,
                                            self.lineEdit_height_rectangular_section,
                                            self.lineEdit_thickness_rectangular_section,
                                            self.lineEdit_offsety_rectangular_section,
                                            self.lineEdit_offsetz_rectangular_section,
                                            self.lineEdit_outer_diameter_circular_section,
                                            self.lineEdit_thickness_circular_section,
                                            self.lineEdit_offsety_circular_section,
                                            self.lineEdit_offsetz_circular_section,
                                            self.lineEdit_height_C_section,
                                            self.lineEdit_w1_C_section,
                                            self.lineEdit_t1_C_section,
                                            self.lineEdit_w2_C_section,
                                            self.lineEdit_t2_C_section,
                                            self.lineEdit_tw_C_section,
                                            self.lineEdit_offsety_C_section,
                                            self.lineEdit_offsetz_C_section,
                                            self.lineEdit_height_I_section,
                                            self.lineEdit_w1_I_section,
                                            self.lineEdit_t1_I_section,
                                            self.lineEdit_w2_I_section,
                                            self.lineEdit_t2_I_section,
                                            self.lineEdit_tw_I_section,
                                            self.lineEdit_offsety_I_section,
                                            self.lineEdit_offsetz_I_section,
                                            self.lineEdit_height_T_section,
                                            self.lineEdit_w1_T_section,
                                            self.lineEdit_t1_T_section,
                                            self.lineEdit_tw_T_section,
                                            self.lineEdit_offsety_T_section,
                                            self.lineEdit_offsetz_T_section,
                                            self.lineEdit_area,
                                            self.lineEdit_Iyy,
                                            self.lineEdit_Izz,
                                            self.lineEdit_Iyz,
                                            self.lineEdit_shear_coefficient  ]     

    def update_QDialog_info(self):
        if len(self.lines_id) > 0:   
            self.reset_all_input_texts()
            self.selection = self.dict_tag_to_entity[self.lines_id[0]]
            element_type = self.selection.structural_element_type
            if element_type is None:
                for element_id in self.preprocessor.line_to_elements[self.lines_id[0]]:
                    element = self.structural_elements[element_id]
                    element_type = element.element_type
                    if element_type in ["pipe_1", "pipe_2", "beam_1"]:
                        break
            _variable_cross_section_data = self.selection.variable_cross_section_data
        elif len(self.elements_id) > 0:   
            self.reset_all_input_texts()
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
                        
                if element_type in ['pipe_1', 'pipe_2']:
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                    self.tabWidget_pipe_section.setCurrentWidget(self.tab_straight_pipe_section)
                                
                elif element_type in ['beam_1']:
                    self.tabWidget_general.setCurrentWidget(self.tab_beam)

                self.update_section_entries()

        else:

            if element_type in ['pipe_1', 'pipe_2']:
                self.tabWidget_general.setCurrentIndex(0)
                if self.selection.variable_cross_section_data:
                    self.tabWidget_pipe_section.setCurrentIndex(1)
                    self.update_section_entries(variable_section=True)
            
            elif element_type in ['beam_1']:
                self.tabWidget_general.setCurrentWidget(self.tab_beam)

        self.update_tabs()

    def check_variable_section_pipe(self):
        
        message = ""
        N = len(self.list_elements)

        outerDiameter_initial = self.check_inputs(self.lineEdit_outerDiameter_initial, "'outer diameter (initial)'")
        if self.stop:
            return
        outerDiameter_final = self.check_inputs(self.lineEdit_outerDiameter_final, "'outer diameter (final)'")
        if self.stop:
            return

        thickness_initial = self.check_inputs(self.lineEdit_thickness_initial, "'thickness (initial)'")
        if self.stop:
            return
        thickness_final = self.check_inputs(self.lineEdit_thickness_final, "'thickness (final)'")
        if self.stop:
            return

        if np.isclose(outerDiameter_initial, 2*thickness_initial, atol=1e-5) or 2*thickness_initial > outerDiameter_initial:
            message = "The INITIAL THICKNESS must be less than \nthe INITIAL OUTER RADIUS." 

        elif thickness_initial == 0.0:
            message = "The INITIAL THICKNESS must be greater than zero." 

        if np.isclose(outerDiameter_final, 2*thickness_final, atol=1e-5) or 2*thickness_final > outerDiameter_final:
            message = "The FINAL THICKNESS must be less than \nthe FINAL OUTER RADIUS." 

        elif thickness_final == 0.0:
            message = "The FINAL THICKNESS must be greater than zero." 
        
        if message != "":
            title = "INPUT CROSS-SECTION ERROR"
            PrintMessageInput([title, message, window_title])
            return

        offset_y_initial = self.check_inputs(self.lineEdit_offset_y_initial, "'offset y (initial)'", only_positive=False, zero_included=True)
        if self.stop:
            return
        offset_y_final = self.check_inputs(self.lineEdit_offset_y_final, "'offset y (final)'", only_positive=False, zero_included=True)
        if self.stop:
            return

        offset_z_initial = self.check_inputs(self.lineEdit_offset_z_initial, "'offset z (initial)'", only_positive=False, zero_included=True)
        if self.stop:
            return
        offset_z_final = self.check_inputs(self.lineEdit_offset_z_final, "'offset z (final)'", only_positive=False, zero_included=True)
        if self.stop:
            return
        
        insulation_thickness = self.check_inputs(   self.lineEdit_insulation_thickness_variable_section, 
                                                    "'insulation thickness (variable pipe section)'",
                                                    zero_included=True  )
        if self.stop:
            return
        
        insulation_density = self.check_inputs(   self.lineEdit_insulation_density_variable_section, 
                                                    "'density thickness (variable pipe section)'",
                                                    zero_included=True  )
        if self.stop:
            return    

        list_outerDiameter = get_linear_distribution(outerDiameter_initial, outerDiameter_final, N)
        list_thickness = get_linear_distribution(thickness_initial, thickness_final, N)
        list_offset_y = get_linear_distribution(offset_y_initial, offset_y_final, N)
        list_offset_z = get_linear_distribution(offset_z_initial, offset_z_final, N)

        if self.flip:
            list_outerDiameter = np.flip(list_outerDiameter)
            list_thickness = np.flip(list_thickness)
            list_offset_y = np.flip(list_offset_y)
            list_offset_z = np.flip(list_offset_z)

            list_variable_parameters = [    outerDiameter_final, thickness_final, offset_y_final, offset_z_final,
                                            outerDiameter_initial, thickness_initial, offset_y_initial, offset_z_initial,
                                            insulation_thickness, insulation_density  ]

        else:

            list_variable_parameters = [    outerDiameter_initial, thickness_initial, offset_y_initial, offset_z_initial,
                                            outerDiameter_final, thickness_final, offset_y_final, offset_z_final,
                                            insulation_thickness, insulation_density  ]
 
        self.section_label = "Pipe section"

        for index, element_id in enumerate(self.list_elements):
  
            section_parameters = {  "outer_diameter" : list_outerDiameter[index],
                                    "thickness" : list_thickness[index], 
                                    "offset_y" : list_offset_y[index], 
                                    "offset_z" : list_offset_z[index], 
                                    "insulation_thickness" : insulation_thickness, 
                                    "insulation_density" : insulation_density }
            
            pipe_section_info = {   "section_type_label" : self.section_label ,
                                    "section_parameters" : section_parameters }

            self.cross_section = CrossSection(pipe_section_info=pipe_section_info)
            self.project.set_cross_section_by_elements([element_id], self.cross_section)
        
        self.project.add_cross_sections_expansion_joints_valves_in_file(self.list_elements)
        self.project.set_structural_element_type_by_lines(self.lines_typed[0], self.element_type)
        self.project.set_variable_cross_section_by_line(self.lines_typed[0], list_variable_parameters)
        
        self.remove_line_from_list(self.lines_typed[0])
        self.actions_to_finalize()

    def update_section_entries(self, variable_section=False):

        if variable_section:
    
            data = self.selection.variable_cross_section_data

            for index, lineEdit in enumerate(self.list_pipe_section_entries[6:]):
                lineEdit.setText(str(data[index]))
            return
        
        if self.section_label == 'Pipe section':

            outer_diameter = self.section_parameters["outer_diameter"]
            thickness = self.section_parameters["thickness"]
            offset_y = self.section_parameters["offset_y"] 
            offset_z = self.section_parameters["offset_z"]
            insulation_thickness = self.section_parameters["insulation_thickness"]
            insulation_density = self.section_parameters["insulation_density"]

            self.section_type = 0
            self.lineEdit_outerDiameter.setText(str(outer_diameter))
            self.lineEdit_thickness.setText(str(thickness))
            if offset_y != 0:
                self.lineEdit_offset_y.setText(str(offset_y))
            if offset_z != 0:
                self.lineEdit_offset_z.setText(str(offset_z))
            if insulation_density != 0:
                self.lineEdit_insulation_density.setText(str(insulation_density))
            if insulation_thickness != 0:
                self.lineEdit_insulation_thickness.setText(str(insulation_thickness))

        elif self.section_label == 'Rectangular section':
            [base, height, base_in, height_in, offset_y, offset_z] = self.section_parameters
            self.section_type = 1
            self.lineEdit_base_rectangular_section.setText(str(base))
            self.lineEdit_height_rectangular_section.setText(str(height))
            self.lineEdit_offsety_rectangular_section.setText(str(offset_y))
            self.lineEdit_offsetz_rectangular_section.setText(str(offset_z))
            if base_in != 0 and height_in != 0:
                self.lineEdit_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 
        
        elif self.section_label == 'Circular section':
            [outer_diameter_beam, thickness, offset_y, offset_z] = self.section_parameters
            self.section_type = 2
            self.lineEdit_outer_diameter_circular_section.setText(str(outer_diameter_beam))
            self.lineEdit_offsety_circular_section.setText(str(offset_y))
            self.lineEdit_offsetz_circular_section.setText(str(offset_z))
            if thickness != 0:
                self.lineEdit_thickness_circular_section.setText(str(thickness))
        
        elif self.section_label == 'C-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 3
            self.lineEdit_height_C_section.setText(str(h))
            self.lineEdit_w1_C_section.setText(str(w1))
            self.lineEdit_tw_C_section.setText(str(tw))
            self.lineEdit_w2_C_section.setText(str(w2))
            self.lineEdit_t1_C_section.setText(str(t1))   
            self.lineEdit_t2_C_section.setText(str(t2))
            self.lineEdit_offsety_C_section.setText(str(offset_y))
            self.lineEdit_offsetz_C_section.setText(str(offset_z))             
        
        elif self.section_label == 'I-section':
            [h, w1, t1, w2, t2, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 4
            self.lineEdit_height_I_section.setText(str(h))
            self.lineEdit_w1_I_section.setText(str(w1))
            self.lineEdit_tw_I_section.setText(str(tw))
            self.lineEdit_w2_I_section.setText(str(w2))
            self.lineEdit_t1_I_section.setText(str(t1))   
            self.lineEdit_t2_I_section.setText(str(t2))
            self.lineEdit_offsety_I_section.setText(str(offset_y))
            self.lineEdit_offsetz_I_section.setText(str(offset_z))
        
        elif self.section_label == 'T-section':
            [h, w1, t1, tw, offset_y, offset_z] = self.section_parameters
            self.section_type = 5
            self.lineEdit_height_T_section.setText(str(h))
            self.lineEdit_w1_T_section.setText(str(w1))
            self.lineEdit_tw_T_section.setText(str(tw))
            self.lineEdit_t1_T_section.setText(str(t1))
            self.lineEdit_offsety_T_section.setText(str(offset_y))
            self.lineEdit_offsetz_T_section.setText(str(offset_z))  

    def update_tabs(self):
        if self.currentTab_cross_section == 0:
            if self.currentTab_pipe == 1:
                return
        beam_tabs = [   self.tab_rectangular_section, 
                        self.tab_circular_section, 
                        self.tab_C_section, 
                        self.tab_I_section, 
                        self.tab_T_section,
                        self.tab_generic_section  ]
       
        if self.section_type == 0:
            self.tabWidget_pipe_section.setCurrentWidget(self.tab_straight_pipe_section)
            return

        for i in range(6):
            if i+1 == self.section_type:
                # self.tabWidget_beam_section.setTabEnabled(i, True)
                self.tabWidget_beam_section.setCurrentWidget(beam_tabs[i])
            # else:
                # self.tabWidget_beam_section.setTabEnabled(i, False)

    def update(self):

        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()
        self.update_QDialog_info()

        if self.lines_id != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.write_ids(self.lines_id)
            self.radioButton_selected_lines.setChecked(True)
            
        elif self.elements_id != []:
            self.lineEdit_id_labels.setText("Elements IDs:")
            self.write_ids(self.elements_id)
            self.radioButton_selected_elements.setChecked(True)
            
        else:
            if self.currentTab_cross_section == 0:
                if self.currentTab_pipe == 1:
                    self.lineEdit_selected_ID.setText("")
                    return
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all_lines.setChecked(True)

    def reset_all_input_texts(self):
        for lineEdit in self.list_pipe_section_entries:
            lineEdit.setText("")
        for lineEdit in self.list_beam_section_entries:
            lineEdit.setText("")

    def flip_element_ids(self):
        self.flip = not self.flip
        temp_initial = self.lineEdit_element_id_initial.text()
        temp_final = self.lineEdit_element_id_final.text()
        self.lineEdit_element_id_initial.setText(temp_final)
        self.lineEdit_element_id_final.setText(temp_initial)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.confirm_pipe()
            if self.tabWidget_general.currentIndex() == 1:
                self.confirm_beam()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        self.lineEdit_selected_ID.setEnabled(True)
        self.lineEdit_selected_ID.setText("")

        if self.flagAll:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)

        elif self.flagEntity:
            self.lineEdit_id_labels.setText("Lines IDs:")
            if self.lines_id != []:
                self.write_ids(self.lines_id)
                    
        elif self.flagElements:
            self.lineEdit_id_labels.setText("Elements IDs:")
            if self.elements_id != []:
                self.write_ids(self.elements_id)
        
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)
        self.update_variable_section_info()
    
    def update_variable_section_info(self):
        if self.currentTab_cross_section == 0:
            if self.flagEntity:
                if len(self.lines_id) == 1:
                    line_id = self.lines_id[0]
                    self.list_elements = self.project.preprocessor.line_to_elements[line_id]
                    self.lineEdit_element_id_initial.setText(str(self.list_elements[0]))
                    self.lineEdit_element_id_final.setText(str(self.list_elements[-1]))

    def tabEvent_cross_section(self):
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()
        if self.currentTab_cross_section == 0:
            if self.currentTab_pipe == 1:
                self.tabEvent_pipe()
            for i in range(2):
                self.tabWidget_pipe_section.setTabEnabled(i, True)
        else:
            self.set_disable_radioButtons(False)
            for i in range(6):
                self.tabWidget_beam_section.setTabEnabled(i, True)

    def tabEvent_beam(self):
        self.currentTab_beam = self.tabWidget_beam_section.currentIndex()

    def tabEvent_pipe(self):
        self.currentTab_pipe = self.tabWidget_pipe_section.currentIndex()
        if self.currentTab_pipe == 0:
            self.pushButton_plot_pipe_cross_section.setDisabled(False)
            self.set_disable_radioButtons(False)
        if self.currentTab_pipe == 1:
            self.pushButton_plot_pipe_cross_section.setDisabled(True)
            self.radioButton_selected_lines.setChecked(True)
            self.radioButton_selected_elements.setDisabled(True)
            self.radioButton_all_lines.setDisabled(True)

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

        message = ""
                    
        outerDiameter = self.check_inputs(self.lineEdit_outerDiameter, "'outer diameter (Pipe section)'")
        if self.stop:
            return

        thickness = self.check_inputs(self.lineEdit_thickness, "'thickness (Pipe section)'")
        if self.stop:
            return
        
        offset_y = self.check_inputs(self.lineEdit_offset_y, "'offset y (Pipe section)'", only_positive=False, zero_included=True)
        if self.stop:
            return

        offset_z = self.check_inputs(self.lineEdit_offset_z, "'offset z (Pipe section)'", only_positive=False, zero_included=True)
        if self.stop:
            return

        insulation_density = self.check_inputs(self.lineEdit_insulation_density, "'insulation density'", zero_included=True)
        if self.stop:
            return

        insulation_thickness = self.check_inputs(self.lineEdit_insulation_thickness, "'insulation thickness'", zero_included=True)
        if self.stop:
            return
        
        if np.isclose(outerDiameter, 2*thickness, atol=1e-5) or 2*thickness > outerDiameter:
            message = "The THICKNESS must be less than \nthe outer radius."
            
        elif thickness == 0.0:
            message = "The THICKNESS must be greater than zero."

        if message != "":
            title = "INPUT CROSS-SECTION ERROR"
            PrintMessageInput([title, message, window_title]) 
            return

        # elif abs(offset_y) > 0.2*(outerDiameter/2):
        #     title = "INPUT CROSS-SECTION ERROR"
        #     message = f"The OFFSET_Y must be less or equals to 20{'%'} of the outer radius."
        #     PrintMessageInput([title, message, window_title]) 
        #     return
        
        # elif abs(offset_z) > 0.2*(outerDiameter/2):
        #     title = "INPUT CROSS-SECTION ERROR"
        #     message = message = f"The OFFSET_Z must be less or equals to 20{'%'} of the outer radius."
        #     PrintMessageInput([title, message, window_title]) 
        #     return
            
        self.section_label = "Pipe section"

        self.section_parameters = { "outer_diameter" : outerDiameter,
                                    "thickness" : thickness, 
                                    "offset_y" : offset_y, 
                                    "offset_z" : offset_z, 
                                    "insulation_thickness" : insulation_thickness, 
                                    "insulation_density" : insulation_density }
        
        self.pipe_section_info = {  "section_type_label" : self.section_label ,
                                    "section_parameters" : self.section_parameters  }

        if plot:
            return
        self.cross_section = CrossSection(pipe_section_info=self.pipe_section_info)
        self.set_cross_sections()
        self.actions_to_finalize()

    def confirm_pipe(self):

        self.index = self.comboBox_pipe.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'

        if self.flagElements:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
            if self.stop:
                return

        elif self.flagEntity:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True 

        if self.currentTab_pipe == 0:
            self.check_straight_pipe()
        elif self.currentTab_pipe == 1:
            self.check_variable_section_pipe()

    def check_beam(self):

        if self.flagElements:
            return
            #TODO: future implementation
            # lineEdit = self.lineEdit_elementID.text()
            # self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
            # if self.stop:
            #     return
        elif self.flagEntity:
            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True        
        
        elif self.flagAll:
            self.lines_typed = self.preprocessor.all_lines

        if self.currentTab_cross_section == 1:

            if self.currentTab_beam == 6:

                area = float(0)
                Iyy = float(0)
                Izz = float(0)
                Iyz = float(0)

                area = self.check_inputs(self.lineEdit_area, "'Area (Generic section)'")
                if self.stop:
                    return

                Iyy = self.check_inputs(self.lineEdit_Iyy, "'Iyy (Generic section)'")
                if self.stop:
                    return

                Izz = self.check_inputs(self.lineEdit_Izz, "'Izz (Generic section)'")
                if self.stop:
                    return

                Iyz = self.check_inputs(self.lineEdit_Iyz, "'Iyz (Generic section)'", only_positive=False, zero_included=True)
                if self.stop:
                    return

                shear_coefficient = self.check_inputs(self.lineEdit_shear_coefficient, "'Shear Factor (Generic section)'")
                if self.stop:
                    return

                if shear_coefficient > 1:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "The SHEAR FACTOR must be less or equals to 1."
                    PrintMessageInput([title, message, window_title]) 
                    return
                else:  

                    self.section_label = "Generic section"
                    self.section_parameters = None
                    _section_properties = [area, Iyy, Izz, Iyz, shear_coefficient, 0, 0]

                    self.section_properties = get_beam_section_properties(self.section_label, _section_properties)
                
            else:

                if self.check_beam_inputs_common_sections():
                    return
            
            self.beam_section_info = {  "section_type_label" : self.section_label,
                                        "section_parameters" : self.section_parameters,
                                        "section_properties" : self.section_properties  }
       
            self.cross_section = CrossSection(beam_section_info=self.beam_section_info)
            self.set_cross_sections()
            self.project.set_capped_end_by_lines(self.lines_typed, False)
            self.project.set_structural_element_wall_formulation_by_lines(self.lines_typed, None)
        self.actions_to_finalize()

    def remove_line_from_list(self, line):
        if line in list(self.project.number_sections_by_line.keys()):
            self.project.number_sections_by_line.pop(line)

    def set_cross_sections(self):

        if self.flagEntity:
            if self.remove_expansion_joint_tables_files:
                self.process_expansion_joint_table_files_removal(self.lines_typed)
            for line_id in self.lines_typed:
                self.remove_line_from_list(line_id)
            self.project.add_valve_by_line(line_id, None, reset_cross=False)
            self.project._set_expansion_joint_to_selected_lines(self.lines_typed, None)
                
            self.project.set_cross_section_by_line(self.lines_typed, self.cross_section)
            self.project.set_structural_element_type_by_lines(self.lines_typed, self.element_type)
            
            if len(self.lines_typed) < 20:
                print("[Set Cross-section] - defined at the {} lines".format(self.lines_typed))
            else:
                print("[Set Cross-section] - defined at {} selected lines".format(len(self.lines_typed)))

        elif self.flagElements:
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

    def confirm_beam(self):
        self.element_type = 'beam_1'
        self.check_beam()

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

    def check_beam_inputs_common_sections(self, plot=False):

        if self.currentTab_beam == 0: # Rectangular section

            self.section_label = "Rectangular section"

            base = self.check_inputs(self.lineEdit_base_rectangular_section, 'Base (Rectangular section)')
            if self.stop:
                return True
            
            height = self.check_inputs(self.lineEdit_height_rectangular_section, 'Height (Rectangular section)')
            if self.stop:
                return True
            
            offset_y = self.check_inputs(self.lineEdit_offsety_rectangular_section, 'Offset y (Rectangular section)', only_positive=False, zero_included=True)
            if self.stop:
                return True
            
            offset_z = self.check_inputs(self.lineEdit_offsetz_rectangular_section, 'Offset z (Rectangular section)', only_positive=False, zero_included=True)
            if self.stop:
                return True
   
            if self.lineEdit_thickness_rectangular_section.text() != "":
                
                thickness = self.check_inputs(self.lineEdit_thickness_rectangular_section, 'Thickness (Rectangular section)')
                if self.stop:
                    return True

                if thickness > np.min([(base/2), (height/2)]):
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Error in THICKNESS value input."
                    PrintMessageInput([title, message, window_title])
                    self.stop = True
                    return True             
                else:
                    base_in = base - 2*thickness
                    height_in = height - 2*thickness
            else:
                base_in = 0
                height_in = 0
            
            self.section_parameters = [base, height, base_in, height_in, offset_y, offset_z]

        elif self.currentTab_beam == 1: # Circular section

            self.section_label = "Circular section"

            outer_diameter_beam = self.check_inputs(self.lineEdit_outer_diameter_circular_section, 'Outer diameter (Circular section)')
            if self.stop:
                return True
            
            offset_y = self.check_inputs(self.lineEdit_offsety_circular_section, 'Offset y (Circular section)', only_positive=False, zero_included=True)
            if self.stop:
                return True
            
            offset_z = self.check_inputs(self.lineEdit_offsetz_circular_section, 'Offset z (Circular section)', only_positive=False, zero_included=True)
            if self.stop:
                return True

            if self.lineEdit_thickness_circular_section != "":
                thickness = self.check_inputs(self.lineEdit_thickness_circular_section, 'Thickness (Circular section)', zero_included=True)
                if self.stop:
                    return
 
            if np.isclose(outer_diameter_beam, 2*thickness, atol=1e-5) or 2*thickness > outer_diameter_beam:
                title = "INPUT CROSS-SECTION ERROR (CIRCULAR PROFILE)"
                message = "The OUTER DIAMETER must be greater than 2*THICKNESS."
                message += "Note: let THICKNESS input field blank for massive sections"
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return True

            self.section_parameters = [outer_diameter_beam, thickness, offset_y, offset_z]

        elif self.currentTab_beam == 2: # Beam: C-section

            self.section_label = "C-section"

            h = self.check_inputs(self.lineEdit_height_C_section, 'Height (C-profile)')
            if self.stop:
                return True
            
            w1 = self.check_inputs(self.lineEdit_w1_C_section, 'w1 (C-profile)')
            if self.stop:
                return True

            tw = self.check_inputs(self.lineEdit_tw_C_section, 'tw (C-profile)')
            if self.stop:
                return True
            
            w2 = self.check_inputs(self.lineEdit_w2_C_section, 'w2 (C-profile)')
            if self.stop:
                return True

            t1 = self.check_inputs(self.lineEdit_t1_C_section, 't1 (C-profile)')
            if self.stop:
                return True

            t2 = self.check_inputs(self.lineEdit_t2_C_section, 't2 (C-profile)')
            if self.stop:
                return True

            offset_y = self.check_inputs(self.lineEdit_offsety_C_section, 'Offset y (C-profile)',only_positive=False, zero_included=True)
            if self.stop:
                return True

            offset_z = self.check_inputs(self.lineEdit_offsetz_C_section, 'Offset z (C-profile)', only_positive=False, zero_included=True)            
            if self.stop:
                return True

            if h < (t1 + t2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]

        elif self.currentTab_beam == 3: # Beam: I-section

            self.section_label = "I-section"

            h = self.check_inputs(self.lineEdit_height_I_section, 'Height (I-profile)')
            if self.stop:
                return True

            w1 = self.check_inputs(self.lineEdit_w1_I_section, 'w1 (I-profile)')
            if self.stop:
                return True

            tw = self.check_inputs(self.lineEdit_tw_I_section, 'tw (I-profile)')
            if self.stop:
                return True

            w2 = self.check_inputs(self.lineEdit_w2_I_section, 'w2 (I-profile)')
            if self.stop:
                return True

            t1 = self.check_inputs(self.lineEdit_t1_I_section, 't1 (I-profile)')
            if self.stop:
                return True

            t2 = self.check_inputs(self.lineEdit_t2_I_section, 't2 (I-profile)')
            if self.stop:
                return True

            offset_y = self.check_inputs(self.lineEdit_offsety_I_section, 'Offset y (I-profile)', only_positive=False, zero_included=True)
            if self.stop:
                return True

            offset_z = self.check_inputs(self.lineEdit_offsetz_I_section, 'Offset z (I-profile)', only_positive=False, zero_included=True)
            if self.stop:
                return True

            if h < (t1 + t2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]
            
        elif self.currentTab_beam == 4: # Beam: T-section

            self.section_label = "T-section"

            h = self.check_inputs(self.lineEdit_height_T_section, 'HEIGHT (T-profile)')
            if self.stop:
                return True

            w1 = self.check_inputs(self.lineEdit_w1_T_section, 'W1 (T-profile)')
            if self.stop:
                return True

            tw = self.check_inputs(self.lineEdit_tw_T_section, 'tw (T-profile)')
            if self.stop:
                return True

            t1 = self.check_inputs(self.lineEdit_t1_T_section, 't1 (T-profile)')
            if self.stop:
                return True

            offset_y = self.check_inputs(self.lineEdit_offsety_T_section, 'OFFSET Y (T-profile)', only_positive=False, zero_included=True)
            if self.stop:
                return True

            offset_z = self.check_inputs(self.lineEdit_offsetz_T_section, 'OFFSET Y (T-profile)', only_positive=False, zero_included=True)
            if self.stop:
                return True

            if h < t1:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return True

            self.section_parameters = [h, w1, t1, tw, offset_y, offset_z]

        self.section_properties = get_beam_section_properties(self.section_label, self.section_parameters)
        
        return False
                
    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False):
        self.stop = False
        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if only_positive:
                    if zero_included:
                        if out < 0:
                            title = "INPUT CROSS-SECTION ERROR"
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
                    else:
                        if out <= 0:
                            title = "INPUT CROSS-SECTION ERROR"
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
            except Exception as _err:
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Wrong input for {label}.\n\n"
                message += str(_err)
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return None
        else:
            if zero_included:
                return float(0)
            else: 
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([title, message, window_title])                   
                self.stop = True
                return None
        return out
            
    def plot_section(self):

        plt.close()

        if self.currentTab_cross_section == 0:
            self.check_straight_pipe(plot=True) 
        
        elif self.currentTab_cross_section == 1:
            self.check_beam_inputs_common_sections(plot=True)

        if self.stop:
            self.stop = False
            return

        if self.section_label == "Pipe section":
            Yp, Zp, Yp_ins, Zp_ins, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)
        else:
            Yp, Zp, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)

        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(Yc, Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)
        third_plot = plt.scatter(0, 0, marker="+", linewidth=1.5, zorder=4, color=[0,0,1], s=120)
        
        if self.section_label == "Pipe section" and Yp_ins is not None:
            fourth, = plt.fill(Yp_ins, Zp_ins, color=[0.5,1,1], linewidth=2, zorder=5) 
            _max = np.max(np.abs(np.array([Zp_ins, Yp_ins])))*1.2
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            fourth.set_label("Insulation material")
            plt.legend(handles=[second_plot, fourth], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')
        else:
            second_plot.set_label("y: %7.5e // z: %7.5e" % (Yc, Zc))
            plt.legend(handles=[second_plot], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')

        ax.set_title('CROSS-SECTION PLOT', fontsize = 18, fontweight = 'bold')
        ax.set_xlabel('y [m]', fontsize = 16, fontweight = 'bold')
        ax.set_ylabel('z [m]', fontsize = 16, fontweight = 'bold')
        
        f = 1.25
        if self.section_type == 3:
            plt.xlim(-(1/2)*_max, (3/2)*_max)
        else:
            plt.xlim(-_max*f, _max*f)

        plt.ylim(-_max*f, _max*f)
        plt.grid()
        plt.show()