from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect
from pathlib import Path

from pulse.interface.menu.border_item_delegate import BorderItemDelegate
from pulse.interface.menu.common_menu_items import CommonMenuItems
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse import app

class ResultsViewerItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.main_window = app().main_window
        self.project = self.main_window.getProject()

        self.setObjectName("results_viewer_items")
        self._create_items()

    def _create_items(self):
        # Structural results items
        self.item_top_resultsViewer_structural = self.add_top_item("Results Viewer - Structural")
        self.item_child_plot_structural_mode_shapes = self.add_item("Plot structural mode shapes")
        self.item_child_plot_displacement_field = self.add_item("Plot displacement field")
        self.item_child_plot_structural_frequency_response = self.add_item("Plot structural frequency response")
        self.item_child_plot_reaction_frequency_response = self.add_item("Plot reactions frequency response")
        self.item_child_plot_stress_field = self.add_item("Plot stress field")
        self.item_child_plot_stress_frequency_response = self.add_item("Plot stress frequency response")
        # Acoustic results items
        self.item_top_resultsViewer_acoustic = self.add_top_item("Results Viewer - Acoustic")
        self.item_child_plot_acoustic_mode_shapes = self.add_item("Plot acoustic mode shapes")
        self.item_child_plot_acoustic_pressure_field = self.add_item("Plot acoustic pressure field")
        self.item_child_plot_acoustic_frequency_response = self.add_item("Plot acoustic frequency response")
        self.item_child_plot_acoustic_frequency_response_function = self.add_item("Plot acoustic frequency response function")
        self.item_child_plot_acoustic_delta_pressures = self.add_item("Plot acoustic delta pressures")
        self.item_child_plot_transmission_loss = self.add_item("Plot transmission loss")
        self.item_child_plot_perforated_plate_convergence_data = self.add_item("Plot perforated plate convergence data")
        self.item_child_check_pulsation_criteria = self.add_item("Check pulsation criteria")
    
    def update_plot_mesh(self):
        if not self.main_window.opv_widget.change_plot_to_mesh:
            self.main_window.plot_mesh()

    def update_plot_entities(self):
        if not (self.main_window.opv_widget.change_plot_to_entities or self.main_window.opv_widget.change_plot_to_entities_with_cross_section):
            self.main_window.plot_entities()  

    def update_plot_entities_with_cross_section(self):
        if not self.main_window.opv_widget.change_plot_to_entities_with_cross_section:
            self.main_window.plot_entities_with_cross_section()

    def _update_items(self):
        """Enables and disables the Child Items on the menu after the solution is done."""

        self.item_top_resultsViewer_structural.setHidden(True)
        self.item_top_resultsViewer_acoustic.setHidden(True)
        self.item_child_plot_structural_mode_shapes.setDisabled(True)
        self.item_child_plot_displacement_field.setDisabled(True)
        self.item_child_plot_structural_frequency_response.setDisabled(True)
        self.item_child_plot_reaction_frequency_response.setDisabled(True)
        self.item_child_plot_stress_field.setDisabled(True)
        self.item_child_plot_stress_frequency_response.setDisabled(True)
        self.item_child_plot_acoustic_mode_shapes.setDisabled(True)
        self.item_child_plot_acoustic_frequency_response.setDisabled(True)
        self.item_child_plot_acoustic_frequency_response_function.setDisabled(True)
        self.item_child_plot_acoustic_pressure_field.setDisabled(True)
        self.item_child_plot_acoustic_delta_pressures.setDisabled(True)
        self.item_child_check_pulsation_criteria.setDisabled(True)
        self.item_child_plot_transmission_loss.setDisabled(True)
        self.item_child_plot_perforated_plate_convergence_data.setDisabled(True)
        self.item_child_plot_perforated_plate_convergence_data.setHidden(True)
                            
        if self.project.get_structural_solution() is not None or self.project.get_acoustic_solution() is not None:

            if self.project.analysis_ID in [0, 1, 2, 7]:
                self.item_top_resultsViewer_structural.setHidden(False)
            
            elif self.project.analysis_ID in [3, 4]:
                self.item_top_resultsViewer_acoustic.setHidden(False)
            
            elif self.project.analysis_ID in [5, 6]:    
                self.item_top_resultsViewer_acoustic.setHidden(False)
                self.item_top_resultsViewer_structural.setHidden(False)

            if self.project.analysis_ID in [0, 1]:
                self.item_child_plot_structural_frequency_response.setDisabled(False)
                self.item_child_plot_displacement_field.setDisabled(False)
                self.item_child_plot_reaction_frequency_response.setDisabled(False)
                self.item_child_plot_stress_field.setDisabled(False)
                self.item_child_plot_stress_frequency_response.setDisabled(False)
            
            elif self.project.analysis_ID == 2:
                self.item_child_plot_structural_mode_shapes.setDisabled(False)
                # self.item_child_plot_structural_mode_shapes.set_warning(True)
                if self.project.get_acoustic_solution() is not None:
                    self.item_child_plot_acoustic_mode_shapes.setDisabled(False)    
            
            elif self.project.analysis_ID == 4:
                self.item_child_plot_acoustic_mode_shapes.setDisabled(False)
                if self.project.get_structural_solution() is not None:
                    self.item_child_plot_structural_mode_shapes.setDisabled(False)  
            
            elif self.project.analysis_ID == 3:

                if self.project.perforated_plate_data_log:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)
                    self.item_child_plot_perforated_plate_convergence_data.setHidden(False)

                self.item_child_plot_acoustic_frequency_response.setDisabled(False)
                self.item_child_plot_acoustic_frequency_response_function.setDisabled(False)
                self.item_child_plot_acoustic_pressure_field.setDisabled(False)
                self.item_child_plot_acoustic_delta_pressures.setDisabled(False)
                self.item_child_plot_transmission_loss.setDisabled(False)
                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID in [5, 6]:

                if self.project.perforated_plate_data_log:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)
                    self.item_child_plot_perforated_plate_convergence_data.setHidden(False)

                self.item_child_plot_displacement_field.setDisabled(False)
                self.item_child_plot_structural_frequency_response.setDisabled(False)
                self.item_child_plot_stress_field.setDisabled(False)
                self.item_child_plot_stress_frequency_response.setDisabled(False)
                self.item_child_plot_reaction_frequency_response.setDisabled(False)  

                self.item_child_plot_acoustic_frequency_response.setDisabled(False)
                self.item_child_plot_acoustic_frequency_response_function.setDisabled(False)
                self.item_child_plot_acoustic_pressure_field.setDisabled(False)
                self.item_child_plot_acoustic_delta_pressures.setDisabled(False)
                self.item_child_plot_transmission_loss.setDisabled(False)

                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID == 7:
                self.item_child_plot_displacement_field.setDisabled(False)
                self.item_child_plot_stress_field.setDisabled(False)
                self.item_child_plot_structural_frequency_response.setDisabled(False)
                self.item_child_plot_reaction_frequency_response.setDisabled(False)
                self.item_child_plot_stress_frequency_response.setDisabled(False)

            self.modify_item_names_according_to_analysis()
            # self.update_TreeVisibility_after_solution()
            
    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items ont the menu after the solution is done.
        
        """

        if self.project.analysis_ID in [0, 1, 2, 7]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)            
        
        elif self.project.analysis_ID in [3, 4]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_acoustic)
        
        elif self.project.analysis_ID in [5, 6]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            self.expandItem(self.item_top_resultsViewer_acoustic)

    def modify_item_names_according_to_analysis(self):
        if self.project.analysis_ID == 7:
            self.item_child_plot_structural_frequency_response.setText(0, "Plot nodal response")
            self.item_child_plot_reaction_frequency_response.setText(0, "Plot reactions")
            self.item_child_plot_stress_frequency_response.setText(0, "Plot stresses")
        else:
            self.item_child_plot_structural_frequency_response.setText(0, "Plot structural frequency response")
            self.item_child_plot_reaction_frequency_response.setText(0, "Plot reactions frequency response")
            self.item_child_plot_stress_frequency_response.setText(0, "Plot stress frequency response")

    def empty_project_action_message(self):
        window_title = 'Error'
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' \nbuttons to continue."
        PrintMessageInput([window_title, title, message])
