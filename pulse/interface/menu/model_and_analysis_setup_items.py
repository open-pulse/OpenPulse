from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect
from pathlib import Path

from pulse.interface.menu.common_menu_items import CommonMenuItems
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput


class ModelAndAnalysisSetupItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self.project = main_window.getProject()

        self._create_items()
        self._create_connections()
        self._update_items()

    def keyPressEvent(self, event):
        """This deals with key events that are directly linked with the menu."""
        if event.key() == Qt.Key_F5:
            self.mainWindow.getInputWidget().run_analysis()
            self._update_items()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_createGeometry = self.add_item('Create/Edit Geometry')
        self.item_child_set_material = self.add_item('Set Material')
        self.item_child_set_fluid = self.add_item('Set Fluid')
        self.item_child_set_crossSection = self.add_item('Set Cross-Section')
        #
        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup')
        self.item_child_setStructuralElementType = self.add_item('Set Structural Element Type')
        self.item_child_setPrescribedDofs = self.add_item('Set Prescribed DOFs')
        self.item_child_setNodalLoads = self.add_item('Set Nodal Loads')
        self.item_child_addMassSpringDamper = self.add_item('Add: Mass / Spring / Damper')
        self.item_child_add_elastic_nodal_links = self.add_item('Add Elastic Nodal Links')
        self.item_child_set_inertial_loads = self.add_item('Set Inertial Loads')
        self.item_child_set_stress_stiffening = self.add_item('Set Stress Stiffening')
        self.item_child_setcappedEnd = self.add_item('Set Capped End')
        self.item_child_add_valve = self.add_item('Add Valve')
        self.item_child_addFlanges = self.add_item('Add Connecting Flanges')
        self.item_child_add_expansion_joint = self.add_item('Add Expansion Joint')
        self.item_child_setBeamXaxisRotation = self.add_item('Set Beam X-axis Rotation')
        self.item_child_setRotationDecoupling = self.add_item('Set Rotation Decoupling')
        #
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')
        self.item_child_setAcousticElementType = self.add_item('Set Acoustic Element Type')
        self.item_child_setAcousticPressure = self.add_item('Set Acoustic Pressure')
        self.item_child_setVolumeVelocity = self.add_item('Set Volume Velocity')
        self.item_child_setSpecificImpedance = self.add_item('Set Specific Impedance')
        self.item_child_set_radiation_impedance = self.add_item('Set Radiation Impedance')
        self.item_child_add_perforated_plate = self.add_item('Add Perforated Plate')
        self.item_child_set_acoustic_element_length_correction = self.add_item('Set Element Length Correction')
        self.item_child_add_compressor_excitation = self.add_item('Add Compressor Excitation')
        #
        self.item_top_analysis = self.add_top_item('Analysis')
        self.item_child_select_analysis_type = self.add_item('Select Analysis Type')
        self.item_child_analysis_setup = self.add_item('Analysis Setup')
        self.item_child_run_analysis = self.add_item('Run Analysis')

    def _create_connections(self):
        # General Settings
        self.item_child_createGeometry.clicked.connect(self.item_child_create_geometry_callback)
        self.item_child_set_material.clicked.connect(self.item_child_set_material_callback)
        self.item_child_set_fluid.clicked.connect(self.item_child_set_fluid_callback)
        self.item_child_set_crossSection.clicked.connect(self.item_child_set_cross_section_callback)
        # Structural Model Setup
        self.item_child_setStructuralElementType.clicked.connect(self.item_child_set_structural_element_type_callback)
        self.item_child_setPrescribedDofs.clicked.connect(self.item_child_set_prescribed_dofs_callback)
        self.item_child_setNodalLoads.clicked.connect(self.item_child_set_nodal_loads_callback)
        self.item_child_addMassSpringDamper.clicked.connect(self.item_child_add_mass_spring_damper_callback)
        self.item_child_add_elastic_nodal_links.clicked.connect(self.item_child_add_elastic_nodal_links_callback)
        self.item_child_set_inertial_loads.clicked.connect(self.item_child_set_inertial_loads_callback)
        self.item_child_set_stress_stiffening.clicked.connect(self.item_child_set_stress_stiffening_callback)
        self.item_child_setcappedEnd.clicked.connect(self.item_child_set_capped_end_callback)
        self.item_child_add_valve.clicked.connect(self.item_child_add_valve_callback)
        self.item_child_addFlanges.clicked.connect(self.item_child_add_flanges_callback)
        self.item_child_add_expansion_joint.clicked.connect(self.item_child_add_expansion_joint_callback)
        self.item_child_setBeamXaxisRotation.clicked.connect(self.item_child_set_beam_x_axis_rotation_callback)
        self.item_child_setRotationDecoupling.clicked.connect(self.item_child_set_rotation_decoupling_callback)
        # Acoustic Model Setup
        self.item_child_setAcousticElementType.clicked.connect(self.item_child_set_acoustic_element_type_callback)
        self.item_child_setAcousticPressure.clicked.connect(self.item_child_set_acoustic_pressure_callback)
        self.item_child_setVolumeVelocity.clicked.connect(self.item_child_set_volume_velocity_callback)
        self.item_child_setSpecificImpedance.clicked.connect(self.item_child_set_specific_impedance_callback)
        self.item_child_set_radiation_impedance.clicked.connect(self.item_child_set_radiation_impedance_callback)
        self.item_child_add_perforated_plate.clicked.connect(self.item_child_add_perforated_plate_callback)
        self.item_child_set_acoustic_element_length_correction.clicked.connect(self.item_child_set_acoustic_element_length_correction_callback)
        self.item_child_add_compressor_excitation.clicked.connect(self.item_child_add_compressor_excitation_callback)
        # Analysis Setup
        self.item_child_select_analysis_type.clicked.connect(self.item_child_select_analysis_type_callback)
        self.item_child_analysis_setup.clicked.connect(self.item_child_analisys_setup_callback)
        self.item_child_run_analysis.clicked.connect(self.item_child_run_analysis_callback)

    def update_plot_mesh(self):
        if not self.mainWindow.opv_widget.change_plot_to_mesh:
            self.mainWindow.plot_mesh()

    def update_plot_entities(self):
        if not (self.mainWindow.opv_widget.change_plot_to_entities or self.mainWindow.opv_widget.change_plot_to_entities_with_cross_section):
            self.mainWindow.plot_entities()  

    def update_plot_entities_with_cross_section(self):
        if not self.mainWindow.opv_widget.change_plot_to_entities_with_cross_section:
            self.mainWindow.plot_entities_with_cross_section()   

    # def create_plot_convergence_data(self):
    #     self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)

    # Callbacks
    def item_child_create_geometry_callback(self):
        self.mainWindow.getInputWidget().call_geometry_editor()

    def item_child_edit_geometry_callback(self):
        read = self.mainWindow.getInputWidget().edit_an_imported_geometry()

    # def item_child_set_geometry_file_callback(self):
    #     self.mainWindow.getInputWidget().set_geometry_file()

    def item_child_set_material_callback(self):
        self.update_plot_entities()
        self.mainWindow.getInputWidget().set_material()
        self.mainWindow.plot_entities()

    def item_child_set_fluid_callback(self):
        self.update_plot_entities()
        self.mainWindow.getInputWidget().set_fluid()
        self.mainWindow.plot_entities()

    def item_child_set_cross_section_callback(self):
        if self.mainWindow.getInputWidget().set_cross_section():
            self.mainWindow.plot_entities_with_cross_section()

    def item_child_set_structural_element_type_callback(self):
        self.update_plot_entities()
        self.mainWindow.getInputWidget().setStructuralElementType()

    def item_child_set_prescribed_dofs_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().setDOF()
        self.mainWindow.plot_mesh()

    def item_child_set_nodal_loads_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().setNodalLoads()
        self.mainWindow.plot_mesh()

    def item_child_add_mass_spring_damper_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().addMassSpringDamper()
        self.mainWindow.plot_mesh()

    def item_child_add_elastic_nodal_links_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().add_elastic_nodal_links()
        self.mainWindow.plot_mesh()

    def item_child_set_inertial_loads_callback(self):
        obj = self.mainWindow.getInputWidget().set_inertial_load()
        if obj.complete:
            self.mainWindow.plot_mesh()

    def item_child_set_stress_stiffening_callback(self):
        self.mainWindow.getInputWidget().set_stress_stress_stiffening()
        # self.mainWindow.plot_entities()

    def item_child_set_capped_end_callback(self):
        self.mainWindow.getInputWidget().set_capped_end()
        # self.mainWindow.plot_entities()

    def item_child_add_valve_callback(self):
        read = self.mainWindow.getInputWidget().add_valve()
        if read.complete:
            self.mainWindow.plot_mesh()
        # self.mainWindow.plot_entities_with_cross_section()

    def item_child_add_flanges_callback(self):
        self.mainWindow.getInputWidget().add_flanges()

    def item_child_add_expansion_joint_callback(self):
        self.mainWindow.getInputWidget().add_expansion_joint()
        # self.mainWindow.plot_entities_with_cross_section()

    def item_child_set_beam_x_axis_rotation_callback(self):
        self.update_plot_entities_with_cross_section()
        self.mainWindow.getInputWidget().set_beam_xaxis_rotation()

    def item_child_set_rotation_decoupling_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().setRotationDecoupling()
        self.mainWindow.plot_mesh()

    def item_child_set_acoustic_element_type_callback(self):
        self.update_plot_entities()
        self.mainWindow.getInputWidget().set_acoustic_element_type()
        self.mainWindow.plot_entities()

    def item_child_set_acoustic_pressure_callback(self):
        self.update_plot_mesh()      
        self.mainWindow.getInputWidget().setAcousticPressure()
        self.mainWindow.plot_mesh()

    def item_child_set_volume_velocity_callback(self):
        self.update_plot_mesh()  
        self.mainWindow.getInputWidget().setVolumeVelocity()
        self.mainWindow.plot_mesh()

    def item_child_set_specific_impedance_callback(self):
        self.update_plot_mesh() 
        self.mainWindow.getInputWidget().setSpecificImpedance()
        self.mainWindow.plot_mesh()

    def item_child_set_radiation_impedance_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().set_radiation_impedance()
        self.mainWindow.plot_mesh()

    def item_child_add_perforated_plate_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().add_perforated_plate()
        self.mainWindow.plot_mesh()

    def item_child_set_acoustic_element_length_correction_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().set_acoustic_element_length_correction()
        self.mainWindow.plot_mesh()

    def item_child_add_compressor_excitation_callback(self):
        self.update_plot_mesh()
        self.mainWindow.getInputWidget().add_compressor_excitation()
        self.mainWindow.plot_mesh()

    def item_child_select_analysis_type_callback(self):
        self.mainWindow.getInputWidget().analysisTypeInput()
        self._update_items()
    
    def item_child_analisys_setup_callback(self):
        self.mainWindow.getInputWidget().analysis_setup()
        self._update_items()

    def item_child_run_analysis_callback(self):
        self.mainWindow.getInputWidget().run_analysis()
        self._update_items()
        self.mainWindow.use_results_workspace()

    def enable_actions_according_to_import_type(self):
        import_type = self.project.file.get_import_type()
        if import_type == 0:
            pass
            
    # Items access
    def modify_geometry_item_access(self, bool_key):
        self.item_child_createGeometry.setDisabled(bool_key)

    def modify_general_settings_items_access(self, bool_key):
        self.item_child_createGeometry.setDisabled(bool_key)
        # self.item_child_set_material.setDisabled(bool_key)
        # self.item_child_set_fluid.setDisabled(bool_key)
        # self.item_child_set_crossSection.setDisabled(bool_key)

    def modify_model_setup_items_access(self, bool_key):
        #
        self.item_child_createGeometry.setDisabled(bool_key)
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_set_crossSection.setDisabled(bool_key)
        #
        self.item_child_setStructuralElementType.setDisabled(bool_key) 
        self.item_child_setPrescribedDofs.setDisabled(bool_key)
        self.item_child_setNodalLoads.setDisabled(bool_key)
        self.item_child_addMassSpringDamper.setDisabled(bool_key)
        self.item_child_set_inertial_loads.setDisabled(bool_key)
        self.item_child_add_elastic_nodal_links.setDisabled(bool_key)
        self.item_child_set_stress_stiffening.setDisabled(bool_key)
        self.item_child_setcappedEnd.setDisabled(bool_key)
        self.item_child_add_valve.setDisabled(bool_key) 
        self.item_child_addFlanges.setDisabled(bool_key) 
        self.item_child_add_expansion_joint.setDisabled(bool_key)  
        self.item_child_setBeamXaxisRotation.setDisabled(bool_key)
        self.item_child_setRotationDecoupling.setDisabled(bool_key)
        #   
        self.item_child_setAcousticElementType.setDisabled(bool_key)
        self.item_child_setAcousticPressure.setDisabled(bool_key)
        self.item_child_setVolumeVelocity.setDisabled(bool_key)
        self.item_child_setSpecificImpedance.setDisabled(bool_key)
        self.item_child_set_radiation_impedance.setDisabled(bool_key)
        self.item_child_add_perforated_plate.setDisabled(bool_key)
        self.item_child_set_acoustic_element_length_correction.setDisabled(bool_key)
        self.item_child_add_compressor_excitation.setDisabled(bool_key)
        #
        self.item_child_select_analysis_type.setDisabled(bool_key)

    def _update_items(self):
        """Enables and disables the Child Items on the menu after the solution is done."""
        self.modify_model_setup_items_access(False)

        if True:
            self.item_child_analysis_setup.setDisabled(True)
            self.item_child_run_analysis.setDisabled(True)
            # self.item_top_analysis.setHidden(True)
                    
        if self.project.analysis_ID in [None, 2, 4]:
            self.item_child_analysis_setup.setDisabled(True)
        else:
            self.item_child_analysis_setup.setDisabled(False)
        
        if self.project.analysis_ID is not None and self.project.setup_analysis_complete:
            self.item_child_run_analysis.setDisabled(False)

            # self.update_TreeVisibility_after_solution()
            
    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items on the menu after the solution is done.
        
        """
        self.collapseItem(self.item_top_general_settings)
        self.collapseItem(self.item_top_structural_model_setup)
        self.collapseItem(self.item_top_acoustic_model_setup)

    def update_structural_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(True)
        
    def update_acoustic_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(False)

    def update_coupled_analysis_visibility_items(self):
        self.item_top_structural_model_setup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(False)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' \nbuttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title], opv=self.mainWindow.getOPVWidget())