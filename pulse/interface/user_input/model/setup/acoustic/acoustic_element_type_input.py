from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_element_type_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.update()
        self.selectionChange()

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
        self.lines_id = self.opv.getListPickedLines()

        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity
        self.comboBox_index = 0
        self.element_type = 'undamped'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_flow_effects = self.findChild(QCheckBox, 'checkBox_flow_effects')
        # QComboBox
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        # QLabel
        self.label_vol_flow = self.findChild(QLabel, 'label_vol_flow')
        self.label_ms_unit = self.findChild(QLabel, 'label_ms_unit')
        # QLineEdit
        self.lineEdit_vol_flow = self.findChild(QLineEdit, 'lineEdit_vol_flow')
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_group = self.findChild(QLineEdit, 'lineEdit_selected_group')
        self.lineEdit_proportional_damping = self.findChild(QLineEdit, 'lineEdit_proportional_damping')
        self.lineEdit_selected_group.setDisabled(True)
        # QPushButton
        # self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        # self.pushButton_remove.clicked.connect(self.group_remove)
        # self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        # self.pushButton_reset.clicked.connect(self.reset_all)
        self.pushButton_get_information = self.findChild(QPushButton, 'pushButton_get_information')
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        # self.pushButton_get_information.setDisabled(True)
        # self.pushButton_remove.setDisabled(True)
        # QRadioButton
        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selection')
        # QTabWidget
        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tabWidget_element_type = self.findChild(QTabWidget, 'tabWidget_element_type')
        # self.tabWidget_element_type.currentChanged.connect(self.tabWidget_etype)
        # self.tabWidget_element_type.setTabEnabled(1, False)
        # QTreeWidget
        self.treeWidget_element_type = self.findChild(QTreeWidget, 'treeWidget_element_type')
        self.treeWidget_element_type.setColumnWidth(0, 150)
        # self.tabWidget_general.currentChanged.connect(self.tabEvent_)
        # self.currentTab_ = self.tabWidget_general.currentIndex()

    def _create_connections(self):
        self.checkBox_flow_effects.toggled.connect(self.checkBoxEvent_flow_effects)
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.comboBox_index = self.comboBox.currentIndex()

        # index: 0 - Undamped
        # index: 1 - Proportional
        # index: 2 - Wide-duct
        # index: 3 - LRF fluid equivalent
        # index: 4 - LRF full

        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()

        self.pushButton_confirm.clicked.connect(self.confirm_element_type_attribution)
        self.pushButton_get_information.clicked.connect(self.get_information)

        self.treeWidget_element_type.itemClicked.connect(self.on_click_item_line)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):
        self.lines_id  = self.opv.getListPickedLines()

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
        self.lines_id  = self.opv.getListPickedLines()
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

    def selectionChange(self):
        self.comboBox_index = self.comboBox.currentIndex()
        self.tabWidget_element_type.setTabVisible(1, False)

        if self.checkBox_flow_effects.isChecked():
            if self.comboBox_index == 0:
                self.element_type = 'undamped mean flow'
            elif self.comboBox_index == 1:
                self.element_type = 'peters'
            elif self.comboBox_index == 2:
                self.element_type = 'howe'
        else:
            if self.comboBox_index == 0:
                self.element_type = 'undamped'
            elif self.comboBox_index == 1:
                self.element_type = 'proportional'
                self.tabWidget_element_type.setTabVisible(1, True)
                self.tabWidget_element_type.setCurrentIndex(1)
            elif self.comboBox_index == 2:
                self.element_type = 'wide-duct'
            elif self.comboBox_index == 3:
                self.element_type = 'LRF fluid equivalent'
            elif self.comboBox_index == 4:
                self.element_type = 'LRF full'

    def checkBoxEvent_flow_effects(self):
        flow_effects = self.checkBox_flow_effects.isChecked()
        self.label_vol_flow.setDisabled(not flow_effects)
        self.lineEdit_vol_flow.setDisabled(not flow_effects)
        self.label_ms_unit.setDisabled(not flow_effects)
        self.comboBox.clear()

        if flow_effects:
            list_items = ["Undamped mean flow", "Peters", "Howe"]    
        else:
            list_items = ["Undamped", "Proportional", "Wide-duct", "LRF fluid equivalent", "LRF full"]
        
        self.comboBox.addItems(list_items)

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
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value

            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            title = "Empty entry to the " + label
            message = "Please, input a valid " + label + " value to continue."
            PrintMessageInput([window_title_1, title, message])
            self.tabWidget_element_type.setCurrentIndex(1)
            self.value = None
            return True
        return False

    def confirm_element_type_attribution(self):
        flow_effects = self.checkBox_flow_effects.isChecked()
        if self.comboBox_index == 1 and not flow_effects:
            if self.check_input_parameters(self.lineEdit_proportional_damping.text(), "proportional damping"):
                return
            proportional_damping = self.value
        else:
            proportional_damping = None

        if flow_effects:
            if self.check_input_parameters(self.lineEdit_vol_flow.text(), "Volume flow rate"):
                return
            vol_flow = self.value
        else:
            vol_flow = None

        if self.flagSelection:
            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.typed_lines = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True
            lines = self.typed_lines
            if len(self.typed_lines) <= 20:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned to {self.typed_lines} lines")
            else:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned in {len(self.typed_lines)} lines")
        elif self.flagAll:
            lines = self.project.preprocessor.all_lines
            print(f"[Set Acoustic Element Type] - {self.element_type} assigned in all the entities")
        
        self.project.set_acoustic_element_type_by_lines(lines, self.element_type, proportional_damping = proportional_damping, vol_flow = vol_flow)
        self.complete = True
        self.close()
    
    def on_click_item_line(self, item):
        self.lineEdit_selected_group.setText(item.text(0))

    def load_element_type_info(self):
        self.treeWidget_element_type.clear()
        header = self.treeWidget_element_type.headerItem()
        header.setText(0, "Element type")
        header.setText(1, "Volume flow rate")
        header.setText(2, "Lines")
        header.setTextAlignment(0, Qt.AlignCenter)
        header.setTextAlignment(1, Qt.AlignCenter)
        header.setTextAlignment(2, Qt.AlignCenter)
        for key, lines in self.project.preprocessor.dict_acoustic_element_type_to_lines.items():
            vol_flow = [self.dict_tag_to_entity[line].vol_flow for line in lines]
            if None in vol_flow:
                new = QTreeWidgetItem([str(key), str('---'), str(lines)])
            else:
                new = QTreeWidgetItem([str(key), str(vol_flow), str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            new.setTextAlignment(2, Qt.AlignCenter)
            self.treeWidget_element_type.addTopLevelItem(new)  

    def get_information(self):
        try:
            if self.lineEdit_selected_group.text() != "":
                key = self.lineEdit_selected_group.text()
                GetInformationOfGroup(self.project, key)
            else:
                title = "UNSELECTED GROUP OF LINES"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(e)
            PrintMessageInput([window_title_1, title, message])


class GetInformationOfGroup(QDialog):
    def __init__(self, project, key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "model/info/getGroupInformationInput.ui", self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

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
        elif self.key in ["undamped mean flow", "peters", "howe"]:
            header.setText(2, "Volume mean flow")
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
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        self.treeWidget_group_info.clear()
        values = self.project.preprocessor.dict_acoustic_element_type_to_lines[self.key]
        for line in values:
            if self.key == 'proportional':
                damping = self.dict_tag_to_entity[line].proportional_damping
                new = QTreeWidgetItem([str(line), self.key, str(damping)])
                new.setTextAlignment(2, Qt.AlignCenter)
            elif self.key in ["undamped mean flow", "peters", "howe"]:
                vol_flow = self.dict_tag_to_entity[line].vol_flow
                new = QTreeWidgetItem([str(line), self.key, str(vol_flow)])
                new.setTextAlignment(2, Qt.AlignCenter)
            else:
                new = QTreeWidgetItem([str(line), self.key])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_group_info.addTopLevelItem(new)

    def force_to_close(self):
        self.close()