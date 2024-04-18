from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.tools.utils import get_new_path, remove_bc_from_file
from pulse.interface.user_input.model.setup.fluid.fluid_input import FluidInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

# from pulse.preprocessing.compressor_model import CompressorModel
from compressors.reciprocating.model import CompressorModel

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = 0.45359237*9.80665/((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5

class CompressorModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/compressor_model_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_treeWidget()
        self.update()
        self.load_compressor_excitation_tables_info()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.remove_message = True
        self.table_name = None
        self.not_update_event = False
        
        self.node_id = self.opv.getListPickedPoints()

        self.preprocessor = self.project.preprocessor
        self.nodes = self.preprocessor.nodes
        self.before_run = self.project.get_pre_solution_model_checks()    

        self.project_folder_path = self.project.file._project_path  
        self.node_acoustic_path = self.project.file._node_acoustic_path   
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.compressor_excitation_tables_folder_path = get_new_path(self.acoustic_folder_path, "compressor_excitation_files")  

    def _define_qt_variables(self):
        
        # QComboBox
        self.comboBox_connection_setup : QComboBox
        self.comboBox_cylinder_acting : QComboBox
        self.comboBox_frequency_resolution : QComboBox
        self.comboBox_compressors_tables : QComboBox
        self.comboBox_stage : QComboBox
        self.comboBox_suction_pressure_units : QComboBox
        self.comboBox_suction_temperature_units : QComboBox
        
        # QLabel
        self.label_molar_mass : QLabel
        self.label_molar_mass_unit : QLabel
        self.label_isentropic_exp : QLabel
        self.label_isentropic_exp_unit : QLabel
        
        # QLineEdit
        self.lineEdit_suction_node_ID : QLineEdit
        self.lineEdit_discharge_node_ID : QLineEdit
        self.lineEdit_frequency_resolution : QLineEdit
        self.lineEdit_number_of_revolutions : QLineEdit
        self.lineEdit_bore_diameter : QLineEdit
        self.lineEdit_stroke : QLineEdit
        self.lineEdit_connecting_rod_length : QLineEdit
        self.lineEdit_rod_diameter : QLineEdit
        self.lineEdit_pressure_ratio : QLineEdit
        self.lineEdit_clearance_head_end : QLineEdit
        self.lineEdit_clearance_crank_end : QLineEdit
        self.lineEdit_rotational_speed : QLineEdit
        self.lineEdit_isentropic_exponent : QLineEdit
        self.lineEdit_molar_mass : QLineEdit
        self.lineEdit_pressure_at_suction : QLineEdit
        self.lineEdit_temperature_at_suction : QLineEdit
        self.lineEdit_selection_info : QLineEdit
        self.lineEdit_node_ID_info : QLineEdit
        self.lineEdit_table_name_info : QLineEdit
        self.current_lineEdit = self.lineEdit_suction_node_ID
        
        # QPushButton
        self.pushButton_flipNodes : QPushButton
        self.pushButton_reset_entries : QPushButton
        self.pushButton_plot_PV_diagram_head_end : QPushButton
        self.pushButton_plot_PV_diagram_crank_end : QPushButton
        self.pushButton_plot_PV_diagram_both_ends : QPushButton
        self.pushButton_plot_piston_position_and_velocity_time : QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_suction_time : QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time : QPushButton
        self.pushButton_plot_rod_pressure_load_frequency : QPushButton
        self.pushButton_plot_rod_pressure_load_time : QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency : QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency : QPushButton
        self.pushButton_plot_pressure_head_end_angle : QPushButton
        self.pushButton_plot_volume_head_end_angle : QPushButton
        self.pushButton_plot_pressure_crank_end_angle : QPushButton
        self.pushButton_plot_volume_crank_end_angle : QPushButton
        self.pushButton_process_aquisition_parameters : QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove_table : QPushButton
        self.pushButton_reset_node : QPushButton
        self.pushButton_reset_all : QPushButton
        self.pushButton_cancel : QPushButton
        #
        self.pushButton_reset_entries.setCursor(Qt.PointingHandCursor)
        self.pushButton_process_aquisition_parameters.setCursor(Qt.PointingHandCursor)
        self.pushButton_confirm.setCursor(Qt.PointingHandCursor)
        self.pushButton_cancel.setCursor(Qt.PointingHandCursor)
        
        # QSpinBox
        self.spinBox_number_of_points : QSpinBox
        self.spinBox_max_frequency : QSpinBox
        self.spinBox_number_of_cylinders : QSpinBox
        self.spinBox_tdc1_crank_angle : QSpinBox
        self.spinBox_tdc2_crank_angle : QSpinBox
        self.spinBox_capacity : QSpinBox
        
        # QTabWidget
        self.tabWidget_compressor : QTabWidget
        
        # QTreeWidget
        self.treeWidget_compressor_excitation : QTreeWidget

    def _config_treeWidget(self):
        self.treeWidget_compressor_excitation.setColumnWidth(0, 70)
        # self.treeWidget_compressor_excitation.setColumnWidth(1, 140)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def _create_connections(self):
        self.comboBox_connection_setup.currentIndexChanged.connect(self.update_compressor_to_pipeline_connections)
        self.comboBox_cylinder_acting.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_compressors_tables.currentIndexChanged.connect(self.comboBox_event_update)
        self.comboBox_stage.currentIndexChanged.connect(self.comboBox_event_stage)
        self.comboBox_compressors_tables.setVisible(False)
        self.comboBox_event_stage()
        self.update_compressing_cylinders_setup()
        self.update_compressor_to_pipeline_connections()
        #
        # self.pushButton_flipNodes.clicked.connect(self.flip_nodes)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries)
        self.pushButton_plot_PV_diagram_head_end.clicked.connect(self.plot_PV_diagram_head_end)
        self.pushButton_plot_PV_diagram_crank_end.clicked.connect(self.plot_PV_diagram_crank_end)
        self.pushButton_plot_PV_diagram_both_ends.clicked.connect(self.plot_PV_diagram_both_ends)
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.clicked.connect(self.plot_volumetric_flow_rate_at_suction_time)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_time)
        self.pushButton_plot_rod_pressure_load_frequency.clicked.connect(self.plot_rod_pressure_load_frequency)
        self.pushButton_plot_rod_pressure_load_time.clicked.connect(self.plot_rod_pressure_load_time)
        self.pushButton_plot_piston_position_and_velocity_time.clicked.connect(self.plot_piston_position_and_velocity_time)
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_suction_frequency)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_frequency)
        self.pushButton_plot_pressure_head_end_angle.clicked.connect(self.plot_pressure_head_end_angle)
        self.pushButton_plot_volume_head_end_angle.clicked.connect(self.plot_volume_head_end_angle)
        self.pushButton_plot_pressure_crank_end_angle.clicked.connect(self.plot_pressure_crank_end_angle)
        self.pushButton_plot_volume_crank_end_angle.clicked.connect(self.plot_volume_crank_end_angle)
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        self.pushButton_confirm.clicked.connect(self.process_all_inputs)
        self.pushButton_remove_table.clicked.connect(self.remove_table)
        self.pushButton_reset_node.clicked.connect(self.reset_node)
        self.pushButton_reset_all.clicked.connect(self.reset_all)
        self.pushButton_cancel.clicked.connect(self.force_to_close)
        #
        self.spinBox_number_of_points.valueChanged.connect(self.spinBox_event_number_of_points)        
        self.spinBox_max_frequency.valueChanged.connect(self.spinBox_event_max_frequency)
        self.spinBox_number_of_cylinders.valueChanged.connect(self.spinBox_event_number_of_cylinders)
        self.spinBox_event_number_of_cylinders()
        #
        self.tabWidget_compressor.currentChanged.connect(self.tabEvent)
        self.treeWidget_compressor_excitation.itemClicked.connect(self.on_click_item)
        #
        self.clickable(self.lineEdit_suction_node_ID).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_discharge_node_ID).connect(self.lineEdit_2_clicked)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_1_clicked(self):
        self.current_lineEdit = self.lineEdit_suction_node_ID

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_discharge_node_ID

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
    
    # def flip_nodes(self):
    #     if self.connection_at_suction_and_discharge:
    #         temp_text_suction = self.lineEdit_suction_node_ID.text()
    #         temp_text_discharge = self.lineEdit_discharge_node_ID.text()
    #         self.lineEdit_suction_node_ID.setText(temp_text_discharge)
    #         self.lineEdit_discharge_node_ID.setText(temp_text_suction)   

    def update_compressing_cylinders_setup(self):

        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.comboBox_cylinder_acting.currentIndex() == 1:
            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        if self.comboBox_cylinder_acting.currentIndex() == 2:
            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)

    def update_compressor_to_pipeline_connections(self):

        self.lineEdit_suction_node_ID.setDisabled(False)
        self.lineEdit_discharge_node_ID.setDisabled(False)     
        index = self.comboBox_connection_setup.currentIndex()
        list_node_ids = self.opv.getListPickedPoints()

        if index == 1:
            self.current_lineEdit = self.lineEdit_suction_node_ID
            self.lineEdit_discharge_node_ID.setDisabled(True)
            self.lineEdit_discharge_node_ID.setText("")
            if len(list_node_ids) == 1:
                self.lineEdit_suction_node_ID.setText(str(list_node_ids[-1]))

        elif index == 2:
            self.current_lineEdit = self.lineEdit_discharge_node_ID
            self.lineEdit_suction_node_ID.setDisabled(True)
            self.lineEdit_suction_node_ID.setText("")
            if len(list_node_ids) == 1:
                self.lineEdit_discharge_node_ID.setText(str(list_node_ids[-1]))
        else:
            self.current_lineEdit = self.lineEdit_suction_node_ID
            self.update()
            
    def writeNodes(self, list_node_ids):

        index = self.comboBox_connection_setup.currentIndex()

        if index == 1:
            self.lineEdit_discharge_node_ID.setText("")
            self.lineEdit_discharge_node_ID.setDisabled(True)

        elif index == 2:
            self.lineEdit_suction_node_ID.setText("")
            self.lineEdit_suction_node_ID.setDisabled(True)

        self.current_lineEdit.setText(str(list_node_ids[-1]))
        self.table_name = None
        self.comboBox_compressors_tables.clear()
        self.comboBox_compressors_tables.setVisible(False)
        self.get_existing_compressor_info(list_node_ids, update_tables=True)

    def comboBox_event_update(self):
        if self.not_update_event:
            return
        self.currentIndex_table = self.comboBox_compressors_tables.currentIndex()
        self.table_name = self.comboBox_compressors_tables.currentText()
        list_node_ids = self.opv.getListPickedPoints()
        self.get_existing_compressor_info(list_node_ids)
        
    def change_aquisition_parameters_controls(self, _bool):
        self.pushButton_process_aquisition_parameters.setDisabled(_bool)
        self.spinBox_max_frequency.setDisabled(_bool)
        self.spinBox_number_of_points.setDisabled(_bool)
        self.comboBox_frequency_resolution.setDisabled(_bool)
    
    def get_existing_compressor_info(self, list_node_ids, update_tables=False):
        self.not_update_event = True
        node = self.preprocessor.nodes[list_node_ids[0]]
        self.change_aquisition_parameters_controls(False)
        if len(node.compressor_excitation_table_names) > 0:
            self.comboBox_compressors_tables.setVisible(True)
            if len(node.compressor_excitation_table_names) > 1:
                self.change_aquisition_parameters_controls(True)
            if update_tables:
                self.table_name = node.compressor_excitation_table_names[0]
                for table in node.compressor_excitation_table_names:
                    self.comboBox_compressors_tables.addItem(table)
                if len(node.compressor_excitation_table_names) > 1:
                    self.comboBox_compressors_tables.setCurrentIndex(0)
            try:
                folder_table_path = get_new_path(self.acoustic_folder_path, "compressor_excitation_files")
                load_path_table = get_new_path(folder_table_path, self.table_name)
                
                if self.table_name != "":
                    table_file = open(load_path_table, "r")
                    lines = table_file.readlines()                
                    compressor_info = {}
                    for str_line in lines[2:23]:
                        if str_line[2:-1] != "":
                            key_value = str_line[2:-1].split(" = ")
                            try:
                                compressor_info[key_value[0]] = float(key_value[1])
                            except:
                                compressor_info[key_value[0]] = key_value[1]

                    data = np.loadtxt(load_path_table, delimiter=",")
                    compressor_info["frequencies"] = data[:,0]
                    table_file.close()                   
                    self.update_compressor_inputs(compressor_info)

            except Exception as log_error:
                title = f"Error while loading compressor parameters"
                message = str(log_error) 
                PrintMessageInput([window_title_1, title, message]) 

        self.not_update_event = False

    def get_aquisition_parameters(self, compressor_info):
        frequencies = compressor_info["frequencies"]
        rotational_speed = compressor_info["rotational speed"]
        f_min = frequencies[0]
        f_max = frequencies[-1]
        df = frequencies[1]-frequencies[0]
        N_rev = int((1/df)/(60/rotational_speed))
        self.N_rev = N_rev
        return f_min, f_max, df, N_rev

    def update(self):
        list_nodes = self.opv.getListPickedPoints()
        if len(list_nodes) == 1:
            self.writeNodes(list_nodes)
        else:
            self.current_lineEdit.setFocus()

    def update_compressor_inputs(self, compressor_info):

        node_ID = self.current_lineEdit.text()
        
        if 'discharge' in self.table_name:
            self.comboBox_connection_setup.setCurrentIndex(2)
            self.lineEdit_suction_node_ID.setText("")
            self.lineEdit_suction_node_ID.setDisabled(True)
            self.lineEdit_discharge_node_ID.setText(node_ID)
            
        if 'suction' in self.table_name:
            self.comboBox_connection_setup.setCurrentIndex(1)
            self.lineEdit_discharge_node_ID.setText("")
            self.lineEdit_discharge_node_ID.setDisabled(True)
            self.lineEdit_suction_node_ID.setText(node_ID)
            
        if "bore diameter" in compressor_info.keys():
            self.lineEdit_bore_diameter.setText(str(compressor_info["bore diameter"]))
        if "stroke" in compressor_info.keys():
            self.lineEdit_stroke.setText(str(compressor_info["stroke"]))
        if "connecting rod length" in compressor_info.keys():
            self.lineEdit_connecting_rod_length.setText(str(compressor_info["connecting rod length"]))
        if "rod diameter" in compressor_info.keys():
            self.lineEdit_rod_diameter.setText(str(compressor_info["rod diameter"]))
        if "pressure ratio" in compressor_info.keys():
            self.lineEdit_pressure_ratio.setText(str(compressor_info["pressure ratio"]))
        if "clearance (HE)" in compressor_info.keys():
            self.lineEdit_clearance_head_end.setText(str(compressor_info["clearance (HE)"]))
        if "clearance (CE)" in compressor_info.keys():
            self.lineEdit_clearance_crank_end.setText(str(compressor_info["clearance (CE)"]))
        if "TDC crank angle 1" in compressor_info.keys():
            self.spinBox_tdc1_crank_angle.setValue(int(compressor_info["TDC crank angle 1"]))
        if "rotational speed" in compressor_info.keys():
            self.lineEdit_rotational_speed.setText(str(compressor_info["rotational speed"]))
        if "capacity" in compressor_info.keys():
            self.spinBox_capacity.setValue(int(compressor_info["capacity"]))
        if "isentropic exponent" in compressor_info.keys():
            self.lineEdit_isentropic_exponent.setText(str(compressor_info["isentropic exponent"]))
        if "molar mass" in compressor_info.keys():
            self.lineEdit_molar_mass.setText(str(compressor_info["molar mass"]))
        if "pressure at suction" in compressor_info.keys():
            self.lineEdit_pressure_at_suction.setText(str(compressor_info["pressure at suction"]))
        if compressor_info["pressure unit"] == "kgf/cm²":
            self.comboBox_suction_pressure_units.setCurrentIndex(0)
        else:
            self.comboBox_suction_pressure_units.setCurrentIndex(1)
        if "temperature at suction" in compressor_info.keys():
            self.lineEdit_temperature_at_suction.setText(str(compressor_info["temperature at suction"]))
        if compressor_info["temperature unit"] == "°C":
            self.comboBox_suction_temperature_units.setCurrentIndex(0)
        else:
            self.comboBox_suction_temperature_units.setCurrentIndex(1)
        if "acting label" in compressor_info.keys():
            acting_key = int(compressor_info["acting label"])
            self.comboBox_cylinder_acting.setCurrentIndex(acting_key)

        if "number of cylinders" in compressor_info.keys():
            if compressor_info["number of cylinders"] == 1:
                self.spinBox_number_of_cylinders.setValue(1)
            elif compressor_info["number of cylinders"] == 2:
                self.spinBox_number_of_cylinders.setValue(2)
                if "TDC crank angle 2" in compressor_info.keys():
                    self.spinBox_tdc2_crank_angle.setValue(int(compressor_info["TDC crank angle 2"]))

        if "points per revolution" in compressor_info.keys():
            self.spinBox_number_of_points.setValue(int(compressor_info["points per revolution"]))

        f_min, f_max, df, N_rev = self.get_aquisition_parameters(compressor_info)
        self.lineEdit_frequency_resolution.setText(str(df))
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))

    def reset_entries(self):
        self.comboBox_compressors_tables.clear()
        self.comboBox_compressors_tables.setVisible(False)
        self.comboBox_cylinder_acting.setCurrentIndex(0)
        self.comboBox_stage.setCurrentIndex(0)
        self.comboBox_suction_pressure_units.setCurrentIndex(0)
        self.comboBox_suction_temperature_units.setCurrentIndex(0)
        self.lineEdit_bore_diameter.setText("")
        self.lineEdit_stroke.setText("")
        self.lineEdit_connecting_rod_length.setText("")
        self.lineEdit_rod_diameter.setText("")
        self.lineEdit_pressure_ratio.setText("")
        self.lineEdit_clearance_head_end.setText("")
        self.lineEdit_clearance_crank_end.setText("")
        self.lineEdit_rotational_speed.setText("")
        self.lineEdit_isentropic_exponent.setText("")
        self.lineEdit_molar_mass.setText("")
        self.lineEdit_pressure_at_suction.setText("")
        self.lineEdit_temperature_at_suction.setText("")
        self.spinBox_number_of_cylinders.setValue(1)
        self.spinBox_tdc1_crank_angle.setValue(0)
        self.spinBox_tdc2_crank_angle.setValue(0)
        self.spinBox_capacity.setValue(100)
        self.table_name = None

    def check_node_id(self, lineEdit):
        
        lineEdit_nodeID = lineEdit.text()
        self.stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        
        if self.stop:
            return True
              
    def check_all_nodes(self, check_nodes=True):
        index = self.comboBox_connection_setup.currentIndex()
        if check_nodes:
            if index == 0:

                if self.check_node_id(self.lineEdit_suction_node_ID):
                    self.lineEdit_suction_node_ID.setFocus()
                    return True

                self.suction_node_ID = self.node_ID
                
                if self.check_node_id(self.lineEdit_discharge_node_ID):
                    self.lineEdit_discharge_node_ID.setFocus()
                    return True

                self.discharge_node_ID = self.node_ID

                if self.suction_node_ID == self.discharge_node_ID:
                    title = "ERROR IN NODES SELECTION"
                    message = "The nodes selected to the suction and discharge must differ. Try to choose another pair of nodes."
                    PrintMessageInput([window_title_1, title, message])
                    return True

            if index == 1:
                if self.check_node_id(self.lineEdit_suction_node_ID):
                    self.lineEdit_suction_node_ID.setFocus()
                    return True
              
                self.suction_node_ID = self.node_ID

            if index == 2:
                if self.check_node_id(self.lineEdit_discharge_node_ID):
                    self.lineEdit_discharge_node_ID.setFocus()
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
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            message = "None value has been typed to the {}.".format(label)
            PrintMessageInput([window_title_1, title, message])
            return True
        return False

    def check_all_parameters(self):
        self.parameters = {}

        if self.check_input_parameters(self.lineEdit_bore_diameter, "BORE DIAMETER"):
            self.lineEdit_bore_diameter.setFocus()
            return True
        else:
            self.parameters['bore diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_stroke, "STROKE"):
            self.lineEdit_stroke.setFocus()
            return True
        else:
            self.parameters['stroke'] = self.value

        if self.check_input_parameters(self.lineEdit_connecting_rod_length, "CONNECTING ROD LENGTH"):
            self.lineEdit_connecting_rod_length.setFocus()
            return True
        else:
            self.parameters['connecting rod length'] = self.value

        if self.check_input_parameters(self.lineEdit_rod_diameter, "ROD DIAMETER"):
            self.lineEdit_rod_diameter.setFocus()
            return True
        else:
            self.parameters['rod diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_ratio, "PRESSURE RATIO"):
            self.lineEdit_pressure_ratio.setFocus()
            return True
        else:
            self.parameters['pressure ratio'] = self.value
    
        if self.check_input_parameters(self.lineEdit_clearance_head_end, "CLEARANCE (HE)"):
            self.lineEdit_clearance_head_end.setFocus()
            return True
        else:
            self.parameters['clearance (HE)'] = self.value
        
        if self.check_input_parameters(self.lineEdit_clearance_crank_end, "CLEARANCE (CE)"):
            self.lineEdit_clearance_crank_end.setFocus()
            return True
        else:
            self.parameters['clearance (CE)'] = self.value

        self.parameters['TDC crank angle 1'] = self.spinBox_tdc1_crank_angle.value()

        if self.check_input_parameters(self.lineEdit_rotational_speed, "ROTATIONAL SPEED"):
            self.lineEdit_rotational_speed.setFocus()
            return True
        else:
            self.parameters['rotational speed'] = self.value

        self.parameters['capacity'] = self.spinBox_capacity.value()

        if self.check_input_parameters(self.lineEdit_molar_mass, "MOLAR MASS"):
            self.lineEdit_molar_mass.setFocus()
            return True
        else:
            self.parameters['molar mass'] = self.value

        if self.check_input_parameters(self.lineEdit_isentropic_exponent, "ISENTROPIC EXPONENT"):
            self.lineEdit_isentropic_exponent.setFocus()
            return True
        else:
            self.parameters['isentropic exponent'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_at_suction, "PRESSURE AT SUCTION"):
            self.lineEdit_pressure_at_suction.setFocus()
            return True
        else:
            self.parameters['pressure at suction'] = self.value

        if self.comboBox_suction_pressure_units.currentIndex() == 0:
            self.parameters['pressure unit'] = "kgf/cm²"
        elif self.comboBox_suction_pressure_units.currentIndex() == 1:
            self.parameters['pressure unit'] = "bar"

        if self.check_input_parameters(self.lineEdit_temperature_at_suction, "TEMPERATURE AT SUCTION"):
            self.lineEdit_temperature_at_suction.setFocus()
            return True
        else:
            self.parameters['temperature at suction'] = self.value

        if self.comboBox_suction_temperature_units.currentIndex() == 0:
            self.parameters['temperature unit'] = "°C"
        elif self.comboBox_suction_temperature_units.currentIndex() == 1:
            self.parameters['temperature unit'] = "K"

        self.parameters['compression stage'] = self.compression_stage_index
        self.parameters['number of cylinders'] = self.number_of_cylinders
        self.parameters['acting label'] = self.comboBox_cylinder_acting.currentIndex()

        if self.number_of_cylinders > 1:
            self.parameters['TDC crank angle 2'] = self.spinBox_tdc2_crank_angle.value()
        else:
            self.parameters['TDC crank angle 2'] = None

        self.compressor = CompressorModel(self.parameters)
        self.compressor.number_of_cylinders = self.parameters['number of cylinders']

        if self.comboBox_suction_pressure_units.currentIndex() == 0:
            self.P_suction = self.parameters['pressure at suction']*kgf_cm2_to_Pa
        elif self.comboBox_suction_pressure_units.currentIndex() == 1:
            self.P_suction = self.parameters['pressure at suction']*bar_to_Pa
        
        if self.comboBox_suction_temperature_units.currentIndex() == 0:
            self.T_suction = self.parameters['temperature at suction'] + 273.15
        elif self.comboBox_suction_temperature_units.currentIndex() == 1:
            self.T_suction = self.parameters['temperature at suction']

        if self.parameters['TDC crank angle 2'] is not None:   
            self.compressor.tdc2 = self.parameters['TDC crank angle 2']*np.pi/180
        
        return False
    
    def process_aquisition_parameters(self):
        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.update_max_frequency()

        if self.table_name is not None:
            self.aquisition_parameters_processed = True
            return

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

        if self.project.change_project_frequency_setup("Compressor excitation", list(frequencies)):
            return True
        else:
            self.project.set_frequencies(frequencies, f_min, f_max, f_step)

        self.project.create_folders_acoustic("compressor_excitation_files")
        self.new_load_path_table = get_new_path(self.compressor_excitation_tables_folder_path, basename)

        real_values = np.real(complex_values)
        imag_values = np.imag(complex_values)
        abs_values = np.abs(complex_values)
        data = np.array([frequencies, real_values, imag_values, abs_values]).T
        np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)
        return False

    def get_table_name(self, node_id, label):
        _run = True
        table_index = 1
        node = self.preprocessor.nodes[node_id]
        while _run:
            if table_index not in node.compressor_excitation_table_indexes:
                node.compressor_excitation_table_indexes.append(table_index)
                _run = False
            else:
                table_index += 1 
        self.table_index = table_index        
        table_name = f"table{self.table_index}_node{node_id}_compressor_excitation_{label}.dat"
        return table_name

    def check_existing_compressor_parameters_and_edit(self):
        if self.table_name == self.comboBox_compressors_tables.currentText():
            self.remove_table()

    def process_all_inputs(self):

        if self.check_all_nodes():
            return
        if self.check_all_parameters():
            return

        self.process_aquisition_parameters()
        self.check_existing_compressor_parameters_and_edit()
        index = self.comboBox_connection_setup.currentIndex()
        if index in [0, 1]:
            
            line_suction_node_ID = self.preprocessor.get_line_from_node_id(self.suction_node_ID)
            compressor_info = { "temperature (suction)" : self.T_suction,
                                "pressure (suction)" : self.P_suction,
                                "line_id" : line_suction_node_ID[0],
                                "node_id" : self.suction_node_ID,
                                "pressure ratio" : self.parameters['pressure ratio'],
                                "connection type" : 0 }

            read = FluidInput(compressor_thermodynamic_state = compressor_info)

            if not read.complete:
                return
            else:
                if read.REFPROP is not None:
                    if read.REFPROP.complete:
                        self.parameters['molar mass'] = round(read.fluid_data_REFPROP["molar mass"], 6)
                        self.parameters['isentropic exponent'] = round(read.fluid_data_REFPROP["isentropic exponent"], 6)
                        self.parameters['fluid properties source'] = "REFPROP"
                else:
                    self.parameters['fluid properties source'] = "user-defined"

                self.parameters['points per revolution'] = self.compressor.number_points
                self.compressor.set_fluid_properties_and_update_state(self.parameters['isentropic exponent'],
                                                                      self.parameters['molar mass'])

                # self.T_discharge = self.compressor.T_disc

                freq, in_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'in_flow')
                table_name = self.get_table_name(self.suction_node_ID, 'suction')
                data = [in_flow_rate, table_name]

            self.project.remove_acoustic_pressure_table_files(self.suction_node_ID)
            self.project.remove_volume_velocity_table_files(self.suction_node_ID)

            if self.project.set_compressor_excitation_bc_by_node(   [self.suction_node_ID], 
                                                                    data, 
                                                                    self.table_index,
                                                                    'suction'   ):
                return
            else:
                if self.save_table_values(freq, in_flow_rate, table_name):
                    return
                
        if index in [0, 2]:

            line_discharge_node_ID = self.preprocessor.get_line_from_node_id(self.discharge_node_ID)
            compressor_info = { "temperature (suction)" : self.T_suction,
                                "pressure (suction)" : self.P_suction,
                                "line_id" : line_discharge_node_ID[0],
                                "node_id" : self.discharge_node_ID,
                                "pressure ratio" : self.parameters['pressure ratio'],
                                "connection type" : 1 }
            
            read = FluidInput(compressor_thermodynamic_state = compressor_info)
            if not read.complete:
                return
            else:
                if read.REFPROP is not None:
                    if read.REFPROP.complete:
                        self.parameters['molar mass'] = round(read.fluid_data_REFPROP["molar mass"], 6)
                        self.parameters['isentropic exponent'] = round(read.fluid_data_REFPROP["isentropic exponent"], 6)
                        self.parameters['fluid properties source'] = "REFPROP"
                else:
                    self.parameters['fluid properties source'] = "user-defined"
    
                self.parameters['points per revolution'] = self.compressor.number_points
                self.compressor.set_fluid_properties_and_update_state(self.parameters['isentropic exponent'],
                                                                      self.parameters['molar mass'])

            freq, out_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'out_flow') 
            table_name = self.get_table_name(self.discharge_node_ID, 'discharge')
            data = [out_flow_rate, table_name]

            self.project.remove_acoustic_pressure_table_files(self.discharge_node_ID)
            self.project.remove_volume_velocity_table_files(self.discharge_node_ID)

            if self.project.set_compressor_excitation_bc_by_node(   [self.discharge_node_ID], 
                                                                    data, 
                                                                    self.table_index, 
                                                                    'discharge'   ):
                return
            else:
                if self.save_table_values(freq, out_flow_rate, table_name):
                    return
                    
        self.opv.updateRendererMesh()
        self.close()

    # def save_compressor_parameters(self, connection_type):
    #     parameters = []
    #     for key, parameter in self.parameters.items():
    #         if key == 'fluid properties source':
    #             fluid_prop_source = parameter
    #         else:
    #             parameters.append(parameter)

    #     compressor_parameters = parameters
    #     compressor_fluid_prop_source = fluid_prop_source
        

    def remove_volume_velocity_table_files(self, node_id, table_name):
        self.project.remove_volume_velocity_table_files(node_id, table_name)
    
    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()
    
    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_number_of_cylinders(self):
        self.number_of_cylinders = self.spinBox_number_of_cylinders.value()
        if self.number_of_cylinders == 1:
            self.spinBox_tdc2_crank_angle.setDisabled(True)
        else:
            self.spinBox_tdc2_crank_angle.setDisabled(False)

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

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return
        N = self.update_number_points()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_both_ends()

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

    def plot_rod_pressure_load_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_time()
        return
    
    def plot_piston_position_and_velocity_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="time")

    def plot_piston_position_and_velocity_angle(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="angle")

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

    def reset_node(self):
        self.dict_node_to_compressor_excitation = self.project.file.get_dict_of_compressor_excitation_from_file()
        if self.node_ID_remove is None:    
            node_id = self.lineEdit_node_ID_info.text()
            if node_id == "":
                title = "EMPTY NODE SELECTION"
                message = "You should to select a node from the list before continue."
                PrintMessageInput([window_title_2, title, message])
                return
            else:
                self.selected_node = int(node_id)
        else:
            self.selected_node = self.node_ID_remove
        
        try:

            self.project.reset_compressor_info_by_node(self.selected_node)  
    
            if self.remove_message:
                title = "Compressor excitation removal finished"
                message = f"The compressor excitation attributed to \n"
                message += f"the {self.selected_node} node has been removed."
                PrintMessageInput([window_title_2, title, message])
            self.load_compressor_excitation_tables_info()
            self.opv.updateRendererMesh()
        
        except Exception as log_error:
            title = "Error while removing compressor excitation from node"
            message = "An error has been detected during the compressor \n"
            message += "excitation removal from selected node.\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])
        self.remove_message = True

    def remove_table(self):
        self.dict_node_to_compressor_excitation = self.project.file.get_dict_of_compressor_excitation_from_file()
        if self.table_name == self.comboBox_compressors_tables.currentText():
            self.selected_node = self.current_lineEdit.text()
            self.selected_table = self.table_name
        else:
            self.selected_node = self.lineEdit_node_ID_info.text()
            self.selected_table = self.lineEdit_table_name_info.text()
        
        if self.selected_node == "":
            title = "EMPTY TABLE SELECTION"
            message = "You should to select a table from list before continue."
            PrintMessageInput([window_title_2, title, message])
            return

        else:

            node_id = int(self.selected_node)
            node = self.preprocessor.nodes[node_id]
            prefix = self.selected_table.split("_node")[0]
            str_table_index = prefix.split("table")[1]
            table_index = int(str_table_index)

            if table_index in node.compressor_excitation_table_indexes:
                node.compressor_excitation_table_indexes.remove(table_index)
            if table_index in node.dict_index_to_compressor_connection_info.keys():
                node.dict_index_to_compressor_connection_info.pop(table_index)
            for list_data in self.dict_node_to_compressor_excitation[node_id]:
                [str_key, table_name_file] = list_data
                if self.selected_table in table_name_file:
                    remove_bc_from_file([node_id], self.node_acoustic_path, [str_key], None)

            title = "Compressor excitation table removal finished"
            message = f"The following compressor excitation table attributed to \n"
            message += f"the {node_id} node has been removed from the model:\n\n"
            message += f"{self.selected_table}"
            PrintMessageInput([window_title_2, title, message])

            self.load_compressor_excitation_tables_info()
            self.reset_node_and_reload(node_id)
    
    def reset_node_and_reload(self, node_id):
        self.preprocessor.set_compressor_excitation_bc_by_node(node_id, [None, None])
        if node_id in self.dict_node_to_compressor_excitation.keys():
            for str_key, table_name in self.dict_node_to_compressor_excitation[node_id]:
                compressor_excitation, table_name, _ = self.project.file._get_acoustic_bc_from_string(  table_name, str_key, 
                                                                                                        "compressor_excitation_files"  )
                if 'discharge' in table_name:
                    connection_info = "discharge"
                else:
                    connection_info = "suction"
                self.preprocessor.set_compressor_excitation_bc_by_node( node_id, 
                                                                        [compressor_excitation, table_name], 
                                                                        connection_info=connection_info )
        else:
            self.project.reset_compressor_info_by_node(node_id)

        if self.project.file.check_if_table_can_be_removed_in_acoustic_model( node_id, "compressor excitation",
                                                                              self.selected_table, "compressor_excitation_files" ):
            self.project.remove_acoustic_table_files_from_folder( self.selected_table, "compressor_excitation_files" )
            self.load_compressor_excitation_tables_info()
        self.opv.updateRendererMesh()

    def reset_all(self):
        if len(self.preprocessor.nodes_with_compressor_excitation) > 0:
            title = f"Removal of all compressor excitations"
            message = "Do you really want to remove all compressor excitations \napplied to the following nodes?\n\n"
            for node in self.preprocessor.nodes_with_compressor_excitation:
                message += f"{node.external_index}\n"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            if read._continue:
                self.dict_node_to_compressor_excitation = self.project.file.get_dict_of_compressor_excitation_from_file()
                for node_id in self.dict_node_to_compressor_excitation.keys():
                    self.remove_message = False
                    self.node_ID_remove = node_id
                    self.reset_node()
                self.node_ID_remove = None
                title = "Reset of compressor excitations"
                message = "All compressor excitations have been removed from the model."
                PrintMessageInput([window_title_2, title, message])

    def load_compressor_excitation_tables_info(self):
        self.treeWidget_compressor_excitation.clear()
        self.dict_node_to_compressor_excitation = self.project.file.get_dict_of_compressor_excitation_from_file()
        for node_ID, tables_info in self.dict_node_to_compressor_excitation.items():
            for _, table_str in tables_info:
                table_name = table_str[1:-1]       
                new = QTreeWidgetItem([str(node_ID), table_name])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_compressor_excitation.addTopLevelItem(new)
        self.lineEdit_node_ID_info.setText("")
        self.lineEdit_table_name_info.setText("")
        self.update_tabs_visibility()

    def on_click_item(self, item):
        self.lineEdit_node_ID_info.setText(item.text(0))
        self.lineEdit_table_name_info.setText(item.text(1))
        
    def force_to_close(self):
        self.close()

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_compressor_excitation) == 0:
            self.tabWidget_compressor.setCurrentIndex(0)
            self.tabWidget_compressor.setTabVisible(3, False)
        else:
            self.tabWidget_compressor.setTabVisible(3, True)

    def get_volume_velocity_table_names_in_typed_nodes(self, list_node_ids):
        list_table_names = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.volume_velocity_table_name is not None:
                table_name = node.volume_velocity_table_name
                if table_name not in list_table_names:
                    list_table_names.append(table_name)
        return list_table_names

    def remove_compressor_excitation_table_files(self, list_node_ids):
        self.project.remove_compressor_excitation_table_files(list_node_ids)
