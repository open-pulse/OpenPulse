from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import configparser

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class BeamXaxisRotationInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/Setup/Structural/beamXaxisRotationInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_id = self.opv.getListPickedLines()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        # self.typed_lines = []
        self.dict_entities = project.preprocessor.dict_tag_to_entity
        self.index = 0
        self.element_type = 'pipe_1'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.list_lines_to_update_cross_section = []
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.QLabel_selected_ID = self.findChild(QLabel, "QLabel_selected_ID")
        self.QLabel_selected_ID.setText("Selected lines:")
        # self.lineEdit_selected_ID.setDisabled(True)
        # self.lineEdit_selected_group = self.findChild(QLineEdit, 'lineEdit_selected_group')
        # self.lineEdit_selected_group.setDisabled(True)

        self.lineEdit_xaxis_rotation_increment_angle = self.findChild(QLineEdit, "lineEdit_xaxis_rotation_increment_angle")
        self.lineEdit_xaxis_rotation_actual_angle = self.findChild(QLineEdit, "lineEdit_xaxis_rotation_actual_angle")
        self.lineEdit_xaxis_rotation_increment_angle.setDisabled(False)
        self.lineEdit_xaxis_rotation_actual_angle.setDisabled(True)

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()

        self.treeWidget_xaxis_rotation_angle = self.findChild(QTreeWidget, 'treeWidget_xaxis_rotation_angle')
        self.treeWidget_xaxis_rotation_angle.setColumnWidth(0, 140)
        # self.treeWidget_xaxis_rotation_angle.setColumnWidth(1, 100)
        self.treeWidget_xaxis_rotation_angle.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_xaxis_rotation_angle.headerItem().setText(0, "ANGLE [degrees]")
        self.treeWidget_xaxis_rotation_angle.headerItem().setText(1, "LINES")
        # self.treeWidget_xaxis_rotation_angle.headerItem().setBackground(0,QBrush(QColor(100,100,100,100)))
        # self.treeWidget_xaxis_rotation_angle.headerItem().setBackground(1,QBrush(QColor(100,100,100,100)))
        # self.treeWidget_xaxis_rotation_angle.headerItem().setForeground(0,QBrush(QColor(100,100,100)))
        # self.treeWidget_xaxis_rotation_angle.headerItem().setForeground(1,QBrush(QColor(100,100,100)))
        # print(self.treeWidget_xaxis_rotation_angle.headerItem().background(0).color().getRgb())
        
        self.tabWidget_xaxis_rotation_angle = self.findChild(QTabWidget, 'tabWidget_xaxis_rotation_angle')
        self.tabWidget_xaxis_rotation_angle.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_xaxis_rotation_angle.currentIndex()

        self.tab_setup = self.tabWidget_xaxis_rotation_angle.findChild(QWidget, "tab_setup")
        self.tab_remove = self.tabWidget_xaxis_rotation_angle.findChild(QWidget, "tab_remove")       

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_remove.clicked.connect(self.remove_selected_beam_xaxis_rotation)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information)
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_input)
        self.pushButton_get_information.setDisabled(True)
        # self.pushButton_remove.setDisabled(True)

        if self.lines_id != []:
            self.write_ids(self.lines_id)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(False)
            if len(self.lines_id) == 1:
                entity = self.preprocessor.dict_tag_to_entity[self.lines_id[0]]
                angle = entity.xaxis_beam_rotation
                self.lineEdit_xaxis_rotation_actual_angle.setText(str(angle))
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(True)

        self.load_beam_xaxis_rotation_info()
        self.exec()
    
    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_input()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def update(self):
        self.lines_id  = self.opv.getListPickedLines()
        self.pushButton_confirm.setDisabled(False)

        if self.lines_id != []:
            self.radioButton_selected_lines.setChecked(True)    
            for line_id in self.lines_id:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type != "beam_1":
                    self.lineEdit_xaxis_rotation_actual_angle.setText("")
                    self.lineEdit_selected_ID.setText("")
                    self.pushButton_confirm.setDisabled(True)
                    return
            if len(self.lines_id) == 1:
                entity = self.preprocessor.dict_tag_to_entity[self.lines_id[0]]
                angle = entity.xaxis_beam_rotation
                self.lineEdit_xaxis_rotation_actual_angle.setText(str(angle))
            else:
                self.lineEdit_xaxis_rotation_actual_angle.setText("")
            self.write_ids(self.lines_id)            
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.lines_id  = self.opv.getListPickedLines()
        if self.flagEntity:
            if self.lines_id != []:
                self.write_ids(self.lines_id)
            elif self.lineEdit_selected_ID.text() not in ["", "All lines"]:
                pass
            else:
                self.lineEdit_selected_ID.setText("")
            if self.currentTab_ == 0:
                self.lineEdit_selected_ID.setDisabled(False)
        elif self.flagAll:
            if self.tabWidget_xaxis_rotation_angle.currentIndex() == 0:
                self.lineEdit_selected_ID.setText("All lines")
                self.lineEdit_selected_ID.setDisabled(True)
            else:
                self.radioButton_selected_lines.setChecked(True)

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_xaxis_rotation_angle.currentIndex()
        if self.currentTab_ == 0:
            self.QLabel_selected_ID.setText("Selected lines:")
            self.radioButton_selected_lines.setDisabled(False) 
            self.radioButton_all.setDisabled(False)           
            self.radioButtonEvent()
        elif self.currentTab_ == 1:
            self.QLabel_selected_ID.setText("Group of lines:")
            self.lineEdit_selected_ID.setText("")
            self.lineEdit_selected_ID.setDisabled(True)
            self.radioButton_selected_lines.setChecked(True)
            self.radioButton_selected_lines.setDisabled(True)
            self.radioButton_all.setDisabled(True)
            self.set_disable_tab_1_buttons(True)
    
    def set_disable_tab_1_buttons(self, disable):
        self.pushButton_remove.setDisabled(disable)
        self.pushButton_get_information.setDisabled(disable) 

    def on_click_item_line(self, item):
        self.selected_key = item.text(0)
        self.lineEdit_selected_ID.setText(item.text(1))
        if self.lineEdit_selected_ID.text() != "":
            self.radioButton_selected_lines.setChecked(True)
            self.flagEntity = self.radioButton_selected_lines.isChecked()
            self.set_disable_tab_1_buttons(False)
        else:
            self.set_disable_tab_1_buttons(True)

    def confirm_input(self):
        if self.check_xaxis_rotation_angle():
            return    
        if self.flagEntity:

            lineEdit_lineID = self.lineEdit_selected_ID.text()
            self.stop, lines = self.before_run.check_input_LineID(lineEdit_lineID)
            if self.stop:
                return
 
        elif self.flagAll:
            lines = self.project.preprocessor.all_lines
        for line in lines:
            self.project.set_beam_xaxis_rotation_by_line(line, self.rotation_angle)
        self.close()
        self.update_plots()

    def update_plots(self):
        self.load_beam_xaxis_rotation_info()
        self.project.preprocessor.process_all_rotation_matrices() 
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntitiesWithCrossSection() 

    def check_xaxis_rotation_angle(self):
        self.rotation_angle = 0
        try:
            self.rotation_angle = float(self.lineEdit_xaxis_rotation_increment_angle.text())
        except Exception as error:
            self.print_error_message()
            return True
        return False

    def print_error_message(self):
        window_title = "ERROR"
        message_title = f"Invalid X-axis Rotation Angle"
        message = f"Please, inform a valid number at the 'Rotation angle' input field to continue."
        message += "The input value should be a float or an integer number."
        PrintMessageInput([message_title, message, window_title])

    def load_beam_xaxis_rotation_info(self):
        self.treeWidget_xaxis_rotation_angle.clear()
        _dict = self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines
        if len(_dict) == 0:
            self.tabWidget_xaxis_rotation_angle.setTabEnabled(1, False)
            return
        else:
            self.tabWidget_xaxis_rotation_angle.setTabEnabled(1, True)
            for key, lines in _dict.items():
                new = QTreeWidgetItem([str(key), str(lines)[1:-1]])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                # new.setBackground(0,QBrush(QColor(20,20,20,80)))
                # new.setBackground(1,QBrush(QColor(20,20,20,80)))
                self.treeWidget_xaxis_rotation_angle.addTopLevelItem(new)  

    def remove_selected_beam_xaxis_rotation(self):
        if self.selected_key == "":
            return
        lines = self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines[self.selected_key]
        self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines.pop(self.selected_key)
        for line in lines:
            delta_angle = - self.project.preprocessor.dict_lines_to_rotation_angles[line]
            self.project.set_beam_xaxis_rotation_by_line(line, delta_angle)
        self.update_plots()
        title = "X-axis rotation angle removal"
        message = f"The x-axis rotation angle attributed to the lines {lines} has been removed from the current model setup.\n\n\n "
        message += "Press Close button to continue."
        PrintMessageInput([title, message, window_title2])
    
    def reset_all(self):
        title = "Remove all x-axis rotations attributed to the model"
        message = "Are you really sure you want to remove all x-axis rotations associated to beam elements?\n\n\n"
        message += "Press the Continue button to proceed with removal or press Cancel or Close buttons to abort the current operation."
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._doNotRun:
            return

        if read._continue:
            if len(self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines) > 0:
                for line in self.project.preprocessor.all_lines:
                    delta_angle = - self.project.preprocessor.dict_lines_to_rotation_angles[line]
                    self.project.set_beam_xaxis_rotation_by_line(line, delta_angle)
                self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines.clear()
                self.project.preprocessor.create_dict_lines_to_rotation_angles()
                self.update_plots()

    def get_information(self):
        try:
            if self.lineEdit_selected_ID.text() != "":           
                # key = self.lineEdit_selected_ID.text()
                read = GetInformationOfGroup(self.project, self.selected_key)
            else:
                title = "UNSELECTED GROUP OF LINES"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([title, message, window_title2])
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([title, message, window_title1])


class GetInformationOfGroup(QDialog):
    def __init__(self, project, key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/Info/getGroupInformationInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.key = key

        # self.lines_removed = False

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, "Line")
        self.treeWidget_group_info.headerItem().setText(1, "Angle [degrees]")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        
        self.treeWidget_group_info.setColumnWidth(0, 130)
        self.treeWidget_group_info.setColumnWidth(1, 140)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.load_group_info()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        lines = self.project.preprocessor.dict_beam_xaxis_rotating_angle_to_lines[self.key]
        for line in lines:
            new = QTreeWidgetItem([str(line), self.key])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)

    def force_to_close(self):
        self.close()