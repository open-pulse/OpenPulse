from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.tools.utils import remove_bc_from_file

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticElementLengthCorrectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/element_length_correction_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_elements_info()
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

        self.type_label = None
        self.dkey = None
        self.log_removal = True
        self.elements_info_path = self.project.file._element_info_path
        self.prefix_label = "ACOUSTIC ELEMENT LENGTH CORRECTION || {}"

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.acoustic_elements = self.project.preprocessor.acoustic_elements
        self.dict_group_elements = self.project.preprocessor.group_elements_with_length_correction
    
    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_element_length_correction_type :  QComboBox
        # QLabel
        self.label_selection : QLabel
        # QLineEdit
        self.lineEdit_element_id : QLineEdit
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove_by_group_confirm : QPushButton
        self.pushButton_reset_confirm : QPushButton
        # QTabWidget
        self.tabWidget_element_length_correction : QTabWidget
        # QTreeWidget
        self.treeWidget_length_correction_groups : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_confirm.clicked.connect(self.check_element_correction_type)
        self.pushButton_reset_confirm.clicked.connect(self.remove_all_element_length_correction)
        self.pushButton_remove_by_group_confirm.clicked.connect(self.remove_element_length_correction_by_group)
        #
        self.tabWidget_element_length_correction.currentChanged.connect(self._tab_event_update)
        #
        self.treeWidget_length_correction_groups.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_groups.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _config_widgets(self):
        self.treeWidget_length_correction_groups.setColumnWidth(0, 100)
        self.treeWidget_length_correction_groups.setColumnWidth(1, 80)
        self.treeWidget_length_correction_groups.setColumnWidth(2, 90)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _tab_event_update(self):
        index = self.tabWidget_element_length_correction.currentIndex()
        if index == 0:
            text = "Element IDs:"
            selected_elements = app().main_window.list_selected_elements()
            self.write_ids(selected_elements)
            self.lineEdit_element_id.setDisabled(False)
        elif index == 1: 
            text = "Group ID:"
            self.lineEdit_element_id.setText("")
            self.lineEdit_element_id.setDisabled(True)
        self.label_selection.setText(text)

    def check_element_correction_type(self):

        lineEdit = self.lineEdit_element_id.text()
        self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
        
        if self.stop:
            return
        
        index = self.comboBox_element_length_correction_type.currentIndex()

        if index == 0:
            type_id = 0
            self.type_label = "'Expansion'"
   
        elif index == 1:
            type_id = 1
            self.type_label = "'Side branch'"

        elif index == 2:
            type_id = 2
            self.type_label = "'Loop'"
        
        section = self.prefix_label.format("Selection-1")
        keys = self.preprocessor.group_elements_with_length_correction.keys()

        if section in keys:
            index = 1
            while section in keys:
                index += 1
                section = self.prefix_label.format(f"Selection-{index}")

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

        self.load_elements_info()
        # self.close()

    def set_elements_to_correct(self, type_id, section, _print=False): 
        self.project.set_element_length_correction_by_elements(list(np.sort(self.elements_typed)), type_id, section)
        if _print:
            if len(self.elements_id) > 20:
                print("Set acoustic element length correction due the {} at {} selected elements".format(self.type_label, len(self.elements_id)))
            else:
                print("Set acoustic element length correction due the {} at elements: {}".format(self.type_label, self.elements_id))
        self.load_elements_info()

    def load_elements_info(self):
        keys = [0, 1, 2]
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
        self.update_tabs_visibility()         

    def on_click_item(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        key = self.prefix_label.format(item.text(0))
        list_elements = self.dict_group_elements[key][1]
        self.opv.opvRenderer.highlight_elements(list_elements)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
        self.get_information_of_group()

    def remove_function(self, key):
        section = key

        if self.log_removal:
            group_label = section.split(" || ")[1]
            message = f"The element length correction attributed to the {group_label} "
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
            key = self.prefix_label.format(self.lineEdit_element_id.text())
            if "Selection-" in self.lineEdit_element_id.text():
                self.remove_function(key)
            self.lineEdit_element_id.setText("")
        else:
            self.remove_function(self.dkey)

    def remove_all_element_length_correction(self):
        temp_dict_groups = self.dict_group_elements.copy()
        keys = temp_dict_groups.keys()
        for key in keys:
            self.log_removal = False
            self.remove_function(key)

        title = "Removal process complete"
        message = "The element length correction has been removed from all elements."
        PrintMessageInput([window_title_2, title, message])

    def get_information_of_group(self):
        try:

            selected_key = self.prefix_label.format(self.lineEdit_element_id.text())
            if "Selection-" in selected_key:

                self.close()
                data = dict()
                group_data = self.dict_group_elements[selected_key]

                key = self.dict_correction_types[group_data[0]]
                for element_id in group_data[1]:
                    data[element_id] = [key]

                header_labels = ["Element ID", "Element length correction type"]
                GetInformationOfGroup(  group_label = "Element length correction",
                                        selection_label = "Element ID:",
                                        header_labels = header_labels,
                                        column_widths = [100, 200],
                                        data = data  )

            else:
                title = "Error in group selection"
                message = "Please, select a group in the list to get the information."
                self.info_text = [window_title_1, title, message]
                PrintMessageInput(self.info_text)

        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            self.info_text = [window_title_1, title, message]
            PrintMessageInput(self.info_text)
        self.show()

    def update(self):
        index = self.tabWidget_element_length_correction.currentIndex()
        if index == 0:
            selected_elements = app().main_window.list_selected_elements()
            self.write_ids(selected_elements)
        else:
            self.lineEdit_element_id.setText("")

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_element_id.setText(text)
        self.elements_id = app().main_window.list_selected_elements()

    def update_tabs_visibility(self):
        if len(self.dict_group_elements) == 0:
            self.tabWidget_element_length_correction.setCurrentIndex(0)
            self.tabWidget_element_length_correction.setTabVisible(1, False)
        else:
            self.tabWidget_element_length_correction.setTabVisible(1, True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_element_correction_type()
        elif event.key() == Qt.Key_Delete:
            self.remove_element_length_correction_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()