from PyQt5.QtWidgets import QDialog, QComboBox, QCheckBox, QFrame, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from PyQt5.uic.uiparser import QtWidgets

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class StructuralElementTypeInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/model/setup/structural/structuralElementTypeInput.ui'), self)

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

        self.dict_tag_to_entity = project.preprocessor.dict_tag_to_entity
        self.index = 0
        self.element_type = 'pipe_1'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.list_lines_to_update_cross_section = []
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_group = self.findChild(QLineEdit, 'lineEdit_selected_group')
        self.lineEdit_selected_group.setDisabled(True)

        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()

        self.radioButton_thick_wall_formulation = self.findChild(QRadioButton, 'radioButton_thick_wall_formulation')
        self.radioButton_thin_wall_formulation = self.findChild(QRadioButton, 'radioButton_thin_wall_formulation')
        self.radioButton_force_offset_off = self.findChild(QRadioButton, 'radioButton_force_offset_off')
        self.radioButton_force_offset_on = self.findChild(QRadioButton, 'radioButton_force_offset_on')
      
        self.thick_wall_formulation = self.radioButton_thick_wall_formulation.isChecked()
        self.thin_wall_formulation = self.radioButton_thin_wall_formulation.isChecked()
        self.radioButton_thick_wall_formulation.clicked.connect(self.radioButton_formulation_Event)
        self.radioButton_thin_wall_formulation.clicked.connect(self.radioButton_formulation_Event)
        self.check_wall_formulation()
    
        self.force_offset_off = self.radioButton_force_offset_off.isChecked()
        self.force_offset_on = self.radioButton_force_offset_on.isChecked()
        self.radioButton_force_offset_off.clicked.connect(self.radioButton_force_offset_Event)
        self.radioButton_force_offset_on.clicked.connect(self.radioButton_force_offset_Event)
        self.check_force_offset()

        self.checkBox_capped_end = self.findChild(QCheckBox, 'checkBox_capped_end')
        self.checkBox_capped_end.clicked.connect(self.checkBox_Event)
        self.capped_end_effect = self.checkBox_capped_end.isChecked()

        self.treeWidget_element_type = self.findChild(QTreeWidget, 'treeWidget_element_type')
        self.treeWidget_element_type.setColumnWidth(0, 120)
        # self.treeWidget_element_type.setColumnWidth(1, 100)
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_element_type.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setText(0, "ELEMENT TYPE")
        self.treeWidget_element_type.headerItem().setText(1, "LINES")
        
        self.tabWidget_main = self.findChild(QTabWidget, 'tabWidget_main')
        self.tabWidget_main.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_main.currentIndex()

        self.tab_setup = self.tabWidget_main.findChild(QWidget, 'tab_setup')
        self.tab_details = self.tabWidget_main.findChild(QWidget, 'tab_details')

        self.tabWidget_selection_options = self.findChild(QTabWidget, 'tabWidget_selection_options')
        # self.tabWidget_selection_options.currentChanged.connect(self.tabEvent_selection_options)
        self.currentTab_selection_options = self.tabWidget_selection_options.currentIndex()

        self.tab_type_selection = self.tabWidget_selection_options.findChild(QWidget, 'tab_type_selection')
        self.tab_element_options = self.tabWidget_selection_options.findChild(QWidget, 'tab_element_options')
        
        # self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        # self.pushButton_remove.clicked.connect(self.group_remove)
        # self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        # self.pushButton_reset.clicked.connect(self.reset_all)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information)
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_button_clicked)
        self.pushButton_get_information.setDisabled(True)
        self.frame_wall_formulation = self.findChild(QFrame, 'frame_wall_formulation')
        # self.pushButton_remove.setDisabled(True)

        self.update()
        self.load_element_type_info()
        self.exec()

    def checkBox_Event(self):
        self.capped_end_effect = self.checkBox_capped_end.isChecked()

    def radioButton_formulation_Event(self):
        self.thick_wall_formulation = self.radioButton_thick_wall_formulation.isChecked()
        self.thin_wall_formulation = self.radioButton_thin_wall_formulation.isChecked()
        self.check_wall_formulation()
   
    def radioButton_force_offset_Event(self):
        self.force_offset_on = self.radioButton_force_offset_on.isChecked()
        self.check_force_offset()

    # def reset_all(self):
    #     temp_dict = self.project.preprocessor.dict_structural_element_type_to_lines
    #     element_type = ""
    #     for line in self.project.preprocessor.all_lines:
    #         self.project.set_structural_element_type_by_lines(line, element_type)

    # def group_remove(self):
    #     key = self.lineEdit_selected_group.text()
    #     if key != "":
    #         try:
    #             lines = self.project.preprocessor.dict_structural_element_type_to_lines[key]
    #             for line in lines:
    #                 element_type = ""
    #                 self.project.set_structural_element_type_by_lines(line, element_type, remove=True)
    #         except Exception as error:
    #             title = "ERROR WHILE DELETING GROUP OF LINES"
    #             message = str(error)
    #             PrintMessageInput([title, message, window_title1])
    #         self.load_element_type_info()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):
        self.lines_id  = self.opv.getListPickedLines()

        if self.lines_id != []:
            self.write_ids(self.lines_id)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(False)

            if len(self.lines_id) == 1:
                entity = self.preprocessor.dict_tag_to_entity[self.lines_id[0]]

                _element_type = entity.structural_element_type
                if _element_type == 'pipe_1':
                    self.comboBox.setCurrentIndex(0)
                elif _element_type == 'beam_1':
                    self.comboBox.setCurrentIndex(1)
                
                _wall_formulation = entity.structural_element_wall_formulation
                if _wall_formulation == 'thick_wall':
                    self.radioButton_thick_wall_formulation.setChecked(True)
                elif _wall_formulation == 'thin_wall': 
                    if not self.radioButton_thin_wall_formulation.isChecked():
                        self.radioButton_thin_wall_formulation.setChecked(True)

                _force_offset = entity.force_offset
                if _force_offset == 0:
                    self.radioButton_force_offset_off.setChecked(True)
                elif _force_offset == 1:
                    if not self.radioButton_force_offset_on.isChecked():
                        self.radioButton_force_offset_on.setChecked(True)

        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(True)

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.lines_id  = self.opv.getListPickedLines()
        if self.flagEntity:
            self.lineEdit_selected_ID.setDisabled(False)
            if self.lines_id != []:
                self.write_ids(self.lines_id)
            else:
                self.lineEdit_selected_ID.setText("")
        elif self.flagAll:
            self.lineEdit_selected_ID.setDisabled(True)
            self.lineEdit_selected_ID.setText("All lines")

    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_main.currentIndex()
        self.pushButton_get_information.setDisabled(True)
        # self.pushButton_remove.setDisabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def on_click_item_line(self, item):
        self.lineEdit_selected_group.setText(item.text(0))
        # self.pushButton_remove.setDisabled(False)
        self.pushButton_get_information.setDisabled(False)

    def load_element_type_info(self):
        self.treeWidget_element_type.clear()
        for key, lines in self.project.preprocessor.dict_structural_element_type_to_lines.items():
            new = QTreeWidgetItem([str(key), str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_element_type.addTopLevelItem(new)  

    def check_wall_formulation(self):
        if self.thick_wall_formulation:
            self.wall_formulation = "thick_wall"
        else:
            self.wall_formulation = "thin_wall"

    def check_force_offset(self):
        if self.force_offset_on:
            self.force_offset = 1
        else:
            self.force_offset = 0

    def check_element_type_changes(self):

        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.update_cross_section = False
        
        final_etype = self.element_type
        if self.lines_id == []:
            tags = self.preprocessor.all_lines#list(self.dict_tag_to_entity.keys())
        else:
            tags = self.lines_id
            
        for tag in tags:
            initial_etype = self.dict_tag_to_entity[tag].structural_element_type
            
            if initial_etype in ['pipe_1', None] and final_etype in ['beam_1']:
                
                self.update_cross_section = True
                self.pipe_to_beam = True
                self.list_lines_to_update_cross_section.append(tag)

            elif initial_etype in ['beam_1', None] and final_etype in ['pipe_1']:
                
                self.update_cross_section = True
                self.beam_to_pipe = True
                self.list_lines_to_update_cross_section.append(tag)

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
                PrintMessageInput([title, message, window_title2])
            
    def update_modified_cross_sections(self):
        lines_to_reset = self.list_lines_to_update_cross_section
        self.project.set_cross_section_by_line(lines_to_reset, None)
        
        # final_etype = self.element_type
        # for tag in tags:
        #     initial_etype = self.dict_tag_to_entity[tag].structural_element_type
        #     if initial_etype in ['pipe_1'] and final_etype in ['beam_1']:
        #         self.project.set_cross_section_by_line(tag, None)
        #     elif initial_etype in ['beam_1'] and final_etype in ['pipe_1']:
        #         self.project.set_cross_section_by_line(tag, None)

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'beam_1'
        
        if self.index in [2]:
            self.frame_wall_formulation.setDisabled(True)
            self.checkBox_capped_end.setDisabled(True)
        else:
            self.frame_wall_formulation.setDisabled(False)
            self.checkBox_capped_end.setDisabled(False)

        # if self.index in [2]:
        #     self.tabWidget_selection_options.removeTab(1)
        # else:
        #     self.tabWidget_selection_options.addTab(self.tab_element_options, 'Element options')

    def confirm_button_clicked(self):
        if self.flagEntity:
            lineEdit_lineID = self.lineEdit_selected_ID.text()
            self.stop, self.typed_lines = self.before_run.check_input_LineID(lineEdit_lineID)
            if self.stop:
                return
            self.check_element_type_changes()
            lines = self.typed_lines
            if len(self.typed_lines) <= 20:
                print(f"[Set Structural Element Type] - {self.element_type} assigned to {self.typed_lines} lines")
            else:
                print(f"[Set Structural Element Type] - {self.element_type} assigned in {len(self.typed_lines)} lines")
        elif self.flagAll:
            self.check_element_type_changes()
            lines = self.preprocessor.all_lines
            print(f"[Set Structural Element Type] - {self.element_type} assigned to all lines")

        self.project.set_structural_element_type_by_lines(lines, self.element_type)
    
        if self.element_type == 'pipe_1':
            self.project.set_capped_end_by_lines(lines, self.capped_end_effect)
            self.project.set_structural_element_wall_formulation_by_lines(lines, self.wall_formulation)
        else:
            self.project.set_structural_element_wall_formulation_by_lines(lines, None)
            self.project.set_capped_end_by_lines(lines, False)
        self.project.set_structural_element_force_offset_by_lines(lines, self.force_offset)

        self.complete = True
        self.close()

    def get_information(self):
        try:
            if self.lineEdit_selected_group.text() != "":           
                key = self.lineEdit_selected_group.text()
                read = GetInformationOfGroup(self.project, key)
                if read.lines_removed:
                    self.load_lines_info()
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

        uic.loadUi(Path('pulse/interface/ui_files/model/info/getGroupInformationInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.key = key

        self.lines_removed = False

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, "LINE")
        self.treeWidget_group_info.headerItem().setText(1, "ELEMENT TYPE")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        
        self.treeWidget_group_info.setColumnWidth(0, 100)
        self.treeWidget_group_info.setColumnWidth(1, 140)
        # self.treeWidget_group_info.itemClicked.connect(self.on_click_item_)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.load_group_info()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        # elif event.key() == Qt.Key_Delete:
        #     self.check_remove()

    # def on_click_item_(self, item):
    #     text = item.text(0)
    #     self.lineEdit_selected_ID.setText(text)
    #     self.lineEdit_selected_ID.setDisabled(True)
    #     self.pushButton_remove.setDisabled(False)

    # def check_remove(self):
    #     if self.flagLines:
    #         if self.lineEdit_selected_ID.text() != "":
    #             line = int(self.lineEdit_selected_ID.text())
    #             if line in self.list_of_values:
    #                 self.list_of_values.remove(line)
    #             self.project.set_capped_end_by_lines(line, False)
    #             self.load_group_info()
    #             self.lines_removed = True
    #     self.lineEdit_selected_ID.setText("")

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        lines = self.project.preprocessor.dict_structural_element_type_to_lines[self.key]
        for line in lines:
            new = QTreeWidgetItem([str(line), self.key])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)

    def force_to_close(self):
        self.close()