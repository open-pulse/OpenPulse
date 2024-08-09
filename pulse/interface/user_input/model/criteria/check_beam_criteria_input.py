from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.model.before_run import BeforeRun
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"

class CheckBeamCriteriaInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "criterias/check_beam_criteria.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self.define_qt_variables()
        self.create_connections()
        self.load_existing_sections()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _initialize(self):
        self.before_run = BeforeRun()

    def define_qt_variables(self):
        # QLineEdit
        self.lineEdit_beam_criteria : QLineEdit
        self.lineEdit_section_id : QLineEdit
        self.lineEdit_segment_id : QLineEdit
        # QPushButton
        self.pushButton_check_criteria : QPushButton
        self.pushButton_more_info : QPushButton
        # QTreeWidget
        self.treeWidget_non_beam_segments : QTreeWidget
        self.treeWidget_sections_parameters_by_lines : QTreeWidget

    def create_connections(self):
        self.pushButton_check_criteria.clicked.connect(self.check_beam_theory_criteria)
        self.pushButton_more_info.clicked.connect(self.get_beam_validity_criteria_info)
        self.treeWidget_non_beam_segments.itemClicked.connect(self.on_click_non_beam_segments)
        self.treeWidget_non_beam_segments.itemDoubleClicked.connect(self.on_double_click_non_beam_segments)
        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_line)
        self.config_treeWidget()

    def config_treeWidget(self):
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,120)
        self.treeWidget_non_beam_segments.setColumnWidth(0,40)
        self.treeWidget_non_beam_segments.setColumnWidth(1,80)
        self.treeWidget_non_beam_segments.setColumnWidth(2,240)

    def load_existing_sections(self):

        self.section_id_data_lines = dict()
        self.section_id_data_elements = dict()
        self.treeWidget_sections_parameters_by_lines.clear()
        self.section_data_lines, self.section_data_elements = self.project.file.get_cross_sections_from_file()

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
        self.treeWidget_non_beam_segments.clear()
        self.before_run.check_beam_theory_criteria()
        lineEdit = self.lineEdit_beam_criteria
        criteria = self.check_inputs(lineEdit, "Beam criteria")

        if criteria is not None:
            internal_index = 0
            lines_to_highlight = []
            self.non_beam_segments = []

            for section_id, criteria_data in self.before_run.one_section_one_line.items():
                # print(section_id, key, criteria_data["ratio"], criteria_data["lines"])
                [element_type, section_parameters, tag_type, tags] = self.section_data_lines[section_id]
                
                if criteria > criteria_data["ratio"]:
                    for line in criteria_data["line ID"]:
                        if line not in lines_to_highlight:
                            lines_to_highlight.append(line)
                            
                    internal_index += 1
                    data = [section_id, section_id, section_parameters, criteria_data["ratio"], criteria_data["line ID"]]
                    self.non_beam_data[internal_index] = data
                    if data not in self.non_beam_segments:
                        self.non_beam_segments.append(data)

            for section_id, data in self.before_run.one_section_multiple_lines.items():
                for key, criteria_data in data.items():
                    # print(section_id, key, criteria_data["ratio"], criteria_data["lines"])
                    [element_type, section_parameters, tag_type, tags] = self.section_data_lines[section_id]
                    
                    if criteria > criteria_data["ratio"]:
                        for line in criteria_data["lines"]:
                            if line not in lines_to_highlight:
                                lines_to_highlight.append(line)
                                
                        internal_index += 1
                        data = [section_id, key, section_parameters, criteria_data["ratio"], criteria_data["lines"]]
                        self.non_beam_data[internal_index] = data
                        if data not in self.non_beam_segments:
                            self.non_beam_segments.append(data)

            if len(lines_to_highlight)>0:
                app().main_window.set_selection(lines = lines_to_highlight)
        
            for index, data in self.non_beam_data.items():

                str_parameters = str(data[2])[1:-1]
                ratio = round(data[3], 4)
                lines = data[4]
                str_lines = str(lines)[1:-1]

                new = QTreeWidgetItem([str(index), str(ratio), str_parameters, str_lines])
                for i in range(4):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_non_beam_segments.addTopLevelItem(new)

    def on_click_non_beam_segments(self, item):
        self.lineEdit_segment_id.setText("")
        section_id = item.text(0)
        if section_id != "":
            self.lineEdit_segment_id.setText(section_id)

    def on_double_click_non_beam_segments(self, item):
        self.lineEdit_segment_id.setText("")
        section_id = item.text(0)
        if section_id != "":
            self.lineEdit_segment_id.setText(section_id)
            if int(section_id) in self.non_beam_data.keys():
                data = self.non_beam_data[int(section_id)]
                app().main_window.set_selection(lines = data[4])

    def on_click_treeWidget_section_parameters_by_line(self, item):
        self.lineEdit_section_id.setText("")
        key = item.text(0)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                self.lineEdit_section_id.setText(key)               

    def on_doubleClick_treeWidget_section_parameters_by_line(self, item):
        self.lineEdit_section_id.setText("")
        key = item.text(0)
        if key != "":
            if int(key) in self.section_data_lines.keys():
                self.lineEdit_section_id.setText(key)
                [_element_type, _section_parameters, _, section_lines] = self.section_data_lines[int(key)]
                app().main_window.set_selection(lines = section_lines)

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

        title = "Beam validity criteria relevant information"
        message = "1) The Beam Validity Criteria Tool has been developed to aid the user to find "
        message += "segments in the structure that potentially do not attempt the 3D Timoshenko beam theory. "
        #
        message += "\n\n2) It is known for structural engineers that to fit the Timoshenko beam "
        message += "theory hypothesis the ratio of length and cross-section predominant dimension " 
        message += "should reach, depending on geometry details, at least a factor of 10 or 20. "
        #
        message += "\n\n3) The current tool evaluates the ratios for each continuous segment with "
        message += "the same section and compared them with the user-defined value. "
        #
        message += "\n\n4) The segments that do not meet the criteria are then highlighted on OpenPulse's render. "
        #
        message += "\n\n5) This auxiliar tool does not intend to automate or replace the engineer criteria, "
        message += "but to provide an additional filter to focus on segments that could lead to physically "
        message += "non-representative results."
        #
        window_title = "Warning"
        PrintMessageInput([window_title_1, title, message], alignment=Qt.AlignJustify)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()