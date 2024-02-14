from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import configparser
import numpy as np
import matplotlib.pyplot as plt

from pulse.preprocessing.cross_section import get_beam_section_properties, get_points_to_plot_section
from data.user_input.model.setup.structural.get_standard_cross_section import GetStandardCrossSection
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.utils import check_inputs

window_title = "Error"
window_title2 = "Warning"

class CrossSectionInputs(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/geometry/cross_section_mainwidget.ui'), self)

        self.reset()
        self.define_qt_variables()
        self.create_connections()
        self.create_lists_of_entries()
        self.config_treeWidget()
        

    def reset(self):
        
        self.section_type = None
        self.section_label = None
        self.section_parameters = None
        self.section_properties = None
        self.beam_section_info = None

        self.complete = False
        self.flip = False
 
        self.currentTab = 0
        self.list_elements = []
        self.section_data_lines = {}
        self.section_data_elements = {}
        self.variable_parameters = []

    def define_qt_variables(self):

        # QFrame
        self.bottom_frame = self.findChild(QFrame, 'bottom_frame')
        self.top_frame = self.findChild(QFrame, 'top_frame')
        self.selection_frame = self.findChild(QFrame, 'selection_frame')
        # self.top_frame.setVisible(False)
        # self.selection_frame.setVisible(False)
        # self.adjustSize()

        self.lineEdit_element_id_initial = self.findChild(QLineEdit, 'lineEdit_element_id_initial')
        self.lineEdit_element_id_final = self.findChild(QLineEdit, 'lineEdit_element_id_final')

        self.lineEdit_outside_diameter = self.findChild(QLineEdit, 'lineEdit_outside_diameter')
        self.lineEdit_wall_thickness = self.findChild(QLineEdit, 'lineEdit_wall_thickness')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')
        self.lineEdit_insulation_density = self.findChild(QLineEdit, 'lineEdit_insulation_density')
        self.lineEdit_insulation_thickness = self.findChild(QLineEdit, 'lineEdit_insulation_thickness')

        self.lineEdit_outside_diameter_initial = self.findChild(QLineEdit, 'lineEdit_outside_diameter_initial')
        self.lineEdit_wall_thickness_initial = self.findChild(QLineEdit, 'lineEdit_wall_thickness_initial')
        self.lineEdit_offset_y_initial = self.findChild(QLineEdit, 'lineEdit_offset_y_initial')
        self.lineEdit_offset_z_initial = self.findChild(QLineEdit, 'lineEdit_offset_z_initial')

        self.lineEdit_outside_diameter_final = self.findChild(QLineEdit, 'lineEdit_outside_diameter_final')
        self.lineEdit_wall_thickness_final = self.findChild(QLineEdit, 'lineEdit_wall_thickness_final')
        self.lineEdit_offset_y_final = self.findChild(QLineEdit, 'lineEdit_offset_y_final')
        self.lineEdit_offset_z_final = self.findChild(QLineEdit, 'lineEdit_offset_z_final')

        self.lineEdit_insulation_thickness_variable_section = self.findChild(QLineEdit, 'lineEdit_insulation_thickness_variable_section')
        self.lineEdit_insulation_density_variable_section = self.findChild(QLineEdit, 'lineEdit_insulation_density_variable_section')

        self.lineEdit_base_rectangular_section = self.findChild(QLineEdit, 'lineEdit_base_rectangular_section')
        self.lineEdit_height_rectangular_section = self.findChild(QLineEdit, 'lineEdit_height_rectangular_section')
        self.lineEdit_wall_thickness_rectangular_section = self.findChild(QLineEdit, 'lineEdit_wall_thickness_rectangular_section')
        self.lineEdit_offsety_rectangular_section = self.findChild(QLineEdit, 'lineEdit_offsety_rectangular_section')
        self.lineEdit_offsetz_rectangular_section = self.findChild(QLineEdit, 'lineEdit_offsetz_rectangular_section')

        self.lineEdit_outside_diameter_circular_section = self.findChild(QLineEdit, 'lineEdit_outside_diameter_circular_section')
        self.lineEdit_wall_thickness_circular_section = self.findChild(QLineEdit, 'lineEdit_wall_thickness_circular_section')
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

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_pipe_section = self.findChild(QTabWidget, 'tabWidget_pipe_section')
        self.tabWidget_beam_section = self.findChild(QTabWidget, 'tabWidget_beam_section')
        self.tabWidget_sections_data = self.findChild(QTabWidget, 'tabWidget_sections_data')

        self.tab_pipe = self.tabWidget_general.findChild(QWidget, "tab_pipe")
        self.tab_beam = self.tabWidget_general.findChild(QWidget, "tab_beam")
        self.tab_sections =  self.tabWidget_general.findChild(QTabWidget, 'tab_sections')

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
        
        self.treeWidget_sections_parameters_by_lines = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_lines')
        self.treeWidget_sections_parameters_by_elements = self.findChild(QTreeWidget, 'treeWidget_sections_parameters_by_elements')  
            
    def create_connections(self):
                
        # self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe_section)
        # self.pushButton_confirm_beam.clicked.connect(self.confirm_beam_section)
        self.pushButton_select_standard_section.clicked.connect(self.select_standard_section)
        self.pushButton_select_standard_section_initial.clicked.connect(self.select_standard_section_initial)
        self.pushButton_select_standard_section_final.clicked.connect(self.select_standard_section_final)
        self.pushButton_check_if_section_is_normalized.clicked.connect(self.check_if_section_is_normalized)
        self.pushButton_plot_pipe_cross_section.clicked.connect(self.plot_section)
        self.pushButton_plot_beam_cross_section.clicked.connect(self.plot_section)
        # self.pushButton_load_section_info.clicked.connect(self.load_section_info)
        # self.pushButton_load_section_info.setDisabled(True)
    
        # self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        # self.tabWidget_pipe_section.currentChanged.connect(self.tabEvent_pipe)
        # self.currentTab_pipe = self.tabWidget_pipe_section.currentIndex()

        # self.tabWidget_beam_section.currentChanged.connect(self.tabEvent_beam)
        # self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_line)
        # self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_line)
        # self.treeWidget_sections_parameters_by_elements.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_element)
        # self.treeWidget_sections_parameters_by_elements.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_element)

    def create_lists_of_entries(self):
        self.list_pipe_section_entries = [  self.lineEdit_outside_diameter,
                                            self.lineEdit_wall_thickness,
                                            self.lineEdit_offset_y,
                                            self.lineEdit_offset_z,
                                            self.lineEdit_insulation_thickness,
                                            self.lineEdit_insulation_density,
                                            self.lineEdit_outside_diameter_initial,
                                            self.lineEdit_wall_thickness_initial,
                                            self.lineEdit_offset_y_initial,
                                            self.lineEdit_offset_z_initial,
                                            self.lineEdit_outside_diameter_final,
                                            self.lineEdit_wall_thickness_final,
                                            self.lineEdit_offset_y_final,
                                            self.lineEdit_offset_z_final,
                                            self.lineEdit_insulation_thickness_variable_section,
                                            self.lineEdit_insulation_density_variable_section,
                                            self.lineEdit_element_id_initial,
                                            self.lineEdit_element_id_final  ] 

        self.list_beam_section_entries = [  self.lineEdit_base_rectangular_section,
                                            self.lineEdit_height_rectangular_section,
                                            self.lineEdit_wall_thickness_rectangular_section,
                                            self.lineEdit_offsety_rectangular_section,
                                            self.lineEdit_offsetz_rectangular_section,
                                            self.lineEdit_outside_diameter_circular_section,
                                            self.lineEdit_wall_thickness_circular_section,
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

        self.list_straight_pipe_entries =   [   self.lineEdit_outside_diameter,
                                                self.lineEdit_wall_thickness,
                                                self.lineEdit_offset_y,
                                                self.lineEdit_offset_z,
                                                self.lineEdit_insulation_thickness,
                                                self.lineEdit_insulation_density    ]

        self.list_variable_pipe_entries =   [   self.lineEdit_outside_diameter_initial,
                                                self.lineEdit_wall_thickness_initial,
                                                self.lineEdit_offset_y_initial,
                                                self.lineEdit_offset_z_initial,
                                                self.lineEdit_outside_diameter_final,
                                                self.lineEdit_wall_thickness_final,
                                                self.lineEdit_offset_y_final,
                                                self.lineEdit_offset_z_final,
                                                self.lineEdit_insulation_thickness_variable_section,
                                                self.lineEdit_insulation_density_variable_section   ] 

    def reset_all_input_texts(self):
        """
        """
        for lineEdit in self.list_pipe_section_entries:
            lineEdit.setText("")
        for lineEdit in self.list_beam_section_entries:
            lineEdit.setText("")

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

    def select_standard_section(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.lineEdit_outside_diameter.setText(str(outside_diameter))
            self.lineEdit_wall_thickness.setText(str(thickness))

    def select_standard_section_initial(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.lineEdit_outside_diameter_initial.setText(str(outside_diameter))
            self.lineEdit_wall_thickness_initial.setText(str(thickness))

    def select_standard_section_final(self):
        read = GetStandardCrossSection()
        if read.complete:
            outside_diameter = round(read.outside_diameter, 6)
            thickness = round(read.wall_thickness, 6)
            self.lineEdit_outside_diameter_final.setText(str(outside_diameter))
            self.lineEdit_wall_thickness_final.setText(str(thickness))

    def set_inputs_to_geometry_creator(self, section_type=0):
        self.tabWidget_general.setTabVisible(2,False)
        # self.tabWidget_pipe_section.setCurrentTab(0)
        if section_type == 0:
            self.tabWidget_general.setTabVisible(0,True)
            self.tabWidget_general.setTabVisible(1,False)
        else:
            self.tabWidget_general.setTabVisible(0,False)
            self.tabWidget_general.setTabVisible(1,True)
        self.lineEdit_element_id_initial.setVisible(False)
        self.lineEdit_element_id_final.setVisible(False)
        self.pushButton_flip_element_ids_initial.setVisible(False)
        self.pushButton_flip_element_ids_final.setVisible(False)

    def set_geometry_creator(self, geometry_creator):
        self.geometry_creator_input = geometry_creator

    def get_straight_pipe_parameters(self):

        message = ""

        outside_diameter = check_inputs(self.lineEdit_outside_diameter, "'outside diameter (Pipe section)'")
        if outside_diameter is None:
            self.lineEdit_outside_diameter.setFocus()
            return True

        thickness = check_inputs(self.lineEdit_wall_thickness, "'thickness (Pipe section)'")
        if thickness is None:
            self.lineEdit_wall_thickness.setFocus()
            return True
        
        offset_y = check_inputs(self.lineEdit_offset_y, "'offset y (Pipe section)'", only_positive=False, zero_included=True)
        if offset_y is None:
            self.lineEdit_offset_y.setFocus()
            return True

        offset_z = check_inputs(self.lineEdit_offset_z, "'offset z (Pipe section)'", only_positive=False, zero_included=True)
        if offset_z is None:
            self.lineEdit_offset_z.setFocus()
            return True

        insulation_density = check_inputs(self.lineEdit_insulation_density, "'insulation density'", zero_included=True)
        if insulation_density is None:
            self.lineEdit_insulation_density.setFocus()
            return True

        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness, "'insulation thickness'", zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness.setFocus()
            return True
        
        if np.isclose(outside_diameter, 2*thickness, atol=1e-5) or 2*thickness > outside_diameter:
            message = "The THICKNESS must be less than \nthe outside radius."
            
        elif thickness == 0.0:
            message = "The THICKNESS must be greater than zero."

        if message != "":
            title = "INPUT CROSS-SECTION ERROR"
            PrintMessageInput([window_title, title, message]) 
            return True
           
        self.section_label = "Pipe section"

        self.section_parameters = { "outer_diameter" : outside_diameter,
                                    "thickness" : thickness, 
                                    "offset_y" : offset_y, 
                                    "offset_z" : offset_z, 
                                    "insulation_thickness" : insulation_thickness, 
                                    "insulation_density" : insulation_density }
        
        self.pipe_section_info = {  "section_type_label" : self.section_label ,
                                    "section_parameters" : self.section_parameters  }
        
    def get_variable_section_pipe_parameters(self):
        
        message = ""

        outside_diameter_initial = check_inputs(self.lineEdit_outside_diameter_initial, "'outside diameter (initial)'")
        if outside_diameter_initial is None:
            self.lineEdit_outside_diameter_initial.setFocus()
            return
        
        outside_diameter_final = check_inputs(self.lineEdit_outside_diameter_final, "'outside diameter (final)'")
        if outside_diameter_final is None:
            self.lineEdit_outside_diameter_final.setFocus()
            return

        thickness_initial = check_inputs(self.lineEdit_wall_thickness_initial, "'thickness (initial)'")
        if thickness_initial is None:
            self.lineEdit_wall_thickness_initial.setFocus()
            return
        
        thickness_final = check_inputs(self.lineEdit_wall_thickness_final, "'thickness (final)'")
        if thickness_final is None:
            self.lineEdit_wall_thickness_final.setFocus()
            return

        if np.isclose(outside_diameter_initial, 2*thickness_initial, atol=1e-5) or 2*thickness_initial > outside_diameter_initial:
            message = "The INITIAL THICKNESS must be less than \nthe initial outside radius." 

        elif thickness_initial == 0.0:
            message = "The INITIAL THICKNESS must be greater than zero." 

        if np.isclose(outside_diameter_final, 2*thickness_final, atol=1e-5) or 2*thickness_final > outside_diameter_final:
            message = "The FINAL THICKNESS must be less than \nthe final outside radius." 

        elif thickness_final == 0.0:
            message = "The FINAL THICKNESS must be greater than zero." 
        
        if message != "":
            title = "INPUT CROSS-SECTION ERROR"
            PrintMessageInput([title, message, window_title])
            return

        offset_y_initial = check_inputs(self.lineEdit_offset_y_initial, "'offset y (initial)'", only_positive=False, zero_included=True)
        if offset_y_initial is None:
            self.lineEdit_offset_y_initial.setFocus()
            return

        offset_y_final = check_inputs(self.lineEdit_offset_y_final, "'offset y (final)'", only_positive=False, zero_included=True)
        if offset_y_final is None:
            self.lineEdit_offset_y_final.setFocus()
            return

        offset_z_initial = check_inputs(self.lineEdit_offset_z_initial, "'offset z (initial)'", only_positive=False, zero_included=True)
        if offset_z_initial is None:
            self.lineEdit_offset_z_initial.setFocus()
            return
        
        offset_z_final = check_inputs(self.lineEdit_offset_z_final, "'offset z (final)'", only_positive=False, zero_included=True)
        if offset_z_final is None:
            self.lineEdit_offset_z_final.setFocus()
            return
        
        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness_variable_section, 
                                            "'insulation thickness (variable pipe section)'",
                                            zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness_variable_section.setFocus()
            return
        
        insulation_density = check_inputs(  self.lineEdit_insulation_density_variable_section, 
                                            "'density thickness (variable pipe section)'",
                                            zero_included=True  )
        if insulation_density is None:
            self.lineEdit_insulation_density_variable_section.setFocus()
            return    

        if self.flip:
            self.variable_parameters = [    outside_diameter_final, 
                                            thickness_final, 
                                            offset_y_final, 
                                            offset_z_final,
                                            outside_diameter_initial, 
                                            thickness_initial, 
                                            offset_y_initial, 
                                            offset_z_initial,
                                            insulation_thickness, 
                                            insulation_density  ]
        else:
            self.variable_parameters = [    outside_diameter_initial, 
                                            thickness_initial, 
                                            offset_y_initial, 
                                            offset_z_initial,
                                            outside_diameter_final, 
                                            thickness_final, 
                                            offset_y_final, 
                                            offset_z_final,
                                            insulation_thickness, 
                                            insulation_density  ]

    def get_beam_section_parameters(self):

        self.currentTab_beam = self.tabWidget_beam_section.currentIndex()

        if self.currentTab_beam == 0: # Rectangular section

            self.section_label = "Rectangular section"

            base = check_inputs(self.lineEdit_base_rectangular_section, 'Base (Rectangular section)')
            if base is None:
                self.lineEdit_base_rectangular_section.setFocus()
                return True
            
            height = check_inputs(self.lineEdit_height_rectangular_section, 'Height (Rectangular section)')
            if height is None:
                self.lineEdit_height_rectangular_section.setFocus()
                return True
            
            offset_y = check_inputs(self.lineEdit_offsety_rectangular_section, 'Offset y (Rectangular section)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_rectangular_section.setFocus()
                return True
            
            offset_z = check_inputs(self.lineEdit_offsetz_rectangular_section, 'Offset z (Rectangular section)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_rectangular_section.setFocus()
                return True
   
            if self.lineEdit_wall_thickness_rectangular_section.text() != "":
                
                thickness = check_inputs(self.lineEdit_wall_thickness_rectangular_section, 'Thickness (Rectangular section)')
                if thickness is None:
                    self.lineEdit_wall_thickness_rectangular_section.setFocus()
                    return True

                if thickness > np.min([(base/2), (height/2)]):
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Error in THICKNESS value input."
                    PrintMessageInput([title, message, window_title])
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

            outside_diameter_beam = check_inputs(self.lineEdit_outside_diameter_circular_section, 'Outside diameter (Circular section)')
            if outside_diameter_beam is None:
                self.lineEdit_outside_diameter_circular_section.setFocus()
                return True
            
            offset_y = check_inputs(self.lineEdit_offsety_circular_section, 'Offset y (Circular section)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_circular_section.setFocus()
                return True
            
            offset_z = check_inputs(self.lineEdit_offsetz_circular_section, 'Offset z (Circular section)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_circular_section.setFocus()
                return True

            if self.lineEdit_wall_thickness_circular_section != "":
                thickness = check_inputs(self.lineEdit_wall_thickness_circular_section, 'Thickness (Circular section)', zero_included=True)
                if thickness is None:
                    self.lineEdit_wall_thickness_circular_section.setFocus()
                    return True
 
            if np.isclose(outside_diameter_beam, 2*thickness, atol=1e-5) or 2*thickness > outside_diameter_beam:
                title = "INPUT CROSS-SECTION ERROR (CIRCULAR PROFILE)"
                message = "The outside diameter must be greater than 2*THICKNESS."
                message += "Note: let THICKNESS input field blank for massive sections"
                PrintMessageInput([title, message, window_title])
                return True

            self.section_parameters = [outside_diameter_beam, thickness, offset_y, offset_z]

        elif self.currentTab_beam == 2: # Beam: C-section

            self.section_label = "C-section"

            h = check_inputs(self.lineEdit_height_C_section, 'Height (C-profile)')
            if h is None:
                self.lineEdit_height_C_section
                return True
            
            w1 = check_inputs(self.lineEdit_w1_C_section, 'w1 (C-profile)')
            if w1 is None:
                self.lineEdit_w1_C_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_C_section, 'tw (C-profile)')
            if tw is None:
                self.lineEdit_tw_C_section.setFocus()
                return True
            
            w2 = check_inputs(self.lineEdit_w2_C_section, 'w2 (C-profile)')
            if w2 is None:
                self.lineEdit_w2_C_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_C_section, 't1 (C-profile)')
            if t1 is None:
                self.lineEdit_t1_C_section.setFocus()
                return True

            t2 = check_inputs(self.lineEdit_t2_C_section, 't2 (C-profile)')
            if t2 is None:
                self.lineEdit_t2_C_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_C_section, 'Offset y (C-profile)',only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_C_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_C_section, 'Offset z (C-profile)', only_positive=False, zero_included=True)            
            if offset_z is None:
                self.lineEdit_offsetz_C_section.setFocus()
                return True

            if h < (t1 + t2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([title, message, window_title])
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]

        elif self.currentTab_beam == 3: # Beam: I-section

            self.section_label = "I-section"

            h = check_inputs(self.lineEdit_height_I_section, 'Height (I-profile)')
            if height is None:
                self.lineEdit_height_I_section.setFocus()
                return True

            w1 = check_inputs(self.lineEdit_w1_I_section, 'w1 (I-profile)')
            if w1 is None:
                self.lineEdit_w1_I_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_I_section, 'tw (I-profile)')
            if tw is None:
                self.lineEdit_tw_I_section.setFocus()
                return True

            w2 = check_inputs(self.lineEdit_w2_I_section, 'w2 (I-profile)')
            if w2 is None:
                self.lineEdit_w2_I_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_I_section, 't1 (I-profile)')
            if t1 is None:
                self.lineEdit_t1_I_section.setFocus()
                return True

            t2 = check_inputs(self.lineEdit_t2_I_section, 't2 (I-profile)')
            if t2 is None:
                self.lineEdit_t2_I_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_I_section, 'Offset y (I-profile)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_I_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_I_section, 'Offset z (I-profile)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_I_section.setFocus()
                return True

            if h < (t1 + t2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([title, message, window_title])
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]
            
        elif self.currentTab_beam == 4: # Beam: T-section

            self.section_label = "T-section"

            h = check_inputs(self.lineEdit_height_T_section, 'HEIGHT (T-profile)')
            if h is None:
                self.lineEdit_height_T_section.setFocus()
                return True

            w1 = check_inputs(self.lineEdit_w1_T_section, 'W1 (T-profile)')
            if w1 is None:
                self.lineEdit_w1_T_section.setFocus()
                return True

            tw = check_inputs(self.lineEdit_tw_T_section, 'tw (T-profile)')
            if tw is None:
                self.lineEdit_tw_T_section.setFocus()
                return True

            t1 = check_inputs(self.lineEdit_t1_T_section, 't1 (T-profile)')
            if t1 is None:
                self.lineEdit_t1_T_section.setFocus()
                return True

            offset_y = check_inputs(self.lineEdit_offsety_T_section, 'OFFSET Y (T-profile)', only_positive=False, zero_included=True)
            if offset_y is None:
                self.lineEdit_offsety_T_section.setFocus()
                return True

            offset_z = check_inputs(self.lineEdit_offsetz_T_section, 'OFFSET Y (T-profile)', only_positive=False, zero_included=True)
            if offset_z is None:
                self.lineEdit_offsetz_T_section.setFocus()
                return True

            if h < t1:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1."
                PrintMessageInput([title, message, window_title])
                return True

            self.section_parameters = [h, w1, t1, tw, offset_y, offset_z]

        elif self.currentTab_beam == 5: # Beam: Generic

            area = float(0)
            Iyy = float(0)
            Izz = float(0)
            Iyz = float(0)

            area = check_inputs(self.lineEdit_area, "'Area (Generic section)'")
            if area is None:
                return True

            Iyy = check_inputs(self.lineEdit_Iyy, "'Iyy (Generic section)'")
            if Iyy is None:
                return True

            Izz = check_inputs(self.lineEdit_Izz, "'Izz (Generic section)'")
            if Izz is None:
                return True

            Iyz = check_inputs(self.lineEdit_Iyz, "'Iyz (Generic section)'", only_positive=False, zero_included=True)
            if Iyz is None:
                return True

            shear_coefficient = check_inputs(self.lineEdit_shear_coefficient, "'Shear Factor (Generic section)'")
            if shear_coefficient is None:
                return True

            if shear_coefficient > 1:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The SHEAR FACTOR must be less or equals to 1."
                PrintMessageInput([title, message, window_title]) 
                return True
            else:  

                self.section_label = "Generic section"
                self.section_parameters = None
                _section_properties = [area, Iyy, Izz, Iyz, shear_coefficient, 0, 0]
        
        if self.currentTab_beam == 5:
            self.section_properties = get_beam_section_properties(self.section_label, _section_properties)
            
        else:
            self.section_properties = get_beam_section_properties(self.section_label, self.section_parameters)
        self.beam_section_info = {  "section_type_label" : self.section_label,
                                    "section_parameters" : self.section_parameters,
                                    "section_properties" : self.section_properties  }
        return False

    def check_if_section_is_normalized(self):
                            
        outside_diameter = check_inputs(self.lineEdit_outside_diameter, "'outside diameter (Pipe section)'")
        if outside_diameter:
            self.lineEdit_outside_diameter.setFocus()
            return

        thickness = check_inputs(self.lineEdit_wall_thickness, "'thickness (Pipe section)'")
        if thickness:
            self.lineEdit_wall_thickness.setFocus()
            return
        
        section_data = {"outside diameter" : outside_diameter,
                        "wall thickness" : thickness}
        
        read = GetStandardCrossSection(section_data=section_data)

    def plot_section(self):

        plt.ion()

        plt.close()

        if self.tabWidget_general.currentIndex() == 0:
            if self.get_straight_pipe_parameters():
                return
        
        elif self.tabWidget_general.currentIndex() == 1:
            if self.get_beam_section_parameters():
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