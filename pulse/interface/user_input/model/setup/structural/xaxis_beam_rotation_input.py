from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

window_title_1 = "Error"
window_title_2 = "Warning"

class BeamXaxisRotationInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/setup/structural/xaxis_beam_rotation_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._config_widgets()
        self._create_connections()
        self.selection_callback()
        self.load_beam_xaxis_rotation_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.before_run = self.project.get_pre_solution_model_checks()

        self.index = 0
        self.element_type = 'pipe_1'
        self.complete = False
        self.update_cross_section = False
        self.pipe_to_beam = False
        self.beam_to_pipe = False
        self.list_lines_to_update_cross_section = list()
        self.beam_lines = list()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_selection : QComboBox

        # QLabel
        self.label_attribute_to : QLabel
        self.label_selected_id : QLabel

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_xaxis_rotation_increment_angle : QLineEdit
        self.lineEdit_xaxis_rotation_actual_angle : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset_all : QPushButton

        # QTreeWidget
        self.treeWidget_xaxis_rotation_angle : QTreeWidget

        # QTabWidget
        self.tabWidget_xaxis_rotation_angle : QTabWidget

    def _config_widgets(self):
        self.pushButton_remove.setDisabled(True)
        #
        self.treeWidget_xaxis_rotation_angle.setColumnWidth(0, 120)
        # self.treeWidget_xaxis_rotation_angle.setColumnWidth(1, 100)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_xaxis_rotation_angle.headerItem().setTextAlignment(1, Qt.AlignCenter)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _create_connections(self):
        self.comboBox_selection.currentIndexChanged.connect(self.change_selection_callback)
        #
        self.pushButton_confirm.clicked.connect(self.confirm_input)
        self.pushButton_remove.clicked.connect(self.remove_selected_beam_xaxis_rotation)
        self.pushButton_reset_all.clicked.connect(self.reset_all)
        #
        self.tabWidget_xaxis_rotation_angle.currentChanged.connect(self.tab_event_update)
        self.treeWidget_xaxis_rotation_angle.itemClicked.connect(self.on_click_item)
        self.treeWidget_xaxis_rotation_angle.itemDoubleClicked.connect(self.on_double_click_item)    
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selected_id.setText(text)
            self.process_selection(selected_nodes)

    def process_selection(self, selected_lines : list):

        self.tabWidget_xaxis_rotation_angle.setDisabled(False)

        if selected_lines:

            self.comboBox_selection.setCurrentIndex(1)
            for line_id in selected_lines:
                line = self.model.mesh.lines_from_model[line_id]

                if line.structural_element_type != "beam_1":
                    self.lineEdit_selected_id.setText("")
                    self.tabWidget_xaxis_rotation_angle.setDisabled(True)
                    return

            if len(selected_lines) == 1:
                line = self.model.mesh.lines_from_model[selected_lines[0]]
                angle = line.xaxis_beam_rotation
                self.lineEdit_xaxis_rotation_actual_angle.setText(str(angle))
            else:
                self.lineEdit_xaxis_rotation_actual_angle.setText("")

    def change_selection_callback(self):
        self.lineEdit_selected_id.setText("")
        self.lineEdit_selected_id.setEnabled(True)
        selection_index = self.comboBox_selection.currentIndex()

        if selection_index == 0:
            self.lineEdit_selected_id.setText("All lines")
            self.lineEdit_selected_id.setEnabled(False)

        else:
            if app().main_window.list_selected_lines():
                self.selection_callback()

    def tab_event_update(self):

        self.pushButton_remove.setDisabled(True)
        tab_index = self.tabWidget_xaxis_rotation_angle.currentIndex()

        if tab_index == 0:
            self.label_attribute_to.setDisabled(False)
            self.label_selected_id.setText("Selected lines:")
            self.lineEdit_selected_id.setDisabled(False)
            self.comboBox_selection.setDisabled(False)

        elif tab_index == 1:
            self.label_attribute_to.setDisabled(True)
            self.label_selected_id.setText("Selected group:")
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)
            self.comboBox_selection.setDisabled(True)

    def on_click_item(self, item):
        self.selected_key = item.text(0)
        self.lineEdit_selected_id.setText(item.text(1))
        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item):
        self.selected_key = item.text(0)
        self.lineEdit_selected_id.setText(item.text(1))
        self.lineEdit_selected_id.setDisabled(True)
        self.get_information(item)

    def check_typed_lines(self, lines):
        try:

            self.beam_lines = list()
            non_beam_lines = list()
            for line in lines:
                entity = self.model.mesh.lines_from_model[line]
                if entity.structural_element_type != "beam_1":
                    non_beam_lines.append(line)
                else:
                    self.beam_lines.append(line)

            if len(non_beam_lines):
                title = "Non-beam line selected"
                message = "The following non-beam lines have been removed from the current selection:\n\n"
                message += f"{non_beam_lines}"
                PrintMessageInput([window_title_2, title, message])                

        except:
            return True

        return False

    def confirm_input(self):

        selection_index = self.comboBox_selection.currentIndex()
        if selection_index == 0:
            lines = list(self.model.mesh.lines_from_model.keys())

        else:
            str_lines = self.lineEdit_selected_id.text()
            self.stop, lines = self.before_run.check_selected_ids(str_lines, "lines")
            if self.stop:
                return

        if self.check_typed_lines(lines):
            return

        if self.check_xaxis_rotation_angle():
            return
    
        for line in self.beam_lines:
            self.project.set_beam_xaxis_rotation_by_line(line, self.rotation_angle)

        self.update_plots()
        self.close()

    def update_plots(self):
        self.load_beam_xaxis_rotation_info()
        self.preprocessor.process_all_rotation_matrices() 
        app().main_window.update_plots() 

    def check_xaxis_rotation_angle(self):
        self.rotation_angle = 0
        try:
            self.rotation_angle = float(self.lineEdit_xaxis_rotation_increment_angle.text())
        except Exception as error_log:
            title = f"Invalid X-axis Rotation Angle"
            message = f"Please, inform a valid number at the 'Rotation angle' input field to continue.\n\n"
            message += f"{str(error_log)}"
            PrintMessageInput([window_title_1, title, message])
            return True
        return False

    def load_beam_xaxis_rotation_info(self):
        self.treeWidget_xaxis_rotation_angle.clear()
        _dict = self.preprocessor.dict_beam_xaxis_rotating_angle_to_lines
        for key, lines in _dict.items():
            new = QTreeWidgetItem([str(key), str(lines)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_xaxis_rotation_angle.addTopLevelItem(new)  
        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.dict_beam_xaxis_rotating_angle_to_lines) == 0:
            self.tabWidget_xaxis_rotation_angle.setCurrentIndex(0)
            self.tabWidget_xaxis_rotation_angle.setTabVisible(1, False)
        else:
            self.tabWidget_xaxis_rotation_angle.setTabVisible(1, True)

    def remove_selected_beam_xaxis_rotation(self):
        try:

            if self.selected_key == "":
                return

            lines = self.preprocessor.dict_beam_xaxis_rotating_angle_to_lines[self.selected_key]
            self.preprocessor.dict_beam_xaxis_rotating_angle_to_lines.pop(self.selected_key)
            for line in lines:
                delta_angle = - self.preprocessor.dict_lines_to_rotation_angles[line]
                self.project.set_beam_xaxis_rotation_by_line(line, delta_angle)

            self.update_plots()
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_selected_id.setText("")

            title = "X-axis rotation angle removal"
            message = f"The x-axis rotation angle attributed to the lines {lines} has been removed from the current model setup."
            PrintMessageInput([window_title_2, title, message], auto_close=True)
        
        except:
            pass

    def reset_all(self):

        self.hide()

        title = "Resetting x-axis beam rotations"
        message = "Would you like to remove all x-axis rotations attributed to beam elements?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            aux_dict = self.preprocessor.dict_beam_xaxis_rotating_angle_to_lines.copy()
            if len(aux_dict) > 0:
                for key, lines in aux_dict.items():

                    _lines = lines.copy()
                    delta_angle = -float(key)

                    for line in _lines:
                        self.project.set_beam_xaxis_rotation_by_line(line, delta_angle)

                self.preprocessor.create_dict_lines_to_rotation_angles()
                self.update_plots()

    def get_list_typed_entries(self, str_list):
        try:
            tokens = str_list[1:-1].strip().split(',')
            tokens.remove('')
        except:
            pass
        return list(map(int, tokens))

    def get_information(self, item):
        try:
            if self.lineEdit_selected_id.text() != "":

                data = dict()
                for line in self.get_list_typed_entries(item.text(1)):
                    data[line] = ["Enabled"]

                if len(data):
                    self.close()
                    header_labels = ["Lines", "Capped end effect"]
                    GetInformationOfGroup(  group_label = "Capped end effect",
                                            selection_label = "Line ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 140],
                                            data = data  )        

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
        except Exception as e:
            title = "Error while getting information of selected group"
            message = str(e)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_input()
        elif event.key() == Qt.Key_Escape:
            self.close()