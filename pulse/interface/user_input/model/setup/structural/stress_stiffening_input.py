from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem#, QHeaderView

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.stress_stiffening_input_ui import (
    StressStiffeningInput_UI,
)
from pulse.interface.user_input.model.setup.user_input import UserInput
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    PressureUnits,
    pressure_units_labels,
)
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


class AssignmentType(IntEnum):
    ALL_LINES = 0
    SELECTED_LINES = 1


error_title = "Error"


class StressStiffeningInput(UserInput, StressStiffeningInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties
        self.before_run = app().project.get_pre_solution_model_checks()

        self._initialize()
        self._config_widgets()
        self.configure_dynamic_validators()
        self._create_connections()

        self.load_lines_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True

    def _config_widgets(self):
        #
        # self.treeWidget_lines_info.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        #
        for i, width in enumerate([60, 140, 140]):
            self.treeWidget_lines_info.setColumnWidth(i, width)
            self.treeWidget_lines_info.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self._load_units_labels()

    def configure_dynamic_validators(self):

        # adjust pressure bounds (p_min -> perfect vacuum)      
        p_min = 0 
        p_max = 1e10

        punit_index = self.comboBox_pressure_units.currentIndex()
        if punit_index == PressureUnits.Pa_g:
            p_min = -101325

        elif punit_index == PressureUnits.kPa_g:
            p_min = -101.325

        elif punit_index == PressureUnits.bar_g:
            p_min = -1.101325
            p_max = 2e3

        elif punit_index == PressureUnits.kgf_cm2_g:
            p_min = -(9.80665*1e4)

        elif punit_index == PressureUnits.psi_g:
            p_min = -(0.45359237*9.80665) / (0.0254**2)

        elif punit_index == PressureUnits.ksi_g:
            p_min = -(0.45359237*9.80665) / (1e3 * (0.0254**2))
            p_max = 1e3

        # configure validator for pressure and temeperature inputs
        self.lineEdit_external_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_internal_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))

        press_unit = self.comboBox_pressure_units.currentText()
        self.label_external_pressure_unit.setText(f"[{press_unit}]")
        self.label_internal_pressure_unit.setText(f"[{press_unit}]")

    def _load_units_labels(self):

        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()

        # add pressure labels into unit comboBox
        self.comboBox_pressure_units.addItems(pressure_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("Pa (a)")

    def _create_connections(self):
        #
        self.comboBox_attribution_type.currentIndexChanged.connect(self.attribution_type_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_lines_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_lines_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.selection_callback()

    def selection_callback(self):

        selected_lines = app().main_window.list_selected_lines()
        if not selected_lines:
            return

        self.comboBox_attribution_type.blockSignals(True)

        text = ", ".join([str(i) for i in selected_lines])
        self.lineEdit_selected_id.setText(text)

        self.lineEdit_selected_id.setEnabled(True)
        self.comboBox_attribution_type.setCurrentIndex(AssignmentType.SELECTED_LINES)

        if len(selected_lines) == 1:
            line_id = selected_lines[0]
            prop_data = self.properties._get_property("stress_stiffening", line_id=line_id)
            self.load_property_data(prop_data)

        self.comboBox_attribution_type.blockSignals(False)

    def load_property_data(self, data: dict):
        if not isinstance(data, dict):
            return

        pressure_unit = data.get("pressure_unit", "Pa (a)")
        external_pressure = data.get("external_pressure")
        internal_pressure = data.get("internal_pressure")
        self.comboBox_pressure_units.setCurrentText(pressure_unit)
        self.lineEdit_external_pressure.setText(f"{external_pressure : .8e}")
        self.lineEdit_internal_pressure.setText(f"{internal_pressure : .8e}")

    def attribution_type_callback(self):

        all_lines = self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_LINES
        self.lineEdit_selected_id.setDisabled(all_lines)

        if all_lines:
            self.lineEdit_selected_id.setText("All lines")
            return

        self.lineEdit_selected_id.clear()
        self.selection_callback()

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.frame_attribution_options.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

        if tab_list:
            self.lineEdit_selected_id.clear()
            self.comboBox_attribution_type.setCurrentIndex(AssignmentType.SELECTED_LINES)

    def on_click_item(self, item: QTreeWidgetItem):

        line_ids = list()
        for item in self.treeWidget_lines_info.selectedItems():
            line_ids.append(int(item.text(0)))

        text = ", ".join([str(i) for i in line_ids])      
        self.lineEdit_selected_id.setText(text)

        self.lineEdit_selected_id.setDisabled(True)
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def attribute_callback(self):
        
        external_pressure = 0.
        if self.lineEdit_external_pressure.text() != "":
            external_pressure = float(self.lineEdit_external_pressure.text())

        internal_pressure = 0.
        if self.lineEdit_external_pressure.text() != "":
            internal_pressure = float(self.lineEdit_internal_pressure.text())

        if not any((external_pressure, internal_pressure)):
            title = "Empty entries at the input pressure fields"
            message = "Enter a value different from zero at the external "
            message += "or internal pressure field inputs to continue."
            PrintMessageInput([error_title, title, message])  
            return
        
        parameters = {
            "pressure_unit" : self.comboBox_pressure_units.currentText(),
            "external_pressure" : external_pressure,
            "internal_pressure" : internal_pressure,
            }

        if self.comboBox_attribution_type.currentIndex() == AssignmentType.ALL_LINES:
            line_ids = app().project.model.mesh.lines_from_model
    
        elif self.comboBox_attribution_type.currentIndex() == AssignmentType.SELECTED_LINES:
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return

        else:
            return

        filtered_selection = list()
        for line_id in line_ids:
            element_type = self.properties._get_property("structural_element_type", line_id=line_id)
            if element_type != "pipe_1":
                continue

            filtered_selection.append(line_id)

        if not filtered_selection:
            return

        # app().main_window.set_selection(lines=filtered_selection)

        self.preprocessor.set_stress_stiffening_by_lines(filtered_selection, parameters)
        self.properties._set_line_property("stress_stiffening", parameters, filtered_selection)

        self.actions_to_finalize()
        self.complete = True

    def remove_callback(self):

        line_ids = list()
        for item in self.treeWidget_lines_info.selectedItems():
            line_ids.append(int(item.text(0)))

        parameters = {
            "external_pressure" : 0.,
            "internal_pressure" : 0.,
            }

        self.preprocessor.set_stress_stiffening_by_lines(line_ids, parameters)
        self.properties._remove_line_property("stress_stiffening", line_ids)

        self.lineEdit_selected_id.clear()
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Stress stiffenings resetting"
        message = "Would you like to remove the stress stiffenings from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        line_ids = list()
        for (line_id, data) in self.properties.line_properties.items():
            if "stress_stiffening" in data.keys():
                line_ids.append(line_id)

        parameters = {
            "external_pressure" : 0.,
            "internal_pressure" : 0.,
            }

        self.preprocessor.set_stress_stiffening_by_lines(line_ids, parameters)
        self.properties._remove_line_property("stress_stiffening", line_ids)

        self.actions_to_finalize()

    def actions_to_finalize(self):

        self.load_lines_info()
        app().project.file.write_line_properties_in_file()

        self.preprocessor.stress_stiffening_enabled = False
        for data in self.properties.line_properties.values():
            if "stress_stiffening" in data.keys():
                self.preprocessor.stress_stiffening_enabled = True
                return

    def load_lines_info(self):

        self.treeWidget_lines_info.clear()
        for line_id, data in self.properties.line_properties.items():

            if "stress_stiffening" in data.keys():
                prop_data = data.get("stress_stiffening")
                if not isinstance(prop_data, dict):
                    continue

                pressure_unit = prop_data.get("pressure_unit", "Pa (a)")
                ext_pressure = prop_data.get("external_pressure")
                int_pressure = prop_data.get("internal_pressure")

                item = QTreeWidgetItem([
                    f"{line_id}",
                    f"{ext_pressure : .4e}", 
                    f"{int_pressure : .4e}",
                    pressure_unit,
                    ])

                for i in range(4):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_lines_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        self.pushButton_remove.setDisabled(True)
        for data in self.properties.line_properties.values():
            if "stress_stiffening" not in data.keys():
                continue

            self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
            return

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
        self.lineEdit_external_pressure.setFocus()

        if self.comboBox_attribution_type.currentIndex() == AssignmentType.SELECTED_LINES:
            if not self.lineEdit_selected_id.isEnabled():
                self.lineEdit_selected_id.setEnabled(True)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        if event.key() == Qt.Key_Delete:
            self.remove_callback()

        if event.key() == Qt.Key_Escape:
            self.close()