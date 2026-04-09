
from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.acoustic_property_input_ui import (
    AcousticPropertyInput_UI,
)
from pulse.interface.user_input.model.setup.acoustic.acoustic_nodes_input import (
    AcousticNodesInput,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


error_title = "Error"
warning_title = "Warning"


class VolumeVelocityInput(AcousticNodesInput, AcousticPropertyInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._config_widgets()
        self._create_connections()

        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.array = None
        self.table_name = None
        self.table_path = None
        self.table_values = None

        self.keep_window_open = True
        
    def _config_widgets(self):
        #
        self.label_bondary_condition.setText("Volume velocity:")
        self.label_unit.setText("[m³/s]")
        self.label_title.setText("Volume velocity setup")
        #
        self.treeWidget_nodal_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_search.clicked.connect(self.load_volume_velocity_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) != 1:
                return

            for (property, *args), data in self.properties.nodal_properties.items():
                if property != "volume_velocity":
                    continue

                if selected_nodes != args:
                    continue

                if "table_paths" in data.keys():
                    table_paths = data["table_paths"]
                    self.lineEdit_table_path.setText(table_paths[0])

                else:
                    real_value = float(data["real_values"][0])
                    imag_value = float(data["imag_values"][0])
                    self.lineEdit_real_value.setText(str(real_value))
                    self.lineEdit_imag_value.setText(str(imag_value))

    def tab_event_callback(self):
        self.lineEdit_node_ids.clear()
        self.pushButton_remove.setDisabled(True)
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        if not tab_list:
            self.selection_callback()

        self.lineEdit_node_ids.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "volume_velocity":
                self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property != "volume_velocity":
                continue

            values = data["values"]
            new = QTreeWidgetItem([str(args[0]), str(self.text_label(values[0]))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def attribute_callback(self):
        _input_name = "volume_velocity"
        _properties = [
            "acoustic_pressure",
            "reciprocating_compressor_excitation",
            "reciprocating_pump_excitation",
            "volume_velocity",
        ]
        _reset_camera = False

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabIndex.CONSTANT:
            self.constant_values_attribution_callback(
                lineEdit_node_ids=self.lineEdit_node_ids,
                lineEdit_real=self.lineEdit_real_value,
                lineEdit_imag=self.lineEdit_imag_value,
                input_name=_input_name,
                properties=_properties,
                reset_camera=_reset_camera,
            )
        elif tab_index == TabIndex.TABULAR:
            self.table_values_attribution_callback(
                lineEdit_node_ids=self.lineEdit_node_ids,
                lineEdit_table_path=self.lineEdit_table_path,
                input_name=_input_name,
                properties=_properties,
                reset_camera=_reset_camera,
            )

    def load_volume_velocity_table(self):
        self.imported_values, self.table_path = self.load_table(
            self.lineEdit_table_path, 
            "volume velocity",
            )

        if self.table_path is None:
            self.line_edit_reset(self.lineEdit_table_path)

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item(self, item):
        self.lineEdit_node_ids.setText(item.text(0))

    def remove_callback(self):

        if  self.lineEdit_node_ids.text() == "":
            self.hide()
            title = "Invalid selection"
            message = "You should to select an item from the list "
            message += "to proceed with the removal."
            PrintMessageInput([warning_title, title, message])
            return

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return

        self.properties._remove_nodal_property("volume_velocity", node_ids)
        self.actions_to_finalize(reset_camera=False)

    def reset_callback(self):

        self.hide()

        title = "Resetting of volume velocities"
        message = (
            "Would you like to remove all volume velocities from the acoustic model?"
        )

        buttons_config = {"left_button_label": "No", "right_button_label": "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("volume_velocity")
        self.actions_to_finalize(reset_camera=False)

    def reset_input_fields(self):
        self.lineEdit_node_ids.clear()
        self.lineEdit_real_value.clear()
        self.lineEdit_imag_value.clear()
        self.lineEdit_table_path.clear()
