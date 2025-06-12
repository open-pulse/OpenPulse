from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from molde import load_ui

import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"


class TurnOffAcousticElementsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/turn_off_acoustic_elements_input.ui"
        load_ui(ui_path, self, UI_DIR)

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
        self.comboBox_action_selector :  QComboBox

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
        for i, w in enumerate([120, 140]):
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

    def attribute_callback(self):

        lineEdit = self.lineEdit_element_id.text()
        stop, element_ids = self.before_run.check_selected_ids(lineEdit, "elements")
        
        if stop:
            return

        index = self.comboBox_action_selector.currentIndex()
        self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(element_ids, True)

        for element_id in element_ids:

            coords = list()
            element = self.preprocessor.acoustic_elements[element_id]
            coords.extend(list(np.round(element.first_node.coordinates, 5)))
            coords.extend(list(np.round(element.last_node.coordinates, 5)))

            data = {
                    "coords" : coords,
                    "turned_off" : not bool(index)
                    }

            self.properties._set_element_property("acoustic_element_turned_off", data, element_ids=element_id)

        self.actions_to_finalize()

    def remove_callback(self):

        if  self.lineEdit_element_id.text() != "":

            str_element = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(str_element, "elements")
            if stop:
                return

            for element_id in element_ids:
                self.properties._remove_element_property("acoustic_element_turned_off", element_id)
            
            self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(element_ids, False)
            self.lineEdit_element_id.setText("")
            self.actions_to_finalize()

    def reset_callback(self):

            self.hide()

            title = f"Turn-on all acoustic elements"
            message = "Would you like to turn-on the all acoustic elements?"

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                element_ids = list()
                for (property, element_id) in self.properties.element_properties.keys():
                    if property == "acoustic_element_turned_off":
                        element_ids.append(element_id)

                if element_ids:
                    for element_id in element_ids:
                        self.properties._remove_element_property("acoustic_element_turned_off", element_id)

                    self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(element_ids, False)
                    self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_element_properties_in_file()
        app().main_window.update_plots()
        self.load_elements_info()
        self.pushButton_cancel.setText("Exit")

    def load_elements_info(self):

        self.treeWidget_elements_info.clear()
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "acoustic_element_turned_off":

                if data["turned_off"]:
                    action_label = "Turned-off"
                else:
                    continue

                item = QTreeWidgetItem([str(element_id), action_label])
                for i in range(3):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_elements_info.addTopLevelItem(item)

        self.update_tabs_visibility()         

    def update_tabs_visibility(self):

        self.pushButton_remove.setDisabled(True)
        for (property, _) in self.properties.element_properties.keys():
            if property == "acoustic_element_turned_off":
                # self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

        self.tabWidget_main.setTabVisible(1, False)

    def on_click_item(self, item):
        if item.text(0) != "":
            self.pushButton_remove.setEnabled(True)
            element_id = int(item.text(0))
            self.lineEdit_element_id.setText(item.text(0))
            app().main_window.set_selection(elements=[element_id])

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