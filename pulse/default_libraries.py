import configparser

def default_material_library(path):
    config = configparser.ConfigParser()

    config['Steel'] = { 
                            'Name': 'Steel',
                            'Identifier': 1,
                            'Color': '[170,170,170]', #Light Gray
                            'Density': 7860,
                            'Young Modulus': 210,
                            'Poisson': 0.3,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['Stainless_steel'] = {  
                            'Name': 'Stainless_steel',
                            'Identifier': 2,
                            'Color': '[126,46,31]', #Wood color
                            'Density': 7750,
                            'Young Modulus': 193,
                            'Poisson': 0.31,
                            'Thermal expansion coefficient': 1.7e-5 }

    config['Ni-Co-Cr_alloy'] = {   
                            'Name': 'Ni-Co-Cr_alloy',
                            'Identifier': 3,
                            'Color': '[0,255,255]', #Cyan
                            'Density': 8220,
                            'Young Modulus': 212,
                            'Poisson': 0.315,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['Cast_iron'] = { 
                            'Name': 'Cast_iron',
                            'Identifier': 4,
                            'Color': '[50,50,50]', #Dark Grey
                            'Density': 7200,
                            'Young Modulus': 110,
                            'Poisson': 0.28,
                            'Thermal expansion coefficient': 1.1e-5 }

    config['Aluminum'] = {  
                            'Name': 'Aluminum',
                            'Identifier': 5,
                            'Color': '[255,255,255]', #White
                            'Density': 2770,
                            'Young Modulus': 71,
                            'Poisson': 0.333,
                            'Thermal expansion coefficient': 2.3e-5 }

    config['Brass'] = { 
                            'Name': 'Brass',
                            'Identifier': 6,
                            'Color': '[181,166,66]', #Brass color
                            'Density': 8150,
                            'Young Modulus': 96,
                            'Poisson': 0.345,
                            'Thermal expansion coefficient': 1.9e-5 }
    
    config['Ductile cast iron'] = { 
                                    'Name': 'Ductile cast iron',
                                    'Identifier': 7,
                                    'Color': '[100,100,100]', #Medium Grey
                                    'Density': 7200,
                                    'Young Modulus': 161,
                                    'Poisson': 0.29,
                                    'Thermal expansion coefficient': 1.1e-5 }

    config['API 5L-A'] = { 
                            'Name': 'API 5L-A',
                            'Identifier': 8,
                            'Color': '[255,255,255]', #White color
                            'Density': 7833.44,
                            'Young Modulus': 202.7,
                            'Poisson': 0.292,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['API 5L-A25'] = { 
                            'Name': 'API 5L-25A',
                            'Identifier': 9,
                            'Color': '[255,255,255]', #White color
                            'Density': 7833.44,
                            'Young Modulus': 203.4,
                            'Poisson': 0.292,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['API 5L-B'] = { 
                            'Name': 'API 5L-B',
                            'Identifier': 10,
                            'Color': '[255,255,255]', #White color
                            'Density': 7833.44,
                            'Young Modulus': 202.7,
                            'Poisson': 0.292,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['API 5L-X42/X80'] = { 
                                'Name': 'API 5L-X42/X80',
                                'Identifier': 11,
                                'Color': '[255,255,255]', #White color
                                'Density': 7833.44,
                                'Young Modulus': 202.7,
                                'Poisson': 0.292,
                                'Thermal expansion coefficient': 1.2e-5 }

    with open(path, 'w') as config_file:
        config.write(config_file)

def default_fluid_library(path):

    # References:   Incropera, et al. FUNDAMENTALS OF HEAT AND MASS TRANSFER. 6th edition. 
    #               Çengel, Yunus A., Boles, Michael A. THERMODYNAMICS. 5th edition. 
    # TODO: check the fluids pressure state

    config = configparser.ConfigParser()

    config['Air @300K'] = {
                            'Name': 'Air @300K',
                            'Identifier': 1,
                            'Color': '[0,0,255]', #Blue
                            'Fluid density': 1.1614, 
                            'Speed of sound': 347.21,
                            'Impedance': 403.2496,
                            'Isentropic exponent': 1.400, 
                            'Thermal conductivity': 0.0263,
                            'Specific heat Cp': 1007,
                            'Dynamic viscosity': float(184.6e-7),
                            'Temperature' : 300,
                            'Pressure' : 101325 }      

    config['Air @400K'] = {
                            'Name': 'Air @400K',
                            'Identifier': 2,
                            'Color': '[0,255,255]', #light Blue
                            'Fluid density': 0.8711, 
                            'Speed of sound': 400.21,
                            'Impedance': 348.629,
                            'Isentropic exponent': 1.395, 
                            'Thermal conductivity': 0.0338,
                            'Specific heat Cp': 1013,
                            'Dynamic viscosity': float(230.1e-7),
                            'Temperature' : 400,
                            'Pressure' : 101325 }     

    config['Hydrogen @300K'] = {
                            'Name': 'Hydrogen @300K',
                            'Identifier': 3,
                            'Color': '[150,0,150]', #Magenta
                            'Fluid density': 0.08078,
                            'Speed of sound': 1318.43,
                            'Impedance': 106.5027,
                            'Isentropic exponent': 1.405, 
                            'Thermal conductivity': float(183e-3),
                            'Specific heat Cp': 14307,
                            'Dynamic viscosity': float(89.6e-7),
                            'Temperature' : 300,
                            'Pressure' : 101325 } 
    
    config['Hydrogen @400K'] = {
                            'Name': 'Hydrogen @400K',
                            'Identifier': 4,
                            'Color': '[200,125,255]', #Magenta
                            'Fluid density': 0.06059,
                            'Speed of sound': 1518.598,
                            'Impedance': 92.0118,
                            'Isentropic exponent': 1.398, 
                            'Thermal conductivity': float(226e-3),
                            'Specific heat Cp': 14476,
                            'Dynamic viscosity': float(108.2e-7),
                            'Temperature' : 400,
                            'Pressure' : 101325 } 
    
    config['Methane @300K'] = {
                            'Name': 'Methane @300K',
                            'Identifier': 5,
                            'Color': '[200,150,50]', #Cyan
                            'Fluid density': 0.657,
                            'Speed of sound': 449.2,
                            'Impedance': 295.1244,
                            'Isentropic exponent': 1.299, 
                            'Thermal conductivity': 0.0339,
                            'Specific heat Cp': 2232,
                            'Dynamic viscosity': float(110e-7),
                            'Temperature' : 300,
                            'Pressure' : 101325 }   

    with open(path, 'w') as config_file:
        config.write(config_file)