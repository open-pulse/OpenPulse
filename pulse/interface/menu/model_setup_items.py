from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.menu.common_menu_items import ChildTreeWidgetItem, CommonMenuItems


class ModelSetupItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.project = app().project

        self._create_items()
        self._create_connections()
        self.update_tooltips_warnings()
        self._connect_domain_filter()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_set_material = self.add_item('Material', property_name="material")
        self.item_child_set_fluid = self.add_item('Fluid', property_name="fluid")
        self.item_child_set_crossSection = self.add_item('Cross-Section', property_name="cross_section")
        #
        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup')
        self.item_child_set_structural_element_type = self.add_item('Structural Element Type', property_name="structural_element_type")
        self.item_child_set_prescribed_dof = self.add_item('Prescribed DOF', property_name="prescribed_dofs")
        self.item_child_set_nodal_loads = self.add_item('Nodal Loads', property_name="nodal_loads")
        self.item_child_add_mass_spring_damper = self.add_item('Mass / Spring / Damper', property_name="mass_spring_damper")
        self.item_child_add_elastic_nodal_links = self.add_item('Elastic Nodal Links', property_name="elastic_nodal_links")
        self.item_child_set_beam_xaxis_rotation = self.add_item('Beam X-axis Rotation', property_name="beam_xaxis_rotation")
        self.item_child_set_rotation_decoupling_dofs = self.add_item('B2P Rotation Decoupling', property_name="rotation_decoupling_dofs")
        self.item_child_set_stress_stiffening = self.add_item('Stress Stiffening', property_name="stress_stiffening")
        self.item_child_add_valve = self.add_item('Valve', property_name="valve")
        self.item_child_add_expansion_joint = self.add_item('Expansion Joint', property_name="expansion_joint")
        self.item_child_set_inertial_loads = self.add_item('Inertial Loads', property_name="inertial_loads")
        #
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')
        self.item_child_set_acoustic_element_type = self.add_item('Acoustic Element Type', property_name="acoustic_element_type")
        self.item_child_set_acoustic_pressure = self.add_item('Acoustic Pressure', property_name="acoustic_pressure")
        self.item_child_set_volume_velocity = self.add_item('Volume Velocity', property_name="volume_velocity")
        self.item_child_set_specific_impedance = self.add_item('Specific Impedance', property_name="specific_impedance")
        self.item_child_set_radiation_impedance = self.add_item('Radiation Impedance', property_name="radiation_impedance")
        self.item_child_add_perforated_plate = self.add_item('Perforated Plate', property_name="perforated_plate")
        self.item_child_set_acoustic_element_length_correction = self.add_item('Element Length Correction', property_name="acoustic_element_length_correction")
        self.item_child_add_reciprocating_compressor_excitation = self.add_item('Reciprocating Compressor Excitation', property_name="reciprocating_compressor_excitation")
        self.item_child_add_reciprocating_pump_excitation = self.add_item('Reciprocating Pump Excitation', property_name="reciprocating_pump_excitation")
        self.item_child_add_acoustic_transfer_element = self.add_item('Acoustic Transfer Element', property_name="acoustic_transfer_element")
        self.item_child_turn_off_acoustic_elements = self.add_item('Turn-off Acoustic Elements', property_name="turn_off_acoustic_elements")
        #
        self.top_level_items = [
                                self.item_top_general_settings,
                                self.item_top_structural_model_setup,
                                self.item_top_acoustic_model_setup
                                ]

    def _create_connections(self):
        #
        # General Settings
        self.item_child_set_material.clicked.connect(self.item_child_set_material_callback)
        self.item_child_set_fluid.clicked.connect(self.item_child_set_fluid_callback)
        self.item_child_set_crossSection.clicked.connect(self.item_child_set_cross_section_callback)
        #
        # Structural Model Setup
        self.item_child_set_structural_element_type.clicked.connect(self.item_child_set_structural_element_type_callback)
        self.item_child_set_prescribed_dof.clicked.connect(self.item_child_set_prescribed_dof_callback)
        self.item_child_set_nodal_loads.clicked.connect(self.item_child_set_nodal_loads_callback)
        self.item_child_add_mass_spring_damper.clicked.connect(self.item_child_add_mass_spring_damper_callback)
        self.item_child_add_elastic_nodal_links.clicked.connect(self.item_child_add_elastic_nodal_links_callback)
        self.item_child_set_inertial_loads.clicked.connect(self.item_child_set_inertial_loads_callback)
        self.item_child_set_stress_stiffening.clicked.connect(self.item_child_set_stress_stiffening_callback)
        self.item_child_add_valve.clicked.connect(self.item_child_add_valve_callback)
        self.item_child_add_expansion_joint.clicked.connect(self.item_child_add_expansion_joint_callback)
        self.item_child_set_beam_xaxis_rotation.clicked.connect(self.item_child_set_beam_x_axis_rotation_callback)
        self.item_child_set_rotation_decoupling_dofs.clicked.connect(self.item_child_set_rotation_decoupling_callback)
        #
        # Acoustic Model Setup
        self.item_child_set_acoustic_element_type.clicked.connect(self.item_child_set_acoustic_element_type_callback)
        self.item_child_set_acoustic_pressure.clicked.connect(self.item_child_set_acoustic_pressure_callback)
        self.item_child_set_volume_velocity.clicked.connect(self.item_child_set_volume_velocity_callback)
        self.item_child_set_specific_impedance.clicked.connect(self.item_child_set_specific_impedance_callback)
        self.item_child_set_radiation_impedance.clicked.connect(self.item_child_set_radiation_impedance_callback)
        self.item_child_add_perforated_plate.clicked.connect(self.item_child_add_perforated_plate_callback)
        self.item_child_set_acoustic_element_length_correction.clicked.connect(self.item_child_set_acoustic_element_length_correction_callback)
        self.item_child_add_reciprocating_compressor_excitation.clicked.connect(self.item_child_add_reciprocating_compressor_excitation_callback)
        self.item_child_add_reciprocating_pump_excitation.clicked.connect(self.item_child_add_reciprocating_pump_excitation_callback)
        self.item_child_add_acoustic_transfer_element.clicked.connect(self.item_child_add_acoustic_transfer_element_callback)
        self.item_child_turn_off_acoustic_elements.clicked.connect(self.item_child_turn_off_acoustic_elements_callback)
        #
        app().main_window.theme_changed.connect(self.set_theme)

    # Callbacks

    def item_child_set_material_callback(self):
        previous_color_mode = app().main_window.get_color_mode()
        self.configure_render_according_to_inputs("lines")
        app().main_window.action_plot_material_callback()
        app().main_window.input_ui.set_material()
        app().main_window.set_input_widget(None)
        app().main_window.set_color_mode(previous_color_mode)

        self.update_tooltips_warnings()

    def item_child_set_fluid_callback(self):
        previous_color_mode = app().main_window.get_color_mode()
        app().main_window.action_plot_fluid_callback()
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_fluid()
        app().main_window.set_input_widget(None)
        app().main_window.set_color_mode(previous_color_mode)

        self.update_tooltips_warnings()

    def item_child_set_cross_section_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_cross_section()
        app().main_window.set_input_widget(None)

    def item_child_set_structural_element_type_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_structural_element_type()
        app().main_window.set_input_widget(None)

    def item_child_set_prescribed_dof_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.set_prescribed_dof()
        app().main_window.set_input_widget(None)

    def item_child_set_nodal_loads_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.set_nodal_loads()
        app().main_window.set_input_widget(None)

    def item_child_add_mass_spring_damper_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.add_mass_spring_damper()
        app().main_window.set_input_widget(None)

    def item_child_add_elastic_nodal_links_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.add_elastic_nodal_links()
        app().main_window.set_input_widget(None)

    def item_child_set_inertial_loads_callback(self):
        app().main_window.input_ui.set_inertial_load()
        app().main_window.set_input_widget(None)

    def item_child_set_stress_stiffening_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_stress_stress_stiffening()
        app().main_window.set_input_widget(None)

    def item_child_add_valve_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.add_valve()
        app().main_window.set_input_widget(None)

    def item_child_add_expansion_joint_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.add_expansion_joint()
        app().main_window.set_input_widget(None)

    def item_child_set_beam_x_axis_rotation_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_beam_xaxis_rotation()
        app().main_window.set_input_widget(None)

    def item_child_set_rotation_decoupling_callback(self):
        self.configure_render_according_to_inputs("elements")
        app().main_window.input_ui.set_rotation_decoupling_dofs()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_element_type_callback(self):
        self.configure_render_according_to_inputs("lines")
        app().main_window.input_ui.set_acoustic_element_type()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_pressure_callback(self):
        self.configure_render_according_to_inputs("nodes")     
        app().main_window.input_ui.set_acoustic_pressure()
        app().main_window.set_input_widget(None)

    def item_child_set_volume_velocity_callback(self):
        self.configure_render_according_to_inputs("nodes")  
        app().main_window.input_ui.set_volume_velocity()
        app().main_window.set_input_widget(None)

    def item_child_set_specific_impedance_callback(self):
        self.configure_render_according_to_inputs("nodes") 
        app().main_window.input_ui.set_specific_impedance()
        app().main_window.set_input_widget(None)

    def item_child_set_radiation_impedance_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.set_radiation_impedance()
        app().main_window.set_input_widget(None)

    def item_child_add_perforated_plate_callback(self):
        self.configure_render_according_to_inputs("elements")
        app().main_window.input_ui.add_perforated_plate()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_element_length_correction_callback(self):
        self.configure_render_according_to_inputs("elements")
        app().main_window.input_ui.set_acoustic_element_length_correction()
        app().main_window.set_input_widget(None)

    def item_child_add_reciprocating_compressor_excitation_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.add_reciprocating_compressor_excitation()
        app().main_window.set_input_widget(None)

    def item_child_add_reciprocating_pump_excitation_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.add_reciprocating_pump_excitation()
        app().main_window.set_input_widget(None)

    def item_child_add_acoustic_transfer_element_callback(self):
        self.configure_render_according_to_inputs("nodes")
        app().main_window.input_ui.add_acoustic_transfer_element()
        app().main_window.set_input_widget(None)

    def item_child_turn_off_acoustic_elements_callback(self):
        self.configure_render_according_to_inputs("elements")
        app().main_window.input_ui.turn_off_acoustic_elements()
        app().main_window.set_input_widget(None)

    def configure_render_according_to_inputs(self, set_by: str):

        geometry_data = app().main_window.action_show_geometry_data.isChecked()
        mesh_data = app().main_window.action_show_mesh_data.isChecked()
        lines = app().main_window.action_plot_lines.isChecked()
        lines_with_cross_sections = app().main_window.action_plot_lines_with_cross_section.isChecked()

        if set_by == "nodes":
            if not (mesh_data or geometry_data):
                app().main_window.plot_geometry_points()

        elif set_by == "elements":
            if not mesh_data:
                app().main_window.plot_mesh()

        elif set_by == "lines":
            if not (lines or lines_with_cross_sections):
                app().main_window.plot_lines_with_cross_sections()

    def enable_actions_according_to_import_type(self):
        import_type = app().project.model.mesh.import_type
        if import_type == 0:
            pass

    # Items access
    def modify_model_setup_items_access(self, bool_key):
        #
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_set_crossSection.setDisabled(bool_key)
        #
        self.item_child_set_structural_element_type.setDisabled(bool_key) 
        self.item_child_set_prescribed_dof.setDisabled(bool_key)
        self.item_child_set_nodal_loads.setDisabled(bool_key)
        self.item_child_add_mass_spring_damper.setDisabled(bool_key)
        self.item_child_set_inertial_loads.setDisabled(bool_key)
        self.item_child_add_elastic_nodal_links.setDisabled(bool_key)
        self.item_child_set_stress_stiffening.setDisabled(bool_key)
        self.item_child_add_valve.setDisabled(bool_key)
        self.item_child_add_expansion_joint.setDisabled(bool_key)  
        self.item_child_set_beam_xaxis_rotation.setDisabled(bool_key)
        self.item_child_set_rotation_decoupling_dofs.setDisabled(bool_key)
        #   
        self.item_child_set_acoustic_element_type.setDisabled(bool_key)
        self.item_child_set_acoustic_pressure.setDisabled(bool_key)
        self.item_child_set_volume_velocity.setDisabled(bool_key)
        self.item_child_set_specific_impedance.setDisabled(bool_key)
        self.item_child_set_radiation_impedance.setDisabled(bool_key)
        self.item_child_add_perforated_plate.setDisabled(bool_key)
        self.item_child_set_acoustic_element_length_correction.setDisabled(bool_key)
        self.item_child_add_reciprocating_compressor_excitation.setDisabled(bool_key)
        self.item_child_add_reciprocating_pump_excitation.setDisabled(bool_key)
        self.item_child_add_acoustic_transfer_element.setDisabled(bool_key)
        self.item_child_turn_off_acoustic_elements.setDisabled(bool_key)

    def set_theme(self, theme : str):

        if theme == "dark":
            # self.line_color = QColor(220,220,220)
            # self.line_color = QColor(26,115,232,150)
            self.line_color = QColor(107,137,185)
            self.background_color = QColor(60,60,70)

        else:
            # self.line_color = QColor(60,60,60)
            # self.line_color = QColor(26,115,232,150)
            self.line_color = QColor(107,137,185)
            self.background_color = QColor(230,230,230)

        border_role = Qt.ItemDataRole.UserRole + 1
        # border_pen = QPen(self.background_color)
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)
            
        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)
    
    def _get_physical_domain(self) -> str:
        try:
            return app().main_window.analysis_toolbar.combo_box_physical_domain.currentText().strip().lower()
        except Exception:
            return "structural"

    def needs_property(self, property_name: str, domain: str) -> bool:

        if property_name == "material":
            return True

        if property_name == "fluid":
            return domain in ["acoustic", "coupled"]

        return False

    def contains_property(self, property_name: str) -> bool:
        if (properties := app().project.model.properties) is None:
            return False

        return properties.is_the_property_applied(property_name)

    def update_items_apperence(self):
        physical_domain = self._get_physical_domain()
        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child: ChildTreeWidgetItem = top_level_items.child(index)

                if item_child.isDisabled():
                    continue

                item_child.set_warning(False)

                if self.contains_property(item_child.property_name):
                    item_child.set_icon()

                elif self.needs_property(item_child.property_name, physical_domain):
                    item_child.set_warning(True)

                else:
                    item_child.set_icon(visible=False)

    def update_tooltips_warnings(self):
        physical_domain = self._get_physical_domain()

        for top_level in self.top_level_items:
            for i in range(top_level.childCount()):
                item = top_level.child(i)
                prop_name = getattr(item, "property_name", "")

                if not prop_name:
                    continue

                is_needed = self.needs_property(prop_name, physical_domain)
                is_filled = self.contains_property(prop_name)

                if is_needed and not is_filled:
                    item.set_tooltips(requirement=True)
                else:
                    item.set_tooltips(requirement=False)

    def filter_by_domain(self):
        domain = self._get_physical_domain()
        self.item_top_general_settings.setHidden(False)

        show_structural = domain in ("structural", "coupled")
        show_acoustic = domain in ("acoustic", "coupled")

        self.item_top_structural_model_setup.setHidden(not show_structural)
        self.item_top_acoustic_model_setup.setHidden(not show_acoustic)

    def _connect_domain_filter(self):
        app().main_window.analysis_changed.connect(self.filter_by_domain)
        app().main_window.analysis_changed.connect(self.update_tooltips_warnings)
        app().main_window.analysis_changed.connect(self.update_items_apperence)
        self.filter_by_domain()
