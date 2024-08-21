# fmt: off

from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from collections import defaultdict


window_title_1 = "Error"
window_title_2 = "Warning"

class BeamXaxisRotationInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/setup/structural/xaxis_beam_rotation_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._config_widgets()
        self._create_connections()
        self.selection_callback()
        self.load_lines_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True

        self.index = 0
        self.element_type = 'pipe_1'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.list_lines_to_update_cross_section = list()
        self.beam_lines = list()

        self.before_run = self.project.get_pre_solution_model_checks()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection: QComboBox

        # QLabel
        self.label_attribute_to: QLabel
        self.label_selected_id: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_xaxis_rotation_increment_angle: QLineEdit
        self.lineEdit_xaxis_rotation_actual_angle: QLineEdit

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTreeWidget
        self.treeWidget_xaxis_rotation_angle: QTreeWidget

        # QTabWidget
        self.tabWidget_xaxis_rotation_angle: QTabWidget

    def _config_widgets(self):
        self.pushButton_remove.setDisabled(True)
        #
        self.treeWidget_xaxis_rotation_angle.setColumnWidth(0, 120)
        # self.treeWidget_xaxis_rotation_angle.setColumnWidth(1, 100)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _create_connections(self):
        self.comboBox_selection.currentIndexChanged.connect(self.change_selection_callback)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.xaxis_beam_rotation_attribution_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_xaxis_rotation_angle.currentChanged.connect(self.tab_event_update)
        self.treeWidget_xaxis_rotation_angle.itemClicked.connect(self.on_click_item)
        self.treeWidget_xaxis_rotation_angle.itemDoubleClicked.connect(self.on_double_click_item)    
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        filtered_selection = list()
        self.comboBox_selection.blockSignals(True)

        selected_lines = app().main_window.list_selected_lines()
        if selected_lines:
            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)

            for line_id in selected_lines:
                element_type = self.properties._get_property("structural_element_type", line_id=line_id)
                if element_type == "beam_1":
                    filtered_selection.append(line_id)

            if filtered_selection:
                self.tabWidget_xaxis_rotation_angle.setDisabled(False)
            else:
                self.lineEdit_selected_id.setText("")
                self.tabWidget_xaxis_rotation_angle.setDisabled(True)

            if len(selected_lines) == 1:
                line_id = selected_lines[0]
                self.comboBox_selection.setCurrentIndex(1)
                element_type = self.properties._get_property("structural_element_type", line_id=line_id)
                if element_type == "beam_1":
                    data = self.properties._get_property("beam_xaxis_rotation", line_id=line_id)
                    if isinstance(data, dict):
                        angle = data["rotation angle"]
                        self.lineEdit_xaxis_rotation_actual_angle.setText(str(angle))

        self.comboBox_selection.blockSignals(False)

    def change_selection_callback(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)
        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        else:
            if app().main_window.list_selected_lines():
                self.selection_callback()

    def tab_event_update(self):

        self.lineEdit_selected_id.setText("")
        self.pushButton_remove.setDisabled(True)
        tab_index = self.tabWidget_xaxis_rotation_angle.currentIndex()

        if tab_index == 0:
            self.label_attribute_to.setDisabled(False)
            self.label_selected_id.setText("Selected lines:")
            self.lineEdit_selected_id.setDisabled(False)
            self.comboBox_selection.setDisabled(False)

        elif tab_index == 1:
            self.label_attribute_to.setDisabled(True)
            self.label_selected_id.setText("Selected group:")
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
            self.comboBox_selection.setDisabled(True)

    def on_click_item(self, item):
        self.selected_key = item.text(0)
        self.lineEdit_selected_id.setText(item.text(1))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item):
        self.selected_key = item.text(0)
        self.lineEdit_selected_id.setText(item.text(1))
        self.lineEdit_selected_id.setDisabled(True)

    def check_xaxis_rotation_angle(self):
        rotation_angle = 0
        try:
            self.rotation_angle = float(self.lineEdit_xaxis_rotation_increment_angle.text())
        except Exception as error_log:
            title = f"Invalid X-axis Rotation Angle"
            message = f"Please, inform a valid number at the 'Rotation angle' input field to continue.\n\n"
            message += f"{str(error_log)}"
            PrintMessageInput([window_title_1, title, message])
            return True, rotation_angle
        return False, rotation_angle

    def filter_beam_lines(self, line_ids: list):
        try:

            beam_lines = list()
            non_beam_lines = list()
            for line_id in line_ids:
                element_type = self.properties._get_property("structural_element_type", line_id=line_id)
                if element_type != "beam_1":
                    non_beam_lines.append(line_id)
                else:
                    self.beam_lines.append(line_id)

            if len(non_beam_lines):
                title = "Non-beam line selected"
                message = "The following non-beam lines have been removed from the current selection:\n\n"
                message += f"{non_beam_lines}"
                PrintMessageInput([window_title_2, title, message])                

        except:
            return True, beam_lines

        return False, beam_lines

    def xaxis_beam_rotation_attribution_callback(self):

        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 0:
            line_ids = list(self.model.mesh.lines_from_model.keys())

        else:
            str_lines = self.lineEdit_selected_id.text()
            self.stop, line_ids = self.before_run.check_selected_ids(str_lines, "lines")
            if self.stop:
                return

        stop, beam_line_ids = self.filter_beam_lines(line_ids)
        if stop:
            return

        stop, rotation_angle = self.check_xaxis_rotation_angle()
        if stop:
            self.lineEdit_xaxis_rotation_increment_angle.setFocus()
            return
    
        for line_id in beam_line_ids:
            actual_angle = self.properties._get_property("beam_xaxis_rotation", line_id=line_id)
            if actual_angle is None:
                actual_angle = rotation_angle
            else:
                rotation_angle += actual_angle

            self.preprocessor.set_beam_xaxis_rotation_by_lines(line_id, rotation_angle)

        self.preprocessor.process_all_rotation_matrices()
        app().pulse_file.write_line_properties_in_file()
        app().main_window.update_plots()
        self.close()

    def load_lines_info(self):

        rotation_data = defaultdict(list)
        for line_id, data in self.properties.line_properties.items():
            if "beam_xaxis_rotation" in data.keys():
                rot_angle = data["ratation angle"]
                rotation_data[rot_angle].append(line_id)

        self.treeWidget_xaxis_rotation_angle.clear()
        for angle, line_ids in rotation_data.items():
            new = QTreeWidgetItem([str(angle), str(line_ids)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_xaxis_rotation_angle.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.lineEdit_selected_id.setText("")
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_xaxis_rotation_angle.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "beam_xaxis_rotation" in data.keys():
                self.tabWidget_xaxis_rotation_angle.setCurrentIndex(0)
                self.tabWidget_xaxis_rotation_angle.setTabVisible(1, True)
                return

    def remove_callback(self):

        if  self.lineEdit_selected_id.text() != "":

            str_lines = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(str_lines, "lines")
            if stop:
                return

            self.preprocessor.set_beam_xaxis_rotation_by_lines(line_ids[0], 0)
            self.preprocessor.process_all_rotation_matrices()

            self.properties._remove_line_property("prescribed_dofs", line_ids[0])
            app().pulse_file.write_line_properties_in_file()
            self.load_lines_info()
            app().main_window.update_plots()

    def reset_callback(self):

        self.hide()

        title = "Resetting x-axis beam rotations"
        message = "Would you like to remove all x-axis rotations attributed to beam elements?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            line_ids = list()
            for (property, line_id) in self.properties.line_properties.keys():
                if property == "beam_xaxis_rotation":
                    line_ids.append(line_id)

            self.preprocessor.set_beam_xaxis_rotation_by_lines(line_ids, 0)
            self.preprocessor.process_all_rotation_matrices()

            self.properties._reset_line_property("beam_xaxis_rotation")
            app().pulse_file.write_line_properties_in_file()
            app().main_window.update_plots()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.xaxis_beam_rotation_attribution_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
# fmt: on