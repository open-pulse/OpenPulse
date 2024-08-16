from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticElementLengthCorrectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/element_length_correction_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_elements_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True

        self.type_label = None
        self.dkey = None
        self.log_removal = True

        self.before_run = app().project.get_pre_solution_model_checks()
    
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
        self.pushButton_confirm.clicked.connect(self.element_correction_type_callback)
        self.pushButton_reset_confirm.clicked.connect(self.reset_callback)
        self.pushButton_remove_by_group_confirm.clicked.connect(self.remove_callback)
        #
        self.tabWidget_element_length_correction.currentChanged.connect(self._tab_event_update)
        #
        self.treeWidget_length_correction_groups.itemClicked.connect(self.on_click_item)
        self.treeWidget_length_correction_groups.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_elements = app().main_window.list_selected_elements()
        if selected_elements:
            text = ", ".join([str(i) for i in selected_elements])
            self.lineEdit_element_id.setText(text)

    def _config_widgets(self):
        self.treeWidget_length_correction_groups.setColumnWidth(0, 100)
        self.treeWidget_length_correction_groups.setColumnWidth(1, 80)
        self.treeWidget_length_correction_groups.setColumnWidth(2, 90)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _tab_event_update(self):

        index = self.tabWidget_element_length_correction.currentIndex()

        if index == 0:
            text = "Element IDs:"
            self.selection_callback()

        elif index == 1: 
            text = "Group ID:"
            self.lineEdit_element_id.setText("")

        self.lineEdit_element_id.setDisabled(bool(index))
        self.label_selection.setText(text)

    def element_correction_type_callback(self):

        lineEdit = self.lineEdit_element_id.text()
        stop, element_ids = self.before_run.check_selected_ids(lineEdit, "elements")
        
        if stop:
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

        data = {"correction type" : type_id}

        _element_ids = self.filter_selection(index, element_ids)
        if _element_ids:
            filt_element_ids = list(np.sort(_element_ids))

            self.preprocessor.set_length_correction_by_element(filt_element_ids, data)

            self.properties._set_element_property("element_length_correction", data, element_ids=_element_ids)

            app().pulse_file.write_model_properties_in_file()

            if len(filt_element_ids) > 20:
                print("Set acoustic element_length_correction due the {} at {} selected elements".format(self.type_label, len(filt_element_ids)))
            else:
                print("Set acoustic element_length_correction due the {} at elements: {}".format(self.type_label, filt_element_ids))
        
            self.load_elements_info()
            self.close()

    def filter_selection(self, index: int, element_ids: list) -> list:

        node_ids = list()
        filtered_elements = list()

        for element_id in element_ids:

            element = self.preprocessor.acoustic_elements[element_id]

            first_node = element.first_node.external_index
            if first_node not in node_ids:
                node_ids.append(first_node)

            last_node = element.last_node.external_index
            if last_node not in node_ids:
                node_ids.append(last_node)
        
        for node_id in node_ids:
            neigh_elements = self.preprocessor.neighboor_elements_of_node(node_id)

            if index in [1, 2]:                

                if len(neigh_elements) == 3:
                    filtered_elements.extend(neigh_elements)

            else:

                if len(neigh_elements) == 2:
                    element_0 = neigh_elements[0]
                    element_1 = neigh_elements[1]

                    diam_0 = element_0.cross_section.outer_diameter
                    diam_1 = element_1.cross_section.outer_diameter

                    if diam_0 != diam_1:
                        filtered_elements.extend(neigh_elements)

        return [element.index for element in filtered_elements]

    def load_elements_info(self):
        
        keys = [0, 1, 2]
        labels = ['Expansion', 'Side branch', 'Loop']
        
        self.dict_correction_types = dict(zip(keys, labels))
        self.treeWidget_length_correction_groups.clear()
        
        self.maps_correction_type = defaultdict(list)
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "element_length_correction":
                self.maps_correction_type[data["correction index"]].append(element_id)

                index = data["correction index"]
                text = self.dict_correction_types[index]

                new = QTreeWidgetItem(["::", text, str(element_id)])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                new.setTextAlignment(2, Qt.AlignCenter)
                self.treeWidget_length_correction_groups.addTopLevelItem(new)
        
        self.update_tabs_visibility()         

    def on_click_item(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        key = self.prefix_label.format(item.text(0))
        list_elements = self.dict_group_elements[key][1]
        app().main_window.set_selection(elements = list_elements)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
        self.get_information_of_group()

    def remove_callback(self):

        if  self.lineEdit_element_id.text() != "":

            str_element = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(str_element, "elements")
            if stop:
                return
            
            self.preprocessor.set_length_correction_by_element(element_ids, None)

            for element_id in element_ids:
                self.properties._remove_nodal_property("element_length_correction", element_id)

            app().pulse_file.write_model_properties_in_file()

            self.lineEdit_element_id.setText("")
            self.pushButton_remove_by_group_confirm.setDisabled(True)
            self.load_elements_info()

            app().main_window.update_plots()
            # self.close()

    def reset_callback(self):

            self.hide()

            title = f"Resetting of volume velocities"
            message = "Would you like to remove all volume velocities from the acoustic model?"

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                element_ids = list()
                for (property, element_id), data in self.properties.nodal_properties.items():
                    if property == "element_length_correction":
                        element_ids.append(element_id)

                self.preprocessor.set_length_correction_by_element(element_ids, None)

                self.properties._reset_property("element_length_correction")
                app().pulse_file.write_model_properties_in_file()
                app().main_window.update_plots()
                self.close()

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
                PrintMessageInput([window_title_1, title, message])

        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def update_tabs_visibility(self):
        self.tabWidget_element_length_correction.setTabVisible(1, False)
        for (property, _) in self.properties.element_properties.keys():
            if property == "element_length_correction":
                self.tabWidget_element_length_correction.setCurrentIndex(0)
                self.tabWidget_element_length_correction.setTabVisible(1, True)
                return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.element_correction_type_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_element_length_correction_by_group()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)