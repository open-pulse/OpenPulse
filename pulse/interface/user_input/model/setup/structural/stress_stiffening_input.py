from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class StressStiffeningInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/stress_stiffening_input.ui"
        uic.loadUi(ui_path, self)
        
        app().main_window.set_input_widget(self)
        self.project = app().project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_treeWidgets_info()
        self.update()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.lines_id = app().main_window.list_selected_lines()
        self.elements_id = app().main_window.list_selected_elements()

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.structural_elements = self.preprocessor.structural_elements
        self.lines_from_model = self.preprocessor.lines_from_model

        # self.dict_group_elements = self.preprocessor.group_elements_with_stress_stiffening
        self.lines_with_stress_stiffening = self.preprocessor.lines_with_stress_stiffening
        self.dict_lines_with_stress_stiffening = self.preprocessor.dict_lines_with_stress_stiffening

        self.stop = False
        self.error_label = ""
        self.dictKey_label = "STRESS STIFFENING || {}"
        self.dictkey_to_remove = None

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selection : QComboBox
        # QLabel
        self.label_attribute_to : QLabel
        self.label_selected_id : QLabel
        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_external_pressure : QLineEdit
        self.lineEdit_internal_pressure : QLineEdit
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_remove : QPushButton
        # QTabWidget
        self.tabWidget_groups : QTabWidget
        self.tabWidget_main : QTabWidget
        # QTreeWidget
        self.treeWidget_stress_stiffening_elements : QTreeWidget
        self.treeWidget_stress_stiffening_lines : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_selection.currentIndexChanged.connect(self.selection_type_callback)
        #
        self.pushButton_remove.clicked.connect(self.remove_group)
        self.pushButton_confirm.clicked.connect(self.press_confirm)
        self.pushButton_reset.clicked.connect(self.check_reset_all)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_stress_stiffening_elements.itemClicked.connect(self.on_click_item_elem)
        self.treeWidget_stress_stiffening_elements.itemDoubleClicked.connect(self.on_doubleclick_item_elem)
        self.treeWidget_stress_stiffening_lines.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_stress_stiffening_lines.itemDoubleClicked.connect(self.on_doubleclick_item_line)

    def _config_widgets(self):
        #
        self.pushButton_remove.setDisabled(True)
        #
        self.treeWidget_stress_stiffening_elements.setColumnWidth(0, 100)
        self.treeWidget_stress_stiffening_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_stress_stiffening_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.treeWidget_stress_stiffening_lines.setColumnWidth(0, 100)
        self.treeWidget_stress_stiffening_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_stress_stiffening_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def selection_type_callback(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)
        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        elif selection_index == 1:
            if len(self.lines_id):
                self.write_ids(self.lines_id)

        elif selection_index == 2:
            if len(self.elements_id):
                self.write_ids(self.elements_id)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            selection_index  = self.comboBox_selection.currentIndex()
            
            if selection_index == 0:
                text = "Lines IDs:"
                self.lineEdit_selected_id.setText("All lines")

            elif selection_index == 1:
                text = "Lines IDs:"
                self.write_ids(self.lines_id)

            elif selection_index == 2:
                text = "Elements IDs:"
                self.write_ids(self.elements_id)

        elif tab_index == 1:
            text = "Group:"
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
 
        self.label_selected_id.setText(text)

    def on_click_item_elem(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_click_item_line(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False) 

    def on_doubleclick_item_elem(self, item):
        self.on_click_item_elem(item)
        self.get_information(item)

    def on_doubleclick_item_line(self, item):
        self.on_click_item_line(item)
        self.get_information(item)

    def get_list_typed_entries(self, str_list):
        tokens = str_list[1:-1].strip().split(',')
        try:
            tokens.remove('')
        except:     
            pass
        output = list(map(int, tokens))
        return output

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False):
        self.stop = False
        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if only_positive:
                    title = f"Invalid input to {label}"
                    message = f"Insert a positive value to the {label}."
                    if zero_included:
                        if out < 0:
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([window_title_1, title, message])
                            self.stop = True
                            return None
                    else:
                        if out <= 0:
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([window_title_1, title, message])
                            self.stop = True
                            return None
            except Exception as log_error:
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Wrong input for {label}.\n\n"
                message += str(log_error)
                PrintMessageInput([window_title_1, title, message])
                self.stop = True
                return None
        else:
            if zero_included:
                return float(0)
            else: 
                title = "INPUT CROSS-SECTION ERROR"
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([window_title_1, title, message])                   
                self.stop = True
                return None
        return out

    def press_confirm(self):

        external_pressure = self.check_inputs(self.lineEdit_external_pressure, "'External pressure'", zero_included=True)
        if self.stop:
            return

        internal_pressure = self.check_inputs(self.lineEdit_internal_pressure, "'Internal pressure'", zero_included=True)
        if self.stop:
            return
        
        if external_pressure == 0 and internal_pressure == 0:
            title = "Empty entries at the input pressure fields"
            message = f"You should to insert a value different from zero at the external or internal "
            message += "pressure field inputs to continue."
            PrintMessageInput([window_title_1, title, message])  
            return
        else:
            self.stress_stiffening_parameters = [external_pressure, internal_pressure]

        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 0:
            for line_id in self.lines_from_model.keys():
                self.project.set_stress_stiffening_by_line(line_id, self.stress_stiffening_parameters)

        elif selection_index == 1:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True                 

            for line_id in self.lines_typed:
                self.project.set_stress_stiffening_by_line(line_id, self.stress_stiffening_parameters)        

        if selection_index == 2:

            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
            if self.stop:
                return

            size = len(self.preprocessor.group_elements_with_stress_stiffening)
            section = self.dictKey_label.format("Selection-{}".format(size+1))
            self.set_stress_stiffening_to_elements(section)
            self.replaced = False

            # checking the oversampling of elements in each group of elements
            if size > 0:
                temp_dict = self.preprocessor.group_elements_with_stress_stiffening.copy()
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

        self.complete = True
        self.close()        

    def set_stress_stiffening_to_elements(self, section):
        self.project.set_stress_stiffening_by_elements(self.elements_typed, 
                                                       self.stress_stiffening_parameters, 
                                                       section)
        self.load_elements_info()

    def check_reset_all(self):

        for line_id in self.preprocessor.all_lines:
            self.project.set_stress_stiffening_by_line(line_id, [0,0,0,0], remove=True)

        temp_dict = self.preprocessor.group_elements_with_stress_stiffening.copy()
        for key, item in temp_dict.items():
            self.project.set_stress_stiffening_by_elements(item[1], item[0], key, remove=True)

        self.preprocessor.stress_stiffening_enabled = False
        self.lineEdit_selected_id.setText("")
        self.load_treeWidgets_info()

        title = "Stress stiffening resetting process complete"
        message = "The stress stiffening applied to all lines has "
        message += "been removed from FE model."
        PrintMessageInput([window_title_2, title, message], auto_close=True)

    def remove_elements(self, key):
        section = key        
        list_data = self.preprocessor.group_elements_with_stress_stiffening[section]
        elements = list_data[1]
        self.project.set_stress_stiffening_by_elements(elements, [0,0,0,0], section, remove=True)
        self.load_elements_info()
        group_label = section.split(" || ")[1]
        #
        title = "Stress stiffening removal process complete"
        message = f"The stress stiffening effects of {group_label} group "
        message += "have been removed from FE model."
        PrintMessageInput([window_title_2, title, message], auto_close=True)

    def remove_elem_group(self):
        if self.dictkey_to_remove is None:
            text = self.lineEdit_selected_id.text()
            key = self.dictKey_label.format(text)
            self.remove_elements(key)
            self.lineEdit_selected_id.setText("")
        else:
            self.remove_elements(self.dictkey_to_remove)

    def remove_line_group(self):
        parameters = [0,0,0,0]
        lines = self.preprocessor.lines_with_stress_stiffening.copy()
        self.project.set_stress_stiffening_by_line(lines, parameters, remove=True)
        self.load_lines_info()
        self.lineEdit_selected_id.setText("")
        #
        title = "Stress stiffening removal process complete"
        message = "The stress stiffening effects of the following group "
        message += "of lines have been removed from FE model.\n\n"
        message += f"{lines}"
        PrintMessageInput([window_title_2, title, message], auto_close=True)

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

            self.pushButton_remove.setDisabled(True)

    def get_information_elem(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                selected_id = item.text(0)
                selected_key = self.dictKey_label.format(selected_id)

                if "Selection-" in selected_key:
                    stiffening_data = self.preprocessor.group_elements_with_stress_stiffening[selected_key]

                    data = dict()
                    for element in stiffening_data[1]:
                        data[element] = stiffening_data[0]

                    if len(data):
                        self.close()
                        header_labels = ["Elements", "Internal pressure", "External pressure"]
                        GetInformationOfGroup(  group_label = "Stress stiffening effect",
                                                selection_label = "Element ID:",
                                                header_labels = header_labels,
                                                column_widths = [100, 120, 120],
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
                    header_labels = ["Lines", "Stress stiffening effect"]
                    GetInformationOfGroup(  group_label = "Stress stiffening effect",
                                            selection_label = "Line ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 140],
                                            data = data  )

                # list_lines = self.get_list_typed_entries()          
                # read = GetInformationOfGroup(self.project, list_lines, "Lines")
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

    def get_information(self, item):
        if self.tabWidget_groups.currentIndex() == 0:
            self.get_information_elem(item)
        else:
            self.get_information_line(item)

    def load_elements_info(self):
        self.treeWidget_stress_stiffening_elements.clear()
        self.tabWidget_groups.setTabVisible(0, False)
        for section, values in self.preprocessor.group_elements_with_stress_stiffening.items():
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, str(values[1])])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_stress_stiffening_elements.addTopLevelItem(new)

    def load_lines_info(self):        
        self.treeWidget_stress_stiffening_lines.clear()
        self.tabWidget_groups.setTabVisible(1, False)
        lines = self.preprocessor.lines_with_stress_stiffening
        if len(lines) != 0:
            new = QTreeWidgetItem(["Selection-1" , str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_stress_stiffening_lines.addTopLevelItem(new)

    def load_treeWidgets_info(self):

        self.load_lines_info()
        self.load_elements_info()
        self.tabWidget_main.setTabVisible(1, False)

        if len(self.preprocessor.lines_with_stress_stiffening):
            self.tabWidget_main.setTabVisible(1, True)
            self.tabWidget_groups.setTabVisible(1, True)

        if len(self.preprocessor.group_elements_with_stress_stiffening):
            self.tabWidget_main.setTabVisible(1, True)
            self.tabWidget_groups.setTabVisible(0, True)

    def update(self):

        self.lines_id = app().main_window.list_selected_lines()
        self.elements_id = app().main_window.list_selected_elements()

        selection_index = self.comboBox_selection.currentIndex()
        if self.lines_id != []:

            if selection_index == 1:
                self.selection_type_callback()
            else:
                self.comboBox_selection.setCurrentIndex(1)

            self.label_selected_id.setText("Lines IDs:")
            self.write_ids(self.lines_id)
            
            if len(self.lines_id) == 1:
                entity = self.preprocessor.lines_from_model[self.lines_id[0]] 
                if entity.stress_stiffening_parameters is not None:
                    pressures = entity.stress_stiffening_parameters
                    self.lineEdit_external_pressure.setText(str(pressures[0]))
                    self.lineEdit_internal_pressure.setText(str(pressures[1]))

        elif self.elements_id != []:

            if selection_index == 2:
                self.selection_type_callback()
            else:
                self.comboBox_selection.setCurrentIndex(2)

            self.label_selected_id.setText("Elements IDs:")
            self.write_ids(self.elements_id)

            if len(self.elements_id) == 1:
                element = self.preprocessor.structural_elements[self.elements_id[0]] 
                self.lineEdit_external_pressure.setText(str(element.external_pressure))       
                self.lineEdit_internal_pressure.setText(str(element.internal_pressure))

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.press_confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()