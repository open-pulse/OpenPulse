from enum import IntEnum

import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtWidgets import QHeaderView, QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface import error_title, warning_title
from pulse.interface.ui_generated.model.setup.structural.elastic_nodal_links_input_ui import (
    ElasticNodalLinksInput_UI,
)
from pulse.interface.user_input.model.setup.structural.structural_nodes_input import (
    StructuralNodesInput,
)
from pulse.interface.user_input.numeric_checks.double_validator import (
    StrictDoubleValidator,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


class TabList(IntEnum):
    MULTIPLE = 0
    STIFFNESS_LINK = 1
    DAMPINGS_LINK = 2


class NodalLinkType(IntEnum):
    STIFFNESS = 0
    DAMPING = 1


class ElasticNodalLinksInput(StructuralNodesInput, ElasticNodalLinksInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._config_widgets()
        self._configure_validators()
        self._create_connections()

        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.damping_labels = ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]
        self.stiffness_labels = ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]

        self.reset_table_variables()
        self.create_widgets_lists()

        self.complete = False
        self.keep_window_open = True
        self.link_applied = False

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        self.treeWidget_stiffness_nodal_links.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.treeWidget_damping_nodal_links.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        for i in range(2):
            self.treeWidget_stiffness_nodal_links.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_damping_nodal_links.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _configure_validators(self):

        validator = StrictDoubleValidator(-1e10, 1e10, 6)

        for line_edit in self.findChildren(QLineEdit):
            obj_name = line_edit.objectName()

            if "table_path" in obj_name:
                continue

            if obj_name in ["lineEdit_first_node_id", "lineEdit_last_node_id"]:
                continue

            line_edit.setValidator(validator)

    def reset_table_variables(self):
        for label in self.damping_labels + self.stiffness_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

    def create_widgets_lists(self):

        self.lineEdits_constant_values_stiffness = [
            self.lineEdit_Kx,
            self.lineEdit_Ky,
            self.lineEdit_Kz,
            self.lineEdit_Krx,
            self.lineEdit_Kry,
            self.lineEdit_Krz,
        ]

        self.lineEdits_constant_values_dampings = [
            self.lineEdit_Cx,
            self.lineEdit_Cy,
            self.lineEdit_Cz,
            self.lineEdit_Crx,
            self.lineEdit_Cry,
            self.lineEdit_Crz,
        ]

        self.lineEdits_table_values_stiffness = [
            self.lineEdit_Kx_table_path,
            self.lineEdit_Ky_table_path,
            self.lineEdit_Kz_table_path,
            self.lineEdit_Krx_table_path,
            self.lineEdit_Kry_table_path,
            self.lineEdit_Krz_table_path,
        ]

        self.lineEdits_table_values_dampings = [
            self.lineEdit_Cx_table_path,
            self.lineEdit_Cy_table_path,
            self.lineEdit_Cz_table_path,
            self.lineEdit_Crx_table_path,
            self.lineEdit_Cry_table_path,
            self.lineEdit_Crz_table_path,
        ]

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if (
                    obj == widget
                    and event.type() == QEvent.MouseButtonRelease
                    and obj.rect().contains(event.pos())
                ):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_first_node_clicked(self):
        self.current_lineEdit = self.lineEdit_first_node_id

    def lineEdit_last_node_clicked(self):
        self.current_lineEdit = self.lineEdit_last_node_id

    def _create_connections(self):
        #
        self.clickable(self.lineEdit_first_node_id).connect(
            self.lineEdit_first_node_clicked
        )
        self.clickable(self.lineEdit_last_node_id).connect(
            self.lineEdit_last_node_clicked
        )
        self.current_lineEdit = self.lineEdit_first_node_id
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        self.connect_load_table_push_buttons(self.lineEdits_table_values_dampings, self.damping_labels)
        self.connect_load_table_push_buttons(self.lineEdits_table_values_stiffness, self.stiffness_labels)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_stiffness_nodal_links.itemClicked.connect(
            self.on_click_item_stiffness
        )
        self.treeWidget_damping_nodal_links.itemClicked.connect(
            self.on_click_item_damping
        )
        self.treeWidget_stiffness_nodal_links.itemDoubleClicked.connect(
            self.on_double_click_item_stiffness
        )
        self.treeWidget_damping_nodal_links.itemDoubleClicked.connect(
            self.on_double_click_item_damping
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        self.selection_callback()

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            if len(selected_nodes) == 1:
                self.current_lineEdit.setText(str(selected_nodes[0]))

            elif len(selected_nodes) == 2:
                first_node = min(selected_nodes)
                last_node = max(selected_nodes)
                sorted_nodes = [first_node, last_node]
                self.lineEdit_first_node_id.setText(str(first_node))
                self.lineEdit_last_node_id.setText(str(last_node))

                ss_link_data = self.properties._get_property(
                    "stiffness_nodal_links", node_ids=sorted_nodes
                )
                if isinstance(ss_link_data, dict):
                    self.reset_stiffness_input_fields()
                    self.reset_dampings_input_fields()

                    if "table_paths" in ss_link_data.keys():
                        self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR)
                        self.tabWidget_table_values.setCurrentIndex(NodalLinkType.STIFFNESS)
                        for i, table_path in enumerate(ss_link_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_stiffness[i]
                                lineEdit.setText(table_path)

                    else:
                        self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                        self.tabWidget_constant_values.setCurrentIndex(NodalLinkType.STIFFNESS)
                        for i, value in enumerate(ss_link_data["values"]):
                            if isinstance(value, complex):
                                _value = np.real(value)
                                lineEdit = self.lineEdits_constant_values_stiffness[i]
                                lineEdit.setText(f"{_value: .3e}")

                sd_link_data = self.properties._get_property(
                    "damping_nodal_links", node_ids=sorted_nodes
                )
                if isinstance(sd_link_data, dict):
                    if "table_paths" in sd_link_data.keys():
                        self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR)
                        self.tabWidget_table_values.setCurrentIndex(NodalLinkType.DAMPING)
                        for i, table_path in enumerate(sd_link_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_dampings[i]
                                lineEdit.setText(table_path)

                    else:
                        self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                        self.tabWidget_constant_values.setCurrentIndex(NodalLinkType.DAMPING)
                        for i, value in sd_link_data["values"]:
                            if isinstance(value, complex):
                                _value = np.real(value)
                                lineEdit = self.lineEdits_constant_values_dampings[i]
                                lineEdit.setText(f"{_value: .3e}")

    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "nodal link")

    def check_linked_nodes(self):

        stop, node_id1 = self.before_run.check_selected_ids(
            self.lineEdit_first_node_id.text(),
            "nodes",
            single_id=True,
        )

        if stop:
            return True, None

        stop, node_id2 = self.before_run.check_selected_ids(
            self.lineEdit_last_node_id.text(),
            "nodes",
            single_id=True,
        )

        if stop:
            return True, None

        if node_id1 == node_id2:
            self.hide()
            title = "invalid pair of nodes selected"
            message = (
                "The selected nodes must differ. Try to choose another pair of nodes."
            )
            PrintMessageInput([error_title, title, message])
            return True, None

        return False, sorted([node_id1, node_id2])

    def check_constant_stiffness_links(self, node_ids: list[int, int]):

        Kx = self.check_entries(self.lineEdit_Kx)
        Ky = self.check_entries(self.lineEdit_Ky)
        Kz = self.check_entries(self.lineEdit_Kz)
        Krx = self.check_entries(self.lineEdit_Krx)
        Kry = self.check_entries(self.lineEdit_Kry)
        Krz = self.check_entries(self.lineEdit_Krz)

        values = [Kx, Ky, Kz, Krx, Kry, Krz]

        if values.count(None) != 6:
            self.link_applied = True

            real_values = [
                value if value is None else np.real(value) for value in values
            ]
            imag_values = [
                value if value is None else np.imag(value) for value in values
            ]

            coords = list()
            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))

            data = {
                "coords": coords,
                "values": values,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_nodal_property("stiffness_nodal_links", data, node_ids)

    def check_constant_dampings_links(self, node_ids: list[int, int]):

        Cx = self.check_entries(self.lineEdit_Cx)
        Cy = self.check_entries(self.lineEdit_Cy)
        Cz = self.check_entries(self.lineEdit_Cz)
        Crx = self.check_entries(self.lineEdit_Crx,)
        Cry = self.check_entries(self.lineEdit_Cry,)
        Crz = self.check_entries(self.lineEdit_Crz,)

        values = [Cx, Cy, Cz, Crx, Cry, Crz]

        if values.count(None) != 6:
            self.link_applied = True

            real_values = [
                value if value is None else np.real(value) for value in values
            ]
            imag_values = [
                value if value is None else np.imag(value) for value in values
            ]

            coords = list()
            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))

            data = {
                "coords": coords,
                "values": values,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_nodal_property("damping_nodal_links", data, node_ids)

    def check_tables_for_stiffness_links(self, node_ids_pair: list[int, int]):

        table_paths = list()

        for label in self.stiffness_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(
                    line_edit, "nodal link", dof_label=label, direct_load=True
                )
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        table_names = list()

        for label in self.stiffness_labels:
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            _table_name = None
            if isinstance(_imported_values, np.ndarray):
                _table_name = self.get_table_name(
                    f"stiffness_link_{label}", node_id=node_ids_pair
                )
                if self.save_table_values(_table_name, _imported_values):
                    return

            table_names.append(_table_name)

        if (table_names).count(None) != 6:
            self.link_applied = True

            coords = list()
            for node_id in node_ids_pair:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))

            data = {
                "coords": coords,
                "table_names": table_names,
                "table_paths": table_paths,
            }

            self.properties._set_nodal_property(
                "stiffness_nodal_links", data, node_ids_pair
            )

    def check_tables_for_dampings_links(self, node_ids_pair: list[int, int]):

        table_paths = list()

        for label in self.damping_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(
                    line_edit, "nodal link", dof_label=label, direct_load=True
                )
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

        table_names = list()

        for label in self.damping_labels:
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            _table_name = None
            if isinstance(_imported_values, np.ndarray):
                _table_name = self.get_table_name(
                    f"damping_link_{label}", node_id=node_ids_pair
                )
                if self.save_table_values(_table_name, _imported_values):
                    return

            table_names.append(_table_name)

        if (table_names).count(None) != 6:
            self.link_applied = True

            coords = list()
            for node_id in node_ids_pair:
                node = app().project.model.preprocessor.nodes[node_id]
                coords.extend(list(np.round(node.coordinates, 5)))
            
            table_paths = [str(path) if path is not None else None for path in table_paths]

            data = {
                "coords": coords,
                "table_names": table_names,
                "table_paths": table_paths,
            }

            self.properties._set_nodal_property(
                "damping_nodal_links", data, node_ids_pair
            )

    def attribute_callback(self):

        stop, node_ids = self.check_linked_nodes()
        if stop:
            return True
        
        self.remove_properties_from_node(node_ids)

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabIndex.CONSTANT:
            self.check_constant_values_inputs(node_ids)

        elif tab_index == TabIndex.TABULAR:
            self.check_table_values_inputs(node_ids)

        if not self.link_applied:
            title = "No inputs entered for the structural stiffness or damping links"
            message = "Define at least one value or table of values to the stiffness "
            message += "or damping links to proceed with the structural link attribution."
            PrintMessageInput([error_title, title, message])
            return

        self.reset_nodes_input_fields()
        self.actions_to_finalize()

    def check_constant_values_inputs(self, node_ids: list[int, int]):
        self.check_constant_stiffness_links(node_ids)
        self.check_constant_dampings_links(node_ids)

    def check_table_values_inputs(self, node_ids: list[int, int]):
        self.check_tables_for_stiffness_links(node_ids)
        self.check_tables_for_dampings_links(node_ids)

    def remove_properties_from_node(self, node_ids_pair: list | tuple):
        _properties = ["stiffness_nodal_links", "damping_nodal_links"]
        for _property in _properties:
            self.properties._remove_nodal_property(_property, node_ids_pair)

    def remove_callback(self):

        _first_node = self.lineEdit_first_node_id.text()
        _last_node = self.lineEdit_last_node_id.text()

        if _first_node == "" and _last_node == "":
            self.hide()
            title = "Invalid selection"
            message = "You should to select an item from the list "
            message += "to proceed with the removal."
            PrintMessageInput([warning_title, title, message])
            return

        node_ids = sorted([int(_first_node), int(_last_node)])

        if self.checkBox_remove_link_stiffness.isChecked():
            self.properties._remove_nodal_property("stiffness_nodal_links", node_ids)

        if self.checkBox_remove_link_damping.isChecked():
            self.properties._remove_nodal_property("damping_nodal_links", node_ids)

        self.reset_nodes_input_fields()
        self.reset_stiffness_input_fields()
        self.reset_dampings_input_fields()
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Structural links resetting"
        message = "Would you like to remove all structural links from the structural model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        if self.checkBox_remove_link_stiffness.isChecked():
            self.properties._reset_nodal_property("stiffness_nodal_links")

        if self.checkBox_remove_link_damping.isChecked():
            self.properties._reset_nodal_property("damping_nodal_links")

        self.reset_nodes_input_fields()
        self.reset_stiffness_input_fields()
        self.reset_dampings_input_fields()
        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize(False)

    def load_elastic_links_stiffness_info(self):

        self.treeWidget_stiffness_nodal_links.clear()
        stiffness_labels = np.array(["k_x", "k_y", "k_z", "k_rx", "k_ry", "k_rz"])

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "stiffness_nodal_links":
                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, stiffness_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_stiffness_nodal_links.addTopLevelItem(item)

    def load_elastic_links_damping_info(self):

        self.treeWidget_damping_nodal_links.clear()
        damping_labels = np.array(["c_x", "c_y", "c_z", "c_rx", "c_ry", "c_rz"])

        for (_property, *args), data in self.properties.nodal_properties.items():
            if _property == "damping_nodal_links":
                key = f"{args[0]}-{args[1]}"

                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [key, str(self.text_label(k_mask, damping_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_damping_nodal_links.addTopLevelItem(item)

    def load_nodes_info(self):
        self.load_elastic_links_stiffness_info()
        self.load_elastic_links_damping_info()
        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        properties = [
            "stiffness_nodal_links", 
            "damping_nodal_links",
            ]

        check_boxes = [
            self.checkBox_remove_link_stiffness,
            self.checkBox_remove_link_damping,
        ]

        self.pushButton_remove.setDisabled(True)
        self.checkBox_remove_link_stiffness.setChecked(False)
        self.checkBox_remove_link_damping.setChecked(False)

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        self.tabWidget_remove.setTabVisible(TabList.STIFFNESS_LINK, False)
        self.tabWidget_remove.setTabVisible(TabList.DAMPINGS_LINK, False)

        for _property, *args in self.properties.nodal_properties.keys():
            if _property in properties:
                index = properties.index(_property)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                self.tabWidget_remove.setTabVisible(index + 1, True)
                self.checkBox_remove_link_stiffness.setChecked(True)
                check_boxes[index].setChecked(True)

        if not self.tabWidget_main.isVisible():
            self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
            self.tabWidget_constant_values.setCurrentIndex(NodalLinkType.STIFFNESS)
            self.lineEdit_Kx.setFocus()

        for check_box in check_boxes:
            is_checked = check_box.isChecked()
            check_box.setEnabled(is_checked)

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == TabIndex.LIST:
            self.selection_frame.setDisabled(True)

        else:
            self.selection_frame.setDisabled(False)

        self.cache_tab = self.tabWidget_main.currentIndex()

    def on_click_item_stiffness(self, item: QTreeWidgetItem):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property(
            "stiffness_nodal_links", node_ids=node_ids
        )
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            self.pushButton_remove.setDisabled(False)

    def on_click_item_damping(self, item: QTreeWidgetItem):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property(
            "damping_nodal_links", node_ids=node_ids
        )
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            self.pushButton_remove.setDisabled(False)

    def on_double_click_item_stiffness(self, item):
        self.on_click_item_stiffness(item)

    def on_double_click_item_damping(self, item):
        self.on_click_item_damping(item)

    def reset_nodes_input_fields(self):
        self.lineEdit_first_node_id.clear()
        self.lineEdit_last_node_id.clear()

    def reset_stiffness_input_fields(self):
        for lineEdit in self.lineEdits_constant_values_stiffness:
            lineEdit.clear()
        for lineEdit in self.lineEdits_table_values_stiffness:
            lineEdit.clear()

    def reset_dampings_input_fields(self):
        for lineEdit in self.lineEdits_constant_values_dampings:
            lineEdit.clear()
        for lineEdit in self.lineEdits_table_values_dampings:
            lineEdit.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()
