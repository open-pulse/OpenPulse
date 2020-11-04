from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QCheckBox, QSpinBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from collections import defaultdict
import os
import numpy as np
import matplotlib.pyplot as plt  

from pulse.preprocessing.compressor_model import CompressorModel
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class NodalLinksInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/nodalLinksInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.mesh = project.mesh
        self.nodes = self.project.mesh.nodes
        self.node_id = self.opv.getListPickedPoints()

        self.project_folder_path = project.project_folder_path        
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        
        self.lineEdit_selected_node_ID = self.findChild(QLineEdit, 'lineEdit_selected_node_ID')
        self.lineEdit_first_node_ID = self.findChild(QLineEdit, 'lineEdit_first_node_ID')
        self.lineEdit_last_node_ID = self.findChild(QLineEdit, 'lineEdit_last_node_ID')

        self.radioButton_button_1 = self.findChild(QRadioButton, 'radioButton_button_1')
        self.radioButton_button_2 = self.findChild(QRadioButton, 'radioButton_button_2')
        self.radioButton_button_3 = self.findChild(QRadioButton, 'radioButton_button_3')

        # self.radioButton_button_1.clicked.connect(self.radioButtonEvent_)
        # self.radioButton_button_2.clicked.connect(self.radioButtonEvent_)
        # self.radioButton_button_3.clicked.connect(self.radioButtonEvent_)

        # self.radioButtonEvent_()
        
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        # self.pushButton_confirm.clicked.connect(self.process_all_inputs)

        self.pushButton_remove_links = self.findChild(QPushButton, 'pushButton_remove_links')
        # self.pushButton_remove_links.clicked.connect(self.remove_links)

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        # self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        # self.tabWidget_compressor = self.findChild(QTabWidget, 'tabWidget_compressor')
        # self.tabWidget_compressor.currentChanged.connect(self.tabEvent)

        self.treeWidget_nodal_links = self.findChild(QTreeWidget, 'treeWidget_nodal_links')
        self.treeWidget_nodal_links.setColumnWidth(0, 90)
        self.treeWidget_nodal_links.setColumnWidth(1, 140)
        self.treeWidget_nodal_links.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_links.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_links.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.lineEdit_node_ID_info = self.findChild(QLineEdit, 'lineEdit_node_ID_info')
        self.lineEdit_table_name_info = self.findChild(QLineEdit, 'lineEdit_table_name_info')

        self.writeNodes(self.opv.getListPickedPoints())
        # self.spinBox_event_number_of_cylinders()
        # self.load_volume_velocity_tables_info()
        
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.process_all_inputs()
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
            self.close()

    # def radioButtonEvent_(self):
    #     self.current_tab_index = self.tabWidget_compressor.currentIndex()
    #     if self.current_tab_index == 3:
    #         self.pushButton_confirm.setDisabled(True)
    #     else:
    #         self.pushButton_confirm.setDisabled(False)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_selected_node_ID.setText(text)

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())

    def check_nodeID(self, lineEdit, export=False):
        try:
            tokens = lineEdit.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            node_typed = list(map(int, tokens))

        except Exception:
            title = "INVALID NODE ID"
            message = "Wrong input for Node ID."
            PrintMessageInput([title, message, window_title1])
            return True

        if len(node_typed) == 1:
            try:
                self.nodeID = self.mesh.nodes[node_typed[0]].external_index
            except:
                title = "INVALID NODE ID"
                message = " The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))
                PrintMessageInput([title, message, window_title1])
                return True

        elif len(node_typed) == 0:
            title = "INVALID NODE ID"
            message = "Please, enter a valid Node ID."
            PrintMessageInput([title, message, window_title1])
            return True
            
        else:
            title = "MULTIPLE NODE IDs"
            message = "Please, type or select only one Node ID."
            PrintMessageInput([title, message, window_title1])
            return True

        if len(self.project.mesh.neighboor_elements_of_node(self.nodeID))>1:
            title = "INVALID SELECTION - NODE {}".format(self.nodeID)
            message = "The selected NODE ID must be in the beginning \nor termination of the pipelines."
            PrintMessageInput([title, message, window_title1])
            return True
              
    def check_all_nodes(self, check_nodes=True):
        
        if check_nodes:
            if self.connection_at_suction_and_discharge:

                if self.check_nodeID(self.lineEdit_suction_node_ID):
                    return True
                self.suction_node_ID = self.nodeID
                
                if self.check_nodeID(self.lineEdit_discharge_node_ID):
                    return True
                self.discharge_node_ID = self.nodeID

                if self.suction_node_ID == self.discharge_node_ID:
                    title = "ERROR IN NODES SELECTION"
                    message = "The nodes selected to the suction and discharge must differ. Try to choose another pair of nodes."
                    PrintMessageInput([title, message, window_title1])
                    return True

            if self.connection_at_suction:
                if self.check_nodeID(self.lineEdit_suction_node_ID):
                    return True
                self.suction_node_ID = self.nodeID

            if self.connection_at_discharge:
                if self.check_nodeID(self.lineEdit_discharge_node_ID):
                    return True
                self.discharge_node_ID = self.nodeID
        return False
        
    def check_input_parameters(self, lineEdit, label, _float=True):
        title = "INPUT ERROR"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([title, message, window_title1])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, window_title1])
                return True
        else:
            message = "None value has been typed to the {}.".format(label)
            PrintMessageInput([title, message, window_title1])
            return True
        return False
    
    def on_click_item(self, item):
        self.lineEdit_node_ID_info.setText(item.text(0))
        self.lineEdit_table_name_info.setText(item.text(1))

    # def get_path_of_selected_table(self):
    #     if "\\" in self.project_folder_path:
    #         self.path_of_selected_table = "{}\\{}".format(self.project_folder_path, self.selected_table)
    #     elif "/" in self.project_folder_path:
    #         self.path_of_selected_table = "{}/{}".format(self.project_folder_path, self.selected_table)

    def force_to_close(self):
        self.close()
