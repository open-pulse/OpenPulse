
tooltips: dict[str, str] = dict()

# general settings
tooltips["create_geometry"] = ("")

tooltips["set_material"] = (
    "Add/edit materials from the materials library or assign "
    "a material to selected entities."
)

tooltips["set_fluid"] = (
    "Add/edit fluids from the fluids library or assign "
    "a fluid to selected entities."
)

tooltips["set_cross_section"] = ("")

# structural model Setup
tooltips["set_structural_element_type"] = ("")

tooltips["set_prescribed_dofs"] = (
    "Define the prescribed values for the structural degrees of freedom."
)

tooltips["set_nodal_loads"] = (
    "Set equally distributed structural nodal loads on the selected entities."
)

tooltips["add_mass_spring_damper"] = ("")

tooltips["add_elastic_nodal_links"] = ("")

tooltips["set_beam_xaxis_rotation"] = ("")

tooltips["set_rotation_decoupling_dofs"] = ("")

tooltips["set_stress_stiffening"] = ("")

tooltips["add_valve"] = ("")

tooltips["add_expansion_joint"] = ("")

tooltips["set_inertial_loads"] = ("")

# acoustic model setup
tooltips["set_acoustic_element_type"] = ("")

tooltips["set_acoustic_pressure"] = (
    "Create a boundary condition that prescribes an acoustic pressure at the domain boundary."
)

tooltips["set_volume_velocity"] = ("")

tooltips["set_specific_impedance"] = (
    "Define a specific impedance (real or complex) at a domain boundary."
)

tooltips["set_radiation_impedance"] = ("")

tooltips["add_perforated_plate"] = (
    "Set an internal perforated plate in the acoustic model to simulate the pressure drop "
    "across this component."
)

tooltips["set_acoustic_element_length_correction"] = ("")

tooltips["add_reciprocating_compressor_excitation"] = (
    "Add an idealized reciprocating compressor excitation in the form of an equivalent surface velocity."
)

tooltips["add_reciprocating_pump_excitation"] = ("")

tooltips["add_acoustic_transfer_element"] = (
    "Configure the surfaces where the acoustic transfer element will be computed."
)

tooltips["turn_off_acoustic_elements"] = ("")