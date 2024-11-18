import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pulse.model.reciprocating_pump_model import ReciprocatingPumpModel

pi = 3.141592653589

def load_default_reciprocating_pump_setup(crank_angle: 0.):

    parameters = {  
                  'bore_diameter' : 0.105,
                  'stroke' : 0.205,
                  'connecting_rod_length' : 0.40,
                  'rod_diameter' : 0.05,
                  'clearance_HE' : 15,
                  'clearance_CE' : 18,
                  'TDC_crank_angle_1' : crank_angle,
                  'rotational_speed' : 178,
                  'number_of_cylinders' : 1,
                  'acting_label' : 0,
                  'pressure_at_suction' : 2.18 + 1.01325,
                  'pressure_at_discharge' : 322.18 + 1.01325,
                  'temperature_at_suction' : 45,
                  'temperature_at_discharge' : 45,
                  'pressure_unit' : "bar",
                  'temperature_unit' : "°C",
                  'bulk_modulus' : 2541031616.236133
                  }

    pump_model = ReciprocatingPumpModel(parameters)
    pump_model.number_points = 3600

    return pump_model

# def test_PV_diagram(print_log=True, export_data=True):
        
#     for angle in [0, 90, 180, 270]:
    
#         path_crank_end = Path(f"tests/data/reciprocating_pump/PV_diagram/PV_diagram_crank_end_crank_angle_{angle}.txt")
#         path_head_end = Path(f"tests/data/reciprocating_pump/PV_diagram/PV_diagram_head_end_crank_angle_{angle}.txt")

#         external_data = dict()

#         if os.path.exists(path_crank_end):
#             external_data[f"crank_end_{angle}"] = np.loadtxt(path_crank_end, skiprows=4)
#         else:
#             continue
        
#         if os.path.exists(path_head_end):
#             external_data[f"head_end_{angle}"] = np.loadtxt(path_head_end, skiprows=4)
#         else:
#             continue
        
#         N_he = external_data[f"head_end_{angle}"].shape[0]
#         N_ce = external_data[f"crank_end_{angle}"].shape[0]

#         if N_ce != N_he:
#             return

#         reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = angle)
#         reciprocating_pump.number_points = N_he - 1

#         volume_HE, pressure_HE, *args = reciprocating_pump.process_head_end_volumes_and_pressures(export_data=export_data)
#         volume_CE, pressure_CE, *args = reciprocating_pump.process_crank_end_volumes_and_pressures(export_data=export_data)

#         volume_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 0] - volume_HE)/np.abs(external_data[f"head_end_{angle}"][:, 0] + volume_HE)/2))
#         pressure_error_head_end = (np.max(np.abs(external_data[f"head_end_{angle}"][:, 1] - pressure_HE)/np.abs(external_data[f"head_end_{angle}"][:, 1] + pressure_HE)/2))

#         volume_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 0] - volume_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 0] + volume_CE)/2))
#         pressure_error_crank_end = (np.max(np.abs(external_data[f"crank_end_{angle}"][:, 1] - pressure_CE)/np.abs(external_data[f"crank_end_{angle}"][:, 1] + pressure_CE)/2))

#         assert volume_error_head_end < 1e-8
#         assert volume_error_crank_end < 1e-8
#         assert pressure_error_head_end < 1e-8
#         assert pressure_error_crank_end < 1e-8

#         # use poetry run pytest tests/test_reciprocating_pump.py -s to print the logs
#         if print_log:
#             print("\n")
#             print(f"Crank angle: {angle} deg")
#             print(f"volume error (head end): {volume_error_head_end*100}%")
#             print(f"pressure error (head end): {pressure_error_head_end*100}%")
#             print(f"volume error (crank end): {volume_error_crank_end*100}%")
#             print(f"pressure error (crank end): {pressure_error_crank_end*100}%")
#             # print("\n")

#         if export_data:

#             data_HE = np.array([external_data[f"head_end_{angle}"][:, 0],
#                                 external_data[f"head_end_{angle}"][:, 1],
#                                 volume_HE,
#                                 pressure_HE], dtype=float).T
            
#             data_CE = np.array([external_data[f"crank_end_{angle}"][:, 0],
#                                 external_data[f"crank_end_{angle}"][:, 1],
#                                 volume_CE,
#                                 pressure_CE], dtype=float).T

#             np.savetxt(f"teste_head_end_{angle}.dat", data_HE, delimiter=",")
#             np.savetxt(f"teste_crank_end_{angle}.dat", data_CE, delimiter=",")       


def test_suction_flow_rate():
    # return

    crank_angle = 0
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 1023

    flow_rate = reciprocating_pump.process_sum_of_volumetric_flow_rate('in_flow')
    if flow_rate is None:
        return

    N = len(flow_rate)
    angles = np.linspace(0, 2*pi, N)
    
    x_label = "Angle [rad]"
    y_label = "Volume [m³/s]"
    title = "Volumetric flow rate at suction"
    
    path = Path(f"tests/data/reciprocating_pump/flow/bp_reciprocating_pump_flow_at_suction_crank_angle_{crank_angle}.txt")
    data_HE = np.loadtxt(path, skiprows=4, max_rows=115)
    data_CE = np.loadtxt(path, skiprows=119)

    volumes = [angles, data_HE[:,0], data_CE[:,0]]
    flow_rates = [flow_rate, -data_HE[:,1], -data_CE[:,1]]
    labels = ["OpenPulse", "Reference (HE)", "Reference (CE)"]
    colors = [(0,0,0), (1,0,0), (0,0,1)]
    linestyles = ["-", "-", "-"]

    plot2(volumes, flow_rates, x_label, y_label, title, labels, colors, linestyles)


def test_discharge_flow_rate():
    # return

    crank_angle = 0
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 1023

    flow_rate = reciprocating_pump.process_sum_of_volumetric_flow_rate('out_flow')
    if flow_rate is None:
        return

    N = len(flow_rate)  
    angles = np.linspace(0, 2*pi, N)

    x_label = "Angle [rad]"
    y_label = "Volume [m³/s]"
    title = "Volumetric flow rate at discharge"

    path = Path(f"tests/data/reciprocating_pump/flow/bp_reciprocating_pump_flow_at_discharge_crank_angle_{crank_angle}.txt")
    data_HE = np.loadtxt(path, skiprows=4, max_rows=102)
    data_CE = np.loadtxt(path, skiprows=111)#, max_rows=110)

    volumes = [angles, data_HE[:,0], data_CE[:,0]]
    flow_rates = [flow_rate, data_HE[:,1], data_CE[:,1]]
    labels = ["OpenPulse", "Reference (HE)", "Reference (CE)"]
    colors = [(0,0,0), (1,0,0), (0,0,1)]
    linestyles = ["-", "-", "-"]

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
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 1023
    reciprocating_pump.get_cycles_boundary_data(acting_label="HE")


# if __name__ == "__main__":
    # test_PV_diagram(print_log=True, export_data=True)
    # test_suction_flow_rate()
    # test_discharge_flow_rate()
    # check_angles()