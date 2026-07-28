import numpy as np
import pytest
from scipy.sparse.linalg import norm as sparse_norm

from examples.example_file_helper import get_example_file_path
from pulse.model import AnalysisID
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.data_classes.project_setup_data_classes import ImportType, MesherSetup, ProjectSetup
from pulse.model.properties.material import Material
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.project.project import Project


@pytest.fixture
def model(tmp_path):

    steel = Material(
        name = 'Steel',
        identifier = 1,
        density = 7850,
        elasticity_modulus = 200e9,
        poisson_ratio = 0.3,
        )

    section_parameters = [0.05, 0.008, 0, 0, 0, 0]
    pipe_section_info = PipeCrossSection(*section_parameters)

    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    project = Project()
    project.initialize_pulse_file_and_loader(dir_path=tmp_path)

    model = project.model
    preprocessor = model.preprocessor

    geometry_path = get_example_file_path("iges_files/new_geometries/example_2_withBeam.iges")

    ## Configure the project setup
    project_setup = ProjectSetup(
        import_type = ImportType.CAD_FILE,
        geometry_path_internal = str(geometry_path),
        mesher_setup = MesherSetup(0.01, 1e-6, "meter"))

    project.reset(reset_all=True)
    project.set_project_setup(project_setup)

    ## Process the geometry and mesh
    model.process_geometry_and_mesh()

    all_lines = model.mesh.lines_from_model
    preprocessor.set_material_by_lines(all_lines, steel)
    preprocessor.set_cross_section_by_lines(all_lines, cross_section)

    # Prescribe DOFs at three support nodes
    points_coords = np.array([
        [0.000,  0.000,  0.000],
        [2.000, -0.250,  1.250],
        [0.850,  1.000, -0.750],
    ], dtype=float)

    for coords in points_coords:
        node_id = preprocessor.get_node_id_by_coordinates(coords)
        assert node_id is not None, f"Node not found at coordinates {coords}"
        prescribed_dofs = [0j, 0j, 0j, 0j, 0j, 0j]
        real_values = [np.real(v) for v in prescribed_dofs]
        imag_values = [np.imag(v) for v in prescribed_dofs]
        data = {
            "coords": list(coords),
            "values": prescribed_dofs,
            "real_values": real_values,
            "imag_values": imag_values,
        }
        model.properties._set_nodal_property("prescribed_dofs", data, node_id)

    # Set frequencies so AssemblyStructural can read model.frequencies
    analysis_setup = {
        "analysis_id": AnalysisID.STRUCTURAL_HARMONIC,
        "f_min": 0,
        "f_max": 200,
        "f_step": 2,
    }
    model.set_analysis_setup(analysis_setup)

    assembly = AssemblyStructural(model)
    names = ['K', 'M', 'Kr', 'Mr']
    answer = assembly.get_global_matrices()

    return dict(zip(names, answer))


def test_global_matrices(model):
    for name, matrix in model.items():
        assert matrix is not None, f"Matrix {name} is None"
        assert matrix.nnz > 0, f"Matrix {name} has no non-zero entries"

    # K and M are (n_free x n_free) — must be square
    K, M = model["K"], model["M"]
    assert K.shape[0] == K.shape[1], "K matrix is not square"
    assert M.shape[0] == M.shape[1], "M matrix is not square"

    # Kr and Mr have shape (n_total x n_prescribed) where n_total = n_free + n_prescribed
    Kr, Mr = model["Kr"], model["Mr"]
    assert Kr.shape[0] == K.shape[0] + Kr.shape[1], "Kr total DOF count inconsistent"
    assert Mr.shape[0] == M.shape[0] + Mr.shape[1], "Mr total DOF count inconsistent"

    # Structural stiffness and mass matrices must be symmetric
    diff_K = K - K.T
    diff_M = M - M.T
    assert sparse_norm(diff_K) / sparse_norm(K) < 1e-10, "K matrix is not symmetric"
    assert sparse_norm(diff_M) / sparse_norm(M) < 1e-10, "M matrix is not symmetric"


