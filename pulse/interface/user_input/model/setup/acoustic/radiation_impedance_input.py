from PyQt5.QtWidgets import QComboBox, QDialog, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.tools.utils import remove_bc_from_file

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class RadiationImpedanceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/radiation_impedance_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().main_window.project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.update()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.keep_window_open = True

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.acoustic_bc_info_path = self.project.file._node_acoustic_path

        self.nodes = self.preprocessor.nodes
        self.radiation_impedance = None
        self.nodes_typed = []
  
        self.remove_acoustic_pressure = False

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_radiation_impedance_type : QComboBox

        # QLineEdit
        self.lineEdit_imag_value : QLineEdit
        self.lineEdit_real_value : QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_table_path : QLineEdit

        # QPushButton
        self.confirm_radiation_impedance_button : QPushButton
        self.remove_button : QPushButton
        self.reset_button : QPushButton
        self.search_button : QPushButton
        self.table_values_confirm_button : QPushButton

        # QTabWidget
        self.tabWidget_radiation_impedance : QTabWidget

        # QTreeWidget
        self.treeWidget_radiation_impedance : QTreeWidget
        self.treeWidget_radiation_impedance.setColumnWidth(1, 20)
        self.treeWidget_radiation_impedance.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.confirm_radiation_impedance_button.clicked.connect(self.check_radiation_impedance_type)
        self.remove_button.clicked.connect(self.remove_bc_from_node)
        self.reset_button.clicked.connect(self.check_reset)
        #
        self.tabWidget_radiation_impedance.currentChanged.connect(self.tabEvent_radiation_impedance)
        #
        self.treeWidget_radiation_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_radiation_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)

    def tabEvent_radiation_impedance(self):
        self.remove_button.setDisabled(True)
        if self.tabWidget_radiation_impedance.currentIndex() == 1:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.update()

    def check_radiation_impedance_type(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_selection_id)
        if self.stop:
            return

        try:

            index = self.comboBox_radiation_impedance_type.currentIndex()
            if index == 0:
                type_id = 0

            elif index == 1:
                type_id = 1

            elif index == 2:
                type_id = 2

            self.radiation_impedance = type_id
            self.project.set_radiation_impedance_bc_by_node(self.nodes_typed, type_id)
            
            self.opv.updateRendererMesh()
            self.close()
            print(f"[Set Radiation Impedance] - defined at node(s) {self.nodes_typed}")
        except:
            return

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item):
        self.remove_button.setDisabled(False)
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_bc_from_node()

    def remove_bc_from_node(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_selection_id)
        if self.stop:
            return

        key_strings = ["radiation impedance"]
        # message = "The radiation impedance attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        self.project.file.filter_bc_data_from_dat_file(self.nodes_typed, key_strings, self.acoustic_bc_info_path)
        self.preprocessor.set_radiation_impedance_bc_by_node(self.nodes_typed, None)

        self.lineEdit_selection_id.setText("")
        self.remove_button.setDisabled(True)
        self.load_nodes_info()
        self.opv.updateRendererMesh()
        # self.close()

    def check_reset(self):
        if self.preprocessor.nodes_with_radiation_impedance:

            list_nodes = list()
            for node in self.preprocessor.nodes_with_radiation_impedance:
                list_nodes.append(node.external_index)

            self.hide()
            
            title = f"Removal of radiation impedances"
            message = "Would you like to remove all radiation impedances from the acoustic model?"

            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)
            
            if read._cancel:
                return

            if read._continue:

                _node_ids = list()
                _nodes_with_radiation_impedance = self.preprocessor.nodes_with_radiation_impedance.copy()

                for node in _nodes_with_radiation_impedance:
                    node_id = node.external_index
                    key_strings = ["radiation impedance"]
                    if node_id not in _node_ids:
                        _node_ids.append(node_id)

                self.project.file.filter_bc_data_from_dat_file(_node_ids, key_strings, self.acoustic_bc_info_path)
                self.preprocessor.set_radiation_impedance_bc_by_node(_node_ids, None)

                self.close()
                self.opv.updateRendererMesh()

    def load_nodes_info(self):
        self.treeWidget_radiation_impedance.clear()
        for node in self.preprocessor.nodes_with_radiation_impedance:
            if node.radiation_impedance_type == 0:
                text = "Anechoic"

            elif node.radiation_impedance_type == 1:
                text = "Unflanged"

            elif node.radiation_impedance_type == 2:
                text = "Flanged"

            new = QTreeWidgetItem([str(node.external_index), text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_radiation_impedance.addTopLevelItem(new)
        self.update_tabs_visibility()

    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.radiation_impedance_type == 0:
                self.comboBox_radiation_impedance_type.setCurrentIndex(0)
            if node.radiation_impedance_type == 1:
                self.comboBox_radiation_impedance_type.setCurrentIndex(1)
            if node.radiation_impedance_type == 2:
                self.comboBox_radiation_impedance_type.setCurrentIndex(2) 
        self.writeNodes(list_picked_nodes)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += f"{node}, "
        if self.tabWidget_radiation_impedance.currentIndex() != 2:
            self.lineEdit_selection_id.setText(text[:-2])

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_radiation_impedance) == 0:
            self.tabWidget_radiation_impedance.setCurrentIndex(0)
            self.tabWidget_radiation_impedance.setTabVisible(1, False)
        else:
            self.tabWidget_radiation_impedance.setTabVisible(1, True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_radiation_impedance.currentIndex()==0:
                self.check_radiation_impedance_type()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_radiation_impedance.currentIndex()==1:
                self.remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)