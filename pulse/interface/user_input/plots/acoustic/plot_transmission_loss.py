from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QEvent, QObject, Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

import numpy as np


class PlotTransmissionLoss(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = UI_DIR / "plots/results/acoustic/plot_transmission_loss.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()
        self.update_flip_buttons()

    def _initialize(self):

        self.preprocessor = app().project.model.preprocessor
        self.solution = self.project.get_acoustic_solution()
        self.before_run = self.project.get_pre_solution_model_checks()

        self.diameters_from_node = self.preprocessor.neighbor_elements_diameter()

        self.unit_label = "dB"
        self.frequencies = self.model.frequencies
        self.elements = self.preprocessor.acoustic_elements
        self.analysis_method = self.project.analysis_method_label

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_processing_selector : QComboBox

        # QLineEdit
        self.lineEdit_input_node_id : QLineEdit  
        self.lineEdit_output_node_id : QLineEdit
        self.current_lineEdit = self.lineEdit_input_node_id

        # QPushButton
        self.pushButton_help : QPushButton
        self.pushButton_plot_data : QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_flip_nodes : QPushButton

    def _create_connections(self):
        #
        self.comboBox_processing_selector.currentIndexChanged.connect(self.update_flip_buttons)
        #
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_help.clicked.connect(self.call_help)
        self.pushButton_flip_nodes.clicked.connect(self.flip_nodes)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        #
        self.clickable(self.lineEdit_input_node_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_node_id).connect(self.lineEdit_2_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        if len(selected_nodes) == 1:
            self.current_lineEdit.setText(str(selected_nodes[0]))

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
        self.current_lineEdit = self.lineEdit_input_node_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_node_id

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input)

    def update_flip_buttons(self):
        index = self.comboBox_processing_selector.currentIndex()
        if index == 0:
            self.pushButton_flip_nodes.setDisabled(True)
        else:
            self.pushButton_flip_nodes.setDisabled(False)

    def call_help(self):
        window_title = "Help"
        if self.comboBox_processing_selector.currentIndex() == 0:
            title = "Required data to process the Transmission Loss"
            message = "Dear user, to determine the Transmission Loss (TL) of a filter or duct it is necessary to "
            message += "select the input node ID where the indicent wave is applied (usually by a volume velocity "
            message += "source) and the output node ID with an anechoic termination. An anechoic termination also "
            message += "should be applied at the input node ID to avoid wave reflections caused by the source itself."
            message += "\n\nInput node ID: incident plane wave (volume velocity + anechoic impedance)"
            message += "\nOutput node ID: outlet of filter or duct with an anechoic impedance\n"
        else:
            title = "Required data to process the Noise Reduction"
            message = "Dear user, to determine the Noise Reduction (NR) it is necessary to select the input "
            message += "node ID at inlet of the duct or filter and the node ID at the end termination. "
            message += "By definition, the NR represents the sound pressure level differece between the "
            message += "input and output of a duct or filter and it does not require a anechoic termination."

        PrintMessageInput([window_title, title, message], height=320, width=580)

    def check_nodes_information(self):

        if self.comboBox_processing_selector.currentIndex() == 0:

            vv_data = app().project.model.properties._get_property("volume_velocity", node_ids=self.input_node_id)
            input_at = app().project.model.properties._get_property("radiation_impedance", node_ids=self.input_node_id)
            
            if (vv_data, input_at).count(None):
                self.input_node_id = None
                self.lineEdit_input_node_id.setText("")

            elif "values" in vv_data.keys():
                self.input_volume_velocity = np.real(vv_data["values"])
                input_impedance_type = input_at["impedance_type"]
                if input_impedance_type != 0:
                    self.input_node_id = None
                    self.lineEdit_input_node_id.setText("")

            output_at = app().project.model.properties._get_property("radiation_impedance", node_ids=self.output_node_id)

            if output_at is None:
                self.output_node_id = None
                self.lineEdit_output_node_id.setText("")

            elif "impedance_type" in output_at.keys():
                output_impedance_type = output_at["impedance_type"]
                if output_impedance_type != 0:
                    self.output_node_id = None
                    self.lineEdit_output_node_id.setText("")

        else:

            if (self.input_node_id, self.output_node_id).count(None):
                return True

        if (self.input_node_id, self.output_node_id).count(None):
            self.call_help()
            return True

    def check_inputs(self):

        input_node = self.lineEdit_input_node_id.text()
        stop, self.input_node_id = self.before_run.check_selected_ids(input_node, "nodes", single_id=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True

        output_node = self.lineEdit_output_node_id.text()
        stop, self.output_node_id = self.before_run.check_selected_ids(output_node, "nodes", single_id=True)
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

        data = self.diameters_from_node[node]
        density = list()
        speed_of_sound = list()
        inner_diameter = list()

        for (index, _, int_dia) in data:
            inner_diameter.append(int_dia)
            density.append(self.elements[index].fluid.density)
            speed_of_sound.append(self.elements[index].speed_of_sound_corrected())
        ind = inner_diameter.index(min(inner_diameter))
        return inner_diameter[ind], density[ind], speed_of_sound[ind]

    def get_TL_NR(self):

        P_out = get_acoustic_frf(self.preprocessor, self.solution, self.output_node_id)

        d_in, rho_in, c0_in = self.get_minor_outer_diameter_from_node(self.input_node_id)
        d_out, rho_out, c0_out = self.get_minor_outer_diameter_from_node(self.output_node_id)
        A_in = np.pi*(d_in**2)/4
        A_out = np.pi*(d_out**2)/4

        # the zero_shift constant is summed to avoid zero values either in P_input2 or P_output2 variables
        zero_shift = 1e-12

        index = self.comboBox_processing_selector.currentIndex()
        if index == 0:

            ## Reference: 
            ## Howard, Carl Q. and Cazzolato, Benjamin S. Acoustic Analyses Using MATLAB® and ANSYS®. pags. 74 and 75. 2014.
  
            Q = self.input_volume_velocity
            u_n = Q / A_in
            P_in = u_n*rho_in*c0_in / 2
            # P_out += zero_shift

            # Prms_in2 = (P_in/np.sqrt(2))**2
            # Prms_out2 = np.real(P_out*np.conjugate(P_out))/2 + zero_shift

            # W_in = 10*np.log10(Prms_in2*A_in/(rho_in*c0_in))
            # W_out = 10*np.log10(Prms_out2*A_out/(rho_out*c0_out))
            # TL = W_in - W_out

            TL = 20*np.log10(P_in/P_out) + 20*np.log10(A_in/A_out)

            return TL

        if index == 1:

            P_in = get_acoustic_frf(self.preprocessor, self.solution, self.input_node_id)
            Prms_in2 = np.real(P_in*np.conjugate(P_in))/2 + zero_shift
            Prms_out2 = np.real(P_out*np.conjugate(P_out))/2 + zero_shift
            NR = 10*np.log10(Prms_in2/Prms_out2)

            return NR

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "{} between nodes {} and {}".format(self.y_label,
                                                           self.input_node_id, 
                                                           self.output_node_id)
        
        key = ("nodes", (self.input_node_id, self.output_node_id))

        self.model_results[key] = { 
                                    "x_data" : self.frequencies,
                                    "y_data" : self.get_TL_NR(),
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : self.y_label,
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : self.unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"
                                   }

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter.imported_dB_data()
        self.plotter._set_model_results_data_to_plot(self.model_results)

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