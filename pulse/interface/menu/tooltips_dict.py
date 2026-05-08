tooltips: dict[str, str] = dict()

# general settings
tooltips["create_geometry"] = ("")

tooltips["material"] = (
    "Add/edit materials from the materials library or assign a material to selected lines."
    )

tooltips["fluid"] = (
    "Add/edit fluids from the fluids library or assign a fluid to selected lines."
    )

tooltips["cross_section"] = (
    "Use this feature to configure cross-sections for pipe and beam elements."
    )

# structural model setup
tooltips["structural_element_type"] = (
    "Define the structural element type at the selected lines."
    )

tooltips["prescribed_dofs"] = (
    "Define the prescribed values for the structural degrees of freedom."
    )

tooltips["nodal_loads"] = (
    "Set structural nodal loads (forces and moments) at the selected nodes."
    )

tooltips["mass_spring_damper"] = (
    "Add a lumped element (mass or grounded stiffness and damping) at selected nodes."
    )

tooltips["elastic_nodal_links"] = (
    "Configure a stiffness or damping link between selected pair of nodes."
    )

tooltips["beam_xaxis_rotation"] = (
    "Configure the beam x-axis rotation at the selected lines."
    )

tooltips["rotation_decoupling_dofs"] = (
    "Use this feature to decouple the pipe rotation dof at the beam-to-pipe T-joints."
    )

tooltips["stress_stiffening"] = (
    "Enable the stress stiffening at the selected lines."
    )

tooltips["valve"] = (
    "Use this feature to configure and add a valve."
    )

tooltips["expansion_joint"] = (
    "Use this feature to configure and add an expansion joint."
    )

tooltips["inertial_loads"] = (
    "Configure the inertial loads."
    )

# acoustic model setup
tooltips["acoustic_element_type"] = (
    "Define the acoustic element type at the selected lines."
    )

tooltips["acoustic_pressure"] = (
    "Create a boundary condition that prescribes an acoustic pressure at the selected nodes."
    )

tooltips["volume_velocity"] = (
    "Define a volume velocity (real or complex) acoustic excitation at the selected nodes."
    )

tooltips["specific_impedance"] = (
    "Define a specific impedance (real or complex) at the selected nodes."
    )

tooltips["radiation_impedance"] = (
    "Set a radiation impedance (anechoic, flanged and unflanged) at the selected nodes."
    )

tooltips["perforated_plate"] = (
    "Set an internal perforated plate in the acoustic model to simulate the pressure drop "
    "across this component."
    )

tooltips["acoustic_element_length_correction"] = (
    "Enable the element length correction for side-branches, loops, and expansions/reductions."
    )

tooltips["reciprocating_compressor_excitation"] = (
    "Add an idealized reciprocating compressor excitation in the form of an equivalent volume velocity."
    )

tooltips["reciprocating_pump_excitation"] = (
    "Add an idealized reciprocating pump excitation in the form of an equivalent volume velocity."
    )

tooltips["acoustic_transfer_element"] = (
    "Configure the pair of nodes where the acoustic transfer element will connect."
    )

tooltips["turn_off_acoustic_elements"] = (
    "Use this feature to turn off acoustic elements of interest."
    )
