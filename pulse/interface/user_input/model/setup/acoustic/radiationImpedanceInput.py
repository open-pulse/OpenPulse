from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
from pulse.utils import remove_bc_from_file

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

window_title_1 = "Error"
window_title_2 = "Warning"

class RadiationImpedanceInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/model/setup/acoustic/radiationImpedanceInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.acoustic_bc_info_path = project.file._node_acoustic_path

        self.nodes = project.preprocessor.nodes
        self.radiation_impedance = None
        self.nodes_typed = []
  
        self.remove_acoustic_pressure = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.radioButton_anechoic = self.findChild(QRadioButton, 'radioButton_anechoic')
        self.radioButton_flanged = self.findChild(QRadioButton, 'radioButton_flanged')
        self.radioButton_unflanged = self.findChild(QRadioButton, 'radioButton_unflanged')
        self.radioButton_anechoic.toggled.connect(self.radioButtonEvent)
        self.radioButton_flanged.toggled.connect(self.radioButtonEvent)
        self.radioButton_unflanged.toggled.connect(self.radioButtonEvent)
        self.flag_anechoic = self.radioButton_anechoic.isChecked()
        self.flag_flanged = self.radioButton_flanged.isChecked()
        self.flag_unflanged = self.radioButton_unflanged.isChecked()

        self.tabWidget_radiation_impedance = self.findChild(QTabWidget, "tabWidget_radiation_impedance")
        self.tabWidget_radiation_impedance.currentChanged.connect(self.tabEvent_radiation_impedance)

        self.tab_model = self.tabWidget_radiation_impedance.findChild(QWidget, "tab_model")
        self.tab_remove = self.tabWidget_radiation_impedance.findChild(QWidget, "tab_remove")

        self.treeWidget_radiation_impedance = self.findChild(QTreeWidget, 'treeWidget_radiation_impedance')
        self.treeWidget_radiation_impedance.setColumnWidth(1, 20)
        self.treeWidget_radiation_impedance.setColumnWidth(2, 80)
        self.treeWidget_radiation_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_radiation_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_radiation_impedance_type)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.check_reset)
        
        self.update()
        self.load_nodes_info()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_radiation_impedance.currentIndex()==0:
                self.check_radiation_impedance_type()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_radiation_impedance.currentIndex()==1:
                self.check_remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flag_anechoic = self.radioButton_anechoic.isChecked()
        self.flag_flanged = self.radioButton_flanged.isChecked()
        self.flag_unflanged = self.radioButton_unflanged.isChecked()

    def tabEvent_radiation_impedance(self):
        self.current_tab =  self.tabWidget_radiation_impedance.currentIndex()
        if self.current_tab == 1:
            self.lineEdit_nodeID.setDisabled(True)
        else:
            self.lineEdit_nodeID.setDisabled(False)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += f"{node}, "
        self.lineEdit_nodeID.setText(text[:-2])

    def check_radiation_impedance_type(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        try:
            if self.flag_anechoic:
                type_id = 0
            elif self.flag_unflanged:
                type_id = 1
            elif self.flag_flanged:
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
        self.lineEdit_nodeID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.check_remove_bc_from_node()

    def check_remove_bc_from_node(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        key_strings = ["radiation impedance"]
        message = "The radiation impedance attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.acoustic_bc_info_path, key_strings, message)
        self.preprocessor.set_radiation_impedance_bc_by_node(self.nodes_typed, None)
        self.opv.updateRendererMesh()
        self.load_nodes_info()
        # self.close()

    def check_reset(self):
        if len(self.preprocessor.nodes_with_radiation_impedance)>0:
            
            title = f"Removal of all applied radiation impedances"
            message = "Do you really want to remove the radiation impedance(s) \napplied to the following node(s)?\n\n"
            for node in self.preprocessor.nodes_with_radiation_impedance:
                message += f"{node.external_index}\n"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            _nodes_with_radiation_impedance = self.preprocessor.nodes_with_radiation_impedance.copy()
            if read._continue:
                for node in _nodes_with_radiation_impedance:
                    node_id = node.external_index
                    key_strings = ["radiation impedance"]
                    remove_bc_from_file([node_id], self.acoustic_bc_info_path, key_strings, None)
                    self.preprocessor.set_radiation_impedance_bc_by_node(node_id, None)
                
                title = "Radiation impedance resetting process complete"
                message = "All radiation impedances applied to the acoustic\n" 
                message += "model have been removed from the model."
                PrintMessageInput([title, message, window_title_2])

                self.opv.updateRendererMesh()
                self.close()

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
    
    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.radiation_impedance_type == 0:
                self.radioButton_anechoic.setChecked(True)
            if node.radiation_impedance_type == 1:
                self.radioButton_unflanged.setChecked(True)
            if node.radiation_impedance_type == 2:
                self.radioButton_flanged.setChecked(True)                
        self.writeNodes(self.opv.getListPickedPoints())