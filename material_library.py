import numpy as np
import pandas as pd

header = ['Material', 'ID', 'Density [kg/m³]',' Young modulus [GPa]', 'Poisson ratio [-]']
filename = 'material_library.dat'

def material_properties():

    name, identifier, density, YoungModulus, poisson = [], [], [], [], []

    name.append('steel')
    identifier.append(1)
    density.append(7850)
    YoungModulus.append(210)
    poisson.append(0.3)

    name.append('stainless_steel')
    identifier.append(2)
    density.append(7750)
    YoungModulus.append(193)
    poisson.append(0.31)

    name.append('Ni-Co-Cr_steel')
    identifier.append(3)
    density.append(8220)
    YoungModulus.append(212)
    poisson.append(0.315)
    
    name.append('Ni-Cr-Mo_steel')
    identifier.append(4)
    density.append(7850)
    YoungModulus.append(200)
    poisson.append(0.29)

    name.append('cast_iron')
    identifier.append(5)
    density.append(7200)
    YoungModulus.append(110)
    poisson.append(0.28)

    name.append('aluminum')
    identifier.append(6)
    density.append(2770)
    YoungModulus.append(71)
    poisson.append(0.33)

    name.append('brass') # cast brass
    identifier.append(7)
    density.append(8150)
    YoungModulus.append(96)
    poisson.append(0.345)

    name.append('copper')
    identifier.append(8)
    density.append(8300)
    YoungModulus.append(110)
    poisson.append(0.34)

    name.append('bronze')
    identifier.append(9)
    density.append(8810)
    YoungModulus.append(80)
    poisson.append(0.345)

    name.append('concrete')
    identifier.append(10)
    density.append(2300)
    YoungModulus.append(30)
    poisson.append(0.18)

    return name, identifier, density, YoungModulus, poisson

name, identifier, density, YoungModulus, poisson = material_properties()
#
## ADD A NEW MATERIAL TO THE LIBRARY
#
name.append("test")
identifier.append(11)
density.append("3500")
YoungModulus.append("150")
poisson.append("0.3")
#
##
#
data = [name, identifier, density, YoungModulus, poisson]
data_to_save = list(map(list, zip(*data)))
material_properties = dict(zip(np.array(data[1],dtype=int), np.array(data[2:5],dtype=float).T))
data_to_save.insert(0, header)

np.savetxt(filename, data_to_save, fmt = "%18s, %3s, %15s, %19s, %17s,")
imported_library = np.loadtxt(filename, dtype=str, skiprows=1, delimiter=",")

# material_ID = np.array(imported_library[:,1], dtype=float)  
# density = np.array(imported_library[:,2], dtype=float)
# YoungModulus = np.array(imported_library[:,3], dtype=float)
# poisson = np.array(imported_library[:,4], dtype=float)