from collections import defaultdict
from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface import error_title, warning_title
from pulse.interface.ui_generated.model.setup.structural.structural_element_type_input_ui import (
    StructuralElementTypeInput_UI,
)
from pulse.interface.user_input.model.setup.general.get_information_of_group import (
    GetInformationOfGroup,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


class AssignmentType(IntEnum):
    ALL_LINES = 0
    SELECTED_LINES = 1


class ElementType(IntEnum):
    PIPE_1 = 0
    BEAM_1 = 1


class CappedEnd(IntEnum):
    DISABLED = 0
    ENABLED = 1


class ForceOffset(IntEnum):
    DISABLED = 0
    ENABLED = 1


class WallFormulation(IntEnum):
    THIN = 0
    THICK = 1
    NONE = 2


class StructuralElementTypeInput(StructuralElementTypeInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._create_connections()

        self.load_element_type_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _config_widgets(self):
        #
        for i, width in enumerate([120, 200]):
            self.treeWidget_lines_info.setColumnWidth(i, width)
            self.treeWidget_lines_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _initialize(self):

        self.complete = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False

        self.lines_to_update_cross_section = list()

        self.before_run = app().project.get_pre_solution_model_checks()

    def _create_connections(self):
        #
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_change_callback)
        self.comboBox_selection.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_lines_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_lines_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.selection_callback()
        self.attribution_type_callback()
        self.element_type_change_callback()

    def selection_callback(self):

        selected_lines = app().main_window.list_selected_lines()
        if not selected_lines:
            return
        
        text = ", ".join([str(i) for i in selected_lines])
        self.lineEdit_selected_id.setText(text)

        self.comboBox_selection.blockSignals(True)
        self.comboBox_selection.setCurrentIndex(AssignmentType.SELECTED_LINES)
        self.comboBox_selection.blockSignals(False)

        if len(selected_lines) != 1:
            return

        line_id = selected_lines[0]
        element_type = self.properties._get_property("structural_element_type", line_id = line_id)
        wall_formulation = self.properties._get_property("wall_formulation", line_id = line_id)

        if element_type == "pipe_1":
            self.comboBox_element_type.setCurrentIndex(ElementType.PIPE_1)
            if wall_formulation == 'thick_wall': 
                self.comboBox_wall_formulation.setCurrentIndex(WallFormulation.THICK)
            else:
                self.comboBox_wall_formulation.setCurrentIndex(WallFormulation.THIN)

        elif element_type == "beam_1":
            self.comboBox_element_type.setCurrentIndex(ElementType.BEAM_1)

        else:
            return

        force_offset = self.properties._get_property("force_offset", line_id = line_id)
        if force_offset is None:
            force_offset = True

        capped_end = self.properties._get_property("capped_end", line_id = line_id)
        if capped_end is None:
            capped_end = True

        self.comboBox_capped_end.setCurrentIndex(int(capped_end))
        self.comboBox_force_offset.setCurrentIndex(int(force_offset))

    def tab_event_callback(self):

        self.lineEdit_selected_id.clear()
        self.pushButton_remove.setDisabled(True)

        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.frame_selection.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

        if not tab_list:
            self.treeWidget_lines_info.clearSelection()
            return

        self.comboBox_selection.setCurrentIndex(AssignmentType.SELECTED_LINES)

    def attribution_type_callback(self):

        if self.comboBox_selection.currentIndex() == AssignmentType.ALL_LINES:
            self.lineEdit_selected_id.setDisabled(True)
            self.lineEdit_selected_id.setText("All lines")
            return

        self.lineEdit_selected_id.setDisabled(False)
        if app().main_window.list_selected_lines():
            self.selection_callback()
        else:
            self.lineEdit_selected_id.clear()

    def element_type_change_callback(self):

        index = self.comboBox_element_type.currentIndex()
        if index == ElementType.PIPE_1:
            self.label_capped_end.setDisabled(False)
            self.label_force_offset.setDisabled(False)
            self.label_wall_formulation.setDisabled(False)
            self.comboBox_capped_end.setDisabled(False)
            self.comboBox_force_offset.setDisabled(False)
            self.comboBox_wall_formulation.setDisabled(False)

        elif index == ElementType.BEAM_1:
            self.label_capped_end.setDisabled(True)
            self.label_force_offset.setDisabled(True)
            self.label_wall_formulation.setDisabled(True)
            self.comboBox_capped_end.setDisabled(True)
            self.comboBox_force_offset.setDisabled(True)
            self.comboBox_wall_formulation.setDisabled(True)

    def get_elementy_type(self) -> str:

        if self.comboBox_element_type.currentIndex() == ElementType.PIPE_1:
            return "pipe_1"
        else:
            return "beam_1"

    def get_wall_formulation(self):

        index = self.comboBox_wall_formulation.currentIndex()
        if index == WallFormulation.THIN:
            return "thin_wall"

        elif index == WallFormulation.THICK:
            return "thick_wall"

        else:
            return None

    def check_element_type_changes(self):

        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.lines_to_update_cross_section = list()

        line_ids = app().main_window.list_selected_lines()
        if len(line_ids) == 0:
            line_ids = app().project.model.mesh.lines_from_model

        final_etype = self.get_elementy_type()

        for line_id in line_ids:

            initial_etype = self.properties._get_property("structural_element_type", line_id=line_id)

            if initial_etype in ['pipe_1', None] and final_etype in ['beam_1']:
                self.pipe_to_beam = True
                self.lines_to_update_cross_section.append(line_id)

            elif initial_etype in ['beam_1', None] and final_etype in ['pipe_1']:
                self.beam_to_pipe = True
                self.lines_to_update_cross_section.append(line_id)

        if not self.lines_to_update_cross_section:
            return

        self.update_modified_cross_sections(self.lines_to_update_cross_section)

        if initial_etype is None:
            return

        self.hide()
        title = "Change in element type detected"
        message = f"The element type previously defined at the lines {self.lines_to_update_cross_section} "
        message += "has been modified, therefore, it is necessary to update "
        message += "the cross-section(s) of this(ese) line(s) to continue."

        PrintMessageInput([warning_title, title, message])

    def update_modified_cross_sections(self, lines_to_reset: list):
        app().project.model.preprocessor.set_cross_section_by_lines(lines_to_reset, None)
        app().project.model.preprocessor.add_expansion_joint_by_lines(lines_to_reset, None)
        app().project.model.preprocessor.add_valve_by_lines(lines_to_reset, None)

    def attribute_callback(self):

        self.check_element_type_changes()

        if self.comboBox_element_type.currentIndex() == AssignmentType.ALL_LINES:
            line_ids = app().project.model.mesh.lines_from_model

        else:
            str_lines = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(str_lines, "lines")
            if stop:
                return
            
        element_type = self.get_elementy_type()

        if self.comboBox_element_type.currentIndex() == ElementType.PIPE_1:
            wall_formulation = self.get_wall_formulation()
            capped_end = self.comboBox_capped_end.currentIndex() == CappedEnd.ENABLED
            force_offset = self.comboBox_force_offset.currentIndex() == ForceOffset.ENABLED

        else:
            wall_formulation = None
            capped_end = False

        app().project.model.preprocessor.set_structural_element_type_by_lines(line_ids, element_type)
        app().project.model.preprocessor.set_capped_end_by_lines(line_ids, capped_end)
        app().project.model.preprocessor.set_structural_element_force_offset_by_lines(line_ids, force_offset)
        app().project.model.preprocessor.set_structural_element_wall_formulation_by_lines(line_ids, wall_formulation)

        self.properties._set_line_property("structural_element_type", element_type, line_ids)
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

        title = "Structural element types resetting"
        message = "Would you like to reset the structural element types from the model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

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

    def on_click_item(self, item: QTreeWidgetItem):
        self.lineEdit_selected_id.setText(item.text(2))

    def on_double_click_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)
        self.get_information(item)

    def load_element_type_info(self):

        self.treeWidget_lines_info.clear()
        header = self.treeWidget_lines_info.headerItem()

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

            self.treeWidget_lines_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "structural_element_type" in data.keys():
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

    def get_information(self, item: QTreeWidgetItem):
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
                PrintMessageInput([warning_title, title, message])

        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)