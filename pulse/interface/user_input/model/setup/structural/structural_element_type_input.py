from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class StructuralElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/structural_element_type_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.update()
        self.attribution_type_callback()
        self.element_type_change_callback()
        self.load_element_type_info()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

        self.element_type = 'pipe_1'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.list_lines_to_update_cross_section = []

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selection : QComboBox
        self.comboBox_element_type : QComboBox
        self.comboBox_capped_end : QComboBox
        self.comboBox_force_offset : QComboBox
        self.comboBox_wall_formulation : QComboBox
        # QLabel
        self.label_selected_id : QLabel
        self.label_capped_end : QLabel
        self.label_force_offset : QLabel
        self.label_wall_formulation : QLabel
        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset : QPushButton
        # QTabWidget
        self.tabWidget_main : QTabWidget
        # QTreeWidget
        self.treeWidget_element_type : QTreeWidget

    def _create_connections(self):
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_change_callback)
        self.comboBox_selection.currentIndexChanged.connect(self.attribution_type_callback)
        self.pushButton_confirm.clicked.connect(self.confirm_button_clicked)
        self.pushButton_reset.clicked.connect(self.reset_element_type)
        self.tabWidget_main.currentChanged.connect(self.tab_selection_callback)
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_element_type.itemDoubleClicked.connect(self.on_double_click_item)

    def _config_widgets(self):
        self.treeWidget_element_type.setColumnWidth(0, 120)
        # self.treeWidget_element_type.setColumnWidth(1, 100)
        self.treeWidget_element_type.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def tab_selection_callback(self):
        
        if self.comboBox_selection.currentIndex() == 1:
            self.lineEdit_selected_id.setDisabled(False)
        
        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == 0:
            self.label_selected_id.setText("Selection ID:")
            self.lineEdit_selected_id.setText("")

        else:
            self.label_selected_id.setText("Selection ID:")
            self.lineEdit_selected_id.setText("")

    def attribution_type_callback(self):
        index = self.comboBox_selection.currentIndex()
        if index == 0:
            self.lineEdit_selected_id.setDisabled(True)
            self.lineEdit_selected_id.setText("All lines")
        elif index == 1:
            self.lineEdit_selected_id.setDisabled(False)
            line_ids  = app().main_window.list_selected_entities()
            if line_ids:
                self.write_ids(line_ids)
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
        self.update_cross_section = False

        final_etype = self.element_type
        line_ids = app().main_window.list_selected_entities()

        if len(line_ids) == 0:
            line_ids = self.preprocessor.all_lines

        for line_id in line_ids:

            entity = self.dict_tag_to_entity[line_id]
            initial_etype = entity.structural_element_type

            if initial_etype in ['pipe_1', None] and final_etype in ['beam_1']:

                self.update_cross_section = True
                self.pipe_to_beam = True
                self.list_lines_to_update_cross_section.append(line_id)

            elif initial_etype in ['beam_1', None] and final_etype in ['pipe_1']:

                self.update_cross_section = True
                self.beam_to_pipe = True
                self.list_lines_to_update_cross_section.append(line_id)

        if self.update_cross_section:
            self.update_modified_cross_sections()
            if initial_etype is not None:
                title = "Change in element type detected"
                if len(self.list_lines_to_update_cross_section) <= 20:
                    message = f"The element type previously defined at the {self.list_lines_to_update_cross_section} line(s) \n"
                else:
                    size = len(self.list_lines_to_update_cross_section)
                    message = f"The element type previously defined in {size} lines \n"
                message += "has been modified, therefore, it is necessary to update \n"
                message += "the cross-section(s) of this(ese) line(s) to continue."
                PrintMessageInput([window_title_2, title, message])
            
    def update_modified_cross_sections(self):
        lines_to_reset = self.list_lines_to_update_cross_section
        self.project.set_cross_section_by_lines(lines_to_reset, None)
        
        # final_etype = self.element_type
        # for tag in tags:
        #     initial_etype = self.dict_tag_to_entity[tag].structural_element_type
        #     if initial_etype in ['pipe_1'] and final_etype in ['beam_1']:
        #         self.project.set_cross_section_by_lines(tag, None)
        #     elif initial_etype in ['beam_1'] and final_etype in ['pipe_1']:
        #         self.project.set_cross_section_by_lines(tag, None)

    def confirm_button_clicked(self):

        index = self.comboBox_element_type.currentIndex()

        if index == 0:
            self.check_element_type_changes()
            lines = self.preprocessor.all_lines
            print(f"[Set Structural Element Type] - {self.element_type} assigned to all lines")

        elif index == 1:

            lineEdit_lineID = self.lineEdit_selected_id.text()
            self.stop, self.typed_lines = self.before_run.check_selected_ids(lineEdit_lineID, "lines")

            if self.stop:
                return

            self.check_element_type_changes()
            lines = self.typed_lines

            if len(self.typed_lines) <= 20:
                print(f"[Set Structural Element Type] - {self.element_type} assigned to {self.typed_lines} lines")
            else:
                print(f"[Set Structural Element Type] - {self.element_type} assigned in {len(self.typed_lines)} lines")

        self.project.set_structural_element_type_by_lines(lines, self.element_type)
        
        capped_end = False
        if self.element_type == 'pipe_1':
            if self.comboBox_capped_end.currentIndex() == 0:
                capped_end = True
            wall_formulation = self.get_wall_formulation()
            self.project.set_capped_end_by_lines(lines, capped_end)
            self.project.set_structural_element_wall_formulation_by_lines(lines, wall_formulation)

        else:
            self.project.set_structural_element_wall_formulation_by_lines(lines, None)
            self.project.set_capped_end_by_lines(lines, False)

        self.project.set_structural_element_force_offset_by_lines(lines, self.force_offset)

        self.complete = True
        self.close()

    def get_wall_formulation(self):
        index = self.comboBox_wall_formulation.currentIndex()
        if index == 0:
            return "thin_wall"
        else:
            return "thick_wall"

    def on_click_item_line(self, item):
        self.lineEdit_selected_id.setText(item.text(0))

    def on_double_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.get_information(item)

    def reset_element_type(self):
        self.element_type = "pipe_1"
        lines = self.preprocessor.all_lines
        self.project.set_structural_element_type_by_lines(lines, self.element_type)
        self.complete = True
        self.close()
        title = "Resetting process complete"
        message = "The structural element type has been reset to the default option 'pipe_1'."
        PrintMessageInput([window_title_2, title, message], auto_close=True)

    def load_element_type_info(self):
        self.treeWidget_element_type.clear()
        for key, lines in self.preprocessor.dict_structural_element_type_to_lines.items():
            item = QTreeWidgetItem([str(key), str(lines)])
            item.setTextAlignment(0, Qt.AlignCenter)
            item.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_element_type.addTopLevelItem(item)
        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.dict_structural_element_type_to_lines) == 0:
            self.tabWidget_main.setCurrentIndex(0)
            self.tabWidget_main.setTabVisible(1, False)
        else:
            self.tabWidget_main.setTabVisible(1, True)

    def get_information(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                if item is None:
                    return

                self.close()
                key = item.text(0)

                data = dict()
                for line_id in self.preprocessor.dict_structural_element_type_to_lines[key]:
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

    def update(self):

        line_ids  = app().main_window.list_selected_entities()
        if line_ids:

            self.comboBox_selection.setCurrentIndex(1)
            self.write_ids(line_ids)
            self.lineEdit_selected_id.setDisabled(False)

            if len(line_ids) == 1:

                entity = self.preprocessor.dict_tag_to_entity[line_ids[0]]

                element_type = entity.structural_element_type
                if element_type == 'pipe_1':
                    self.comboBox_element_type.setCurrentIndex(0)
                else:
                    self.comboBox_element_type.setCurrentIndex(1)

                wall_formulation = entity.structural_element_wall_formulation
                if wall_formulation == 'thin_wall': 
                    self.comboBox_wall_formulation.setCurrentIndex(0)
                elif wall_formulation == 'thick_wall':
                    self.comboBox_wall_formulation.setCurrentIndex(1)
                elif wall_formulation is None:
                    if element_type == "pipe_1":
                        self.comboBox_wall_formulation.setCurrentIndex(1)

                if entity.capped_end:
                    self.comboBox_capped_end.setCurrentIndex(0)
                else:
                    self.comboBox_capped_end.setCurrentIndex(1)

                if entity.force_offset == 1:
                    self.comboBox_force_offset.setCurrentIndex(0)
                else:
                    self.comboBox_force_offset.setCurrentIndex(1)

        else:
            self.comboBox_selection.setCurrentIndex(0)
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setDisabled(True)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    # def group_remove(self):
    #     key = self.lineEdit_selected_group.text()
    #     if key != "":
    #         try:
    #             lines = self.preprocessor.dict_structural_element_type_to_lines[key]
    #             for line in lines:
    #                 element_type = ""
    #                 self.project.set_structural_element_type_by_lines(line, element_type, remove=True)
    #         except Exception as error:
    #             title = "ERROR WHILE DELETING GROUP OF LINES"
    #             message = str(error)
    #             PrintMessageInput([title, message, window_title1])
    #         self.load_element_type_info()