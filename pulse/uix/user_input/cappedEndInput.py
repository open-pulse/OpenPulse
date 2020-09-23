from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np

from pulse.utils import error, info_messages, remove_bc_from_file

class cappedEndInput(QDialog):
    def __init__(self, project, lines_id, elements_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/cappedEndInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.structural_elements = self.project.mesh.structural_elements
        self.entities = self.project.mesh.entities
        self.lines_id = lines_id
        self.elements_id = elements_id

        self.project_lines = {}
        for line in self.project.mesh.all_lines:
            self.project_lines[line] = True

        self.dict_group_elements = project.mesh.group_elements_with_capped_end
        self.dict_group_lines = project.mesh.group_lines_with_capped_end
        self.elements_id = elements_id
        self.type_label = "'capped End'"
        self.dkey = None
        self.elements_info_path = project.file._element_info_path
        self.entity_path = project.file._entity_path
        self.dict_label = "capped END || {}"

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')
        self.label_selection = self.findChild(QLabel, 'label_selection')

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)

        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)

        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)
        
        self.radioButton_cappedEnd = self.findChild(QRadioButton, 'radioButton_cappedEnd')
        self.radioButton_cappedEnd.toggled.connect(self.radioButtonEvent)

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        self.flagcappedEnd = self.radioButton_cappedEnd.isChecked()

        self.treeWidget_cappedEnd_elements = self.findChild(QTreeWidget, 'treeWidget_cappedEnd_elements')
        self.treeWidget_cappedEnd_elements.setColumnWidth(0, 100)
        self.treeWidget_cappedEnd_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_cappedEnd_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)

        self.treeWidget_cappedEnd_lines = self.findChild(QTreeWidget, 'treeWidget_cappedEnd_lines')
        self.treeWidget_cappedEnd_lines.setColumnWidth(0, 100)
        self.treeWidget_cappedEnd_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_cappedEnd_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)

        self.tabWidget_cappedEnd = self.findChild(QTabWidget, 'tabWidget_cappedEnd')
        self.tabWidget_cappedEnd.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_cappedEnd.currentIndex()

        self.pushButton_remove_elem = self.findChild(QPushButton, 'pushButton_remove_elem')
        self.pushButton_remove_elem.clicked.connect(self.remove_elem_group)

        self.pushButton_remove_line = self.findChild(QPushButton, 'pushButton_remove_line')
        self.pushButton_remove_line.clicked.connect(self.remove_line_group)

        self.pushButton_get_information_elem = self.findChild(QPushButton, 'pushButton_get_information_elem')
        self.pushButton_get_information_elem.clicked.connect(self.get_information_elem)

        self.pushButton_get_information_line = self.findChild(QPushButton, 'pushButton_get_information_line')
        self.pushButton_get_information_line.clicked.connect(self.get_information_line)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_element_capped_end)

        if self.lines_id != []:
            self.label_selection.setText("Lines IDs:")
            self.write_ids(lines_id)
            self.radioButton_selected_lines.setChecked(True)
        elif self.elements_id != []:
            self.label_selection.setText("Elements IDs:")
            self.write_ids(elements_id)
            self.radioButton_selected_elements.setChecked(True)
        else:
            self.label_selection.setText("Lines IDs:")
            self.lineEdit_elementID.setText("All lines")
            self.radioButton_all_lines.setChecked(True)

        if self.elements_id != []:
            self.write_ids(elements_id)

        self.load_lines_info()
        self.load_elements_info()
        self.tabEvent_()
        self.exec_()

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_cappedEnd.currentIndex()
        if self.currentTab_ == 0:
            if self.flagElements:
                text = "Elements IDs:"
                self.write_ids(self.elements_id)
            elif self.flagEntity:
                text = "Lines IDs:"
                self.write_ids(self.lines_id)
            elif self.flagAll:
                text = "Lines IDs:"
                self.lineEdit_elementID.setText("All lines")
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
            self.remove_cappedEnd_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()
        

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        self.flagcappedEnd = self.radioButton_cappedEnd.isChecked()
        if self.currentTab_ == 0:
            if self.radioButton_selected_elements.isChecked():
                text = "Elements IDs:"
                self.write_ids(self.elements_id)
            elif self.radioButton_selected_lines.isChecked():
                text = "Lines IDs:"
                self.write_ids(self.lines_id)
            elif self.radioButton_all_lines.isChecked():
                text = "Lines IDs:"
                self.lineEdit_elementID.setText("All lines")
        elif self.currentTab_ == 1: 
            text = "Group:"
            self.lineEdit_elementID.setText("")
        self.label_selection.setText(text)
     
    def check_input_elements(self):
        if self.flagAll:
            self.set_capped_end_to_all_lines()
        else:
            try:
                tokens = self.lineEdit_elementID.text().strip().split(',')
                try:
                    tokens.remove('')
                except:     
                    pass
                self.typed_id = np.sort(list(map(int, tokens))).tolist()

                if self.lineEdit_elementID.text()=="":
                    error("Inform a valid Element ID before to confirm the input!", title = "ERROR IN ELEMENT ID's")
                    return True

            except Exception:
                error("Wrong input for Element ID's!", "ERROR IN ELEMENT ID's")
                return True

            try:
                if self.flagElements:
                    for element_id in self.typed_id:
                        self.structural_elements[element_id]
                elif self.flagEntity:
                    for entity_id in self.typed_id:
                        self.project_lines[entity_id]
                elif self.flagAll:
                    self.typed_id = 'all'
                
            except:
                if self.flagElements:
                    message = ["The Element ID input values must be \nmajor than 1 and less than {}.".format(len(self.structural_elements))]
                    error(message[0], title = " INCORRECT ELEMENT ID INPUT! ")
                elif self.flagEntity:
                    message = ["The Line ID input values must be \nmajor than 1 and less than {}.".format(len(self.entities))]
                    error(message[0], title = " INCORRECT ELEMENT ID INPUT! ")
                return True

    def check_element_capped_end(self):

        if self.check_input_elements():
            return

        size = len(self.dict_group_elements) + len(self.dict_group_lines)
        selection = self.dict_label.format("Selection-{}".format(size+1))

        ind = 0
        while True:
            if selection in self.dict_group_elements.keys():
                ind += 1
                selection = self.dict_label.format("Selection-{}".format(ind))
            else:
                break

        if self.flagElements:
            self.set_capped_end_to_elements(selection)
            self.replaced = False
            temp_dict = self.dict_group_elements.copy()
            for select, item in temp_dict.items():
                _, elements = item
                if self.typed_id == elements:
                    if self.replaced:
                        self.dkey = select
                        self.remove_elem_group()
                    else:
                        self.set_capped_end_to_elements(select)
                        self.replaced = True
                else:
                    count1, count2 = 0, 0
                    for element in self.typed_id:
                        if element in elements:
                            count1 += 1
                    fill_rate1 = count1/len(self.typed_id)

                    for element in elements:
                        if element in self.typed_id:
                            count2 += 1
                    fill_rate2 = count2/len(elements)
                    
                    if np.max([fill_rate1, fill_rate2])>0.5 :
                        if not self.replaced:
                            self.set_capped_end_to_elements(select)
                            self.replaced = True
                        else:
                            self.dkey = select
                            self.remove_elem_group()
                self.dkey = None 
        elif self.flagEntity:
            self.set_capped_end_to_lines(selection)
            self.replaced = False
            temp_dict = self.dict_group_lines.copy()
            for select, item in temp_dict.items():
                _, lines = item
                if self.typed_id == lines:
                    if self.replaced:
                        self.dkey = select
                        self.remove_line_group()
                    else:
                        self.set_capped_end_to_lines(select)
                        self.replaced = True
                self.dkey = None 
        
    def set_capped_end_to_elements(self, selection):
        
        self.project.set_capped_end_by_elements(self.typed_id, True, selection)
        if len(self.typed_id)>20:
            print("Set capped end correction to {} selected elements".format(len(self.typed_id)))
        else:
            print("Set capped end at elements: {}".format(self.typed_id))
        self.load_elements_info()

    def set_capped_end_to_lines(self, selection):
        self.project.set_capped_end_by_line(self.typed_id, True, selection)
        if len(self.typed_id)>20:
            print("Set capped end correction to {} selected lines".format(len(self.typed_id)))
        else:
            print("Set capped end to lines: {}".format(self.typed_id))
        self.load_lines_info()

    def set_capped_end_to_all_lines(self):
        message = None
        for select, item in self.dict_group_elements.items():
            _, elements = item
            self.project.mesh.set_capped_end_by_element(elements, None, select, delete_from_dict=False)
            key_strings = ["list of elements"]
            remove_bc_from_file([select], self.elements_info_path, key_strings, message)
        for select, item in self.dict_group_lines.items():
            _, lines = item
            self.project.mesh.set_capped_end_by_line(lines, None, select, delete_from_dict=False)
            self.remove_lines_from_file(select, message)

        selection = self.dict_label.format("Selection-{}".format(1))
        self.project.set_capped_end_by_line("all", True, selection)
        print("Set capped end correction to all lines")

        self.dict_group_elements = self.project.mesh.group_elements_with_capped_end
        self.dict_group_lines = self.project.mesh.group_lines_with_capped_end

        self.load_lines_info()
        self.load_elements_info()

    def load_elements_info(self):
        
        self.treeWidget_cappedEnd_elements.clear()
        for section, value in self.dict_group_elements.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(value[1])])
            self.treeWidget_cappedEnd_elements.addTopLevelItem(new)  

    def load_lines_info(self):
        
        self.treeWidget_cappedEnd_lines.clear()
        for section, value in self.dict_group_lines.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(value[1])])
            self.treeWidget_cappedEnd_lines.addTopLevelItem(new)           

    def on_click_item_elem(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        self.pushButton_remove_line.setDisabled(True)
        self.pushButton_get_information_line.setDisabled(True)
        self.pushButton_remove_elem.setDisabled(False)
        self.pushButton_get_information_elem.setDisabled(False)        

    def on_click_item_line(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        self.pushButton_remove_line.setDisabled(False)
        self.pushButton_get_information_line.setDisabled(False)
        self.pushButton_remove_elem.setDisabled(True)
        self.pushButton_get_information_elem.setDisabled(True)        

    def on_doubleclick_item_elem(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        if self.currentTab_ == 1:
            self.remove_elem_group()

    def on_doubleclick_item_line(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        if self.currentTab_ == 1:
            self.remove_line_group()

    def remove_elements(self, key, reset=False):
        section = key

        if not reset:
            group_label = section.split(" || ")[1]
            message = "The element length correction attributed to the {} of element(s) have been removed.".format(group_label)
        else:
            message = None
        
        elements = self.dict_group_elements[section][1]
        self.project.mesh.set_capped_end_by_element(elements, None, section, delete_from_dict=True)
        key_strings = ["list of elements"]
        remove_bc_from_file([section], self.elements_info_path, key_strings, message)
        self.load_elements_info()

    def remove_elem_group(self):
        if self.dkey is None:
            key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in self.lineEdit_elementID.text():
                self.remove_elements(key)
            self.lineEdit_elementID.setText("")
        else:
            self.remove_elements(self.dkey)

    def remove_lines(self, key, reset=False):
        section = key

        if not reset:
            group_label = section.split(" || ")[1]
            message = "The element length correction attributed to the {} of line(s) have been removed.".format(group_label)
        else:
            message = None

        lines = self.dict_group_lines[section][1]
        self.project.mesh.set_capped_end_by_line(lines, None, section, delete_from_dict=True)
        self.remove_lines_from_file(section, message)
        self.load_lines_info()

    def remove_line_group(self):
        if self.dkey is None:
            key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in self.lineEdit_elementID.text():
                self.remove_lines(key)
            self.lineEdit_elementID.setText("")
        else:
            self.remove_lines(self.dkey)

    def remove_lines_from_file(self, section, message):
        try:
            bc_removed = False
            config = configparser.ConfigParser()
            config.read(self.entity_path)

            for entity_id in config.sections():
                keys = list(config[entity_id].keys())
                if 'capped end' in keys:
                    if config[entity_id]['capped end'] == section:
                        config[entity_id]['capped end'] = ''
                        bc_removed = True
            
            with open(self.entity_path, 'w') as config_file:
                config.write(config_file)
            
            if message is not None and bc_removed:
                info_messages(message)
        
        except Exception as e:
            error(str(e))
    
    # def remove_all_element_capped_end(self):
    #     temp_dict_groups = self.dict_group_elements.copy()
    #     keys = temp_dict_groups.keys()
    #     for key in keys:
    #         self.remove_function(key, reset=True)
    #     info_messages("The element length correction of all elements has been removed.", title=">>> WARNING <<<")

    def get_information_elem(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                values = self.dict_group_elements[selected_key]
                GetInformationOfGroup(values, "Elements")
            else:
                error("Please, select a group in the list to get the information.", title="ERROR IN GROUP SELECTION")
                return
        except Exception as e:
            error(str(e), title="ERROR WHILE GETTING INFORMATION OF SELECTED GROUP")

    def get_information_line(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                values = self.dict_group_lines[selected_key]
                GetInformationOfGroup(values, "Lines")
            else:
                error("Please, select a group in the list to get the information.", title="ERROR IN GROUP SELECTION")
                return
        except Exception as e:
            error(str(e), title="ERROR WHILE GETTING INFORMATION OF SELECTED GROUP")


class GetInformationOfGroup(QDialog):
    def __init__(self, values, line_or_elem, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/getInformationOfGroupInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.type = line_or_elem
        self.list_of_elements = values[1]

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
            if self.type:
                new = QTreeWidgetItem([str(element), "capped end"])
                self.treeWidget_length_correction_group_info.addTopLevelItem(new)
            else:
                pass
    
    def force_to_close(self):
        self.close()

    