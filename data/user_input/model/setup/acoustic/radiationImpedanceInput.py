import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QWidget, QTreeWidgetItem, QTreeWidget, QRadioButton
from pulse.utils import error
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile
from pulse.utils import error, remove_bc_from_file

class RadiationImpedanceInput(QDialog):
    def __init__(self, project, opv, transform_points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/radiationImpedanceInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""

        self.project = project
        self.mesh = project.mesh
        self.transform_points = transform_points
        self.project_folder_path = project.project_folder_path
        self.acoustic_bc_info_path = project.file._node_acoustic_path

        self.nodes = project.mesh.nodes
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

        self.pushButton_remove_bc_confirm_2 = self.findChild(QPushButton, 'pushButton_remove_bc_confirm_2')
        self.pushButton_remove_bc_confirm_2.clicked.connect(self.check_remove_bc_from_node)
        
        self.writeNodes(self.opv.getListPickedPoints())
        self.load_nodes_info()
        self.exec_()

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
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check_radiation_impedance_type(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.mesh.check_input_NodeID(lineEdit_nodeID)
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
            self.transform_points(self.nodes_typed)
            self.close()
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
        self.stop, self.nodes_typed = self.mesh.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        key_strings = ["radiation impedance"]
        message = "The radiation impedance attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.acoustic_bc_info_path, key_strings, message)
        self.project.mesh.set_radiation_impedance_bc_by_node(self.nodes_typed, None)
        self.transform_points(self.nodes_typed)
        self.treeWidget_radiation_impedance.clear()
        self.load_nodes_info()
        # self.close()

    def load_nodes_info(self):
        for node in self.project.mesh.nodes_with_radiation_impedance:
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
        self.writeNodes(self.opv.getListPickedPoints())