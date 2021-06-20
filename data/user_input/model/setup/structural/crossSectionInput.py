from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection
from data.user_input.project.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt

window_title = "ERROR MESSAGE"

class CrossSectionInput(QDialog):
    def __init__(   self, 
                    project, 
                    opv, 
                    external_diameter = 0, 
                    thickness = 0, 
                    offset_y = 0, 
                    offset_z = 0,
                    pipe_to_beam = False,
                    beam_to_pipe = False,
                    lines_to_update_cross_section = [], 
                    *args, 
                    **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/crossSectionInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.structural_elements = self.project.mesh.structural_elements
        self.dict_tag_to_entity = self.project.mesh.dict_tag_to_entity#get_dict_of_entities()
        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()

        self.external_diameter = external_diameter
        self.thickness = thickness
        self.offset_y = offset_y
        self.offset_z = offset_z

        self.pipe_to_beam = pipe_to_beam
        self.beam_to_pipe = beam_to_pipe
        self.lines_to_update_cross_section = lines_to_update_cross_section

        self.section_key = None
        self.parameters = None
        self.section_info = None
        self.section_data = None
        self.complete = False
        self.flagAll = False
        self.flagEntity = False
        self.currentTab = 0

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')
        self.lineEdit_selected_ID.setEnabled(True)

        self.lineEdit_outerDiameter = self.findChild(QLineEdit, 'lineEdit_outerDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')
        self.lineEdit_InsulationDensity = self.findChild(QLineEdit, 'lineEdit_InsulationDensity')
        self.lineEdit_InsulationThickness = self.findChild(QLineEdit, 'lineEdit_InsulationThickness')    

        self.lineEdit_area = self.findChild(QLineEdit, 'lineEdit_area')
        self.lineEdit_Iyy = self.findChild(QLineEdit, 'lineEdit_Iyy')
        self.lineEdit_Izz = self.findChild(QLineEdit, 'lineEdit_Izz')
        self.lineEdit_Iyz = self.findChild(QLineEdit, 'lineEdit_Iyz')
        self.lineEdit_shear_coefficient = self.findChild(QLineEdit, 'lineEdit_shear_coefficient')
        self.lineEdit_base = self.findChild(QLineEdit, 'lineEdit_base')
        self.lineEdit_height = self.findChild(QLineEdit, 'lineEdit_height')
        self.lineEdit_outer_diameter_beam = self.findChild(QLineEdit, 'lineEdit_outer_diameter_beam')
        self.lineEdit_inner_diameter_beam = self.findChild(QLineEdit, 'lineEdit_inner_diameter_beam')

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.radioButton_rectangular_section = self.findChild(QRadioButton, 'radioButton_rectangular_section')
        self.radioButton_circular_section = self.findChild(QRadioButton, 'radioButton_circular_section')
        self.radioButton_C_section = self.findChild(QRadioButton, 'radioButton_C_section')
        self.radioButton_I_section = self.findChild(QRadioButton, 'radioButton_I_section')
        self.radioButton_T_section = self.findChild(QRadioButton, 'radioButton_T_section')
        self.radioButton_rectangular_section.toggled.connect(self.radioButtonEvent_beam_section_type)
        self.radioButton_circular_section.toggled.connect(self.radioButtonEvent_beam_section_type)
        self.radioButton_C_section.toggled.connect(self.radioButtonEvent_beam_section_type)
        self.radioButton_I_section.toggled.connect(self.radioButtonEvent_beam_section_type)
        self.radioButton_T_section.toggled.connect(self.radioButtonEvent_beam_section_type)

        self.rectangular_flag = self.radioButton_rectangular_section.isChecked()
        self.circular_flag = self.radioButton_circular_section.isChecked()
        self.C_section_flag = self.radioButton_C_section.isChecked()
        self.I_section_flag = self.radioButton_I_section.isChecked()
        self.T_section_flag = self.radioButton_T_section.isChecked()
        self.beam_section_type()

        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_general.currentChanged.connect(self.tabEvent_cross_section)
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()

        self.tabWidget_section_beam_info1 = self.findChild(QTabWidget, 'tabWidget_section_beam_info1')
        self.tabWidget_section_beam_info1.currentChanged.connect(self.tabEvent_beam)
        self.currentTab_beam = self.tabWidget_section_beam_info1.currentIndex()
        
        self.tab_pipe = self.tabWidget_general.findChild(QWidget, "tab_pipe")
        self.tab_beam = self.tabWidget_general.findChild(QWidget, "tab_beam")
        
        self.pushButton_confirm_pipe = self.findChild(QPushButton, 'pushButton_confirm_pipe')
        self.pushButton_confirm_pipe.clicked.connect(self.confirm_pipe)

        self.pushButton_confirm_pipe_2 = self.findChild(QPushButton, 'pushButton_confirm_pipe_2')
        self.pushButton_confirm_pipe_2.clicked.connect(self.confirm_pipe)

        self.pushButton_confirm_generic_section_beam = self.findChild(QPushButton, 'pushButton_confirm_generic_section_beam')
        self.pushButton_confirm_generic_section_beam.clicked.connect(self.confirm_beam)

        self.pushButton_enter_section_parameters = self.findChild(QPushButton, 'pushButton_enter_section_parameters')
        self.pushButton_enter_section_parameters.clicked.connect(self.confirm_beam)

        self.comboBox_pipe = self.findChild(QComboBox, 'comboBox_pipe')
        # self.comboBox_pipe.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox_pipe.currentIndex()

        self.comboBox_beam = self.findChild(QComboBox, 'comboBox_beam')
        # self.comboBox_beam.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox_beam.currentIndex()
        
        # if self.external_diameter!=0 and self.thickness!=0:
        #     self.lineEdit_outerDiameter.setText(str(self.external_diameter))
        #     self.lineEdit_thickness.setText(str(self.thickness))
        #     self.lineEdit_offset_y.setText(str(self.offset_y))
        #     self.lineEdit_offset_z.setText(str(self.offset_z))
               
        if self.pipe_to_beam:
            self.tabWidget_general.setCurrentWidget(self.tab_beam)
            self.tabWidget_general.setTabEnabled(0, False)

        if self.beam_to_pipe:
            self.tabWidget_general.setCurrentWidget(self.tab_pipe)
            self.tabWidget_general.setTabEnabled(1, False)
        
        if self.lines_id != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_id)
            
        elif self.elements_id != []:
            self.lineEdit_id_labels.setText("Elements IDs:")
            self.radioButton_selected_elements.setChecked(True)
            self.write_ids(self.elements_id)
                    
        elif self.lines_to_update_cross_section != []:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_selected_lines.setChecked(True)
            self.write_ids(self.lines_to_update_cross_section)
            
        else:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.radioButton_all_lines.setChecked(True)  
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)

        self.update_QDialog_info()       
        self.exec_()

    def update_QDialog_info(self):
        if len(self.lines_id) > 0:   
            line = self.lines_id[0]
            # for line in self.lines_id:
            entity = self.dict_tag_to_entity[line]
            if entity.cross_section is not None:
                cross = entity.cross_section
                self.section_data = None

                if entity.structural_element_type in ['pipe_1', 'pipe_2']:
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                    self.radioButton_rectangular_section.setChecked(False)
                    self.external_diameter = cross.external_diameter
                    self.thickness = cross.thickness
                    self.lineEdit_outerDiameter.setText(str(self.external_diameter))
                    self.lineEdit_thickness.setText(str(self.thickness))
                    
                    if cross.offset_y != 0:
                        self.lineEdit_outerDiameter.setText(str(self.offset_y))
                    if cross.offset_z != 0:
                        self.lineEdit_outerDiameter.setText(str(self.offset_z))
                
                elif entity.structural_element_type in ['beam_1']:
                    self.reset_pipe_input_texts()
                    self.section_data = cross.additional_section_info
                    section_type = self.section_data[0]
                    self.tabWidget_general.setCurrentWidget(self.tab_beam)
                    
                    if section_type == 'Rectangular section':
                        self.radioButton_rectangular_section.setChecked(True)
                    if section_type == 'Circular section':
                        self.radioButton_circular_section.setChecked(True)
                    if section_type == 'C-section':
                        self.radioButton_C_section.setChecked(True)                        
                    if section_type == 'I-section':
                        self.radioButton_I_section.setChecked(True)
                    if section_type == 'T-section':
                        self.radioButton_T_section.setChecked(True)
            else:
                if entity.structural_element_type in ['pipe_1', 'pipe_2']:
                    self.tabWidget_general.setCurrentWidget(self.tab_pipe)
                elif entity.structural_element_type in ['beam_1']:
                    self.tabWidget_general.setCurrentWidget(self.tab_beam)

    def reset_pipe_input_texts(self):
        self.lineEdit_outerDiameter.setText('')
        self.lineEdit_thickness.setText('')
        self.lineEdit_outerDiameter.setText('')
        self.lineEdit_outerDiameter.setText('')

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

    def radioButtonEvent_beam_section_type(self):
        self.rectangular_flag = self.radioButton_rectangular_section.isChecked()
        self.circular_flag = self.radioButton_circular_section.isChecked()
        self.C_section_flag = self.radioButton_C_section.isChecked()
        self.I_section_flag = self.radioButton_I_section.isChecked()
        self.T_section_flag = self.radioButton_T_section.isChecked()
        self.beam_section_type()

    def beam_section_type(self):
        if self.rectangular_flag:
            self.section_key = 0
        elif self.circular_flag:
            self.section_key = 1
        elif self.C_section_flag:
            self.section_key = 2
        elif self.I_section_flag:
            self.section_key = 3
        elif self.T_section_flag:
            self.section_key = 4
        
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def tabEvent_cross_section(self):
        self.currentTab_cross_section = self.tabWidget_general.currentIndex()

    def tabEvent_beam(self):
        self.currentTab_beam = self.tabWidget_section_beam_info1.currentIndex()

    def check_input_elements(self):
        try:
            tokens = self.lineEdit_selected_ID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.elements_typed = list(map(int, tokens))
            
            if self.lineEdit_selected_ID.text()=="":
                title = "Error: empty Element ID input"
                message = "Inform a valid Element ID before \nto confirm the input."
                self.info_text = [title, message, window_title]     
                return True
        except Exception:
            title = "Error: invalid Element ID input"
            message = "Wrong input for Node ID's."
            self.info_text = [title, message, window_title]   
            return True

        try:
            for element in self.elements_typed:
                self.elementID = self.structural_elements[element].index
        except Exception:
            title = "Error: invalid Element ID input"
            message = " The Element ID input values must be \nmajor than 1 and less than {}.".format(len(self.structural_elements))
            self.info_text = [title, message, window_title]
            return True
        return False

    def check_input_lines(self):
        
        try:
            tokens = self.lineEdit_selected_ID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.lines_typed = list(map(int, tokens))
            
            if self.lineEdit_selected_ID.text()=="":
                title = "Error: empty Line ID input"
                message = "Inform a valid Line ID before \nto confirm the input.."
                self.info_text = [title, message, window_title]
                return True
        except Exception:
            title = "Error: invalid Line ID input"
            message = "Wrong input for Line ID."
            self.info_text = [title, message, window_title]
            return True
        try:
            for line in self.lines_typed:
                self.line = self.dict_tag_to_entity[line]
        except Exception:
            title = "Error: invalid Line ID"
            message = "The Line ID input values must be \nmajor than 1 and less than {}.".format(len(self.dict_tag_to_entity))
            self.info_text = [title, message, window_title]
            return True
        return False

    def check_pipe(self):
        
        if self.flagElements:
            if self.check_input_elements():
                PrintMessageInput(self.info_text) 
                return

        elif self.flagEntity:
            if self.check_input_lines():
                PrintMessageInput(self.info_text) 
                return

        if self.currentTab_cross_section == 0:
            if self.lineEdit_outerDiameter.text() == "":
                title = "INPUT CROSS-SECTION ERROR"
                message = "Insert some value (OUTER DIAMETER)."
                PrintMessageInput([title, message, window_title]) 
                return
            elif self.lineEdit_thickness.text() == "":
                title = "INPUT CROSS-SECTION ERROR"
                message = "Insert some value (THICKENSS)."
                PrintMessageInput([title, message, window_title]) 
                return

            offset_y = float(0)
            offset_z = float(0)
            insulation_density = float(0)
            insulation_thickness = float(0)

            try:
                outerDiameter = float(self.lineEdit_outerDiameter.text())
            except Exception:
                title = "INPUT CROSS-SECTION ERROR"
                message = "Wrong input to the OUTER DIAMETER."
                PrintMessageInput([title, message, window_title]) 
                return
            try:
                thickness = float(self.lineEdit_thickness.text())
            except Exception:
                title = "INPUT CROSS-SECTION ERROR"
                message = "Wrong input to the THICKENSS."
                PrintMessageInput([title, message, window_title]) 
                return

            if self.lineEdit_offset_y.text() != "":
                try:
                    offset_y = float(self.lineEdit_offset_y.text())
                except Exception:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Wrong input to the OFFSET Y."
                    PrintMessageInput([title, message, window_title]) 
                    return

            if self.lineEdit_offset_z.text() != "":
                try:
                    offset_z = float(self.lineEdit_offset_z.text())
                except Exception:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Wrong input to the OFFSET Z."
                    PrintMessageInput([title, message, window_title]) 
                    return
           
            if self.lineEdit_InsulationDensity.text() != "":
                try:
                    insulation_density = float(self.lineEdit_InsulationDensity.text())
                except Exception:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Wrong input to the INSULATION DENSITY."
                    PrintMessageInput([title, message, window_title]) 
                    return
           
            if self.lineEdit_InsulationThickness.text() != "":
                try:
                    insulation_thickness = float(self.lineEdit_InsulationThickness.text())
                except Exception:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Wrong input to the INSULATION THICKNESS."
                    PrintMessageInput([title, message, window_title]) 
                    return
           
            if thickness > (outerDiameter/2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The THICKNESS must be less or \nequals to the OUTER RADIUS."
                PrintMessageInput([title, message, window_title]) 
                return

            elif thickness == 0.0:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The THICKNESS must be greater than zero."
                PrintMessageInput([title, message, window_title]) 
                return
            
            elif abs(offset_y) > 0.2*(outerDiameter/2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The OFFSET_Y must be less than 20{%} \nof the external radius."
                PrintMessageInput([title, message, window_title]) 
                return
            
            elif abs(offset_z) > 0.2*(outerDiameter/2):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The OFFSET_Z must be less than 20{%} \nof the external radius."
                PrintMessageInput([title, message, window_title]) 
                return
            
            section_info = ["Pipe section", [outerDiameter, thickness, offset_y, offset_z, insulation_thickness]]

            self.cross_section = CrossSection(  outerDiameter, thickness, offset_y, offset_z, 
                                                insulation_density=insulation_density, 
                                                insulation_thickness=insulation_thickness, 
                                                additional_section_info=section_info  )

        self.complete = True
        self.close()

    def confirm_pipe(self):

        self.index = self.comboBox_pipe.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'
        self.check_pipe()

    def check_beam(self):

        if self.flagElements:
            if self.check_input_elements():
                return
        elif self.flagEntity:
            if self.check_input_lines():
                PrintMessageInput(self.info_text) 
                return            
        
        if self.currentTab_cross_section == 1:

            if self.currentTab_beam == 0:

                read = CrossSectionBeamInput(self.section_key, section_data=self.section_data)
                if not read.complete:
                    return
                self.cross_section = read.cross_section

            elif self.currentTab_beam == 1:

                area = float(0)
                Iyy = float(0)
                Izz = float(0)
                Iyz = float(0)

                area = self.check_beam_inputs(self.lineEdit_area, 'AREA')
                Iyy = self.check_beam_inputs(self.lineEdit_Iyy, 'Iyy')
                Izz = self.check_beam_inputs(self.lineEdit_Izz, 'Izz')
                Iyz = self.check_beam_inputs(self.lineEdit_Iyz, 'Iyz', only_positive_values=False)
                shear_coefficient = self.check_beam_inputs(self.lineEdit_shear_coefficient, 'Shear Factor')

                if None in [area, Iyy, Izz, Iyz, shear_coefficient]:
                    return
                elif shear_coefficient > 1:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "The SHEAR FACTOR must be less or equals to 1."
                    PrintMessageInput([title, message, window_title]) 
                    return
                
                self.external_diameter = 2*np.abs(np.sqrt(area/np.pi))
                self.thickness = 0
                section_info = ["Generic section", None]
                self.cross_section = CrossSection(  self.external_diameter, self.thickness, 0, 0, 
                                                    area=area, 
                                                    Iyy=Iyy, 
                                                    Izz=Izz, 
                                                    Iyz=Iyz, 
                                                    additional_section_info=section_info, 
                                                    shear_coefficient=shear_coefficient)

        self.complete = True
        self.close()

    def check_beam_inputs(self, lineEdit, label, only_positive_values=True):

        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if out <= 0 and only_positive_values:
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Insert a positive value to the {}.".format(label)
                    PrintMessageInput([title, message, window_title]) 
                    return None
            except Exception:
                title = "INPUT CROSS-SECTION ERROR"
                message = "Wrong input to the {}.".format(label)
                PrintMessageInput([title, message, window_title]) 
                return None
        else:
            title = "INPUT CROSS-SECTION ERROR"
            message = "Insert some value to the {}.".format(label)
            PrintMessageInput([title, message, window_title]) 
            return None
        return out

    def confirm_beam(self):

        self.index = self.comboBox_beam.currentIndex()
        if self.index == 0:
            self.element_type = 'beam_1'
        self.check_beam()

    def update(self):

        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()
        # print('passei update')
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
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all_lines.setChecked(True)


class CrossSectionBeamInput(QDialog):
    def __init__(self, section_type, section_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/crossSectionBeamInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        # self.parameters = parameters
        self.section_type = section_type
        self.section_data = section_data
        self.complete = False
        self.stop = False
        # self._get_dict_key_section()
        
        self.lineEdit_base_rectangular_section = self.findChild(QLineEdit, 'lineEdit_base_rectangular_section')
        self.lineEdit_height_rectangular_section = self.findChild(QLineEdit, 'lineEdit_height_rectangular_section')
        self.lineEdit_thickness_rectangular_section = self.findChild(QLineEdit, 'lineEdit_thickness_rectangular_section')

        self.lineEdit_outer_diameter_circular_section = self.findChild(QLineEdit, 'lineEdit_outer_diameter_circular_section')
        self.lineEdit_inner_diameter_circular_section = self.findChild(QLineEdit, 'lineEdit_inner_diameter_circular_section')

        self.lineEdit_height_C_section = self.findChild(QLineEdit, 'lineEdit_height_C_section')
        self.lineEdit_radius_C_section = self.findChild(QLineEdit, 'lineEdit_radius_C_section')
        self.lineEdit_w1_C_section = self.findChild(QLineEdit, 'lineEdit_w1_C_section')
        self.lineEdit_w2_C_section = self.findChild(QLineEdit, 'lineEdit_w2_C_section')
        self.lineEdit_w3_C_section = self.findChild(QLineEdit, 'lineEdit_w3_C_section')
        self.lineEdit_t1_C_section = self.findChild(QLineEdit, 'lineEdit_t1_C_section')    
        self.lineEdit_t3_C_section = self.findChild(QLineEdit, 'lineEdit_t3_C_section')         

        self.lineEdit_height_I_section = self.findChild(QLineEdit, 'lineEdit_height_I_section')
        self.lineEdit_radius_I_section = self.findChild(QLineEdit, 'lineEdit_radius_I_section')
        self.lineEdit_w1_I_section = self.findChild(QLineEdit, 'lineEdit_w1_I_section')
        self.lineEdit_w2_I_section = self.findChild(QLineEdit, 'lineEdit_w2_I_section')
        self.lineEdit_w3_I_section = self.findChild(QLineEdit, 'lineEdit_w3_I_section')
        self.lineEdit_t1_I_section = self.findChild(QLineEdit, 'lineEdit_t1_I_section')    
        self.lineEdit_t3_I_section = self.findChild(QLineEdit, 'lineEdit_t3_I_section') 

        self.lineEdit_height_T_section = self.findChild(QLineEdit, 'lineEdit_height_T_section')
        self.lineEdit_radius_T_section = self.findChild(QLineEdit, 'lineEdit_radius_T_section')
        self.lineEdit_w1_T_section = self.findChild(QLineEdit, 'lineEdit_w1_T_section')
        self.lineEdit_w2_T_section = self.findChild(QLineEdit, 'lineEdit_w2_T_section')
        self.lineEdit_t1_T_section = self.findChild(QLineEdit, 'lineEdit_t1_T_section')  

        self.tabWidget_section_beam_info = self.findChild(QTabWidget, 'tabWidget_section_beam_info')
        self.tabWidget_section_beam_info.currentChanged.connect(self.tabEvent_beam_type)
        self.currentTab_beam_type = self.tabWidget_section_beam_info.currentIndex()

        self.pushButton_confirm_beam = self.findChild(QPushButton, 'pushButton_confirm_beam')  
        self.pushButton_confirm_beam.clicked.connect(self.confirm_beam)

        self.pushButton_plot_cross_section = self.findChild(QPushButton, 'pushButton_plot_cross_section')  
        self.pushButton_plot_cross_section.clicked.connect(self.plot_section)

        self.tab_rectangular_section = self.tabWidget_section_beam_info.findChild(QWidget, "tab_rectangular_section")
        self.tab_circular_section = self.tabWidget_section_beam_info.findChild(QWidget, "tab_circular_section")
        self.tab_C_section = self.tabWidget_section_beam_info.findChild(QWidget, "tab_C_section")
        self.tab_I_section = self.tabWidget_section_beam_info.findChild(QWidget, "tab_I_section")
        self.tab_T_section = self.tabWidget_section_beam_info.findChild(QWidget, "tab_T_section")

        if self.section_data is not None:
            section_type, section_entries = self.section_data
            if section_type == 'Rectangular section':
                # print('Rectangular section')
                [base, height, base_in, height_in, _, _] = section_entries
                self.lineEdit_base_rectangular_section.setText(str(base))
                self.lineEdit_height_rectangular_section.setText(str(height))
                if base_in != 0 and height_in != 0:
                    self.lineEdit_thickness_rectangular_section.setText(str(round((base-base_in)/2,4))) 
            elif section_type == 'Circular section':
                # print('Circular section')
                [outer_diameter_beam, inner_diameter_beam, _, _] = section_entries
                self.lineEdit_outer_diameter_circular_section.setText(str(outer_diameter_beam))
                if inner_diameter_beam != 0:
                    self.lineEdit_inner_diameter_circular_section.setText(str(inner_diameter_beam))
            elif section_type == 'C-section':
                # print('C-section')
                [h, w1, w2, w3, t1, t2, t3, r, _ ,_ ] = section_entries
                self.lineEdit_height_C_section.setText(str(h))
                self.lineEdit_w1_C_section.setText(str(w1))
                self.lineEdit_w2_C_section.setText(str(w2))
                self.lineEdit_w3_C_section.setText(str(w3))
                self.lineEdit_t1_C_section.setText(str(t1))   
                self.lineEdit_t3_C_section.setText(str(t3))
                if r != 0:
                    self.lineEdit_radius_C_section.setText(str(r))                
            elif section_type == 'I-section':
                # print('I-section')
                [h, w1, w2, w3, t1, _, t3, r, _, _] = section_entries
                self.lineEdit_height_I_section.setText(str(h))
                self.lineEdit_w1_I_section.setText(str(w1))
                self.lineEdit_w2_I_section.setText(str(w2))
                self.lineEdit_w3_I_section.setText(str(w3))
                self.lineEdit_t1_I_section.setText(str(t1))   
                self.lineEdit_t3_I_section.setText(str(t3))
                if r != 0:
                    self.lineEdit_radius_I_section.setText(str(r))
            elif section_type == 'T-section':
                # print('T-section')
                [h, w1, w2, t1, t2, r, _ ,_ ] = section_entries
                self.lineEdit_height_T_section.setText(str(h))
                self.lineEdit_w1_T_section.setText(str(w1))
                self.lineEdit_w2_T_section.setText(str(w2))
                self.lineEdit_t1_T_section.setText(str(t1))   
                if r != 0:
                    self.lineEdit_radius_I_section.setText(str(r))
            else:
                pass

        self.update_tabs()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_beam()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def update_tabs(self):

        tabs = [self.tab_rectangular_section, self.tab_circular_section, self.tab_C_section, self.tab_I_section, self.tab_T_section]

        for i in range(5):
            if i == self.section_type:
                self.tabWidget_section_beam_info.setTabEnabled(i, True)
                self.tabWidget_section_beam_info.setCurrentWidget(tabs[i])
            else:
                self.tabWidget_section_beam_info.setTabEnabled(i, False)

    def tabEvent_beam_type(self):
        self.currentTab_beam_type = self.tabWidget_section_beam_info.currentIndex()

    def confirm_beam(self):
        self.element_type = 'beam_1'
        self.check_beam()

    def check_beam(self, plot=False):

        if self.currentTab_beam_type == 0: # Rectangular section

            self.section_label = "Rectangular section"

            base = self.check_beam_inputs(self.lineEdit_base_rectangular_section, 'BASE')
            height = self.check_beam_inputs(self.lineEdit_height_rectangular_section, 'HEIGHT')
            
            if None in [base, height]:
                self.stop = True
                return

            if self.lineEdit_thickness_rectangular_section.text() != "":
                thickness = self.check_beam_inputs(self.lineEdit_thickness_rectangular_section, 'THICKNESS')
                if thickness is None:
                    self.stop = True
                    return
                if thickness > np.min([(base/2), (height/2)]):
                    title = "INPUT CROSS-SECTION ERROR"
                    message = "Error in THICKNESS value input."
                    PrintMessageInput([title, message, window_title])
                    self.stop = True
                    return             
                else:
                    base_in = base - 2*thickness
                    height_in = height - 2*thickness
            else:
                base_in = 0
                height_in = 0
    
            area = base*height - base_in*height_in
            Iyy = ((height**3)*base/12) - ((height_in**3)*base_in/12)
            Izz = ((base**3)*height/12) - (base_in**3)*height_in/12

            Iyz = 0.
            Yc, Zc = 0, 0
            
            self.parameters = [base, height, base_in, height_in, Yc, Zc]
            self.external_diameter = 2*np.abs(np.sqrt(area/np.pi))

        elif self.currentTab_beam_type == 1: # Circular section

            self.section_label = "Circular section"

            outer_diameter_beam = self.check_beam_inputs(self.lineEdit_outer_diameter_circular_section, 'OUTER DIAMETER')
            if self.lineEdit_inner_diameter_circular_section != "":
                inner_diameter_beam = self.check_beam_inputs(self.lineEdit_inner_diameter_circular_section, 'INNER DIAMETER', check_radius=True)
            else:
                inner_diameter_beam = float(0)

            if outer_diameter_beam <= inner_diameter_beam:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The OUTER DIAMETER must be greater than INNER DIAMETER."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return
            
            area = np.pi*((outer_diameter_beam**2)-(inner_diameter_beam**2))/4
            Iyy = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
            Izz = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
            Iyz = 0
            Yc, Zc = 0, 0

            self.parameters = [outer_diameter_beam, inner_diameter_beam, Yc, Zc]
            self.external_diameter = outer_diameter_beam

        elif self.currentTab_beam_type == 2: # Beam: C-section

            self.section_label = "C-section"

            height = self.check_beam_inputs(self.lineEdit_height_C_section, 'HEIGHT')
            w1 = self.check_beam_inputs(self.lineEdit_w1_C_section, 'W1')
            w2 = self.check_beam_inputs(self.lineEdit_w2_C_section, 'W2')
            w3 = self.check_beam_inputs(self.lineEdit_w3_C_section, 'W3')
            t1 = self.check_beam_inputs(self.lineEdit_t1_C_section, 't1')
            t3 = self.check_beam_inputs(self.lineEdit_t3_C_section, 't3')
            radius_C = self.check_beam_inputs(self.lineEdit_radius_C_section, 'RADIUS (C PROFILE)', check_radius=True)

            if None in [height, w1, w2, w3, t1, t3]:
                self.stop = True
                return

            if height < (t1 + t3):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t3 summation."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return

            h = height
            t2 = h - t1 - t3

            if self.lineEdit_radius_C_section.text() != "":
                if radius_C is None:
                    self.stop = True
                    return
                else:
                    r = radius_C
            else:
                r = float(0)

            self.parameters = [h, w1, w2, w3, t1, t2, t3, r]

            A_i = np.array([w1*t1, w2*t2, w3*t3, ((4-np.pi)/4)*r**2, ((4-np.pi)/4)*r**2])
            A_t = np.sum(A_i)

            y_ci = np.array([w1/2, w2/2, w3/2, (w2 + ((10-3*np.pi)/(3*(4-np.pi)))*r), (w2 + ((10-3*np.pi)/(3*(4-np.pi)))*r)])
            z_ci = np.array([((t1+t2)/2), 0, -((t2+t3)/2), ((h/2) - t1 - ((10-3*np.pi)/(3*(4-np.pi)))*r), -((h/2) - t3 - ((10-3*np.pi)/(3*(4-np.pi)))*r)])
            
            I_yi = np.array([(w1*t1**3)/12, (w2*t2**3)/12, (w3*t3**3)/12, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4])
            I_zi = np.array([(t1*w1**3)/12, (t2*w2**3)/12, (t3*w3**3)/12, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4])
            I_yzi = np.array([0, 0, 0, ((28-9*np.pi)/(72*(4-np.pi)))*r**4, -((28-9*np.pi)/(72*(4-np.pi)))*r**4])

        elif self.currentTab_beam_type == 3: # Beam: I-section

            self.section_label = "I-section"

            height = self.check_beam_inputs(self.lineEdit_height_I_section, 'HEIGHT')
            w1 = self.check_beam_inputs(self.lineEdit_w1_I_section, 'W1')
            w2 = self.check_beam_inputs(self.lineEdit_w2_I_section, 'W2')
            w3 = self.check_beam_inputs(self.lineEdit_w3_I_section, 'W3')
            t1 = self.check_beam_inputs(self.lineEdit_t1_I_section, 't1')
            t3 = self.check_beam_inputs(self.lineEdit_t3_I_section, 't3')
            radius_I = self.check_beam_inputs(self.lineEdit_radius_I_section, 'RADIUS (I PROFILE)', check_radius=True)

            if None in [height, w1, w2, w3, t1, t3]:
                self.stop = True
                return

            if height < (t1 + t3):
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1+t3 summation."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return

            h = height
            t2 = h - t1 - t3

            if self.lineEdit_radius_I_section.text() != "":
                if radius_I is None:
                    self.stop = True
                    return
                else:
                    r = radius_I
            else:
                r = float(0)
        
            self.parameters = [h, w1, w2, w3, t1, t2, t3, r]

            A_i = np.array([w1*t1, w2*t2, w3*t3, ((4-np.pi)/4)*r**2, ((4-np.pi)/4)*r**2, ((4-np.pi)/4)*r**2, ((4-np.pi)/4)*r**2])
            A_t = np.sum(A_i)

            y_c47 = ((w2/2) + ((10-3*np.pi)/(3*(4-np.pi)))*r)
            y_c56 = -((w2/2) + ((10-3*np.pi)/(3*(4-np.pi)))*r) 
            z_c45 = ((h/2) - t1 - ((10-3*np.pi)/(3*(4-np.pi)))*r)
            z_c67 = -((h/2) - t3 - ((10-3*np.pi)/(3*(4-np.pi)))*r)   

            y_ci = np.array([0, 0, 0, y_c47, y_c56, y_c56, y_c47])
            z_ci = np.array([((t1+t2)/2), 0, -((t2+t3)/2), z_c45, z_c45, z_c67, z_c67])

            I_y4567 = (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4
            I_z4567 = (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4
            I_yz4567 = ((28-9*np.pi)/(72*(4-np.pi)))*r**4

            I_yi = np.array([(w1*t1**3)/12, (w2*t2**3)/12, (w3*t3**3)/12, I_y4567, I_y4567, I_y4567, I_y4567])
            I_zi = np.array([(t1*w1**3)/12, (t2*w2**3)/12, (t3*w3**3)/12, I_z4567, I_z4567, I_z4567, I_z4567])
            I_yzi = np.array([0, 0, 0, I_yz4567, -I_yz4567, I_yz4567, -I_yz4567])

        elif self.currentTab_beam_type == 4: # Beam: T-section

            self.section_label = "T-section"

            height = self.check_beam_inputs(self.lineEdit_height_T_section, 'HEIGHT')
            w1 = self.check_beam_inputs(self.lineEdit_w1_T_section, 'W1')
            w2 = self.check_beam_inputs(self.lineEdit_w2_T_section, 'W2')
            t1 = self.check_beam_inputs(self.lineEdit_t1_T_section, 't1')
            radius_T = self.check_beam_inputs(self.lineEdit_radius_T_section, 'RADIUS (T PROFILE)', check_radius=True)

            if self.lineEdit_radius_T_section.text() != "":
                if radius_T is None:
                    return
                else:
                    r = radius_T
            else:
                r = float(0)

            if None in [height, w1, w2, t1]:
                self.stop = True
                return

            if height < t1:
                title = "INPUT CROSS-SECTION ERROR"
                message = "The HEIGHT must be greater than t1."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return

            h = height
            t2 = h - t1        

            self.parameters = [h, w1, w2, t1, t2, r]

            A_i = np.array([w1*t1, w2*t2, ((4-np.pi)/4)*r**2, ((4-np.pi)/4)*r**2])
            A_t = np.sum(A_i)

            y_ci = np.array([0, 0, ((w2/2) + ((10-3*np.pi)/(3*(4-np.pi)))*r), -((w2/2) + ((10-3*np.pi)/(3*(4-np.pi)))*r)])
            z_ci = np.array([((t1+t2)/2), 0, ((t2/2) - ((10-3*np.pi)/(3*(4-np.pi)))*r), ((t2/2) - ((10-3*np.pi)/(3*(4-np.pi)))*r)])

            I_yi = np.array([(w1*t1**3)/12, (w2*t2**3)/12, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4])
            I_zi = np.array([(t1*w1**3)/12, (t2*w2**3)/12, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4, (((16-3*np.pi)/48)-(1/(9*(4-np.pi))))*r**4])
            I_yzi = np.array([0, 0, ((28-9*np.pi)/(72*(4-np.pi)))*r**4, -((28-9*np.pi)/(72*(4-np.pi)))*r**4])  

        if self.currentTab_beam_type in [2,3,4]:
            area = A_t
            Yc = (y_ci@A_i)/A_t
            Zc = (z_ci@A_i)/A_t
            Iyy = np.sum(I_yi + ((z_ci-Zc)**2)*A_i)
            Izz = np.sum(I_zi + ((y_ci-Yc)**2)*A_i)
            Iyz = np.sum(I_yzi + ((y_ci-Yc)*(z_ci-Zc))*A_i)
            self.parameters.append(Yc)
            self.parameters.append(Zc)

        self.external_diameter = 2*np.abs(np.sqrt(area/np.pi))
        self.thickness = 0
        self.Yc = Yc
        self.Zc = Zc

        if not plot:
            section_info = [self.section_label, self.parameters]
            self.cross_section = CrossSection(  self.external_diameter, self.thickness, 0, 0, 
                                                area=area, 
                                                Iyy=Iyy, 
                                                Izz=Izz, 
                                                Iyz=Iyz, 
                                                additional_section_info=section_info)
            self.complete = True
            plt.close()
            self.close()
        
    def check_beam_inputs(self, lineEdit, label, check_radius=False):

        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if check_radius:
                    if out < 0:
                        title = "INPUT CROSS-SECTION ERROR"
                        message = "Insert a positive value to the {}.".format(label)
                        PrintMessageInput([title, message, window_title])
                        self.stop = True
                        return None
                    elif out == 0:
                        return float(0)
                else:
                    if out <= 0:
                        title = "INPUT CROSS-SECTION ERROR"
                        message = "Insert a positive value to the {}.".format(label)
                        PrintMessageInput([title, message, window_title])
                        self.stop = True
                        return None
            except Exception:
                title = "INPUT CROSS-SECTION ERROR"
                message = "Wrong input for {}.".format(label)
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return None
        else:
            if check_radius:
                return float(0)
            else: 
                title = "INPUT CROSS-SECTION ERROR"
                message = "Insert some value for {}.".format(label)
                PrintMessageInput([title, message, window_title])                   
                self.stop = True
                return None
        return out

    def check_radius_values(self, lineEdit, value):
        if lineEdit.text() != "":
            if value is None:
                self.stop = True
                return None
            else:
                return value
        else:
            return 0

    def get_points_to_plot_section(self):

        if self.section_type == 0: # Rectangular section

            b, h, b_in, h_in, _, _ = self.parameters
            Yp_right = [0, (b/2), (b/2), 0, 0, (b_in/2), (b_in/2), 0, 0]
            Zp_right = [-(h/2), -(h/2), (h/2), (h/2), (h_in/2), (h_in/2), -(h_in/2), -(h_in/2), -(h/2)]
            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 1: # Circular section
            
            N = 60
            d_out, d_in, _, _ = self.parameters
            
            d_theta = np.pi/N
            theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)

            Yp_out = (d_out/2)*np.cos(theta)
            Zp_out = (d_out/2)*np.sin(theta)
            Yp_in = (d_in/2)*np.cos(-theta)
            Zp_in = (d_in/2)*np.sin(-theta)

            Yp_list = [list(Yp_out), list(Yp_in), [0]]
            Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 2: # Beam: C-section

            h, w1, w2, w3, t1, t2, t3, r, _, _ = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w3, w3, w2+r]) 
            Yp_list.append(list(np.flip(-y_r+w2)))
            Yp_list.append([w2, w2])
            Yp_list.append(list(w2-y_r))
            Yp_list.append([w2+r, w1, w1, 0, 0])

            Zp_list =[]
            Zp_list.append([-(h/2), -(h/2), -(t2/2), -(t2/2)]) 
            Zp_list.append(list(np.flip((-z_r+r)-(t2/2))))
            Zp_list.append([-(h/2)+t3+r, (h/2)-t1-r])
            Zp_list.append(list(z_r+(t2/2)-r))
            Zp_list.append([(h/2)-t1, (h/2)-t1, (h/2), (h/2), -(h/2)])

            Yp = [value for _list in Yp_list for value in _list]
            Zp = [value for _list in Zp_list for value in _list]

        elif self.section_type == 3: # Beam: I-section

            h, w1, w2, w3, t1, t2, t3, r, _, _ = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w3/2, w3/2, (w2/2)+r]) 
            Yp_list.append(list(np.flip(-y_r+(w2/2))))
            Yp_list.append([w2/2, w2/2])
            Yp_list.append(list((w2/2)-y_r))
            Yp_list.append([(w2/2)+r, w1/2, w1/2, 0])

            Zp_list =[]
            Zp_list.append([-(h/2), -(h/2), -((h/2)-t3), -((h/2)-t3)]) 
            Zp_list.append(list(np.flip((-z_r+r)-((h/2)-t3))))
            Zp_list.append([-(h/2)+t3+r, (h/2)-t1-r])
            Zp_list.append(list(z_r+(h/2)-t1-r))
            Zp_list.append([(h/2)-t1, (h/2)-t1, (h/2), (h/2)])

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]
            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        elif self.section_type == 4: # Beam: T-section

            h, w1, w2, t1, t2, r, _, _ = self.parameters
            y_r, z_r = self.get_points_at_radius(r)

            Yp_list =[]
            Yp_list.append([0, w2/2, w2/2])
            Yp_list.append(list((w2/2)-y_r))
            Yp_list.append([(w2/2)+r, w1/2, w1/2, 0])

            Zp_list =[]
            Zp_list.append([-(t2/2), -(t2/2), (h/2)-t1-r])
            Zp_list.append(list(z_r+(t2/2)-r))
            Zp_list.append([(t2/2), (t2/2), (t2/2)+t1, (t2/2)+t1])

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]
            Yp_left = -np.flip(Yp_right)
            Zp_left =  np.flip(Zp_right)

            Yp = np.array([Yp_right, Yp_left]).flatten()
            Zp = np.array([Zp_right, Zp_left]).flatten()

        return Yp, Zp
        
    def get_points_at_radius(self, r, N=20):

        if self.section_type in [2,3,4]:

            d_theta = (np.pi/2)/N
            theta = np.arange(d_theta, (np.pi/2), d_theta)
            y_r = -r + r*np.cos(theta)
            z_r = r*np.sin(theta)

            return y_r, z_r

    def plot_section(self):

        plt.close()

        self.check_beam(plot=True)
        if self.stop:
            self.stop = False
            return

        Yp, Zp = self.get_points_to_plot_section()
        _max = np.max(np.abs(np.array([Yp, Zp])))

        fig = plt.figure(figsize=[8,8])
        ax = fig.add_subplot(1,1,1)

        first_plot, = plt.fill(Yp, Zp, color=[0.2,0.2,0.2], linewidth=2, zorder=2)
        second_plot = plt.scatter(self.Yc, self.Zc, marker="+", linewidth=2, zorder=3, color=[1,0,0], s=150)

        second_plot.set_label("y: %7.5e // z: %7.5e" % (self.Yc, self.Zc))
        plt.legend(handles=[second_plot], framealpha=1, facecolor=[1,1,1], loc='upper right', title=r'$\bf{Centroid}$ $\bf{coordinates:}$')

        ax.set_title('CROSS-SECTION PLOT', fontsize = 18, fontweight = 'bold')
        ax.set_xlabel('y [m]', fontsize = 16, fontweight = 'bold')
        ax.set_ylabel('z [m]', fontsize = 16, fontweight = 'bold')
        
        f = 1.25
        if self.section_type == 2:
            np.min(np.array([Yp]))
            plt.xlim(-(1/2)*_max, (3/2)*_max)
        elif self.section_type in [0, 1, 3, 4]:
            plt.xlim(-_max*f, _max*f)

        plt.ylim(-_max*f, _max*f)
        plt.grid()
        plt.show()