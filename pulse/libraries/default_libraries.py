import configparser

from pulse import app

def default_material_library():
    config = configparser.ConfigParser()

    config["1"] = {
        "name": "Steel",
        "identifier": 1,
        "color": "[170,170,170]",  # Light Gray
        "density": 7860,
        "elasticity_modulus": 210,
        "poisson_ratio": 0.3,
        "thermal_expansion_coefficient": 1.2e-5,
    }

    config["2"] = {
        "name": "Stainless_steel",
        "identifier": 2,
        "color": "[126,46,31]",  # Wood color
        "density": 7750,
        "elasticity_modulus": 193,
        "poisson_ratio": 0.31,
        "thermal_expansion_coefficient": 1.7e-5,
    }

    config["3"] = {
        "name": "Ni-Co-Cr_alloy",
        "identifier": 3,
        "color": "[0,255,255]",  # Cyan
        "density": 8220,
        "elasticity_modulus": 212,
        "poisson_ratio": 0.315,
        "thermal_expansion_coefficient": 1.2e-5,
    }

    config["4"] = {
        "name": "Cast_iron",
        "identifier": 4,
        "color": "[50,50,50]",  # Dark Grey
        "density": 7200,
        "elasticity_modulus": 110,
        "poisson_ratio": 0.28,
        "thermal_expansion_coefficient": 1.1e-5,
    }

    config["5"] = {
        "name": "Aluminum",
        "identifier": 5,
        "color": "[255,255,255]",  # White
        "density": 2770,
        "elasticity_modulus": 71,
        "poisson_ratio": 0.333,
        "thermal_expansion_coefficient": 2.3e-5,
    }

    config["6"] = {
        "name": "Brass",
        "identifier": 6,
        "color": "[181,166,66]",  # Brass color
        "density": 8150,
        "elasticity_modulus": 96,
        "poisson_ratio": 0.345,
        "thermal_expansion_coefficient": 1.9e-5,
    }

    app().pulse_file.write_material_library_in_file(config)


def default_fluid_library():

    # Reference: RefProp v10.0

    config = configparser.ConfigParser()

    config["1"] = {
        "name": "Air",
        "identifier": 1,
        "color": "[255,170,127]",  # Blue
        "density": 1.204263,
        "speed_of_sound": 343.395034,
        "isentropic_exponent": 1.401985,
        "thermal_conductivity": 0.025503,
        "specific_heat_Cp": 1006.400178,
        "dynamic_viscosity": float(1.8247e-5),
        "temperature": 293.15,
        "pressure": 101325,
        "molar_mass" : 28.958601
    }

    config["2"] = {
        "name": "Air",
        "identifier": 2,
        "color": "[255,85,255]",  # Blue
        "density": 0.945625,
        "speed_of_sound": 387.054839,
        "isentropic_exponent": 1.397945,
        "thermal_conductivity": 0.031167,
        "specific_heat_Cp": 1011.477011,
        "dynamic_viscosity": float(2.1948e-5),
        "temperature": 373.15,
        "pressure": 101325,
        "molar_mass" : 28.958601
    }

    config["3"] = {
        "name": "Hydrogen",
        "identifier": 3,
        "color": "[116,200,255]",  # Magenta
        "density": 0.077173,
        "speed_of_sound": 1357.568075,
        "isentropic_exponent": 1.402898,
        "thermal_conductivity": 0.19527,
        "specific_heat_Cp": 14367.266634,
        "dynamic_viscosity": float(9.3092e-6),
        "temperature": 318.15,
        "pressure": 101325,
    }

    config["4"] = {
        "name": "Hydrogen",
        "identifier": 4,
        "color": "[255,102,102]",  # Magenta
        "density": 0.767785,
        "speed_of_sound": 1365.114753,
        "isentropic_exponent": 1.404047,
        "thermal_conductivity": 0.1964,
        "specific_heat_Cp": 14388.94084,
        "dynamic_viscosity": float(9.3137e-6),
        "temperature": 318.15,
        "pressure": 1013250,
    }

    config["5"] = {
        "name": "Methane",
        "identifier": 5,
        "color": "[103,255,164]",  # Cyan
        "density": 0.66816,
        "speed_of_sound": 445.010623,
        "isentropic_exponent": 1.308321,
        "thermal_conductivity": 0.033271,
        "specific_heat_Cp": 2220.597802,
        "dynamic_viscosity": float(1.0914e-5),
        "temperature": 293.15,
        "pressure": 101325,
    }

    app().pulse_file.write_fluid_library_in_file(config)