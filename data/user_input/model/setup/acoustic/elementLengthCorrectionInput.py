from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import configparser
import numpy as np

from pulse.utils import remove_bc_from_file
from data.user_input.project.printMessageInput import PrintMessageInput

window_title = "ERROR"

class AcousticElementLengthCorrectionInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/Model/Setup/Acoustic/elementLengthCorrectionInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.elements_id = self.opv.getListPickedElements()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()   

        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.dict_group_elements = project.preprocessor.group_elements_with_length_correction
        
        self.type_label = None
        self.dkey = None
        self.log_removal = True
        self.elements_info_path = project.file._element_info_path
        self.dict_label = "ACOUSTIC ELEMENT LENGTH CORRECTION || {}"

        self.currentTab = 0
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')
        self.label_selection = self.findChild(QLabel, 'label_selection')

        self.radioButton_expansion = self.findChild(QRadioButton, 'radioButton_expansion')
        self.radioButton_side_branch = self.findChild(QRadioButton, 'radioButton_side_branch')
        self.radioButton_loop = self.findChild(QRadioButton, 'radioButton_loop')

        self.radioButton_expansion.toggled.connect(self.radioButtonEvent)
        self.radioButton_side_branch.toggled.connect(self.radioButtonEvent)
        self.radioButton_loop.toggled.connect(self.radioButtonEvent)

        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()

        self.treeWidget_length_correction_groups = self.findChild(QTreeWidget, 'treeWidget_length_correction_groups')
        self.treeWidget_length_correction_groups.setColumnWidth(0, 100)
        self.treeWidget_length_correction_groups.setColumnWidth(1, 80)
        self.treeWidget_length_correction_groups.setColumnWidth(2, 90)        
        self.treeWidget_length_correction_groups.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_groups.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_element_length_correction = self.findChild(QTabWidget, 'tabWidget_element_length_correction')
        self.tabWidget_element_length_correction.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_element_length_correction.currentIndex()

        self.pushButton_remove_by_group_confirm = self.findChild(QPushButton, 'pushButton_remove_by_group_confirm')
        self.pushButton_remove_by_group_confirm.clicked.connect(self.remove_element_length_correction_by_group)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information_of_group)

        self.pushButton_reset_confirm = self.findChild(QPushButton, 'pushButton_reset_confirm')
        self.pushButton_reset_confirm.clicked.connect(self.remove_all_element_length_correction)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_element_correction_type)

        if self.elements_id != []:
            self.write_ids(self.elements_id)

        self.load_elements_info()
        self.exec_()

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_element_length_correction.currentIndex()
        if self.currentTab_ == 0:
            text = "Elements IDs:"
            self.write_ids(self.elements_id)
        elif self.currentTab_ == 1: 
            text = "Group:"
            self.lineEdit_elementID.setText("")
        self.label_selection.setText(text)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_elementID.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_element_correction_type()
        elif event.key() == Qt.Key_Delete:
            self.remove_element_length_correction_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()
        
    def radioButtonEvent(self):
        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()
     
    def check_element_correction_type(self):

        lineEdit = self.lineEdit_elementID.text()
        self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
        
        if self.stop:
            return

        if self.flag_expansion:
            type_id = 0
            self.type_label = "'Expansion'"
   
        elif self.flag_side_branch:
            type_id = 1
            self.type_label = "'Side branch'"

        elif self.flag_loop:
            type_id = 2
            self.type_label = "'Loop'"
        
        size = len(self.dict_group_elements)
        section = self.dict_label.format("Selection-{}".format(size+1))
        dict_keys = self.preprocessor.group_elements_with_perforated_plate.keys()
        if section in dict_keys:
            index = 0
            while section in dict_keys:
                index += 1
                section = self.dict_label.format(f"Selection-{index}")

        self.set_elements_to_correct(type_id, section, _print=True)
        self.replaced = False

        temp_dict = self.dict_group_elements.copy()
        
        for key, values in temp_dict.items():
            if list(np.sort(self.elements_typed)) == list(np.sort(values[1])):
                if self.replaced:
                    self.dkey = key
                    self.log_removal = False
                    self.remove_element_length_correction_by_group()
                else:
                    self.set_elements_to_correct(type_id, key)
                    self.replaced = True
            else:

                count1, count2 = 0, 0
                for element in self.elements_typed:
                    if element in values[1]:
                        count1 += 1
                fill_rate1 = count1/len(self.elements_typed)

                for element in values[1]:
                    if element in self.elements_typed:
                        count2 += 1
                fill_rate2 = count2/len(values[1])
                
                if np.max([fill_rate1, fill_rate2])>0.5 :
                    if not self.replaced:
                        self.set_elements_to_correct(type_id, key)
                        self.replaced = True
                    else:
                        self.dkey = key
                        self.log_removal = False
                        self.remove_element_length_correction_by_group()
            self.dkey = None  
        self.close()         

    def set_elements_to_correct(self, type_id, section, _print=False): 
        self.project.set_element_length_correction_by_elements(list(np.sort(self.elements_typed)), type_id, section)
        if _print:
            if len(self.elements_id)>20:
                print("Set acoustic element length correction due the {} at {} selected elements".format(self.type_label, len(self.elements_id)))
            else:
                print("Set acoustic element length correction due the {} at elements: {}".format(self.type_label, self.elements_id))
        self.load_elements_info()

    def load_elements_info(self):
        
        keys = [0,1,2]
        labels = ['Expansion', 'Side branch', 'Loop']
        self.dict_correction_types = dict(zip(keys, labels))
        self.treeWidget_length_correction_groups.clear()
        for section, value in self.dict_group_elements.items():
            text = self.dict_correction_types[value[0]]
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text, str(value[1])])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            new.setTextAlignment(2, Qt.AlignCenter)
            self.treeWidget_length_correction_groups.addTopLevelItem(new)            

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        if self.currentTab_remove == 0:
            self.remove_element_length_correction_by_group()
        elif self.currentTab_remove == 1:
            self.check_remove_element_length_correction()

    def remove_function(self, key):
        section = key

        if self.log_removal:
            group_label = section.split(" || ")[1]
            message = f"The element length correction attributed to the {group_label}\n"
            message += "group of elements have been removed."
        else:
            message = None

        values = self.dict_group_elements[section]
        self.project.preprocessor.set_length_correction_by_element(values[1], None, section, delete_from_dict=True)
        key_strings = ["length correction type", "list of elements"]
        
        remove_bc_from_file([section], self.elements_info_path, key_strings, message)
        self.load_elements_info()
        self.log_removal = True

    def remove_element_length_correction_by_group(self):
        if self.dkey is None:
            key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in self.lineEdit_elementID.text():
                self.remove_function(key)
            self.lineEdit_elementID.setText("")
        else:
            self.remove_function(self.dkey)

    def remove_all_element_length_correction(self):
        temp_dict_groups = self.dict_group_elements.copy()
        keys = temp_dict_groups.keys()
        for key in keys:
            self.log_removal = False
            self.remove_function(key)
        window_title = "WARNING" 
        title = "INFO MESSAGE"
        message = "The element length correction has been \nremoved from all elements."
        PrintMessageInput([title, message, window_title])

    def get_information_of_group(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                values = self.dict_group_elements[selected_key]
                GetInformationOfGroup(values, self.dict_correction_types)
            else:
                title = "ERROR IN GROUP SELECTION"
                message = "Please, select a group in the list to get the information."
                self.info_text = [title, message, window_title]
                PrintMessageInput(self.info_text)
        except Exception as er:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(er)
            self.info_text = [title, message, window_title]
            PrintMessageInput(self.info_text)

    def update(self):
        self.write_ids(self.opv.getListPickedElements())
        self.elements_id = self.opv.getListPickedElements()


class GetInformationOfGroup(QDialog):
    def __init__(self, key_elements, dict_keys_labels, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/Model/Info/getGroupInformationInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.type = key_elements[0]
        self.list_of_elements = key_elements[1]
        self.dict_keys_labels = dict_keys_labels

        self.treeWidget_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.setColumnWidth(0, 140)
        # self.treeWidget_group_info.setColumnWidth(2, 140)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.load_group_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        for element in self.list_of_elements:
            text = self.dict_keys_labels[self.type]
            new = QTreeWidgetItem([str(element), text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)
    
    def force_to_close(self):
        self.close()