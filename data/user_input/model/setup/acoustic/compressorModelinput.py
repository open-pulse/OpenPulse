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
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class CompressorModelInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/compressorModelInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.node_id = self.opv.getListPickedPoints()

        self.project = project
        self.mesh = project.mesh
        self.nodes = self.mesh.nodes
        self.before_run = self.mesh.get_model_checks()    

        self.project_folder_path = project.file._project_path      
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        
        self.lineEdit_selected_node_ID = self.findChild(QLineEdit, 'lineEdit_selected_node_ID')
        self.lineEdit_suction_node_ID = self.findChild(QLineEdit, 'lineEdit_suction_node_ID')
        self.lineEdit_discharge_node_ID = self.findChild(QLineEdit, 'lineEdit_discharge_node_ID')

        self.lineEdit_frequency_resolution = self.findChild(QLineEdit, 'lineEdit_frequency_resolution')
        self.lineEdit_number_of_revolutions = self.findChild(QLineEdit, 'lineEdit_number_of_revolutions')

        self.lineEdit_bore_diameter = self.findChild(QLineEdit, 'lineEdit_bore_diameter')
        self.lineEdit_stroke = self.findChild(QLineEdit, 'lineEdit_stroke')
        self.lineEdit_connecting_rod_length = self.findChild(QLineEdit, 'lineEdit_connecting_rod_length')
        self.lineEdit_rod_diameter = self.findChild(QLineEdit, 'lineEdit_rod_diameter')

        self.lineEdit_pressure_ratio = self.findChild(QLineEdit, 'lineEdit_pressure_ratio')
        self.lineEdit_clearance = self.findChild(QLineEdit, 'lineEdit_clearance')
        self.lineEdit_TDC_crank_angle_1 = self.findChild(QLineEdit, 'lineEdit_TDC_crank_angle_1')
        self.lineEdit_TDC_crank_angle_2 = self.findChild(QLineEdit, 'lineEdit_TDC_crank_angle_2')
        self.lineEdit_number_of_pistons = self.findChild(QLineEdit, 'lineEdit_number_of_pistons')
        self.lineEdit_rotational_speed = self.findChild(QLineEdit, 'lineEdit_rotational_speed')
        self.lineEdit_capacity = self.findChild(QLineEdit, 'lineEdit_capacity')
        self.lineEdit_isentropic_coefficient = self.findChild(QLineEdit, 'lineEdit_isentropic_coefficient')
        self.lineEdit_molar_mass = self.findChild(QLineEdit, 'lineEdit_molar_mass')
        self.lineEdit_pressure_at_suction = self.findChild(QLineEdit, 'lineEdit_pressure_at_suction')
        self.lineEdit_temperature_at_suction = self.findChild(QLineEdit, 'lineEdit_temperature_at_suction')

        self.radioButton_both_cylinders = self.findChild(QRadioButton, 'radioButton_both_cylinders')
        self.radioButton_head_end_cylinder = self.findChild(QRadioButton, 'radioButton_head_end_cylinder')
        self.radioButton_crank_end_cylinder = self.findChild(QRadioButton, 'radioButton_crank_end_cylinder')

        self.radioButton_both_cylinders.clicked.connect(self.radioButtonEvent_compression_setup)
        self.radioButton_head_end_cylinder.clicked.connect(self.radioButtonEvent_compression_setup)
        self.radioButton_crank_end_cylinder.clicked.connect(self.radioButtonEvent_compression_setup)

        self.radioButton_connected_at_suction_and_discharge = self.findChild(QRadioButton, 'radioButton_connected_at_suction_and_discharge')
        self.radioButton_connected_at_suction = self.findChild(QRadioButton, 'radioButton_connected_at_suction')
        self.radioButton_connected_at_discharge = self.findChild(QRadioButton, 'radioButton_connected_at_discharge')

        self.radioButton_connected_at_suction_and_discharge.clicked.connect(self.radioButtonEvent_connections_compressor_to_pipelines)
        self.radioButton_connected_at_suction.clicked.connect(self.radioButtonEvent_connections_compressor_to_pipelines)
        self.radioButton_connected_at_discharge.clicked.connect(self.radioButtonEvent_connections_compressor_to_pipelines)
        self.connection_at_suction_and_discharge = self.radioButton_connected_at_suction_and_discharge.isChecked()

        self.radioButtonEvent_compression_setup()
        self.radioButtonEvent_connections_compressor_to_pipelines()

        self.comboBox_frequency_resolution = self.findChild(QComboBox, 'comboBox_frequency_resolution')
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)

        self.comboBox_stage = self.findChild(QComboBox, 'comboBox_stage')
        self.comboBox_stage.currentIndexChanged.connect(self.comboBox_event_stage)
        self.comboBox_event_stage()

        self.spinBox_number_of_points = self.findChild(QSpinBox, 'spinBox_number_of_points')
        self.spinBox_number_of_points.valueChanged.connect(self.spinBox_event_number_of_points)

        self.spinBox_max_frequency = self.findChild(QSpinBox, 'spinBox_max_frequency')
        self.spinBox_max_frequency.valueChanged.connect(self.spinBox_event_max_frequency)

        self.spinBox_number_of_cylinders = self.findChild(QSpinBox, 'spinBox_number_of_cylinders')
        self.spinBox_number_of_cylinders.valueChanged.connect(self.spinBox_event_number_of_cylinders)

        self.pushButton_flipNodes = self.findChild(QPushButton, 'pushButton_flipNodes')
        self.pushButton_flipNodes.clicked.connect(self.flip_nodes)

        self.pushButton_plot_PV_diagram_head_end = self.findChild(QPushButton, 'pushButton_plot_PV_diagram_head_end')
        self.pushButton_plot_PV_diagram_head_end.clicked.connect(self.plot_PV_diagram_head_end)

        self.pushButton_plot_PV_diagram_crank_end = self.findChild(QPushButton, 'pushButton_plot_PV_diagram_crank_end')
        self.pushButton_plot_PV_diagram_crank_end.clicked.connect(self.plot_PV_diagram_crank_end)

        self.pushButton_plot_volumetric_flow_rate_at_suction_time = self.findChild(QPushButton, 'pushButton_plot_volumetric_flow_rate_at_suction_time')
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.clicked.connect(self.plot_volumetric_flow_rate_at_suction_time)

        self.pushButton_plot_volumetric_flow_rate_at_discharge_time = self.findChild(QPushButton, 'pushButton_plot_volumetric_flow_rate_at_discharge_time')
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_time)

        self.pushButton_plot_rod_pressure_load_frequency = self.findChild(QPushButton, 'pushButton_plot_rod_pressure_load_frequency')
        self.pushButton_plot_rod_pressure_load_frequency.clicked.connect(self.plot_rod_pressure_load_frequency)

        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency = self.findChild(QPushButton, 'pushButton_plot_volumetric_flow_rate_at_suction_frequency')
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_suction_frequency)

        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency = self.findChild(QPushButton, 'pushButton_plot_volumetric_flow_rate_at_discharge_frequency')
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_frequency)

        self.pushButton_plot_pressure_head_end_angle = self.findChild(QPushButton, 'pushButton_plot_pressure_head_end_angle')
        self.pushButton_plot_pressure_head_end_angle.clicked.connect(self.plot_pressure_head_end_angle)

        self.pushButton_plot_volume_head_end_angle = self.findChild(QPushButton, 'pushButton_plot_volume_head_end_angle')
        self.pushButton_plot_volume_head_end_angle.clicked.connect(self.plot_volume_head_end_angle)

        self.pushButton_plot_pressure_crank_end_angle = self.findChild(QPushButton, 'pushButton_plot_pressure_crank_end_angle')
        self.pushButton_plot_pressure_crank_end_angle.clicked.connect(self.plot_pressure_crank_end_angle)

        self.pushButton_plot_volume_crank_end_angle = self.findChild(QPushButton, 'pushButton_plot_volume_crank_end_angle')
        self.pushButton_plot_volume_crank_end_angle.clicked.connect(self.plot_volume_crank_end_angle)

        self.pushButton_process_aquisition_parameters = self.findChild(QPushButton, 'pushButton_process_aquisition_parameters')
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.process_all_inputs)

        self.pushButton_remove_table = self.findChild(QPushButton, 'pushButton_remove_table')
        self.pushButton_remove_table.clicked.connect(self.remove_table)

        self.pushButton_reset_node = self.findChild(QPushButton, 'pushButton_reset_node')
        self.pushButton_reset_node.clicked.connect(self.reset_node)

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.tabWidget_compressor = self.findChild(QTabWidget, 'tabWidget_compressor')
        self.tabWidget_compressor.currentChanged.connect(self.tabEvent)

        self.treeWidget_compressor_excitation = self.findChild(QTreeWidget, 'treeWidget_compressor_excitation')
        self.treeWidget_compressor_excitation.setColumnWidth(0, 90)
        self.treeWidget_compressor_excitation.setColumnWidth(1, 140)
        self.treeWidget_compressor_excitation.itemClicked.connect(self.on_click_item)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.lineEdit_node_ID_info = self.findChild(QLineEdit, 'lineEdit_node_ID_info')
        self.lineEdit_table_name_info = self.findChild(QLineEdit, 'lineEdit_table_name_info')

        self.writeNodes(self.opv.getListPickedPoints())
        self.spinBox_event_number_of_cylinders()
        self.load_volume_velocity_tables_info()
        
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.process_all_inputs()
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
            self.close()

    def tabEvent(self):
        self.current_tab_index = self.tabWidget_compressor.currentIndex()
        if self.current_tab_index == 3:
            self.pushButton_confirm.setDisabled(True)
        else:
            self.pushButton_confirm.setDisabled(False)
    
    def flip_nodes(self):
        if self.connection_at_suction_and_discharge:
            temp_text_suction = self.lineEdit_suction_node_ID.text()
            temp_text_discharge = self.lineEdit_discharge_node_ID.text()
            self.lineEdit_suction_node_ID.setText(temp_text_discharge)
            self.lineEdit_discharge_node_ID.setText(temp_text_suction)   

    def update_compressing_cylinders_setup(self):
        self.both_cylinders = self.radioButton_both_cylinders.isChecked()
        self.head_end_cylinder = self.radioButton_head_end_cylinder.isChecked()
        self.crank_end_cylinder = self.radioButton_crank_end_cylinder.isChecked()

        self.single_acting = False
        self.double_acting = False
        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.both_cylinders:
            self.double_acting = True

        if self.head_end_cylinder:
            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)
            self.single_acting = True

        if self.crank_end_cylinder:
            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)
            self.single_acting = True

    def radioButtonEvent_compression_setup(self):
        self.update_compressing_cylinders_setup()

    def radioButtonEvent_connections_compressor_to_pipelines(self):
        self.connection_at_suction_and_discharge = self.radioButton_connected_at_suction_and_discharge.isChecked()
        self.connection_at_suction = self.radioButton_connected_at_suction.isChecked()
        self.connection_at_discharge = self.radioButton_connected_at_discharge.isChecked()

        self.lineEdit_suction_node_ID.setDisabled(False)
        self.lineEdit_discharge_node_ID.setDisabled(False)       

        list_node_ids = self.opv.getListPickedPoints()

        if self.connection_at_suction:
            self.lineEdit_discharge_node_ID.setDisabled(True)
            self.lineEdit_discharge_node_ID.setText("")
            if len(list_node_ids) == 1:
                self.lineEdit_suction_node_ID.setText(str(list_node_ids[-1]))
        elif self.connection_at_discharge:
            self.lineEdit_suction_node_ID.setDisabled(True)
            self.lineEdit_suction_node_ID.setText("")
            if len(list_node_ids) == 1:
                self.lineEdit_discharge_node_ID.setText(str(list_node_ids[-1]))
        else:
            self.writeNodes(list_node_ids)
            
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_selected_node_ID.setText(text)
        if len(list_node_ids) == 2:
            self.lineEdit_suction_node_ID.setText(str(min(list_node_ids[-2:])))
            self.lineEdit_discharge_node_ID.setText(str(max(list_node_ids[-2:])))
        elif len(list_node_ids) == 1:
            self.lineEdit_suction_node_ID.setText(str(list_node_ids[-1]))
            self.lineEdit_discharge_node_ID.setText("")

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())

    def check_nodeID(self, lineEdit, export=False):
        
        lineEdit_nodeID = lineEdit.text()
        self.stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        
        if self.stop:
            return True

        if len(self.project.mesh.neighboor_elements_of_node(self.node_ID))>1:
            title = "INVALID SELECTION - NODE {}".format(self.node_ID)
            message = "The selected NODE ID must be in the beginning \nor termination of the pipelines."
            PrintMessageInput([title, message, window_title1])
            return True
              
    def check_all_nodes(self, check_nodes=True):
        
        if check_nodes:
            if self.connection_at_suction_and_discharge:

                if self.check_nodeID(self.lineEdit_suction_node_ID):
                    return True

                self.suction_node_ID = self.node_ID
                
                if self.check_nodeID(self.lineEdit_discharge_node_ID):
                    return True

                self.discharge_node_ID = self.node_ID

                if self.suction_node_ID == self.discharge_node_ID:
                    title = "ERROR IN NODES SELECTION"
                    message = "The nodes selected to the suction and discharge must differ. Try to choose another pair of nodes."
                    PrintMessageInput([title, message, window_title1])
                    return True

            if self.connection_at_suction:
                if self.check_nodeID(self.lineEdit_suction_node_ID):
                    return True
              
                self.suction_node_ID = self.node_ID

            if self.connection_at_discharge:
                if self.check_nodeID(self.lineEdit_discharge_node_ID):
                    return True

                self.discharge_node_ID = self.node_ID

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

    def check_all_parameters(self):
        self.parameters = {}

        if self.check_input_parameters(self.lineEdit_bore_diameter, "BORE DIAMETER"):
            return True
        else:
            self.parameters['bore diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_stroke, "STROKE"):
            return True
        else:
            self.parameters['stroke'] = self.value

        if self.check_input_parameters(self.lineEdit_connecting_rod_length, "CONNECTING ROD LENGTH"):
            return True
        else:
            self.parameters['connecting rod length'] = self.value

        if self.check_input_parameters(self.lineEdit_rod_diameter, "ROD DIAMETER"):
            return True
        else:
            self.parameters['rod diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_ratio, "PRESSURE RATIO"):
            return True
        else:
            self.parameters['pressure ratio'] = self.value
    
        if self.check_input_parameters(self.lineEdit_clearance, "CLEARANCE"):
            return True
        else:
            self.parameters['clearance'] = self.value
    
        if self.check_input_parameters(self.lineEdit_TDC_crank_angle_1, "TOP DEAD CENTER CRANCK ANGLE 1"):
            return True
        else:
            self.parameters['TDC crank angle 1'] = self.value

        if self.check_input_parameters(self.lineEdit_rotational_speed, "ROTATIONAL SPEED"):
            return True
        else:
            self.parameters['rotational speed'] = self.value

        if self.check_input_parameters(self.lineEdit_capacity, "CAPACITY"):
            return True
        elif self.value<10:
            title = "INVALID INPUT VALUE TO THE STAGE CAPACITY"
            message = "The compressor stage capacity value must be greater or equals to 10%."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            self.parameters['capacity'] = self.value

        if self.check_input_parameters(self.lineEdit_molar_mass, "MOLAR MASS"):
            return True
        else:
            self.parameters['molar mass'] = self.value

        if self.check_input_parameters(self.lineEdit_isentropic_coefficient, "ISENTROPIC COEFFICIENT"):
            return True
        else:
            self.parameters['isentropic coefficient'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_at_suction, "PRESSURE AT SUCTION"):
            return True
        else:
            self.parameters['pressure at suction'] = self.value

        if self.check_input_parameters(self.lineEdit_temperature_at_suction, "TEMPERATURE AT SUCTION"):
            return True
        else:
            self.parameters['temperature at suction'] = self.value

        self.parameters['compression stage'] = self.compression_stage_index
        self.parameters['number of cylinders'] = self.number_of_cylinders
        
        if self.number_of_cylinders > 1:    
            if self.check_input_parameters(self.lineEdit_TDC_crank_angle_2, "TOP DEAD CENTER CRANCK ANGLE 2"):
                return True
            else:
                self.parameters['TDC crank angle 2'] = self.value
                # self.tdc2 = self.value

        if self.double_acting:
            self.parameters['double effect'] = True

        if self.single_acting:
            if self.head_end_cylinder:
                cylinder_label = 'HEAD END'
            elif self.crank_end_cylinder:
                cylinder_label = 'CRANK END'
            self.parameters['double effect'] = False
            self.parameters['cylinder label'] = cylinder_label

        list_parameters = []
        for key, parameter in self.parameters.items():
            if key not in ['cylinder label', 'compression stage', 'number of cylinders', 'TDC crank angle 2']:
                list_parameters.append(parameter)

        self.compressor = CompressorModel(list_parameters)
        self.compressor.number_of_cylinders = self.parameters['number of cylinders']
        
        if 'cylinder label' in self.parameters.keys():
            self.compressor.active_cylinder = self.parameters['cylinder label']
        if 'TDC crank angle 2' in self.parameters.keys():
            self.compressor.tdc2 = self.parameters['TDC crank angle 2']*np.pi/180

        return False
    
    def process_aquisition_parameters(self):
        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.update_max_frequency()

        T_rev = 60/self.parameters['rotational speed']
        list_T = [10, 5, 2, 1, 0.5]
        list_df = [0.1, 0.2, 0.5, 1, 2]

        T_selected = list_T[self.currentIndex]
        df_selected = list_df[self.currentIndex]

        if np.remainder(T_selected, T_rev) == 0:
            T = T_selected
            df = 1/T
        else:
            i = 0
            df = 1/(T_rev)
            while df > df_selected:
                i += 1
                df = 1/(i*T_rev)
        self.N_rev = i

        final_df_label = '{} Hz'.format(round(df,6))
        self.lineEdit_frequency_resolution.setText(final_df_label)
        self.lineEdit_number_of_revolutions.setText(str(self.N_rev))
        self.aquisition_parameters_processed = True

    def save_table_values(self, frequencies, complex_values, basename):

        header = " COMPRESSOR MODEL PARAMETERS\n\n"
        for key, value in self.parameters.items():
            header += "{} = {}\n".format(key, str(value))

        header += "\nACOUSTIC COMPRESSOR EXCITATION: VOLUME VELOCITY SOURCE" 
        header += "\n\nFrequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 
        
        self.project.set_frequencies(frequencies, f_min, f_max, f_step)

        if "\\" in self.project_folder_path:
            self.new_load_path_table = "{}\\{}".format(self.project_folder_path, basename)
        elif "/" in self.project_folder_path:
            self.new_load_path_table = "{}/{}".format(self.project_folder_path, basename)

        real_values = np.real(complex_values)
        imag_values = np.imag(complex_values)
        abs_values = np.abs(complex_values)
        data = np.array([frequencies, real_values, imag_values, abs_values]).T
        np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

    def get_table_name(self, label, _node):
        self.size = self.mesh.volume_velocity_table_index + 1
        return 'table{}_compressor_excitation_{}.dat'.format( self.size, label)

    def process_all_inputs(self):
        self.project.file.temp_table_name = None
        if self.check_all_nodes():
            return
        if self.check_all_parameters():
            return
        self.process_aquisition_parameters()

        if self.connection_at_suction_and_discharge or self.connection_at_suction:
            freq, in_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'in_flow')
            table_name = self.get_table_name('suction', self.suction_node_ID)
            connection_type = 'suction'
            if self.project.set_volume_velocity_bc_by_node( [self.suction_node_ID], 
                                                            in_flow_rate, 
                                                            True, 
                                                            table_name=table_name, 
                                                            table_index=self.size, 
                                                            additional_info=connection_type):
                return
            else:
                self.save_table_values(freq, in_flow_rate, table_name)
                
        if self.connection_at_suction_and_discharge or self.connection_at_discharge:  
            freq, out_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'out_flow') 
            table_name = self.get_table_name('discharge', self.discharge_node_ID)
            connection_type = 'discharge'
            if self.project.set_volume_velocity_bc_by_node( [self.discharge_node_ID], 
                                                            out_flow_rate, 
                                                            True, 
                                                            table_name=table_name, 
                                                            table_index=self.size, 
                                                            additional_info=connection_type):
                return
            else:
                self.save_table_values(freq, out_flow_rate, table_name)

        self.close()

    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()
    
    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_number_of_cylinders(self):
        self.number_of_cylinders = self.spinBox_number_of_cylinders.value()
        if self.number_of_cylinders == 1:
            self.lineEdit_TDC_crank_angle_2.setDisabled(True)
        else:
            self.lineEdit_TDC_crank_angle_2.setDisabled(False)

    def comboBox_event_frequency_resolution(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def comboBox_event_stage(self):
        self.currentIndex_stage = self.comboBox_stage.currentIndex()
        list_stage_labels = ['stage_1', 'stage_2', 'stage_3'] 
        self.compression_stage_label = list_stage_labels[self.currentIndex_stage]
        self.compression_stage_index = self.currentIndex_stage + 1

    def update_number_points(self):
        return self.spinBox_number_of_points.value()

    def update_max_frequency(self):
        return self.spinBox_max_frequency.value()

    def plot_PV_diagram_head_end(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_head_end()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_crank_end()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_pressure_vs_time()
        return

    def plot_volume_time(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_volume_vs_time()
        return
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_suction_time()
        return

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_discharge_time()
        return
    
    def plot_rod_pressure_load_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_frequency(self.N_rev)
        return

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_suction_frequency(self.N_rev)
        return

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_discharge_frequency(self.N_rev)
        return

    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_head_end_pressure_vs_angle()
        return

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_head_end_volume_vs_angle()
        return

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_pressure_vs_angle()
        return

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_volume_vs_angle()
        return    

    def double_confirm_action(self):
        confirm_act = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure want to remove all compressor excitations?",
            QMessageBox.No | QMessageBox.Yes)
        
        if confirm_act == QMessageBox.Yes:
            return False
        else:
            return True
            
    def reset_all(self):
        if self.double_confirm_action():
            return
        self.get_dict_of_volume_velocity_from_file()
        for node in self.dict_volume_velocity.keys():
            self.node_ID_remove = int(node)
            self.reset_node()
        self.node_ID_remove = None
        title = "RESET OF COMPRESSOR EXCITATION"
        message = "All compressor excitations have been removed from the model."
        PrintMessageInput([title, message, window_title2])
        self.mesh.volume_velocity_table_index = 0

    def reset_node(self):
        self.get_dict_of_volume_velocity_from_file()
        if self.node_ID_remove is None:    
            self.selected_node = self.lineEdit_node_ID_info.text()
            if self.selected_node == "":
                title = "EMPTY NODE SELECTION"
                message = "None node has been selected from list. You should select a node before continue."
                PrintMessageInput([title, message, window_title2])
                return
        else:
            self.selected_node = self.node_ID_remove
        config = configparser.ConfigParser()
        config.read(self.project.file._node_acoustic_path)
        config.remove_section(str(self.selected_node)) 
        self.project.mesh.set_volume_velocity_bc_by_node(int(self.selected_node), None)
        for _, table_str in self.dict_volume_velocity[int(self.selected_node)]:
            self.selected_table = table_str.replace("[", "").replace("]", "")
            self.get_path_of_selected_table()
            os.remove(self.path_of_selected_table)
        with open(self.project.file._node_acoustic_path, 'w') as config_file:
            config.write(config_file)
        self.load_volume_velocity_tables_info()
        self.lineEdit_node_ID_info.setText("")
        self.lineEdit_table_name_info.setText("")
        self.opv.updateRendererMesh()

    def remove_table(self):
        self.get_dict_of_volume_velocity_from_file()
        self.selected_node = self.lineEdit_node_ID_info.text()
        self.selected_table = self.lineEdit_table_name_info.text()
        if self.selected_node == "":
            title = "EMPTY TABLE SELECTION"
            message = "None table has been selected from list. You should select a table before continue."
            PrintMessageInput([title, message, window_title2])
            return
        else:
            config = configparser.ConfigParser()
            config.read(self.project.file._node_acoustic_path)
            for key, table_str in self.dict_volume_velocity[int(self.selected_node)]:
                if self.selected_table in table_str:
                    config.remove_option(section=str(self.selected_node), option=key)  
                    if list(config[self.selected_node].keys())==[]:
                        config.remove_section(self.selected_node)
                    self.lineEdit_node_ID_info.setText("")
                    self.lineEdit_table_name_info.setText("")
            with open(self.project.file._node_acoustic_path, 'w') as config_file:
                config.write(config_file)
            self.load_volume_velocity_tables_info()
            self.get_path_of_selected_table()
            os.remove(self.path_of_selected_table)
            self.reset_node_and_reload()
    
    def reset_node_and_reload(self):
        self.get_dict_of_volume_velocity_from_file()
        self.project.mesh.set_volume_velocity_bc_by_node(int(self.selected_node), None)
        for key, table_name in self.dict_volume_velocity[int(self.selected_node)]:
            volume_velocity = self.project.file._get_acoustic_bc_from_string(table_name, key)
            self.project.mesh.set_volume_velocity_bc_by_node(int(self.selected_node), volume_velocity)

    def load_volume_velocity_tables_info(self):
        self.treeWidget_compressor_excitation.clear()
        self.get_dict_of_volume_velocity_from_file()
        for node_ID, tables_info in self.dict_volume_velocity.items():
            for _, table_str in tables_info:
                table_name = str(table_str).replace("[", "").replace("]", "")        
                new = QTreeWidgetItem([str(node_ID), table_name])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_compressor_excitation.addTopLevelItem(new)

    def get_dict_of_volume_velocity_from_file(self):
        config = configparser.ConfigParser()
        config.read(self.project.file._node_acoustic_path)
        self.dict_volume_velocity = defaultdict(list)  
        for node in config.sections():
            node_id = int(node)
            keys = list(config[node].keys())
            for key in keys:
                if "volume velocity - " in key:
                    table_file_name = config[str(node)][key]
                    self.dict_volume_velocity[node_id].append([key, table_file_name])

    def on_click_item(self, item):
        self.lineEdit_node_ID_info.setText(item.text(0))
        self.lineEdit_table_name_info.setText(item.text(1))

    def get_path_of_selected_table(self):
        if "\\" in self.project_folder_path:
            self.path_of_selected_table = "{}\\{}".format(self.project_folder_path, self.selected_table)
        elif "/" in self.project_folder_path:
            self.path_of_selected_table = "{}/{}".format(self.project_folder_path, self.selected_table)

    def force_to_close(self):
        self.close()
