import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.turn_off_acoustic_elements_input_ui import (
    TurnOffAcousticElementsInput_UI,
)
from pulse.interface.user_input.model.setup.elements_input import ElementsInput
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)

window_title_1 = "Error"
window_title_2 = "Warning"


class TurnOffAcousticElementsInput(ElementsInput, TurnOffAcousticElementsInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.load_elements_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.keep_window_open = True

        self.type_label = None
        self.dkey = None
        self.log_removal = True

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self._tab_event_update)
        #
        self.treeWidget_elements_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_elements_info.itemDoubleClicked.connect(
            self.on_doubleclick_item
        )
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
            self.treeWidget_elements_info.headerItem().setTextAlignment(
                i, Qt.AlignCenter
            )

    def _tab_event_update(self):

        index = self.tabWidget_main.currentIndex()

        if index == 0:
            self.selection_callback()

        elif index == 1:
            self.lineEdit_element_id.clear()

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

            data = {"coords": coords, "turned_off": not bool(index)}

            self.properties._set_element_property(
                "acoustic_element_turned_off", data, element_ids=element_id
            )

        self.actions_to_finalize()

    def remove_callback(self):

        if self.lineEdit_element_id.text() != "":
            str_element = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(
                str_element, "elements"
            )
            if stop:
                return

            for element_id in element_ids:
                self.properties._remove_element_property(
                    "acoustic_element_turned_off", element_id
                )

            self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(
                element_ids, False
            )
            self.lineEdit_element_id.clear()
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Turn-on all acoustic elements"
        message = "Would you like to turn-on the all acoustic elements?"

        buttons_config = {"left_button_label": "No", "right_button_label": "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            element_ids = list()
            for property, element_id in self.properties.element_properties.keys():
                if property == "acoustic_element_turned_off":
                    element_ids.append(element_id)

            if element_ids:
                for element_id in element_ids:
                    self.properties._remove_element_property(
                        "acoustic_element_turned_off", element_id
                    )

                self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(
                    element_ids, False
                )
                self.actions_to_finalize()

    def actions_to_finalize(self):
        self.load_elements_info()
        app().project.file.write_element_properties_in_file()
        app().main_window.update_plots()

    def load_elements_info(self):

        self.treeWidget_elements_info.clear()
        for (property, element_id), data in self.properties.element_properties.items():
            if property != "acoustic_element_turned_off":
                continue

            if not isinstance(data, dict):
                continue

            if data.get("turned_off"):
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
        for property, _ in self.properties.element_properties.keys():
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
