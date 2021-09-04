from PyQt5.QtWidgets import  QDialog, QComboBox, QPushButton, QRadioButton, QLineEdit, QTreeWidget, QTreeWidgetItem, QTabWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class StructuralElementTypeInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/structuralElementTypeInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_id = self.opv.getListPickedEntities()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()

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

        self.treeWidget_element_type = self.findChild(QTreeWidget, 'treeWidget_element_type')
        self.treeWidget_element_type.setColumnWidth(0, 120)
        # self.treeWidget_element_type.setColumnWidth(1, 100)
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item_line)
        self.treeWidget_element_type.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_element_type.headerItem().setText(0, "ELEMENT TYPE")
        self.treeWidget_element_type.headerItem().setText(1, "LINES")
        
        self.tabWidget_element_type = self.findChild(QTabWidget, 'tabWidget_element_type')
        self.tabWidget_element_type.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_element_type.currentIndex()

        # self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        # self.pushButton_remove.clicked.connect(self.group_remove)
        # self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        # self.pushButton_reset.clicked.connect(self.reset_all)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information)
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.button_clicked)
        self.pushButton_get_information.setDisabled(True)
        # self.pushButton_remove.setDisabled(True)

        self.update()
        self.load_element_type_info()
        self.exec_()
    
    # def reset_all(self):
    #     temp_dict = self.project.preprocessor.dict_structural_element_type_to_lines
    #     element_type = ""
    #     for line in self.project.preprocessor.all_lines:
    #         self.project.set_structural_element_type_by_entity(line, element_type)

    # def group_remove(self):
    #     key = self.lineEdit_selected_group.text()
    #     if key != "":
    #         try:
    #             lines = self.project.preprocessor.dict_structural_element_type_to_lines[key]
    #             for line in lines:
    #                 element_type = ""
    #                 self.project.set_structural_element_type_by_entity(line, element_type, remove=True)
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
        self.lines_id  = self.opv.getListPickedEntities()

        if self.lines_id != []:
            self.write_ids(self.lines_id)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(False)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setDisabled(True)

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_selected_lines.isChecked()
        self.lines_id  = self.opv.getListPickedEntities()
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
        self.currentTab_ = self.tabWidget_element_type.currentIndex()
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

    def check_element_type_changes(self):

        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.update_cross_section = False
        
        final_etype = self.element_type
        if self.lines_id == []:
            tags = list(self.dict_tag_to_entity.keys())
        else:
            tags = self.lines_id
            
        for tag in tags:
            initial_etype = self.dict_tag_to_entity[tag].structural_element_type
            
            if initial_etype in ['pipe_1', 'pipe_2', None] and final_etype in ['beam_1']:
                self.update_cross_section = True
                self.pipe_to_beam = True
                self.list_lines_to_update_cross_section.append(tag)

            elif initial_etype in ['beam_1', None] and final_etype in ['pipe_1', 'pipe_2']:
                self.update_cross_section = True
                self.beam_to_pipe = True
                self.list_lines_to_update_cross_section.append(tag)

        if self.update_cross_section:
            self.update_modified_cross_sections(tags)
            if initial_etype is not None:
                title = "Change in element type detected"
                message = f"The element type previously defined to the {self.list_lines_to_update_cross_section} line(s) \n"
                message += "has been modified, therefore, it is necessary to update \n"
                message += "the cross-section(s) of this(ese) line(s) to continue."
                PrintMessageInput([title, message, window_title2])
            
    def update_modified_cross_sections(self, tags):

        final_etype = self.element_type

        for tag in tags:
            initial_etype = self.dict_tag_to_entity[tag].structural_element_type
            if initial_etype in ['pipe_1', 'pipe_2'] and final_etype in ['beam_1']:
                self.project.set_cross_section_by_line(tag, None)
            elif initial_etype in ['beam_1'] and final_etype in ['pipe_1', 'pipe_2']:
                self.project.set_cross_section_by_line(tag, None)

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'
        elif self.index ==2:
            self.element_type = 'beam_1'

    def button_clicked(self):
        if self.flagEntity:
            lineEdit_lineID = self.lineEdit_selected_ID.text()
            self.stop, self.typed_lines = self.before_run.check_input_LineID(lineEdit_lineID)
            if self.stop:
                return
            self.check_element_type_changes()
            for line in self.typed_lines:
                self.project.set_structural_element_type_by_entity(line, self.element_type)
            print("[Set Element Type] - defined in the entities {}".format(self.typed_lines))
        elif self.flagAll:
            self.check_element_type_changes()
            for line in self.project.preprocessor.all_lines:
                self.project.set_structural_element_type_by_entity(line, self.element_type)
            print("[Set Element Type] - defined in all the entities")
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

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        uic.loadUi('data/user_input/ui/Model/Info/getGroupInformationInput.ui', self)

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
        self.exec_()

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
    #             self.project.set_capped_end_by_line(line, False)
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