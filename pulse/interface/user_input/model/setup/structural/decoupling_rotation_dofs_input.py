from PyQt5.QtWidgets import QComboBox, QDialog, QCheckBox, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
#from pulse.interface.formatters.icons import *
from pulse.interface.formatters.icons import get_openpulse_icon 
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import get_list_bool_from_string


import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class DecouplingRotationDOFsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/decoupling_rotation_dofs_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.project = app().project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_decoupling_info()
        self.update()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.node_id = app().main_window.list_selected_nodes()
        self.line_id = app().main_window.list_selected_lines()
        self.element_id = app().main_window.list_selected_elements()

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks() 

        self.nodes = self.preprocessor.nodes
        self.structural_elements = self.preprocessor.structural_elements
        self.lines_from_model = self.preprocessor.lines_from_model

        self.stop = False
        self.complete = False

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_rotation_x : QCheckBox
        self.checkBox_rotation_y : QCheckBox
        self.checkBox_rotation_z : QCheckBox
        # QComboBox
        self.comboBox_node_to_uncouple_dofs : QComboBox
        # QLineEdit
        self.lineEdit_decoupled_DOFs : QLineEdit
        self.lineEdit_element_IDs : QLineEdit
        self.lineEdit_first_node : QLineEdit
        self.lineEdit_last_node : QLineEdit
        self.lineEdit_node_IDs : QLineEdit
        self.lineEdit_selected_element : QLineEdit
        # QTabWidget
        self.tabWidget_main : QTabWidget
        # QTreeWidget
        self.treeWidget_B2PX_rotation_decoupling : QTreeWidget
        # QPushButton       
        self.pushButton_confirm : QPushButton
        self.pushButton_remove_group : QPushButton
        self.pushButton_reset : QPushButton

    def _create_connections(self):
        #
        self.pushButton_confirm.clicked.connect(self.check_dofs_coupling)
        self.pushButton_reset.clicked.connect(self.check_reset_all)
        self.pushButton_remove_group.clicked.connect(self.remove_group)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_B2PX_rotation_decoupling.itemClicked.connect(self.on_click_item)
        self.treeWidget_B2PX_rotation_decoupling.itemDoubleClicked.connect(self.on_double_click_item)

    def _config_widgets(self):
        self.lineEdit_decoupled_DOFs.setDisabled(True)
        self.lineEdit_element_IDs.setDisabled(True)
        self.lineEdit_node_IDs.setDisabled(True)
        for i, width in enumerate([120, 140, 110]):
            self.treeWidget_B2PX_rotation_decoupling.setColumnWidth(i, width)
            self.treeWidget_B2PX_rotation_decoupling.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def tab_event_callback(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.clear_texts()
            self.pushButton_remove_group.setDisabled(True)  

    def clear_texts(self):
        self.lineEdit_decoupled_DOFs.setText("")
        self.lineEdit_element_IDs.setText("")
        self.lineEdit_node_IDs.setText("")

    def update_texts(self, element_id):
        self.first_node = self.structural_elements[element_id].first_node.external_index
        self.last_node  = self.structural_elements[element_id].last_node.external_index
        self.lineEdit_first_node.setText(str(self.first_node))
        self.lineEdit_last_node.setText(str(self.last_node))
        self.lineEdit_selected_element.setText(str(element_id))

    def on_click_item(self, item):
        self.lineEdit_decoupled_DOFs.setText(item.text(0))
        self.lineEdit_element_IDs.setText(item.text(1))
        self.lineEdit_node_IDs.setText(item.text(2))
        self.pushButton_remove_group.setDisabled(False)

    def on_double_click_item(self, item):
        self.on_click_item(item)
        self.get_information(item)

    def remove_group(self):

        decoupled_dof_labels = self.lineEdit_decoupled_DOFs.text()
        key = self.dict_decoupled_DOFs_label_to_bool[decoupled_dof_labels]
        _, _, section = self.preprocessor.dict_B2PX_rotation_decoupling[key]
        self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.pop(key)
        self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling.pop(key)
        self.preprocessor.dict_B2PX_rotation_decoupling.pop(key)

        self.project.file.modify_B2PX_rotation_decoupling_in_file(section = section, 
                                                                  remove = True)
        self.load_decoupling_info()
        self.clear_texts()

        title = "Removing process complete"
        message = f"The selected rotation decoupling has been removed."
        PrintMessageInput([window_title_2, title, message], auto_close = True)

    def check_reset_all(self):

        self.project.reset_B2PX_rotation_decoupling()
        self.load_decoupling_info()
        self.clear_texts()

        title = "Resetting process complete"
        message = "The rotation decoupling applied to all dofs has been reseted." 
        PrintMessageInput([window_title_2, title, message], auto_close = True)

    def get_rotation_mask(self):

        rotations_mask = [  self.checkBox_rotation_x.isChecked(), 
                            self.checkBox_rotation_y.isChecked(), 
                            self.checkBox_rotation_z.isChecked()  ]

        if np.sum(rotations_mask) == 0:
            title = "Invalid decoupling setup"
            message = "There are no rotation DOFs decoupling in the current setup. "
            message += "You should tick at least one rotation DOF before continue."
            PrintMessageInput([window_title_1, title, message])
            return None

        else:
            return rotations_mask

    def check_get_nodes(self):

        lineEdit = self.lineEdit_selected_element.text()
        self.stop, self.element_typed = self.before_run.check_input_ElementID(lineEdit, 
                                                                              single_ID = True)
        if self.stop:
            return True

        self.element_id = self.element_typed
        self.update_texts(self.element_id)
        return False

    def check_dofs_coupling(self):

        if self.check_get_nodes():
            return

        index = self.comboBox_node_to_uncouple_dofs.currentIndex()
        if index == 0:
            self.selected_node_id = self.first_node
        elif index == 1:
            self.selected_node_id = self.last_node

        neighboor_elements = self.preprocessor.neighboor_elements_of_node(self.selected_node_id)
        if len(neighboor_elements) < 3:
            title = "Incorrect Node ID selection"
            message = "The decoupling of rotation dofs can only be applied to the T connections." 
            PrintMessageInput([window_title_1, title, message])
            return
        
        rotations_mask = self.get_rotation_mask()
        if len(rotations_mask):
            if self.structural_elements[self.element_id].element_type in ['beam_1']:

                self.project.set_B2PX_rotation_decoupling(  self.element_id, 
                                                            self.selected_node_id, 
                                                            rotations_mask  )

                print("[Set Rotation Decoupling] - defined at element {} and at node {}".format(self.element_id, self.selected_node_id))
                self.complete = True
                self.close()

            else:

                element_type = self.structural_elements[self.element_id]

                title = "Invalid decoupling setup"
                message = f"The selected element have a '{element_type}' formulation, you should "
                message += "have a 'beam_1' element type in selection to decouple the rotation dofs. "
                message += " Try to choose another element or change the element type formulation."
                PrintMessageInput([window_title_1, title, message])
                return

    def text_label(self, mask):
        text = ""
        load_labels = np.array(['Rx','Ry','Rz'])
        temp = load_labels[mask]
        if list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_decoupling_info(self):

        self.treeWidget_B2PX_rotation_decoupling.clear()
        self.dict_decoupled_DOFs_label_to_bool = dict()
        self.dict_decoupled_DOFs_bool_to_label = dict()

        for key, elements in self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.items():

            nodes = self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling[key]
            decoupling_dofs_mask = get_list_bool_from_string(key)
            label_decoupled_DOFs = self.text_label(decoupling_dofs_mask)

            new = QTreeWidgetItem([label_decoupled_DOFs, str(elements), str(nodes)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            new.setTextAlignment(2, Qt.AlignCenter)
            self.treeWidget_B2PX_rotation_decoupling.addTopLevelItem(new)
            self.dict_decoupled_DOFs_label_to_bool[label_decoupled_DOFs] = key
            self.dict_decoupled_DOFs_bool_to_label[key] = label_decoupled_DOFs

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.dict_elements_with_B2PX_rotation_decoupling) == 0:
            self.tabWidget_main.setCurrentIndex(0)
            self.tabWidget_main.setTabVisible(1, False)
        else:
            self.tabWidget_main.setTabVisible(1, True)

    def get_information(self, item):
        try:
            if self.lineEdit_decoupled_DOFs.text() != "":

                decoupled_DOFs_bool = self.dict_decoupled_DOFs_label_to_bool[item.text(0)]  
                decoupled_DOFs_labels =  self.dict_decoupled_DOFs_bool_to_label[decoupled_DOFs_bool]     

                data = dict()                
                for key, elements in self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.items():
                    nodes = self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling[key]
                    for element in elements:
                        for node in nodes: 
                            data[(element, node)] = decoupled_DOFs_labels

                if len(data):
                    self.close()
                    header_labels = ["Element ID", "Node ID", "Decoupled DOFs"]
                    GetInformationOfGroup(  group_label = "Decoupling rotation DOFs",
                                            selection_label = "Element ID:",
                                            header_labels = header_labels,
                                            column_widths = [100, 100, 150],
                                            data = data  )

                # if read.lines_removed:
                #     self.load_decoupling_info()
                #     self.clear_texts()

            else:
                title = "Invalid selection"
                message = "Please, select a group in the list to get the information."
                PrintMessageInput([window_title_2, title, message])
                
        except Exception as error_log:
            title = "Error while getting information of selected group"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
        self.show()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_element.setText(text)

    def update(self):
        if len(app().main_window.list_selected_elements()):
            self.element_id, *_ = app().main_window.list_selected_elements()
            for key, elements in self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.items():
                if self.element_id in elements:
                    decoupling_dofs_mask = get_list_bool_from_string(key)
                    self.checkBox_rotation_x.setChecked(decoupling_dofs_mask[0])
                    self.checkBox_rotation_y.setChecked(decoupling_dofs_mask[1])
                    self.checkBox_rotation_z.setChecked(decoupling_dofs_mask[2])

            self.update_texts(self.element_id)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_get_nodes()
        if event.key() == Qt.Key_Escape:
            self.close()