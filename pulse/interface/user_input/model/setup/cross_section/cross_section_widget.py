from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.model.cross_section import get_beam_section_properties, get_points_to_plot_section
from pulse.interface.user_input.model.setup.structural.get_standard_cross_section import GetStandardCrossSection
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.utils import check_inputs

import numpy as np

window_title = "Error"
window_title2 = "Warning"

class CrossSectionWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/cross_section/cross_section_widget.ui"
        uic.loadUi(ui_path, self)

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.create_lists_of_entries()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _add_icon_and_title(self):
        self._config_window()

    def _initialize(self):
        
        self.section_type = None
        self.section_label = None
        self.section_parameters = None
        self.section_properties = None
        self.beam_section_info = None
        self.pipe_section_info = dict()

        self.complete = False
        self.flip = False
 
        self.section_data_lines = dict()
        self.section_data_elements = dict()
        self.variable_parameters = list()

    def _define_qt_variables(self):

        # QFrame
        self.bottom_frame : QFrame
        self.top_frame : QFrame
        self.selection_frame : QFrame

        # QLabel
        self.label_element_id : QLabel
        
        # QLineEdit
        self.lineEdit_element_id_initial : QLineEdit
        self.lineEdit_element_id_final : QLineEdit
        
        self.lineEdit_outside_diameter : QLineEdit
        self.lineEdit_wall_thickness : QLineEdit
        self.lineEdit_offset_y : QLineEdit
        self.lineEdit_offset_z : QLineEdit
        self.lineEdit_insulation_density : QLineEdit
        self.lineEdit_insulation_thickness : QLineEdit

        self.lineEdit_outside_diameter_initial : QLineEdit
        self.lineEdit_wall_thickness_initial : QLineEdit
        self.lineEdit_offset_y_initial : QLineEdit
        self.lineEdit_offset_z_initial : QLineEdit

        self.lineEdit_outside_diameter_final : QLineEdit
        self.lineEdit_wall_thickness_final : QLineEdit
        self.lineEdit_offset_y_final : QLineEdit
        self.lineEdit_offset_z_final : QLineEdit

        self.lineEdit_insulation_thickness_variable_section : QLineEdit
        self.lineEdit_insulation_density_variable_section : QLineEdit

        self.lineEdit_base_rectangular_section : QLineEdit
        self.lineEdit_height_rectangular_section : QLineEdit
        self.lineEdit_wall_thickness_rectangular_section : QLineEdit
        self.lineEdit_offsety_rectangular_section : QLineEdit
        self.lineEdit_offsetz_rectangular_section : QLineEdit

        self.lineEdit_outside_diameter_circular_section : QLineEdit
        self.lineEdit_wall_thickness_circular_section : QLineEdit
        self.lineEdit_offsety_circular_section : QLineEdit
        self.lineEdit_offsetz_circular_section : QLineEdit

        self.lineEdit_height_C_section : QLineEdit
        self.lineEdit_w1_C_section : QLineEdit
        self.lineEdit_t1_C_section : QLineEdit
        self.lineEdit_w2_C_section : QLineEdit
        self.lineEdit_t2_C_section : QLineEdit 
        self.lineEdit_tw_C_section : QLineEdit      
        self.lineEdit_offsety_C_section : QLineEdit
        self.lineEdit_offsetz_C_section : QLineEdit

        self.lineEdit_height_I_section : QLineEdit
        self.lineEdit_w1_I_section : QLineEdit
        self.lineEdit_t1_I_section : QLineEdit
        self.lineEdit_w2_I_section : QLineEdit
        self.lineEdit_t2_I_section : QLineEdit  
        self.lineEdit_tw_I_section : QLineEdit
        self.lineEdit_offsety_I_section : QLineEdit
        self.lineEdit_offsetz_I_section : QLineEdit

        self.lineEdit_height_T_section : QLineEdit
        self.lineEdit_w1_T_section : QLineEdit
        self.lineEdit_t1_T_section : QLineEdit
        self.lineEdit_tw_T_section : QLineEdit 
        self.lineEdit_offsety_T_section : QLineEdit
        self.lineEdit_offsetz_T_section : QLineEdit

        self.lineEdit_area : QLineEdit
        self.lineEdit_Iyy : QLineEdit
        self.lineEdit_Izz : QLineEdit
        self.lineEdit_Iyz : QLineEdit
        self.lineEdit_shear_coefficient : QLineEdit

        # QPushButton
        self.pushButton_confirm_pipe : QPushButton
        self.pushButton_confirm_beam : QPushButton
        self.pushButton_flip_element_ids_initial : QPushButton
        self.pushButton_flip_element_ids_final : QPushButton
        self.pushButton_load_section_info : QPushButton
        self.pushButton_plot_pipe_cross_section : QPushButton
        self.pushButton_plot_beam_cross_section : QPushButton
        self.pushButton_select_standard_section : QPushButton
        self.pushButton_select_standard_section_initial : QPushButton
        self.pushButton_select_standard_section_final : QPushButton
        self.pushButton_check_if_section_is_normalized : QPushButton

        # QTabWidget
        self.tabWidget_general : QTabWidget
        self.tabWidget_pipe_section : QTabWidget
        self.tabWidget_beam_section : QTabWidget
        self.tabWidget_sections_data : QTabWidget
        
        # QTreeWidget
        self.treeWidget_sections_parameters_by_lines : QTreeWidget
        self.treeWidget_sections_parameters_by_elements : QTreeWidget
            
    def _create_connections(self):
        #
        self.pushButton_select_standard_section.clicked.connect(self.select_standard_section)
        self.pushButton_select_standard_section_initial.clicked.connect(self.select_standard_section_initial)
        self.pushButton_select_standard_section_final.clicked.connect(self.select_standard_section_final)
        self.pushButton_check_if_section_is_normalized.clicked.connect(self.check_if_section_is_normalized)
        self.pushButton_plot_pipe_cross_section.clicked.connect(self.plot_section)
        self.pushButton_plot_beam_cross_section.clicked.connect(self.plot_section)
        self.config_treeWidget()

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

        self.list_constant_pipe_entries =   [   self.lineEdit_outside_diameter,
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
        for lineEdit in self.list_pipe_section_entries:
            lineEdit.setText("")
        for lineEdit in self.list_beam_section_entries:
            lineEdit.setText("")

    def config_treeWidget(self):
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,120)
        self.treeWidget_sections_parameters_by_elements.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_elements.setColumnWidth(1,120)

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

    def set_inputs_to_geometry_creator(self):
        self.tabWidget_general.setTabVisible(2,False)
        self.label_element_id.setVisible(False)
        self.lineEdit_element_id_initial.setVisible(False)
        self.lineEdit_element_id_final.setVisible(False)
        self.pushButton_flip_element_ids_initial.setVisible(False)
        self.pushButton_flip_element_ids_final.setVisible(False)
    
    def hide_all_tabs(self):
        for i in range(self.tabWidget_general.count()):
            self.tabWidget_general.setTabVisible(i, False)

        for i in range(self.tabWidget_pipe_section.count()):
            self.tabWidget_pipe_section.setTabVisible(i, False)

        for i in range(self.tabWidget_beam_section.count()):
            self.tabWidget_beam_section.setTabVisible(i, False)

    def set_geometry_creator(self, geometry_creator):
        self.geometry_creator_input = geometry_creator

    def get_constant_section_pipe_parameters(self):

        self.section_label = None
        self.section_parameters = list()
        self.pipe_section_info = dict()

        outside_diameter = check_inputs(self.lineEdit_outside_diameter, "'outside diameter (Pipe section)'")
        if outside_diameter is None:
            self.lineEdit_outside_diameter.setFocus()
            return True
        self.section_parameters.append(outside_diameter)

        thickness = check_inputs(self.lineEdit_wall_thickness, "'thickness (Pipe section)'")
        if thickness is None:
            self.lineEdit_wall_thickness.setFocus()
            return True
        self.section_parameters.append(thickness)
        
        offset_y = check_inputs(self.lineEdit_offset_y, "'offset y (Pipe section)'", only_positive=False, zero_included=True)
        if offset_y is None:
            self.lineEdit_offset_y.setFocus()
            return True
        self.section_parameters.append(offset_y)

        offset_z = check_inputs(self.lineEdit_offset_z, "'offset z (Pipe section)'", only_positive=False, zero_included=True)
        if offset_z is None:
            self.lineEdit_offset_z.setFocus()
            return True
        self.section_parameters.append(offset_z)

        insulation_density = check_inputs(self.lineEdit_insulation_density, "'insulation density'", zero_included=True)
        if insulation_density is None:
            self.lineEdit_insulation_density.setFocus()
            return True
        self.section_parameters.append(insulation_density)

        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness, "'insulation thickness'", zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness.setFocus()
            return True
        self.section_parameters.append(insulation_thickness)

        message = ""
        if np.isclose(outside_diameter, 2*thickness, atol=1e-5) or 2*thickness > outside_diameter:
            message = "The THICKNESS must be less than \nthe outside radius."
            return True
            
        if thickness == 0.0:
            message = "The THICKNESS must be greater than zero."
            return True

        if message != "":
            title = "Input cross-section error"
            PrintMessageInput([window_title, title, message]) 
            return True
        
        if len(self.section_parameters) == 6:
            
            self.section_label = "Pipe"
            self.pipe_section_info = {  "section_type_label" : self.section_label ,
                                        "section_parameters" : self.section_parameters  }

    def get_variable_section_pipe_parameters(self):

        print("entrei get_variable_section_pipe_parameters")
        
        message = ""

        outside_diameter_initial = check_inputs(self.lineEdit_outside_diameter_initial, "'outside diameter (initial)'")
        if outside_diameter_initial is None:
            self.lineEdit_outside_diameter_initial.setFocus()
            return True
        
        outside_diameter_final = check_inputs(self.lineEdit_outside_diameter_final, "'outside diameter (final)'")
        if outside_diameter_final is None:
            self.lineEdit_outside_diameter_final.setFocus()
            return True

        thickness_initial = check_inputs(self.lineEdit_wall_thickness_initial, "'thickness (initial)'")
        if thickness_initial is None:
            self.lineEdit_wall_thickness_initial.setFocus()
            return True
        
        thickness_final = check_inputs(self.lineEdit_wall_thickness_final, "'thickness (final)'")
        if thickness_final is None:
            self.lineEdit_wall_thickness_final.setFocus()
            return True

        if np.isclose(outside_diameter_initial, 2*thickness_initial, atol=1e-5) or 2*thickness_initial > outside_diameter_initial:
            message = "The INITIAL THICKNESS must be less than \nthe initial outside radius."
            return True

        if thickness_initial == 0.0:
            message = "The INITIAL THICKNESS must be greater than zero."
            return True

        if np.isclose(outside_diameter_final, 2*thickness_final, atol=1e-5) or 2*thickness_final > outside_diameter_final:
            message = "The FINAL THICKNESS must be less than \nthe final outside radius."
            return True

        if thickness_final == 0.0:
            message = "The FINAL THICKNESS must be greater than zero."
            return True
        
        if message != "":
            title = "Input cross-section error"
            PrintMessageInput([window_title, title, message])
            return True

        offset_y_initial = check_inputs(self.lineEdit_offset_y_initial, "'offset y (initial)'", only_positive=False, zero_included=True)
        if offset_y_initial is None:
            self.lineEdit_offset_y_initial.setFocus()
            return True

        offset_y_final = check_inputs(self.lineEdit_offset_y_final, "'offset y (final)'", only_positive=False, zero_included=True)
        if offset_y_final is None:
            self.lineEdit_offset_y_final.setFocus()
            return True

        offset_z_initial = check_inputs(self.lineEdit_offset_z_initial, "'offset z (initial)'", only_positive=False, zero_included=True)
        if offset_z_initial is None:
            self.lineEdit_offset_z_initial.setFocus()
            return True
        
        offset_z_final = check_inputs(self.lineEdit_offset_z_final, "'offset z (final)'", only_positive=False, zero_included=True)
        if offset_z_final is None:
            self.lineEdit_offset_z_final.setFocus()
            return True
        
        insulation_thickness = check_inputs(self.lineEdit_insulation_thickness_variable_section, 
                                            "'insulation thickness (variable pipe section)'",
                                            zero_included=True)
        if insulation_thickness is None:
            self.lineEdit_insulation_thickness_variable_section.setFocus()
            return True
        
        insulation_density = check_inputs(  self.lineEdit_insulation_density_variable_section, 
                                            "'density thickness (variable pipe section)'",
                                            zero_included=True  )
        if insulation_density is None:
            self.lineEdit_insulation_density_variable_section.setFocus()
            return True

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

        self.section_label = "Reducer"
        self.pipe_section_info = {  "section_type_label" : self.section_label ,
                                    "section_parameters" : self.variable_parameters  }

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
                    title = "Input cross-section error"
                    message = "Error in THICKNESS value input."
                    PrintMessageInput([window_title, title, message])
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
                PrintMessageInput([window_title, title, message])
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
                title = "Input cross-section error"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([window_title, title, message])
                return True

            self.section_parameters = [h, w1, t1, w2, t2, tw, offset_y, offset_z]

        elif self.currentTab_beam == 3: # Beam: I-section

            self.section_label = "I-section"

            h = check_inputs(self.lineEdit_height_I_section, 'Height (I-profile)')
            if h is None:
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
                title = "Input cross-section error"
                message = "The HEIGHT must be greater than t1+t2 summation."
                PrintMessageInput([window_title, title, message])
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
                title = "Input cross-section error"
                message = "The HEIGHT must be greater than t1."
                PrintMessageInput([window_title, title, message])
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
                title = "Input cross-section error"
                message = "The SHEAR FACTOR must be less or equals to 1."
                PrintMessageInput([window_title, title, message]) 
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
        if outside_diameter is None:
            self.lineEdit_outside_diameter.setFocus()
            return

        thickness = check_inputs(self.lineEdit_wall_thickness, "'thickness (Pipe section)'")
        if thickness is None:
            self.lineEdit_wall_thickness.setFocus()
            return
        
        section_data = {"outside diameter" : outside_diameter,
                        "wall thickness" : thickness}

        read = GetStandardCrossSection(section_data=section_data)

    def plot_section(self):
        import matplotlib.pyplot as plt

        plt.ion()

        plt.close()

        if self.tabWidget_general.currentIndex() == 0:
            if self.get_constant_section_pipe_parameters():
                return
        
        elif self.tabWidget_general.currentIndex() == 1:
            if self.get_beam_section_parameters():
                return

        if self.section_label in ["Pipe", "Reducer"]:
            Yp, Zp, Yp_ins, Zp_ins, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)
        else:
            Yp, Zp, Yc, Zc = get_points_to_plot_section(self.section_label, self.section_parameters)

        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(Yc, Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)
        third_plot = plt.scatter(0, 0, marker="+", linewidth=1.5, zorder=4, color=[0,0,1], s=120)
        
        if self.section_label in ["Pipe", "Reducer"] and Yp_ins is not None:
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