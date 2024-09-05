from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
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
        self.pushButton_attribute : QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_elements_info : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self._tab_event_update)
        #
        self.treeWidget_elements_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_elements_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_elements = app().main_window.list_selected_elements()
        if selected_elements:
            if self.tabWidget_main.currentIndex() == 1:
                return
            text = ", ".join([str(i) for i in selected_elements])
            self.lineEdit_element_id.setText(text)

    def _config_widgets(self):
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")
        #
        for i, w in enumerate([80, 120, 140]):
            self.treeWidget_elements_info.setColumnWidth(i, w)
            self.treeWidget_elements_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _tab_event_update(self):

        index = self.tabWidget_main.currentIndex()

        if index == 0:
            self.selection_callback()

        elif index == 1:
            self.lineEdit_element_id.setText("")

        self.lineEdit_element_id.setDisabled(bool(index))
        self.pushButton_remove.setDisabled(True)

    def filter_selection(self, correction_type: int, element_ids: list) -> dict:

        node_ids = list()
        filtered_data = dict()

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

            if correction_type in [1, 2]:

                if len(neigh_elements) == 3:
                    node = app().project.model.preprocessor.nodes[node_id]
                    coords = list(np.round(node.coordinates, 5))
                    filtered_data[node_id] = { 
                                              "correction_type" : correction_type,
                                              "coords" : coords,
                                              "element_ids" : [element.index for element in neigh_elements]
                                              }

            else:

                if len(neigh_elements) == 2:
                    element_0 = neigh_elements[0]
                    element_1 = neigh_elements[1]

                    diam_0 = element_0.cross_section.outer_diameter
                    diam_1 = element_1.cross_section.outer_diameter

                    if diam_0 != diam_1:
                        node = app().project.model.preprocessor.nodes[node_id]
                        coords = list(np.round(node.coordinates, 5))
                        filtered_data[node_id] = { 
                                                  "correction_type" : correction_type,
                                                  "coords" : coords,
                                                  "element_ids" : [element.index for element in neigh_elements]
                                                  }

        if filtered_data:
            return filtered_data

        else:
            self.hide()
            title = "Invalid selection"
            message = f"The '{self.correction_labels[correction_type]}' has not been detected in "
            message += f"the selected group of elements. You should to change the elements "
            message += "selection and/or modify the correction type to proceed."
            PrintMessageInput([window_title_2, title, message])
            return dict()

    def attribute_callback(self):

        lineEdit = self.lineEdit_element_id.text()
        stop, element_ids = self.before_run.check_selected_ids(lineEdit, "elements")
        
        if stop:
            return
        
        index = self.comboBox_element_length_correction_type.currentIndex()

        if index == 0:
            correction_type = 0
            self.type_label = "'Expansion'"
   
        elif index == 1:
            correction_type = 1
            self.type_label = "'Side branch'"

        elif index == 2:
            correction_type = 2
            self.type_label = "'Loop'"

        filtered_data = self.filter_selection(correction_type, element_ids)
        
        for selection_data in filtered_data.values():

            element_ids = selection_data["element_ids"]

            data = {
                    "correction_type" : selection_data["correction_type"],
                    "coords" : selection_data["coords"]
                    }

            self.preprocessor.set_element_length_correction_by_element(element_ids, data)
            self.properties._set_element_property("element_length_correction", data, element_ids=element_ids)

            app().pulse_file.write_element_properties_in_file()

            print("The acoustic element length correction {} was attributed to elements: {}".format(self.type_label, element_ids))

            self.load_elements_info()
            # self.close()

    def remove_callback(self):

        if  self.lineEdit_element_id.text() != "":

            str_element = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(str_element, "elements")
            if stop:
                return
            
            self.preprocessor.set_element_length_correction_by_element(element_ids, None)

            for element_id in element_ids:
                self.properties._remove_element_property("element_length_correction", element_id)

            self.lineEdit_element_id.setText("")
            

            app().pulse_file.write_element_properties_in_file()
            app().main_window.update_plots()
            self.load_elements_info()
            # self.close()

    def reset_callback(self):

            self.hide()

            title = f"Resetting of element length corrections"
            message = "Would you like to remove all element length corrections from the acoustic model?"

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                element_ids = list()
                for (property, element_id) in self.properties.element_properties.keys():
                    if property == "element_length_correction":
                        element_ids.append(element_id)

                if element_ids:
                    self.preprocessor.set_element_length_correction_by_element(element_ids, None)

                    for element_id in element_ids:
                        self.properties._remove_element_property("element_length_correction", element_id)

                    app().pulse_file.write_element_properties_in_file()
                    app().main_window.update_plots()
                    self.load_elements_info()
                    # self.close()

    def maps_correction_type_to_elements(self):

        keys = [0, 1, 2]
        labels = ['Expansion', 'Side branch', 'Loop']
        self.correction_labels = dict(zip(keys, labels))

        aux = defaultdict(list)
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "element_length_correction":
                coords = data["coords"]
                index = data["correction_type"]
                elc_label = self.correction_labels[index]
                aux[elc_label, str(coords)].append(element_id)

        group_id = 1
        self.elements_correction_data = dict()
        for key, element_ids in aux.items():
            self.elements_correction_data[group_id] = (element_ids, key[0])
            group_id += 1

    def load_elements_info(self):

        self.maps_correction_type_to_elements()
        self.treeWidget_elements_info.clear()

        for group_id, (element_ids, elc_label) in self.elements_correction_data.items():
            item = QTreeWidgetItem([str(group_id), elc_label, str(element_ids)])
            for i in range(3):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_elements_info.addTopLevelItem(item)

        self.update_tabs_visibility()         

    def update_tabs_visibility(self):

        self.pushButton_remove.setDisabled(True)
        for (property, _) in self.properties.element_properties.keys():
            if property == "element_length_correction":
                # self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return
        
        self.tabWidget_main.setTabVisible(1, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            self.pushButton_remove.setEnabled(True)
            group_id = int(item.text(0))
            (element_ids, _) = self.elements_correction_data[group_id]
            app().main_window.set_selection(elements=element_ids)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.set_selection()
        return super().closeEvent(a0)