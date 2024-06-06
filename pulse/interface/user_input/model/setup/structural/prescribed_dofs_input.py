
from PyQt5.QtWidgets import QComboBox, QDialog, QFileDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.tools.utils import remove_bc_from_file, get_new_path
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np
from math import pi

window_title = "Error"

class PrescribedDofsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/setup/structural/prescribed_dofs_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.update()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True

        self.preprocessor = self.project.preprocessor
        self.file = self.project.file
        self.before_run = self.project.get_pre_solution_model_checks()

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_filename = ""
        self.structural_bc_info_path = self.file._node_structural_path
        self.structural_folder_path = self.file._structural_imported_data_folder_path
        self.prescribed_dofs_files_folder_path = get_new_path(self.structural_folder_path, "prescribed_dofs_files")

        self.nodes = self.preprocessor.nodes
        self.prescribed_dofs = None
        self.inputs_from_node = False
        self.copy_path = False
        self.stop = False
        self.list_Nones = [None, None, None, None, None, None]
        self.dofs_labels = np.array(['Ux','Uy','Uz','Rx','Ry','Rz'])

        self.nodes_typed = list()
        self.basenames = list()
        self.list_frequencies = list()

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

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_linear_data_type : QComboBox
        self.comboBox_angular_data_type : QComboBox
        # QLineEdit
        self.lineEdit_nodeID : QLineEdit
        self.lineEdit_real_ux : QLineEdit
        self.lineEdit_real_uy : QLineEdit
        self.lineEdit_real_uz : QLineEdit
        self.lineEdit_real_rx : QLineEdit
        self.lineEdit_real_ry : QLineEdit
        self.lineEdit_real_rz : QLineEdit
        self.lineEdit_real_alldofs : QLineEdit
        #
        self.lineEdit_imag_ux : QLineEdit
        self.lineEdit_imag_uy : QLineEdit
        self.lineEdit_imag_uz : QLineEdit
        self.lineEdit_imag_rx : QLineEdit
        self.lineEdit_imag_ry : QLineEdit
        self.lineEdit_imag_rz : QLineEdit
        #
        self.lineEdit_imag_alldofs : QLineEdit
        self.lineEdit_path_table_ux : QLineEdit
        self.lineEdit_path_table_uy : QLineEdit
        self.lineEdit_path_table_uz : QLineEdit
        self.lineEdit_path_table_rx : QLineEdit
        self.lineEdit_path_table_ry : QLineEdit
        self.lineEdit_path_table_rz : QLineEdit
        self._create_list_lineEdits()
        # QPushButton
        self.pushButton_load_ux_table : QPushButton
        self.pushButton_load_uy_table : QPushButton
        self.pushButton_load_uz_table : QPushButton
        self.pushButton_load_rx_table : QPushButton
        self.pushButton_load_ry_table : QPushButton
        self.pushButton_load_rz_table : QPushButton
        self.pushButton_constant_value_confirm : QPushButton
        self.pushButton_remove_bc_confirm : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_table_values_confirm : QPushButton
        # QTabWidget
        self.tabWidget_prescribed_dofs : QTabWidget
        # QTreeWidget
        self.treeWidget_prescribed_dofs : QTreeWidget
        
    def _create_list_lineEdits(self):
        self.list_lineEdit_constant_values = [  [self.lineEdit_real_ux, self.lineEdit_imag_ux],
                                                [self.lineEdit_real_uy, self.lineEdit_imag_uy],
                                                [self.lineEdit_real_uz, self.lineEdit_imag_uz],
                                                [self.lineEdit_real_rx, self.lineEdit_imag_rx],
                                                [self.lineEdit_real_ry, self.lineEdit_imag_ry],
                                                [self.lineEdit_real_rz, self.lineEdit_imag_rz]  ]

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_ux,
                                            self.lineEdit_path_table_uy,
                                            self.lineEdit_path_table_uz,
                                            self.lineEdit_path_table_rx,
                                            self.lineEdit_path_table_ry,
                                            self.lineEdit_path_table_rz ]

    def _config_widgets(self):
        self.treeWidget_prescribed_dofs.setColumnWidth(0, 80)
        # self.treeWidget_prescribed_dofs.setColumnWidth(1, 60)
        #
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")   

    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)
        self.pushButton_load_ux_table.clicked.connect(self.load_ux_table)
        self.pushButton_load_uy_table.clicked.connect(self.load_uy_table)
        self.pushButton_load_uz_table.clicked.connect(self.load_uz_table)
        self.pushButton_load_rx_table.clicked.connect(self.load_rx_table)
        self.pushButton_load_ry_table.clicked.connect(self.load_ry_table)
        self.pushButton_load_rz_table.clicked.connect(self.load_rz_table)
        self.pushButton_reset.clicked.connect(self.reset_all)
        #
        self.treeWidget_prescribed_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_prescribed_dofs.itemDoubleClicked.connect(self.on_double_click_item)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title, title, message])
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
                PrintMessageInput([window_title, title, message])
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
            PrintMessageInput([window_title, title, message]) 

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
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([window_title, title, message])
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
            PrintMessageInput([window_title, title, message])
            lineEdit.setFocus()
            return None, None

    def process_integration_and_save_table_files(self, node_id, values, filename, dof_label, linear=False, angular=False):
        if self.frequencies[0]==0:
            self.frequencies[0] = float(1e-6)
        
        if linear:
            index_lin = self.comboBox_linear_data_type.currentIndex() 
            if index_lin == 0:
                values = values
                header = "OpenPulse - imported table for prescribed displacement {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m], imaginary[m], absolute[m]"
            elif index_lin == 1:
                values = values/(1j*2*pi*self.frequencies)
                header = "OpenPulse - imported table for prescribed velocity {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m/s], imaginary[m/s], absolute[m/s]"
            elif index_lin == 2:
                values = values/((1j*2*pi*self.frequencies)**2)
                header = "OpenPulse - imported table for prescribed acceleration {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[m/s²], imaginary[m/s²], absolute[m/s²]"
        
        if angular:
            index_ang = self.comboBox_angular_data_type.currentIndex() 
            if index_ang == 0:
                values = values
                header = "OpenPulse - imported table for prescribed angular displacement {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[rad], imaginary[rad], absolute[rad]"
            elif index_ang == 1:
                values = values/(1j*2*pi*self.frequencies)
                header = "OpenPulse - imported table for prescribed angular velocity {} @ node {} \n"
                header += f"\nSource filename: {filename}\n"
                header += "\nFrequency [Hz], real[rad/s], imaginary[rad/s], absolute[rad/s]"
            elif index_ang == 2:              
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
                message = "You must inform at least one prescribed dof "
                message += "table path before confirming the input!"
                PrintMessageInput([window_title, title, message]) 
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
        temp = self.dofs_labels[mask]

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
        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_prescribed_dofs) == 0:
            self.tabWidget_prescribed_dofs.setCurrentIndex(0)
            self.tabWidget_prescribed_dofs.setTabVisible(2, False)
        else:
            self.tabWidget_prescribed_dofs.setTabVisible(2, True)

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))

    def on_double_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.get_nodal_loads_info(item)

    def get_nodal_loads_info(self, item):
        try:

            data = dict()
            node = int(item.text(0))
            for node in self.preprocessor.nodes_with_prescribed_dofs:
                index = node.external_index
                if str(index) == item.text(0):
                    nodal_loads_mask = [False if bc is None else True for bc in node.prescribed_dofs]
                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.dofs_labels[i]
                            data[index, dof_label] = node.prescribed_dofs[i]

            if len(data):
                self.hide()
                header_labels = ["Node ID", "Dof label", "Value"]
                GetInformationOfGroup(  group_label = "Prescribed dof",
                                        selection_label = "Node ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
                                        data = data  )

        except Exception as error_log:
            title = "Error while gathering prescribed dofs information"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return

    def check_remove_bc_from_node(self):

        if  self.lineEdit_nodeID.text() != "":
        
            self.basenames = []
            lineEdit_nodeID = self.lineEdit_nodeID.text()
            self.stop, nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
            if self.stop:
                return

            key_strings = ["displacements", "rotations"]
            self.project.file.filter_bc_data_from_dat_file(nodes_typed, key_strings, self.structural_bc_info_path)
            self.remove_all_table_files_from_nodes(nodes_typed)
            data = [self.list_Nones, self.list_Nones]
            self.preprocessor.set_prescribed_dofs_bc_by_node(nodes_typed, data)
            self.opv.updateRendererMesh()
            self.load_nodes_info()
            # self.close()

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

        self.hide()

        title = "Resetting of prescribed dofs"
        message = "Would you like to remove all prescribed dofs from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            self.basenames = []
            temp_list_nodes = self.preprocessor.nodes_with_prescribed_dofs.copy()
            nodes_typed = [node.external_index for node in temp_list_nodes]

            key_strings = ["displacements", "rotations"]
            self.project.file.filter_bc_data_from_dat_file(nodes_typed, key_strings, self.structural_bc_info_path)
            self.remove_all_table_files_from_nodes(nodes_typed)
            data = [self.list_Nones, self.list_Nones]
            self.preprocessor.set_prescribed_dofs_bc_by_node(nodes_typed, data)

            self.close()
            self.opv.updateRendererMesh()

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
                    self.tabWidget_prescribed_dofs.setCurrentIndex(1)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.prescribed_dofs_files_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    prescribed_dofs = node.prescribed_dofs
                    self.tabWidget_prescribed_dofs.setCurrentIndex(0)
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
    #     PrintMessageInput([window_title, title, message])
    #     lineEdit.setText("")
    #     lineEdit.setFocus()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_prescribed_dofs.currentIndex()==0:
                self.check_constant_values()
            elif self.tabWidget_prescribed_dofs.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)