from PySide6.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from molde import load_ui

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class RadiationImpedanceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/radiation_impedance_input.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.before_run = app().project.get_pre_solution_model_checks()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_radiation_impedance_type: QComboBox

        # QLineEdit
        self.lineEdit_node_ids: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_search: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_nodal_info: QTreeWidget
        self.treeWidget_nodal_info.setColumnWidth(1, 20)
        self.treeWidget_nodal_info.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) == 1:
                for (_property, *args), data in self.properties.nodal_properties.items():
                    if _property == "radiation_impedance" and selected_nodes == args:

                        impedance_type = data["impedance_type"]
                        self.comboBox_radiation_impedance_type.setCurrentIndex(impedance_type)

    def tab_event_callback(self):
        self.lineEdit_node_ids.setText("")
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_node_ids.setText("")
            self.lineEdit_node_ids.setDisabled(True)
        else:
            self.selection_callback()
            self.lineEdit_node_ids.setDisabled(False)

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        radiation_impedances = ["Anechoic", "Flanged", "Unflanged"]

        for (property, *args), data in self.properties.nodal_properties.items():

            if property == "radiation_impedance":
                index = data["impedance_type"]
                text = radiation_impedances[index]

                new = QTreeWidgetItem([str(args[0]), text])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.tabWidget_main.setTabVisible(1, False)
        for (property, *args) in self.properties.nodal_properties.keys():
            if property == "radiation_impedance":
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

    def attribute_callback(self):

        lineEdit = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            return
        
        self.remove_conflicting_excitations(node_ids)

        impedance_type = self.comboBox_radiation_impedance_type.currentIndex()

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {
                    "coords" : coords,
                    "impedance_type": impedance_type
                    }

            self.properties._set_nodal_property("radiation_impedance", data, node_id)
            self.actions_to_finalize()

        print(f"[Set Radiation Impedance] - defined at node(s) {node_ids}")

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item(self, item):
        self.lineEdit_node_ids.setText(item.text(0))

    def remove_conflicting_excitations(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["specific_impedance"]:
                table_names = self.properties.get_nodal_related_table_names(label, node_id)
                self.properties._remove_nodal_property(label, node_id)

                self.process_table_file_removal(table_names)

        app().pulse_file.write_nodal_properties_in_file()

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_callback(self):

        if  self.lineEdit_node_ids.text() != "":

            str_nodes = self.lineEdit_node_ids.text()
            stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            for node_id in node_ids:
                self.properties._remove_nodal_property("radiation_impedance", node_id)

            self.actions_to_finalize()

    def reset_callback(self):

            self.hide()

            title = f"Resetting of radiation impedances"
            message = "Would you like to remove all radiation impedances from the acoustic model?"

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return

            if read._continue:

                node_ids = list()
                for (_property, *args) in self.properties.nodal_properties.keys():
                    if _property == "radiation_impedance":
                        node_ids.append(args[0])

                self.properties._reset_nodal_property("radiation_impedance")
                self.actions_to_finalize()

    def actions_to_finalize(self):
        app().pulse_file.write_nodal_properties_in_file()
        app().main_window.update_plots(reset_camera=False)
        self.load_nodes_info()
        self.pushButton_cancel.setText("Exit")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)