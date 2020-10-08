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
        self.dict_group_elements = project.mesh.group_elements_with_stress_stiffening

        self.stop = False
        self.error_label = ""
        self.dict_label = "STRESS STIFFENING || {}"

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

        self.lineEdit_external_pressure = self.findChild(QLineEdit, 'lineEdit_external_pressure')
        self.lineEdit_internal_pressure = self.findChild(QLineEdit, 'lineEdit_internal_pressure')   
        self.lineEdit_external_temperature = self.findChild(QLineEdit, 'lineEdit_external_temperature')
        self.lineEdit_internal_temperature = self.findChild(QLineEdit, 'lineEdit_internal_temperature')

        self.checkBox_thermal_effect = self.findChild(QCheckBox, 'checkBox_thermal_effect')
        self.checkBox_pressure_effect = self.findChild(QCheckBox, 'checkBox_pressure_effect')
        self.checkBox_thermal_effect.toggled.connect(self.checkBoxEvent)
        self.checkBox_pressure_effect.toggled.connect(self.checkBoxEvent)
        self.flag_thermal_effect = self.checkBox_thermal_effect.isChecked()
        self.flag_pressure_effect = self.checkBox_pressure_effect.isChecked()

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')  
        self.pushButton_confirm.clicked.connect(self.press_confirm)
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset') 
        self.pushButton_reset.clicked.connect(self.check_reset_all)
        
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.press_confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def checkBoxEvent(self):
        self.flag_thermal_effect = self.checkBox_thermal_effect.isChecked()
        self.flag_pressure_effect = self.checkBox_pressure_effect.isChecked()
        
        if self.flag_thermal_effect:
            self.lineEdit_external_temperature.setDisabled(False)
            self.lineEdit_internal_temperature.setDisabled(False)
        else:
            self.lineEdit_external_temperature.setDisabled(True)
            self.lineEdit_internal_temperature.setDisabled(True)

        if self.flag_pressure_effect:
            self.lineEdit_external_pressure.setDisabled(False)
            self.lineEdit_internal_pressure.setDisabled(False)
        else:
            self.lineEdit_external_pressure.setDisabled(True)
            self.lineEdit_internal_pressure.setDisabled(True)

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

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

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

    def check_input_parameters(self):

        external_temperature = float(0)
        internal_temperature = float(0)
        external_pressure = float(0)
        internal_pressure = float(0)
        self.stop = False

        if not (self.flag_thermal_effect or self.flag_pressure_effect):
            title = "NONE EFFECT IS SELECTED"
            message = "Please, enable at least one effect \nbefore to confirm the attribution."
            PrintMessageInput([title, message, window_title])
            self.stop = True
            return True

        if self.flag_thermal_effect:

            self.error_label = "OUTER TEMPERATURE"
            if self.lineEdit_external_temperature.text() != "":

                try:
                    external_temperature = float(self.lineEdit_external_temperature.text())
                except Exception:
                    return True
            else:
                return True

            self.error_label = "INNER TEMPERATURE"
            if self.lineEdit_internal_temperature.text() != "":
                
                try:
                    internal_temperature = float(self.lineEdit_internal_temperature.text())
                except Exception:
                    return True
            else:
                return True

        if self.flag_pressure_effect:

            self.error_label = "OUTER PRESSURE"
            if self.lineEdit_external_pressure.text() != "":
                try:
                    external_pressure = float(self.lineEdit_external_pressure.text())
                except Exception:
                    return True
            else:
                return True

            self.error_label = "INNER PRESSURE"
            if self.lineEdit_internal_pressure.text() != "":
                try:
                    internal_pressure = float(self.lineEdit_internal_pressure.text())
                except Exception:
                    return True
            else:
                return True
        
        self.stress_stiffening_parameters = [external_temperature, internal_temperature, external_pressure, internal_pressure]

        return False

    def press_confirm(self):

        if self.check_input_parameters():
            if self.stop:
                return
            title = "STRESS STIFFENING INPUT ERROR"
            message = "Wrong input to the {}.".format(self.error_label)
            PrintMessageInput([title, message, window_title])
        else:

            if self.flagElements:
                if self.check_input_elements():
                    PrintMessageInput(self.info_text) 
                    return
                size = len(self.dict_group_elements)
                section = self.dict_label.format("Group-{}".format(size+1))
                self.project.set_stress_stiffening_by_elements(section, self.elements_typed, self.stress_stiffening_parameters)

            elif self.flagEntity:
                if self.check_input_lines():
                    PrintMessageInput(self.info_text) 
                    return
                for line_id in self.lines_typed:
                    self.project.set_stress_stiffening_by_line(line_id, self.stress_stiffening_parameters)
            elif self.flagAll:
                self.project.set_stress_stiffening_to_all_lines(self.stress_stiffening_parameters)

            self.complete = True
            self.close()        

    def check_reset_all(self):
        for line_id in self.project.mesh.all_lines:
            self.project.set_stress_stiffening_by_line(line_id, [0, 0, 0, 0], reset=True)
            self.project.file.remove_all_stress_stiffnening_in_file_by_group_elements()
        window_title = "WARNING MESSAGE"
        title = "STRESS STIFFENING REMOVAL"
        message = "The stress stiffening applied \nto all lines has been removed."
        PrintMessageInput([title, message, window_title])