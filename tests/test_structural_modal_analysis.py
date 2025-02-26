
from pulse.model.cross_section import CrossSection, get_beam_section_properties
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project

# import pytest
import numpy as np

from pathlib import Path

# Setting up model
# @pytest.fixture

def test_structural_modal_analysis():

    ## Initialize a project

    project = Project()
    project.initialize_pulse_file()

    ## Define usefull objects

    model = project.model
    mesh = model.mesh
    preprocessor = model.preprocessor

    # Load geometry file (only the *.iges and *.step formats are supported)
    geometry_path = Path("examples/iges_files/new_geometries/example_2_withBeam.iges")

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

    ## Define the fluid
    # fluid = Fluid(  
    #                 'Air',
    #                 1.204263,
    #                 343.395034,
    #                 isentropic_exponent = 1.401985,
    #                 thermal_conductivity = 0.025503,
    #                 specific_heat_Cp = 1006.400178,
    #                 dynamic_viscosity = float(1.8247e-5),
    #                 temperature = 293.15,
    #                 pressure = 101325,
    #                 molar_mass  = 28.958601
    #                 )

    ## Define the material
    material = Material(
                        'Carbon Steel', 
                        7860, 
                        identifier = 1, 
                        elasticity_modulus = 210e9, 
                        poisson_ratio = 0.3,
                        thermal_expansion_coefficient = 1.2e-5,
                        )

    create_material_library(project, material)

    all_lines = project.model.mesh.lines_from_model
    preprocessor.set_material_by_lines(all_lines, material)
    model.properties._set_line_property("material_id", material.identifier, all_lines)
    model.properties._set_line_property("material", material, all_lines)

    ## Create the model cross-sections

    main_section_info = {"section_type_label" : "pipe" ,
                        "section_parameters" : [0.100, 0.008, 0, 0, 0, 0]}

    branch_section_info = {"section_type_label" : "pipe" ,
                           "section_parameters" : [0.050, 0.008, 0, 0, 0, 0]}

    beam_section_parameters = [0.16, 0.12, 0.01, 0.12, 0.01, 0.01, 0.0, 0.0]
    beam_section_info = {"section_type_label" : "i_beam" ,
                         "section_parameters" : beam_section_parameters,
                         "section_properties" : get_beam_section_properties("i_beam", beam_section_parameters)}

    cross_section_main = CrossSection(pipe_section_info = main_section_info)
    cross_section_branch = CrossSection(pipe_section_info = branch_section_info)
    cross_section_beam = CrossSection(beam_section_info = beam_section_info)

    beam_lines = [20, 23, 24]
    branch_lines = [31, 32, 33]
    main_lines = [line_id for line_id in all_lines if line_id not in beam_lines + branch_lines]

    ## Assign the cross-sections to main lines

    for line_id in main_lines:
        center_coords = model.properties._get_property("center_coords", line_id=line_id)
        corner_coords = model.properties._get_property("corner_coords", line_id=line_id)

        if (center_coords, corner_coords).count(None) == 2:
            section_label = main_section_info["section_type_label"]
            model.properties._set_line_property("structure_name", section_label, line_id)
        else:
            model.properties._set_line_property("structure_name", "bend", line_id)

    model.properties._set_multiple_line_properties(main_section_info, main_lines)
    model.properties._set_line_property("cross_section", cross_section_main, main_lines)
    model.properties._set_line_property("structural_element_type", "pipe_1", main_lines)
    preprocessor.set_cross_section_by_lines(main_lines, cross_section_main)
    preprocessor.set_structural_element_type_by_lines(main_lines, "pipe_1")

    ## Assign the cross-sections to branch lines

    for line_id in branch_lines:
        center_coords = model.properties._get_property("center_coords", line_id=line_id)
        corner_coords = model.properties._get_property("corner_coords", line_id=line_id)

        if (center_coords, corner_coords).count(None) == 2:
            section_label = branch_section_info["section_type_label"]
            model.properties._set_line_property("structure_name", section_label, line_id)
        else:
            model.properties._set_line_property("structure_name", "bend", line_id)

    model.properties._set_multiple_line_properties(branch_section_info, branch_lines)
    model.properties._set_line_property("cross_section", cross_section_branch, branch_lines)
    model.properties._set_line_property("structural_element_type", "pipe_1", branch_lines)
    preprocessor.set_cross_section_by_lines(branch_lines, cross_section_branch)
    preprocessor.set_structural_element_type_by_lines(branch_lines, "pipe_1")

    ## Assign the cross-sections to beam lines

    model.properties._set_line_property("structure_name", beam_section_info["section_type_label"], beam_lines)
    model.properties._set_multiple_line_properties(beam_section_info, beam_lines)
    model.properties._set_line_property("cross_section", cross_section_beam, beam_lines)
    model.properties._set_line_property("structural_element_type", "beam_1", beam_lines)
    preprocessor.set_cross_section_by_lines(beam_lines, cross_section_beam)
    preprocessor.set_structural_element_type_by_lines(beam_lines, "beam_1")

    ## Apply the dofs prescriptions

    points_coords = np.array([[ 0.000,  0.000,  0.000],
                              [ 2.000, -0.250,  1.250],
                              [ 0.850,  1.000, -0.750],
                              [ 1.350,  1.250,  0.500],
                              [ 0.850,  0.000,  0.500]], dtype=float)

    for coords in points_coords:

        node_id = preprocessor.get_node_id_by_coordinates(coords)

        prescribed_dofs = [0j, 0j, 0j, 0j, 0j, 0j]
        real_values = [value if value is None else np.real(value) for value in prescribed_dofs]
        imag_values = [value if value is None else np.imag(value) for value in prescribed_dofs]

        data = {
                "coords" : list(coords),
                "values" : prescribed_dofs,
                "real_values" : real_values,
                "imag_values" : imag_values
                }

        model.properties._set_nodal_property("prescribed_dofs", data, node_id)

    ## Define the analysis setup

    analysis_setup = {
                      "analysis_id" : 2,
                      "modes" : 40,
                      "sigma_factor" : 1e-2
                      }

    model.set_analysis_setup(analysis_setup = analysis_setup)

    # write data in file
    project.pulse_file.write_line_properties_in_file()
    project.pulse_file.write_nodal_properties_in_file()
    project.pulse_file.write_project_setup_in_file(mesher_setup)
    project.pulse_file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    natural_frequencies = project.structural_solver.natural_frequencies
    print(f"Natural frequencies: \n {natural_frequencies.reshape(-1, 1)}")

    # remove_files_from_temporary_folder()

def create_material_library(project: Project, material: Material):

    from configparser import ConfigParser
    config = ConfigParser()

    config[f"{material.identifier}"] = {
                                        "name": material.name,
                                        "identifier": material.identifier,
                                        "color": "[200, 200, 200]",
                                        "density": material.density,
                                        "elasticity_modulus": material.elasticity_modulus / 1e9,
                                        "poisson_ratio": material.poisson_ratio,
                                        "thermal_expansion_coefficient": material.thermal_expansion_coefficient,
                                        }

    project.pulse_file.write_material_library_in_file(config)

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
    test_structural_modal_analysis()