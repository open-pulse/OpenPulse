from PySide6.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class StructuralElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/structural_element_type_input.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self.element_type_change_callback()
        self.load_element_type_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.element_type = 'pipe_1'

        self.complete = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False

        self.before_run = app().project.get_pre_solution_model_checks()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection: QComboBox
        self.comboBox_element_type: QComboBox
        self.comboBox_capped_end: QComboBox
        self.comboBox_force_offset: QComboBox
        self.comboBox_wall_formulation: QComboBox

        # QLabel
        self.label_selected_id: QLabel
        self.label_capped_end: QLabel
        self.label_force_offset: QLabel
        self.label_wall_formulation: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_element_type: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_change_callback)
        self.comboBox_selection.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.element_type_attribution_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_selection_callback)
        #
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item)
        self.treeWidget_element_type.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.selection_callback()
        self.attribution_type_callback()

    def selection_callback(self):

        self.comboBox_selection.blockSignals(True)
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:

            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)

            self.comboBox_selection.setCurrentIndex(1)
            self.lineEdit_selected_id.setDisabled(False)

            if len(selected_lines) == 1:

                line_id = selected_lines[0]
                element_type = self.properties._get_property("structural_element_type", line_id=line_id)

                if element_type == 'pipe_1':
                    self.comboBox_element_type.setCurrentIndex(0)
                else:
                    self.comboBox_element_type.setCurrentIndex(1)

                capped_end = self.properties._get_property("capped_end", line_id=line_id)
                self.comboBox_capped_end.setCurrentIndex(bool(capped_end))

                force_offset = self.properties._get_property("force_offset", line_id=line_id)
                self.comboBox_force_offset.setCurrentIndex(bool(force_offset))

                wall_formulation = self.properties._get_property("wall_formulation", line_id=line_id)

                if wall_formulation == 'thin_wall': 
                    self.comboBox_wall_formulation.setCurrentIndex(0)
                elif wall_formulation == 'thick_wall':
                    self.comboBox_wall_formulation.setCurrentIndex(1)
                else:
                    if element_type == "pipe_1":
                        self.comboBox_wall_formulation.setCurrentIndex(2)

        self.comboBox_selection.blockSignals(False)

    def _config_widgets(self):
        self.treeWidget_element_type.setColumnWidth(0, 120)
        # self.treeWidget_element_type.setColumnWidth(1, 100)
        self.treeWidget_element_type.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def tab_selection_callback(self):
        if self.tabWidget_main.currentIndex() == 0:
            self.label_selected_id.setText("Selected ID:")
            self.attribution_type_callback()
        else:
            self.label_selected_id.setText("Selection:")
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)

    def attribution_type_callback(self):
        if self.comboBox_selection.currentIndex() == 0:
            self.lineEdit_selected_id.setDisabled(True)
            self.lineEdit_selected_id.setText("All lines")
        else:
            self.lineEdit_selected_id.setDisabled(False)
            if app().main_window.list_selected_lines():
                self.selection_callback()
            else:
                self.lineEdit_selected_id.setText("")

    def element_type_change_callback(self):
        index = self.comboBox_element_type.currentIndex()
        if index == 0:
            self.element_type = 'pipe_1'
            self.label_capped_end.setDisabled(False)
            self.label_force_offset.setDisabled(False)
            self.label_wall_formulation.setDisabled(False)
            self.comboBox_capped_end.setDisabled(False)
            self.comboBox_force_offset.setDisabled(False)
            self.comboBox_wall_formulation.setDisabled(False)
        
        elif index == 1:
            self.element_type = 'beam_1'
            self.label_capped_end.setDisabled(True)
            self.label_force_offset.setDisabled(True)
            self.label_wall_formulation.setDisabled(True)
            self.comboBox_capped_end.setDisabled(True)
            self.comboBox_force_offset.setDisabled(True)
            self.comboBox_wall_formulation.setDisabled(True)

    def check_element_type_changes(self):

        self.pipe_to_beam = False
        self.beam_to_pipe = False
        update_cross_section = False

        lines_to_update_cross_section = list()

        final_etype = self.element_type
        line_ids = app().main_window.list_selected_lines()

        if len(line_ids) == 0:
            line_ids = app().project.model.mesh.lines_from_model

        for line_id in line_ids:

            initial_etype = self.properties._get_property("structural_element_type", line_id=line_id)

            if initial_etype in ['pipe_1', None] and final_etype in ['beam_1']:

                update_cross_section = True
                self.pipe_to_beam = True
                lines_to_update_cross_section.append(line_id)

            elif initial_etype in ['beam_1', None] and final_etype in ['pipe_1']:

                update_cross_section = True
                self.beam_to_pipe = True
                lines_to_update_cross_section.append(line_id)

        if update_cross_section:

            self.update_modified_cross_sections(lines_to_update_cross_section)

            if initial_etype is not None:

                title = "Change in element type detected"

                if len(lines_to_update_cross_section) <= 20:
                    message = f"The element type previously defined at the {lines_to_update_cross_section} line(s) \n"
                else:
                    size = len(lines_to_update_cross_section)
                    message = f"The element type previously defined in {size} lines \n"

                message += "has been modified, therefore, it is necessary to update \n"
                message += "the cross-section(s) of this(ese) line(s) to continue."
                PrintMessageInput([window_title_2, title, message])

    def update_modified_cross_sections(self, lines_to_reset: list):
        app().project.model.preprocessor.set_cross_section_by_lines(lines_to_reset, None)
        app().project.model.preprocessor.add_expansion_joint_by_lines(lines_to_reset, None)
        app().project.model.preprocessor.add_valve_by_lines(lines_to_reset, None)

    def get_wall_formulation(self):
        index = self.comboBox_wall_formulation.currentIndex()
        if index == 0:
            return "thin_wall"
        else:
            return "thick_wall"

    def element_type_attribution_callback(self):

        self.check_element_type_changes()

        if self.comboBox_element_type.currentIndex() == 0:
            line_ids = app().project.model.mesh.lines_from_model
            print(f"[Set Structural Element Type] - {self.element_type} assigned to all lines")

        else:

            str_lines = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(str_lines, "lines")

            if stop:
                return

            if len(line_ids) <= 20:
                print(f"[Set Structural Element Type] - {self.element_type} assigned to {line_ids} lines")
            else:
                print(f"[Set Structural Element Type] - {self.element_type} assigned in {len(line_ids)} lines")

        if self.element_type == 'pipe_1':
            capped_end = True
            wall_formulation = self.get_wall_formulation()
        else:
            capped_end = False
            wall_formulation = None

        capped_end = bool(self.comboBox_capped_end.currentIndex())
        force_offset = bool(self.comboBox_force_offset.currentIndex())

        app().project.model.preprocessor.set_structural_element_type_by_lines(line_ids, self.element_type)
        app().project.model.preprocessor.set_capped_end_by_lines(line_ids, capped_end)
        app().project.model.preprocessor.set_structural_element_force_offset_by_lines(line_ids, force_offset)
        app().project.model.preprocessor.set_structural_element_wall_formulation_by_lines(line_ids, wall_formulation)

        self.properties._set_line_property("structural_element_type", self.element_type, line_ids)
        self.properties._set_line_property("capped_end", capped_end, line_ids)
        self.properties._set_line_property("force_offset", force_offset, line_ids)
        self.properties._set_line_property("wall_formulation", wall_formulation, line_ids)

        app().project.file.write_line_properties_in_file()

        self.complete = True
        self.close()

    def remove_callback(self):
        pass

    def reset_callback(self):

        self.hide()

        title = f"Resetting of structural element types"
        message = "Would you like to reset the structural element types from the model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            for (line_id, data) in self.properties.line_properties.items():
                if "structural_element_type" in data.keys():

                    app().project.model.preprocessor.set_structural_element_type_by_lines(line_id, "pipe_1")
                    app().project.model.preprocessor.set_capped_end_by_lines(line_id, True)
                    app().project.model.preprocessor.set_structural_element_force_offset_by_lines(line_id, "pipe_1")
                    app().project.model.preprocessor.set_structural_element_wall_formulation_by_lines(line_id, "pipe_1")

                    app().project.model.properties._remove_line_property("structural_element_type", line_id)
                    app().project.model.properties._remove_line_property("capped_end", line_id)

            app().project.file.write_line_properties_in_file()

            self.complete = True
            self.close()

    def on_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)

    def on_double_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)
        self.get_information(item)

    def load_element_type_info(self):

        self.treeWidget_element_type.clear()
        header = self.treeWidget_element_type.headerItem()

        header_labels = ["Element type", "Lines"]
        for col, label in enumerate(header_labels):
            header.setText(col, label)
            header.setTextAlignment(col, Qt.AlignCenter)

        aux = defaultdict(list)
        for line_id in self.properties.line_properties.keys():

            element_type = self.properties._get_property("structural_element_type", line_id=line_id)
            if element_type is None:
                continue

            aux[element_type].append(line_id)

        for key, line_ids in aux.items():
            item = QTreeWidgetItem([str(key), str(line_ids)])
            for col in range(len(header_labels)):
                item.setTextAlignment(col, Qt.AlignCenter)

            self.treeWidget_element_type.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "structural_element_type" in data.keys():
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

    def get_information(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                if item is None:
                    return

                self.close()
                key = item.text(0)

                data = dict()
                for line_id in self.properties.line_properties.keys():

                    element_type = self.properties._get_property("acoustic_element_type", line_id=line_id)
                    if element_type is None:
                        continue

                    if key == element_type:
                        element_data = [key]

                    data[line_id] = element_data

                header_labels = ["Line ID", "Element type"]
                GetInformationOfGroup(  group_label = "Element type",
                                        selection_label = "Line ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.element_type_attribution_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)