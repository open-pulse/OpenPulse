import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QWidget, QTreeWidgetItem, QTreeWidget, QSpinBox
from pulse.utils import error
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile
from pulse.utils import error, remove_bc_from_file

class VolumeVelocityInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/volumevelocityInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.transform_points = self.opv.transformPoints

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = self.preprocessor.get_model_checks()

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.project_folder_path = project.project_folder_path
        self.acoustic_bc_info_path = project.file._node_acoustic_path

        self.nodes = project.preprocessor.nodes
        self.volume_velocity = None
        self.nodes_typed = []
        self.imported_table = False
        self.remove_volume_velocity = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.lineEdit_volume_velocity_real = self.findChild(QLineEdit, 'lineEdit_volume_velocity_real')
        self.lineEdit_volume_velocity_imag = self.findChild(QLineEdit, 'lineEdit_volume_velocity_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')

        self.tabWidget_volume_velocity = self.findChild(QTabWidget, "tabWidget_volume_velocity")
        self.tabWidget_volume_velocity.currentChanged.connect(self.tabEvent_volume_velocity)

        self.tab_single_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_single_values")
        self.tab_table_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_table_values")

        self.treeWidget_volume_velocity = self.findChild(QTreeWidget, 'treeWidget_volume_velocity')
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)
        self.treeWidget_volume_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_volume_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.toolButton_load_table = self.findChild(QToolButton, 'toolButton_load_table')
        self.toolButton_load_table.clicked.connect(self.load_volume_velocity_table)

        self.pushButton_single_values_confirm = self.findChild(QPushButton, 'pushButton_single_values_confirm')
        self.pushButton_single_values_confirm.clicked.connect(self.check_single_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.lineEdit_skiprows = self.findChild(QSpinBox, 'spinBox')

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_bc_confirm_2 = self.findChild(QPushButton, 'pushButton_remove_bc_confirm_2')
        self.pushButton_remove_bc_confirm_2.clicked.connect(self.check_remove_bc_from_node)
        
        self.writeNodes(self.opv.getListPickedPoints())
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_volume_velocity.currentIndex()==0:
                self.check_single_values()
            if self.tabWidget_volume_velocity.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_volume_velocity.currentIndex()==2:
                self.check_remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def tabEvent_volume_velocity(self):
        self.current_tab =  self.tabWidget_volume_velocity.currentIndex()
        if self.current_tab == 2:
            self.lineEdit_nodeID.setDisabled(True)
        else:
            self.lineEdit_nodeID.setDisabled(False)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                error("Wrong input for real part of volume velocity.", title="Error")
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                error("Wrong input for imaginary part of volume velocity.", title="Error")
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F

    def check_single_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        volume_velocity = self.check_complex_entries(self.lineEdit_volume_velocity_real, self.lineEdit_volume_velocity_imag)
 
        if self.stop:
            return

        if volume_velocity is not None:
            self.volume_velocity = volume_velocity
            self.project.set_volume_velocity_bc_by_node(self.nodes_typed, self.volume_velocity, False)
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            error("You must to inform at least one nodal load to confirm the input!", title = " ERROR ")
 
    def load_table(self, lineEdit, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the volume velocity'
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.dat; *.csv)')

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        lineEdit.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        if "\\" in self.project_folder_path:
            self.new_load_path_table = "{}\\{}".format(self.project_folder_path, self.basename)
        elif "/" in self.project_folder_path:
            self.new_load_path_table = "{}/{}".format(self.project_folder_path, self.basename)

        try:
            skiprows = int(self.lineEdit_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
        except Exception as e:
            message = [str(e) + " It is recommended to skip the header rows."] 
            error(message[0], title="ERROR WHILE LOADING TABLE")
            return

        if imported_file.shape[1]<2:
            error("The imported table has insufficient number of columns. The spectrum \ndata must have frequencies, real and imaginary columns.")
            return
    
        try:
            self.imported_values = imported_file[:,1] + 1j*imported_file[:,2]
            if imported_file.shape[1]>2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.imported_table = True

                real_values = np.real(self.imported_values)
                imag_values = np.imag(self.imported_values)
                abs_values = np.abs(self.imported_values)
                data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
                np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

        except Exception as e:
            error(str(e))

        return self.imported_values, self.basename

    def load_volume_velocity_table(self):
        header = "Volume velocity || Frequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"
        self.volume_velocity, self.basename_volume_velocity = self.load_table(self.lineEdit_load_table_path, header)
    
    def check_table_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        if self.lineEdit_load_table_path != "":
            if self.volume_velocity is not None:
                self.project.set_volume_velocity_bc_by_node(self.nodes_typed, self.volume_velocity, True, table_name=self.basename_volume_velocity)
                self.transform_points(self.nodes_typed)
        self.close()

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def load_nodes_info(self):
        for node in self.project.preprocessor.nodes_with_volume_velocity:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.volume_velocity))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_volume_velocity.addTopLevelItem(new)

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
            
        key_strings = ["volume velocity"]
        message = "The volume velocity attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.acoustic_bc_info_path, key_strings, message)
        self.project.preprocessor.set_volume_velocity_bc_by_node(self.nodes_typed, None)
        self.transform_points(self.nodes_typed)
        self.treeWidget_volume_velocity.clear()
        self.load_nodes_info()
        # self.close()

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())