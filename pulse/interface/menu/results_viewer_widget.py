from PySide6.QtWidgets import QFrame, QWidget

from pulse import app
from pulse.interface.ui_generated.menus.left_menu_widget_ui import LeftMenuWidget_UI
from pulse.interface.menu.results_viewer_items import ResultsViewerItems

class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None

    def _define_qt_variables(self):

        self.main_frame = QFrame()
        self.results_viewer_items = ResultsViewerItems()
        self.layout().replaceWidget(self.top_widget, self.results_viewer_items)
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
        widget = app().main_window.input_ui.plot_structural_mode_shapes()
        self.add_widget(widget, animation_widget=True)

    def add_displacement_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_displacement_field()
        self.add_widget(widget, animation_widget=True)

    def add_structural_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_structural_frequency_response()
        self.add_widget(widget)

    def add_stress_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_stress_field()
        self.add_widget(widget, animation_widget=True)

    def add_stress_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_stress_frequency_response()
        self.add_widget(widget)

    def add_reaction_frequency_response_widget(self):
        self.configure_render_according_to_plot_type("nodes")
        widget = app().main_window.input_ui.plot_reaction_frequency_response()
        self.add_widget(widget)

    def add_acoustic_mode_shape_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_acoustic_mode_shapes()
        self.add_widget(widget, animation_widget=True)

    def add_acoustic_pressure_field_widget(self):
        self.configure_render_according_to_plot_type("tubes")
        widget = app().main_window.input_ui.plot_acoustic_pressure_field()
        self.add_widget(widget, animation_widget=True)

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

    def add_widget(self, widget: QWidget, animation_widget=False):

        app().main_window.animation_toolbar.setEnabled(False)

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        app().main_window.animation_toolbar.setEnabled(animation_widget)
        self.adjustSize()

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
                app().main_window.render_tools_toolbar.enable_selection_tool()

        elif set_by == "lines":
            if not (lines or lines_with_cross_sections):
                app().main_window.plot_lines_with_cross_sections()
                app().main_window.render_tools_toolbar.enable_selection_tool()

        else:
            app().main_window.plot_results()
            app().main_window.render_tools_toolbar.disable_selection_tool()
            app().main_window.use_base_render_tool = True
        
        app().main_window.results_widget.update_render_tool_according_to_results_viewer_widget(has_selection = set_by in ["nodes", "lines"])

