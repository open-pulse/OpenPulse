
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project

# import pytest
import numpy as np

from pathlib import Path
from shutil import copy

# Setting up model
# @pytest.fixture

def test_coupled_harmonic_analysis(project_path: str | Path):

    ## Initialize a project
    project = Project()
    project.initialize_pulse_file_and_loader()

    ## Copy the project to the temp_pulse folder
    copy(project_path, project.file.path)

    ## Load project
    project.load_project()

    ## Define usefull objects
    model = project.model
    mesh = project.model.mesh
    preprocessor = model.preprocessor

    ## Remove the previous attributed volume velocity excitation
    coords = np.array([ 0.000,  0.000,  0.000], dtype=float)
    node_id = preprocessor.get_node_id_by_coordinates(coords)
    model.properties._remove_nodal_property("volume_velocity", node_id)

    ## Apply reciprocating pump excitation at point 0,0,0
    coords = np.array([ 0.000,  0.000,  0.000], dtype=float)
    node_id = preprocessor.get_node_id_by_coordinates(coords)

    line_id = mesh.lines_from_node[node_id]
    fluid = model.properties._get_property("fluid", line_id=line_id[0])

    connection_type = "discharge"
    parameters, freq, flow_rate = get_reciprocating_pump_excitation(connection_type, fluid)

    table_name = f"pump_excitation_{connection_type}_node_{node_id}"

    data = {
            "coords" : list(coords),
            "connection_type" : connection_type,
            "table_names" : [table_name],
            "parameters" : parameters
            }

    if save_table_values(project, table_name, freq, flow_rate):
        return

    model.properties._set_nodal_property("reciprocating_pump_excitation", data, node_id)


    """
    |--------------------------------------------------------------------|
    |                    Analysis ID codification                        |
    |--------------------------------------------------------------------|
    |    0 - Structural - Harmonic analysis through direct method        |
    |    1 - Structural - Harmonic analysis through mode superposition   |
    |    2 - Structural - Modal analysis                                 |
    |    3 - Acoustic - Harmonic analysis through direct method          |
    |    4 - Acoustic - Modal analysis (convetional FE 1D)               |
    |    5 - Coupled - Harmonic analysis through direct method           |
    |    6 - Coupled - Harmonic analysis through mode superposition      |
    |    7 - Structural - Static analysis (under development)            |
    |--------------------------------------------------------------------|
    """

    ## Analysis setup for acoustic harmonic analysis

    analysis_setup = {
                      "analysis_id" : 3,
                    #   "f_min" : 1,
                    #   "f_max" : 300,
                    #   "f_step" : 1,
                      "global_damping" : [1e-3, 1e-5, 0., 0.],
                      }
    
    model.set_analysis_setup(analysis_setup)

    ## Write project data in the temp_pulse folder

    # Note: if some modification exists, it is necessary to update the property-related data in the file

    # project.file.write_line_properties_in_file()
    # project.file.write_element_properties_in_file()
    project.file.write_nodal_properties_in_file()
    project.file.write_imported_table_data_in_file()

    # project.file.write_project_setup_in_file(mesher_setup)
    project.file.write_analysis_setup_in_file(model.analysis_setup)

    ## Build the mathematical model and solve it (it also saves the model results in the temp_pulse folder)
    project.build_model_and_solve(running_by_script=True)

    ## Uncomment the following function to remove the created files from the temp_pulse folder
    # remove_files_from_temporary_folder()

def create_temporary_fluid_library(project: Project, fluids: dict):

    from configparser import ConfigParser
    config = ConfigParser()

    for fluid_id, fluid in fluids.items():
        fluid: Fluid

        config[f"{fluid_id}"] = {
                                 "name": fluid.name,
                                 "identifier": fluid.identifier,
                                 "pressure": fluid.pressure,
                                 "temperature": fluid.temperature,
                                 "density": fluid.density,
                                 "speed_of_sound": fluid.speed_of_sound,
                                 "isentropic_exponent": fluid.isentropic_exponent,
                                 "thermal_conductivity": fluid.thermal_conductivity,
                                 "dynamic_viscosity": fluid.dynamic_viscosity,
                                 "molar_mass": fluid.molar_mass,
                                 "color": fluid.color,
                                 }

    project.file.write_fluid_library_in_file(config)

def get_reciprocating_pump_excitation(connection_type: str, fluid: Fluid):

    from pulse.model.reciprocating_pump_model import ReciprocatingPumpModel

    parameters = {  
                  'bore_diameter' : 0.105,
                  'stroke' : 0.205,
                  'connecting_rod_length' : 0.40,
                  'rod_diameter' : 0.05,
                  'pressure_ratio' : 1.90788804,
                  'clearance_HE' : 15.8,
                  'clearance_CE' : 18.39,
                  'TDC_crank_angle_1' : 0,
                  'rotational_speed' : 178,
                  'number_of_cylinders' : 5,
                  'acting_label' : 1,
                  'pressure_at_suction' : 2.18 + 1.01325,
                  'pressure_at_discharge' : 322.18 + 1.01325,
                  'temperature_at_suction' : 45,
                  'pressure_unit' : "bar",
                  'temperature_unit' : "°C",
                  'bulk_modulus' : fluid.bulk_modulus
                  }

    pump_model = ReciprocatingPumpModel(parameters)

    pump_model.number_points = 1000
    pump_model.max_frequency = 300

    T_rev = 60 / pump_model.rpm
    list_T = [10, 5, 4, 2, 1, 0.5]
    list_df = [0.1, 0.2, 0.25, 0.5, 1, 2]

    T_selected = list_T[3]
    df_selected = list_df[3]

    if np.remainder(T_selected, T_rev) == 0:
        T = T_selected
        df = 1 / T
    else:
        i = 0
        df = 1 / (T_rev)
        while df > df_selected:
            i += 1
            df = 1 / (i * T_rev)

    N_rev = i

    if connection_type == "discharge":
        flow_label = "out_flow"

    else:
        flow_label = "in_flow"

    freq, flow_rate = pump_model.process_FFT_of_volumetric_flow_rate(N_rev, flow_label)

    return parameters, freq, flow_rate

def save_table_values(project: Project, table_name: str, frequencies: np.ndarray, complex_values: np.ndarray):

    f_min = frequencies[0]
    f_max = frequencies[-1]
    f_step = frequencies[1] - frequencies[0]

    analysis_setup = project.file.read_analysis_setup_from_file()
    if analysis_setup is None:
        analysis_setup = dict()

    analysis_setup["f_min"] = f_min
    analysis_setup["f_max"] = f_max
    analysis_setup["f_step"] = f_step

    project.model.set_analysis_setup(analysis_setup)

    real_values = np.real(complex_values)
    imag_values = np.imag(complex_values)
    data = np.array([frequencies, real_values, imag_values], dtype=float).T

    project.model.properties.add_imported_tables("acoustic", table_name, data)

def remove_files_from_temporary_folder():

    from pulse import TEMP_PROJECT_DIR
    from shutil import rmtree
    from os import path, remove, listdir

    if TEMP_PROJECT_DIR.exists():
        for filename in listdir(TEMP_PROJECT_DIR).copy():
            file_path = TEMP_PROJECT_DIR / filename
            if path.exists(file_path):
                if "." in filename:
                    remove(file_path)
                else:
                    rmtree(file_path)

if __name__ == "__main__":

    project_path = "examples//projects//piping_with_pulsation_damper.pulse"
    test_coupled_harmonic_analysis(project_path)