from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.model.before_run import BeforeRun
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"


class CheckBeamCriteriaInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "criterias/beam_criteria_assistant.ui"
        load_ui(ui_path, self, UI_DIR)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self.define_qt_variables()
        self.create_connections()
        self._config_widgets()

        self.load_existing_sections()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _config_widgets(self):
        pass

    def _initialize(self):
        self.keep_window_open = True
        self.before_run = BeforeRun()

    def define_qt_variables(self):

        # QLineEdit
        self.lineEdit_beam_criteria: QLineEdit
        self.lineEdit_section_id: QLineEdit

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_check_criteria: QPushButton
        self.pushButton_more_info: QPushButton

        # QTreeWidget
        self.treeWidget_non_beam_segments: QTreeWidget
        self.treeWidget_sections_parameters_by_lines: QTreeWidget

    def create_connections(self):
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_check_criteria.clicked.connect(self.check_beam_theory_criteria)
        self.pushButton_more_info.clicked.connect(self.get_beam_validity_criteria_info)
        #
        self.treeWidget_non_beam_segments.itemClicked.connect(self.on_click_non_beam_segments)
        self.treeWidget_non_beam_segments.itemDoubleClicked.connect(self.on_double_click_non_beam_segments)
        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_section_parameters_by_line)
        #
        self.config_treeWidget()

    def config_treeWidget(self):

        for i, w in enumerate([80, 120, 160]):
            self.treeWidget_sections_parameters_by_lines.setColumnWidth(i, w)
            self.treeWidget_sections_parameters_by_lines.headerItem().setTextAlignment(i, Qt.AlignCenter)

        for i, w in enumerate([80, 80, 200, 60]):
            self.treeWidget_non_beam_segments.setColumnWidth(i, w)
            self.treeWidget_non_beam_segments.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def load_existing_sections(self):

        self.section_id_data_lines = dict()
        self.section_id_data_elements = dict()
        self.treeWidget_sections_parameters_by_lines.clear()
        self.section_data_lines = app().loader.get_cross_sections_from_file()

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_lines.items():
            if section_parameters:
                self.section_id_data_lines[section_id] = [tag_type, tags]
                str_parameters = str(section_parameters)[1:-1]
    
                new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
    
                for i in range(3):
                    new.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)

    def check_beam_theory_criteria(self):

        self.non_beam_data = dict()

        lineEdit = self.lineEdit_beam_criteria
        criteria = self.check_inputs(lineEdit, "Beam criteria")

        self.treeWidget_non_beam_segments.clear()
        self.before_run.check_beam_theory_criteria()

        if criteria is not None:

            internal_index = 0
            lines_to_highlight = list()
            non_beam_segments = list()

            for section_id, data in self.before_run.one_section_multiple_lines.items():

                data: dict
                for criteria_data in data.values():
                    
                    if criteria > criteria_data["ratio"]:
                        for line in criteria_data["lines"]:
                            if line not in lines_to_highlight:
                                lines_to_highlight.append(line)
                                
                        internal_index += 1
                        data = [section_id, criteria_data["ratio"], criteria_data["lines"]]
                        self.non_beam_data[internal_index] = data
                        if data not in non_beam_segments:
                            non_beam_segments.append(data)

            if lines_to_highlight:
                app().main_window.set_selection(lines = lines_to_highlight)

            if self.non_beam_data:

                for group_id, data in self.non_beam_data.items():

                    section_index = data[0]
                    ratio = round(data[1], 4)
                    lines = data[2]

                    new = QTreeWidgetItem([str(group_id), str(section_index), str(lines)[1:-1], str(ratio)])

                    for i in range(4):
                        new.setTextAlignment(i, Qt.AlignCenter)

                    self.treeWidget_non_beam_segments.addTopLevelItem(new)

            else:

                self.hide()
                title = "No branches out of user-defined criteria"
                message = "The all piping branches from current structure meets "
                message += "the user-defined 'L/d' beam validity criteria."
                PrintMessageInput([window_title_2, title, message])

    def on_click_non_beam_segments(self, item):
        section_id = item.text(0)
        if section_id != "":
            if int(section_id) in self.non_beam_data.keys():
                data = self.non_beam_data[int(section_id)]
                lines_to_highlight = data[2]
                app().main_window.set_selection(lines = lines_to_highlight)

    def on_double_click_non_beam_segments(self, item):
        self.on_double_click_non_beam_segments(item)

    def on_click_section_parameters_by_line(self, item):
        self.lineEdit_section_id.setText("")
        key = item.text(0)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                self.lineEdit_section_id.setText(key)
                *_, section_lines = self.section_data_lines[int(key)]
                app().main_window.set_selection(lines = section_lines)           

    def on_doubleClick_section_parameters_by_line(self, item):
        self.on_click_section_parameters_by_line(item)

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False):

        self.stop = False
        title = "Invalid value typed at criteria input field"
        if lineEdit.text() != "":
            try:
                out = float(lineEdit.text())
                if only_positive:
                    if zero_included:
                        if out < 0:
                    
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            PrintMessageInput([window_title_1, title, message])
                            self.stop = True
                            return None
                    else:
                        if out <= 0:
                    
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([window_title_1, title, message])
                            self.stop = True
                            return None
            except Exception as _err:
        
                message = f"Wrong input for {label}.\n\n"
                message += "Error details: " + str(_err)
                PrintMessageInput([window_title_1, title, message])
                self.stop = True
                return None
        else:
            if zero_included:
                return float(0)
            else: 
        
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([window_title_1, title, message])                   
                self.stop = True
                return None
        return out
    
    def get_beam_validity_criteria_info(self):

        self.hide()

        title = "Beam validity criteria relevant information"
        message = "1) The Beam Validity Criteria Tool has been developed to aid the user in finding "
        message += "branches that potentially do not fit the 3D Timoshenko beam theory;"
        #
        message += "\n\n2) It is known for structural engineers that to fit the Timoshenko beam "
        message += "theory hypothesis the ratio of length and cross-section predominant dimension " 
        message += "should reach, depending on geometry details, at least a factor of 10 or 20;"
        #
        message += "\n\n3) The current tool evaluates the ratios for each continuous segment with "
        message += "the same section and compared them with the user-defined value;"
        #
        message += "\n\n4) The segments that do not meet the criteria are then highlighted on the OpenPulse's render;"
        #
        message += "\n\n5) This auxiliar tool does not intend to automate or replace the engineer criteria, "
        message += "but to provide an additional filter to focus on segments that could lead to physically "
        message += "non-representative results."
        #
        PrintMessageInput([window_title_1, title, message], alignment=Qt.AlignJustify)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)