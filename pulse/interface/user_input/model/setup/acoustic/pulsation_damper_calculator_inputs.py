from enum import IntEnum

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.pulsation_damper_calculator_inputs_ui import (
    PulsationDamperCalculatorInputs_UI,
)
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import (
    SetFluidInputSimplified,
)
from pulse.interface.user_input.numeric_checks.double_validator import (
    StrictDoubleValidator,
)
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    PressureUnits,
    TemperatureUnits,
    VolumeUnits,
    convert_pressure_unit,
    convert_temperature_unit,
    convert_volume_unit,
    pressure_units_labels,
    temperature_units_labels,
    volume_units_labels,
)
from pulse.model.properties.fluid import Fluid


class CompressionType(IntEnum):
    ISENTROPIC = 0
    ISOTHERMAL = 1


class PulsationDamperCalculatorInputs(PulsationDamperCalculatorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()
        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._config_widgets()
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
        self.selected_fluid = None
        self.isentropic_exponent = 1.4
        self.residual_pulsation = 0.01
        self.pressure_ratio = 0.8

        self.keep_window_open = True

        self.state_properties = dict()

    def _config_widgets(self):

        self.default_stylesheet = self.lineEdit_pressure.styleSheet()
        # self.pushButton_confirm.setVisible(False)

        self._load_units_labels()
        # self.configure_dynamic_validators()
        # self.configure_static_validators()

    def _load_units_labels(self):

        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()
        self.comboBox_temperature_units.clear()
        self.comboBox_volume_units.clear()

        # add temperature and pressure labels into unit combo boxes
        self.comboBox_pressure_units.addItems(pressure_units_labels)
        self.comboBox_temperature_units.addItems(temperature_units_labels)
        self.comboBox_volume_units.addItems(volume_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("bar (a)")
        self.comboBox_temperature_units.setCurrentText("°C")
        self.comboBox_volume_units.setCurrentText("m³")

    def configure_dynamic_validators(self):

        # adjust temperature bounds (t_min -> zero absolute)
        t_min = 0
        t_max = 1e4
        if self.comboBox_temperature_units.currentIndex() == TemperatureUnits.CELSIUS:
            t_min = -273.15
        elif self.comboBox_temperature_units.currentIndex() == TemperatureUnits.FARENHEIT:
            t_min = -459.67

        # adjust pressure bounds (p_min -> perfect vacuum)      
        p_min = 0 
        p_max = 1e8

        punit_index = self.comboBox_pressure_units.currentIndex()
        if punit_index == PressureUnits.Pa_g:
            p_min = -101325

        elif punit_index == PressureUnits.kPa_g:
            p_min = -101.325

        elif punit_index == PressureUnits.bar_g:
            p_min = -1.101325
            p_max = 2e3

        elif punit_index == PressureUnits.kgf_cm2_g:
            p_min = -(9.80665*1e4)

        elif punit_index == PressureUnits.psi_g:
            p_min = -(0.45359237*9.80665) / (0.0254**2)

        elif punit_index == PressureUnits.ksi_g:
            p_min = -(0.45359237*9.80665) / (1e3 * (0.0254**2))
            p_max = 1e3

        # configure validator for pressure and temeperature inputs
        self.lineEdit_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))

    def configure_static_validators(self):

        # configure validator for volume-related parameters
        volume_validator = StrictDoubleValidator(1e-6, 1e8, 8)
        self.lineEdit_fluctuating_volume.setValidator(volume_validator)
        self.lineEdit_effective_volume.setValidator(volume_validator)
        self.lineEdit_volume_at_average_pressure.setValidator(volume_validator)

    def _create_connections(self):
        #
        self.comboBox_compression_type.currentIndexChanged.connect(self.change_compression_type_callback)
        self.comboBox_volume_units.currentIndexChanged.connect(self.update_volume_unit_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        #
        self.doubleSpinBox_isentropic_exponent.valueChanged.connect(self.calculate_effective_volume)
        self.doubleSpinBox_residual_pulsation.valueChanged.connect(self.calculate_effective_volume)   
        self.doubleSpinBox_pressure_ratio.valueChanged.connect(self.calculate_effective_volume)   
        #
        self.lineEdit_fluctuating_volume.textChanged.connect(self.calculate_effective_volume)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified(state_properties = self.state_properties)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if not isinstance(self.selected_fluid, Fluid):
            return

        self.fluid_dialog.close()
        self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
        self.doubleSpinBox_isentropic_exponent.setValue(self.selected_fluid.isentropic_exponent)

    def change_compression_type_callback(self):

        self.doubleSpinBox_isentropic_exponent.blockSignals(True)

        if self.comboBox_compression_type.currentIndex() == CompressionType.ISENTROPIC:
            self.doubleSpinBox_isentropic_exponent.setEnabled(True)
            self.label_polytropic_exponent.setText("Polytropic exponent:")

            if isinstance(self.selected_fluid, Fluid):
                self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
                self.doubleSpinBox_isentropic_exponent.setValue(self.selected_fluid.isentropic_exponent)

        elif self.comboBox_compression_type.currentIndex() == CompressionType.ISOTHERMAL:
            self.doubleSpinBox_isentropic_exponent.setValue(1.000)
            self.doubleSpinBox_isentropic_exponent.setEnabled(False)
            self.label_polytropic_exponent.setText("Polytropic exponent:")

        self.doubleSpinBox_isentropic_exponent.blockSignals(False)
        self.calculate_effective_volume()

    def _load_pump_data(self, **kwargs):

        dV = kwargs.get('fluctuating_volume', None)
        if isinstance(dV, (float | int)):
            self.lineEdit_fluctuating_volume.setText(f"{dV : .8e}")

        self.state_properties = kwargs.get("state_properties", dict())
        if self.state_properties:
            self.load_state_properties()

    def load_state_properties(self):
        if not self.state_properties:
            return
        
        connection_type = self.state_properties.get("connection_type")

        if connection_type == "discharge":
            pressure = self.state_properties.get("discharge_pressure")
            temperature = self.state_properties.get("discharge_temperature")
        else:
            pressure = self.state_properties.get("suction_pressure")
            temperature = self.state_properties.get("suction_temperature")

        pressure_unit = self.state_properties.get("pressure_unit")
        temperature_unit = self.state_properties.get("temperature_unit")

        self.comboBox_pressure_units.setCurrentText(pressure_unit)
        self.comboBox_temperature_units.setCurrentText(temperature_unit)

        pressure_Pa = convert_pressure_unit(pressure, pressure_unit, "Pa")
        temperature_K = convert_temperature_unit(temperature, temperature_unit, "K")

        self.lineEdit_temperature.setText(f"{temperature_K}")
        self.lineEdit_pressure.setText(f"{pressure_Pa : .8e}")

    def update_volume_unit_callback(self):

        index = self.comboBox_volume_units.currentIndex()
        if index == VolumeUnits.CUBIC_METER:
            unit_label = "m³"
        elif index == VolumeUnits.CUBIC_CENTIMETER:
            unit_label = "cm³"
        elif index == VolumeUnits.LITER:
            unit_label = "L"
        else:
            return

        self.label_effective_volume_unit.setText(f"[{unit_label}]")
        self.label_volume_avg_pressure_unit.setText(f"[{unit_label}]")

        self.calculate_effective_volume()

    def calculate_effective_volume(self):

        if self.lineEdit_fluctuating_volume.text() == "":
            self.lineEdit_fluctuating_volume.setFocus()
            self.lineEdit_fluctuating_volume.setStyleSheet("border: 2px solid red")
        
        else:
            _style_sheet = self.lineEdit_fluctuating_volume.styleSheet()
            if _style_sheet != self.default_stylesheet:
                self.lineEdit_fluctuating_volume.setStyleSheet(self.default_stylesheet)
                return

        dV_m3 = float(self.lineEdit_fluctuating_volume.text())
        if dV_m3 is None:
            self.lineEdit_effective_volume.setText("")
            self.lineEdit_volume_at_average_pressure.setText("")
            return

        phi = self.doubleSpinBox_pressure_ratio.value()
        x = self.doubleSpinBox_residual_pulsation.value() / 100
        k = self.doubleSpinBox_isentropic_exponent.value()

        V0_m3 = dV_m3 / ((phi / (1 - x))**(1 / k) - (phi / (1 + x))**(1 / k))
        Vm_m3 = V0_m3 * (phi**(1 / k))

        volume_unit = self.comboBox_volume_units.currentText()
        V0 = convert_volume_unit(V0_m3, "m³", volume_unit)
        Vm = convert_volume_unit(Vm_m3, "m³", volume_unit)

        self.lineEdit_effective_volume.setText(f"{V0 : .8e}")
        self.lineEdit_volume_at_average_pressure.setText(f"{Vm : .8e}")

    def attribute_callback(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)