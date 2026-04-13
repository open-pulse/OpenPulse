from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.b2p_decoupling_rotation_dofs_input_ui import (
    B2pDecouplingRotationDofsInput_UI,
)
from pulse.interface.user_input.model.setup.elements_input import ElementsInput
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.structural_element import decoupling_matrix


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


error_title = "Error"


class DecouplingRotationDOFsInput(ElementsInput, B2pDecouplingRotationDofsInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._create_connections()
        self._config_widgets()
        self.load_decoupling_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_elements_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_elements_info.itemDoubleClicked.connect(
            self.on_double_click_item
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()
        if not selected_elements:
            return

        if len(selected_elements) != 1:
            return
    
        for (
            property,
            element_id,
        ), data in self.properties.element_properties.items():
            if (
                property == "B2P_rotation_decoupling"
                and element_id == selected_elements[0]
            ):
                self.lineEdit_element_id.setText(str(element_id))

                coords = np.array(data["coords"], dtype=float)
                node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                if isinstance(node_id, int):
                    self.lineEdit_tjoint_node_id.setText(str(node_id))

                decoupled_dofs = data["decoupled_rotations"]
                self.checkBox_rotation_x.setChecked(decoupled_dofs[0])
                self.checkBox_rotation_y.setChecked(decoupled_dofs[1])
                self.checkBox_rotation_z.setChecked(decoupled_dofs[2])
                return

        element_id = selected_elements[0]
        self.lineEdit_element_id.setText(str(element_id))
        element = self.preprocessor.structural_elements[element_id]

        if element.element_type != "beam_1":
            self.reset_line_edits()
            return
    
        node_ids = [
            element.first_node.external_index,
            element.last_node.external_index,
        ]

        for node_id in node_ids:
            neighboor_elements = (
                self.preprocessor.structural_elements_connected_to_node[
                    node_id
                ]
            )
            if len(neighboor_elements) >= 3:
                self.lineEdit_tjoint_node_id.setText(str(node_id))
                return
            self.lineEdit_tjoint_node_id.clear()

    def _config_widgets(self):
        for i, width in enumerate([100, 100, 100]):
            self.treeWidget_elements_info.setColumnWidth(i, width)
            self.treeWidget_elements_info.headerItem().setTextAlignment(
                i, Qt.AlignCenter
            )

    def tab_event_callback(self):
        self.reset_line_edits()
        self.pushButton_remove.setDisabled(True)
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.pushButton_attribute.setDisabled(tab_list)
        if not tab_list:
            self.treeWidget_elements_info.clearSelection()

    def on_click_item(self, item: QTreeWidgetItem):
        element_id = int(item.text(0))
        self.lineEdit_element_id.setText(str(element_id))
        app().main_window.set_selection(elements=[element_id])
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def attribute_callback(self):

        if (
            self.lineEdit_element_id.text() == ""
            and app().main_window.list_selected_elements()
        ):
            self.hide()
            title = "Invalid element selected"
            message = "To proceed, selecting a beam element connected to the pipe is necessary."
            PrintMessageInput([error_title, title, message])
            return

        lineEdit = self.lineEdit_element_id.text()
        stop, element_id = self.before_run.check_selected_ids(
            lineEdit, "elements", single_id=True
        )
        if stop:
            return

        element = self.preprocessor.structural_elements[element_id]

        tjoint_node_id = None
        node_ids = [element.first_node.external_index, element.last_node.external_index]

        for node_id in node_ids:
            neighboor_elements = (
                self.preprocessor.structural_elements_connected_to_node[node_id]
            )
            if len(neighboor_elements) >= 3:
                tjoint_node_id = node_id
                break

        if tjoint_node_id is None:
            self.hide()
            title = "Invalid element selected"
            message = "The beam-to-pipe decoupling of rotation dofs can only "
            message += "be applied to the T connections."
            PrintMessageInput([error_title, title, message])
            return

        element_type = element.element_type
        rotations_mask = self.get_rotation_mask()

        if not any(rotations_mask):
            return

        if element_type != "beam_1":
            return

        node = app().project.model.preprocessor.nodes[node_id]
        coords = list(np.round(node.coordinates, 5))

        data = {
            "coords": coords, 
            "decoupled_rotations": rotations_mask,
            }

        self.preprocessor.set_B2P_rotation_decoupling(element_id, data)
        self.properties._set_element_property(
            "B2P_rotation_decoupling", data, element_ids=element_id
        )

        self.actions_to_finalize()
        self.complete = True

        return

    def remove_callback(self):

        selected_items = self.treeWidget_elements_info.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            
            if item.text(0) == "":
                continue

            element_id = int(item.text(0))
            element = self.preprocessor.structural_elements[element_id]
            element.decoupling_matrix = decoupling_matrix
            element.decoupling_info = None

            self.properties._remove_element_property(
                "B2P_rotation_decoupling", element_id
            )

        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Beam-to-pipe (B2P) decoupling rotations resetting"
        message = "Would you like to remove all B2P decoupling rotations from the structural model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return
            
        element_ids = list()
        for (property, element_id) in self.properties.element_properties.keys():
            if property == "B2P_rotation_decoupling":
                element_ids.append(element_id)

        for element_id in element_ids:
            element = self.preprocessor.structural_elements[element_id]
            element.decoupling_matrix = decoupling_matrix
            element.decoupling_info = None

            self.properties._remove_element_property("B2P_rotation_decoupling", element_id)

        self.actions_to_finalize()

    def reset_line_edits(self):
        self.lineEdit_element_id.clear()
        self.lineEdit_tjoint_node_id.clear()

    def actions_to_finalize(self):
        app().main_window.set_selection()
        app().project.file.write_element_properties_in_file()
        self.load_decoupling_info()
        self.reset_line_edits()

    def get_rotation_mask(self):

        rotations_mask = [
            self.checkBox_rotation_x.isChecked(),
            self.checkBox_rotation_y.isChecked(),
            self.checkBox_rotation_z.isChecked(),
        ]

        if not any(rotations_mask):
            self.hide()
            title = "Invalid decoupling setup"
            message = "There are no rotation DOFs decoupling in the current setup. "
            message += "You should tick at least one rotation DOF before continue."
            PrintMessageInput([error_title, title, message])

        return rotations_mask

    def text_label(self, mask: list[bool, bool, bool]):

        text = ""
        load_labels = np.array(["Rx", "Ry", "Rz"])
        labels = load_labels[mask]

        if list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(*labels)

        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(*labels)

        elif list(mask).count(True) == 1:
            text = "[{}]".format(*labels)

        return text

    def load_decoupling_info(self):

        self.treeWidget_elements_info.clear()
        for (property, element_id), data in self.properties.element_properties.items():
            if property != "B2P_rotation_decoupling":
                continue

            coords = np.array(data["coords"], dtype=float)
            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            if not isinstance(node_id, int):
                continue

            decoupled_dofs = data["decoupled_rotations"]
            decoupled_dofs_labels = self.text_label(decoupled_dofs)

            item = QTreeWidgetItem(
                [str(element_id), str(node_id), decoupled_dofs_labels]
            )

            for i in range(4):
                item.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_elements_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.reset_line_edits()
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for property, _ in self.properties.element_properties.keys():
            if property == "B2P_rotation_decoupling":
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

        self.lineEdit_element_id.setFocus()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        if event.key() == Qt.Key_Delete:
            self.remove_callback()

        if event.key() == Qt.Key_Escape:
            self.close()