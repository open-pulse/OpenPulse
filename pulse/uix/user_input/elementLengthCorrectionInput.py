from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.utils import error, remove_bc_from_file

class AcousticElementLengthCorrectionInput(QDialog):
    def __init__(self, project, elements_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/elementLengthCorrectionInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.acoustic_elements = project.mesh.acoustic_elements
        self.elements_id = elements_id
        self.type_label = None
        self.elements_info_path = project.file._element_info_path

        self.currentTab = 0
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')#lineEdit_elementID
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

        self.treeWidget_length_correction_elements = self.findChild(QTreeWidget, 'treeWidget_length_correction_elements')
        self.treeWidget_length_correction_elements.setColumnWidth(1, 20)
        self.treeWidget_length_correction_elements.setColumnWidth(2, 80)
        self.treeWidget_length_correction_elements.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_elements.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.treeWidget_length_correction_groups = self.findChild(QTreeWidget, 'treeWidget_length_correction_groups')
        self.treeWidget_length_correction_groups.setColumnWidth(0, 100)
        self.treeWidget_length_correction_groups.setColumnWidth(1, 100)
        # self.treeWidget_length_correction_groups.setColumnWidth(2, 100)
        self.treeWidget_length_correction_groups.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_groups.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_element_length_correction = self.findChild(QTabWidget, 'tabWidget_element_length_correction')
        self.tabWidget_element_length_correction.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_element_length_correction.currentIndex()

        self.pushButton_remove_by_group_confirm = self.findChild(QPushButton, 'pushButton_remove_by_group_confirm')
        self.pushButton_remove_by_group_confirm.clicked.connect(self.check_remove_element_length_correction_by_group)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information_of_group)

        self.pushButton_remove_by_elements_confirm = self.findChild(QPushButton, 'pushButton_remove_by_elements_confirm')
        self.pushButton_remove_by_elements_confirm.clicked.connect(self.check_remove_element_length_correction)   

        self.pushButton_reset_confirm = self.findChild(QPushButton, 'pushButton_reset_confirm')
        self.pushButton_reset_confirm.clicked.connect(self.check_remove_all_element_length_correction)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_element_correction_type)

        if self.elements_id != []:
            self.write_ids(elements_id)

        self.tabWidget_remove = self.findChild(QTabWidget, 'tabWidget_remove')
        self.tabWidget_remove.currentChanged.connect(self.tabEvent_remove)
        self.currentTab_remove = self.tabWidget_remove.currentIndex()

        self.load_elements_info()
        self.exec_()

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_element_length_correction.currentIndex()
        if self.currentTab_ == 0:
            text = "Elements IDs:"
        elif self.currentTab_ == 1: 
            if self.currentTab_remove == 0:
                text = "Group:"
            elif self.currentTab_remove == 1:
                text = "Elements IDs:"
        self.label_selection.setText(text)

    def tabEvent_remove(self):
        self.currentTab_remove = self.tabWidget_remove.currentIndex()
        if self.currentTab_remove == 0:
            text = "Group:"
        elif self.currentTab_remove == 1:
            text = "Elements IDs:"
        self.label_selection.setText(text)
        self.lineEdit_elementID.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()
     
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_elementID.setText(text)

    def check_input_elements(self):
        try:
            tokens = self.lineEdit_elementID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.elements_typed = list(map(int, tokens))

            if self.lineEdit_elementID.text()=="":
                error("Inform a valid Element ID before to confirm the input!", title = "ERROR IN ELEMENT ID's")
                return True

        except Exception:
            error("Wrong input for Element ID's!", "ERROR IN ELEMENT ID's")
            return True

        try:
            for element_id in self.elements_typed:
                self.acoustic_elements[element_id]
        except:
            message = [" The Element ID input values must be\n major than 1 and less than {}.".format(len(self.acoustic_elements))]
            error(message[0], title = " INCORRECT ELEMENT ID INPUT! ")
            return True

    def check_element_correction_type(self):
        if self.check_input_elements():
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

        self.project.set_element_length_correction_by_elements(self.elements_typed, type_id)
        self.close()

    def load_elements_info(self):
        
        keys = [0,1,2]
        labels = ['Expansion', 'Side branch', 'Loop']
        self.dict_correction_types = dict(zip(keys, labels))

        for element in self.project.mesh.element_with_length_correction:
            text = self.dict_correction_types[element.acoustic_length_correction]
            new = QTreeWidgetItem([str(element.index), text])
            self.treeWidget_length_correction_elements.addTopLevelItem(new)
        
        for _key, value in self.project.mesh.group_elements_with_length_correction.items():
            text = self.dict_correction_types[value[0]]
            new = QTreeWidgetItem([_key, text, str(value[1])])
            self.treeWidget_length_correction_groups.addTopLevelItem(new)            

    def check_remove_all_element_length_correction(self):
        for element in self.project.mesh.element_with_length_correction:
            self.project.set_element_length_correction_by_elements(element, None)
        self.project.mesh.group_elements_with_length_correction = {}
        error("The element length correction has been removed from all elements.", title="ELEMENT LENGTH CORRECTION RESET")

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        if self.currentTab_remove == 0:
            self.check_remove_element_length_correction_by_group()
        elif self.currentTab_remove == 1:
            self.check_remove_element_length_correction()

    def check_remove_element_length_correction_by_group(self):
        selected_key = self.lineEdit_elementID.text()
        if "Selection" in self.lineEdit_elementID.text():
            section = ["ACOUSTIC ELEMENT LENGTH CORRECTION || {}".format(selected_key)]
            values = self.project.mesh.group_elements_with_length_correction[selected_key]
            self.project.mesh.set_length_correction_by_element(values[1], None, group_to_remove=selected_key)
            key_strings = ["length correction type", "list of elements"]
            message = "The element length correction attributed to the {} group of elements have been removed.".format(selected_key)
            remove_bc_from_file(section, self.elements_info_path, key_strings, message)
            self.treeWidget_length_correction_groups.clear()
            self.load_elements_info()

    def get_information_of_group(self):
        try:
            selected_key = self.lineEdit_elementID.text()
            if "Selection-" in selected_key:
                values = self.project.mesh.group_elements_with_length_correction[selected_key]
                GetInformationOfGroup(values, self.dict_correction_types)
            else:
                error("Please, select a group in the list to get the information.", title="ERROR IN GROUP SELECTION")
                return
        except Exception as e:
            error(str(e), title="ERROR WHILE GETTING INFORMATION OF SELECTED GROUP")

    def check_remove_element_length_correction(self):
        return
        # self.check_input_elements()
        # self.project.mesh.set_acoustic_pressure_bc_by_node(self.elements_typed, None)
        # # #TODO under construction
        # # key_strings = ["length correction type", "list of elements"]
        # # message = "The element length correction attributed to the {} elements have been removed.".format(self.elements_typed)
        # # remove_bc_from_file(self.elements_typed, self.elements_info_path, key_strings, message)
        
        # # self.project.set_length_correction_by_element(self.elements_typed, None)
        # # self.treeWidget_length_correction_elements.clear()
        # # self.load_elements_info()


class GetInformationOfGroup(QDialog):
    def __init__(self, key_elements, dict_keys_labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/getInformationOfGroupInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.type = key_elements[0]
        self.list_of_elements = key_elements[1]
        self.dict_keys_labels = dict_keys_labels

        self.treeWidget_length_correction_group_info = self.findChild(QTreeWidget, 'treeWidget_length_correction_group_info')
        self.treeWidget_length_correction_group_info.setColumnWidth(1, 20)
        self.treeWidget_length_correction_group_info.setColumnWidth(2, 140)

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
            self.treeWidget_length_correction_group_info.addTopLevelItem(new)
    
    def force_to_close(self):
        self.close()

    