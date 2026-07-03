from PySide6.QtWidgets import QFrame, QSizePolicy, QSpacerItem, QWidget

from pulse import app
from pulse.interface.menu.results_viewer_items import ResultsViewerItems
from pulse.interface.ui_generated.menus.left_menu_widget_ui import LeftMenuWidget_UI
from pulse.interface.user_input.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
from pulse.interface.user_input.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget
from pulse.interface.user_input.plots.structural.plot_nodal_results_field_for_harmonic_analysis import PlotNodalResultsFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_stress_field_for_static_analysis import PlotStressesFieldForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_stresses_field_for_harmonic_analysis import PlotStressesFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from pulse.model import AnalysisID


class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self.plot_structural_modal = PlotStructuralModeShape()
        self.plot_structural_harmonic = PlotNodalResultsFieldForHarmonicAnalysis()
        self.plot_acoustic_modal = PlotAcousticModeShape()
        self.plot_acoustic_harmonic = PlotAcousticPressureField()
        self.plot_stresses_harmonic = PlotStressesFieldForHarmonicAnalysis()
        self.plot_stresses_static = PlotStressesFieldForStaticAnalysis()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None

    def _define_qt_variables(self):

        self.main_frame = QFrame()
        self.results_viewer_items = ResultsViewerItems()
        self.layout().replaceWidget(self.top_widget, self.results_viewer_items)
       
        self.results_viewer_items.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.layout().addItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 2, 0
        )
        self.adjustSize()

    def _create_connections(self):
        items = self.results_viewer_items
        
        # structural plot items
        items.item_child_plot_structural_mode_shapes.clicked.connect(self.add_structural_mode_shape_widget)
        items.item_child_plot_displacement_field.clicked.connect(self.add_displacement_field_widget)
        items.item_child_plot_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        items.item_child_plot_reaction_frequency_response.clicked.connect(self.add_reaction_frequency_response_widget)
        items.item_child_plot_stress_field.clicked.connect(self.add_stress_field_widget)
        items.item_child_plot_stress_frequency_response.clicked.connect(self.add_stress_frequency_response_widget)

        # acoustic plot items
        items.item_child_plot_acoustic_mode_shapes.clicked.connect(self.add_acoustic_mode_shape_widget)
        items.item_child_plot_acoustic_pressure_field.clicked.connect(self.add_acoustic_pressure_field_widget)
        items.item_child_plot_acoustic_frequency_response.clicked.connect(self.add_acoustic_frequency_response_widget)
        items.item_child_plot_acoustic_pressure_waveform.clicked.connect(self.add_acoustic_pressure_waveform_widget)
        items.item_child_plot_acoustic_frequency_response_function.clicked.connect(self.add_acoustic_frequency_response_function_widget)
        items.item_child_plot_acoustic_delta_pressures.clicked.connect(self.add_acoustic_delta_pressures_widget)
        items.item_child_plot_transmission_loss.clicked.connect(self.add_transmission_loss_widget)
        items.item_child_plot_perforated_plate_convergence_data.clicked.connect(self.plot_perforated_plate_convergence_data)
        items.item_child_allowable_pulsations_for_reciprocating_compressor.clicked.connect(self.add_allowable_pulsations_for_reciprocating_compressor_widget)
        items.item_child_reciprocating_pump_pulsation_criteria.clicked.connect(self.add_reciprocating_pump_pulsation_criteria_widget)
        items.item_child_reciprocating_pump_inlet_pressure_criteria.clicked.connect(self.add_reciprocating_pump_inlet_pressure_criteria_widget)
        items.item_child_shaking_forces.clicked.connect(self.add_shaking_forces_criteria_widget)

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()

    def add_structural_mode_shape_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        self.top_widget.setFixedHeight(120)
        self.current_widget = self.plot_structural_modal
        self.plot_structural_modal.load_natural_frequencies()
        self.plot_structural_modal.load_user_preference_colormap()
        self.add_widget(self.plot_structural_modal, fill=True)

    def add_displacement_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        self.current_widget = self.plot_structural_harmonic
        self.plot_structural_harmonic.load_frequencies()
        self.plot_structural_harmonic.load_user_preference_colormap()
        self.add_widget(self.plot_structural_harmonic, fill=True)

    def add_structural_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_structural_frequency_response()
        self.add_widget(widget)

    def add_stress_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")

        if AnalysisID(app().project.analysis_id).is_static():
            self.current_widget = self.plot_stresses_static
        else:
            self.current_widget = self.plot_stresses_harmonic

        self.current_widget.load_frequencies()
        self.current_widget.load_user_preference_colormap()
        self.add_widget(self.current_widget, fill=True)

    def add_stress_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_stress_frequency_response()
        self.add_widget(widget)

    def add_reaction_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_reaction_frequency_response()
        self.add_widget(widget, fill=True)

    def add_acoustic_mode_shape_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        self.current_widget = self.plot_acoustic_modal
        self.plot_acoustic_modal.load_natural_frequencies()
        self.plot_acoustic_modal.load_user_preference_colormap()
        self.add_widget(self.plot_acoustic_modal, fill=True)

    def add_acoustic_pressure_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        self.current_widget = self.plot_acoustic_harmonic
        self.plot_acoustic_harmonic.load_frequencies()
        self.plot_acoustic_harmonic.load_user_preference_colormap()
        self.add_widget(self.plot_acoustic_harmonic, fill=True)

    def add_acoustic_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_frequency_response()
        self.add_widget(widget)

    def add_acoustic_pressure_waveform_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_pressure_waveform()
        self.add_widget(widget)

    def add_acoustic_frequency_response_function_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_frequency_response_function()
        self.add_widget(widget)

    def add_acoustic_delta_pressures_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_acoustic_delta_pressures()
        self.add_widget(widget)

    def add_transmission_loss_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_transmission_loss()
        self.add_widget(widget)

    def plot_perforated_plate_convergence_data(self):
        app().project.acoustic_solver.plot_2d.show()

    def add_allowable_pulsations_for_reciprocating_compressor_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.allowable_pulsations_for_reciprocating_compressor()
        self.add_widget(widget)

    def add_reciprocating_pump_pulsation_criteria_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.reciprocating_pump_pulsation_criteria()
        self.add_widget(widget)

    def add_reciprocating_pump_inlet_pressure_criteria_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.reciprocating_pump_inlet_pressure_criteria()
        self.add_widget(widget)

    def add_shaking_forces_criteria_widget(self):
        self.configure_render_according_to_plot_type("lines")
        widget = app().main_window.input_ui.shaking_forces_criteria()
        self.add_widget(widget)

    def add_widget(self, widget: QWidget, fill: bool = False):
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = self.current_widget = widget

        if fill:
            self.layout().setRowStretch(1, 1)
            self.layout().setRowStretch(2, 0)
        else:
            self.layout().setRowStretch(1, 0)
            self.layout().setRowStretch(2, 1)

        self.adjustSize()
        widget.show()

    def configure_render_according_to_plot_type(self, set_by: str):

        geometry_data = app().main_window.action_show_geometry_data.isChecked()
        mesh_data = app().main_window.action_show_mesh_data.isChecked()
        lines = app().main_window.action_plot_lines.isChecked()
        lines_with_cross_sections = app().main_window.action_plot_lines_with_cross_section.isChecked()

        app().main_window.use_base_render_tool = False

        if set_by == "nodes":
            if not (mesh_data or geometry_data):
                # app().main_window.plot_mesh()
                app().main_window.plot_geometry_points()
                app().main_window.view_toolbar.enable_selection_tool()

        elif set_by == "lines":
            if not (lines or lines_with_cross_sections):
                app().main_window.plot_lines_with_cross_sections()
                app().main_window.view_toolbar.enable_selection_tool()

        else:
            app().main_window.plot_results()
            app().main_window.view_toolbar.disable_selection_tool()
            app().main_window.use_base_render_tool = True
        
        app().main_window.results_widget.update_render_tool_according_to_results_viewer_widget(has_selection = set_by in ["nodes", "lines"])
    
    def current_widget_is_animatable(self) -> bool:
        return isinstance(self.current_widget, (
            PlotStructuralModeShape,
            PlotNodalResultsFieldForHarmonicAnalysis,
            PlotStressesFieldForStaticAnalysis,
            PlotStressesFieldForHarmonicAnalysis,
            PlotAcousticPressureField,
            PlotAcousticModeShape,
        ))
    
    def get_animation_widget(self) -> AnimationWidget | None:
        if self.current_widget_is_animatable():
            return self.current_widget.animation_widget

        return None

    def clear_treeWidgets_of_frequencies(self):
        self.plot_structural_modal.treeWidget_frequencies.clear()
        self.plot_structural_harmonic.treeWidget_frequencies.clear()
        self.plot_stresses_harmonic.treeWidget_frequencies.clear()
        self.plot_acoustic_modal.treeWidget_frequencies.clear()
        self.plot_acoustic_harmonic.treeWidget_frequencies.clear()