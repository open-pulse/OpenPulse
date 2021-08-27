import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

from pulse.utils import remove_bc_from_file, get_new_path
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

class LoadsInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/loadsInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.transform_points = opv.transformPoints

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()
        
        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""
        self.structural_bc_info_path = project.file._node_structural_path
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.nodal_loads_tables_folder_path = get_new_path(self.structural_folder_path, "nodal_loads_tables")

        self.nodes = project.preprocessor.nodes
        self.loads = None
        self.nodes_typed = []
        self.imported_table = False
        self.inputs_from_node = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_real_Fx = self.findChild(QLineEdit, 'lineEdit_real_Fx')
        self.lineEdit_real_Fy = self.findChild(QLineEdit, 'lineEdit_real_Fy')
        self.lineEdit_real_Fz = self.findChild(QLineEdit, 'lineEdit_real_Fz')
        self.lineEdit_real_Mx = self.findChild(QLineEdit, 'lineEdit_real_Mx')
        self.lineEdit_real_My = self.findChild(QLineEdit, 'lineEdit_real_My')
        self.lineEdit_real_Mz = self.findChild(QLineEdit, 'lineEdit_real_Mz')

        self.lineEdit_imag_Fx = self.findChild(QLineEdit, 'lineEdit_imag_Fx')
        self.lineEdit_imag_Fy = self.findChild(QLineEdit, 'lineEdit_imag_Fy')
        self.lineEdit_imag_Fz = self.findChild(QLineEdit, 'lineEdit_imag_Fz')
        self.lineEdit_imag_Mx = self.findChild(QLineEdit, 'lineEdit_imag_Mx')
        self.lineEdit_imag_My = self.findChild(QLineEdit, 'lineEdit_imag_My')
        self.lineEdit_imag_Mz = self.findChild(QLineEdit, 'lineEdit_imag_Mz')

        self.list_lineEdit_constant_values = [  [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
                                                [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
                                                [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
                                                [self.lineEdit_real_Mx, self.lineEdit_imag_Mx],
                                                [self.lineEdit_real_My, self.lineEdit_imag_My],
                                                [self.lineEdit_real_Mz, self.lineEdit_imag_Mz]  ]

        self.lineEdit_path_table_Fx = self.findChild(QLineEdit, 'lineEdit_path_table_Fx')
        self.lineEdit_path_table_Fy = self.findChild(QLineEdit, 'lineEdit_path_table_Fy')
        self.lineEdit_path_table_Fz = self.findChild(QLineEdit, 'lineEdit_path_table_Fz')
        self.lineEdit_path_table_Mx = self.findChild(QLineEdit, 'lineEdit_path_table_Mx')
        self.lineEdit_path_table_My = self.findChild(QLineEdit, 'lineEdit_path_table_My')
        self.lineEdit_path_table_Mz = self.findChild(QLineEdit, 'lineEdit_path_table_Mz')

        self.list_lineEdit_table_values = [ self.lineEdit_path_table_Fx,
                                            self.lineEdit_path_table_Fy,
                                            self.lineEdit_path_table_Fz,
                                            self.lineEdit_path_table_Mx,
                                            self.lineEdit_path_table_My,
                                            self.lineEdit_path_table_Mz ]

        self.toolButton_load_Fx_table = self.findChild(QToolButton, 'toolButton_load_Fx_table')
        self.toolButton_load_Fy_table = self.findChild(QToolButton, 'toolButton_load_Fy_table')
        self.toolButton_load_Fz_table = self.findChild(QToolButton, 'toolButton_load_Fz_table')
        self.toolButton_load_Mx_table = self.findChild(QToolButton, 'toolButton_load_Mx_table')
        self.toolButton_load_My_table = self.findChild(QToolButton, 'toolButton_load_My_table')
        self.toolButton_load_Mz_table = self.findChild(QToolButton, 'toolButton_load_Mz_table') 

        self.toolButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.toolButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.toolButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.toolButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.toolButton_load_My_table.clicked.connect(self.load_My_table)
        self.toolButton_load_Mz_table.clicked.connect(self.load_Mz_table)

        self.Fx_table = None
        self.Fy_table = None
        self.Fz_table = None
        self.Mx_table = None
        self.My_table = None
        self.Mz_table = None

        self.basename_Fx = None
        self.basename_Fy = None
        self.basename_Fz = None
        self.basename_Mx = None
        self.basename_My = None
        self.basename_Mz = None

        self.tabWidget_nodal_loads = self.findChild(QTabWidget, "tabWidget_nodal_loads")
        self.tab_constant_values = self.tabWidget_nodal_loads.findChild(QWidget, "tab_constant_values")
        self.tab_table = self.tabWidget_nodal_loads.findChild(QWidget, "tab_table")

        self.treeWidget_nodal_loads = self.findChild(QTreeWidget, 'treeWidget_nodal_loads')
        self.treeWidget_nodal_loads.setColumnWidth(0, 80)
        # self.treeWidget_nodal_loads.setColumnWidth(1, 60)
        self.treeWidget_nodal_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_loads.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton_constant_value_confirm = self.findChild(QPushButton, 'pushButton_constant_value_confirm')
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_bc_confirm_2 = self.findChild(QPushButton, 'pushButton_remove_bc_confirm_2')
        self.pushButton_remove_bc_confirm_2.clicked.connect(self.check_remove_bc_from_node)

        self.update()
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_nodal_loads.currentIndex()==0:
                self.check_constant_values()
            elif self.tabWidget_nodal_loads.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text[:-2])

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                window_title ="ERROR"
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return
        else:
            _real = None

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                window_title ="ERROR"
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return
        else:
            _imag = None
        
        if _real == 0 and _imag == 0:
            return None
        else:
            return _real + 1j*_imag

    def check_constant_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        Fx = self.check_complex_entries(self.lineEdit_real_Fx, self.lineEdit_imag_Fx, "Fx")
        if self.stop:
            return
        Fy = self.check_complex_entries(self.lineEdit_real_Fy, self.lineEdit_imag_Fy, "Fy")
        if self.stop:
            return        
        Fz = self.check_complex_entries(self.lineEdit_real_Fz, self.lineEdit_imag_Fz, "Fz")
        if self.stop:
            return        
        Mx = self.check_complex_entries(self.lineEdit_real_Mx, self.lineEdit_imag_Mx, "Mx")
        if self.stop:
            return        
        My = self.check_complex_entries(self.lineEdit_real_My, self.lineEdit_imag_My, "My")
        if self.stop:
            return        
        Mz = self.check_complex_entries(self.lineEdit_real_Mz, self.lineEdit_imag_Mz, "Mz")
        if self.stop:
            return

        loads = [Fx, Fy, Fz, Mx, My, Mz]
        
        if loads.count(None) != 6:
            self.loads = loads
            table_names = [None, None, None, None, None, None]
            data = [self.loads, table_names]
            self.project.set_loads_by_node(self.nodes_typed, data, False)
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            window_title ="ERROR"
            title = "Additional inputs required"
            message = "You must to inform at least one nodal load to confirm the input!"
            PrintMessageInput([title, message, window_title]) 
            
    def load_table(self, lineEdit, text, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the {} nodal load'.format(text)
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        lineEdit.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        self.project.create_folders_structural("nodal_loads_tables")
        self.new_load_path_table = get_new_path(self.nodal_loads_tables_folder_path, self.basename)

        try:                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as log_error:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = f" {str(log_error)} \n\nIt is recommended to skip the header rows."
            PrintMessageInput([title, message, window_title])
            return

        if imported_file.shape[1]<2:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = "The imported table has insufficient number of columns. The spectrum \n"
            message += "data must have frequencies, real and imaginary columns."
            PrintMessageInput([title, message, window_title])
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

        except Exception as log_error:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = f" {str(log_error)} \n\nIt is recommended to skip the header rows."
            PrintMessageInput([title, message, window_title])

        return self.imported_values, self.basename

    def load_Fx_table(self):
        header = "Fx || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fx_table, self.basename_Fx = self.load_table(self.lineEdit_path_table_Fx, "Fx", header)

    def load_Fy_table(self):
        header = "Fy || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fy_table, self.basename_Fy = self.load_table(self.lineEdit_path_table_Fy, "Fy", header)

    def load_Fz_table(self):
        header = "Fz || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fz_table, self.basename_Fz = self.load_table(self.lineEdit_path_table_Fz, "Fz", header)

    def load_Mx_table(self):
        header = "Mx || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.Mx_table, self.basename_Mx = self.load_table(self.lineEdit_path_table_Mx, "Mx", header)

    def load_My_table(self):
        header = "My || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.My_table, self.basename_My = self.load_table(self.lineEdit_path_table_My, "My", header)

    def load_Mz_table(self):
        header = "Mz || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.Mz_table, self.basename_Mz = self.load_table(self.lineEdit_path_table_Mz, "Mz", header)

    def check_table_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        Fx = Fy = Fz = None
        if self.lineEdit_path_table_Fx != "":
            if self.Fx_table is not None:
                Fx = self.Fx_table
        if self.lineEdit_path_table_Fy != "":
            if self.Fy_table is not None:
                Fy = self.Fy_table
        if self.lineEdit_path_table_Fz != "":
            if self.Fz_table is not None:
                Fz = self.Fz_table

        Mx = My = Mz = None
        if self.lineEdit_path_table_Mx != "":
            if self.Mx_table is not None:
                Mx = self.Mx_table
        if self.lineEdit_path_table_My != "":
            if self.My_table is not None:
                My = self.My_table
        if self.lineEdit_path_table_Mz != "":
            if self.Mz_table is not None:
                Mz = self.Mz_table

        self.basenames = [  self.basename_Fx, 
                            self.basename_Fy, 
                            self.basename_Fz, 
                            self.basename_Mx, 
                            self.basename_My, 
                            self.basename_Mz  ]
        self.loads = [Fx, Fy, Fz, Mx, My, Mz]
        data = [self.loads, self.basenames]
        self.project.set_loads_by_node(self.nodes_typed, data, True)
        self.transform_points(self.nodes_typed)
        self.close()

    def text_label(self, mask):
        
        text = ""
        load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
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
        self.treeWidget_nodal_loads.clear()
        for node in self.preprocessor.nodes_with_nodal_loads:
            nodal_loads_mask = [False if bc is None else True for bc in node.nodal_loads]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(nodal_loads_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)            
            self.treeWidget_nodal_loads.addTopLevelItem(new)

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
        key_strings = ["forces", "moments"]
        message = "The nodal loads attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
        self.remove_nodal_loads_table_files()
        self.preprocessor.set_structural_load_bc_by_node(self.nodes_typed, [None, None, None, None, None, None])
        self.transform_points(self.nodes_typed)
        self.load_nodes_info()
        self.close()

    def remove_nodal_loads_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_nodal_loads:
                list_table_names = node.nodal_loads_table_names
                self.confirm_table_file_removal(list_table_names, "Nodal loads")

    def confirm_table_file_removal(self, list_table_names, label):
        _list_table_names = []
        for table_name in list_table_names:
            if table_name is not None:
                if table_name not in _list_table_names:
                    _list_table_names.append(table_name)

        title = f"{label} - removal of imported table files"
        message = "Do you want to remove the following unused imported table \nfrom the project folder?\n\n"
        for _table_name in _list_table_names:
            message += f"{_table_name}\n"
        message += "\n\nPress the Continue button to proceed with removal or press Cancel or \nClose buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return

        if read._continue:
            for _table_name in _list_table_names:
                self.project.remove_structural_table_files_from_folder(_table_name, folder_name="nodal_loads_tables")
            # self.project.remove_structural_empty_folders(folder_name="lumped_elements_tables")   

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
            if node.there_are_nodal_loads:
                self.reset_input_fields(force_reset=True)
                if node.loaded_table_for_nodal_loads:
                    table_names = node.nodal_loads_table_names
                    self.tabWidget_nodal_loads.setCurrentWidget(self.tab_table_values)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.nodal_loads_tables_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    nodal_loads = node.nodal_loads
                    self.tabWidget_nodal_loads.setCurrentWidget(self.tab_constant_values)
                    for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                        if nodal_loads[index] is not None:
                            lineEdit_real.setText(str(np.real(nodal_loads[index])))
                            lineEdit_imag.setText(str(np.imag(nodal_loads[index])))
                self.inputs_from_node = True
            else:
                self.reset_input_fields()
            self.writeNodes(self.opv.getListPickedPoints())