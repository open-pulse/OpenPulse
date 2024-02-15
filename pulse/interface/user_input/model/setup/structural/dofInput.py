
from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QRadioButton, QTabWidget, QToolButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
from math import pi

from pulse.utils import remove_bc_from_file, get_new_path
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

window_title ="Error"

class DOFInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super(DOFInput, self).__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/model/setup/structural/dofInput.ui'), self)

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

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_filename = ""
        self.structural_bc_info_path = project.file._node_structural_path
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.prescribed_dofs_files_folder_path = get_new_path(self.structural_folder_path, "prescribed_dofs_files")

        self.nodes = self.preprocessor.nodes
        self.prescribed_dofs = None
        self.nodes_typed = []
        self.inputs_from_node = False
        self.copy_path = False
        self.basenames = []
        self.list_Nones = [None, None, None, None, None, None]

        self.stop = False
        self.list_frequencies = []
        
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

        self.list_lineEdit_constant_values = [  [self.lineEdit_real_ux, self.lineEdit_imag_ux],
                                                [self.lineEdit_real_uy, self.lineEdit_imag_uy],
                                                [self.lineEdit_real_uz, self.lineEdit_imag_uz],
                                                [self.lineEdit_real_rx, self.lineEdit_imag_rx],
                                                [self.lineEdit_real_ry, self.lineEdit_imag_ry],
                                                [self.lineEdit_real_rz, self.lineEdit_imag_rz]  ]

        self.lineEdit_path_table_ux = self.findChild(QLineEdit, 'lineEdit_path_table_ux')
        self.lineEdit_path_table_uy = self.findChild(QLineEdit, 'lineEdit_path_table_uy')
        self.lineEdit_path_table_uz = self.findChild(QLineEdit, 'lineEdit_path_table_uz')
        self.lineEdit_path_table_rx = self.findChild(QLineEdit, 'lineEdit_path_table_rx')
        self.lineEdit_path_table_ry = self.findChild(QLineEdit, 'lineEdit_path_table_ry')
        self.lineEdit_path_table_rz = self.findChild(QLineEdit, 'lineEdit_path_table_rz')

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_ux,
                                            self.lineEdit_path_table_uy,
                                            self.lineEdit_path_table_uz,
                                            self.lineEdit_path_table_rx,
                                            self.lineEdit_path_table_ry,
                                            self.lineEdit_path_table_rz ]

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

        self.ux_filename = None
        self.uy_filename = None
        self.uz_filename = None
        self.rx_filename = None
        self.ry_filename = None
        self.rz_filename = None

        self.ux_basename = None
        self.uy_basename = None
        self.uz_basename = None
        self.rx_basename = None
        self.ry_basename = None
        self.rz_basename = None

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
        self.tab_table_values = self.tabWidget_prescribed_dofs.findChild(QWidget, "tab_table_values")

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

        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.reset_all)

        self.update()
        self.load_nodes_info()
        self.exec()

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

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([title, message, window_title])
                lineEdit_real.setFocus()
                self.stop = True
                return
        else:
            _real = None

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([title, message, window_title])
                lineEdit_imag.setFocus()
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
            self.lineEdit_nodeID.setFocus()
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

        if prescribed_dofs != self.list_Nones:
            self.prescribed_dofs = prescribed_dofs
            table_names = self.list_Nones
            data = [self.prescribed_dofs, table_names]
            self.remove_all_table_files_from_nodes(self.nodes_typed)
            self.project.set_prescribed_dofs_bc_by_node(self.nodes_typed, data, False)   
            print(f"[Set Prescribed DOF] - defined at node(s) {self.nodes_typed}")    
            self.opv.updateRendererMesh()
            self.close()
        else:
            title = "Additional inputs required"
            message = "You must inform at least one prescribed dof\n"
            message += "before confirming the input!"
            PrintMessageInput([title, message, window_title]) 

    def load_table(self, lineEdit, dof_label, direct_load=False):
        title = "Error reached while loading table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the {} nodal load'.format(dof_label)
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None
            
            self.imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)         
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum \n"
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([title, message, window_title])
                lineEdit.setFocus()
                return None, None

            self.imported_values = imported_file[:,1] + 1j*imported_file[:,2]

            if imported_file.shape[1] >= 3:
                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]

                if self.project.change_project_frequency_setup(self.imported_filename, list(self.frequencies)):
                    self.stop = True
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                    self.stop = False
            
            return self.imported_values, self.imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([title, message, window_title])
            lineEdit.setFocus()
            return None, None

    def process_integration_and_save_table_files(self, node_id, values, filename, dof_label, linear=False, angular=False):
        if self.frequencies[0]==0:
            self.frequencies[0] = float(1e-6)
        if linear:    
            if self.linear_disp:
                values = values
                header = "OpenPulse - imported table for prescribed displacement {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m], imaginary[m], absolute[m]"
            elif self.linear_vel:
                values = values/(1j*2*pi*self.frequencies)
                header = "OpenPulse - imported table for prescribed velocity {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m/s], imaginary[m/s], absolute[m/s]"
            elif self.linear_acc:
                values = values/((1j*2*pi*self.frequencies)**2)
                header = "OpenPulse - imported table for prescribed acceleration {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m/s²], imaginary[m/s²], absolute[m/s²]"
        if angular:    
            if self.angular_disp:
                values = values
                header = "OpenPulse - imported table for prescribed angular displacement {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[rad], imaginary[rad], absolute[rad]"
            elif self.angular_vel:
                values = values/(1j*2*pi*self.frequencies)
                header = "OpenPulse - imported table for prescribed angular velocity {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[rad/s], imaginary[rad/s], absolute[rad/s]"
            elif self.angular_acc:              
                values = values/((1j*2*pi*self.frequencies)**2)
                header = "OpenPulse - imported table for prescribed angular acceleration {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[rad/s²], imaginary[rad/s²], absolute[rad/s²]"
        
        if self.frequencies[0] == float(1e-6):
            self.frequencies[0] = 0
        
        real_values = np.real(values)
        imag_values = np.imag(values)
        abs_values = np.abs(values)
        data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
        self.project.create_folders_structural("prescribed_dofs_files")
        
        basename = f"prescribed_dof_{dof_label}_node_{node_id}.dat"

        header = header.format(dof_label.capitalize(), node_id)
        new_path_table = get_new_path(self.prescribed_dofs_files_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def load_ux_table(self):
        self.ux_table, self.ux_filename = self.load_table(self.lineEdit_path_table_ux, "ux")
        if self.stop:
            self.stop = False
            self.ux_table, self.ux_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_ux)

    def load_uy_table(self):
        self.uy_table, self.uy_filename = self.load_table(self.lineEdit_path_table_uy, "uy")
        if self.stop:
            self.stop = False
            self.uy_table, self.uy_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_uy)
            
    def load_uz_table(self):
        self.uz_table, self.uz_filename = self.load_table(self.lineEdit_path_table_uz, "uz")
        if self.stop:
            self.stop = False
            self.uz_table, self.uz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_uz)
            
    def load_rx_table(self):
        self.rx_table, self.rx_filename = self.load_table(self.lineEdit_path_table_rx, "rx")
        if self.stop:
            self.stop = False
            self.rx_table, self.rx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_rx)
            
    def load_ry_table(self):
        self.ry_table, self.ry_filename = self.load_table(self.lineEdit_path_table_ry, "ry")
        if self.stop:
            self.stop = False
            self.ry_table, self.ry_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_ry)
            
    def load_rz_table(self):
        self.rz_table, self.rz_filename = self.load_table(self.lineEdit_path_table_rz, "rz")
        if self.stop:
            self.stop = False
            self.rz_table, self.rz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_rz)

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()      

    def check_table_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            self.lineEdit_nodeID.setFocus()
            return
        list_table_names = self.get_list_tables_names_from_selected_nodes(self.nodes_typed)

        for node_id in self.nodes_typed:
            ux = uy = uz = None
            if self.ux_table is None:
                if self.ux_filename is None:
                    self.ux_table, self.ux_filename = self.load_table(self.lineEdit_path_table_ux, "ux", direct_load=True)

            if self.ux_table is not None:
                ux, self.ux_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.ux_table, 
                                                                                        self.ux_filename, 
                                                                                        "ux", 
                                                                                        linear=True   )

            if self.uy_table is None:
                if self.uy_filename is None:
                    self.uy_table, self.uy_filename = self.load_table(self.lineEdit_path_table_uy, "uy", direct_load=True)
            if self.uy_table is not None:
                uy, self.uy_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.uy_table, 
                                                                                        self.uy_filename, 
                                                                                        "uy", 
                                                                                        linear=True   )
 
            if self.uz_table is None:
                if self.uz_filename is None:
                    self.uz_table, self.uz_filename = self.load_table(self.lineEdit_path_table_uz, "uz", direct_load=True)
            if self.uz_table is not None:
                uz, self.uz_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.uz_table, 
                                                                                        self.uz_filename, 
                                                                                        "uz", 
                                                                                        linear=True   )
            rx = ry = rz = None
            if self.rx_table is None:
                if self.rx_filename is None:
                    self.rx_table, self.rx_filename = self.load_table(self.lineEdit_path_table_rx, "rx", direct_load=True)
            if self.rx_table is not None:
                rx, self.rx_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.rx_table, 
                                                                                        self.rx_filename, 
                                                                                        "rx", 
                                                                                        angular=True   )

            if self.ry_table is None:
                if self.ry_filename is None:
                    self.ry_table, self.ry_filename = self.load_table(self.lineEdit_path_table_ry, "ry", direct_load=True)
            if self.ry_table is not None:
                ry, self.ry_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.ry_table, 
                                                                                        self.ry_filename, 
                                                                                        "ry", 
                                                                                        angular=True   )

            if self.rz_table is None:
                if self.rz_filename is None:
                    self.rz_table, self.rz_filename = self.load_table(self.lineEdit_path_table_rz, "rz", direct_load=True)
            if self.rz_table is not None:
                rz, self.rz_basename = self.process_integration_and_save_table_files(   node_id, 
                                                                                        self.rz_table, 
                                                                                        self.rz_filename, 
                                                                                        "rz", 
                                                                                        angular=True   )
 

            self.basenames = [  self.ux_basename, self.uy_basename, self.uz_basename, 
                                self.rx_basename, self.ry_basename, self.rz_basename  ]
            self.prescribed_dofs = [ux, uy, uz, rx, ry, rz]
            data = [self.prescribed_dofs, self.basenames]
                        
            if self.basenames == self.list_Nones:
                title = "Additional inputs required"
                message = "You must inform at least one prescribed dof\n"
                message += "table path before confirming the input!"
                PrintMessageInput([title, message, window_title]) 
                return 

            for basename in self.basenames:
                if basename in list_table_names:
                    list_table_names.remove(basename)
           
            self.project.set_prescribed_dofs_bc_by_node([node_id], data, True)

        self.process_table_file_removal(list_table_names)
        print(f"[Set Prescribed DOF] - defined at node(s) {self.nodes_typed}") 
        self.opv.updateRendererMesh()
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
        self.treeWidget_prescribed_dofs.clear()
        for node in self.project.preprocessor.nodes_with_prescribed_dofs:
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
        
        self.basenames = []
        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        key_strings = ["displacements", "rotations"]
        message = f"The prescribed dof(s) value(s) attributed to the {self.nodes_typed} node(s) \nhave been removed."

        remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
        self.remove_all_table_files_from_nodes(self.nodes_typed)
        data = [self.list_Nones, self.list_Nones]
        self.preprocessor.set_prescribed_dofs_bc_by_node(self.nodes_typed, data)
        self.opv.updateRendererMesh()
        self.load_nodes_info()
        self.close()
    
    def get_list_tables_names_from_selected_nodes(self, list_node_ids):
        table_names_from_nodes = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_prescribed_dofs:
                for table_name in node.prescribed_dofs_table_names:
                    if table_name is not None:
                        if table_name not in table_names_from_nodes:
                            table_names_from_nodes.append(table_name)
        return table_names_from_nodes
    
    def remove_all_table_files_from_nodes(self, list_node_ids):
        list_table_names = self.get_list_tables_names_from_selected_nodes(list_node_ids)
        self.process_table_file_removal(list_table_names)

    def reset_all(self):

        title = "Remove all prescribed dofs from structural model"
        message = "Do you really want to remove all prescribed dofs from the structural model?\n\n\n"
        message += "Press the Continue button to proceed with removal or press Cancel or Close buttons to abort the current operation."
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)


        if read._continue:
            self.basenames = []
            temp_list_nodes = self.preprocessor.nodes_with_prescribed_dofs.copy()
            self.nodes_typed = [node.external_index for node in temp_list_nodes]

            key_strings = ["displacements", "rotations"]
            message = None
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.remove_all_table_files_from_nodes(self.nodes_typed)
            data = [self.list_Nones, self.list_Nones]
            self.preprocessor.set_prescribed_dofs_bc_by_node(self.nodes_typed, data)

            self.opv.updateRendererMesh()
            self.load_nodes_info()
            self.close()

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="prescribed_dofs_files")

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
                lineEdit_real.setText("")
                lineEdit_imag.setText("")
            for lineEdit_table in self.list_lineEdit_table_values:
                lineEdit_table.setText("")
            self.inputs_from_node = False

    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.there_are_prescribed_dofs:
                self.reset_input_fields(force_reset=True)
                if node.loaded_table_for_prescribed_dofs:
                    table_names = node.prescribed_dofs_table_names
                    self.tabWidget_prescribed_dofs.setCurrentWidget(self.tab_table_values)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.prescribed_dofs_files_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    prescribed_dofs = node.prescribed_dofs
                    self.tabWidget_prescribed_dofs.setCurrentWidget(self.tab_constant_values)
                    for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                        if prescribed_dofs[index] is not None:
                            lineEdit_real.setText(str(np.real(prescribed_dofs[index])))
                            lineEdit_imag.setText(str(np.imag(prescribed_dofs[index])))
                self.inputs_from_node = True
            else:
                self.reset_input_fields()
            self.writeNodes(self.opv.getListPickedPoints())

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += f"{node}, "
        self.lineEdit_nodeID.setText(text[:-2])


    # def tables_frequency_setup_message(self, lineEdit, label):
    #     title = f"Invalid frequency setup of the '{label}' imported table"
    #     message = f"The frequency setup from '{label}' selected table mismatches\n"
    #     message += f"the frequency setup from previously imported tables.\n"
    #     message += f"All imported tables must have the same frequency\n"
    #     message += f"setup to avoid errors in the model processing."
    #     PrintMessageInput([title, message, window_title])
    #     lineEdit.setText("")
    #     lineEdit.setFocus()