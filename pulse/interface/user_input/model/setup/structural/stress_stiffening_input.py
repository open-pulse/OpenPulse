from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
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
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties
        self.before_run = app().project.get_pre_solution_model_checks()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.selection_callback()
        self.load_treeWidgets_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_attribution_type: QComboBox

        # QLabel
        self.label_attribute_to: QLabel
        self.label_selected_id: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_external_pressure: QLineEdit
        self.lineEdit_internal_pressure: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_remove: QPushButton

        # QTabWidget
        self.tabWidget_groups: QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_stress_stiffening: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_stress_stiffening.itemClicked.connect(self.on_click_item)
        self.treeWidget_stress_stiffening.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def _config_widgets(self):
        #
        self.pushButton_remove.setDisabled(True)
        #
        for i, w in enumerate([100, 130, 140]):
            self.treeWidget_stress_stiffening.setColumnWidth(i, w)
            self.treeWidget_stress_stiffening.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def attribution_type_callback(self):

        index = self.comboBox_attribution_type.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            self.selection_callback()

        self.lineEdit_selected_id.setEnabled(bool(index))

    def selection_callback(self):

        self.comboBox_attribution_type.blockSignals(True)

        selected_lines = app().main_window.list_selected_lines()
        if selected_lines:

            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)

            self.lineEdit_selected_id.setEnabled(True)
            self.comboBox_attribution_type.setCurrentIndex(1)

            if len(selected_lines) == 1:
                line_id = selected_lines[0]
                prop_data = self.properties._get_property("stress_stiffening", line_id=line_id)
                
                if isinstance(prop_data, dict):
                    pressures = prop_data["pressures"]
                    self.lineEdit_external_pressure.setText(str(pressures[0]))
                    self.lineEdit_internal_pressure.setText(str(pressures[1]))

        self.comboBox_attribution_type.blockSignals(False)

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 0:
            self.selection_callback()

        else:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)

    def tabs_visibility(self):
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "stress_stiffening" in data.keys():
                self.tabWidget_main.setTabVisible(1, True)
                return

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def check_inputs(self, lineEdit: QLineEdit, label: str, only_positive=True, zero_included=False):
        title = "Ivalid entry"
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
                            return True, None
                    else:
                        if out <= 0:
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([window_title_1, title, message])
                            return True, None

            except Exception as log_error:
                message = f"Wrong input for {label}.\n\n"
                message += str(log_error)
                PrintMessageInput([window_title_1, title, message])
                return True, None

        else:
            if zero_included:
                return False, float(0)
            else:
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([window_title_1, title, message])
                return True, None

        return False, out

    def attribute_callback(self):

        stop, external_pressure = self.check_inputs(self.lineEdit_external_pressure, 
                                                    "'External pressure'", 
                                                    zero_included=True)
        if stop:
            return

        stop, internal_pressure = self.check_inputs(self.lineEdit_internal_pressure, 
                                                    "'Internal pressure'", 
                                                    zero_included=True)
        if stop:
            return
        
        if (external_pressure + internal_pressure) == 0:
            title = "Empty entries at the input pressure fields"
            message = f"You should to insert a value different from zero at the external or internal "
            message += "pressure field inputs to continue."
            PrintMessageInput([window_title_1, title, message])  
            return
        
        parameters = {  "external_pressure" : external_pressure,
                        "internal_pressure" : internal_pressure  }

        selection_index = self.comboBox_attribution_type.currentIndex()
        if selection_index == 0:
            line_ids = list(app().project.model.mesh.lines_from_model.keys())
    
        else:
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return True

        filtered_selection = list()
        for line_id in line_ids:
            element_type = self.properties._get_property("structural_element_type", line_id=line_id)
            if element_type == "pipe_1":
                filtered_selection.append(line_id)

        if filtered_selection:

            app().main_window.set_selection(lines=filtered_selection)

            self.preprocessor.set_stress_stiffening_by_lines(filtered_selection, parameters)
            self.properties._set_line_property("stress_stiffening", parameters, filtered_selection)

            self.actions_to_finalize()
            self.complete = True

    def remove_callback(self):
        if self.lineEdit_selected_id.text() != "":

            line_id = int(self.lineEdit_selected_id.text())

            parameters = {  "external_pressure" : 0.,
                            "internal_pressure" : 0.  }

            self.preprocessor.set_stress_stiffening_by_lines(line_id, parameters)
            self.properties._remove_line_property("stress_stiffening", line_id)

            self.lineEdit_selected_id.setText("")
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of stress stiffenings"
        message = "Would you like to remove the stress stiffenings from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            line_ids = list()
            for (line_id, data) in self.properties.line_properties.items():
                if "stress_stiffening" in data.keys():
                    line_ids.append(line_id)

            parameters = {  "external_pressure" : 0.,
                            "internal_pressure" : 0.  }

            self.preprocessor.set_stress_stiffening_by_lines(line_ids, parameters)
            self.properties._remove_line_property("stress_stiffening", line_ids)

            self.actions_to_finalize()

    def actions_to_finalize(self):

        self.load_treeWidgets_info()
        app().pulse_file.write_line_properties_in_file()

        self.preprocessor.stress_stiffening_enabled = False
        for data in self.properties.line_properties.values():
            if "stress_stiffening" in data.keys():
                self.preprocessor.stress_stiffening_enabled = True
                return

    def load_treeWidgets_info(self):

        self.treeWidget_stress_stiffening.clear()
        for line_id, data in self.properties.line_properties.items():
            if "stress_stiffening" in data.keys():

                prop_data = data["stress_stiffening"]
                ext_pressure = prop_data["external_pressure"]
                int_pressure = prop_data["internal_pressure"]

                item = QTreeWidgetItem([str(line_id) ,f"{ext_pressure : .4e}", f"{int_pressure : .4e}"])
                for i in range(3):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_stress_stiffening.addTopLevelItem(item)

        self.tabs_visibility()

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