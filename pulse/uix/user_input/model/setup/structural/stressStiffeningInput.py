from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

import numpy as np
import matplotlib.pyplot as plt

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class StressStiffeningInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/Model/Setup/Structural/stressStiffeningInput.ui', self)

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
        self.lines_with_stress_stiffening = project.mesh.lines_with_stress_stiffening
        self.dict_lines_with_stress_stiffening = project.mesh.dict_lines_with_stress_stiffening
        
        self.stop = False
        self.error_label = ""
        self.dictKey_label = "STRESS STIFFENING || {}"
        self.dictkey_to_remove = None

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

        self.treeWidget_stress_stiffening_elements = self.findChild(QTreeWidget, 'treeWidget_stress_stiffening_elements')
        self.treeWidget_stress_stiffening_elements.setColumnWidth(0, 100)
        self.treeWidget_stress_stiffening_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_stress_stiffening_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)
        self.treeWidget_stress_stiffening_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_stress_stiffening_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.treeWidget_stress_stiffening_lines = self.findChild(QTreeWidget, 'treeWidget_stress_stiffening_lines')
        self.treeWidget_stress_stiffening_lines.setColumnWidth(0, 100)
        self.treeWidget_stress_stiffening_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_stress_stiffening_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)
        self.treeWidget_stress_stiffening_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_stress_stiffening_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.tabWidget_stress_stiffening = self.findChild(QTabWidget, 'tabWidget_stress_stiffening')
        self.tabWidget_stress_stiffening.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_stress_stiffening.currentIndex()

        self.pushButton_remove_elem = self.findChild(QPushButton, 'pushButton_remove_elem')
        self.pushButton_remove_elem.clicked.connect(self.remove_elem_group)
        self.pushButton_remove_line = self.findChild(QPushButton, 'pushButton_remove_line')
        self.pushButton_remove_line.clicked.connect(self.remove_line_group)
        self.pushButton_get_information_elem = self.findChild(QPushButton, 'pushButton_get_information_elem')
        self.pushButton_get_information_elem.clicked.connect(self.get_information_elem)
        self.pushButton_get_information_line = self.findChild(QPushButton, 'pushButton_get_information_line')
        self.pushButton_get_information_line.clicked.connect(self.get_information_line)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')  
        self.pushButton_confirm.clicked.connect(self.press_confirm)
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset') 
        self.pushButton_reset.clicked.connect(self.check_reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close') 
        self.pushButton_close.clicked.connect(self.force_to_close)

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

        self.update_info()
        self.update_buttons_()
        self.tabEvent_()
        self.exec_()

    def force_to_close(self):
        self.close()

    def update_buttons_(self):
        self.pushButton_get_information_elem.setDisabled(True)
        self.pushButton_get_information_line.setDisabled(True)
        self.pushButton_remove_elem.setDisabled(True)
        self.pushButton_remove_line.setDisabled(True)

    def update_info(self):
        self.load_lines_info()
        self.load_elements_info()

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

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_stress_stiffening.currentIndex()
        if self.currentTab_ == 0:
            if self.flagElements:
                text = "Elements IDs:"
                self.write_ids(self.elements_id)
            elif self.flagEntity:
                text = "Lines IDs:"
                self.write_ids(self.lines_id)
            elif self.flagAll:
                text = "Lines IDs:"
                self.lineEdit_selected_ID.setText("All lines")
        elif self.currentTab_ == 1:
            text = "Group:"
            self.lineEdit_selected_ID.setText("")
            self.lineEdit_selected_ID.setDisabled(True)
            self.pushButton_remove_line.setDisabled(True)
            self.pushButton_get_information_line.setDisabled(True)
            self.pushButton_remove_elem.setDisabled(True)
            self.pushButton_get_information_elem.setDisabled(True)   
        self.lineEdit_id_labels.setText(text)

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

        if self.currentTab_ == 0:
            if self.radioButton_selected_elements.isChecked():
                text = "Elements IDs:"
                self.write_ids(self.elements_id)
            elif self.radioButton_selected_lines.isChecked():
                text = "Lines IDs:"
                self.write_ids(self.lines_id)
            elif self.radioButton_all_lines.isChecked():
                text = "Lines IDs:"
                self.lineEdit_selected_ID.setText("All lines")
                self.lineEdit_selected_ID.setEnabled(False)
        elif self.currentTab_ == 1: 
            text = "Group:"
            self.lineEdit_selected_ID.setText("")
        self.lineEdit_id_labels.setText(text)

    def load_elements_info(self):
        self.treeWidget_stress_stiffening_elements.clear()
        for section, values in self.dict_group_elements.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(values[1])])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_stress_stiffening_elements.addTopLevelItem(new)  

    def load_lines_info(self):        
        self.treeWidget_stress_stiffening_lines.clear()
        lines = self.project.mesh.lines_with_stress_stiffening
        if len(lines) != 0:
            new = QTreeWidgetItem(["Enabled lines" , str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_stress_stiffening_lines.addTopLevelItem(new)   

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def on_click_item_elem(self, item):
        self.lineEdit_selected_ID.setText(item.text(0))
        self.lineEdit_id_labels.setText("Group")
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove_line.setDisabled(True)
        self.pushButton_get_information_line.setDisabled(True)
        self.pushButton_remove_elem.setDisabled(False)
        self.pushButton_get_information_elem.setDisabled(False)        

    def on_click_item_line(self, item):
        text = item.text(1).replace("[","")
        text = text.replace("]","")
        self.lineEdit_selected_ID.setText(text)
        self.lineEdit_id_labels.setText("Lines IDs")
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove_line.setDisabled(False)
        self.pushButton_get_information_line.setDisabled(False)
        self.pushButton_remove_elem.setDisabled(True)
        self.pushButton_get_information_elem.setDisabled(True)        

    def on_doubleclick_item_elem(self, item):
        self.lineEdit_selected_ID.setText(item.text(0))
        if self.currentTab_ == 1:
            self.remove_elem_group()

    def on_doubleclick_item_line(self, item):
        self.lineEdit_selected_ID.setText(item.text(1))
        if self.currentTab_ == 1:
            self.remove_line_group()

    def get_list_typed_entries(self):
        tokens = self.lineEdit_selected_ID.text().strip().split(',')
        try:
            tokens.remove('')
        except:     
            pass
        output = list(map(int, tokens))
        return output

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
                self.info_text = [title, message, window_title1]     
                return True
        except Exception:
            title = "Error: invalid Element ID input"
            message = "Wrong input for Node ID's."
            self.info_text = [title, message, window_title1]   
            return True

        try:
            for element in self.elements_typed:
                self.elementID = self.structural_elements[element].index
        except Exception:
            title = "Error: invalid Element ID input"
            message = " The Element ID input values must be \nmajor than 1 and less than {}.".format(len(self.structural_elements))
            self.info_text = [title, message, window_title1]
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
                self.info_text = [title, message, window_title1]
                return True
        except Exception:
            title = "Error: invalid Line ID input"
            message = "Wrong input for Line ID."
            self.info_text = [title, message, window_title1]
            return True
        try:
            for line in self.lines_typed:
                self.line = self.dict_tag_to_entity[line]
        except Exception:
            title = "Error: invalid Line ID"
            message = "The Line ID input values must be \nmajor than 1 and less than {}.".format(len(self.dict_tag_to_entity))
            self.info_text = [title, message, window_title1]
            return True
        return False

    def check_input_parameters(self):

        external_temperature = float(0)
        internal_temperature = float(0)
        external_pressure = float(0)
        internal_pressure = float(0)
        self.stop = False

        if not (self.flag_thermal_effect or self.flag_pressure_effect):
            title = "NONE EFFECT HAS BEEN SELECTED"
            message = "Please, enable at least one effect \nbefore to confirm the attribution."
            PrintMessageInput([title, message, window_title1])
            self.stop = True
            return True

        if self.flag_thermal_effect:

            self.error_label = "EXTERNAL TEMPERATURE"
            if self.lineEdit_external_temperature.text() != "":

                try:
                    external_temperature = float(self.lineEdit_external_temperature.text())
                except Exception:
                    return True
            else:
                return True

            self.error_label = "INTERNAL TEMPERATURE"
            if self.lineEdit_internal_temperature.text() != "":
                
                try:
                    internal_temperature = float(self.lineEdit_internal_temperature.text())
                except Exception:
                    return True
            else:
                return True

        if self.flag_pressure_effect:

            self.error_label = "EXTERNAL PRESSURE"
            if self.lineEdit_external_pressure.text() != "":
                try:
                    external_pressure = float(self.lineEdit_external_pressure.text())
                except Exception:
                    return True
            else:
                return True

            self.error_label = "INTERNAL PRESSURE"
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
            PrintMessageInput([title, message, window_title1])
        else:

            if self.flagElements:
                if self.check_input_elements():
                    PrintMessageInput(self.info_text) 
                    return

                size = len(self.project.mesh.group_elements_with_stress_stiffening)
                section = self.dictKey_label.format("Selection-{}".format(size+1))
                self.set_stress_stiffening_to_elements(section)
                self.replaced = False

                # checking the oversampling of elements in each group of elements
                if size > 0:
                    temp_dict = self.dict_group_elements.copy()
                    for key, item in temp_dict.items():
                        elements = item[1]
                        if list(np.sort(self.elements_typed)) == list(np.sort(elements)):
                            if self.replaced:
                                self.dictkey_to_remove = key
                                self.remove_elem_group()
                            else:
                                self.set_stress_stiffening_to_elements(key)
                                self.replaced = True
                        else:    
                            count1, count2 = 0, 0
                            for element in self.elements_typed:
                                if element in elements:
                                    count1 += 1
                            fill_rate1 = count1/len(self.elements_typed)

                            for element in elements:
                                if element in self.elements_typed:
                                    count2 += 1
                            fill_rate2 = count2/len(elements)
                            
                            if np.max([fill_rate1, fill_rate2])>0.5 :
                                if self.replaced:
                                    self.dictkey_to_remove = key
                                    self.remove_elem_group()
                                else:
                                    self.set_stress_stiffening_to_elements(key)
                                    self.replaced = True
                        self.dictkey_to_remove = None 

            elif self.flagEntity:
                if self.check_input_lines():
                    PrintMessageInput(self.info_text) 
                    return
                for line_id in self.lines_typed:
                    self.project.set_stress_stiffening_by_line(line_id, self.stress_stiffening_parameters)

            elif self.flagAll:
                all_lines = self.project.mesh.all_lines
                self.project.set_stress_stiffening_by_line(all_lines, self.stress_stiffening_parameters)

            self.complete = True
            self.close()        

    def set_stress_stiffening_to_elements(self, section):
        self.project.set_stress_stiffening_by_elements(self.elements_typed, self.stress_stiffening_parameters, section)
        self.load_elements_info()

    def check_reset_all(self):
        temp_dict_group_elements = self.dict_group_elements.copy()
        for line_id in self.project.mesh.all_lines:
            self.project.set_stress_stiffening_by_line(line_id, [0,0,0,0], remove=True)
            self.project.file.remove_all_stress_stiffnening_in_file_by_group_elements()
        for key, item in temp_dict_group_elements.items():
            self.project.set_stress_stiffening_by_elements(item[1], item[0], key, remove=True)

        self.update_info()
        self.update_buttons_()
        self.lineEdit_selected_ID.setText("")
        
        title = "STRESS STIFFENING REMOVAL"
        message = "The stress stiffening applied \nto all lines has been removed."
        PrintMessageInput([title, message, window_title2])

    def remove_elements(self, key, reset=False):
        section = key        
        list_data = self.dict_group_elements[section]
        elements = list_data[1]
        self.project.set_stress_stiffening_by_elements(elements, [0,0,0,0], section, remove=True)
        self.load_elements_info()
        group_label = section.split(" || ")[1]
        print("The Stress Stiffening enabled to the {} of element(s) have been removed.".format(group_label))

    def remove_elem_group(self):
        if self.dictkey_to_remove is None:
            text = self.lineEdit_selected_ID.text()
            key = self.dictKey_label.format(text)
            self.remove_elements(key)
            self.lineEdit_selected_ID.setText("")
        else:
            self.remove_elements(self.dictkey_to_remove)

    def remove_line_group(self):
        parameters = [0,0,0,0]
        lines = self.project.mesh.lines_with_stress_stiffening.copy()
        self.project.set_stress_stiffening_by_line(lines, parameters, remove=True)
        self.load_lines_info()
        self.lineEdit_selected_ID.setText("")

    def get_information_elem(self):
        try:
            selected_key = self.dictKey_label.format(self.lineEdit_selected_ID.text())
            if "Selection-" in selected_key:
                values = self.dict_group_elements[selected_key]
                GetInformationOfGroup(self.project, values, "Elements")
            else:
                title = "UNSELECTED GROUP OF ELEMENTS"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([title, message, window_title2])
                  
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([title, message, window_title1])

    def get_information_line(self):
        try:
            if self.lineEdit_selected_ID.text() != "":
                list_lines = self.get_list_typed_entries()          
                read = GetInformationOfGroup(self.project, list_lines, "Lines")
                if read.lines_removed:
                    self.load_lines_info()
            else:
                title = "UNSELECTED GROUP OF LINES"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([title, message, window_title2])
                
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([title, message, window_title1])

class GetInformationOfGroup(QDialog):
    def __init__(self, project, values, label, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        if label == "Elements":
            uic.loadUi('pulse/uix/user_input/ui/Model/Info/getGroupInformationInput.ui', self)
            self.flagElements = True
            self.flagLines = False

        elif label == "Lines":
            uic.loadUi('pulse/uix/user_input/ui/Model/Info/getGroupInformationAndRemoveInput.ui', self)
            self.flagLines = True
            self.flagElements = False
            self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
            self.lineEdit_selected_ID.setDisabled(True)
            self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')
            self.lineEdit_id_labels.setText("Line ID")
            self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
            self.pushButton_remove.clicked.connect(self.check_remove)
            self.lines_removed = False

        self.label = label
        self.input_values = values
        self.project = project

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, self.label)
        self.treeWidget_group_info.headerItem().setText(1, "Parameters [Tout, Tin, Pout, Pin]")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        
        self.treeWidget_group_info.setColumnWidth(0, 80)
        self.treeWidget_group_info.setColumnWidth(1, 140)
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.update_dict()
        self.load_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()

    def update_dict(self):
        self.dict_lines_parameters = self.project.mesh.dict_lines_with_stress_stiffening
        self.dict_elements_parameters = self.project.mesh.group_elements_with_stress_stiffening

    def on_click_item_(self, item):
        text = item.text(0)
        self.lineEdit_selected_ID.setText(text)
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def check_remove(self):
        if self.flagLines:
            if self.lineEdit_selected_ID.text() != "":
                line = int(self.lineEdit_selected_ID.text())
                if line in self.input_values:
                    self.input_values.remove(line)
                parameters = self.dict_lines_parameters[line]
                self.project.set_stress_stiffening_by_line(line, parameters, remove=True)
                self.update_dict()
                self.load_info()
                self.lines_removed = True
        self.lineEdit_selected_ID.setText("")

    def load_info(self):
        self.treeWidget_group_info.clear()
        if self.label == "Lines":       
            for key, parameters in self.dict_lines_parameters.items():
                new = QTreeWidgetItem([str(key), str(parameters)])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_group_info.addTopLevelItem(new)
        elif self.label == "Elements":
            data = self.input_values
            elements = list(np.sort(data[1]))
            for element in elements:
                new = QTreeWidgetItem([str(element), str(data[0])])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_group_info.addTopLevelItem(new)                

    def force_to_close(self):
        self.close()