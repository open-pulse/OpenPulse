
from pulse.model.reciprocating_compressor_model import ReciprocatingCompressorModel

import os
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from scipy import signal

pi = 3.141592653589

def load_default_compressor_setup(crank_angle=0):

    parameters = {  'bore_diameter' : 0.780,
                    'stroke' : 0.33,
                    'connecting_rod_length' : 1.25,
                    'rod_diameter' : 0.135,
                    'pressure_ratio' : 1.90788804,
                    'clearance_HE' : 15.8,
                    'clearance_CE' : 18.39,
                    'TDC_crank_angle_1' : crank_angle,
                    'rotational_speed' : 360,
                    'capacity' : 100,
                    'acting_label' : 0,
                    'pressure_at_suction' : 19.65,
                    'pressure_unit' : "bar",
                    'temperature_at_suction' : 45,
                    'temperature_unit' : "°C",
                    'isentropic_exponent' : 1.400,
                    'molar_mass' : 2.01568  }

    compressor = ReciprocatingCompressorModel(parameters)
    compressor.set_fluid_properties_and_update_state(   parameters['isentropic_exponent'],
                                                        parameters['molar_mass']   )

    compressor.number_of_cylinders = 1

    return compressor

def test_PV_diagram(print_log=True, export_data=True):
    return
        
    for angle in [0, 90, 180, 270]:
    
        path_crank_end = Path(f"tests/data/compressor/PV_diagram/PV_diagram_crank_end_crank_angle_{angle}.txt")
        path_head_end = Path(f"tests/data/compressor/PV_diagram/PV_diagram_head_end_crank_angle_{angle}.txt")

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

        volume_HE, pressure_HE, *args = compressor.process_head_end_volumes_and_pressures(export_data=export_data)
        volume_CE, pressure_CE, *args = compressor.process_crank_end_volumes_and_pressures(export_data=export_data)

        volume_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 0] - volume_HE)/np.abs(external_data[f"head_end_{angle}"][:, 0] + volume_HE)/2))
        pressure_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 1] - pressure_HE)/np.abs(external_data[f"head_end_{angle}"][:, 1] + pressure_HE)/2))

        volume_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 0] - volume_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 0] + volume_CE)/2))
        pressure_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 1] - pressure_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 1] + pressure_CE)/2))

        assert volume_error_head_end < 1e-8
        assert volume_error_crank_end < 1e-8
        assert pressure_error_head_end < 1e-8
        assert pressure_error_crank_end < 1e-8

        # use poetry run pytest tests/test_compressor.py -s to print the logs
        if print_log:
            print("\n")
            print(f"Crank angle: {angle} deg")
            print(f"volume error (head end): {volume_error_head_end*100}%")
            print(f"pressure error (head end): {pressure_error_head_end*100}%")
            print(f"volume error (crank end): {volume_error_crank_end*100}%")
            print(f"pressure error (crank end): {pressure_error_crank_end*100}%")
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


def test_suction_flow_rate():
    return
    
    crank_angle = 0
    reciprocating_compressor = load_default_compressor_setup(crank_angle = crank_angle)
    reciprocating_compressor.number_points = 1023

    flow_rate = reciprocating_compressor.process_sum_of_volumetric_flow_rate('in_flow', smooth_data=False)
    if flow_rate is None:
        return

    N = len(flow_rate)
    angles = np.linspace(0, 2*pi, N)
    
    x_label = "Angle [rad]"
    y_label = "Volume [m³/s]"
    title = "Volumetric flow rate at suction"
    
    path = Path(f"tests/data/compressor/flow/full_load/bp_reciprocating_compressor_flow_at_suction_crank_angle_{crank_angle}.txt")
    data_HE = np.loadtxt(path, skiprows=4, max_rows=103)
    data_CE = np.loadtxt(path, skiprows=112, max_rows=113)

    volumes = [angles, data_HE[:,0], data_CE[:,0]]
    flow_rates = [flow_rate, -data_HE[:,1], -data_CE[:,1]]
    labels = ["OpenPulse", "Reference (HE)", "Reference (CE)"]
    colors = [(0,0,0),(1,0,0),(0,0,1)]
    linestyles = ["-","-", "-"]

    plot2(volumes, flow_rates, x_label, y_label, title, labels, colors, linestyles)


def test_discharge_flow_rate():
    return
    
    crank_angle = 0
    reciprocating_compressor = load_default_compressor_setup(crank_angle = crank_angle)
    reciprocating_compressor.number_points = 1023

    flow_rate = reciprocating_compressor.process_sum_of_volumetric_flow_rate('out_flow', smooth_data=False)
    if flow_rate is None:
        return

    N = len(flow_rate)  
    angles = np.linspace(0, 2*pi, N)

    x_label = "Angle [rad]"
    y_label = "Volume [m³/s]"
    title = "Volumetric flow rate at discharge"
    
    path = Path(f"tests/data/compressor/flow/full_load/bp_reciprocating_compressor_flow_at_discharge_crank_angle_{crank_angle}.txt")
    data_CE = np.loadtxt(path, skiprows=4, max_rows=80)
    data_HE = np.loadtxt(path, skiprows=89, max_rows=93)
    
    volumes = [angles, data_HE[:,0], data_CE[:,0]]
    flow_rates = [flow_rate, data_HE[:,1], data_CE[:,1]]
    labels = ["OpenPulse", "Reference (HE)", "Reference (CE)"]
    colors = [(0,0,0),(1,0,0),(0,0,1)]
    linestyles = ["-","-", "-"]

    plot2(volumes, flow_rates, x_label, y_label, title, labels, colors, linestyles)


def plot2(x, y, x_label, y_label, title, labels, colors, linestyles):

    fig = plt.figure(figsize=[8,6])
    ax_ = fig.add_subplot(1,1,1)

    for i, label in enumerate(labels): 
        ax_.plot(x[i], y[i], color=colors[i], linewidth=2, linestyle=linestyles[i], label=label)
    
    ax_.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax_.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax_.set_title(title, fontsize = 12, fontweight = 'bold')

    plt.legend()
    plt.grid()
    plt.show()


def check_angles():
    crank_angle = 0
    compressor = load_default_compressor_setup(crank_angle = crank_angle)
    compressor.number_points = 1023

    compressor.get_cycles_boundary_data(acting_label="HE")

if __name__ == "__main__":
    test_PV_diagram(print_log=True, export_data=True)
    # test_suction_flow_rate()
    # test_discharge_flow_rate()
    # check_angles()