from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QStackedWidget, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

from collections import defaultdict
import numpy as np


window_title_1 = "Error"
window_title_2 = "Warning"

class ReciprocatingMachineSelector(QDialog):
    def __init__(self, machine_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/reciprocating_pump_selector.ui"
        uic.loadUi(ui_path, self)

        self.machine_type = machine_type

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.selection_callback()

        self.load_reciprocating_pump_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.complete = False
        self.volumetric_flow_rate = None
        self.before_run = app().project.get_pre_solution_model_checks()

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_connection_type: QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_volumetric_flow_rate: QLineEdit

        # QPushButton
        self.pushButton_select: QPushButton
        self.pushButton_exit: QPushButton
        self.pushButton_reset_selection: QPushButton

        # QTreeWidget
        self.treeWidget_reciprocating_machine_data: QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_reset_selection.clicked.connect(self.reset_selection)
        self.pushButton_select.clicked.connect(self.select_callback)
        #
        self.treeWidget_reciprocating_machine_data.itemClicked.connect(self.on_click_item)
        self.treeWidget_reciprocating_machine_data.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selected_id.setText(text)

            if len(selected_nodes) == 1:
                node_id = selected_nodes[0]
                recip_pump = self.properties._get_property(f"reciprocating_{self.machine_type}_excitation", node_id=node_id)

                if isinstance(recip_pump, dict):
                    connection_type = recip_pump["connection_type"]
                    volumetric_flow_rate = recip_pump["values"][0, 1]
                    self.lineEdit_selected_id.setText(str(node_id))
                    self.lineEdit_connection_type.setText(connection_type)
                    self.lineEdit_volumetric_flow_rate.setText(f"{volumetric_flow_rate : .6e}")

    def _config_widgets(self):
        self.lineEdit_connection_type.setDisabled(True)
        self.lineEdit_selected_id.setDisabled(True)
        self.lineEdit_volumetric_flow_rate.setDisabled(True)
        self.treeWidget_reciprocating_machine_data.setColumnWidth(0, 150)

    def reset_selection(self):
        self.lineEdit_selected_id.setText("")
        self.lineEdit_connection_type.setText("")
        self.lineEdit_volumetric_flow_rate.setText("")

    def select_callback(self):
        if self.lineEdit_selected_id.text() != "":
            self.selected_node =  int(self.lineEdit_selected_id.text())
            self.volumetric_flow_rate = float(self.lineEdit_volumetric_flow_rate.text())
            self.close()

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_connection_type.setText(item.text(1))
        self.lineEdit_volumetric_flow_rate.setText(f"{float(item.text(2)) : .6e}")

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def load_reciprocating_pump_info(self):

        self.treeWidget_reciprocating_machine_data.clear()
        header = self.treeWidget_reciprocating_machine_data.headerItem()

        header_labels = ["Node ID", "Connection type", "Volumetric flow rate [m³/s]"]
        for col, label in enumerate(header_labels):
            header.setText(col, label)
            header.setTextAlignment(col, Qt.AlignCenter)

        for (property, node_id), data in self.properties.nodal_properties.items():
            if property == f"reciprocating_{self.machine_type}_excitation":
                volumetric_flow_rate = np.real(data["values"][0][0])
                connection_type = data.get("connection_type", "not detected")
                item = QTreeWidgetItem([str(node_id), connection_type, f"{volumetric_flow_rate : .6e}"])

                for col in range(len(header_labels)):
                    item.setTextAlignment(col, Qt.AlignCenter)

                self.treeWidget_reciprocating_machine_data.addTopLevelItem(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.select_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)