from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.tools.utils import remove_bc_from_file, get_new_path
from pulse.interface.user_input.model.setup.general.get_information_of_group import GetInformationOfGroup
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os
import numpy as np

window_title = "Error"

class NodalLoadsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/external_nodal_loads_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
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
        self.nodal_loads_files_folder_path = get_new_path(self.structural_folder_path, "nodal_loads_files")

        self.nodes = self.preprocessor.nodes
        self.nodal_loads = None
        self.inputs_from_node = False
        self.copy_path = False

        self.list_Nones = [None, None, None, None, None, None]
        self.load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])

        self.nodes_typed = list()
        self.basenames = list()
        self.list_frequencies = list()

        self.Fx_table = None
        self.Fy_table = None
        self.Fz_table = None
        self.Mx_table = None
        self.My_table = None
        self.Mz_table = None

        self.Fx_filename = None
        self.Fy_filename = None
        self.Fz_filename = None
        self.Mx_filename = None
        self.My_filename = None
        self.Mz_filename = None

        self.Fx_basename = None
        self.Fy_basename = None
        self.Fz_basename = None
        self.Mx_basename = None
        self.My_basename = None
        self.Mz_basename = None

    def _define_qt_variables(self):

        # QLineEdit        
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_real_Fx : QLineEdit
        self.lineEdit_real_Fy : QLineEdit
        self.lineEdit_real_Fz : QLineEdit
        self.lineEdit_real_Mx : QLineEdit
        self.lineEdit_real_My : QLineEdit
        self.lineEdit_real_Mz : QLineEdit
        self.lineEdit_imag_Fx : QLineEdit
        self.lineEdit_imag_Fy : QLineEdit
        self.lineEdit_imag_Fz : QLineEdit
        self.lineEdit_imag_Mx : QLineEdit
        self.lineEdit_imag_My : QLineEdit
        self.lineEdit_imag_Mz : QLineEdit
        #
        self.lineEdit_path_table_Fx : QLineEdit
        self.lineEdit_path_table_Fy : QLineEdit
        self.lineEdit_path_table_Fz : QLineEdit
        self.lineEdit_path_table_Mx : QLineEdit
        self.lineEdit_path_table_My : QLineEdit
        self.lineEdit_path_table_Mz : QLineEdit
        self._create_list_lineEdits()

        # QPushButton
        self.pushButton_load_Fx_table : QPushButton
        self.pushButton_load_Fy_table : QPushButton
        self.pushButton_load_Fz_table : QPushButton
        self.pushButton_load_Mx_table : QPushButton
        self.pushButton_load_My_table : QPushButton
        self.pushButton_load_Mz_table : QPushButton
        self.pushButton_constant_value_confirm : QPushButton
        self.pushButton_table_values_confirm : QPushButton
        self.pushButton_remove_bc_confirm : QPushButton
        self.pushButton_reset : QPushButton

        # QTabWidget
        self.tabWidget_nodal_loads : QTabWidget

        # QTreeWidget
        self.treeWidget_nodal_loads : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.pushButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.pushButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.pushButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.pushButton_load_My_table.clicked.connect(self.load_My_table)
        self.pushButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_node)
        self.pushButton_reset.clicked.connect(self.reset_all)
        #
        self.tabWidget_nodal_loads.currentChanged.connect(self.tabWidget_selection_event)
        #
        self.treeWidget_nodal_loads.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_loads.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selection_id.setText(text)
            self.process_selection(selected_nodes)

    def process_selection(self, selected_nodes : list):
        if selected_nodes:
            picked_node = selected_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.there_are_nodal_loads:
                self.reset_input_fields(force_reset=True)
                if node.loaded_table_for_nodal_loads:
                    table_names = node.nodal_loads_table_names
                    self.tabWidget_nodal_loads.setCurrentIndex(1)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.nodal_loads_files_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    nodal_loads = node.nodal_loads
                    self.tabWidget_nodal_loads.setCurrentIndex(0)
                    for index, [lineEdit_real, lineEdit_imag] in enumerate(self.list_lineEdit_constant_values):
                        if nodal_loads[index] is not None:
                            lineEdit_real.setText(str(np.real(nodal_loads[index])))
                            lineEdit_imag.setText(str(np.imag(nodal_loads[index])))
                self.inputs_from_node = True
            else:
                self.reset_input_fields()

    def _create_list_lineEdits(self):   
        self.list_lineEdit_constant_values = [  [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
                                                [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
                                                [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
                                                [self.lineEdit_real_Mx, self.lineEdit_imag_Mx],
                                                [self.lineEdit_real_My, self.lineEdit_imag_My],
                                                [self.lineEdit_real_Mz, self.lineEdit_imag_Mz]  ]
        
        self.list_lineEdit_table_values = [ self.lineEdit_path_table_Fx,
                                            self.lineEdit_path_table_Fy,
                                            self.lineEdit_path_table_Fz,
                                            self.lineEdit_path_table_Mx,
                                            self.lineEdit_path_table_My,
                                            self.lineEdit_path_table_Mz ]
    
    def _config_widgets(self):
        self.treeWidget_nodal_loads.setColumnWidth(0, 80)
        # self.treeWidget_nodal_loads.setColumnWidth(1, 60)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")   

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([window_title, title, message])
                stop = True
                return
        else:
            _real = 0

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([window_title, title, message])
                stop = True
                return
        else:
            _imag = 0
        
        if _real == 0 and _imag == 0:
            return stop, None
        else:
            return stop, _real + 1j*_imag

    def check_constant_values(self):

        str_nodes = self.lineEdit_selection_id.text()
        stop, self.nodes_typed = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return

        stop, Fx = self.check_complex_entries(self.lineEdit_real_Fx, self.lineEdit_imag_Fx, "Fx")
        if stop:
            return

        stop, Fy = self.check_complex_entries(self.lineEdit_real_Fy, self.lineEdit_imag_Fy, "Fy")
        if stop:
            return
 
        stop, Fz = self.check_complex_entries(self.lineEdit_real_Fz, self.lineEdit_imag_Fz, "Fz")
        if stop:
            return

        stop, Mx = self.check_complex_entries(self.lineEdit_real_Mx, self.lineEdit_imag_Mx, "Mx")
        if stop:
            return

        stop, My = self.check_complex_entries(self.lineEdit_real_My, self.lineEdit_imag_My, "My")
        if stop:
            return

        stop, Mz = self.check_complex_entries(self.lineEdit_real_Mz, self.lineEdit_imag_Mz, "Mz")
        if stop:
            return

        nodal_loads = [Fx, Fy, Fz, Mx, My, Mz]
        
        if nodal_loads.count(None) != 6:
            self.nodal_loads = nodal_loads
            table_names = self.list_Nones
            data = [self.nodal_loads, table_names]
            self.remove_all_table_files_from_nodes(self.nodes_typed)
            self.project.set_nodal_loads_by_node(self.nodes_typed, data, False)

            app().main_window.update_plots()
            self.close()

            print(f"[Set Nodal loads] - defined at node(s) {self.nodes_typed}")

        else:    
    
            title = "Additional inputs required"
            message = "You must to inform at least one nodal load " 
            message += "before confirming the input!"
            PrintMessageInput([window_title, title, message]) 
            
    def load_table(self, lineEdit, load_label, direct_load=False):
        title = "Error reached while loading table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the {} nodal load'.format(load_label)
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None
            
            self.imported_filename  = os.path.basename(self.path_imported_table)
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
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
            
            return self.imported_values, self.imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title, title, message])
            lineEdit.setFocus()
            return None, None

    def load_Fx_table(self):
        self.Fx_table, self.Fx_filename = self.load_table(self.lineEdit_path_table_Fx, "Fx")
        if (self.Fx_table, self.Fx_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Fx)

    def load_Fy_table(self):
        self.Fy_table, self.Fy_filename = self.load_table(self.lineEdit_path_table_Fy, "Fy")
        if (self.Fy_table, self.Fy_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Fy)

    def load_Fz_table(self):
        self.Fz_table, self.Fz_filename = self.load_table(self.lineEdit_path_table_Fz, "Fz")
        if (self.Fz_table, self.Fz_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Fz)

    def load_Mx_table(self):
        self.Mx_table, self.Mx_filename = self.load_table(self.lineEdit_path_table_Mx, "Mx")
        if (self.Mx_table, self.Mx_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Mx)

    def load_My_table(self):
        self.My_table, self.My_filename = self.load_table(self.lineEdit_path_table_My, "My")
        if (self.My_table, self.My_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_My)

    def load_Mz_table(self):
        self.Mz_table, self.Mz_filename = self.load_table(self.lineEdit_path_table_Mz, "Mz")
        if (self.Mz_table, self.Mz_filename).count(None) == 2:
            self.lineEdit_reset(self.lineEdit_path_table_Mz)

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_tables_files(self, node_id, values, filename, load_label):

        real_values = np.real(values)
        imag_values = np.imag(values)
        abs_values = np.abs(values)
        data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
        self.project.create_folders_structural("nodal_loads_files")

        if load_label in ["Fx", "Fy", "Fz"]:
            header = f"OpenPulse - imported table for {load_label} nodal force @ node {node_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[N], imaginary[N], absolute[N]"
        else:
            header = f"OpenPulse - imported table for {load_label} nodal moment @ node {node_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        
        basename = f"nodal_load_{load_label}_node_{node_id}.dat"
    
        new_path_table = get_new_path(self.nodal_loads_files_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def check_table_values(self):

        str_nodes = self.lineEdit_selection_id.text()
        stop, self.nodes_typed = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return

        list_table_names = self.get_table_names_from_selected_nodes(self.nodes_typed)

        for node_id in self.nodes_typed:
            Fx = Fy = Fz = None
            
            if self.lineEdit_path_table_Fx.text() != "":
                if self.Fx_table is None:
                    if self.Fx_filename is None:
                        self.Fx_table, self.Fx_filename = self.load_table(self.lineEdit_path_table_Fx, "Fx", direct_load=True)
                if self.Fx_table is not None:
                    Fx, self.Fx_basename = self.save_tables_files(node_id, self.Fx_table, self.Fx_filename, "Fx")
            
            if self.lineEdit_path_table_Fy.text() != "":
                if self.Fy_table is None:
                    if self.Fy_filename is None:
                        self.Fy_table, self.Fy_filename = self.load_table(self.lineEdit_path_table_Fy, "Fy", direct_load=True)
                if self.Fy_table is not None:
                    Fy, self.Fy_basename = self.save_tables_files(node_id, self.Fy_table, self.Fy_filename, "Fy")
            
            if self.lineEdit_path_table_Fz.text() != "":
                if self.Fz_table is None:
                    if self.Fz_filename is None:
                        self.Fz_table, self.Fz_filename = self.load_table(self.lineEdit_path_table_Fz, "Fz", direct_load=True)           
                if self.Fz_table is not None:
                    Fz, self.Fz_basename = self.save_tables_files(node_id, self.Fz_table, self.Fz_filename, "Fz")
            
            Mx = My = Mz = None
            if self.lineEdit_path_table_Mx.text() != "":
                if self.Mx_table is None:
                    if self.Mx_filename is None:
                        self.Mx_table, self.Mx_filename = self.load_table(self.lineEdit_path_table_Mx, "Mx", direct_load=True)            
                if self.Mx_table is not None:
                    Mx, self.Mx_basename = self.save_tables_files(node_id, self.Mx_table, self.Mx_filename, "Mx")
            
            if self.lineEdit_path_table_My.text() != "":
                if self.My_table is None:
                    if self.My_filename is None:
                        self.My_table, self.My_filename = self.load_table(self.lineEdit_path_table_My, "My", direct_load=True)             
                if self.My_table is not None:
                    My, self.My_basename = self.save_tables_files(node_id, self.My_table, self.My_filename, "My")
            
            if self.lineEdit_path_table_Mz.text() != "":
                if self.Mz_table is None:
                    if self.Mz_filename is None:
                        self.Mz_table, self.Mz_filename = self.load_table(self.lineEdit_path_table_Mz, "Mz", direct_load=True)              
                if self.Mz_table is not None:
                    Mz, self.Mz_basename = self.save_tables_files(node_id, self.Mz_table, self.Mz_filename, "Mz")

            self.basenames = [  self.Fx_basename, self.Fy_basename, self.Fz_basename, 
                                self.Mx_basename, self.My_basename, self.Mz_basename  ]
            self.nodal_loads = [Fx, Fy, Fz, Mx, My, Mz]
            data = [self.nodal_loads, self.basenames]
                        
            if self.basenames == self.list_Nones:
                title = "Additional inputs required"
                message = "You must inform at least one nodal load "
                message += "table path before confirming the input!"
                PrintMessageInput([window_title, title, message]) 
                return 

            for basename in self.basenames:
                if basename in list_table_names:
                    list_table_names.remove(basename)

            self.project.set_nodal_loads_by_node([node_id], data, True)

        self.process_table_file_removal(list_table_names)

        app().main_window.update_plots()
        self.close()

        print(f"[Set Nodal loads] - defined at node(s) {self.nodes_typed}")

    def text_label(self, mask):

        text = ""
        temp = self.load_labels[mask]

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
        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_nodal_loads) == 0:
            self.tabWidget_nodal_loads.setCurrentIndex(0)
            self.tabWidget_nodal_loads.setTabVisible(2, False)
        else:
            self.tabWidget_nodal_loads.setTabVisible(2, True)

    def tabWidget_selection_event(self):
        self.pushButton_remove_bc_confirm.setDisabled(True)
        if self.tabWidget_nodal_loads.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)
            self.selection_callback()

    def on_click_item(self, item):
        self.pushButton_remove_bc_confirm.setDisabled(False)
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        # self.on_click_item(item)
        self.lineEdit_selection_id.setText(item.text(0))
        self.get_nodal_loads_info(item)

    def get_nodal_loads_info(self, item):
        try:

            data = dict()
            node = int(item.text(0))
            for node in self.preprocessor.nodes_with_nodal_loads:
                index = node.external_index
                if str(index) == item.text(0):
                    nodal_loads_mask = [False if bc is None else True for bc in node.nodal_loads]
                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.load_labels[i]
                            data[index, dof_label] = node.nodal_loads[i]

            if len(data):
                self.close()
                header_labels = ["Node ID", "Load label", "Value"]
                GetInformationOfGroup(  group_label = "Structural nodal load",
                                        selection_label = "Node ID:",
                                        header_labels = header_labels,
                                        column_widths = [70, 140, 150],
                                        data = data  )

        except Exception as error_log:
            title = "Error while gathering nodal load information"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            return
        
        self.show()
            
    def remove_bc_from_node(self):

        if  self.lineEdit_selection_id.text() != "":

            str_nodes = self.lineEdit_selection_id.text()
            stop, nodes_typed = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            key_strings = ["forces", "moments"]
            self.project.file.filter_bc_data_from_dat_file(nodes_typed, key_strings, self.structural_bc_info_path)
            self.remove_all_table_files_from_nodes(nodes_typed)
            data = [self.list_Nones, self.list_Nones]
            self.preprocessor.set_structural_load_bc_by_node(nodes_typed, data)

            self.lineEdit_selection_id.setText("")
            self.pushButton_remove_bc_confirm.setDisabled(True)
            self.load_nodes_info()

            app().main_window.update_plots()
            # self.close()

    def get_table_names_from_selected_nodes(self, list_node_ids):
        table_names_from_nodes = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_nodal_loads:
                for table_name in node.nodal_loads_table_names:
                    if table_name is not None:
                        if table_name not in table_names_from_nodes:
                            table_names_from_nodes.append(table_name)
        return table_names_from_nodes
    
    def remove_all_table_files_from_nodes(self, list_node_ids):
        list_table_names = self.get_table_names_from_selected_nodes(list_node_ids)
        self.process_table_file_removal(list_table_names)    

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="nodal_loads_files")

    def reset_all(self):

        self.hide()

        title = "Resetting of nodal loads"
        message = "Would you like to remove all nodal loads from the structural model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.basenames = list()
            temp_list_nodes = self.preprocessor.nodes_with_nodal_loads.copy()
            nodes_typed = [node.external_index for node in temp_list_nodes]

            key_strings = ["forces", "moments"]
            self.project.file.filter_bc_data_from_dat_file(nodes_typed, key_strings, self.structural_bc_info_path)

            self.remove_all_table_files_from_nodes(nodes_typed)
            data = [self.list_Nones, self.list_Nones]
            self.preprocessor.set_structural_load_bc_by_node(nodes_typed, data)

            app().main_window.update_plots()
            self.close()

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
                lineEdit_real.setText("")
                lineEdit_imag.setText("")
            for lineEdit_table in self.list_lineEdit_table_values:
                lineEdit_table.setText("")
            self.inputs_from_node = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_nodal_loads.currentIndex()==0:
                self.check_constant_values()
            elif self.tabWidget_nodal_loads.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Escape:
            self.close()

    # def tables_frequency_setup_message(self, lineEdit, label):
    #     title = f"Invalid frequency setup of the '{label}' imported table"
    #     message = f"The frequency setup from '{label}' selected table mismatches\n"
    #     message += f"the frequency setup from previously imported tables.\n"
    #     message += f"All imported tables must have the same frequency\n"
    #     message += f"setup to avoid errors in the model processing."
    #     PrintMessageInput([window_title, title, message])
    #     lineEdit.setText("")
    #     lineEdit.setFocus()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)