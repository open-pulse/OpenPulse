
import matplotlib
matplotlib.use('Agg')

from pulse.model.reciprocating_pump_model import ReciprocatingPumpModel

import numpy as np

pi = 3.141592653589

def load_default_reciprocating_pump_setup(crank_angle = 0):

    parameters = {  
                  'bore_diameter' : 0.105,
                  'stroke' : 0.205,
                  'connecting_rod_length' : 0.40,
                  'rod_diameter' : 0.05,
                  'clearance_HE' : 15,
                  'clearance_CE' : 18,
                  'tdc_crank_angle_1' : crank_angle,
                  'rotational_speed' : 178,
                  'number_of_cylinders' : 1,
                  'acting_label' : 0,
                  'suction_pressure' : 2.18,
                  'discharge_pressure' : 322.18,
                  'suction_temperature' : 45,
                  'discharge_temperature' : 45,
                  'pressure_unit' : "bar (g)",
                  'temperature_unit' : "°C",
                  'bulk_modulus' : 2541031616.236133
                  }

    pump_model = ReciprocatingPumpModel(**parameters)
    pump_model.process_remaining_fluid_properties()
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


def test_suction_flow_rate(smooth_data: bool=False):
    crank_angle = 0
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 1024

    flow_rate = reciprocating_pump.process_sum_of_volumetric_flow_rate('in_flow', smooth_data=smooth_data)

    assert flow_rate is not None, "Suction flow rate computation returned None"
    N = len(flow_rate)
    assert N > 0, "Suction flow rate array is empty"
    assert np.all(np.isfinite(flow_rate)), "Non-finite values in suction flow rate"

def test_discharge_flow_rate(smooth_data: bool=False):
    crank_angle = 0
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 3600

    flow_rate = reciprocating_pump.process_sum_of_volumetric_flow_rate('out_flow', smooth_data=smooth_data)

    assert flow_rate is not None, "Discharge flow rate computation returned None"
    N = reciprocating_pump.number_points
    assert len(flow_rate) > 0, "Discharge flow rate array is empty"
    assert np.all(np.isfinite(flow_rate)), "Non-finite values in discharge flow rate"

    # Verify the computed stroke volume is physically positive
    f_rot = reciprocating_pump.rpm / 60
    V_pos = flow_rate - np.average(flow_rate)
    mask = V_pos <= 0
    V_pos[mask] = np.zeros(sum(mask), dtype=float)
    dt = 1 / (f_rot * (N - 1))
    dVt = np.trapezoid(V_pos, dx=dt)
    dV = dVt / reciprocating_pump.number_of_cylinders
    assert dV > 0, "Computed stroke volume should be positive"


def check_angles():
    crank_angle = 0
    reciprocating_pump = load_default_reciprocating_pump_setup(crank_angle = crank_angle)
    reciprocating_pump.number_points = 1023
    reciprocating_pump.get_cycles_boundary_data(acting_label="HE")
