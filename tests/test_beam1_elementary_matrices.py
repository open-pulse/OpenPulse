from pulse.model.cross_section import CrossSection, get_beam_section_properties
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project

# import pytest
import numpy as np

from pathlib import Path

# Setting up model
# @pytest.fixture

def test_elementary_matrices_for_beam1_element():

    ## Initialize a project
    project = Project()
    project.initialize_pulse_file()

    ## Define usefull objects
    model = project.model
    mesh = model.mesh
    preprocessor = model.preprocessor

    section_label = "rectangular_beam"
    section_parameters = [0.06, 0.10, 0.0, 0.0, 0.0, 0.0]

    # section_label = "i_beam"
    # section_parameters = [0.16, 0.12, 0.01, 0.12, 0.01, 0.01, 0.0, 0.0]

    line_id = 1
    length = 0.01

    # end_coords = [length, 0.0, 0.0]
    end_coords = [length/(3**(1/2)), length/(3**(1/2)), length/(3**(1/2))]

    geometry_info = {
                     "structure_name" : section_label ,
                     "start_coords": [0.0, 0.0, 0.0],
                     "end_coords": end_coords,
                     "section_type_label": section_label,
                     "section_parameters" : section_parameters,
                     "section_properties" : get_beam_section_properties(section_label, section_parameters),
                     "structural_element_type" : "beam_1"
                     }

    model.properties._set_multiple_line_properties(geometry_info, line_id)

    # for key, values in geometry_info.items():
    #     project.model.properties._set_line_property(key, values, line_ids=line_id)

    # Load geometry file (only the *.iges and *.step formats are supported)
    # geometry_path = Path("examples/iges_files/run_by_script/reciprocating_pump_piping.step")
    project.pulse_file.write_line_properties_in_file()

    ## Configure the mesher setup
    mesher_setup = {
                    "element_size" : 0.02,
                    "geometry_tolerance" : 1e-6,
                    "length_unit" : "meter",
                    "import_type" : 1,
                    # "geometry_path" : str(geometry_path)
                    }

    project.reset(reset_all=True)
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    ## Process the geometry and mesh
    preprocessor.generate()

    ## Define the material
    materials = create_materials()
    create_temporary_material_library(project, materials)

    preprocessor.set_material_by_lines(line_id, materials[1])
    model.properties._set_line_property("material_id", materials[1].identifier, line_id)
    model.properties._set_line_property("material", materials[1], line_id)

    ## Create the model cross-sections

    # section_parameters = [0.16, 0.12, 0.01, 0.12, 0.01, 0.01, 0.0, 0.0]
    # section_info = {
    #                 "section_type_label" : "i_beam" ,
    #                 "section_parameters" : section_parameters,
    #                 "section_properties" : get_beam_section_properties("i_beam", section_parameters)
    #                 }

    section_parameters = [0.06, 0.10, 0.0, 0.0, 0.0, 0.0]
    section_info = {
                    "section_type_label" : "rectangular_beam" ,
                    "section_parameters" : section_parameters,
                    "section_properties" : get_beam_section_properties("rectangular_beam", section_parameters)
                    }

    cross_section = CrossSection(beam_section_info = section_info)
    model.properties._set_line_property("cross_section", cross_section, line_id)

    preprocessor.set_cross_section_by_lines(line_id, cross_section)
    preprocessor.set_structural_element_type_by_lines(line_id, "beam_1")

    structural_elements = model.preprocessor.structural_elements
    element = structural_elements[1]

    Ke, Me = element.matrices_gcs()
    # np.savetxt("Ke_beam1.dat", Ke, delimiter=",", fmt="%.24e")
    # np.savetxt("Me_beam1.dat", Me, delimiter=",", fmt="%.24e")

    path = "tests/data/structural_elements/beam_1/"
    Ke_ref = np.loadtxt(path + "K_dense_diag.csv", delimiter=",")
    Me_ref = np.loadtxt(path + "M_dense_diag.csv", delimiter=",")

    diff_Ke = Ke - Ke_ref
    diff_Me = Me - Me_ref

    mask_Ke = Ke_ref != 0
    mask_Me = Me_ref != 0

    rel_diff_Ke = np.abs(diff_Ke[mask_Ke] / Ke_ref[mask_Ke])
    rel_diff_Me = np.abs(diff_Me[mask_Me] / Me_ref[mask_Me])

    max_diff_Ke = np.max(rel_diff_Ke)
    max_diff_Me = np.max(rel_diff_Me)

    print(f"Maximum relative difference for Ke matrix: {max_diff_Ke}" )
    print(f"Maximum relative difference for Me matrix: {max_diff_Me}" )

    assert np.max(rel_diff_Ke) < 1e-14
    assert np.max(rel_diff_Me) < 1e-14

    project.pulse_file.write_line_properties_in_file()
    project.pulse_file.write_project_setup_in_file(mesher_setup)
    project.pulse_file.write_analysis_setup_in_file(model.analysis_setup)

    remove_files_from_temporary_folder()

def create_materials():

    materials = dict()
    materials[1] = Material(
                            'carbon_steel', 
                            7850, 
                            identifier = 1, 
                            elasticity_modulus = 200e9, 
                            poisson_ratio = 0.3,
                            thermal_expansion_coefficient = 1.2e-5,
                            color = [253, 152, 145]
                            )

    return materials


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
    test_elementary_matrices_for_beam1_element()