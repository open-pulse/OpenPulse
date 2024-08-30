from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect
from pathlib import Path

from pulse import app
from pulse.interface.menu.common_menu_items import CommonMenuItems
from pulse.interface.user_input.project.print_message import PrintMessageInput


class ModelAndAnalysisSetupItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.project = app().project

        self._create_items()
        self._create_connections()
        self._update_items()

    def keyPressEvent(self, event):
        """This deals with key events that are directly linked with the menu."""
        if event.key() == Qt.Key_F5:
            self.item_child_run_analysis_callback()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_create_geometry = self.add_item('Create/Edit Geometry')
        self.item_child_set_material = self.add_item('Set Material')
        self.item_child_set_fluid = self.add_item('Set Fluid')
        self.item_child_set_crossSection = self.add_item('Set Cross-Section')
        #
        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup')
        self.item_child_set_structural_element_type = self.add_item('Set Structural Element Type')
        self.item_child_set_prescribed_dofs = self.add_item('Set Prescribed DOFs')
        self.item_child_set_nodal_loads = self.add_item('Set Nodal Loads')
        self.item_child_add_mass_spring_damper = self.add_item('Add: Mass / Spring / Damper')
        self.item_child_add_elastic_nodal_links = self.add_item('Add Elastic Nodal Links')
        self.item_child_set_beam_xaxis_rotation = self.add_item('Set Beam X-axis Rotation')
        self.item_child_set_rotation_decoupling_dofs = self.add_item('Set B2P Rotation Decoupling')
        self.item_child_set_stress_stiffening = self.add_item('Set Stress Stiffening')
        self.item_child_add_valve = self.add_item('Add Valve')
        self.item_child_add_expansion_joint = self.add_item('Add Expansion Joint')
        self.item_child_set_inertial_loads = self.add_item('Set Inertial Loads')
        #
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')
        self.item_child_set_acoustic_element_type = self.add_item('Set Acoustic Element Type')
        self.item_child_set_acoustic_pressure = self.add_item('Set Acoustic Pressure')
        self.item_child_set_volume_velocity = self.add_item('Set Volume Velocity')
        self.item_child_set_specific_impedance = self.add_item('Set Specific Impedance')
        self.item_child_set_radiation_impedance = self.add_item('Set Radiation Impedance')
        self.item_child_add_perforated_plate = self.add_item('Add Perforated Plate')
        self.item_child_set_acoustic_element_length_correction = self.add_item('Set Element Length Correction')
        self.item_child_add_compressor_excitation = self.add_item('Add Compressor Excitation')
        #
        self.item_top_analysis = self.add_top_item('Analysis')
        self.item_child_select_analysis_type = self.add_item('Select Analysis Type')
        self.item_child_analysis_setup = self.add_item('Analysis Setup')
        self.item_child_run_analysis = self.add_item('Run Analysis')

        self.top_level_items = [self.item_top_general_settings,
                                self.item_top_structural_model_setup,
                                self.item_top_acoustic_model_setup,
                                self.item_top_analysis]

    def _create_connections(self):
        #
        # General Settings
        self.item_child_create_geometry.clicked.connect(self.item_child_create_geometry_callback)
        self.item_child_set_material.clicked.connect(self.item_child_set_material_callback)
        self.item_child_set_fluid.clicked.connect(self.item_child_set_fluid_callback)
        self.item_child_set_crossSection.clicked.connect(self.item_child_set_cross_section_callback)
        #
        # Structural Model Setup
        self.item_child_set_structural_element_type.clicked.connect(self.item_child_set_structural_element_type_callback)
        self.item_child_set_prescribed_dofs.clicked.connect(self.item_child_set_prescribed_dofs_callback)
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
        self.item_child_add_compressor_excitation.clicked.connect(self.item_child_add_compressor_excitation_callback)
        #
        # Analysis Setup
        self.item_child_select_analysis_type.clicked.connect(self.item_child_select_analysis_type_callback)
        self.item_child_analysis_setup.clicked.connect(self.item_child_analisys_setup_callback)
        self.item_child_run_analysis.clicked.connect(self.item_child_run_analysis_callback)
        #
        app().main_window.theme_changed.connect(self.set_theme)

    # def create_plot_convergence_data(self):
    #     self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)

    # Callbacks
    def item_child_create_geometry_callback(self):
        app().main_window.input_ui.call_geometry_editor()

    def item_child_edit_geometry_callback(self):
        obj = app().main_window.input_ui.edit_an_imported_geometry()

    def item_child_set_material_callback(self):
        previous_color_mode = app().main_window.get_color_mode()
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.action_plot_material_callback()
        app().main_window.input_ui.set_material()
        app().main_window.set_input_widget(None)
        app().main_window.set_color_mode(previous_color_mode)

    def item_child_set_fluid_callback(self):
        previous_color_mode = app().main_window.get_color_mode()
        app().main_window.action_plot_fluid_callback()
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.input_ui.set_fluid()
        app().main_window.set_input_widget(None)
        app().main_window.set_color_mode(previous_color_mode)
    
    def item_child_set_cross_section_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines_with_cross_sections()
        app().main_window.input_ui.set_cross_section()
        app().main_window.set_input_widget(None)

    def item_child_set_structural_element_type_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.input_ui.set_structural_element_type()
        app().main_window.set_input_widget(None)

    def item_child_set_prescribed_dofs_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.set_prescribed_dofs()
        app().main_window.set_input_widget(None)

    def item_child_set_nodal_loads_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.set_nodal_loads()
        app().main_window.set_input_widget(None)

    def item_child_add_mass_spring_damper_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.add_mass_spring_damper()
        app().main_window.set_input_widget(None)

    def item_child_add_elastic_nodal_links_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.add_elastic_nodal_links()
        app().main_window.set_input_widget(None)

    def item_child_set_inertial_loads_callback(self):
        obj = app().main_window.input_ui.set_inertial_load()
        if obj.complete:
            app().main_window.plot_mesh()
        app().main_window.set_input_widget(None)

    def item_child_set_stress_stiffening_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines_with_cross_sections()
        app().main_window.input_ui.set_stress_stress_stiffening()
        app().main_window.set_input_widget(None)

    def item_child_add_valve_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.input_ui.add_valve()
        app().main_window.set_input_widget(None)

    def item_child_add_expansion_joint_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.input_ui.add_expansion_joint()
        app().main_window.set_input_widget(None)

    def item_child_set_beam_x_axis_rotation_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines_with_cross_sections()
        app().main_window.input_ui.set_beam_xaxis_rotation()
        app().main_window.set_input_widget(None)

    def item_child_set_rotation_decoupling_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.set_rotation_decoupling_dofs()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_element_type_callback(self):
        if app().main_window.action_show_mesh_data.isChecked():
            app().main_window.plot_lines()
        app().main_window.input_ui.set_acoustic_element_type()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_pressure_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()      
        app().main_window.input_ui.set_acoustic_pressure()
        app().main_window.set_input_widget(None)

    def item_child_set_volume_velocity_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()  
        app().main_window.input_ui.set_volume_velocity()
        app().main_window.set_input_widget(None)

    def item_child_set_specific_impedance_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh() 
        app().main_window.input_ui.set_specific_impedance()
        app().main_window.set_input_widget(None)

    def item_child_set_radiation_impedance_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.set_radiation_impedance()
        app().main_window.set_input_widget(None)

    def item_child_add_perforated_plate_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.add_perforated_plate()
        app().main_window.set_input_widget(None)

    def item_child_set_acoustic_element_length_correction_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.set_acoustic_element_length_correction()
        app().main_window.set_input_widget(None)

    def item_child_add_compressor_excitation_callback(self):
        if app().main_window.action_show_geometry_data.isChecked():
            app().main_window.plot_mesh()
        app().main_window.input_ui.add_compressor_excitation()
        app().main_window.set_input_widget(None)

    def item_child_select_analysis_type_callback(self):
        app().main_window.input_ui.analysis_type_input()
        self._update_items()
    
    def item_child_analisys_setup_callback(self):
        app().main_window.input_ui.analysis_setup()
        self._update_items()

    def item_child_run_analysis_callback(self):
        app().main_window.input_ui.run_analysis()
        self._update_items()

    def enable_actions_according_to_import_type(self):
        import_type = app().project.model.mesh.import_type
        if import_type == 0:
            pass

    # Items access
    def modify_geometry_item_access(self, bool_key):
        self.item_child_create_geometry.setDisabled(bool_key)

    def modify_general_settings_items_access(self, bool_key):
        self.item_child_create_geometry.setDisabled(bool_key)
        # self.item_child_set_material.setDisabled(bool_key)
        # self.item_child_set_fluid.setDisabled(bool_key)
        # self.item_child_set_crossSection.setDisabled(bool_key)

    def modify_model_setup_items_access(self, bool_key):
        #
        self.item_child_create_geometry.setDisabled(bool_key)
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_set_crossSection.setDisabled(bool_key)
        #
        self.item_child_set_structural_element_type.setDisabled(bool_key) 
        self.item_child_set_prescribed_dofs.setDisabled(bool_key)
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
        self.item_child_add_compressor_excitation.setDisabled(bool_key)
        #
        self.item_child_select_analysis_type.setDisabled(bool_key)
        if bool_key:
            self.item_child_analysis_setup.setDisabled(True)
            self.item_child_run_analysis.setDisabled(True)

    def _update_items(self):
        """ Enables and disables the child items on the menu after
            the solution is done.
        """
        self.modify_model_setup_items_access(False)
        self.item_child_analysis_setup.setDisabled(True)
        self.item_child_run_analysis.setDisabled(True)
                    
        if self.project.analysis_id in [None, 2, 4]:
            self.item_child_analysis_setup.setDisabled(True)
        else:
            self.item_child_analysis_setup.setDisabled(False)
        
        if self.project.analysis_id is not None and self.project.setup_analysis_complete:
            self.item_child_run_analysis.setDisabled(False)
            
    def update_structural_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(True)
        
    def update_acoustic_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(False)

    def update_coupled_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(False)

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

        border_role = Qt.UserRole + 1
        # border_pen = QPen(self.background_color)
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)
            
        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)