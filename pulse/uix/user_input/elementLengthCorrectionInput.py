from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.utils import error, info_messages, remove_bc_from_file

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
        self.treeWidget_length_correction_groups.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_groups.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_element_length_correction = self.findChild(QTabWidget, 'tabWidget_element_length_correction')
        self.tabWidget_element_length_correction.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_element_length_correction.currentIndex()

        self.pushButton_remove_by_group_confirm = self.findChild(QPushButton, 'pushButton_remove_by_group_confirm')
        self.pushButton_remove_by_group_confirm.clicked.connect(self.check_remove_element_length_correction_by_group)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information_of_group)

        self.pushButton_reset_confirm = self.findChild(QPushButton, 'pushButton_reset_confirm')
        self.pushButton_reset_confirm.clicked.connect(self.check_remove_all_element_length_correction)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_element_correction_type)

        if self.elements_id != []:
            self.write_ids(elements_id)

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
            self.check()
        elif event.key() == Qt.Key_Delete:
            self.check_remove_element_length_correction_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()
        

    def radioButtonEvent(self):
        self.flag_expansion = self.radioButton_expansion.isChecked()
        self.flag_side_branch = self.radioButton_side_branch.isChecked()
        self.flag_loop = self.radioButton_loop.isChecked()
     
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
        
        size = len(self.project.mesh.group_elements_with_length_correction)
        section = self.dict_label.format("Selection-{}".format(size+1))

        ind = 0
        while True:
            if section in self.project.mesh.group_elements_with_length_correction.keys():
                ind += 1
                section = self.dict_label.format("Selection-{}".format(ind))
            else:
                break
        self.project.set_element_length_correction_by_elements(self.elements_typed, type_id, section)
        if len(self.elements_id)>20:
            print("Set acoustic element length correction due the {} at {} selected elements".format(self.type_label, len(self.elements_id)))
        else:
            print("Set acoustic element length correction due the {} at elements:".format(self.type_label), self.elements_id)
        self.load_elements_info()
        # self.close()

    def load_elements_info(self):
        
        keys = [0,1,2]
        labels = ['Expansion', 'Side branch', 'Loop']
        self.dict_correction_types = dict(zip(keys, labels))
        self.treeWidget_length_correction_groups.clear()
        for section, value in self.project.mesh.group_elements_with_length_correction.items():
            text = self.dict_correction_types[value[0]]
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text, str(value[1])])
            self.treeWidget_length_correction_groups.addTopLevelItem(new)            

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        if self.currentTab_remove == 0:
            self.check_remove_element_length_correction_by_group()
        elif self.currentTab_remove == 1:
            self.check_remove_element_length_correction()

    def remove_function(self, key, reset=False):
        section = key

        if not reset:
            group_label = section.split(" || ")[1]
            message = "The element length correction attributed to the {} group of elements have been removed.".format(group_label)
        else:
            message = None

        values = self.project.mesh.group_elements_with_length_correction[section]
        self.project.mesh.set_length_correction_by_element(values[1], None, section, delete_from_dict=True)
        key_strings = ["length correction type", "list of elements"]
        
        remove_bc_from_file([section], self.elements_info_path, key_strings, message)
        self.load_elements_info()

    def check_remove_element_length_correction_by_group(self):
        key = self.dict_label.format(self.lineEdit_elementID.text())
        if "Selection-" in self.lineEdit_elementID.text():
            self.remove_function(key)
        self.lineEdit_elementID.setText("")

    def check_remove_all_element_length_correction(self):
        temp_dict_groups = self.project.mesh.group_elements_with_length_correction.copy()
        keys = temp_dict_groups.keys()
        for key in keys:
            self.remove_function(key, reset=True)
        info_messages("The element length correction of all elements has been removed.", title=">>> WARNING <<<")

    def get_information_of_group(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                values = self.project.mesh.group_elements_with_length_correction[selected_key]
                GetInformationOfGroup(values, self.dict_correction_types)
            else:
                error("Please, select a group in the list to get the information.", title="ERROR IN GROUP SELECTION")
                return
        except Exception as e:
            error(str(e), title="ERROR WHILE GETTING INFORMATION OF SELECTED GROUP")


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

    