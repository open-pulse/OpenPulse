import numpy as np
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface import error_title
from pulse.interface.ui_generated.criterias.allowable_pulsations_for_reciprocating_compressor_inputs_ui import (
    AllowablePulsationsForReciprocatingCompressorInputs_UI,
)
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_length_unit, convert_pressure_unit
from pulse.interface.user_input.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.properties.fluid import Fluid
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal


class AllowablePulsationsForReciprocatingCompressorInputs(AllowablePulsationsForReciprocatingCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()        
        self._create_connections()
        self.selection_callback()

    @property
    def model(self):
        return app().project.model

    @property
    def preprocessor(self):
        return app().project.model.preprocessor

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def nodal_solution(self):
        return app().project.get_acoustic_solution()

    def _initialize(self):

        self.model_results = dict()
        self.comp_parameters = dict()

        self.before_run = app().project.get_pre_solution_model_checks()
        self.frequencies = self.model.frequencies

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _create_connections(self):
        #
        self.pushButton_plot_unfiltered_criteria.clicked.connect(self.plot_unfiltered_criteria)
        self.pushButton_plot_filtered_criteria.clicked.connect(self.plot_filtered_criteria)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_unfiltered_fields()
        self.reset_filtered_fields()

        selected_nodes = app().main_window.list_selected_nodes()
        self.line_ids = self.preprocessor.get_line_from_node_id(selected_nodes)

        self.pushButton_plot_unfiltered_criteria.setDisabled(True)
        self.pushButton_plot_filtered_criteria.setDisabled(True)

        if len(selected_nodes) == 1:

            node_id = selected_nodes[0]
            compressor_data = self.properties._get_property("reciprocating_compressor_excitation", node_ids=node_id)

            if isinstance(compressor_data, dict):
                self.pushButton_plot_unfiltered_criteria.setDisabled(False)
                self.lineEdit_compressor_node_id.setText(str(selected_nodes[0]))
                self.get_existing_compressor_info(node_id)
                return

            self.pushButton_plot_filtered_criteria.setDisabled(False)
            self.lineEdit_nozzle_id.setText(str(selected_nodes[0]))

            fluids = self.get_fluids_from_node(node_id)
            if len(fluids) != 1:
                return

            fluid = fluids[0]
            if not isinstance(fluid, Fluid):
                return
            
            diameters = self.get_diameters_from_node(node_id)
            if len(diameters) != 1:
                return
            
            D_in = round(diameters[0], 6)
            C_0 = round(fluid.speed_of_sound, 6)
            P_L = round(convert_pressure_unit(fluid.pressure, "Pa (a)", "bar (a)"), 6)

            self.lineEdit_speed_of_sound.setText(str(C_0))
            self.lineEdit_line_pressure.setText(str(P_L))
            self.lineEdit_internal_diameter.setText(str(D_in))

    def reset_unfiltered_fields(self):
        self.lineEdit_compressor_node_id.clear()
        self.lineEdit_pressure_ratio.clear()
        self.lineEdit_unfiltered_criteria.clear()

    def reset_filtered_fields(self):
        self.lineEdit_nozzle_id.clear()
        self.lineEdit_internal_diameter.clear()
        self.lineEdit_line_pressure.clear()
        self.lineEdit_speed_of_sound.clear()

    def get_existing_compressor_info(self, node_id: int):
        comp_data = self.properties._get_property("reciprocating_compressor_excitation", node_ids=node_id)
        if isinstance(comp_data, dict):
            self.update_compressor_data(comp_data)

    def update_compressor_data(self, stage_data: dict):

        self.comp_parameters = stage_data.get("parameters", dict())
        if not self.comp_parameters:
            return

        if not isinstance(self.comp_parameters, dict):
            return

        pressure_ratio = self.comp_parameters.get("pressure_ratio")
        unfiltered_criteria = min([7, 3 * pressure_ratio])

        self.lineEdit_pressure_ratio.setText(str(pressure_ratio))
        self.lineEdit_unfiltered_criteria.setText(str(round(unfiltered_criteria, 6)))

    def get_acoustic_pressure(self, node_id: int):
        response = get_acoustic_frf(self.preprocessor, self.nodal_solution, node_id)
        if complex(0) in response:
            response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def get_fluids_from_node(self, node_id: int) -> list[Fluid]:
        fluids = list()
        for element in  self.model.preprocessor.structural_elements_connected_to_node.get(node_id, list()):
            fluid = element.fluid
            if fluid in fluids:
                continue

            fluids.append(fluid)

        return fluids
    
    def get_diameters_from_node(self, node_id: int) -> list[float]:
        diameters = list()
        for element in  self.model.preprocessor.structural_elements_connected_to_node.get(node_id, list()):
            cross_section = element.cross_section
            if cross_section.section_type_label != "pipe":
                continue

            section_info = cross_section.section_info
            if not isinstance(section_info, PipeCrossSection):
                continue

            diameter = round(convert_length_unit(section_info.inside_diameter, "m", "mm"), 6)
            if diameter in diameters:
                continue

            diameters.append(diameter)

        return diameters

    def plot_unfiltered_criteria(self):

        self.model_results.clear()
        if not self.comp_parameters:
            return

        # load the compressor parameters
        pressure_unit = self.comp_parameters.get("pressure_unit", "Pa (a)")
        pressure_ratio = self.comp_parameters.get("pressure_ratio")

        node_ids = app().main_window.list_selected_nodes()
        if len(node_ids) != 1:
            title = "Invalid selection"
            message = "Select the node where the compressor excitation has been "
            message += "applied to process the pulsation criterion properly. "
            message += "This pulsation criterion should be evaluated in nodes near "
            message += "the compressor cylinder flange."
            PrintMessageInput([error_title, title, message])
            return

        node_id = node_ids[0]

        fluids = self.get_fluids_from_node(node_id)
        if len(fluids) != 1:
            return

        fluid = fluids[0]
        if not isinstance(fluid, Fluid):
            return

        # get the nodal pressure
        Xf = self.get_acoustic_pressure(node_id)

        # process the iFFT of the nodal pressure
        time_vector, acoustic_pressure = process_ifft_from_one_sided_spectrum_signal(self.frequencies, Xf)

        # convert the pressure units
        acoustic_pressure_conv = convert_pressure_unit(acoustic_pressure, "Pa (a)", "bar (a)")

        key = ("acoustic_pressure", (node_id))
        legend_label = "Acoustic pressure at node {}".format(node_id)
        self.title = "Maximum Allowable Pressure Pulsation at Compressor \nCylinder Flanges"

        self.model_results[key] = { 
            "x_data" : time_vector,
            "y_data" : acoustic_pressure_conv,
            "x_label" : "Time [s]",
            "y_label" : "Acoustic pressure",
            "title" : self.title,
            "data_information" : legend_label,
            "legend" : legend_label,
            "unit" : "bar (a)",
            "color" : [0, 0, 1],
            "linestyle" : "-",
        }

        # mean line fluid pressure
        P_L = acoustic_pressure_conv = convert_pressure_unit(fluid.pressure, "Pa (a)", "bar (a)")

        # NOTE: P_cf is the maximum allowable unfiltered peak-to-peak pulsation level, as a 
        # percentage of average absolute line pressure at the compressor cylinder flange.
        P_cf = min([7, 3 * pressure_ratio]) / 100

        # pulsation recommended limits in bar (a)
        pulsation_criterion_peak = P_cf * P_L * (1 / 2)

        key = ("allowable pulsation limits (upper)", (None))
        legend_label_upper = "Allowable pulsation (upper bound)"

        self.model_results[key] = { 
            "x_data" : time_vector,
            "y_data" : pulsation_criterion_peak,
            "x_label" : "Time [s]",
            "y_label" : "Acoustic pressure",
            "title" : self.title,
            "data_information" : legend_label_upper,
            "legend" : legend_label_upper,
            "unit" : "bar (a)",
            "color" : [0.7, 0, 0],
            "linestyle" : "-",
        }

        key = ("allowable pulsation limits (lower)", (None))
        legend_label_lower = "Allowable pulsation (lower bound)"

        self.model_results[key] = { 
            "x_data" : time_vector,
            "y_data" : -pulsation_criterion_peak,
            "x_label" : "Time [s]",
            "y_label" : "Acoustic pressure",
            "title" : self.title,
            "data_information" : legend_label_lower,
            "legend" : legend_label_lower,
            "unit" : "bar (a)",
            "color" : [1, 0, 0],
            "linestyle" : "-",
        }

        self.plotter = FrequencyResponsePlotter()
        self.plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.plotter.data_format_changed_callback()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def plot_filtered_criteria(self):

        self.model_results.clear()

        # load the compressor parameters
        pressure_unit = self.comp_parameters.get("pressure_unit", "Pa (a)")

        node_ids = app().main_window.list_selected_nodes()
        if len(node_ids) != 1:
            title = "Invalid selection"
            message = "Select the node where the compressor excitation has been "
            message += "applied to process the pulsation criterion properly. "
            message += "This pulsation criterion should be evaluated in nodes near "
            message += "the compressor cylinder flange."
            PrintMessageInput([error_title, title, message])
            return

        node_id = node_ids[0]

        fluids = self.get_fluids_from_node(node_id)
        if len(fluids) != 1:
            return

        fluid = fluids[0]
        if not isinstance(fluid, Fluid):
            return

        diameters = self.get_diameters_from_node(node_id)
        if len(diameters) != 1:
            return

        # get the nodal pressure (peak-to-peak)
        acoustic_pressure_pp = 2 * self.get_acoustic_pressure(node_id)

        # convert the pressure units
        acoustic_pressure_pp_conv = convert_pressure_unit(acoustic_pressure_pp, "Pa (a)", "bar (a)")

        key = ("acoustic_pressure", (node_id))
        legend_label = "Acoustic pressure at node {}".format(node_id)
        self.title = "Allowable Pulsation Levels at and Beyond Line-side \nConnections of Pulsation Suppression Devices"      

        self.model_results[key] = { 
            "x_data" : self.frequencies,
            "y_data" : acoustic_pressure_pp_conv,
            "x_label" : "Frequency [Hz]",
            "y_label" : "Cylinder acoustic pressure",
            "title" : self.title,
            "data_information" : legend_label,
            "legend" : legend_label,
            "unit" : "bar (a) (peak-to-peak)",
            "color" : [0, 0, 1],
            "linestyle" : "-",
        }

        # absolute average line pressure P_L in bar(a)
        P_L = convert_pressure_unit(fluid.pressure, "Pa (a)", "bar (a)")

        # fluid speed of sound in m/s
        C_0 = fluid.speed_of_sound

        # pipe inside diameter in mm
        D_in = diameters[0]

        # define the frequency vector for filtered pulsation criteria
        df = 0.5
        f_max = self.frequencies[-1]
        freq = np.arange(df, f_max + df, df)

        # allowable peak-to-peak pulsation levels in bar(a) as percentage of the average mean line pressure
        P_1 = 400 * ((C_0 / (350 * P_L * D_in * freq))**(1/2))

        # the prestudy factor to penalize the allowable pulsation levels
        factor = 0.7 if self.checkBox_prestudy_analysis.isChecked() else 1.0

        legend_label = "Filtered criteria"
        key = ("filtered_criteria", (node_id))

        self.model_results[key] = { 
            "x_data" : freq,
            "y_data" : factor * P_1 * (P_L / 100),
            "x_label" : "Frequency [Hz]",
            "y_label" : "Cylinder acoustic pressure",
            "title" : self.title,
            "data_information" : legend_label,
            "legend" : legend_label,
            "unit" : "bar (a) (peak-to-peak)",
            "color" : [1, 0, 0],
            "linestyle" : "-",
        }

        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)