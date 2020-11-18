from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np

from pulse.utils import remove_bc_from_file
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR"
window_title2 = "WARNING"

class CappedEndInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/cappedEndInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.lines_id = self.opv.getListPickedEntities()
        self.elements_id = self.opv.getListPickedElements()

        self.structural_elements = self.project.mesh.structural_elements
        self.dict_tag_to_entity = self.project.mesh.get_dict_of_entities()
        self.entities = self.project.mesh.entities
        self.complete = False
        self.info_text = ["NO MESSAGE", "No message", "NO MESSAGE"]

        self.project_lines = {}
        for line in self.project.mesh.all_lines:
            self.project_lines[line] = True

        self.dict_group_elements = project.mesh.group_elements_with_capped_end
        self.dict_group_lines = project.mesh.group_lines_with_capped_end
        self.lines_with_capped_end = project.mesh.lines_with_capped_end
    
        self.dictkey_to_remove = None
        self.elements_info_path = project.file._element_info_path
        self.entity_path = project.file._entity_path
        self.dictKey_label = "CAPPED END || {}"

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_id_labels = self.findChild(QLineEdit, 'lineEdit_id_labels')

        self.radioButton_all_lines = self.findChild(QRadioButton, 'radioButton_all_lines')
        self.radioButton_all_lines.toggled.connect(self.radioButtonEvent)

        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)

        self.radioButton_selected_elements = self.findChild(QRadioButton, 'radioButton_selected_elements')
        self.radioButton_selected_elements.toggled.connect(self.radioButtonEvent)
        
        self.radioButton_enable_cappedEnd = self.findChild(QRadioButton, 'radioButton_enable_cappedEnd')
        self.radioButton_enable_cappedEnd.toggled.connect(self.radioButtonEvent_enable_disable)
        self.radioButton_disable_cappedEnd = self.findChild(QRadioButton, 'radioButton_disable_cappedEnd')
        self.radioButton_disable_cappedEnd.toggled.connect(self.radioButtonEvent_enable_disable)
        self.flag_cappedEnd_enable = self.radioButton_enable_cappedEnd.isChecked()

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()

        self.treeWidget_cappedEnd_elements = self.findChild(QTreeWidget, 'treeWidget_cappedEnd_elements')
        self.treeWidget_cappedEnd_elements.setColumnWidth(0, 100)
        self.treeWidget_cappedEnd_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_cappedEnd_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)
        self.treeWidget_cappedEnd_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_cappedEnd_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.treeWidget_cappedEnd_lines = self.findChild(QTreeWidget, 'treeWidget_cappedEnd_lines')
        self.treeWidget_cappedEnd_lines.setColumnWidth(0, 100)
        self.treeWidget_cappedEnd_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_cappedEnd_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)
        self.treeWidget_cappedEnd_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_cappedEnd_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)

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
        self.pushButton_confirm.clicked.connect(self.check_capped_end)

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        self.pushButton_reset_all.clicked.connect(self.check_reset_all)

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
            self.lineEdit_selected_ID.setEnabled(False)

        if self.elements_id != []:
            self.write_ids(self.elements_id)

        self.load_lines_info()
        self.load_elements_info()
        self.update_buttons_()
        self.tabEvent_()
        self.exec_()

    def update_buttons_(self):
        self.pushButton_get_information_elem.setDisabled(True)
        self.pushButton_get_information_line.setDisabled(True)
        self.pushButton_remove_elem.setDisabled(True)
        self.pushButton_remove_line.setDisabled(True)        

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

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_capped_end()
        # elif event.key() == Qt.Key_Delete:
        #     self.remove_cappedEnd_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()
        
    def radioButtonEvent(self):

        self.flagAll = self.radioButton_all_lines.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.flagElements = self.radioButton_selected_elements.isChecked()
        self.flagcappedEnd = self.radioButton_enable_cappedEnd.isChecked()
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

    def radioButtonEvent_enable_disable(self):
        self.flag_cappedEnd_enable = self.radioButton_enable_cappedEnd.isChecked()

    def load_elements_info(self):
        self.treeWidget_cappedEnd_elements.clear()
        for section, elements in self.dict_group_elements.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(elements)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_cappedEnd_elements.addTopLevelItem(new)  

    def load_lines_info(self):        
        self.treeWidget_cappedEnd_lines.clear()
        lines = self.project.mesh.lines_with_capped_end
        if len(lines) != 0:
            new = QTreeWidgetItem(["Enabled lines" , str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_cappedEnd_lines.addTopLevelItem(new)           

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
        if self.lineEdit_selected_ID.text() == "":
            return []
        tokens = self.lineEdit_selected_ID.text().strip().split(',')
        try:
            tokens.remove('')
        except:     
            pass
        output = list(map(int, tokens))
        return output

    def check_input_elements(self):
        
        try:
            if self.lineEdit_selected_ID.text() == "":
                title = "Error: empty Element ID input"
                message = "Inform a valid Element ID before to confirm the input!"
                self.info_text = [title, message, window_title1]
                return True
            self.elements_typed = np.sort(self.get_list_typed_entries()).tolist()
        except Exception:
            title = "Error: invalid Element ID input"
            message = "Wrong input for Element ID's!"
            self.info_text = [title, message, window_title1]
            return True

        try:
            for _element_id in self.elements_typed:
                self.elementID = self.structural_elements[_element_id].index
        except:
            title = "Error: invalid Element ID input"
            message = "The Element ID input values must be \nmajor than 1 and less than {}.".format(len(self.structural_elements))
            self.info_text = [title, message, window_title1]
            return True
        return False

    def check_input_lines(self):
        
        try:
            if self.lineEdit_selected_ID.text() == "":
                title = "Error: empty Line ID input"
                message = "Inform a valid Line ID before \nto confirm the input.."
                self.info_text = [title, message, window_title1]
                return True
            self.lines_typed = self.get_list_typed_entries()
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

    def check_capped_end(self):

        if self.flagAll:
            self.set_capped_end_to_all_lines()
            print("Set capped end correction to all lines.")

        elif self.flagElements:
            if self.check_input_elements():
                PrintMessageInput(self.info_text)
                return

            size = len(self.project.mesh.group_elements_with_capped_end)
            selection = self.dictKey_label.format("Selection-{}".format(size+1))
            self.set_capped_end_to_elements(selection)
            self.replaced = False

            # checking the oversampling of elements in each group of elements
            if size > 0:
                temp_dict = self.dict_group_elements.copy()
                for select, elements in temp_dict.items():
                    if list(np.sort(self.elements_typed)) == list(np.sort(elements)):
                        if self.replaced:
                            self.dictkey_to_remove = select
                            self.remove_elem_group()
                        else:
                            self.set_capped_end_to_elements(select)
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
                                self.dictkey_to_remove = select
                                self.remove_elem_group()
                            else:
                                self.set_capped_end_to_elements(select)
                                self.replaced = True
                    self.dictkey_to_remove = None 

            if len(self.elements_typed)>20:
                print("Set capped end correction to {} selected elements".format(len(self.elements_typed)))
            else:
                print("Set capped end at elements: {}".format(self.elements_typed))
        
        elif self.flagEntity:
            if self.check_input_lines():
                PrintMessageInput(self.info_text)
                return

            self.set_capped_end_to_lines()
            self.replaced = False

            if len(self.lines_typed)>20:
                print("Set capped end correction to {} selected lines".format(len(self.lines_typed)))
            else:
                print("Set capped end to lines: {}".format(self.lines_typed))
            
        self.complete = True
        self.close()
        
    def remove_elements(self, key, reset=False):
        section = key        
        elements = self.dict_group_elements[section]
        self.project.set_capped_end_by_elements(elements, False, section)
        self.load_elements_info()
        group_label = section.split(" || ")[1]
        print("The element capped end enabled to the {} of element(s) have been removed.".format(group_label))

    def remove_elem_group(self):
        if self.dictkey_to_remove is None:
            text = self.lineEdit_selected_ID.text()
            key = self.dictKey_label.format(text)
            self.remove_elements(key)
            self.lineEdit_selected_ID.setText("")
        else:
            self.remove_elements(self.dictkey_to_remove)

    def remove_line_group(self):
        lines = self.project.mesh.lines_with_capped_end.copy()
        self.project.set_capped_end_by_line(lines, False)
        self.load_lines_info()
        self.lineEdit_selected_ID.setText("")
    
    def set_capped_end_to_elements(self, selection):
        self.project.set_capped_end_by_elements(self.elements_typed, self.flag_cappedEnd_enable, selection)
        self.load_elements_info()

    def set_capped_end_to_lines(self):
        self.project.set_capped_end_by_line(self.lines_typed, self.flag_cappedEnd_enable)
        self.load_lines_info()

    def set_capped_end_to_all_lines(self):
        self.project.set_capped_end_by_line("all", True)
        self.load_lines_info()
        self.load_elements_info()

    def check_reset_all(self):
        temp_dict_group_elements = self.dict_group_elements.copy()
        for key, elements in temp_dict_group_elements.items():
            self.project.set_capped_end_by_elements(elements, False, key)
        self.project.set_capped_end_by_line("all", False)
        self.load_elements_info()
        self.load_lines_info()
        self.lineEdit_selected_ID.setText("")
        title = "CAPPED END RESET"
        message = "The capped end effect has been removed \nfrom all elements of the structural model."
        PrintMessageInput([title, message, window_title2])
    
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
            uic.loadUi('pulse/uix/user_input/ui/getGroupInformationInput.ui', self)
            self.flagElements = True
            self.flagLines = False

        elif label == "Lines":
            uic.loadUi('pulse/uix/user_input/ui/getGroupInformationAndRemoveInput.ui', self)
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
        self.list_of_values = values
        self.project = project

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, self.label)
        self.treeWidget_group_info.headerItem().setText(1, "Capped end")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        
        self.treeWidget_group_info.setColumnWidth(0, 80)
        self.treeWidget_group_info.setColumnWidth(1, 140)
        self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.load_group_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Delete:
            self.check_remove()

    def on_click_item_(self, item):
        text = item.text(0)
        self.lineEdit_selected_ID.setText(text)
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def check_remove(self):
        if self.flagLines:
            if self.lineEdit_selected_ID.text() != "":
                line = int(self.lineEdit_selected_ID.text())
                if line in self.list_of_values:
                    self.list_of_values.remove(line)
                self.project.set_capped_end_by_line(line, False)
                self.load_group_info()
                self.lines_removed = True
        self.lineEdit_selected_ID.setText("")

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        for value in self.list_of_values:
            new = QTreeWidgetItem([str(value), "Enabled"])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)

    def force_to_close(self):
        self.close()

    