from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
import numpy as np

from pulse import app, UI_DIR
from pulse.tools.utils import remove_bc_from_file
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class CappedEndInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "model/setup/structural/capped_end_input.ui", self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.opv = self.main_window.opv_widget
        self.opv.setInputObject(self)    

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_treeWidgets_info()
        self.update()
        self.exec()

    def _initialize(self):

        self.file = self.project.file
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.lines_id = self.opv.getListPickedLines()
        self.elements_id = self.opv.getListPickedElements()
        self.structural_elements = self.preprocessor.structural_elements
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity
    
        self.dictkey_to_remove = None
        self.elements_info_path = self.project.file._element_info_path
        self.entity_path = self.project.file._entity_path
        self.dictKey_label = "CAPPED END || {}"
   
        self.project_lines = {}
        for line in self.preprocessor.all_lines:
            self.project_lines[line] = True
        
        self.complete = False

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selection = self.findChild(QComboBox, 'comboBox_selection')
        # QLabel
        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')       
        # QLineEdit
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        # QRadioButton
        self.radioButton_enable_capped_end = self.findChild(QRadioButton, 'radioButton_enable_capped_end')
        self.radioButton_disable_capped_end = self.findChild(QRadioButton, 'radioButton_disable_capped_end')
        #QTabWidget
        self.tabWidget_capped_end = self.findChild(QTabWidget, 'tabWidget_capped_end')
        # QTreeWidget
        self.treeWidget_capped_end_elements = self.findChild(QTreeWidget, 'treeWidget_capped_end_elements')
        self.treeWidget_capped_end_elements.setColumnWidth(0, 100)
        self.treeWidget_capped_end_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_capped_end_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_capped_end_lines = self.findChild(QTreeWidget, 'treeWidget_capped_end_lines')
        self.treeWidget_capped_end_lines.setColumnWidth(0, 100)
        self.treeWidget_capped_end_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_capped_end_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)
        # QPushButton
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        #
        self.pushButton_get_information.setDisabled(True)
        self.pushButton_remove.setDisabled(True)

    def _create_connections(self):

        self.comboBox_selection.currentIndexChanged.connect(self.update_selection)

        self.pushButton_confirm.clicked.connect(self.set_capped_end)
        self.pushButton_reset.clicked.connect(self.check_reset)
        self.pushButton_remove.clicked.connect(self.remove_group)
        self.pushButton_get_information.clicked.connect(self.get_information)

        self.tabWidget_capped_end.currentChanged.connect(self.tab_event_update)
        self.tab_event_update()

        self.treeWidget_capped_end_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_capped_end_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)
        self.treeWidget_capped_end_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_capped_end_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)            

    def update(self):

        self.lines_id = self.opv.getListPickedLines()
        self.elements_id = self.opv.getListPickedElements()

        if self.lines_id != []:
            self.label_selected_id.setText("Lines IDs:")
            self.write_ids(self.lines_id)
            self.comboBox_selection.setCurrentIndex(1)
            self.update_capped_end_buttons()

        elif self.elements_id != []:
            self.label_selected_id.setText("Elements IDs:")
            self.write_ids(self.elements_id)
            self.comboBox_selection.setCurrentIndex(2)
            
        else:
            self.label_selected_id.setText("Lines IDs:")
            self.lineEdit_selected_ID.setText("All lines")
            self.comboBox_selection.setCurrentIndex(0)

    def update_capped_end_buttons(self):
        if len(self.lines_id) != 0:
            entity = self.preprocessor.dict_tag_to_entity[self.lines_id[0]]
            if entity.capped_end is not None:
                if entity.capped_end:
                    self.radioButton_enable_capped_end.setChecked(True)
                else:
                    self.radioButton_disable_capped_end.setChecked(True)

    def tab_event_update(self):
        self.lineEdit_selected_ID.setEnabled(True)
        selection_index = self.comboBox_selection.currentIndex()
        tab_index = self.tabWidget_capped_end.currentIndex()
        if tab_index == 0:
            if selection_index == 2:
                text = "Elements IDs:"
                self.write_ids(self.elements_id)
            elif selection_index == 1:
                text = "Lines IDs:"
                self.write_ids(self.lines_id)
            elif selection_index == 0:
                text = "Lines IDs:"
                self.lineEdit_selected_ID.setText("All lines")
                self.lineEdit_selected_ID.setEnabled(False)
        elif tab_index == 1:
            text = "Group:"
            self.lineEdit_selected_ID.setText("")
            self.lineEdit_selected_ID.setDisabled(True)
            self.pushButton_remove.setDisabled(True)
            self.pushButton_get_information.setDisabled(True)
        self.label_selected_id.setText(text)

    def update_selection(self):
        self.tab_event_update()
        self.update_renders()

    def update_renders(self):
        selection_index = self.comboBox_selection.currentIndex()
        if selection_index in [0, 1]:
            self.opv.changePlotToEntities()
        else:
            self.opv.changePlotToMesh()

    def load_elements_info(self):
        self.treeWidget_capped_end_elements.clear()
        for section, elements in self.preprocessor.group_elements_with_capped_end.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(elements)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_capped_end_elements.addTopLevelItem(new)  

    def load_lines_info(self):        
        self.treeWidget_capped_end_lines.clear()
        lines = self.preprocessor.lines_with_capped_end
        if len(lines) != 0:
            new = QTreeWidgetItem(["Enabled lines" , str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_capped_end_lines.addTopLevelItem(new)       

    def load_treeWidgets_info(self):

        self.load_lines_info()
        self.load_elements_info()

        if len(self.preprocessor.lines_with_capped_end):
            self.tabWidget_capped_end.setTabVisible(1, True)
            return
        
        if len(self.preprocessor.group_elements_with_capped_end):
            self.tabWidget_capped_end.setTabVisible(1, True)
            return
        
        self.tabWidget_capped_end.setTabVisible(1, False)

    def on_click_item_elem(self, item):
        self.lineEdit_selected_ID.setText(item.text(0))
        self.label_selected_id.setText("Group ID:")
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove.setDisabled(False)
        self.pushButton_get_information.setDisabled(True)      

    def on_click_item_line(self, item):
        text = item.text(1).replace("[","")
        text = text.replace("]","")
        self.lineEdit_selected_ID.setText(text)
        self.label_selected_id.setText("Line IDs:")
        self.lineEdit_selected_ID.setDisabled(True)
        self.pushButton_remove.setDisabled(False)
        self.pushButton_get_information.setDisabled(False)   

    def on_doubleclick_item_elem(self, item):
        self.lineEdit_selected_ID.setText(item.text(0))
        if self.tabWidget_capped_end.currentIndex() == 1:
            self.remove_elem_group()

    def on_doubleclick_item_line(self, item):
        self.lineEdit_selected_ID.setText(item.text(1))
        if self.tabWidget_capped_end.currentIndex() == 1:
            self.remove_line_group()

    def set_capped_end(self):
        selection_index = self.comboBox_selection.currentIndex() 
        if selection_index == 0:
            self.set_capped_end_to_all_lines()
            print("Set capped end correction to all lines.")

        elif selection_index == 1:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True      

            self.set_capped_end_to_lines()
            self.replaced = False

            if len(self.lines_typed)>20:
                print("Set capped end correction to {} selected lines".format(len(self.lines_typed)))
            else:
                print("Set capped end to lines: {}".format(self.lines_typed))

        elif selection_index == 2:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
            if self.stop:
                return

            size = len(self.preprocessor.group_elements_with_capped_end)
            selection = self.dictKey_label.format("Selection-{}".format(size+1))
            self.set_capped_end_to_elements(selection)
            self.replaced = False

            # checking the oversampling of elements in each group of elements
            if size > 0:
                temp_dict = self.preprocessor.group_elements_with_capped_end.copy()
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
            
        self.complete = True
        self.close()
        
    def remove_elements(self, key):
        section = key        
        elements = self.preprocessor.group_elements_with_capped_end[section]
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
        lines = self.preprocessor.lines_with_capped_end.copy()
        self.project.set_capped_end_by_lines(lines, False)
        self.load_lines_info()
        self.lineEdit_selected_ID.setText("")

    def remove_group(self):
        if self.lineEdit_selected_ID.text() != "":
            label = self.label_selected_id.text()
            if label == "Group ID:":
                self.remove_elem_group()
            elif label == "Line IDs:":
                self.remove_line_group()
            self.load_treeWidgets_info()
        
    def set_capped_end_to_elements(self, group_label):
        capped_end = self.radioButton_enable_capped_end.isChecked()
        self.project.set_capped_end_by_elements(self.elements_typed, 
                                                capped_end, 
                                                group_label)
        self.load_elements_info()

    def set_capped_end_to_lines(self):
        capped_end = self.radioButton_enable_capped_end.isChecked()
        self.project.set_capped_end_by_lines(self.lines_typed, capped_end)
        self.load_lines_info()

    def set_capped_end_to_all_lines(self):
        lines = self.preprocessor.all_lines
        capped_end = self.radioButton_enable_capped_end.isChecked()
        self.project.set_capped_end_by_lines(lines, capped_end)
        self.load_lines_info()
        self.load_elements_info()

    def check_reset(self):
        temp_dict_group_elements = self.preprocessor.group_elements_with_capped_end.copy()
        for key, elements in temp_dict_group_elements.items():
            self.project.set_capped_end_by_elements(elements, False, key)
        lines = self.preprocessor.all_lines
        self.project.set_capped_end_by_lines(lines, False)
        self.load_elements_info()
        self.load_lines_info()
        self.lineEdit_selected_ID.setText("")
        title = "CAPPED END RESET"
        message = "The capped end effect has been removed \nfrom all elements of the structural model."
        PrintMessageInput([window_title_2, title, message])
    
    def get_information(self):
        label = self.label_selected_id.text()
        if label == "Group ID:":
            self.get_information_elem()
        elif label == "Line IDs:":
            self.get_information_line()

    def get_information_elem(self):
        try:
            selected_id = self.lineEdit_selected_ID.text()
            selected_key = self.dictKey_label.format(selected_id)
            if "Selection-" in selected_key:
                values = self.preprocessor.group_elements_with_capped_end[selected_key]
                GetInformationOfGroup(values, "Elements")
            else:
                title = "UNSELECTED GROUP OF ELEMENTS"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                  
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([window_title_1, title, message])

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

    def get_information_line(self):
        try:
            if self.lineEdit_selected_ID.text() != "":
                list_lines = self.get_list_typed_entries()            
                read = GetInformationOfGroup(list_lines, "Lines")
                if read.lines_removed:
                    self.load_lines_info()
            else:
                title = "UNSELECTED GROUP OF LINES"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.set_capped_end()
        elif event.key() == Qt.Key_Delete:
            self.remove_group()
        elif event.key() == Qt.Key_Escape:
            self.close()