from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_element_type_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.update_selection()
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
        self.lines_id = app().main_window.list_selected_entities()

        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity
        self.element_type = 'undamped'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_flow_effects : QCheckBox
        # QComboBox
        self.comboBox_element_type : QComboBox
        self.comboBox_selection : QComboBox
        # QLabel
        self.label_proportional_damping : QLabel
        self.label_vol_flow : QLabel
        self.label_volume_rate_unit : QLabel
        self.label_selected_id : QLabel
        # QLineEdit
        self.lineEdit_vol_flow : QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_proportional_damping : QLineEdit
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset : QPushButton
        # QTabWidget
        self.tabWidget_main : QTabWidget
        # QTreeWidget
        self.treeWidget_element_type : QTreeWidget

    def _create_connections(self):
        app().main_window.selection_changed.connect(self.update_selection)
        self.checkBox_flow_effects.toggled.connect(self.checkBoxEvent_flow_effects)
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_change_callback)
        self.comboBox_selection.currentIndexChanged.connect(self.attribution_type_callback)
        self.pushButton_confirm.clicked.connect(self.confirm_element_type_attribution)
        self.pushButton_reset.clicked.connect(self.reset_element_type)
        self.tabWidget_main.currentChanged.connect(self.tab_selection_callback)
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item)
        self.treeWidget_element_type.itemDoubleClicked.connect(self.on_double_click_item)

    def _config_widgets(self):
        self.treeWidget_element_type.setColumnWidth(0, 150)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

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
            self.lines_id  = app().main_window.list_selected_entities()
            if self.lines_id != []:
                self.write_ids(self.lines_id)
            else:
                self.lineEdit_selected_id.setText("")

    def element_type_change_callback(self):

        self.lineEdit_proportional_damping.setText("")
        self.label_proportional_damping.setDisabled(True)
        self.lineEdit_proportional_damping.setDisabled(True)
        element_type_index = self.comboBox_element_type.currentIndex()

        if self.checkBox_flow_effects.isChecked():
            if element_type_index == 0:
                self.element_type = 'undamped mean flow'
            elif element_type_index == 1:
                self.element_type = 'peters'
            elif element_type_index == 2:
                self.element_type = 'howe'

        else:
            if element_type_index == 0:
                self.element_type = 'undamped'
            elif element_type_index == 1:
                self.element_type = 'proportional'
                self.label_proportional_damping.setDisabled(False)
                self.lineEdit_proportional_damping.setDisabled(False)
            elif element_type_index == 2:
                self.element_type = 'wide-duct'
            elif element_type_index == 3:
                self.element_type = 'LRF fluid equivalent'
            elif element_type_index == 4:
                self.element_type = 'LRF full'

    def checkBoxEvent_flow_effects(self):
        flow_effects = self.checkBox_flow_effects.isChecked()
        self.label_vol_flow.setDisabled(not flow_effects)
        self.lineEdit_vol_flow.setDisabled(not flow_effects)
        self.label_volume_rate_unit.setDisabled(not flow_effects)
        self.comboBox_element_type.clear()

        if flow_effects:
            list_items = ["Undamped mean flow", "Peters", "Howe"]    
        else:
            list_items = ["Undamped", "Proportional", "Wide-duct", "LRF fluid equivalent", "LRF full"]
        
        self.comboBox_element_type.addItems(list_items)

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
            self.value = None
            return True
        return False

    def confirm_element_type_attribution(self):
        flow_effects = self.checkBox_flow_effects.isChecked()
        element_type_index = self.comboBox_element_type.currentIndex()
        if element_type_index == 1 and not flow_effects:
            lineEdit = self.lineEdit_proportional_damping.text()
            if self.check_input_parameters(lineEdit, "proportional damping"):
                return
            proportional_damping = self.value
        else:
            proportional_damping = None

        if flow_effects:
            lineEdit = self.lineEdit_vol_flow.text()
            if self.check_input_parameters(lineEdit, "Volume flow rate"):
                return
            vol_flow = self.value
        else:
            vol_flow = None

        index_selection = self.comboBox_selection.currentIndex()
        if index_selection == 0:
            lines = self.preprocessor.all_lines
            print(f"[Set Acoustic Element Type] - {self.element_type} assigned in all the entities")

        elif index_selection == 1:
            lineEdit = self.lineEdit_selected_id.text()
            self.stop, self.typed_lines = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True
            lines = self.typed_lines
            if len(self.typed_lines) <= 20:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned to {self.typed_lines} lines")
            else:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned in {len(self.typed_lines)} lines")
        
        self.project.set_acoustic_element_type_by_lines(lines, 
                                                        self.element_type, 
                                                        proportional_damping = proportional_damping, 
                                                        vol_flow = vol_flow)
        self.complete = True
        self.close()

    def reset_element_type(self):
        self.element_type = "undamped"
        lines = self.preprocessor.all_lines
        self.project.set_acoustic_element_type_by_lines(lines, self.element_type)
        self.complete = True
        self.close()
        title = "Resetting process complete"
        message = "The acoustic element type has been reset to the default option 'undampded'."
        PrintMessageInput([window_title_2, title, message], auto_close=True)

    def on_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)

    def on_double_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)
        self.get_information(item)

    def load_element_type_info(self):

        self.treeWidget_element_type.clear()
        header = self.treeWidget_element_type.headerItem()

        header_labels = ["Element type", "Volume flow rate", "Lines"]
        for col, label in enumerate(header_labels):
            header.setText(col, label)
            header.setTextAlignment(col, Qt.AlignCenter)

        for key, lines in self.preprocessor.dict_acoustic_element_type_to_lines.items():

            vol_flow = [self.dict_tag_to_entity[line].vol_flow for line in lines]
            if None in vol_flow:
                item = QTreeWidgetItem([str(key), str('---'), str(lines)[1:-1]])
            else:
                item = QTreeWidgetItem([str(key), str(vol_flow), str(lines)[1:-1]])

            for col in range(len(header_labels)):
                item.setTextAlignment(col, Qt.AlignCenter)

            self.treeWidget_element_type.addTopLevelItem(item)
        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.dict_acoustic_element_type_to_lines) == 0:
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
                header_labels = ["Line ID", "Element type"]

                if key == "proportional":
                    header_labels.append("Proportional damping")

                elif key in ["undamped mean flow", "peters", "howe"]:
                    header_labels.append("Volume mean flow")

                data = dict()
                for line_id in self.preprocessor.dict_acoustic_element_type_to_lines[key]:

                    element_data = [key]
                    if key == "proportional":
                        damping = self.dict_tag_to_entity[line_id].proportional_damping
                        element_data.append(damping)
    
                    elif key in ["undamped mean flow", "peters", "howe"]:
                        vol_flow = self.dict_tag_to_entity[line_id].vol_flow
                        element_data.append(vol_flow)

                    data[line_id] = element_data

                GetInformationOfGroup(  group_label = "Element type",
                                        selection_label = "Line ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
                                        data = data  )

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])

            self.show()

        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            self.show()

    def update_selection(self):
        self.lines_id  = app().main_window.list_selected_entities()
        if self.lines_id != []:

            self.comboBox_selection.setCurrentIndex(1)
            self.write_ids(self.lines_id)
            self.lineEdit_selected_id.setDisabled(False)

            if len(self.lines_id) == 1:

                self.checkBox_flow_effects.setChecked(False)
                self.lineEdit_proportional_damping.setDisabled(True)
                entity = self.preprocessor.dict_tag_to_entity[self.lines_id[0]]
                element_type = entity.acoustic_element_type

                if element_type == "proportional":
                    proportional_damping = entity.proportional_damping
                    self.comboBox_element_type.setCurrentIndex(1)
                    self.lineEdit_proportional_damping.setText(str(proportional_damping))
                    self.lineEdit_proportional_damping.setDisabled(False)

                else:
                    if element_type == "undamped":
                        self.comboBox_element_type.setCurrentIndex(0)

                    elif element_type in ["undamped mean flow", "peters", "howe"]:
                        vol_flow = entity.vol_flow
                        self.checkBox_flow_effects.setChecked(True)
                        self.lineEdit_vol_flow.setText(str(vol_flow))
        else:
            self.comboBox_selection.setCurrentIndex(0)

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_element_type_attribution()
        elif event.key() == Qt.Key_Escape:
            self.close()