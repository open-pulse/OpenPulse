from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import SetFluidInputSimplified

from pulse.model.properties.fluid import Fluid

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class PulsationDamperCalculatorInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/acoustic/pulsation_damper_calculator_inputs.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._load_pump_data(**kwargs)

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.isentropic_exponent = 1.4
        self.residual_pulsation = 0.01
        self.pressure_ratio = 0.8

        self.keep_window_open = True

        self.selected_fluid = None

        self.state_properties = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_compression_type: QComboBox
        self.comboBox_fluid_data_source: QComboBox
        self.comboBox_volume_unit: QComboBox
        self.comboBox_pressure_units: QComboBox
        self.comboBox_temperature_units: QComboBox

        # QDoubleSpinBox
        self.doubleSpinBox_pressure_ratio: QDoubleSpinBox
        self.doubleSpinBox_isentropic_exponent: QDoubleSpinBox
        self.doubleSpinBox_residual_pulsation: QDoubleSpinBox

        # QLabel
        self.label_polytropic_exponent: QLabel
        self.label_effective_volume_unit: QLabel
        self.label_volume_avg_pressure_unit: QLabel

        # QLineEdit
        self.lineEdit_fluctuating_volume: QLineEdit
        self.lineEdit_effective_volume: QLineEdit
        self.lineEdit_volume_at_average_pressure: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_pressure: QLineEdit
        self.lineEdit_temperature: QLineEdit

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_get_fluid: QPushButton
        #
        self.pushButton_confirm.setVisible(False)
        self.pushButton_cancel.setText("Exit")

    def _create_connections(self):
        #
        self.comboBox_compression_type.currentIndexChanged.connect(self.change_compression_type_callback)
        self.comboBox_volume_unit.currentIndexChanged.connect(self.update_volume_unit_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.load_state_properties)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.load_state_properties)
        #
        self.doubleSpinBox_isentropic_exponent.valueChanged.connect(self.calculate_effective_volume)
        self.doubleSpinBox_residual_pulsation.valueChanged.connect(self.calculate_effective_volume)   
        self.doubleSpinBox_pressure_ratio.valueChanged.connect(self.calculate_effective_volume)   
        #
        self.lineEdit_fluctuating_volume.textChanged.connect(self.calculate_effective_volume)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified(state_properties = self.state_properties)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()

        if isinstance(self.selected_fluid, Fluid):

            self.fluid_dialog.close()
            if self.selected_fluid.name in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys():
                self.comboBox_fluid_data_source.setCurrentIndex(0)

            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.doubleSpinBox_isentropic_exponent.setValue(self.selected_fluid.isentropic_exponent)

    def change_compression_type_callback(self):

        self.doubleSpinBox_isentropic_exponent.blockSignals(True)

        if self.comboBox_compression_type.currentIndex() == 0:
            self.doubleSpinBox_isentropic_exponent.setEnabled(True)
            self.label_polytropic_exponent.setText("Polytropic exponent:")

            if isinstance(self.selected_fluid, Fluid):
                self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
                self.doubleSpinBox_isentropic_exponent.setValue(self.selected_fluid.isentropic_exponent)

        else:
            self.doubleSpinBox_isentropic_exponent.setValue(1.000)
            self.doubleSpinBox_isentropic_exponent.setEnabled(False)
            self.label_polytropic_exponent.setText("Polytropic exponent:")

        self.doubleSpinBox_isentropic_exponent.blockSignals(False)
        self.calculate_effective_volume()

    def _load_pump_data(self, **kwargs):

        dV = kwargs.get('fluctuating_volume', None)
        if isinstance(dV, (float | int)):
            self.lineEdit_fluctuating_volume.setText(f"{dV : 2.8e}")

        self.state_properties = kwargs.get("state_properties", dict())
        if self.state_properties:
            self.load_state_properties()

    def load_state_properties(self):
        if self.state_properties:

            pressure_Pa = self.state_properties["pressure"]
            temperature_K = self.state_properties["temperature"]

            tu_index = self.comboBox_temperature_units.currentIndex()
            if tu_index == 0:
                temperature_C = temperature_K - 273.15
                self.lineEdit_temperature.setText(f"{temperature_C}")

            else:
                self.lineEdit_temperature.setText(f"{temperature_K}")

            pu_index = self.comboBox_pressure_units.currentIndex()
            if pu_index >= 4:
                pressure_Pa_g = pressure_Pa - 101325

            if pu_index == 0:
                pressure_value = pressure_Pa / 9.80665e4

            elif pu_index == 1:
                pressure_value = pressure_Pa / 1e5

            elif pu_index == 2:
                pressure_value = pressure_Pa / 1e3                

            elif pu_index == 3:
                pressure_value = pressure_Pa / 1

            elif pu_index == 4:
                pressure_value = pressure_Pa_g / 9.80665e4

            elif pu_index == 5:
                pressure_value = pressure_Pa_g / 1e5

            elif pu_index == 6:
                pressure_value = pressure_Pa_g / 1e3                

            elif pu_index == 7:
                pressure_value = pressure_Pa_g / 1

            self.lineEdit_pressure.setText(f"{pressure_value : 2.8e}")

    def update_volume_unit_callback(self):

        index = self.comboBox_volume_unit.currentIndex()

        if index == 0:
            unit_label = "m³"
        elif index == 1:
            unit_label = "cm³"
        else:
            unit_label = "L"

        self.label_effective_volume_unit.setText(f"[{unit_label}]")
        self.label_volume_avg_pressure_unit.setText(f"[{unit_label}]")
        self.calculate_effective_volume()

    def calculate_effective_volume(self):

        dV = self.check_input_parameters(self.lineEdit_fluctuating_volume, "Fluctuating volume of reciprocating pump")
        if dV is None:
            self.lineEdit_effective_volume.setText("")
            self.lineEdit_volume_at_average_pressure.setText("")
            return
        
        phi = self.doubleSpinBox_pressure_ratio.value()
        x = self.doubleSpinBox_residual_pulsation.value() / 100
        k = self.doubleSpinBox_isentropic_exponent.value()

        V0 = dV / ((phi/(1-x))**(1/k) - (phi/(1+x))**(1/k))
        Vm = V0 * (phi**(1/k))

        unit_label = self.comboBox_volume_unit.currentText()

        if unit_label == " cubic centimeters":
            V0 = V0 * 1e6
            Vm = Vm * 1e6

        elif unit_label == " liters":
            V0 = V0 * 1e3
            Vm = Vm * 1e6

        self.lineEdit_effective_volume.setText(f"{V0 : 2.8e}")
        self.lineEdit_volume_at_average_pressure.setText(f"{Vm : 2.8e}")

    def attribute_callback(self):
        pass

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        title = "Input error"
        message = ""

        value_string = lineEdit.text()

        if value_string != "":

            value_string = value_string.replace(",", ".")

            try:

                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string)

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."

            except Exception:
                return None
                message = f"You have typed an invalid value to the {label}."

        else:
            message = f"None value has been typed to the {label}."
            return None

        if message != "":
            self.hide()
            PrintMessageInput([window_title_1, title, message])
            return None
        
        return value
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)