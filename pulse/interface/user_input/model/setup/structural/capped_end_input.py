from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup

import numpy as np
from collections import defaultdict


window_title_1 = "Error"
window_title_2 = "Warning"

class CappedEndInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/capped_end_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)    

        self.main_window = app().main_window
        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.selection_callback()
        self.load_treeWidgets_info()
        self.exec()

    def _initialize(self):

        self.file = self.project.file
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.lines_id = app().main_window.list_selected_lines()
        self.elements_id = app().main_window.list_selected_elements()

        self.structural_elements = self.preprocessor.structural_elements
    
        self.dictkey_to_remove = None
        self.elements_info_path = self.project.file._element_info_path
        self.entity_path = self.project.file._pipeline_path
        self.dictKey_label = "CAPPED END || {}"
   
        self.project_lines = {}
        for line in self.model.mesh.lines_from_model.keys():
            self.project_lines[line] = True
        
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_capped_end : QComboBox
        self.comboBox_selection : QComboBox

        # QLabel
        self.label_attribute_to : QLabel
        self.label_selected_id : QLabel     

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_remove : QPushButton

        #QTabWidget
        self.tabWidget_main : QTabWidget
        self.tabWidget_groups : QTabWidget

        # QTreeWidget
        self.treeWidget_capped_end_elements : QTreeWidget
        self.treeWidget_capped_end_lines : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_selection.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_confirm.clicked.connect(self.set_capped_end)
        self.pushButton_reset.clicked.connect(self.check_reset)
        self.pushButton_remove.clicked.connect(self.remove_group)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_update)
        #
        self.treeWidget_capped_end_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_capped_end_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)
        self.treeWidget_capped_end_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_capped_end_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        line_ids = app().main_window.list_selected_lines()
        element_ids = app().main_window.list_selected_elements()

        selection_index = self.comboBox_selection.currentIndex()

        if line_ids:
            selected_ids = line_ids
            if selection_index == 1:
                self.selection_type_callback()
            else:
                self.comboBox_selection.setCurrentIndex(1)
            self.update_capped_end_effect_by_lines_selection()

        elif element_ids:
            selected_ids = element_ids
            if selection_index == 2:
                self.selection_type_callback()
            else:
                self.comboBox_selection.setCurrentIndex(2)
            self.update_capped_end_effect_by_elements_selection()
        
        else:
            return

        self.write_ids(selected_ids)

    def selection_type_callback(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)

        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        elif selection_index == 1:
            selected_lines = app().main_window.list_selected_lines()
            if selected_lines:
                self.write_ids(selected_lines)

        elif selection_index == 2:
            selected_elements = app().main_window.list_selected_elements()
            if selected_elements:
                self.write_ids(selected_elements)

    def write_ids(self, selected_ids):
        text = ", ".join([str(i) for i in selected_ids])
        self.lineEdit_selected_id.setText(text)   

    def tab_event_update(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)

        if self.tabWidget_main.currentIndex() == 0:
            self.label_attribute_to.setDisabled(False)
            self.label_selected_id.setText("Selected IDs:")
            self.comboBox_selection.setDisabled(False)
            self.selection_callback()

        else:
            self.label_attribute_to.setDisabled(True)
            self.label_selected_id.setText("Group:")
            self.lineEdit_selected_id.setDisabled(True)
            self.comboBox_selection.setDisabled(True)
            self.comboBox_selection.setCurrentIndex(0)

        self.update_renders()

    def _config_widgets(self):
        #
        self.lineEdit_selected_id.setText("All lines")
        self.lineEdit_selected_id.setEnabled(False)
        self.pushButton_remove.setDisabled(True)
        #
        self.treeWidget_capped_end_elements.setColumnWidth(0, 100)
        self.treeWidget_capped_end_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_capped_end_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.treeWidget_capped_end_lines.setColumnWidth(0, 100)
        self.treeWidget_capped_end_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_capped_end_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")   

    def update_capped_end_effect_by_elements_selection(self):
        if len(self.elements_id) == 1:
            element = self.preprocessor.structural_elements[self.elements_id[0]]
            if element.capped_end:
                self.comboBox_capped_end.setCurrentIndex(0)
            else:
                self.comboBox_capped_end.setCurrentIndex(1)

    def update_capped_end_effect_by_lines_selection(self):
        if len(self.lines_id) == 1:
            line = self.model.mesh.lines_from_model[self.lines_id[0]]
            if line.capped_end:
                self.comboBox_capped_end.setCurrentIndex(0)
            else:
                self.comboBox_capped_end.setCurrentIndex(1)

    def update_renders(self):
        app().main_window.update_plots()
        if self.comboBox_selection.currentIndex() == 2:
            app().main_window.plot_mesh()
        else:
            app().main_window.plot_lines_with_cross_sections()

            self.process_lines_with_capped_end()
        self.treeWidget_capped_end_lines.clear()
        self.tabWidget_groups.setTabVisible(1, False)

    def process_elements_with_capped_end(self):
        self.capped_end_mapping_for_elements = defaultdict(list)
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "capped_end":
                if data["enable"]:
                    self.capped_end_mapping_for_elements["Enabled"].append(element_id)

    def load_elements_info(self):

        self.process_elements_with_capped_end()
        self.treeWidget_capped_end_elements.clear()
        self.tabWidget_groups.setTabVisible(0, False)

        if self.capped_end_mapping_for_elements:
            element_ids = self.capped_end_mapping_for_elements["Enabled"]
            new = QTreeWidgetItem(["Enabled", str(element_ids)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_capped_end_elements.addTopLevelItem(new)

    def process_lines_with_capped_end(self):
        self.capped_end_mapping_for_lines = defaultdict(list)
        for line_id, data in self.properties.line_properties.items():
            if "capped_end" in data.keys():
                self.capped_end_mapping_for_lines["Enabled"].append(line_id)

    def load_lines_info(self):

        self.process_lines_with_capped_end()
        self.treeWidget_capped_end_lines.clear()
        self.tabWidget_groups.setTabVisible(1, False)

        if self.capped_end_mapping_for_lines:
            line_ids = self.capped_end_mapping_for_lines["Enabled"]
            new = QTreeWidgetItem(["Enabled" , str(line_ids)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_capped_end_lines.addTopLevelItem(new)

    def load_treeWidgets_info(self):

        self.load_lines_info()
        self.load_elements_info()
        self.tabWidget_main.setTabVisible(1, False)

        if self.capped_end_mapping_for_lines:
            self.tabWidget_main.setTabVisible(1, True)
            self.tabWidget_groups.setTabVisible(1, True)

        if self.capped_end_mapping_for_elements:
            self.tabWidget_main.setTabVisible(1, True)
            self.tabWidget_groups.setTabVisible(0, True)

    def on_click_item_elem(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_click_item_line(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False) 

    def on_doubleclick_item_elem(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.get_information(item)

    def on_doubleclick_item_line(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.get_information(item)

    def set_capped_end(self):
        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 0:
            self.set_capped_end_to_all_lines()
            print("The capped end effect was defined to all lines.")

        elif selection_index == 1:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True      

            self.set_capped_end_to_lines()
            self.replaced = False

            if len(self.lines_typed) > 20:
                print(f"Set capped end correction to {len(self.lines_typed)} selected lines")
            else:
                print(f"Set capped end to lines: {self.lines_typed}")

        elif selection_index == 2:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.elements_typed = self.before_run.check_selected_ids(lineEdit, "elements")
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
                        
                        if np.max([fill_rate1, fill_rate2]) > 0.5 :
                            if self.replaced:
                                self.dictkey_to_remove = select
                                self.remove_elem_group()
                            else:
                                self.set_capped_end_to_elements(select)
                                self.replaced = True
                    self.dictkey_to_remove = None 

            if len(self.elements_typed) > 20:
                print(f"Set capped end correction to {len(self.elements_typed)} selected elements")
            else:
                print(f"Set capped end at elements: {self.elements_typed}")
            
        self.complete = True
        self.close()
        
    def remove_elements(self, key):
        section = key        
        elements = self.preprocessor.group_elements_with_capped_end[section]
        self.project.set_capped_end_by_elements(elements, False, section)
        self.load_elements_info()
        group_label = section.split(" || ")[1]
        print(f"The element capped end enabled to the {group_label} of element(s) has been removed.")

    def remove_elem_group(self):
        if self.dictkey_to_remove is None:
            text = self.lineEdit_selected_id.text()
            key = self.dictKey_label.format(text)
            self.remove_elements(key)
            self.lineEdit_selected_id.setText("")
        else:
            self.remove_elements(self.dictkey_to_remove)

    def remove_line_group(self):
        line_ids = self.capped_end_mapping_for_lines["Enabled"]
        self.preprocessor.set_capped_end_by_lines(line_ids, False)
        self.load_lines_info()
        self.lineEdit_selected_id.setText("")

    def remove_group(self):
        if self.lineEdit_selected_id.text() != "":

            index = self.tabWidget_groups.currentIndex()
            if index == 0:
                self.remove_elem_group()
            else:
                self.remove_line_group()

            self.load_treeWidgets_info()
            if not self.tabWidget_main.isTabVisible(1):
                if self.comboBox_selection.currentIndex() == 0:
                    self.selection_type_callback()
                else:
                    self.comboBox_selection.setCurrentIndex(0)

    def get_capped_end(self):
        if self.comboBox_capped_end.currentIndex() == 0:
            return True
        else:
            return False

    def set_capped_end_to_elements(self, group_label):
        capped_end = self.get_capped_end()
        self.project.set_capped_end_by_elements(self.elements_typed, 
                                                capped_end, 
                                                group_label)
        self.load_elements_info()

    def set_capped_end_to_lines(self):
        capped_end = self.get_capped_end()
        self.project.set_capped_end_by_lines(self.lines_typed, capped_end)
        self.load_lines_info()

    def set_capped_end_to_all_lines(self):
        lines = list(self.model.mesh.lines_from_model.keys())
        capped_end = self.get_capped_end()
        self.project.set_capped_end_by_lines(lines, capped_end)
        self.load_lines_info()
        self.load_elements_info()

    def check_reset(self):

        aux_dict = self.preprocessor.group_elements_with_capped_end.copy()
        for key, elements in aux_dict.items():
            self.project.set_capped_end_by_elements(elements, False, key)

        lines = list(self.model.mesh.lines_from_model.keys())
        self.project.set_capped_end_by_lines(lines, False)

        self.load_treeWidgets_info()
        if self.comboBox_selection.currentIndex() == 0:
            self.selection_type_callback()
        else:
            self.comboBox_selection.setCurrentIndex(0)

        title = "Resetting process complete"
        message = "The capped end effect has been removed from all elements of the structural model."
        PrintMessageInput([window_title_2, title, message], auto_close=True)
    
    def get_information(self, item):
        if self.tabWidget_groups.currentIndex() == 0:
            self.get_information_elem(item)
        else:
            self.get_information_line(item)

    def get_information_elem(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                selected_id = item.text(0)
                selected_key = self.dictKey_label.format(selected_id)

                if "Selection-" in selected_key:
                    elements_of_group = self.preprocessor.group_elements_with_capped_end[selected_key]

                    data = dict()
                    for element in elements_of_group:
                        data[element] = ["Enabled"]

                    if len(data):
                        self.close()
                        header_labels = ["Elements", "Capped end effect"]
                        GetInformationOfGroup(  group_label = "Capped end effect",
                                                selection_label = "Element ID:",
                                                header_labels = header_labels,
                                                column_widths = [100, 140],
                                                data = data  )

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def get_information_line(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                data = dict()
                for line in self.get_list_typed_entries(item.text(1)):
                    data[line] = ["Enabled"]

                if len(data):
                    self.close()
                    header_labels = ["Lines", "Capped end effect"]
                    GetInformationOfGroup(  group_label = "Capped end effect",
                                            selection_label = "Line ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 140],
                                            data = data  )

                # read = GetInformationOfGroup(values=list_lines, label="Line")
                # if read.lines_removed:
                #     self.load_lines_info()

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def get_list_typed_entries(self, str_list):
        tokens = str_list[1:-1].strip().split(',')
        try:
            tokens.remove('')
        except:     
            pass
        output = list(map(int, tokens))
        return output

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.set_capped_end()
        elif event.key() == Qt.Key_Delete:
            self.remove_group()
        elif event.key() == Qt.Key_Escape:
            self.close()