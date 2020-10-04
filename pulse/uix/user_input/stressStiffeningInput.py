from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt

window_title = "ERROR MESSAGE"

class StressStiffeningInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/stressStiffeningInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.structural_elements = self.project.mesh.structural_elements
        self.dict_tag_to_entity = self.project.mesh.get_dict_of_entities()
        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()


        # self.section_key = None
        # self.parameters = None
        # self.section_info = None
        # self.complete = False
        # self.flagAll = False
        # self.flagEntity = False
        # self.currentTab = 0

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')
        self.lineEdit_selected_ID.setEnabled(True)

        self.lineEdit_outerPresure = self.findChild(QLineEdit, 'lineEdit_outerPressure')
        self.lineEdit_innerPresure = self.findChild(QLineEdit, 'lineEdit_innerPressure')   
        self.lineEdit_outerTemperature = self.findChild(QLineEdit, 'lineEdit_outerTemperature')
        self.lineEdit_innerTemperature = self.findChild(QLineEdit, 'lineEdit_innerTemperature')

        self.checkBox_thermal_effect = self.findChild(QCheckBox, 'checkBox_thermal_effect')
        self.checkBox_pressure_effect = self.findChild(QCheckBox, 'checkBox_pressure_effect')
        self.checkBox_thermal_effect.toggled.connect(self.checkBoxEvent)
        self.checkBox_pressure_effect.toggled.connect(self.checkBoxEvent)
        self.flag_thermal_effect = self.checkBox_thermal_effect.isChecked()
        self.flag_pressure_effect = self.checkBox_pressure_effect.isChecked()

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')  
        # self.pushButton_confirm.clicked.connect(self.check_dofs_coupling)
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset') 
        # self.pushButton_reset.clicked.connect(self.check_reset_all)
        
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
            self.lineEdit_selected_ID.setEnabled(False)
            self.radioButton_all_lines.setChecked(True)      

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_general.currentIndex() == 0:
                self.confirm_pipe()
            if self.tabWidget_general.currentIndex() == 1:
                self.confirm_beam()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def checkBoxEvent(self):
        self.flag_thermal_effect = self.checkBox_thermal_effect.isChecked()
        self.flag_pressure_effect = self.checkBox_pressure_effect.isChecked()

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        self.lineEdit_selected_ID.setEnabled(True)

        if self.flagAll:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)

        elif self.flagEntity:
            self.lineEdit_id_labels.setText("Lines IDs:")
            self.write_ids(self.lines_id)

        elif self.flagElements:
            self.lineEdit_id_labels.setText("Elements IDs:")
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
            self.element_typed = list(map(int, tokens))
            
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
            for element in self.element_typed:
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
            self.line_typed = list(map(int, tokens))
            
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
            for line in self.line_typed:
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

            self.cross_section = CrossSection(outerDiameter, thickness, offset_y, offset_z, 
                                            insulation_density=insulation_density, insulation_thickness=insulation_thickness, additional_section_info=section_info)

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

                read = CrossSectionBeamInput(self.section_key)
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
                self.cross_section = CrossSection(self.external_diameter, self.thickness, 0, 0, area=area, Iyy=Iyy, Izz=Izz, Iyz=Iyz, 
                                                additional_section_info=section_info, shear_coefficient=shear_coefficient)

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