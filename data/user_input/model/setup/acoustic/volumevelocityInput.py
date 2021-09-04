import os
import numpy as np
from PyQt5.QtWidgets import QToolButton, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QWidget, QTreeWidgetItem, QTreeWidget, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse.utils import get_new_path, remove_bc_from_file
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

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
        self.before_run = project.get_model_checks()

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.acoustic_bc_info_path = project.file._node_acoustic_path
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.volume_velocity_tables_folder_path = get_new_path(self.acoustic_folder_path, "volume_velocity_tables") 

        self.volume_velocity = None
        self.nodes_typed = []
        self.imported_table = False
        self.remove_volume_velocity = False
        self.inputs_from_node = False
        self.list_volume_velocity_table_names = []

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.lineEdit_volume_velocity_real = self.findChild(QLineEdit, 'lineEdit_volume_velocity_real')
        self.lineEdit_volume_velocity_imag = self.findChild(QLineEdit, 'lineEdit_volume_velocity_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')

        self.tabWidget_volume_velocity = self.findChild(QTabWidget, "tabWidget_volume_velocity")
        self.tabWidget_volume_velocity.currentChanged.connect(self.tabEvent_volume_velocity)
        self.current_tab =  self.tabWidget_volume_velocity.currentIndex()
        self.tab_constant_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_table_values")
        self.tab_remove = self.tabWidget_volume_velocity.findChild(QWidget, "tab_remove")

        self.treeWidget_volume_velocity = self.findChild(QTreeWidget, 'treeWidget_volume_velocity')
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)
        self.treeWidget_volume_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_volume_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.toolButton_load_table = self.findChild(QToolButton, 'toolButton_load_table')
        self.toolButton_load_table.clicked.connect(self.load_volume_velocity_table)

        self.pushButton_constant_value_confirm = self.findChild(QPushButton, 'pushButton_constant_value_confirm')
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.lineEdit_skiprows = self.findChild(QSpinBox, 'spinBox')

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.check_reset)
        
        self.update()
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_volume_velocity.currentIndex()==0:
                self.check_constant_values()
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
            self.lineEdit_nodeID.setText("")
            self.lineEdit_nodeID.setDisabled(True)
        else:
            self.lineEdit_nodeID.setDisabled(False)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                window_title ="ERROR"
                title = "Invalid entry to the volume velocity"
                message = "Wrong input for real part of volume velocity."
                PrintMessageInput([title, message, window_title])
                
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                window_title ="ERROR"
                title = "Invalid entry to the volume velocity"
                message = "Wrong input for imaginary part of volume velocity."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F

    def check_constant_values(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        volume_velocity = self.check_complex_entries(self.lineEdit_volume_velocity_real, self.lineEdit_volume_velocity_imag)
 
        if self.stop:
            return

        if volume_velocity is not None:
            self.volume_velocity = volume_velocity
            data = [self.volume_velocity, None]
            self.list_volume_velocity_table_names = self.get_volume_velocity_table_names_in_typed_nodes(self.nodes_typed)
            self.remove_volume_velocity_table_files(self.nodes_typed)
            self.project.set_volume_velocity_bc_by_node(self.nodes_typed, data, False)
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            window_title ="ERROR"
            title = "Additional inputs required"
            message = "You must to inform at least one volume velocity to confirm the input!"
            PrintMessageInput([title, message, window_title])
            
    def load_table(self, lineEdit, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the volume velocity'
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        lineEdit.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        self.project.create_folders_acoustic("volume_velocity_tables")
        self.new_load_path_table = get_new_path(self.volume_velocity_tables_folder_path, self.basename)

        try:
            skiprows = int(self.lineEdit_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
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
                data = [self.volume_velocity, self.basename_volume_velocity]
                self.list_volume_velocity_table_names = self.get_volume_velocity_table_names_in_typed_nodes(self.nodes_typed)
                self.remove_volume_velocity_table_files(self.nodes_typed)
                self.project.set_volume_velocity_bc_by_node(self.nodes_typed, data, True)
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
        self.treeWidget_volume_velocity.clear()
        for node in self.preprocessor.nodes_with_volume_velocity:
            # if node.compressor_connection_info is None:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.volume_velocity))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_volume_velocity.addTopLevelItem(new)
        self.update_tabs_visibility()

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.check_remove_bc_from_node()

    def get_volume_velocity_table_names_in_typed_nodes(self, list_node_ids):
        list_table_names = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.volume_velocity_table_name is not None:
                table_name = node.volume_velocity_table_name
                if table_name not in list_table_names:
                    list_table_names.append(table_name)
        return list_table_names

    def check_remove_bc_from_node(self):
        if self.lineEdit_nodeID.text() != "":
            picked_node_id = int(self.lineEdit_nodeID.text())
            node = self.preprocessor.nodes[picked_node_id]          
            if node in self.preprocessor.nodes_with_volume_velocity:            
                key_strings = ["volume velocity"]
                message = f"The volume velocity attributed to the {picked_node_id} node \nhas been removed."
                remove_bc_from_file([picked_node_id], self.acoustic_bc_info_path, key_strings, message)
                self.remove_volume_velocity_table_files([picked_node_id])
                self.preprocessor.set_volume_velocity_bc_by_node(picked_node_id, [None, None])
                self.transform_points(picked_node_id)
                self.load_nodes_info()
                # self.close()

    def remove_volume_velocity_table_files(self, list_node_ids):
        str_key = "volume velocity"
        folder_table_name = "volume_velocity_tables"
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.volume_velocity_table_name is not None:
                table_name = node.volume_velocity_table_name
                if self.project.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                        str_key,
                                                                                        table_name, 
                                                                                        folder_table_name   ):
                    self.confirm_table_file_removal(table_name, str_key.capitalize())   
            elif len(self.list_volume_velocity_table_names) > 0:
                for table_name in self.list_volume_velocity_table_names:
                    if self.project.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                            str_key, 
                                                                                            table_name,
                                                                                            folder_table_name   ):
                        self.confirm_table_file_removal(table_name, str_key.capitalize())  

    def confirm_table_file_removal(self, table_name, label):
        if table_name is not None:
            title = f"{label} - removal of imported table files"
            message = "Do you want to remove the following unused imported table \nfrom the project folder?\n\n"
            message += f"{table_name}\n"
            message += "\n\nPress the Continue button to proceed with removal or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            read = CallDoubleConfirmationInput(title, message)

            if read._doNotRun:
                return

            if read._continue:
                self.project.remove_acoustic_table_files_from_folder(table_name, "volume_velocity_tables")

    def check_reset(self):
        if len(self.preprocessor.nodes_with_volume_velocity)>0:
            # if len(self.preprocessor.nodes_with_volume_velocity)==1:
            #     node = self.preprocessor.nodes_with_volume_velocity[0]
            #     if node.compressor_connection_info is not None:
            #         return
            
            title = f"Resetting of all applied volume velocities"
            message = "Do you really want to remove the volume velocities \napplied to the following nodes?\n\n"
            for node in self.preprocessor.nodes_with_volume_velocity:
                # if node.compressor_connection_info is None:
                message += f"{node.external_index}\n"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Continue')

            if read._doNotRun:
                return

            _nodes_with_volume_velocity = self.preprocessor.nodes_with_volume_velocity.copy()
            if read._continue:
                for node in _nodes_with_volume_velocity:
                    # if node.compressor_connection_info is None:
                    node_id = node.external_index
                    key_strings = ["volume velocity"]
                    remove_bc_from_file([node_id], self.acoustic_bc_info_path, key_strings, None)
                    self.remove_volume_velocity_table_files([node_id])
                    self.preprocessor.set_volume_velocity_bc_by_node(node_id, [None, None])
                    self.transform_points(node_id)
                # self.load_nodes_info()

                window_title = "WARNING" 
                title = "Volume velocity resetting process complete"
                message = "All volume velocity applied to the acoustic\n" 
                message += "model have been removed from the model."
                PrintMessageInput([title, message, window_title])

                self.close()

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            self.lineEdit_volume_velocity_real.setText("")
            self.lineEdit_volume_velocity_imag.setText("")
            self.lineEdit_load_table_path.setText("")
            self.inputs_from_node = False

    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.volume_velocity is not None:
                self.reset_input_fields(force_reset=True)
                if node.volume_velocity_table_name is not None:
                    table_name = node.volume_velocity_table_name
                    self.tabWidget_volume_velocity.setCurrentWidget(self.tab_table_values)
                    table_name = get_new_path(self.volume_velocity_tables_folder_path, table_name)
                    self.lineEdit_load_table_path.setText(table_name)
                else:
                    volume_velocity = node.volume_velocity
                    self.tabWidget_volume_velocity.setCurrentWidget(self.tab_constant_values)
                    self.lineEdit_volume_velocity_real.setText(str(np.real(volume_velocity)))
                    self.lineEdit_volume_velocity_imag.setText(str(np.imag(volume_velocity)))
                self.inputs_from_node = True
            else:
                self.reset_input_fields()
            self.writeNodes(self.opv.getListPickedPoints())
        
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        if self.current_tab != 2:
            self.lineEdit_nodeID.setText(text[:-2])

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_volume_velocity) == 0:
            self.tabWidget_volume_velocity.setCurrentWidget(self.tab_constant_values)
            self.tab_remove.setDisabled(True)
        else:
            self.tab_remove.setDisabled(False)