import os
import numpy as np
from pathlib import Path

from pulse.preprocessing.compressor_model import CompressorModel

def load_default_compressor_setup(crank_angle=0):

    parameters = {  'bore diameter' : 0.780,
                    'stroke' : 0.33,
                    'connecting rod length' : 1.25,
                    'rod diameter' : 0.135,
                    'pressure ratio' : 1.90788804,
                    'clearance (HE)' : 15.8,
                    'clearance (CE)' : 18.39,
                    'TDC crank angle 1' : crank_angle,
                    'rotational speed' : 360,
                    'capacity' : 100,
                    'acting label' : "HE",
                    'pressure at suction' : 19.65,
                    'pressure unit' : "bar",
                    'temperature at suction' : 45,
                    'temperature unit' : "°C",
                    'isentropic exponent' : 1.400,
                    'molar mass' : 2.01568  }

    compressor = CompressorModel(parameters)
    compressor.set_fluid_properties_and_update_state(   parameters['isentropic exponent'],
                                                        parameters['molar mass']   )

    compressor.number_of_cylinders = 1

    return compressor

def test_PV_diagram(print_log=True, export_data=False):
        
    for angle in [0, 90, 180, 270]:
    
        path_crank_end = Path(f"tests/data_base/PV_diagram_crank_end_crank_angle_{angle}.txt")
        path_head_end = Path(f"tests/data_base/PV_diagram_head_end_crank_angle_{angle}.txt")

        external_data = dict()

        if os.path.exists(path_crank_end):
            external_data[f"crank_end_{angle}"] = np.loadtxt(path_crank_end, skiprows=4)
        else:
            continue
        
        if os.path.exists(path_head_end):
            external_data[f"head_end_{angle}"] = np.loadtxt(path_head_end, skiprows=4)
        else:
            continue
        
        N_he = external_data[f"head_end_{angle}"].shape[0]
        N_ce = external_data[f"crank_end_{angle}"].shape[0]

        if N_ce != N_he:
            return

        compressor = load_default_compressor_setup(crank_angle = angle)
        compressor.number_points = N_he - 1
        
        volume_HE, pressure_HE, *args = compressor.process_head_end_volumes_and_pressures()
        volume_CE, pressure_CE, *args = compressor.process_crank_end_volumes_and_pressures()

        volume_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 0] - volume_HE)/np.abs(external_data[f"head_end_{angle}"][:, 0] + volume_HE)/2))*100
        pressure_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 1] - pressure_HE)/np.abs(external_data[f"head_end_{angle}"][:, 1] + pressure_HE)/2))*100

        volume_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 0] - volume_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 0] + volume_CE)/2))*100
        pressure_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 1] - pressure_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 1] + pressure_CE)/2))*100

        if print_log:
            print("\n")
            print(f"Crank angle: {angle} deg")
            print(f"volume error (head end): {volume_error_head_end}%")
            print(f"pressure error (head end): {pressure_error_head_end}%")
            print(f"volume error (crank end): {volume_error_crank_end}%")
            print(f"pressure error (crank end): {pressure_error_crank_end}%")
            # print("\n")

        if export_data:

            data_HE = np.array([external_data[f"head_end_{angle}"][:, 0],
                                external_data[f"head_end_{angle}"][:, 1],
                                volume_HE,
                                pressure_HE], dtype=float).T
            
            
            data_CE = np.array([external_data[f"crank_end_{angle}"][:, 0],
                                external_data[f"crank_end_{angle}"][:, 1],
                                volume_CE,
                                pressure_CE], dtype=float).T

            np.savetxt(f"teste_head_end_{angle}.dat", data_HE, delimiter=",")
            np.savetxt(f"teste_crank_end_{angle}.dat", data_CE, delimiter=",")       


if __name__ == "__main__":
    test_PV_diagram()