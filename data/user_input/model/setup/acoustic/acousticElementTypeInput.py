from PyQt5.QtWidgets import  QDialog, QComboBox, QPushButton, QRadioButton, QLineEdit, QTreeWidget, QTreeWidgetItem, QTabWidget, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR"
window_title2 = "WARNING"

class AcousticElementTypeInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/acousticElementTypeInput.ui', self)

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
        self.comboBox_index = 0
        self.element_type = 'undamped'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_group = self.findChild(QLineEdit, 'lineEdit_selected_group')
        self.lineEdit_selected_group.setDisabled(True)

        self.lineEdit_proportional_damping = self.findChild(QLineEdit, 'lineEdit_proportional_damping')

        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.comboBox_index = self.comboBox.currentIndex()

        # index: 0 - Undamped
        # index: 1 - Proportional
        # index: 2 - Wide-duct
        # index: 3 - LRF fluid equivalent
        # index: 4 - LRF full
        
        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selection')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()

        self.treeWidget_element_type = self.findChild(QTreeWidget, 'treeWidget_element_type')
        self.treeWidget_element_type.setColumnWidth(0, 150)
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item_line)
                
        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_element_type = self.findChild(QTabWidget, 'tabWidget_element_type')
        # self.tabWidget_element_type.currentChanged.connect(self.tabWidget_etype)
        self.tabWidget_element_type.setTabEnabled(1, False)

        self.tab_element_type = self.tabWidget_element_type.findChild(QWidget, "tab_element_type")
        self.tab_damping = self.tabWidget_element_type.findChild(QWidget, "tab_damping")

        # self.tabWidget_general.currentChanged.connect(self.tabEvent_)
        # self.currentTab_ = self.tabWidget_general.currentIndex()

        # self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        # self.pushButton_remove.clicked.connect(self.group_remove)
        # self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        # self.pushButton_reset.clicked.connect(self.reset_all)

        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_get_information.clicked.connect(self.get_information)
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_element_type_attribution)
        # self.pushButton_get_information.setDisabled(True)
        # self.pushButton_remove.setDisabled(True)

        self.update()

        self.load_element_type_info()
        self.exec_()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):
        self.lines_id  = self.opv.getListPickedEntities()

        if self.lines_id != []:
            self.write_ids(self.lines_id)
            self.lineEdit_selected_ID.setDisabled(False)
            self.radioButton_selected_lines.setChecked(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setDisabled(True)
            self.radioButton_all.setChecked(True)

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()
        self.lines_id  = self.opv.getListPickedEntities()
        if self.flagSelection:
            self.lineEdit_selected_ID.setDisabled(False)
            if self.lines_id != []:
                self.write_ids(self.lines_id)
            else:
                self.lineEdit_selected_ID.setText("")
        elif self.flagAll:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setDisabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_element_type_attribution()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def selectionChange(self, index):
        self.comboBox_index = self.comboBox.currentIndex()
        self.tabWidget_element_type.setTabEnabled(1, False)
        if self.comboBox_index == 0:
            self.element_type = 'undamped'
        elif self.comboBox_index == 1:
            self.element_type = 'proportional'
            self.tabWidget_element_type.setTabEnabled(1, True)
            self.tabWidget_element_type.setCurrentWidget(self.tab_damping)
        elif self.comboBox_index == 2:
            self.element_type = 'wide-duct'
        elif self.comboBox_index == 3:
            self.element_type = 'LRF fluid equivalent'
        elif self.comboBox_index == 4:
            self.element_type = 'LRF full'

    def check_input_parameters(self, input_string, label, _float=True):
        title = "INPUT ERROR"
        value_string = input_string
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([title, message, window_title1])
                    return True
                else:
                    self.value = value

            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, window_title1])
                return True
        else:
            title = "Empty entry to the proportional damping"
            message = "Please, input a valid proportional damping value to continue."
            PrintMessageInput([title, message, window_title1])
            self.tabWidget_element_type.setCurrentWidget(self.tab_damping)
            self.value = None
            return True
        return False

    def confirm_element_type_attribution(self):

        if self.comboBox_index == 1:
            if self.check_input_parameters(self.lineEdit_proportional_damping.text(), "proportional damping"):
                return
            proportional_damping = self.value
        else:
            proportional_damping = None

        if self.flagSelection:

            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True

            for line in self.lines_typed:
                self.project.set_acoustic_element_type_by_line(line, self.element_type, proportional_damping=proportional_damping)
            print("[Set Acoustic Element Type] - defined in the entities {}".format(self.lines_typed))
        elif self.flagAll:
            for line in self.project.preprocessor.all_lines:
                self.project.set_acoustic_element_type_by_line(line, self.element_type, proportional_damping=proportional_damping)
            # self.project.set_acoustic_element_type_to_all(self.element_type, proportional_damping=proportional_damping)
            print("[Set Acoustic Element Type] - defined in all the entities")
        self.complete = True
        self.close()
    
    def on_click_item_line(self, item):
        self.lineEdit_selected_group.setText(item.text(0))

    def load_element_type_info(self):
        self.treeWidget_element_type.clear()
        for key, lines in self.project.preprocessor.dict_acoustic_element_type_to_lines.items():
            new = QTreeWidgetItem([str(key), str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_element_type.addTopLevelItem(new)  

    def get_information(self):
        try:
            if self.lineEdit_selected_group.text() != "":           
                key = self.lineEdit_selected_group.text()
                GetInformationOfGroup(self.project, key)
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
        self.dict_tag_to_entity = project.preprocessor.dict_tag_to_entity
        self.key = key

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        header = self.treeWidget_group_info.headerItem()
        header.setText(0, "Line")
        header.setText(1, "Element type")
        header.setTextAlignment(0, Qt.AlignCenter)
        header.setTextAlignment(1, Qt.AlignCenter)
        
        if self.key == 'proportional':
            header.setText(2, "Proportional damping")
            header.setTextAlignment(2, Qt.AlignCenter)
            self.treeWidget_group_info.setColumnWidth(0, 90)
            self.treeWidget_group_info.setColumnWidth(1, 130)
            self.treeWidget_group_info.setColumnWidth(2, 150)
        else:
            self.treeWidget_group_info.setColumnWidth(0, 100)
            self.treeWidget_group_info.setColumnWidth(1, 140)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        self.load_group_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        lines = self.project.preprocessor.dict_acoustic_element_type_to_lines[self.key]
        for line in lines:
            if self.key == 'proportional':
                damping = self.dict_tag_to_entity[line].proportional_damping
                new = QTreeWidgetItem([str(line), self.key, str(damping)])
                new.setTextAlignment(2, Qt.AlignCenter)
            else:
                new = QTreeWidgetItem([str(line), self.key])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)

    def force_to_close(self):
        self.close()