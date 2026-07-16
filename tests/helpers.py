from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project


def create_air_fluid():
    """Standard air fluid used in structural and acoustic analyses."""
    fluids = dict()
    fluids[1] = Fluid(
        name='air',
        identifier=1,
        temperature=293.15,
        pressure=101325,
        density=1.204263,
        speed_of_sound=343.395034,
        isentropic_exponent=1.401985,
        thermal_conductivity=0.025503,
        specific_heat_Cp=1006.400178,
        dynamic_viscosity=float(1.8247e-5),
        molar_mass=28.958601,
        color=[0, 170, 255],
    )
    return fluids


def create_stainless_steel_material():
    """Standard stainless steel material."""
    materials = dict()
    materials[1] = Material(
        name='stainless_steel',
        identifier=1,
        density=7860,
        elasticity_modulus=210e9,
        poisson_ratio=0.3,
        thermal_expansion_coefficient=1.2e-5,
        color=[253, 152, 145],
    )
    return materials


def create_temporary_fluid_library(project: Project, fluids: dict):
    fluid_data = dict()
    for fluid_id, fluid in fluids.items():
        fluid: Fluid
        fluid_data[f"{fluid_id}"] = {
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
    project.file.write_fluid_library_in_file(fluid_data)


def create_temporary_material_library(project: Project, materials: dict):
    material_data = dict()
    for mat_id, material in materials.items():
        material: Material
        material_data[f"{mat_id}"] = {
            "name": material.name,
            "identifier": material.identifier,
            "color": material.color,
            "density": material.density,
            "elasticity_modulus": material.elasticity_modulus / 1e9,
            "poisson_ratio": material.poisson_ratio,
            "thermal_expansion_coefficient": material.thermal_expansion_coefficient,
        }
    project.file.write_material_library_in_file(material_data)
