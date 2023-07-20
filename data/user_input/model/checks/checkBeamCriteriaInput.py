from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

from pulse.preprocessing.before_run import BeforeRun
from data.user_input.project.printMessageInput import PrintMessageInput

window_title = "ERROR"

class CheckBeamCriteriaInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/Model/Checks/checkBeamCriteriaInput.ui'), self)
        
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.opv = opv
        self.opv.setInputObject(self)
        self.before_run = BeforeRun(project, opv)

        self.initialize_Qt_variables()
        self.create_connections()
        self.load_existing_sections()

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F3:
            self.close()

    def initialize_Qt_variables(self):
        """
        """
        self.lineEdit_beam_criteria = self.findChild(QLineEdit, "lineEdit_beam_criteria")
        self.lineEdit_section_id = self.findChild(QLineEdit, "lineEdit_section_id")
        self.lineEdit_segment_id = self.findChild(QLineEdit, "lineEdit_segment_id")

        self.pushButton_check_criteria = self.findChild(QPushButton, "pushButton_check_criteria")
        self.pushButton_more_info = self.findChild(QPushButton, "pushButton_more_info")
        self.treeWidget_non_beam_segments = self.findChild(QTreeWidget, "treeWidget_non_beam_segments")
        self.treeWidget_sections_parameters_by_lines = self.findChild(QTreeWidget, "treeWidget_sections_parameters_by_lines")

    def create_connections(self):
        """
        """
        self.pushButton_check_criteria.clicked.connect(self.check_beam_theory_criteria)
        self.pushButton_more_info.clicked.connect(self.get_beam_validity_criteria_info)
        self.treeWidget_non_beam_segments.itemClicked.connect(self.on_click_non_beam_segments)
        self.treeWidget_non_beam_segments.itemDoubleClicked.connect(self.on_double_click_non_beam_segments)
        self.treeWidget_sections_parameters_by_lines.itemClicked.connect(self.on_click_treeWidget_section_parameters_by_line)
        self.treeWidget_sections_parameters_by_lines.itemDoubleClicked.connect(self.on_doubleClick_treeWidget_section_parameters_by_line)

    def config_treeWidget(self):
        """
        """
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        #
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(0,40)
        self.treeWidget_sections_parameters_by_lines.setColumnWidth(1,120)
        self.treeWidget_sections_parameters_by_lines.setFont(font)
        #
        self.treeWidget_non_beam_segments.setColumnWidth(0,40)
        self.treeWidget_non_beam_segments.setColumnWidth(1,80)
        self.treeWidget_non_beam_segments.setColumnWidth(2,240)
        self.treeWidget_non_beam_segments.setFont(font)


    def load_existing_sections(self):
        """
        """
        self.config_treeWidget()
        self.section_id_data_lines = {}
        self.section_id_data_elements = {}
        self.treeWidget_sections_parameters_by_lines.clear()
        self.section_data_lines, self.section_data_elements = self.project.file.get_cross_sections_from_file()

        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_lines.items():
            self.section_id_data_lines[section_id] = [tag_type, tags]
            str_parameters = str(section_parameters)[1:-1]
            new = QTreeWidgetItem([str(section_id), element_type, str_parameters])
            for i in range(3):
                new.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_sections_parameters_by_lines.addTopLevelItem(new)


    def check_beam_theory_criteria(self):
        """
        """
        self.non_beam_data = {}
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
                self.opv.opvRenderer.highlight_lines(lines_to_highlight)
        
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
                self.opv.opvRenderer.highlight_lines(data[4])


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
                self.opv.opvRenderer.highlight_lines(section_lines)


    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False):
        """
        """
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
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
                    else:
                        if out <= 0:
                    
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            PrintMessageInput([title, message, window_title])
                            self.stop = True
                            return None
            except Exception as _err:
        
                message = f"Wrong input for {label}.\n\n"
                message += "Error details: " + str(_err)
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return None
        else:
            if zero_included:
                return float(0)
            else: 
        
                message = f"Insert some value at the {label} input field."
                PrintMessageInput([title, message, window_title])                   
                self.stop = True
                return None
        return out
    
    def get_beam_validity_criteria_info(self):
        """
        """
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
        PrintMessageInput([title, message, "INFORMATION"], alignment=Qt.AlignJustify)