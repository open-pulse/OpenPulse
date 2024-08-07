import configparser

from pulse import app

def default_material_library():
    config = configparser.ConfigParser()

    config["Steel"] = {
        "Name": "Steel",
        "Identifier": 1,
        "Color": "[170,170,170]",  # Light Gray
        "Density": 7860,
        "Young Modulus": 210,
        "Poisson": 0.3,
        "Thermal expansion coefficient": 1.2e-5,
    }

    config["Stainless_steel"] = {
        "Name": "Stainless_steel",
        "Identifier": 2,
        "Color": "[126,46,31]",  # Wood color
        "Density": 7750,
        "Young Modulus": 193,
        "Poisson": 0.31,
        "Thermal expansion coefficient": 1.7e-5,
    }

    config["Ni-Co-Cr_alloy"] = {
        "Name": "Ni-Co-Cr_alloy",
        "Identifier": 3,
        "Color": "[0,255,255]",  # Cyan
        "Density": 8220,
        "Young Modulus": 212,
        "Poisson": 0.315,
        "Thermal expansion coefficient": 1.2e-5,
    }

    config["Cast_iron"] = {
        "Name": "Cast_iron",
        "Identifier": 4,
        "Color": "[50,50,50]",  # Dark Grey
        "Density": 7200,
        "Young Modulus": 110,
        "Poisson": 0.28,
        "Thermal expansion coefficient": 1.1e-5,
    }

    config["Aluminum"] = {
        "Name": "Aluminum",
        "Identifier": 5,
        "Color": "[255,255,255]",  # White
        "Density": 2770,
        "Young Modulus": 71,
        "Poisson": 0.333,
        "Thermal expansion coefficient": 2.3e-5,
    }

    config["Brass"] = {
        "Name": "Brass",
        "Identifier": 6,
        "Color": "[181,166,66]",  # Brass color
        "Density": 8150,
        "Young Modulus": 96,
        "Poisson": 0.345,
        "Thermal expansion coefficient": 1.9e-5,
    }

    app().main_window.file.write_material_library_in_file(config)


def default_fluid_library():

    # Reference: RefProp v10.0

    config = configparser.ConfigParser()

    config["1"] = {
        "Name": "Air",
        "Identifier": 1,
        "Color": "[255,170,127]",  # Blue
        "Fluid density": 1.204263,
        "Speed of sound": 343.395034,
        "Isentropic exponent": 1.401985,
        "Thermal conductivity": 0.025503,
        "Specific heat Cp": 1006.400178,
        "Dynamic viscosity": float(1.8247e-5),
        "Temperature": 293.15,
        "Pressure": 101325,
        "Molar mass" : 28.958601
    }

    config["2"] = {
        "Name": "Air",
        "Identifier": 2,
        "Color": "[255,85,255]",  # Blue
        "Fluid density": 0.945625,
        "Speed of sound": 387.054839,
        "Isentropic exponent": 1.397945,
        "Thermal conductivity": 0.031167,
        "Specific heat Cp": 1011.477011,
        "Dynamic viscosity": float(2.1948e-5),
        "Temperature": 373.15,
        "Pressure": 101325,
        "Molar mass" : 28.958601
    }

    config["3"] = {
        "Name": "Hydrogen",
        "Identifier": 3,
        "Color": "[116,200,255]",  # Magenta
        "Fluid density": 0.077173,
        "Speed of sound": 1357.568075,
        "Isentropic exponent": 1.402898,
        "Thermal conductivity": 0.19527,
        "Specific heat Cp": 14367.266634,
        "Dynamic viscosity": float(9.3092e-6),
        "Temperature": 318.15,
        "Pressure": 101325,
    }

    config["4"] = {
        "Name": "Hydrogen",
        "Identifier": 4,
        "Color": "[255,102,102]",  # Magenta
        "Fluid density": 0.767785,
        "Speed of sound": 1365.114753,
        "Isentropic exponent": 1.404047,
        "Thermal conductivity": 0.1964,
        "Specific heat Cp": 14388.94084,
        "Dynamic viscosity": float(9.3137e-6),
        "Temperature": 318.15,
        "Pressure": 1013250,
    }

    config["5"] = {
        "Name": "Methane",
        "Identifier": 5,
        "Color": "[103,255,164]",  # Cyan
        "Fluid density": 0.66816,
        "Speed of sound": 445.010623,
        "Isentropic exponent": 1.308321,
        "Thermal conductivity": 0.033271,
        "Specific heat Cp": 2220.597802,
        "Dynamic viscosity": float(1.0914e-5),
        "Temperature": 293.15,
        "Pressure": 101325,
    }

    app().main_window.file.write_fluid_library_in_file(config)