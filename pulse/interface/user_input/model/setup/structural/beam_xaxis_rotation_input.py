from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.xaxis_beam_rotation_input_ui import (
    XaxisBeamRotationInput_UI,
)
from pulse.interface.user_input.model.setup.structural.structural_lines_input import (
    StructuralLinesInput,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput

error_title = "Error"
warning_title = "Warning"


class BeamXaxisRotationInput(StructuralLinesInput, XaxisBeamRotationInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._config_widgets()
        self._create_connections()
        self.selection_callback()
        self.load_lines_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.keep_window_open = True
        self.complete = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False

        self.element_type = "pipe_1"

    def _config_widgets(self):
        #
        self.pushButton_remove.setDisabled(True)
        #
        for i, width in enumerate([120, 100]):
            self.treeWidget_xaxis_rotation_angle.setColumnWidth(i, width)
            self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        self.comboBox_selection.currentIndexChanged.connect(
            self.change_selection_callback
        )
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_xaxis_rotation_angle.currentChanged.connect(
            self.tab_event_update
        )
        self.treeWidget_xaxis_rotation_angle.itemClicked.connect(self.on_click_item)
        self.treeWidget_xaxis_rotation_angle.itemDoubleClicked.connect(
            self.on_double_click_item
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        filtered_selection = list()
        self.comboBox_selection.blockSignals(True)

        selected_lines = app().main_window.list_selected_lines()
        if selected_lines:
            for line_id in selected_lines:
                element_type = self.properties._get_property(
                    "structural_element_type", line_id=line_id
                )
                if element_type == "beam_1":
                    filtered_selection.append(line_id)

            if filtered_selection:
                text = ", ".join([str(i) for i in filtered_selection])
                self.lineEdit_selected_id.setText(text)
                self.comboBox_selection.setCurrentIndex(1)

            else:
                self.lineEdit_selected_id.clear()

            if len(filtered_selection) == 1:
                line_id = filtered_selection[0]
                element_type = self.properties._get_property(
                    "structural_element_type", line_id=line_id
                )

                if element_type == "beam_1":
                    rot_angle = self.properties._get_property(
                        "beam_xaxis_rotation", line_id=line_id
                    )
                    if rot_angle is None:
                        self.lineEdit_actual_angle.setText(str(0.0))
                    else:
                        self.lineEdit_actual_angle.setText(str(rot_angle))

                    self.lineEdit_increment_angle.setFocus()

        self.comboBox_selection.blockSignals(False)

    def change_selection_callback(self):

        self.lineEdit_selected_id.clear()
        self.lineEdit_selected_id.setEnabled(True)
        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        else:
            if app().main_window.list_selected_lines():
                self.selection_callback()

    def tab_event_update(self):

        self.lineEdit_selected_id.clear()
        self.pushButton_remove.setDisabled(True)
        tab_index = self.tabWidget_xaxis_rotation_angle.currentIndex()

        if tab_index == 0:
            self.label_attribute_to.setDisabled(False)
            self.lineEdit_selected_id.setDisabled(False)
            self.comboBox_selection.setDisabled(False)

        else:
            self.label_attribute_to.setDisabled(True)
            self.lineEdit_selected_id.setDisabled(True)
            self.comboBox_selection.setDisabled(True)

    def update_tabs_visibility(self):
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_xaxis_rotation_angle.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "beam_xaxis_rotation" in data.keys():
                self.tabWidget_xaxis_rotation_angle.setCurrentIndex(0)
                self.tabWidget_xaxis_rotation_angle.setTabVisible(1, True)
                return

    def on_click_item(self, item):
        line_id = int(item.text(0))
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)
        app().main_window.set_selection(lines=[line_id])

    def on_double_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_selected_id.setDisabled(True)

    def check_xaxis_rotation_angle(self):
        try:
            rotation_angle = float(self.lineEdit_increment_angle.text())
        except Exception as error_log:
            title = "Invalid X-axis Rotation Angle"
            message = "Please, inform a valid number at the 'Rotation angle' input field to continue.\n\n"
            message += f"{str(error_log)}"
            PrintMessageInput([error_title, title, message])
            return True, None
        return False, rotation_angle

    def filter_beam_lines(self, line_ids: list):
        try:
            beam_lines = list()
            for line_id in line_ids:
                element_type = self.properties._get_property(
                    "structural_element_type", line_id=line_id
                )
                if element_type == "beam_1":
                    beam_lines.append(line_id)

            if len(beam_lines) == 0:
                title = "Invalid lines selected"
                message = "No beam lines have been detected in the current selection. "
                message += "To proceed, it is necessary to change the lines selection."
                PrintMessageInput([warning_title, title, message])

        except Exception:
            return True, beam_lines

        return False, beam_lines

    def attribute_callback(self):

        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 0:
            line_ids = app().project.model.mesh.lines_from_model

        else:
            str_lines = self.lineEdit_selected_id.text()
            self.stop, line_ids = self.before_run.check_selected_ids(str_lines, "lines")
            if self.stop:
                return

        stop, beam_line_ids = self.filter_beam_lines(line_ids)
        app().main_window.set_selection(lines=beam_line_ids)
        if stop:
            return

        stop, increment_angle = self.check_xaxis_rotation_angle()
        if stop:
            self.lineEdit_increment_angle.setFocus()
            return

        for line_id in beam_line_ids:
            actual_angle = self.properties._get_property(
                "beam_xaxis_rotation", line_id=line_id
            )
            if actual_angle is None:
                actual_angle = 0.0

            rotation_angle = actual_angle + increment_angle

            self.preprocessor.set_beam_xaxis_rotation_by_lines(line_id, rotation_angle)
            self.properties._set_line_property(
                "beam_xaxis_rotation", rotation_angle, line_id
            )

        self.actions_to_finalize()

    def remove_callback(self):

        if self.lineEdit_selected_id.text() != "":
            line_id = int(self.lineEdit_selected_id.text())

            self.preprocessor.set_beam_xaxis_rotation_by_lines(line_id, 0)
            self.properties._remove_line_property("beam_xaxis_rotation", line_id)

            self.lineEdit_selected_id.clear()
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "X-axis beam rotations resetting"
        message = "Would you like to remove all x-axis rotations attributed to beam elements?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.lineEdit_selected_id.clear()
        self.lineEdit_increment_angle.clear()

        line_ids = list()
        for line_id, data in self.properties.line_properties.items():
            if "beam_xaxis_rotation" in data.keys():
                line_ids.append(line_id)

        self.preprocessor.set_beam_xaxis_rotation_by_lines(line_ids, 0)
        self.properties._remove_line_property("beam_xaxis_rotation", line_ids)

        self.actions_to_finalize()

    def load_lines_info(self):
        self.treeWidget_xaxis_rotation_angle.clear()
        for line_id, data in self.properties.line_properties.items():
            if "beam_xaxis_rotation" in data.keys():
                rot_angle = data["beam_xaxis_rotation"]
                new = QTreeWidgetItem([str(line_id), str(rot_angle)])
                for i in range(2):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_xaxis_rotation_angle.addTopLevelItem(new)
        self.update_tabs_visibility()

    def actions_to_finalize(self):
        self.lineEdit_actual_angle.clear()
        self.preprocessor.process_all_rotation_matrices()
        app().project.file.write_line_properties_in_file()
        self.load_lines_info()
        app().main_window.update_plots()