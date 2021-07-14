import os
from os.path import basename
import numpy as np
from math import pi
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox
from pulse.utils import error, remove_bc_from_file
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

class DOFInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super(DOFInput, self).__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/dofInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.transform_points = opv.transformPoints

        self.project = project
        self.mesh = project.mesh
        self.before_run = self.mesh.get_model_checks()

        self.project_folder_path = project.project_folder_path
        self.structural_bc_info_path = project.file._node_structural_path

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""

        self.nodes = self.mesh.nodes
        self.prescribed_dofs = None
        self.nodes_typed = []
        self.imported_table = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_real_ux = self.findChild(QLineEdit, 'lineEdit_real_ux')
        self.lineEdit_real_uy = self.findChild(QLineEdit, 'lineEdit_real_uy')
        self.lineEdit_real_uz = self.findChild(QLineEdit, 'lineEdit_real_uz')
        self.lineEdit_real_rx = self.findChild(QLineEdit, 'lineEdit_real_rx')
        self.lineEdit_real_ry = self.findChild(QLineEdit, 'lineEdit_real_ry')
        self.lineEdit_real_rz = self.findChild(QLineEdit, 'lineEdit_real_rz')
        self.lineEdit_real_alldofs = self.findChild(QLineEdit, 'lineEdit_real_alldofs')

        self.lineEdit_imag_ux = self.findChild(QLineEdit, 'lineEdit_imag_ux')
        self.lineEdit_imag_uy = self.findChild(QLineEdit, 'lineEdit_imag_uy')
        self.lineEdit_imag_uz = self.findChild(QLineEdit, 'lineEdit_imag_uz')
        self.lineEdit_imag_rx = self.findChild(QLineEdit, 'lineEdit_imag_rx')
        self.lineEdit_imag_ry = self.findChild(QLineEdit, 'lineEdit_imag_ry')
        self.lineEdit_imag_rz = self.findChild(QLineEdit, 'lineEdit_imag_rz')
        self.lineEdit_imag_alldofs = self.findChild(QLineEdit, 'lineEdit_imag_alldofs')

        self.lineEdit_path_table_ux = self.findChild(QLineEdit, 'lineEdit_path_table_ux')
        self.lineEdit_path_table_uy = self.findChild(QLineEdit, 'lineEdit_path_table_uy')
        self.lineEdit_path_table_uz = self.findChild(QLineEdit, 'lineEdit_path_table_uz')
        self.lineEdit_path_table_rx = self.findChild(QLineEdit, 'lineEdit_path_table_rx')
        self.lineEdit_path_table_ry = self.findChild(QLineEdit, 'lineEdit_path_table_ry')
        self.lineEdit_path_table_rz = self.findChild(QLineEdit, 'lineEdit_path_table_rz')

        self.toolButton_load_ux_table = self.findChild(QToolButton, 'toolButton_load_ux_table')
        self.toolButton_load_uy_table = self.findChild(QToolButton, 'toolButton_load_uy_table')
        self.toolButton_load_uz_table = self.findChild(QToolButton, 'toolButton_load_uz_table')
        self.toolButton_load_rx_table = self.findChild(QToolButton, 'toolButton_load_rx_table')
        self.toolButton_load_ry_table = self.findChild(QToolButton, 'toolButton_load_ry_table')
        self.toolButton_load_rz_table = self.findChild(QToolButton, 'toolButton_load_rz_table') 

        self.toolButton_load_ux_table.clicked.connect(self.load_ux_table)
        self.toolButton_load_uy_table.clicked.connect(self.load_uy_table)
        self.toolButton_load_uz_table.clicked.connect(self.load_uz_table)
        self.toolButton_load_rx_table.clicked.connect(self.load_rx_table)
        self.toolButton_load_ry_table.clicked.connect(self.load_ry_table)
        self.toolButton_load_rz_table.clicked.connect(self.load_rz_table)

        self.ux_table = None
        self.uy_table = None
        self.uz_table = None
        self.rx_table = None
        self.ry_table = None
        self.rz_table = None

        self.basename_ux = None
        self.basename_uy = None
        self.basename_uz = None
        self.basename_rx = None
        self.basename_ry = None
        self.basename_rz = None

        self.radioButton_linear_disp = self.findChild(QRadioButton, 'radioButton_linear_disp')    
        self.radioButton_linear_vel = self.findChild(QRadioButton, 'radioButton_linear_vel')  
        self.radioButton_linear_acc = self.findChild(QRadioButton, 'radioButton_linear_acc')     
        self.radioButton_linear_disp.clicked.connect(self.radioButtonEvent_linear_data)
        self.radioButton_linear_vel.clicked.connect(self.radioButtonEvent_linear_data)   
        self.radioButton_linear_acc.clicked.connect(self.radioButtonEvent_linear_data) 
        self.linear_disp = self.radioButton_linear_disp.isChecked()
        self.linear_vel  = self.radioButton_linear_vel.isChecked()
        self.linear_acc  = self.radioButton_linear_acc.isChecked()
    
        self.radioButton_angular_disp = self.findChild(QRadioButton, 'radioButton_angular_disp')    
        self.radioButton_angular_vel = self.findChild(QRadioButton, 'radioButton_angular_vel')  
        self.radioButton_angular_acc = self.findChild(QRadioButton, 'radioButton_angular_acc')  
        self.radioButton_angular_disp.clicked.connect(self.radioButtonEvent_angular_data)
        self.radioButton_angular_vel.clicked.connect(self.radioButtonEvent_angular_data)   
        self.radioButton_angular_acc.clicked.connect(self.radioButtonEvent_angular_data)         
        self.angular_disp = self.radioButton_angular_disp.isChecked()
        self.angular_vel  = self.radioButton_angular_vel.isChecked()
        self.angular_acc  = self.radioButton_angular_acc.isChecked()

        self.tabWidget_prescribed_dofs = self.findChild(QTabWidget, "tabWidget_prescribed_dofs")
        self.tab_constant_values = self.tabWidget_prescribed_dofs.findChild(QWidget, "tab_constant_values")
        self.tab_table = self.tabWidget_prescribed_dofs.findChild(QWidget, "tab_table_values")

        self.treeWidget_prescribed_dofs = self.findChild(QTreeWidget, 'treeWidget_prescribed_dofs')
        self.treeWidget_prescribed_dofs.setColumnWidth(0, 80)
        # self.treeWidget_prescribed_dofs.setColumnWidth(1, 60)
        self.treeWidget_prescribed_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton_constant_value_confirm = self.findChild(QPushButton, 'pushButton_constant_value_confirm')
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)

        self.pushButton_data_table_setup = self.findChild(QPushButton, 'pushButton_data_table_setup')
        self.pushButton_data_table_setup.clicked.connect(self.check_table_values)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_bc_confirm_2 = self.findChild(QPushButton, 'pushButton_remove_bc_confirm_2')
        self.pushButton_remove_bc_confirm_2.clicked.connect(self.check_remove_bc_from_node)

        self.writeNodes(self.opv.getListPickedPoints())
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_prescribed_dofs.currentIndex()==0:
                self.check_constant_values()
            elif self.tabWidget_prescribed_dofs.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent_linear_data(self):
        self.linear_disp = self.radioButton_linear_disp.isChecked()
        self.linear_vel  = self.radioButton_linear_vel.isChecked()
        self.linear_acc  = self.radioButton_linear_acc.isChecked()    

    def radioButtonEvent_angular_data(self):
        self.angular_disp = self.radioButton_angular_disp.isChecked()
        self.angular_vel  = self.radioButton_angular_vel.isChecked()
        self.angular_acc  = self.radioButton_angular_acc.isChecked()      

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                error("Wrong input for real part of {}!".format(label), "Error")
                self.stop = True
                return
        else:
            _real = None

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                error("Wrong input for imaginary part of {}!".format(label), "Error")
                self.stop = True
                return
        else:
            _imag = None
        
        if label == 'all dofs':

            if _real is None and _imag is None:
                value = None
            elif _real is None:
                value = 1j*_imag
            elif _imag is None:
                value = complex(_real)
            else:
                value = _real + 1j*_imag
            output = [value, value, value, value, value, value] 

        else:

            if _real is None and _imag is None:
                output = None
            elif _real is None:
                output = 1j*_imag
            elif _imag is None:
                output = complex(_real)
            else:             
                output = _real + 1j*_imag

        return output

    def check_constant_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        if self.lineEdit_real_alldofs.text() != "" or self.lineEdit_imag_alldofs.text() != "":
            prescribed_dofs = self.check_complex_entries(self.lineEdit_real_alldofs, self.lineEdit_imag_alldofs, "all dofs")
            if self.stop:
                return 
        else:    

            ux = self.check_complex_entries(self.lineEdit_real_ux, self.lineEdit_imag_ux, "ux")
            if self.stop:
                return
            uy = self.check_complex_entries(self.lineEdit_real_uy, self.lineEdit_imag_uy, "uy")
            if self.stop:
                return        
            uz = self.check_complex_entries(self.lineEdit_real_uz, self.lineEdit_imag_uz, "uz")
            if self.stop:
                return        
                
            rx = self.check_complex_entries(self.lineEdit_real_rx, self.lineEdit_imag_rx, "rx")
            if self.stop:
                return        
            ry = self.check_complex_entries(self.lineEdit_real_ry, self.lineEdit_imag_ry, "ry")
            if self.stop:
                return        
            rz = self.check_complex_entries(self.lineEdit_real_rz, self.lineEdit_imag_rz, "rz")
            if self.stop:
                return

            prescribed_dofs = [ux, uy, uz, rx, ry, rz]

        if prescribed_dofs.count(None) != 6:
            self.prescribed_dofs = prescribed_dofs
            self.project.set_prescribed_dofs_bc_by_node(self.nodes_typed, self.prescribed_dofs, False)       
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            error("You must to inform at least one nodal load to confirm the input!", title = " ERROR ")
        
    def load_table(self, lineEdit, text):
        
        self.basename = ""
        window_label = 'Choose a table to import the {} nodal load'.format(text)
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.dat;*.csv)')

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
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as log_error:
            error(str(log_error))

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

        except Exception as e:
            error(str(e))

        return self.imported_values, self.basename

    def integration(self, values, dof_label, linear=False, angular=False):
        if self.frequencies[0]==0:
            self.frequencies[0] = float(1e-4)
        if linear:    
            if self.linear_disp:
                values = values
                header = "{} || Frequency [Hz], real[m], imaginary[m], absolute[m]".format(dof_label)
            elif self.linear_vel:
                values = values/(1j*2*pi*self.frequencies)
                header = "{} || Frequency [Hz], real[m/s], imaginary[m/s], absolute[m/s]".format(dof_label)
            elif self.linear_acc:
                values = values/((1j*2*pi*self.frequencies)**2)
                header = "{} || Frequency [Hz], real[m/s²], imaginary[m/s²], absolute[m/s²]".format(dof_label)
        if angular:    
            if self.angular_disp:
                values = values
                header = "{} || Frequency [Hz], real[rad], imaginary[rad], absolute[rad]".format(dof_label)
            elif self.angular_vel:
                values = values/(1j*2*pi*self.frequencies)
                header = "{} || Frequency [Hz], real[rad/s], imaginary[rad/s], absolute[rad/s]".format(dof_label)
            elif self.angular_acc:              
                values = values/((1j*2*pi*self.frequencies)**2)
                header = "{} || Frequency [Hz], real[rad/s²], imaginary[rad/s²], absolute[rad/s²]".format(dof_label)

        real_values = np.real(self.imported_values)
        imag_values = np.imag(self.imported_values)
        abs_values = np.imag(self.imported_values)
        data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
        np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)
        return values

    def load_ux_table(self):
        self.ux_table, self.basename_ux = self.load_table(self.lineEdit_path_table_ux, "ux")

    def load_uy_table(self):
        self.uy_table, self.basename_uy = self.load_table(self.lineEdit_path_table_uy, "uy")

    def load_uz_table(self):
        self.uz_table, self.basename_uz = self.load_table(self.lineEdit_path_table_uz, "uz")

    def load_rx_table(self):
        self.rx_table, self.basename_rx = self.load_table(self.lineEdit_path_table_rx, "rx")

    def load_ry_table(self):
        self.ry_table, self.basename_ry = self.load_table(self.lineEdit_path_table_ry, "ry")

    def load_rz_table(self):
        self.rz_table, self.basename_rz = self.load_table(self.lineEdit_path_table_rz, "rz")

    def check_table_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        ux = uy = uz = None
        if self.lineEdit_path_table_ux != "":
            if self.ux_table is not None:
                ux = self.integration(self.ux_table, "Ux", linear=True)
        if self.lineEdit_path_table_uy != "":
            if self.uy_table is not None:
                uy = self.integration(self.uy_table, "Uy", linear=True)
        if self.lineEdit_path_table_uz != "":
            if self.uz_table is not None:
                uz = self.integration(self.uz_table, "Uz", linear=True)

        rx = ry = rz = None
        if self.lineEdit_path_table_rx != "":
            if self.rx_table is not None:
                rx = self.integration(self.rx_table, "Rx", angular=True)
        if self.lineEdit_path_table_ry != "":
            if self.ry_table is not None:
                ry = self.integration(self.ry_table, "Ry", angular=True)
        if self.lineEdit_path_table_rz != "":
            if self.rz_table is not None:
                rz = self.integration(self.rz_table, "Rz", angular=True)

        self.basenames = [self.basename_ux, self.basename_uy, self.basename_uz, self.basename_rx, self.basename_ry, self.basename_rz]
        self.prescribed_dofs = [ux, uy, uz, rx, ry, rz]
        self.project.set_prescribed_dofs_bc_by_node(self.nodes_typed, self.prescribed_dofs, self.imported_table, table_name=self.basenames)
        self.transform_points(self.nodes_typed)
        self.close()

    def text_label(self, mask):
        
        text = ""
        load_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])
        temp = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4])
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3])
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_nodes_info(self):
        for node in self.project.mesh.nodes_with_prescribed_dofs:
            constrained_dofs_mask = [False if bc is None else True for bc in node.prescribed_dofs]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(constrained_dofs_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_prescribed_dofs.addTopLevelItem(new)

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
        key_strings = ["displacements", "rotations"]
        message = "The prescribed dof(s) value(s) attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
        self.project.mesh.set_prescribed_dofs_bc_by_node(self.nodes_typed, [None, None, None, None, None, None])
        self.transform_points(self.nodes_typed)
        self.treeWidget_prescribed_dofs.clear()
        self.load_nodes_info()
        self.close()

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())