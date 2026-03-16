import numpy as np

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.elastic_nodal_links_input_ui import (
    ElasticNodalLinksInput_UI,
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


class ElasticNodalLinksInput(StructuralNodesInput, ElasticNodalLinksInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_widgets()
        self._initialize()
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

    def reset_table_variables(self):

        self.Kx_table_path = None
        self.Ky_table_path = None
        self.Kz_table_path = None
        self.Krx_table_path = None
        self.Kry_table_path = None
        self.Krz_table_path = None

        self.Cx_table_path = None
        self.Cy_table_path = None
        self.Cz_table_path = None
        self.Crx_table_path = None
        self.Cry_table_path = None
        self.Crz_table_path = None

        self.imported_kx_values = None
        self.imported_ky_values = None
        self.imported_kz_values = None
        self.imported_krx_values = None
        self.imported_kry_values = None
        self.imported_krz_values = None

        self.imported_cx_values = None
        self.imported_cy_values = None
        self.imported_cz_values = None
        self.imported_crx_values = None
        self.imported_cry_values = None
        self.imported_crz_values = None

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

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        for i, width in enumerate([120, 200]):
            self.treeWidget_stiffness_nodal_links.setColumnWidth(i, width)
            self.treeWidget_damping_nodal_links.setColumnWidth(i, width)
            self.treeWidget_stiffness_nodal_links.headerItem().setTextAlignment(
                i, Qt.AlignCenter
            )
            self.treeWidget_damping_nodal_links.headerItem().setTextAlignment(
                i, Qt.AlignCenter
            )

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
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(ss_link_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_stiffness[i]
                                lineEdit.setText(table_path)

                    else:
                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(0)
                        for i, value in enumerate(ss_link_data["real_values"]):
                            if value is not None:
                                lineEdit = self.lineEdits_constant_values_stiffness[i]
                                lineEdit.setText(f"{value: .3e}")

                sd_link_data = self.properties._get_property(
                    "damping_nodal_links", node_ids=sorted_nodes
                )
                if isinstance(sd_link_data, dict):
                    if "table_paths" in sd_link_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(1)
                        for i, table_path in enumerate(sd_link_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.lineEdits_table_values_dampings[i]
                                lineEdit.setText(table_path)

                    else:
                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(1)
                        for i, value in sd_link_data["real_values"]:
                            if value is not None:
                                lineEdit = self.lineEdits_constant_values_dampings[i]
                                lineEdit.setText(f"{value: .3e}")

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)

        else:
            self.selection_frame.setDisabled(False)

        self.cache_tab = self.tabWidget_main.currentIndex()

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

    def check_constant_stiffness_links(self, node_ids: list):

        stop, Kx = self.check_entries(self.lineEdit_Kx, "Kx")
        if stop:
            return True

        stop, Ky = self.check_entries(self.lineEdit_Ky, "Ky")
        if stop:
            return True

        stop, Kz = self.check_entries(self.lineEdit_Kz, "Kz")
        if stop:
            return True

        stop, Krx = self.check_entries(self.lineEdit_Krx, "Krx")
        if stop:
            return True

        stop, Kry = self.check_entries(self.lineEdit_Kry, "Kry")
        if stop:
            return True

        stop, Krz = self.check_entries(self.lineEdit_Krz, "Krz")
        if stop:
            return True

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

    def check_constant_dampings_links(self, node_ids: list):

        stop, Cx = self.check_entries(self.lineEdit_Cx, "Cx")
        if stop:
            return True
        stop, Cy = self.check_entries(self.lineEdit_Cy, "Cy")
        if stop:
            return True
        stop, Cz = self.check_entries(self.lineEdit_Cz, "Cz")
        if stop:
            return True
        stop, Crx = self.check_entries(self.lineEdit_Crx, "Crx")
        if stop:
            return True
        stop, Cry = self.check_entries(self.lineEdit_Cry, "Cry")
        if stop:
            return True
        stop, Crz = self.check_entries(self.lineEdit_Crz, "Crz")
        if stop:
            return True

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

    def attribute_callback(self):

        stop, node_ids = self.check_linked_nodes()
        if stop:
            return True

        self.remove_properties_from_node(node_ids)

        if self.tabWidget_inputs.currentIndex() == 0:
            self.check_constant_stiffness_links(node_ids)
            self.check_constant_dampings_links(node_ids)

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.check_tables_for_stiffness_links(node_ids)
            self.check_tables_for_dampings_links(node_ids)

        if not self.link_applied:
            title = "No inputs entered for the structural stiffness or damping links"
            message = "Define at least one value or table of values to the stiffness "
            message += (
                "or damping links to proceed with the structural link attribution."
            )
            PrintMessageInput([error_title, title, message])
            return

        self.reset_nodes_input_fields()
        self.actions_to_finalize()
    
    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "nodal link")

    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

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

        # real values vector
        real_values = imported_values[:, 1]

        # imaginary values vector
        imag_values = imported_values[:, 2]

        # array to be saved
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False

    def check_tables_for_stiffness_links(self, node_ids_pair: list):

        table_paths = list()

        for label in self.stiffness_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label.lower()}_values"
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
            imported_values_name = f"imported_{label.lower()}_values"
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

    def check_tables_for_dampings_links(self, node_ids_pair: list):

        table_paths = list()

        for label in self.damping_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label.lower()}_values"
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
            imported_values_name = f"imported_{label.lower()}_values"
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

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize()

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

        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)

        self.checkBox_link_stiffness.setChecked(True)
        self.checkBox_link_dampings.setChecked(True)

        for _property, *args in self.properties.nodal_properties.keys():
            if _property == "stiffness_nodal_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(0, True)
                self.checkBox_link_stiffness.setChecked(True)
                break

        for _property, *args in self.properties.nodal_properties.keys():
            if _property == "damping_nodal_links":
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_remove.setTabVisible(1, True)
                self.checkBox_link_dampings.setChecked(True)
                break

    def on_click_item_stiffness(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property(
            "stiffness_nodal_links", node_ids=node_ids
        )
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            # self.lineEdit_first_node_id.setText(str(node_ids[0]))
            # self.lineEdit_last_node_id.setText(str(node_ids[1]))
            self.pushButton_remove.setDisabled(False)

    def on_click_item_damping(self, item):
        key = item.text(0)
        node_ids = [int(value) for value in key.split("-")]
        link_data = self.properties._get_property(
            "damping_nodal_links", node_ids=node_ids
        )
        if isinstance(link_data, dict):
            app().main_window.set_selection(nodes=node_ids)
            # self.lineEdit_first_node_id.setText(str(node_ids[0]))
            # self.lineEdit_last_node_id.setText(str(node_ids[1]))
            self.pushButton_remove.setDisabled(False)

    def on_double_click_item_stiffness(self, item):
        self.on_click_item_stiffness(item)

    def on_double_click_item_damping(self, item):
        self.on_click_item_damping(item)

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

        if self.checkBox_link_stiffness.isChecked():
            self.properties._remove_nodal_property("stiffness_nodal_links", node_ids)

        if self.checkBox_link_dampings.isChecked():
            self.properties._remove_nodal_property("damping_nodal_links", node_ids)

        self.reset_nodes_input_fields()
        self.reset_stiffness_input_fields()
        self.reset_dampings_input_fields()
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of structural links"
        message = (
            "Would you like to remove all structural links from the structural model?"
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

        if self.checkBox_link_stiffness.isChecked():
            self.properties._reset_nodal_property("stiffness_nodal_links")

        if self.checkBox_link_dampings.isChecked():
            self.properties._reset_nodal_property("damping_nodal_links")

        self.reset_nodes_input_fields()
        self.reset_stiffness_input_fields()
        self.reset_dampings_input_fields()
        self.actions_to_finalize()

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
