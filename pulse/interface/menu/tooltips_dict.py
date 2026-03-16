tooltips: dict[str, str] = dict()

# general settings
tooltips["create_geometry"] = ("")

tooltips["set_material"] = (
    "Add/edit materials from the materials library or assign a material to selected lines."
    )

tooltips["set_fluid"] = (
    "Add/edit fluids from the fluids library or assign a fluid to selected lines."
    )

tooltips["set_cross_section"] = (
    "Configure the cross-section."
    )

# structural model setup
tooltips["set_structural_element_type"] = (
    "Define the structural element type at the selected lines."
    )

tooltips["set_prescribed_dof"] = (
    "Define the prescribed values for the structural degrees of freedom."
    )

tooltips["set_nodal_loads"] = (
    "Set structural nodal loads (forces and moments) at the selected nodes."
    )

tooltips["add_mass_spring_damper"] = (
    "Add a lumped element (mass, grounded stiffness and damping) at selected nodes."
    )

tooltips["add_elastic_nodal_links"] = (
    "Configure a stiffness or damping links between selected pair of nodes."
    )

tooltips["set_beam_xaxis_rotation"] = (
    "Configure the beam x-axis rotation at the selected lines."
    )

tooltips["set_rotation_decoupling_dofs"] = (
    "Use this feature to decouple the pipe rotation dof at the beam-to-pipe T-joints."
    )

tooltips["set_stress_stiffening"] = (
    "Enable the stress stiffening at the selected lines."
    )

tooltips["add_valve"] = (
    "Configure a valve."
    )

tooltips["add_expansion_joint"] = (
    "Configure an expansion joint."
    )

tooltips["set_inertial_loads"] = (
    "Configure the inertial loads."
    )

# acoustic model setup
tooltips["set_acoustic_element_type"] = (
    "Define the acoustic element type at the selected lines."
    )

tooltips["set_acoustic_pressure"] = (
    "Create a boundary condition that prescribes an acoustic pressure at the selected nodes."
    )

tooltips["set_volume_velocity"] = (
    "Define a volume velocity (real or complex) acoustic excitation at the selected nodes."
    )

tooltips["set_specific_impedance"] = (
    "Define a specific impedance (real or complex) at the selected nodes."
    )

tooltips["set_radiation_impedance"] = (
    "Set a radiation impedance (anechoic, flanged and unflanged) at the selected nodes."
    )

tooltips["add_perforated_plate"] = (
    "Set an internal perforated plate in the acoustic model to simulate the pressure drop "
    "across this component."
    )

tooltips["set_acoustic_element_length_correction"] = (
    "Enable the element length correction for side-branches, loops, and expansions/reductions."
    )

tooltips["add_reciprocating_compressor_excitation"] = (
    "Add an idealized reciprocating compressor excitation in the form of an equivalent volume velocity."
    )

tooltips["add_reciprocating_pump_excitation"] = (
    "Add an idealized reciprocating pump excitation in the form of an equivalent volume velocity."
    )

tooltips["add_acoustic_transfer_element"] = (
    "Configure the pair of nodes where the acoustic transfer element will connect."
    )

tooltips["turn_off_acoustic_elements"] = (
    "Use this feature to turn off acoustic elements of interest."
    )