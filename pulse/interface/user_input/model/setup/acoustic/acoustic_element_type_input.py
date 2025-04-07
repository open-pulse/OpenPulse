from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QStackedWidget, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.acoustic.reciprocating_machine_selector import ReciprocatingMachineSelector
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.utils.interface_utils import check_inputs

from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_element_type_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.selection_callback()
        self.element_type_change_callback()
        self.attribution_type_callback()

        self.load_element_type_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.element_type = 'undamped'
        self.element_types = [
                              "undamped", 
                              "proportional", 
                              "wide_duct", 
                              "LRF_fluid_equivalent", 
                              "LRF_full", 
                              "damped_liquid", 
                              "undamped_mean_flow", 
                              "peters", 
                              "howe"
                              ]

        self.complete = False
        self.keep_window_open = True

        self.before_run = app().project.get_pre_solution_model_checks()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_element_type: QComboBox
        self.comboBox_selection: QComboBox

        # QLabel
        self.label_proportional_damping: QLabel
        self.label_volumetric_flow_rate: QLabel
        self.label_volume_rate_unit: QLabel
        self.label_selected_id: QLabel

        # QLineEdit
        self.lineEdit_volumetric_flow_rate: QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_proportional_damping: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_get_volumetric_flow_rate: QPushButton

        # QStackedWidget
        self.stackedWidget_main: QStackedWidget

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_element_type: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_element_type.currentIndexChanged.connect(self.element_type_change_callback)
        self.comboBox_selection.currentIndexChanged.connect(self.attribution_type_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_volumetric_flow_rate.clicked.connect(self.get_volumetric_flow_rate_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_selection_callback)
        #
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item)
        self.treeWidget_element_type.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.comboBox_selection.blockSignals(True)
        selected_lines = app().main_window.list_selected_lines()

        if selected_lines:

            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selected_id.setText(text)

            self.comboBox_selection.setCurrentIndex(1)
            self.lineEdit_selected_id.setDisabled(False)

            if len(selected_lines) == 1:

                line_id = selected_lines[0]
                element_type = self.properties._get_property("acoustic_element_type", line_id=line_id)

                if element_type == "undamped":
                    self.comboBox_element_type.setCurrentIndex(0)
                
                elif element_type == "proportional":
                    proportional_damping = self.properties._get_property("proportional_damping", line_id=line_id)
                    if isinstance(proportional_damping, float):
                        self.comboBox_element_type.setCurrentIndex(1)
                        self.lineEdit_proportional_damping.setText(str(proportional_damping))

                elif element_type == "wide_duct":
                    self.comboBox_element_type.setCurrentIndex(2)

                elif element_type == "LRF_fluid_equivalent":
                    self.comboBox_element_type.setCurrentIndex(3)

                elif element_type == "LRF_full":
                    self.comboBox_element_type.setCurrentIndex(4)

                else:

                    mf_element_types = ["damped_liquid", "undamped_mean_flow", "peters", "howe"]

                    if element_type in mf_element_types:

                        # etype_index = mf_element_types.index(element_type)
                        volumetric_flow_rate = self.properties._get_property("volumetric_flow_rate", line_id=line_id)

                        if isinstance(volumetric_flow_rate, float):
                            self.lineEdit_volumetric_flow_rate.setText(str(volumetric_flow_rate))
                            self.comboBox_element_type.setCurrentIndex(self.element_types.index(element_type))

        self.comboBox_selection.blockSignals(False)

    def _config_widgets(self):
        #
        self.comboBox_element_type.setFixedSize(160, 26)
        #
        widths = [120, 180]
        for i, w in enumerate(widths):
            self.treeWidget_element_type.setColumnWidth(i, w)

    def tab_selection_callback(self):
        if self.tabWidget_main.currentIndex() == 0:
            self.label_selected_id.setText("Selected ID:")
            self.attribution_type_callback()
        else:
            self.label_selected_id.setText("Selection:")
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setDisabled(True)

    def attribution_type_callback(self):
        if self.comboBox_selection.currentIndex() == 0:
            self.lineEdit_selected_id.setDisabled(True)
            self.lineEdit_selected_id.setText("All lines")
        else:
            self.lineEdit_selected_id.setDisabled(False)
            if app().main_window.list_selected_lines():
                self.selection_callback()
            else:
                self.lineEdit_selected_id.setText("")

    def element_type_change_callback(self):

        self.lineEdit_proportional_damping.setText("")
        index = self.comboBox_element_type.currentIndex()

        if index in [0, 2, 3, 4]:
            self.stackedWidget_main.setVisible(False)
        else:
            self.stackedWidget_main.setVisible(True)

        if index in [5, 6, 7, 8]:
            if index == 5:
                self.pushButton_get_volumetric_flow_rate.setText("Pump")
            else:
                self.pushButton_get_volumetric_flow_rate.setText("Compressor")
            self.stackedWidget_main.setCurrentIndex(1)

        elif index == 1:
            self.stackedWidget_main.setCurrentIndex(0)

        self.element_type = self.element_types[index]

    def check_input_parameters(self, parameter: str, label: str, _float=True):

        title = "Input error"

        if parameter != "":
            try:

                parameter = parameter.replace(",", ".")

                if _float:
                    value = float(parameter)
                else:
                    value = int(parameter) 

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            title = "Empty entry to the " + label
            message = "Please, input a valid " + label + " value to continue."
            PrintMessageInput([window_title_1, title, message])
            self.value = None
            return True
        return False

    def attribute_callback(self):

        etype_index = self.comboBox_element_type.currentIndex()

        proportional_damping = None
        if etype_index == 1:
            proportional_damping = check_inputs(self.lineEdit_proportional_damping, 'proportional damping', zero_included=False, parent=self)
            if proportional_damping is None:
                return True

        volumetric_flow_rate = None
        if etype_index in [5, 6, 7, 8]:
            volumetric_flow_rate = check_inputs(self.lineEdit_volumetric_flow_rate, 'volumetric flow rate', zero_included=False, parent=self)
            if volumetric_flow_rate is None:
                return True

        index_selection = self.comboBox_selection.currentIndex()
        if index_selection == 0:
            line_ids = app().project.model.mesh.lines_from_model
            print(f"[Set Acoustic Element Type] - {self.element_type} assigned in all the entities")

        elif index_selection == 1:

            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return True

            if len(line_ids) <= 20:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned to {line_ids} lines")
            else:
                print(f"[Set Acoustic Element Type] - {self.element_type} assigned in {len(line_ids)} lines")
        
        app().project.model.preprocessor.set_acoustic_element_type_by_lines(
                                                                            line_ids, 
                                                                            self.element_type, 
                                                                            proportional_damping = proportional_damping, 
                                                                            volumetric_flow_rate = volumetric_flow_rate
                                                                            )

        app().project.model.properties._set_line_property("acoustic_element_type", self.element_type, line_ids)

        if proportional_damping is None:
            for line_id in line_ids:
                app().project.model.properties._remove_line_property("proportional_damping", line_id)

        else:
            app().project.model.properties._set_line_property("proportional_damping", proportional_damping, line_ids)

        if volumetric_flow_rate is None:
            for line_id in line_ids:
                app().project.model.properties._remove_line_property("volumetric_flow_rate", line_id)

        else:
            app().project.model.properties._set_line_property("volumetric_flow_rate", volumetric_flow_rate, line_ids)

        self.actions_to_finalize()

    def remove_callback(self):
        pass

    def reset_callback(self):

        self.hide()

        title = f"Resetting of acoustic element types"
        message = "Would you like to reset the acoustic element types from the model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            for (line_id, data) in self.properties.line_properties.items():
                if "acoustic_element_type" in data.keys():

                    app().project.model.preprocessor.set_acoustic_element_type_by_lines(line_id, "undamped")
                    app().project.model.properties._remove_line_property("acoustic_element_type", line_id)
                    app().project.model.properties._remove_line_property("proportional_damping", line_id)
                    app().project.model.properties._remove_line_property("volumetric_flow_rate", line_id)

            self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_line_properties_in_file()
        self.pushButton_exit.setText("Exit")
        self.complete = True
        self.close()

    def get_volumetric_flow_rate_callback(self):
        self.hide()
        if self.comboBox_element_type.currentIndex() == 5:
            machine_type = "pump"
        else:
            machine_type = "compressor"

        rms = ReciprocatingMachineSelector(machine_type)
        app().main_window.set_input_widget(self)

        if rms.volumetric_flow_rate is None:
            return

        self.lineEdit_volumetric_flow_rate.setText(f"{rms.volumetric_flow_rate : .6e}")

    def on_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)

        lineEdit = self.lineEdit_selected_id.text()
        stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
        if stop:
            return True

        app().main_window.set_selection(lines=line_ids)

    def on_double_click_item(self, item):
        self.comboBox_selection.setCurrentIndex(1)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)
        self.get_information(item)

    def load_element_type_info(self):

        self.treeWidget_element_type.clear()
        # header = self.treeWidget_element_type.headerItem()

        # header_labels = ["Element type", "Volumetric flow rate [m³/s]", "Lines"]
        # for col, label in enumerate(header_labels):
        #     header.setText(col, label)
        #     header.setTextAlignment(col, Qt.AlignCenter)

        aux = defaultdict(list)
        for line_id in self.properties.line_properties.keys():

            element_type = self.properties._get_property("acoustic_element_type", line_id=line_id)
            if element_type is None:
                continue

            volumetric_flow_rate = self.properties._get_property("volumetric_flow_rate", line_id=line_id)
            if volumetric_flow_rate is None:
                volumetric_flow_rate = "---"

            aux[(element_type, volumetric_flow_rate)].append(line_id)
        
        for key, line_ids in aux.items():

            element_type, volumetric_flow_rate = key
            item = QTreeWidgetItem([element_type, str(volumetric_flow_rate), str(line_ids)[1:-1]])

            for col in range(3):
                item.setTextAlignment(col, Qt.AlignCenter)

            self.treeWidget_element_type.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "acoustic_element_type" in data.keys():
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

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

                elif key in ["undamped_mean_flow", "peters", "howe"]:
                    header_labels.append("Volume mean flow")

                data = dict()
                for line_id in self.properties.line_properties.keys():

                    element_type = self.properties._get_property("acoustic_element_type", line_id=line_id)
                    if element_type is None:
                        continue

                    if key == element_type:
                        element_data = [key]

                        if key == "proportional":
                            damping = self.properties._get_property("proportional_damping", line_id=line_id)
                            if damping is None:
                                continue
                            element_data.append(damping)
    
                        elif key in ["undamped_mean_flow", "peters", "howe"]:
                            volumetric_flow_rate = self.properties._get_property("volumetric_flow_rate", line_id=line_id)
                            if volumetric_flow_rate is None:
                                continue
                            element_data.append(volumetric_flow_rate)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)