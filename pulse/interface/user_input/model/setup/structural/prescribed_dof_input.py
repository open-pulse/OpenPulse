from enum import IntEnum
from functools import partial

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.prescribed_dof_input_ui import (
    PrescribedDofInput_UI,
)
from pulse.interface.user_input.model.setup.general.get_information_of_group import (
    GetInformationOfGroup,
)
from pulse.interface.user_input.model.setup.structural.structural_nodes_input import (
    StructuralNodesInput,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput

error_title = "Error"
warning_title = "Warning"


class DOFSetup(IntEnum):
    VALUE = 0
    FREE = 1
    FIXED = 2


class TabType(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


class PrescribedDofInput(StructuralNodesInput, PrescribedDofInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_widgets()
        self._initialize()
        self._create_connections()

        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.reset_table_variables()
        self.create_widgets_lists()

        self.keep_window_open = True

        self.list_Nones = [None, None, None, None, None, None]
        self.dofs_labels = np.array(["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"])

    def create_widgets_lists(self):

        self.value_comboboxes = [
            self.comboBox_displacement_ux,
            self.comboBox_displacement_uy,
            self.comboBox_displacement_uz,
            self.comboBox_rotation_rx,
            self.comboBox_rotation_ry,
            self.comboBox_rotation_rz,
        ]

        self.constant_line_edits = {
            "Ux": [self.lineEdit_real_ux, self.lineEdit_imag_ux],
            "Uy": [self.lineEdit_real_uy, self.lineEdit_imag_uy],
            "Uz": [self.lineEdit_real_uz, self.lineEdit_imag_uz],
            "Rx": [self.lineEdit_real_rx, self.lineEdit_imag_rx],
            "Ry": [self.lineEdit_real_ry, self.lineEdit_imag_ry],
            "Rz": [self.lineEdit_real_rz, self.lineEdit_imag_rz],
        }

        self.dof_setup_combo_boxes = {
            "Ux": self.comboBox_displacement_ux,
            "Uy": self.comboBox_displacement_uy,
            "Uz": self.comboBox_displacement_uz,
            "Rx": self.comboBox_rotation_rx,
            "Ry": self.comboBox_rotation_ry,
            "Rz": self.comboBox_rotation_rz,
        }

        self.list_lineEdit_constant_values = [
            [self.lineEdit_real_ux, self.lineEdit_imag_ux],
            [self.lineEdit_real_uy, self.lineEdit_imag_uy],
            [self.lineEdit_real_uz, self.lineEdit_imag_uz],
            [self.lineEdit_real_rx, self.lineEdit_imag_rx],
            [self.lineEdit_real_ry, self.lineEdit_imag_ry],
            [self.lineEdit_real_rz, self.lineEdit_imag_rz],
        ]

        self.list_lineEdit_table_values = [
            self.lineEdit_ux_table_path,
            self.lineEdit_uy_table_path,
            self.lineEdit_uz_table_path,
            self.lineEdit_rx_table_path,
            self.lineEdit_ry_table_path,
            self.lineEdit_rz_table_path,
        ]

    def reset_table_variables(self):

        self.imported_ux_values = None
        self.imported_uy_values = None
        self.imported_uz_values = None
        self.imported_rx_values = None
        self.imported_ry_values = None
        self.imported_rz_values = None

        self.ux_table_path = None
        self.uy_table_path = None
        self.uz_table_path = None
        self.rx_table_path = None
        self.ry_table_path = None
        self.rz_table_path = None

    def _config_widgets(self):
        #
        for i, width in enumerate([80, 60]):
            self.treeWidget_nodal_info.setColumnWidth(i, width)
            self.treeWidget_nodal_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.pushButton_exit_tab0.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribution_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_load_ux_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_ux_table_path, dof_label="Ux"))
        self.pushButton_load_uy_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_uy_table_path, dof_label="Uy"))
        self.pushButton_load_uz_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_uz_table_path, dof_label="Uz"))
        self.pushButton_load_rx_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_rx_table_path, dof_label="Rx"))
        self.pushButton_load_ry_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_ry_table_path, dof_label="Ry"))
        self.pushButton_load_rz_table.clicked.connect(partial(self.load_table_for_line_edit, line_edit=self.lineEdit_rz_table_path, dof_label="Rz"))
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_all_dof_free.clicked.connect(self.all_dof_free_callback)
        self.pushButton_all_dof_fixed.clicked.connect(self.all_dof_fixed_callback)
        self.comboBox_displacement_ux.currentIndexChanged.connect(
            self.displacement_ux_callback
        )
        self.comboBox_displacement_uy.currentIndexChanged.connect(
            self.displacement_uy_callback
        )
        self.comboBox_displacement_uz.currentIndexChanged.connect(
            self.displacement_uz_callback
        )
        self.comboBox_rotation_rx.currentIndexChanged.connect(self.rotation_rx_callback)
        self.comboBox_rotation_ry.currentIndexChanged.connect(self.rotation_ry_callback)
        self.comboBox_rotation_rz.currentIndexChanged.connect(self.rotation_rz_callback)
        #
        self.tabWidget_prescribed_dof.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        self.selection_callback()

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) == 1:
                prop_data = self.properties._get_property(
                    "prescribed_dofs", node_ids=selected_nodes[0]
                )
                if not isinstance(prop_data, dict):
                    return

                if "table_paths" in prop_data.keys():
                    table_paths = prop_data["table_paths"]
                    for index, lineEdit_table in enumerate(
                        self.list_lineEdit_table_values
                    ):
                        table_path = table_paths[index]
                        if table_path is not None:
                            lineEdit_table.setText(table_path)

                else:
                    values = prop_data["values"]
                    for index, (
                        unit_label,
                        (line_edit_real, line_edit_imag),
                    ) in enumerate(self.constant_line_edits.items()):
                        if values[index] is None:
                            self.dof_setup_combo_boxes[unit_label].setCurrentIndex(
                                DOFSetup.FREE
                            )

                        elif isinstance(values[index], complex):
                            if values[index] == complex(0):
                                self.dof_setup_combo_boxes[unit_label].setCurrentIndex(
                                    DOFSetup.FIXED
                                )
                            else:
                                self.dof_setup_combo_boxes[unit_label].setCurrentIndex(
                                    DOFSetup.VALUE
                                )

                        if isinstance(values[index], complex):
                            if values[index] == complex(0):
                                continue

                            line_edit_real.setText(str(np.real(values[index])))
                            line_edit_imag.setText(str(np.imag(values[index])))

    def check_complex_entries(
        self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit, label: str
    ):

        _real = None
        input_real = lineEdit_real.text()

        stop = False
        if input_real != "":
            if input_real == "fixed":
                _real = 0.0
            elif input_real != "free":
                try:
                    _real = float(input_real)
                except Exception:
                    title = f"Invalid entry to the {label}"
                    message = f"Wrong input for real part of {label}."
                    PrintMessageInput([error_title, title, message])
                    lineEdit_real.setFocus()
                    stop = True
                    return stop, None

        _imag = None
        input_imag = lineEdit_imag.text()

        if input_imag != "":
            if input_imag == "fixed":
                _imag = 0.0
            elif input_imag != "free":
                try:
                    _imag = float(input_imag)
                except Exception:
                    title = f"Invalid entry to the {label}"
                    message = f"Wrong input for imaginary part of {label}."
                    PrintMessageInput([error_title, title, message])
                    lineEdit_imag.setFocus()
                    stop = True
                    return stop, None

        if label == "all dofs":
            if _real is None and _imag is None:
                value = None
            elif _real is None:
                value = 1j * _imag
            elif _imag is None:
                value = complex(_real)
            else:
                value = _real + 1j * _imag
            output = [value, value, value, value, value, value]

        else:
            if _real is None and _imag is None:
                output = None
            elif _real is None:
                output = 1j * _imag
            elif _imag is None:
                output = complex(_real)
            else:
                output = _real + 1j * _imag

        return stop, output

    def constant_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        stop, ux = self.check_complex_entries(
            self.lineEdit_real_ux, self.lineEdit_imag_ux, "Ux"
        )
        if stop:
            return
        stop, uy = self.check_complex_entries(
            self.lineEdit_real_uy, self.lineEdit_imag_uy, "Uy"
        )
        if stop:
            return
        stop, uz = self.check_complex_entries(
            self.lineEdit_real_uz, self.lineEdit_imag_uz, "Uz"
        )
        if stop:
            return

        stop, rx = self.check_complex_entries(
            self.lineEdit_real_rx, self.lineEdit_imag_rx, "Rx"
        )
        if stop:
            return
        stop, ry = self.check_complex_entries(
            self.lineEdit_real_ry, self.lineEdit_imag_ry, "Ry"
        )
        if stop:
            return
        stop, rz = self.check_complex_entries(
            self.lineEdit_real_rz, self.lineEdit_imag_rz, "Rz"
        )
        if stop:
            return

        prescribed_dofs = [ux, uy, uz, rx, ry, rz]
        all_dof_free = prescribed_dofs.count(None) == 6

        self.remove_properties_from_node(node_ids, all_dof_free=all_dof_free)

        if all_dof_free:
            self.actions_to_finalize()
            return

        real_values = [
            value if value is None else np.real(value) for value in prescribed_dofs
        ]
        imag_values = [
            value if value is None else np.imag(value) for value in prescribed_dofs
        ]

        for node_id in node_ids:
            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords": list(coords),
                "values": prescribed_dofs,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_nodal_property("prescribed_dofs", data, node_id)

        app().project.file.write_nodal_properties_in_file()
        self.load_nodes_info()
        app().main_window.update_plots(reset_camera=False)
    
    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "prescribed_dof")

    def integrate_and_save_table_values(
        self,
        table_name: str,
        imported_values: np.ndarray,
        linear: bool = False,
        angular: bool = False,
    ):

        index_lin = self.comboBox_linear_data_type.currentIndex()
        index_ang = self.comboBox_angular_data_type.currentIndex()

        zero_filter = False
        if imported_values[0, 0] == 0:
            if linear and index_lin != 0:
                zero_filter = True

            if angular and index_ang != 0:
                zero_filter = True

        if zero_filter:
            freq_mask = imported_values[:, 0] > 0
        else:
            freq_mask = imported_values[:, 0] >= 0

        _imported_values = imported_values[freq_mask, :]

        # define the frequencies vector
        _frequencies = _imported_values[:, 0]

        # real values vector
        real_values = _imported_values[:, 1]

        # imaginary values vector
        imag_values = _imported_values[:, 2]

        complex_values = real_values + 1j * imag_values

        if bool(index_lin) or bool(index_ang):
            if linear:
                complex_values /= (1j * 2 * np.pi * _frequencies) ** index_lin

            if angular:
                complex_values /= (1j * 2 * np.pi * _frequencies) ** index_ang

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        if bool(index_lin) or bool(index_ang):
            # real values vector
            real_values = np.real(complex_values)

            # imaginary values vector
            imag_values = np.imag(complex_values)

        else:
            # real values vector
            real_values = _imported_values[:, 1]

            # imaginary values vector
            imag_values = _imported_values[:, 2]

        # array to be saved
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        self.remove_properties_from_node(node_ids)

        table_paths = list()
        dof_labels = ["ux", "uy", "uz", "rx", "ry", "rz"]

        for label in dof_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(
                    line_edit,
                    "prescribed dof",
                    dof_label=label.capitalize(),
                    direct_load=True,
                )
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        for node_id in node_ids:
            table_names = list()

            for i, label in enumerate(dof_labels):
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(
                        f"prescribed_dof_{label}", node_id=node_id
                    )
                    if self.integrate_and_save_table_values(
                        _table_name, _imported_values, linear=i <= 2, angular=i >= 3
                    ):
                        return

                table_names.append(_table_name)

            if table_names == self.list_Nones:
                title = "Additional inputs required"
                message = "You must inform at least one prescribed dof "
                message += "table path before confirming the input!"
                PrintMessageInput([error_title, title, message])
                return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)
        
            data = {
                "coords": list(coords),
                "table_names": table_names,
                "table_paths": table_paths,
            }

            self.properties._set_nodal_property("prescribed_dofs", data, node_id)

        app().project.file.write_nodal_properties_in_file()

        self.actions_to_finalize()

    def attribution_callback(self):
        tab_index = self.tabWidget_prescribed_dof.currentIndex()
        if tab_index == TabType.CONSTANT:
            self.constant_values_attribution_callback()

        elif tab_index == TabType.TABULAR:
            self.table_values_attribution_callback()

    def all_dof_free_callback(self):
        for combobox in self.value_comboboxes:
            combobox.setCurrentIndex(DOFSetup.FREE)

        for lineEdit_real, lineEdit_imag in self.constant_line_edits.values():
            lineEdit_real.setText("free")
            lineEdit_imag.setText("free")

    def all_dof_fixed_callback(self):
        for combobox in self.value_comboboxes:
            combobox.setCurrentIndex(DOFSetup.FIXED)

        for lineEdit_real, lineEdit_imag in self.constant_line_edits.values():
            lineEdit_real.setText("fixed")
            lineEdit_imag.setText("fixed")

    def combo_box_callback(self, unit_label: str):

        combo_box = self.dof_setup_combo_boxes[unit_label]
        value_based = combo_box.currentIndex() == DOFSetup.VALUE

        line_edit_real, line_edit_imag = self.constant_line_edits.get(
            unit_label, (None, None)
        )
        if (line_edit_real, line_edit_imag).count(None) == 2:
            return

        line_edit_real.clear()
        line_edit_imag.clear()
        line_edit_real.setEnabled(value_based)
        line_edit_imag.setEnabled(value_based)

        if value_based:
            return

        if combo_box.currentIndex() == DOFSetup.FIXED:
            line_edit_real.setText("fixed")
            line_edit_imag.setText("fixed")

        elif combo_box.currentIndex() == DOFSetup.FREE:
            line_edit_real.setText("free")
            line_edit_imag.setText("free")

    def displacement_ux_callback(self):
        self.combo_box_callback("Ux")

    def displacement_uy_callback(self):
        self.combo_box_callback("Uy")

    def displacement_uz_callback(self):
        self.combo_box_callback("Uz")

    def rotation_rx_callback(self):
        self.combo_box_callback("Rx")

    def rotation_ry_callback(self):
        self.combo_box_callback("Ry")

    def rotation_rz_callback(self):
        self.combo_box_callback("Rz")

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "prescribed_dofs":
                values = data["values"]
                constrained_dofs_mask = [
                    False if value is None else True for value in values
                ]
                new = QTreeWidgetItem(
                    [
                        str(args[0]),
                        str(self.text_label(constrained_dofs_mask, self.dofs_labels)),
                    ]
                )
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.tabWidget_prescribed_dof.setTabVisible(TabType.LIST, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "prescribed_dofs":
                self.tabWidget_prescribed_dof.setCurrentIndex(TabType.CONSTANT)
                self.tabWidget_prescribed_dof.setTabVisible(TabType.LIST, True)
                return

    def tab_event_callback(self):

        tab_list = self.tabWidget_prescribed_dof.currentIndex() == TabType.LIST
        self.lineEdit_node_ids.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)
        self.pushButton_remove.setDisabled(True)

        if not tab_list:
            self.lineEdit_node_ids.setEnabled(True)
            self.selection_callback()
            return

        selected_items = self.treeWidget_nodal_info.selectedItems()
        if selected_items == list():
            self.lineEdit_node_ids.clear()
        else:
            self.on_click_item(selected_items[0])

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_double_click_item(self, item):
        # self.on_click_item(item)
        self.lineEdit_node_ids.setText(item.text(0))
        self.get_nodal_info(item)

    def get_nodal_info(self, item):
        try:
            loads_info = dict()
            selected_node = int(item.text(0))

            for (property, *args), data in self.properties.nodal_properties.items():
                if property == "prescribed_dofs" and selected_node == args[0]:
                    values = data["values"]
                    nodal_loads_mask = [False if bc is None else True for bc in values]

                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.dofs_labels[i]
                            loads_info[selected_node, dof_label] = values[i]

            if len(loads_info):
                self.hide()
                header_labels = ["Node ID", "DOF label", "Value"]
                GetInformationOfGroup(
                    group_label="Prescribed dofs",
                    selection_label="Node ID:",
                    header_labels=header_labels,
                    column_widths=[70, 140, 150],
                    data=data,
                )

        except Exception as error_log:
            title = "Error while gathering prescribed dofs information"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return

    def remove_properties_from_node(
        self, node_ids: int | list | tuple, all_dof_free: bool = False
    ):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for _property in ["nodal_loads", "prescribed_dofs"]:
                if all_dof_free and _property == "nodal_loads":
                    continue

                self.properties._remove_nodal_property(_property, node_id)

        app().project.file.write_nodal_properties_in_file()

    def remove_callback(self):

        if self.lineEdit_node_ids.text() == "":
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

        self.properties._remove_nodal_property("prescribed_dofs", node_ids)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of prescribed dofs"
        message = (
            "Would you like to remove all prescribed dofs from the structural model?"
        )

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("prescribed_dofs")
        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize()

    def reset_input_fields(self):
        self.lineEdit_node_ids.clear()
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.clear()
            lineEdit_imag.clear()

        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_prescribed_dof.currentIndex() == TabType.LIST:
                return

            self.attribution_callback()

        elif event.key() == Qt.Key_Delete:
            self.remove_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
