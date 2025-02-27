
from pulse.model.cross_section import CrossSection, get_beam_section_properties
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project

# import pytest
import numpy as np

from pathlib import Path

# Setting up model
# @pytest.fixture

def test_coupled_harmonic_analysis():

    ## Initialize a project
    project = Project()
    project.initialize_pulse_file()

    ## Define usefull objects
    model = project.model
    mesh = model.mesh
    preprocessor = model.preprocessor

    # Load geometry file (only the *.iges and *.step formats are supported)
    geometry_path = Path("examples/iges_files/run_by_script/reciprocating_pump_piping.step")

    ## Configure the mesher setup
    mesher_setup = {
                    "element_size" : 0.01,
                    "geometry_tolerance" : 1e-6,
                    "length_unit" : "meter",
                    "import_type" : 0,
                    "geometry_path" : str(geometry_path)
                    }

    project.reset(reset_all=True)
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    ## Process the geometry and mesh
    preprocessor.generate()

    mesher_setup["import_type"] = 1
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    all_lines = project.model.mesh.lines_from_model

    N2_line = [14]
    header_lines = [10, 11]
    neck_lines = [12]
    volume_lines = [13, 14]
    main_lines = [line_id for line_id in all_lines if line_id not in header_lines + neck_lines + volume_lines]

    lines_lists = [main_lines, header_lines, neck_lines, volume_lines]

    ## Define the fluid
    fluids = create_fluids()
    create_temporary_fluid_library(project, fluids)

    water_lines = [line_id for line_id in all_lines if line_id not in N2_line]
    preprocessor.set_fluid_by_lines(water_lines, fluids[1])
    model.properties._set_line_property("fluid_id", fluids[1].identifier, water_lines)
    model.properties._set_line_property("fluid", fluids[1], water_lines)

    preprocessor.set_fluid_by_lines(N2_line, fluids[2])
    model.properties._set_line_property("fluid_id", fluids[2].identifier, N2_line)
    model.properties._set_line_property("fluid", fluids[2], N2_line)

    ## Define the material
    materials = create_materials()
    create_temporary_material_library(project, materials)

    preprocessor.set_material_by_lines(all_lines, materials[1])
    model.properties._set_line_property("material_id", materials[1].identifier, all_lines)
    model.properties._set_line_property("material", materials[1], all_lines)

    ## Create the model cross-sections

    main_section_info = {"section_type_label" : "pipe" ,
                        "section_parameters" : [0.219075, 0.015088, 0, 0, 0, 0]}

    header_section_info = {"section_type_label" : "pipe" ,
                           "section_parameters" : [0.32385, 0.015088, 0, 0, 0, 0]}

    neck_section_info = {"section_type_label" : "pipe" ,
                         "section_parameters" : [0.060325, 0.015088, 0, 0, 0, 0]}

    volume_section_info = {"section_type_label" : "pipe" ,
                           "section_parameters" : [0.250, 0.015088, 0, 0, 0, 0]}

    sections_info = [main_section_info, header_section_info, neck_section_info, volume_section_info]

    cross_section_main = CrossSection(pipe_section_info = main_section_info)
    cross_section_header = CrossSection(pipe_section_info = header_section_info)
    cross_section_neck = CrossSection(pipe_section_info = neck_section_info)
    cross_section_volume = CrossSection(pipe_section_info = volume_section_info)

    cross_sections = [cross_section_main, cross_section_header, cross_section_neck, cross_section_volume]

    ## Assign the cross-sections to respective lines

    for i, line_ids in enumerate(lines_lists):

        section_info = sections_info[i]
        cross_section = cross_sections[i]

        for line_id in line_ids:
            center_coords = model.properties._get_property("center_coords", line_id=line_id)
            corner_coords = model.properties._get_property("corner_coords", line_id=line_id)

            if (center_coords, corner_coords).count(None) == 2:
                section_label = main_section_info["section_type_label"]
                model.properties._set_line_property("structure_name", section_label, line_id)
            else:
                model.properties._set_line_property("structure_name", "bend", line_id)

        model.properties._set_multiple_line_properties(section_info, line_ids)
        model.properties._set_line_property("cross_section", cross_section, line_ids)
        model.properties._set_line_property("structural_element_type", "pipe_1", line_ids)
        preprocessor.set_cross_section_by_lines(line_ids, cross_section)
        preprocessor.set_structural_element_type_by_lines(line_ids, "pipe_1")

    ## Apply the dofs prescriptions

    dofs_prescription_data = list()

    # campled nodes
    points_coords = np.array([[  0.000,  0.000,  0.000 ],
                              [ 23.000,  4.000,  4.000 ],
                              [ 23.000,  4.000, -4.000 ]], dtype=float)
    
    values = [0j, 0j, 0j, 0j, 0j, 0j]
    dofs_prescription_data.append((points_coords, values))

    # supported in y and z directions
    points_coords = np.array([[  5.000,  0.000,  0.000 ],
                              [ 10.000,  0.000,  0.000 ],
                              [ 15.000,  0.000,  0.000 ],
                              [ 19.6713875,  0.000,  0.000 ]], dtype=float)
    
    values = [None, 0j, 0j, None, None, None]
    dofs_prescription_data.append((points_coords, values))

    for (points_coords, values) in dofs_prescription_data:
        for coords in points_coords:

            node_id = preprocessor.get_node_id_by_coordinates(coords)

            real_values = [value if value is None else np.real(value) for value in values]
            imag_values = [value if value is None else np.imag(value) for value in values]

            data = {
                    "coords" : list(coords),
                    "values" : values,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            model.properties._set_nodal_property("prescribed_dofs", data, node_id)

    ## Apply the nodal loads

    points_coords = np.array([[ 0.500,  0.000,  0.000],
                              [ 1.200, -0.250,  1.250]], dtype=float)

    for coords in points_coords:
        continue

        node_id = preprocessor.get_node_id_by_coordinates(coords)

        nodal_loads = [None, None, 1 + 0j, None, None, None]
        real_values = [value if value is None else np.real(value) for value in nodal_loads]
        imag_values = [value if value is None else np.imag(value) for value in nodal_loads]

        data = {
                "coords" : list(coords),
                "values" : nodal_loads,
                "real_values" : real_values,
                "imag_values" : imag_values
                }

        model.properties._set_nodal_property("nodal_loads", data, node_id)

    ## Apply the volume velocity excitation

    points_coords = np.array([[ 0.000,  0.000,  0.000]], dtype=float)

    for coords in points_coords:
        continue

        node_id = preprocessor.get_node_id_by_coordinates(coords)

        volume_velocity = [0.01 + 0j]
        real_values = [np.real(value) for value in volume_velocity]
        imag_values = [np.imag(value) for value in volume_velocity]

        data = {
                "coords" : list(coords),
                "values" : volume_velocity,
                "real_values" : real_values,
                "imag_values" : imag_values
                }

        model.properties._set_nodal_property("volume_velocity", data, node_id)

    ## Apply reciprocating pump excitation

    connection_type = "discharge"
    parameters, freq, flow_rate = get_reciprocating_pump_excitation(connection_type)

    points_coords = np.array([[ 0.000,  0.000,  0.000]], dtype=float)

    for coords in points_coords:

        node_id = preprocessor.get_node_id_by_coordinates(coords)
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
    # return
    ## Apply the radiation impedance

    points_coords = np.array([[ 23.000,  4.000,  4.000 ],
                              [ 23.000,  4.000, -4.000 ]], dtype=float)

    for coords in points_coords:

        node_id = preprocessor.get_node_id_by_coordinates(coords)

        data = {
                "coords" : list(coords),
                "impedance_type" : 0,
                }

        model.properties._set_nodal_property("radiation_impedance", data, node_id)

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
    
    ## Analysis setup for acoustic modal analysis

    # analysis_setup = {
    #                   "analysis_id" : 4,
    #                   "modes" : 40,
    #                   "sigma_factor" : 1e-2
    #                   }

    model.set_analysis_setup(analysis_setup)

    ## Write project data in the temp_pulse folder
    project.pulse_file.write_line_properties_in_file()
    project.pulse_file.write_nodal_properties_in_file()
    project.pulse_file.write_imported_table_data_in_file()
    project.pulse_file.write_project_setup_in_file(mesher_setup)
    project.pulse_file.write_analysis_setup_in_file(model.analysis_setup)

    ## Build the mathematical model and solve it (it also saves the model results in the temp_pulse folder)
    project.build_model_and_solve(running_by_script=True)

    # natural_frequencies = project.acoustic_solver.natural_frequencies
    # print(f"Natural frequencies: \n {natural_frequencies.reshape(-1, 1)}")

    ## Uncomment the following function to remove the created files from the temp_pulse folder
    # remove_files_from_temporary_folder()


def create_fluids():

    fluids = dict()
    fluids[1] = Fluid(  
                      'water_discharge',
                      1003.82244263,
                      1592.49759889,
                      identifier = 1,
                      isentropic_exponent = 1.03559951,
                      thermal_conductivity = 6.51065153e-01,
                      specific_heat_Cp = 4110.65882430,
                      dynamic_viscosity = 6.01700293e-04,
                      temperature = 318.15,
                      pressure = 3.23193250e+07,
                      molar_mass  = 18.015268,
                      adiabatic_bulk_modulus = 2545742502.755067,
                      vapor_pressure = 9595.337826781679,
                      color = [0, 170, 255]
                      )

    fluids[2] = Fluid(  
                      'N2_discharge',
                      292.28440365,
                      500.45290389,
                      identifier = 2,
                      isentropic_exponent = 1.67039582,
                      thermal_conductivity = 4.53652092e-02,
                      specific_heat_Cp = 1322.24682798,
                      dynamic_viscosity = 2.74922337e-05,
                      temperature = 318.15,
                      pressure = 3.23193250e+07,
                      molar_mass  = 28.01348,
                      adiabatic_bulk_modulus = 73203537.61198233,
                      color = [255, 255, 0]
                      )

    return fluids


def create_materials():

    materials = dict()
    materials[1] = Material(
                            'stainless_steel', 
                            7860, 
                            identifier = 1, 
                            elasticity_modulus = 210e9, 
                            poisson_ratio = 0.3,
                            thermal_expansion_coefficient = 1.2e-5,
                            color = [253, 152, 145]
                            )

    return materials


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

    project.pulse_file.write_fluid_library_in_file(config)


def create_temporary_material_library(project: Project, materials: dict):

    from configparser import ConfigParser
    config = ConfigParser()

    for mat_id, material in materials.items():
        material: Material
        config[f"{mat_id}"] = {
                                "name": material.name,
                                "identifier": material.identifier,
                                "color": material.color,
                                "density": material.density,
                                "elasticity_modulus": material.elasticity_modulus / 1e9,
                                "poisson_ratio": material.poisson_ratio,
                                "thermal_expansion_coefficient": material.thermal_expansion_coefficient,
                                }

    project.pulse_file.write_material_library_in_file(config)


def get_reciprocating_pump_excitation(connection_type: str):

    from pulse.model.reciprocating_pump_model import ReciprocatingPumpModel

    fluids = create_fluids()

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
                  'bulk_modulus' : fluids[1].bulk_modulus
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

    analysis_setup = project.pulse_file.read_analysis_setup_from_file()
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
    test_coupled_harmonic_analysis()