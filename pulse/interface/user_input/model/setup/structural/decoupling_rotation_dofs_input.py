# fmt: off

from PyQt5.QtWidgets import QDialog, QCheckBox, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse.model.structural_element import decoupling_matrix

import numpy as np


window_title_1 = "Error"
window_title_2 = "Warning"

class DecouplingRotationDOFsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/b2p_decoupling_rotation_dofs_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_decoupling_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True
        self.complete = False

        self.before_run = app().project.get_pre_solution_model_checks() 

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_rotation_x: QCheckBox
        self.checkBox_rotation_y: QCheckBox
        self.checkBox_rotation_z: QCheckBox

        # QLineEdit
        self.lineEdit_selected_id_to_remove: QLineEdit
        self.lineEdit_element_id: QLineEdit
        self.lineEdit_tjoint_node_id: QLineEdit

        # QPushButton       
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_elements_info: QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_elements_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_elements_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()

        if selected_elements:
            if len(selected_elements) == 1:

                for (property, element_id), data in self.properties.element_properties.items():
                    if property == "B2P_rotation_decoupling" and element_id == selected_elements[0]:
                        
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

                if element.element_type == "beam_1":
                    node_ids = [element.first_node.external_index, element.last_node.external_index]
                    for node_id in node_ids:
                        neighboor_elements = self.preprocessor.neighboor_elements_of_node(node_id)
                        if len(neighboor_elements) == 3:
                            self.lineEdit_tjoint_node_id.setText(str(node_id))
                            return
                        self.lineEdit_tjoint_node_id.setText("")

                else:
                    self.lineEdit_element_id.setText("")
                    self.lineEdit_tjoint_node_id.setText("")

    def _config_widgets(self):
        for i, width in enumerate([100, 100, 100]):
            self.treeWidget_elements_info.setColumnWidth(i, width)
            self.treeWidget_elements_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        self.lineEdit_selected_id_to_remove.setText("")
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.pushButton_remove.setDisabled(True)

    def on_click_item(self, item):
        element_id = int(item.text(0))
        self.lineEdit_selected_id_to_remove.setText(str(element_id))
        app().main_window.set_selection(elements = [element_id])
        self.pushButton_remove.setDisabled(False)

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def attribute_callback(self):

        if self.lineEdit_element_id.text() == "" and app().main_window.list_selected_elements():
            self.hide()
            title = "Invalid element selected"
            message = f"To proceed, selecting a beam element connected to the pipe is necessary."
            PrintMessageInput([window_title_1, title, message])
            return

        lineEdit = self.lineEdit_element_id.text()
        stop, element_id = self.before_run.check_selected_ids(lineEdit, "elements", single_id = True)
        if stop:
            return

        element = self.preprocessor.structural_elements[element_id]
        
        tjoint_node_id = None
        node_ids = [element.first_node.external_index, element.last_node.external_index]
        for node_id in node_ids:
            neighboor_elements = self.preprocessor.neighboor_elements_of_node(node_id)
            if len(neighboor_elements) == 3:
                tjoint_node_id = node_id
                break

        if tjoint_node_id is None:
            self.hide()
            title = "Invalid element selected"
            message = "The beam-to-pipe decoupling of rotation dofs can only " 
            message += "be applied to the T connections."
            PrintMessageInput([window_title_1, title, message])
            return

        element_type = element.element_type
        rotations_mask = self.get_rotation_mask()

        if len(rotations_mask):
            if element_type == 'beam_1':

                node = app().project.model.preprocessor.nodes[node_id]
                coords = list(np.round(node.coordinates, 5))

                data = {
                        "coords" : coords,
                        "decoupled_rotations" : rotations_mask
                        }

                self.preprocessor.set_B2P_rotation_decoupling(element_id, data)
                self.properties._set_element_property("B2P_rotation_decoupling", data, element_ids=element_id)

                app().pulse_file.write_element_properties_in_file()
                self.load_decoupling_info()
                app().main_window.set_selection()
                self.lineEdit_element_id.setText("")
                self.lineEdit_tjoint_node_id.setText("")

                print("[Set B2P Rotation Decoupling] - defined at element {} and at node {}".format(element_id, node_id))
                self.complete = True
                return

    def remove_callback(self):

        if self.lineEdit_selected_id_to_remove.text() != "":

            element_id = int(self.lineEdit_selected_id_to_remove.text())
            element = self.preprocessor.structural_elements[element_id]
            element.decoupling_matrix = decoupling_matrix
            element.decoupling_info = None

            self.properties._remove_element_property("B2P_rotation_decoupling", element_id)

            app().pulse_file.write_element_properties_in_file()
            self.load_decoupling_info()

    def reset_callback(self):

        self.hide()

        title = "Resetting of B2P decoupling rotations"
        message = "Would you like to remove all B2P decoupling rotations from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            
            element_ids = list()
            for (property, element_id) in self.properties.element_properties.keys():
                print(property, property == "B2P_rotation_decoupling")
                if property == "B2P_rotation_decoupling":
                    element_ids.append(element_id)

            for element_id in element_ids:
                element = self.preprocessor.structural_elements[element_id]
                element.decoupling_matrix = decoupling_matrix
                element.decoupling_info = None

                self.properties._remove_element_property("B2P_rotation_decoupling", element_id)

            app().pulse_file.write_element_properties_in_file()
            self.load_decoupling_info()

    def get_rotation_mask(self):

        rotations_mask = [  self.checkBox_rotation_x.isChecked(), 
                            self.checkBox_rotation_y.isChecked(), 
                            self.checkBox_rotation_z.isChecked()  ]

        if np.sum(rotations_mask) == 0:
            self.hide()
            title = "Invalid decoupling setup"
            message = "There are no rotation DOFs decoupling in the current setup. "
            message += "You should tick at least one rotation DOF before continue."
            PrintMessageInput([window_title_1, title, message])
            return None

        else:
            return rotations_mask

    def text_label(self, mask):
        text = ""
        load_labels = np.array(['Rx','Ry','Rz'])
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
            if property == "B2P_rotation_decoupling":

                coords = np.array(data["coords"], dtype=float)
                node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                if isinstance(node_id, int):

                    decoupled_dofs = data["decoupled_rotations"]
                    decoupled_dofs_labels = self.text_label(decoupled_dofs)

                    item = QTreeWidgetItem([str(element_id),
                                            str(node_id), 
                                            decoupled_dofs_labels])

                    for i in range(4):
                        item.setTextAlignment(i, Qt.AlignCenter)
                    
                    self.treeWidget_elements_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.lineEdit_selected_id_to_remove.setText("")
        self.tabWidget_main.setTabVisible(1, False)
        for (property, _) in self.properties.element_properties.keys():
            if property == "B2P_rotation_decoupling":
                self.tabWidget_main.setTabVisible(1, True)
                return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on