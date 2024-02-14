from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from data.user_input.data_handler.export_model_results import ExportModelResults
from data.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.print_message import PrintMessageInput

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))
    
class Plot_TL_NR_Input(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_TL_NR_input.ui'), self)

        self.opv = opv
        self.opv.setInputObject(self)

        self.projec = project
        self.analysis_method = project.analysis_method_label
        self.frequencies = project.frequencies
        self.solution = project.get_acoustic_solution()

        self.projec = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.elements = self.preprocessor.acoustic_elements
        self.dict_elements_diameter = self.preprocessor.neighbor_elements_diameter()
        self.neighboor_elements = self.preprocessor.neighboor_elements_of_node

        self._config_window()
        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.update()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))
        self.setWindowIcon(self.pulse_icon)

    def _reset_variables(self):
        self.unit_label = "dB"

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_processing_selector = self.findChild(QComboBox, 'comboBox_processing_selector')
        # QLineEdit
        self.lineEdit_input_node_id = self.findChild(QLineEdit, 'lineEdit_input_node_id')   
        self.lineEdit_output_node_id = self.findChild(QLineEdit, 'lineEdit_output_node_id')
        # QPushButton
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_flip_nodes_1 = self.findChild(QPushButton, 'pushButton_flip_nodes_1')
        self.pushButton_flip_nodes_2 = self.findChild(QPushButton, 'pushButton_flip_nodes_2')
        self.pushButton_help = self.findChild(QPushButton, 'pushButton_help')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_flip_nodes_1.setIcon(self.update_icon)
        self.pushButton_flip_nodes_2.setIcon(self.update_icon)

    def _create_connections(self):
        self.comboBox_processing_selector.currentIndexChanged.connect(self.update_flip_buttons)
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_help.clicked.connect(self.call_help)
        self.pushButton_flip_nodes_1.clicked.connect(self.flip_nodes)
        self.pushButton_flip_nodes_2.clicked.connect(self.flip_nodes)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        self.update_flip_buttons()

    def update_flip_buttons(self):
        index = self.comboBox_processing_selector.currentIndex()
        if index == 0:
            self.pushButton_flip_nodes_1.setDisabled(True)
            self.pushButton_flip_nodes_2.setDisabled(True)
        else:
            self.pushButton_flip_nodes_1.setDisabled(False)
            self.pushButton_flip_nodes_2.setDisabled(False)

    def call_help(self):
        window_title = "Help"
        if self.comboBox_processing_selector.currentIndex() == 0:
            title = "Required data to process the Transmission Loss"
            message = "Dear user, to determine the Transmission Loss (TL) of a filter or duct it is necessary to "
            message += "select the input node ID where the indicent wave is applied (usually by a volume velocity "
            message += "source) and the output node ID with a anechoic termination. An anechoic termination also "
            message += "should be applied at the input node ID to avoid wave reflections caused by the source itself."
            message += "\n\nInput node ID: incident plane wave (volume velocity + anechoic impedance)"
            message += "\nOutput node ID: outlet of filter or duct with an anechoic impedance\n"
        else:
            title = "Required data to process the Noise Reduction"
            message = "Dear user, to determine the Noise Reduction (NR) it is necessary to select the input "
            message += "node ID at inlet of the duct or filter and the node ID at the end termination. "
            message += "By definition, the NR represents the sound pressure level differece between the "
            message += "input and output of a duct or filter and it does not require a anechoic termination."
        PrintMessageInput([window_title, title, message])

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input) 

    def update(self):
        selected_ids = self.opv.getListPickedPoints()
        self.check_nodes_information(selected_ids)

    def check_nodes_information(self, picked_nodes=None):
        
        if picked_nodes is None:
            selected_ids = []
            if self.lineEdit_input_node_id.text() != "":
                input_node_id = self.lineEdit_input_node_id.text()
                selected_ids.append(int(input_node_id))
            if self.lineEdit_output_node_id.text() != "":
                output_node_id = self.lineEdit_output_node_id.text()
                selected_ids.append(int(output_node_id))
        else:
            selected_ids = self.opv.getListPickedPoints()
        
        self.input_node_ID = None
        self.output_node_ID = None
        self.lineEdit_input_node_id.setText("")
        self.lineEdit_output_node_id.setText("")

        if self.comboBox_processing_selector.currentIndex() == 0:
            for node_id in selected_ids:
                neigh_elements = self.neighboor_elements(node_id)
                if len(neigh_elements) == 1:
                    node = self.preprocessor.nodes[node_id]
                    if node in self.preprocessor.nodes_with_volume_velocity:
                        self.input_volume_velocity = np.real(node.volume_velocity)
                        self.input_node_ID = node_id
                        self.lineEdit_input_node_id.setText(str(node_id))
                    if node in self.preprocessor.nodes_with_radiation_impedance:
                        if node not in self.preprocessor.nodes_with_volume_velocity:
                            self.output_node_ID = node_id
                            self.lineEdit_output_node_id.setText(str(node_id))
                else:
                    return True

        
    def check_inputs(self):

        lineEdit_input = self.lineEdit_input_node_id.text()
        stop, self.input_node_ID = self.before_run.check_input_NodeID(lineEdit_input, single_ID=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True

        lineEdit_output = self.lineEdit_output_node_id.text()
        stop, self.output_node_ID = self.before_run.check_input_NodeID(lineEdit_output, single_ID=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True
        
        if self.check_nodes_information():
            return True

        if self.comboBox_processing_selector.currentIndex() == 0:
            self.y_label = "Transmission loss"

        if self.comboBox_processing_selector.currentIndex() == 1:
            self.y_label = "Noise reduction"



    def get_minor_outer_diameter_from_node(self, node):
        data = self.dict_elements_diameter[node]
        inner_diameter = []
        density = []
        speed_of_sound = []
        for (index, _, int_dia) in data:
            inner_diameter.append(int_dia)
            density.append(self.elements[index].fluid.density)
            speed_of_sound.append(self.elements[index].speed_of_sound_corrected())
        ind = inner_diameter.index(min(inner_diameter))
        return inner_diameter[ind], density[ind], speed_of_sound[ind]

    def get_TL_NR(self):

        P_out = get_acoustic_frf(self.preprocessor, self.solution, self.output_node_ID)
        
        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12
        Prms_out2 = np.real(P_out*np.conjugate(P_out))/2 + zero_shift

        d_in, rho_in, c0_in = self.get_minor_outer_diameter_from_node(self.input_node_ID)
        d_out, rho_out, c0_out = self.get_minor_outer_diameter_from_node(self.output_node_ID)
        A_in = np.pi*(d_in**2)/4
        A_out = np.pi*(d_out**2)/4

        index = self.comboBox_processing_selector.currentIndex()
        if index == 0:
            Q = self.input_volume_velocity
            u_n = Q/A_in
            P_in = u_n*rho_in*c0_in/1
            Prms_in2 = (P_in/np.sqrt(2))**2
            W_in = 10*np.log10(Prms_in2*A_in/(rho_in*c0_in))
            W_out = 10*np.log10(Prms_out2*A_out/(rho_out*c0_out))
            TL = W_in - W_out
            return TL

        if index == 1:
            P_in = get_acoustic_frf(self.preprocessor, self.solution, self.input_node_ID)
            Prms_in2 = np.real(P_in*np.conjugate(P_in))/2 + zero_shift
            NR = 10*np.log10(Prms_in2/Prms_out2)
            return NR

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "{} between nodes {} and {}".format(self.y_label,
                                                           self.input_node_ID, 
                                                           self.output_node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_TL_NR(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : self.y_label,
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter.imported_dB_data()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()