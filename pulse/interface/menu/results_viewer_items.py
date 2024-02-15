from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect
from pathlib import Path

from pulse.interface.menu.border_item_delegate import BorderItemDelegate
from pulse.interface.menu.common_menu_items import CommonMenuItems
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

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
        self.item_top_resultsViewer_structural = self.add_top_item("Results Viewer - Structural")
        self.item_child_plot_structural_mode_shapes = self.add_item("Plot Structural Mode Shapes")
        self.item_child_plot_displacement_field = self.add_item("Plot Displacement Field")
        self.item_child_plot_structural_frequency_response = self.add_item("Plot Structural Frequency Response")
        self.item_child_plotReactionsFrequencyResponse = self.add_item("Plot Reactions Frequency Response")
        self.item_child_plotStressField = self.add_item("Plot Stress Field")
        self.item_child_plotStressFrequencyResponse = self.add_item("Plot Stress Frequency Response")

        self.item_top_resultsViewer_acoustic = self.add_top_item("Results Viewer - Acoustic")
        self.item_child_plot_acoustic_mode_shapes = self.add_item('Plot Acoustic Mode Shapes')
        self.item_child_plot_acoustic_pressure_field = self.add_item('Plot Acoustic Pressure Field')
        self.item_child_plot_acoustic_frequency_response = self.add_item('Plot Acoustic Frequency Response')
        self.item_child_plot_acoustic_frequency_response_function = self.add_item('Plot Acoustic Frequency Response Function')
        self.item_child_plotAcousticDeltaPressures = self.add_item('Plot Acoustic Delta Pressures')
        self.item_child_plot_TL_NR = self.add_item('Plot Transmission Loss or Attenuation')
        self.item_child_plot_perforated_plate_convergence_data = self.add_item('Plot perforated plate convergence data')
        self.item_child_check_pulsation_criteria = self.add_item('Check Pulsation Criteria')
    
    # # Results Viewer - Structural

    def item_child_plotReactionsFrequencyResponse_callback(self):
        self.update_plot_mesh()
        self.main_window.getInputWidget().plotReactionsFrequencyResponse()

    def item_child_plotStressField_callback(self):
        self.main_window.getInputWidget().plot_stress_field()

    def item_child_plotStressFrequencyResponse_callback(self):
        self.update_plot_mesh()  
        self.main_window.getInputWidget().plotStressFrequencyResponse()

    # Results Viewer - Acoustic
    # def item_child_plot_acoustic_frequency_response_callback(self):
    #     self.update_plot_mesh()
    #     self.main_window.getInputWidget().plot_acoustic_frequency_response()

    # def item_child_plot_acoustic_frequency_response_function_callback(self):
    #     self.update_plot_mesh()
    #     self.main_window.getInputWidget().plot_acoustic_frequency_response_function()

    def plot_acoustic_delta_pressures_callback(self):
        self.update_plot_mesh()
        self.main_window.getInputWidget().plotAcousticDeltaPressures()

    def item_child_plot_TL_NR_callback(self):
        self.update_plot_mesh()
        self.main_window.getInputWidget().plot_TL_NR()

    def item_child_plot_perforated_plate_convergence_data_callback(self):
        self.main_window.getInputWidget().plotPerforatedPlateConvergenceDataLog()
    
    def item_child_check_pulsation_criteria_callback(self):
        self.update_plot_mesh()
        self.main_window.getInputWidget().check_pulsation_criteria()
        self.main_window.plot_mesh()

    # 
    def update_plot_mesh(self):
        if not self.main_window.opv_widget.change_plot_to_mesh:
            self.main_window.plot_mesh()

    def update_plot_entities(self):
        if not (self.main_window.opv_widget.change_plot_to_entities or self.main_window.opv_widget.change_plot_to_entities_with_cross_section):
            self.main_window.plot_entities()  

    def update_plot_entities_with_cross_section(self):
        if not self.main_window.opv_widget.change_plot_to_entities_with_cross_section:
            self.main_window.plot_entities_with_cross_section()   

    # def create_plot_convergence_data(self):
    #     self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)

    def _updateItems(self):
        """Enables and disables the Child Items on the menu after the solution is done."""

        if True:
            # self.item_top_analysis.setHidden(True)
            self.item_top_resultsViewer_structural.setHidden(True)
            self.item_top_resultsViewer_acoustic.setHidden(True)
            self.item_child_plot_structural_mode_shapes.setDisabled(True)
            self.item_child_plot_displacement_field.setDisabled(True)
            self.item_child_plot_structural_frequency_response.setDisabled(True)
            self.item_child_plotStressField.setDisabled(True)
            self.item_child_plotStressFrequencyResponse.setDisabled(True)
            self.item_child_plot_acoustic_mode_shapes.setDisabled(True)
            self.item_child_plot_acoustic_frequency_response.setDisabled(True)
            self.item_child_plot_acoustic_frequency_response_function.setDisabled(True)
            self.item_child_plot_acoustic_pressure_field.setDisabled(True)
            self.item_child_plotAcousticDeltaPressures.setDisabled(True)
            self.item_child_check_pulsation_criteria.setDisabled(True)
            self.item_child_plot_TL_NR.setDisabled(True)
            self.item_child_plot_perforated_plate_convergence_data.setDisabled(True)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(True)
                            
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
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
            
            elif self.project.analysis_ID == 2:
                self.item_child_plot_structural_mode_shapes.setDisabled(False)
                # Deixei esse set_warning aqui só pra lembrar que dá pra fazer
                # Agora que você viu já pode apagar =D
                self.item_child_plot_structural_mode_shapes.set_warning(True)
                if self.project.get_acoustic_solution() is not None:
                    self.item_child_plot_acoustic_mode_shapes.setDisabled(False)    
            
            elif self.project.analysis_ID == 4:
                self.item_child_plot_acoustic_mode_shapes.setDisabled(False)
                if self.project.get_structural_solution() is not None:
                    self.item_child_plot_structural_mode_shapes.setDisabled(False)  
            
            elif self.project.analysis_ID == 3:
                if self.project.perforated_plate_dataLog:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)
                self.item_child_plot_acoustic_frequency_response.setDisabled(False)
                self.item_child_plot_acoustic_frequency_response_function.setDisabled(False)
                self.item_child_plot_acoustic_pressure_field.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID in [5, 6]:
                if self.project.perforated_plate_dataLog:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)

                self.item_child_plot_displacement_field.setDisabled(False)
                self.item_child_plot_structural_frequency_response.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)  

                self.item_child_plot_acoustic_frequency_response.setDisabled(False)
                self.item_child_plot_acoustic_frequency_response_function.setDisabled(False)
                self.item_child_plot_acoustic_pressure_field.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)

                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID == 7:
                self.item_child_plot_displacement_field.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plot_structural_frequency_response.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)

            self.modify_item_names_according_to_analysis()
            # self.update_TreeVisibility_after_solution()
            
    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items ont the menu after the solution is done.
        
        """
        # self.collapseItem(self.item_top_generalSettings)
        # self.collapseItem(self.item_top_structuralModelSetup)
        # self.collapseItem(self.item_top_acousticModelSetup)

        if self.project.analysis_ID in [0, 1, 2, 7]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            # self.expandItem(self.item_top_structuralModelSetup)            
        elif self.project.analysis_ID in [3,4]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_acoustic)
            # self.expandItem(self.item_top_acousticModelSetup)
        elif self.project.analysis_ID in [5, 6]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            self.expandItem(self.item_top_resultsViewer_acoustic)

    def modify_item_names_according_to_analysis(self):
        if self.project.analysis_ID == 7:
            self.item_child_plot_structural_frequency_response.setText(0, 'Plot Nodal Response')
            self.item_child_plotReactionsFrequencyResponse.setText(0, 'Plot Reactions')
            self.item_child_plotStressFrequencyResponse.setText(0, 'Plot Stresses')
        else:
            self.item_child_plot_structural_frequency_response.setText(0, 'Plot Structural Frequency Response')
            self.item_child_plotReactionsFrequencyResponse.setText(0, 'Plot Reactions Frequency Response')
            self.item_child_plotStressFrequencyResponse.setText(0, 'Plot Stress Frequency Response')

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' \nbuttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title], opv=self.main_window.getOPVWidget())
