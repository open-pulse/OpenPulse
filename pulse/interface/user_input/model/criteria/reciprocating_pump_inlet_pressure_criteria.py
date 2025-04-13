from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.model.properties.fluid import Fluid
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from pulse.utils.signal_processing_utils import process_iFFT_of_onesided_signal

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4

class ReciprocatingPumpInletPressureCriteriaInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "criterias/reciprocating_pump_inlet_pressure_criteria_widget.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()        
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):
        self.frequencies = self.model.frequencies
        self.solution = self.project.get_acoustic_solution()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_line_ids: QComboBox
        self.comboBox_pressure_units: QComboBox
        self.comboBox_temperature_units: QComboBox

        # QLabel
        self.label_selected_id: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_fluid_name: QLineEdit
        self.lineEdit_vapor_pressure : QLineEdit
        self.lineEdit_temperature: QLineEdit
        #
        self.lineEdit_fluid_name.setDisabled(True)
        # self.lineEdit_vapor_pressure.setDisabled(True)
        self.lineEdit_temperature.setDisabled(True)

        # QPushButton
        self.pushButton_plot_criteria : QPushButton

    def _create_connections(self):
        #
        self.comboBox_pressure_units.currentIndexChanged.connect(self.update_pressure_and_temperature)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.update_pressure_and_temperature)
        #
        self.pushButton_plot_criteria.clicked.connect(self.plot_inlet_pressure_criteria)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):


        selected_nodes = app().main_window.list_selected_nodes()
        line_ids = self.preprocessor.get_line_from_node_id(selected_nodes)

        if len(selected_nodes) == 1:

            node_id = selected_nodes[0]
            pump_data = self.properties._get_property("reciprocating_pump_excitation", node_ids=int(node_id))
            if pump_data is None:
                self.reset_input_fields()
                return

            if isinstance(pump_data, dict):
                if pump_data["connection_type"] == "discharge":
                    self.reset_input_fields()
                    return

            if len(line_ids) > 0:
                self.comboBox_line_ids.clear()
                for line_id in line_ids:
                    self.comboBox_line_ids.addItem(f"      {line_id}")

            fluid = self.get_fluid_from_line()
            if fluid is None:
                return

            self.pushButton_plot_criteria.setDisabled(False)
            self.lineEdit_fluid_name.setText(fluid.name)
            self.lineEdit_selected_id.setText(str(selected_nodes[0]))

            self.update_pressure_and_temperature()

    def get_acoustic_pressure(self, node_id: int):

        response = get_acoustic_frf(self.preprocessor, self.solution, node_id)
        if complex(0) in response:
            response += np.ones(len(response), dtype=float) * 1e-12

        return response

    def plot_inlet_pressure_criteria(self):

        node_ids = app().main_window.list_selected_nodes()

        if len(node_ids) == 1:

            node_id = node_ids[0]
            acoustic_pressure = self.get_acoustic_pressure(node_id)

            # processes the inverse Fourier transform of the one-sided spectrum
            df = self.frequencies[1] - self.frequencies[0]
            time, pressure_time = process_iFFT_of_onesided_signal(df, acoustic_pressure, remove_avg=True)

            fluid = self.get_fluid_from_line()
            if fluid is None:
                return

            self.model_results = dict()
            title = "Inlet Pressure vs Liquid Vapor Pressure"       
            legend_label = "Acoustic pressure at node {}".format(node_id)

            key = ("acoustic_pressure", (node_id))

            line_pressure = fluid.pressure
            vapor_pressure = self.get_pressure_in_Pa()

            pressure_kPa = (pressure_time + line_pressure) / 1e3

            self.model_results[key] = { 
                                        "x_data" : time,
                                        "y_data" : pressure_kPa,
                                        "x_label" : "Time [s]",
                                        "y_label" : "Pressure",
                                        "title" : title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : "kPa",
                                        "color" : [0,0,0],
                                        "linestyle" : "-" 
                                    }

            # minimum inlet pressure levels in kPa
            P_min = ((vapor_pressure + 0.03 * line_pressure) / 1e3) + 0.01

            legend_label = "Inlet pressure criteria"

            key = ("pressure_criteria", (node_id))

            self.model_results[key] = { 
                                        "x_data" : time,
                                        "y_data" : P_min * np.ones_like(time),
                                        "x_label" : "Time [s]",
                                        "y_label" : "Pressure",
                                        "title" : title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : "kPa",
                                        "color" : [1,0,0],
                                        "linestyle" : "-"  
                                       }

            self.plotter = FrequencyResponsePlotter()
            self.plotter._set_model_results_data_to_plot(self.model_results)

    def get_fluid_from_line(self) -> (Fluid | None):

        line_id = int(self.comboBox_line_ids.currentText().replace(" ", ""))

        fluid = self.model.properties._get_property("fluid", line_id=line_id)
        if fluid is None:
            return None

        return fluid
    
    def update_pressure_and_temperature(self):

        fluid = self.get_fluid_from_line()
        if isinstance(fluid, Fluid):

            temperature_K = fluid.temperature

            if self.comboBox_temperature_units.currentIndex() == 0:
                temperature = temperature_K - 273.15
            else:
                temperature = temperature_K

            self.lineEdit_temperature.setText(f"{temperature : .4f}")

            vapor_pressure_Pa = fluid.vapor_pressure

            if vapor_pressure_Pa is None:
                if self.lineEdit_vapor_pressure.text() != "":

                    try:
                        _vapor_pressure = self.lineEdit_vapor_pressure.text().replace(",", ".")
                        vapor_pressure = float(_vapor_pressure)
                        self.lineEdit_vapor_pressure.setText(_vapor_pressure)

                    except:
                        self.lineEdit_vapor_pressure.setText("")
                        return

                return

            pressure_unit = self.comboBox_pressure_units.currentText()

            if "(g)" in pressure_unit:
                vapor_pressure_Pa -= 101325

            if "kgf/cm²" in pressure_unit:
                vapor_pressure = vapor_pressure_Pa / 9.80665e4

            elif "bar" in pressure_unit:
                vapor_pressure = vapor_pressure_Pa / 1e5

            elif "atm" in pressure_unit:
                vapor_pressure = vapor_pressure_Pa / 101325

            elif "kPa" in pressure_unit:
                vapor_pressure = vapor_pressure_Pa / 1e3

            else:
                vapor_pressure = vapor_pressure_Pa

            if pressure_unit in ["Pa (a)", "Pa (g)"]:
                str_pressure = f"{vapor_pressure : .8e}"

            else:
                str_pressure = f"{vapor_pressure : .6f}"

            self.lineEdit_vapor_pressure.setText(str_pressure)

    def get_pressure_in_Pa(self):

        pressure_unit = self.comboBox_pressure_units.currentText()

        try:
            _vapor_pressure = self.lineEdit_vapor_pressure.text().replace(",", ".")
            vapor_pressure = float(_vapor_pressure)
            self.lineEdit_vapor_pressure.setText(_vapor_pressure)
        except:
            return None, None

        if "kgf/cm²" in pressure_unit:
            vapor_pressure_Pa = vapor_pressure * 9.80665e4

        elif "bar" in pressure_unit:
            vapor_pressure_Pa = vapor_pressure * 1e5

        elif "atm" in pressure_unit:
            vapor_pressure_Pa = vapor_pressure * 101325

        elif "kPa" in pressure_unit:
            vapor_pressure_Pa = vapor_pressure * 1e3

        else:
            vapor_pressure_Pa = vapor_pressure

        if "(g)" in pressure_unit:
            vapor_pressure_Pa += 101325

        return vapor_pressure_Pa

    def reset_input_fields(self):
        self.lineEdit_selected_id.setText("")
        self.lineEdit_fluid_name.setText("")
        self.lineEdit_vapor_pressure.setText("")
        self.lineEdit_temperature.setText("")
        self.pushButton_plot_criteria.setDisabled(True)