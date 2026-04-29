from collections import defaultdict
from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTreeWidgetItem

from pulse import app
from pulse.interface import error_title, warning_title
from pulse.interface.ui_generated.model.setup.acoustic.acoustic_element_type_input_ui import (
    AcousticElementTypeInput_UI,
)
from pulse.interface.user_input.model.setup.acoustic.reciprocating_machine_selector import (
    ReciprocatingMachineSelector,
)
from pulse.interface.user_input.model.setup.general.get_information_of_group import (
    GetInformationOfGroup,
)
from pulse.interface.user_input.model.setup.lines_input import LinesInput
from pulse.interface.user_input.numeric_checks.double_validator import (
    StrictDoubleValidator,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class ElemenType(IntEnum):
    UNDAMPED = 0
    PROPORTIONAL = 1
    WIDE_DUCT = 2
    LRF_FLUID_EQ = 3
    LRF_FULL = 4
    DAMPED_LIQUID = 5
    UNDAMPED_MEAN_FLOW = 6
    PETERS = 7
    HOWE = 8


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


class AssignmentType(IntEnum):
    ALL_LINES = 0
    SELECTED_LINES = 1


class AcousticElementTypeInput(LinesInput, AcousticElementTypeInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = app().project
        self.model = app().project.model

        self._initialize()
        self._config_widgets()
        self._configure_validators()
        self._create_connections()

        # self.attribution_type_callback()

        self.load_element_type_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.keep_window_open = True
        self.element_type = "undamped"

        self.element_types = [
            "undamped",
            "proportional",
            "wide_duct",
            "LRF_fluid_equivalent",
            "LRF_full",
            "damped_liquid",
            "undamped_mean_flow",
            "peters",
            "howe",
        ]

    def _config_widgets(self):
        self.comboBox_element_type.setFixedSize(160, 26)
        self.treeWidget_element_type.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _configure_validators(self):
        self.lineEdit_proportional_damping.setValidator(StrictDoubleValidator(0, 1, 6))
        self.lineEdit_volumetric_flow_rate.setValidator(StrictDoubleValidator(0, 1e8, 6))

    def _create_connections(self):
        #
        self.comboBox_element_type.currentIndexChanged.connect(
            self.element_type_change_callback
        )
        self.comboBox_selection.currentIndexChanged.connect(
            self.attribution_type_callback
        )
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_get_volumetric_flow_rate.clicked.connect(
            self.get_volumetric_flow_rate_callback
        )
        #
        self.tabWidget_main.currentChanged.connect(self.tab_selection_callback)
        #
        self.treeWidget_element_type.itemClicked.connect(self.on_click_item)
        self.treeWidget_element_type.itemDoubleClicked.connect(
            self.on_double_click_item
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.selection_callback()
        self.element_type_change_callback()

    def selection_callback(self):

        selected_lines = app().main_window.list_selected_lines()
        if not selected_lines:
            return

        self.comboBox_selection.blockSignals(True)

        text = ", ".join([str(i) for i in selected_lines])
        self.lineEdit_selected_id.setText(text)

        self.comboBox_selection.setCurrentIndex(AssignmentType.SELECTED_LINES)
        self.lineEdit_selected_id.setDisabled(False)

        if len(selected_lines) != 1:
            self.comboBox_selection.blockSignals(False)
            return

        line_id = selected_lines[0]
        element_type = self.properties._get_property(
            "acoustic_element_type", line_id=line_id
        )

        if element_type == "undamped":
            self.comboBox_element_type.setCurrentIndex(ElemenType.UNDAMPED)

        elif element_type == "proportional":
            proportional_damping = self.properties._get_property(
                "proportional_damping", line_id=line_id
            )
            if isinstance(proportional_damping, float):
                self.comboBox_element_type.setCurrentIndex(ElemenType.PROPORTIONAL)
                self.lineEdit_proportional_damping.setText(
                    str(proportional_damping)
                )

        elif element_type == "wide_duct":
            self.comboBox_element_type.setCurrentIndex(ElemenType.WIDE_DUCT)

        elif element_type == "LRF_fluid_equivalent":
            self.comboBox_element_type.setCurrentIndex(ElemenType.LRF_FLUID_EQ)

        elif element_type == "LRF_full":
            self.comboBox_element_type.setCurrentIndex(ElemenType.LRF_FULL)

        else:
            mf_element_types = [
                "damped_liquid",
                "undamped_mean_flow",
                "peters",
                "howe",
            ]

            if element_type in mf_element_types:
                volumetric_flow_rate = self.properties._get_property(
                    "volumetric_flow_rate", line_id=line_id
                )

                if isinstance(volumetric_flow_rate, float):
                    self.lineEdit_volumetric_flow_rate.setText(
                        str(volumetric_flow_rate)
                    )
                    self.comboBox_element_type.setCurrentIndex(
                        self.element_types.index(element_type)
                    )

        self.comboBox_selection.blockSignals(False)

    def tab_selection_callback(self):
        if self.tabWidget_main.currentIndex() == TabIndex.SETUP:
            self.attribution_type_callback()

        else:
            self.lineEdit_selected_id.clear()
            self.lineEdit_selected_id.setDisabled(True)

    def attribution_type_callback(self):

        all_lines = self.comboBox_selection.currentIndex() == AssignmentType.ALL_LINES
        self.lineEdit_selected_id.setDisabled(all_lines)

        if self.comboBox_selection.currentIndex() == AssignmentType.ALL_LINES:
            self.lineEdit_selected_id.setText("All lines")
        
        else:
            self.lineEdit_selected_id.clear()
            if app().main_window.list_selected_lines():
                self.selection_callback()

    def element_type_change_callback(self):

        # self.lineEdit_proportional_damping.clear()
        # self.lineEdit_volumetric_flow_rate.clear()

        index = self.comboBox_element_type.currentIndex()
        if index in [ElemenType.UNDAMPED, ElemenType.WIDE_DUCT, ElemenType.LRF_FLUID_EQ, ElemenType.LRF_FULL]:
            self.stackedWidget_main.setVisible(False)
        else:
            self.stackedWidget_main.setVisible(True)

        if index in [ElemenType.DAMPED_LIQUID, ElemenType.UNDAMPED_MEAN_FLOW, ElemenType.PETERS, ElemenType.HOWE]:
            if index == ElemenType.DAMPED_LIQUID:
                self.pushButton_get_volumetric_flow_rate.setText("Pump")
            else:
                self.pushButton_get_volumetric_flow_rate.setText("Compressor")
            self.stackedWidget_main.setCurrentIndex(1)

        elif index == ElemenType.PROPORTIONAL:
            self.stackedWidget_main.setCurrentIndex(0)

        self.element_type = self.element_types[index]

    def attribute_callback(self):

        etype_index = self.comboBox_element_type.currentIndex()

        proportional_damping = None
        if etype_index == ElemenType.PROPORTIONAL:
            if self.lineEdit_proportional_damping.text().isnumeric():
                proportional_damping = float(self.lineEdit_proportional_damping.text())
            if proportional_damping is None:
                return True

        volumetric_flow_rate = None
        if etype_index in [ElemenType.DAMPED_LIQUID, ElemenType.UNDAMPED_MEAN_FLOW, ElemenType.PETERS, ElemenType.HOWE]:
            if self.lineEdit_volumetric_flow_rate.text().isnumeric():
                volumetric_flow_rate = float(self.lineEdit_volumetric_flow_rate.text())
            if volumetric_flow_rate is None:
                return True

        if self.comboBox_selection.currentIndex() == AssignmentType.ALL_LINES:
            line_ids = self.model.mesh.lines_from_model

        else:
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return True

        self.preprocessor.set_acoustic_element_type_by_lines(
            line_ids,
            self.element_type,
            proportional_damping = proportional_damping,
            volumetric_flow_rate = volumetric_flow_rate,
        )

        self.properties._set_line_property(
            "acoustic_element_type", self.element_type, line_ids
        )

        if proportional_damping is None:
            for line_id in line_ids:
                self.properties._remove_line_property("proportional_damping", line_id)

        else:
            self.properties._set_line_property(
                "proportional_damping", proportional_damping, line_ids
            )

        if volumetric_flow_rate is None:
            for line_id in line_ids:
                self.properties._remove_line_property("volumetric_flow_rate", line_id)

        else:
            self.properties._set_line_property(
                "volumetric_flow_rate", volumetric_flow_rate, line_ids
            )

        self.actions_to_finalize()

        if self.comboBox_selection.currentIndex() == AssignmentType.ALL_LINES:
            self.close()

    def remove_callback(self):

        if not self.treeWidget_element_type.selectedItems():
            return

        lineEdit = self.lineEdit_selected_id.text()
        stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
        if stop:
            return True

        for (line_id, data) in self.properties.line_properties.items():
            if "acoustic_element_type" not in data.keys():
                continue

            app().project.model.preprocessor.set_acoustic_element_type_by_lines(line_ids, "undamped")
            app().project.model.properties._remove_line_property("acoustic_element_type", line_ids)
            app().project.model.properties._remove_line_property("proportional_damping", line_ids)
            app().project.model.properties._remove_line_property("volumetric_flow_rate", line_ids)

        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of acoustic element types"
        message = "Would you like to reset the acoustic element types from the model?"

        buttons_config = {"left_button_label": "No", "right_button_label": "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        for (line_id, data) in self.properties.line_properties.items():
            if "acoustic_element_type" in data.keys():

                app().project.model.preprocessor.set_acoustic_element_type_by_lines(line_id, "undamped")
                app().project.model.properties._remove_line_property("acoustic_element_type", line_id)
                app().project.model.properties._remove_line_property("proportional_damping", line_id)
                app().project.model.properties._remove_line_property("volumetric_flow_rate", line_id)

        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.lineEdit_selected_id.clear()
        self.lineEdit_proportional_damping.clear()
        self.lineEdit_volumetric_flow_rate.clear()

        self.load_element_type_info()
        app().project.file.write_line_properties_in_file()

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

        self.lineEdit_volumetric_flow_rate.setText(f"{rms.volumetric_flow_rate: .6e}")

    def on_click_item(self, item: QTreeWidgetItem):
        self.comboBox_selection.setCurrentIndex(AssignmentType.SELECTED_LINES)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)

        lineEdit = self.lineEdit_selected_id.text()
        stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
        if stop:
            return True

        app().main_window.set_selection(lines=line_ids)

    def on_double_click_item(self, item: QTreeWidgetItem):
        self.comboBox_selection.setCurrentIndex(AssignmentType.SELECTED_LINES)
        self.lineEdit_selected_id.setText(item.text(2))
        self.lineEdit_selected_id.setDisabled(True)
        self.get_information(item)

    def load_element_type_info(self):

        self.treeWidget_element_type.clear()

        aux = defaultdict(list)
        for line_id in self.properties.line_properties.keys():
            element_type = self.properties._get_property(
                "acoustic_element_type", line_id=line_id
            )
            if element_type is None:
                continue

            volumetric_flow_rate = self.properties._get_property(
                "volumetric_flow_rate", line_id=line_id
            )
            if volumetric_flow_rate is None:
                volumetric_flow_rate = "---"

            aux[(element_type, volumetric_flow_rate)].append(line_id)

        for key, line_ids in aux.items():
            element_type, volumetric_flow_rate = key
            item = QTreeWidgetItem(
                [element_type, str(volumetric_flow_rate), str(line_ids)[1:-1]]
            )

            for col in range(3):
                item.setTextAlignment(col, Qt.AlignCenter)

            self.treeWidget_element_type.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for data in self.properties.line_properties.values():
            if "acoustic_element_type" in data.keys():
                self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
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
                    element_type = self.properties._get_property(
                        "acoustic_element_type", line_id=line_id
                    )
                    if element_type is None:
                        continue

                    if key == element_type:
                        element_data = [key]

                        if key == "proportional":
                            damping = self.properties._get_property(
                                "proportional_damping", line_id=line_id
                            )
                            if damping is None:
                                continue
                            element_data.append(damping)

                        elif key in ["undamped_mean_flow", "peters", "howe"]:
                            volumetric_flow_rate = self.properties._get_property(
                                "volumetric_flow_rate", line_id=line_id
                            )
                            if volumetric_flow_rate is None:
                                continue
                            element_data.append(volumetric_flow_rate)

                        data[line_id] = element_data

                GetInformationOfGroup(
                    group_label="Element type",
                    selection_label="Line ID:",
                    header_labels=header_labels,
                    column_widths=[70, 140, 150],
                    data=data,
                )

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([warning_title, title, message])

            self.show()

        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
