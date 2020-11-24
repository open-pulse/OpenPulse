import configparser

def default_material_library(path):
    config = configparser.ConfigParser()

    config['STEEL'] = { 
                            'Name': 'steel',
                            'Identifier': 1,
                            'Color': '[170,170,170]', #Light Gray
                            'Density': 7860,
                            'Young Modulus': 210,
                            'Poisson': 0.3,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['STAINLESS_STEEL'] = {  
                            'Name': 'stainless_steel',
                            'Identifier': 2,
                            'Color': '[126,46,31]', #Wood color
                            'Density': 7750,
                            'Young Modulus': 193,
                            'Poisson': 0.31,
                            'Thermal expansion coefficient': 1.7e-5 }

    config['NI-CO-CR_ALLOY'] = {   
                            'Name': 'Ni-Co-Cr_alloy',
                            'Identifier': 3,
                            'Color': '[0,255,255]', #Cyan
                            'Density': 8220,
                            'Young Modulus': 212,
                            'Poisson': 0.315,
                            'Thermal expansion coefficient': 1.2e-5 }

    config['CAST_IRON'] = { 
                            'Name': 'cast_iron',
                            'Identifier': 4,
                            'Color': '[50,50,50]', #Dark Grey
                            'Density': 7200,
                            'Young Modulus': 110,
                            'Poisson': 0.28,
                            'Thermal expansion coefficient': 1.1e-5 }

    config['ALUMINUM'] = {  
                            'Name': 'aluminum',
                            'Identifier': 5,
                            'Color': '[255,255,255]', #White
                            'Density': 2770,
                            'Young Modulus': 71,
                            'Poisson': 0.333,
                            'Thermal expansion coefficient': 2.3e-5 }

    config['BRASS'] = { 
                            'Name': 'brass',
                            'Identifier': 6,
                            'Color': '[181,166,66]', #Brass color
                            'Density': 8150,
                            'Young Modulus': 96,
                            'Poisson': 0.345,
                            'Thermal expansion coefficient': 1.9e-5 }

    with open(path, 'w') as config_file:
        config.write(config_file)

def default_fluid_library(path):

    # References:   Incropera, et al. FUNDAMENTALS OF HEAT AND MASS TRANSFER. 6th edition. 
    #               Çengel, Yunus A., Boles, Michael A. THERMODYNAMICS. 5th edition. 

    config = configparser.ConfigParser()

    config['AIR @300K'] = {
                            'Name': 'air @300K',
                            'Identifier': 1,
                            'Color': '[0,0,255]', #Blue
                            'Fluid density': 1.1614, 
                            'Speed of sound': 347.21,
                            'Impedance': 403.2496,
                            'Isentropic exponent': 1.400, 
                            'Thermal conductivity': 0.0263,
                            'Specific heat Cp': 1007,
                            'Dynamic viscosity': float(184.6e-7) }      

    config['AIR @400K'] = {
                            'Name': 'air @400K',
                            'Identifier': 2,
                            'Color': '[0,255,255]', #light Blue
                            'Fluid density': 0.8711, 
                            'Speed of sound': 400.21,
                            'Impedance': 348.629,
                            'Isentropic exponent': 1.395, 
                            'Thermal conductivity': 0.0338,
                            'Specific heat Cp': 1013,
                            'Dynamic viscosity': float(230.1e-7) }     

    config['HYDROGEN @300K'] = {
                            'Name': 'hydrogen @300K',
                            'Identifier': 3,
                            'Color': '[150,0,150]', #Magenta
                            'Fluid density': 0.08078,
                            'Speed of sound': 1318.43,
                            'Impedance': 106.5027,
                            'Isentropic exponent': 1.405, 
                            'Thermal conductivity': float(183e-3),
                            'Specific heat Cp': 14307,
                            'Dynamic viscosity': float(89.6e-7) } 
    
    config['HYDROGEN @400K'] = {
                            'Name': 'hydrogen @400K',
                            'Identifier': 4,
                            'Color': '[200,125,255]', #Magenta
                            'Fluid density': 0.06059,
                            'Speed of sound': 1518.598,
                            'Impedance': 92.0118,
                            'Isentropic exponent': 1.398, 
                            'Thermal conductivity': float(226e-3),
                            'Specific heat Cp': 14476,
                            'Dynamic viscosity': float(108.2e-7) } 
    
    config['METHANE @300K'] = {
                            'Name': 'methane @300K',
                            'Identifier': 5,
                            'Color': '[200,150,50]', #Cyan
                            'Fluid density': 0.657,
                            'Speed of sound': 449.2,
                            'Impedance': 295.1244,
                            'Isentropic exponent': 1.299, 
                            'Thermal conductivity': 0.0339,
                            'Specific heat Cp': 2232,
                            'Dynamic viscosity': float(110e-7) }   

    with open(path, 'w') as config_file:
        config.write(config_file)