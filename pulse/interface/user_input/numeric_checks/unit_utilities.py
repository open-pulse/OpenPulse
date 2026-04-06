from enum import IntEnum
from pint import UnitRegistry

class PressureUnits(IntEnum):
    Pa_a = 0
    kPa_a = 1
    atm_a = 2
    bar_a = 3
    kgf_cm2_a = 4
    psi_a = 5
    ksi_a = 6
    Pa_g = 7
    kPa_g = 8
    atm_g = 9
    bar_g = 10
    kgf_cm2_g = 11
    psi_g = 12
    ksi_g = 13

class TemperatureUnits(IntEnum):
    KELVIN = 0
    CELSIUS = 1
    FARENHEIT = 2

class VolumeUnits(IntEnum):
    CUBIC_METER = 0
    CUBIC_CENTIMETER = 1
    LITER = 2

pressure_units_labels = [
    "Pa (a)",
    "kPa (a)",
    "atm (a)",
    "bar (a)",
    "kgf/cm² (a)",
    "psi (a)",
    "ksi (a)",
    "Pa (g)",
    "kPa (g)",
    "atm (g)",
    "bar (g)",
    "kgf/cm² (g)",
    "psi (g)",
    "ksi (g)",
]

temperature_units_labels = [
    "K",
    "°C",
    "°F",
]

volume_units_labels = [
    "m³",
    "cm³",
    "L",
]

# instantiate the unit registry
u_reg = UnitRegistry()


def convert_temperature_unit(value: float, input_unit: str, output_unit: str | None=None) -> float:
    """
    This function converts the temperature, scaled in 'input_unit',
    to a temperature scaled in 'output_unit'.

    Parameters
    ----------
    value: float
    The temperature value.

    input_unit: str 
    The input temperature unit. Allowable units are: K, °C and °F.

    output_unit: str or None, optional
    The output temperature unit. Allowable units are: K, °C and °F.
    """

    unit_map = {
        "K" : "kelvin",
        "°C" : "degC",
        "°F" : "degF",
        }

    if input_unit == output_unit:
        return value

    temperature = u_reg.Quantity(value, unit_map.get(input_unit))
    if output_unit is None:
        return temperature.magnitude

    return temperature.to(unit_map.get(output_unit)).magnitude


def convert_pressure_unit(value: float, input_unit: str, output_unit: str | None=None):
    """
    This function converts the pressure, scaled in 'input_unit',
    to a pressure scaled in 'output_unit'.

    Parameters
    ----------
    value: float
    The pressure value.

    input_unit: str 
    The input pressure unit. Allowable units are: K, °C and °F.

    output_unit: str or None, optional
    The output pressure unit. Allowable units are: K, °C and °F.
    """

    unit_map = {
        "Pa" : "pascal",
        "kPa" : "kPa",
        "atm" : "atm",
        "bar" : "bar",
        "kgf/cm²" : "kgf/cm²",
        "psi" : "psi",
        "ksi" : "ksi",
        }

    _input_unit = input_unit
    for suffix in ["(a)", "(g)"]:
        if suffix in input_unit:
            _input_unit = input_unit.split(f" {suffix}")[0]
            break

    pressure = u_reg.Quantity(value, unit_map.get(_input_unit))

    if "(g)" in input_unit:
        pressure += u_reg.Quantity(1, "atm")

    if output_unit is None:
        return pressure.magnitude

    if "(g)" in output_unit:
        pressure -= u_reg.Quantity(1, "atm")

    if input_unit == output_unit:
        return pressure.magnitude
    
    _output_unit = output_unit
    for suffix in ["(a)", "(g)"]:
        if suffix in output_unit:
            _output_unit = output_unit.split(f" {suffix}")[0]
            break

    return pressure.to(unit_map.get(_output_unit)).magnitude


def convert_volume_unit(value: float, input_unit: str, output_unit: str | None=None) -> float:
    """
    This function converts the volume, scaled in 'input_unit',
    to a volume scaled in 'output_unit'.

    Parameters
    ----------
    value: float
    The volume value.

    input_unit: str 
    The input volume unit. Allowable units: m³, m**3, m^3, cubic meters, cm³, cm**3, cm^3, cubic centimeters, L, l, litter.

    output_unit: str or None, optional
    The output volume unit. Allowable units: same as input.
    """

    unit_map = {
        "m³" : "m**3",
        "m**3" : "m**3",
        "m^3" : "m**3",
        "cubic meters" : "m**3",
        "cm³" : "cm**3",
        "cm**3" : "cm**3",
        "cm^3" : "cm**3",
        "cubic centimeters" : "cm**3",
        "L" : "liter",
        "l" : "liter",
        "liters" : "liter",
        }

    if input_unit == output_unit:
        return value

    temperature = u_reg.Quantity(value, unit_map.get(input_unit))
    if output_unit is None:
        return temperature.magnitude

    return temperature.to(unit_map.get(output_unit)).magnitude