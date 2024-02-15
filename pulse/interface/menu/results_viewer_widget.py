from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic

from pathlib import Path

from pulse.interface.menu.results_viewer_items import ResultsViewerItems
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget

class ResultsViewerWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.reset()
        self._define_qt_variables()
        self._create_connections()
        self._config_widget()

    def reset(self):
        self.current_widget = None

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.animation_widget = AnimationWidget(self.main_window)
        self.results_viewer_items = ResultsViewerItems(self.main_window)

    def _create_connections(self):
        self.results_viewer_items.item_child_plotStructuralModeShapes.clicked.connect(
            self.add_structural_mode_shape_widget)

        self.results_viewer_items.item_child_plotDisplacementField.clicked.connect(
            self.add_displacement_field_widget)

        self.results_viewer_items.item_child_plotAcousticModeShapes.clicked.connect(
            self.add_acoustic_mode_shape_widget)

        self.results_viewer_items.item_child_plotAcousticPressureField.clicked.connect(
            self.add_acoustic_pressure_field_widget)

    def _config_widget(self):
        self.grid_layout = QGridLayout()

        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.results_viewer_items, 0, 0)
        self.grid_layout.addWidget(self.animation_widget, 2, 0)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid_layout)
        self.adjustSize()
        self.animation_widget.setVisible(False)

    def udate_visibility_items(self):
        self.results_viewer_items._updateItems()
        self.results_viewer_items.update_TreeVisibility_after_solution()

    def add_structural_mode_shape_widget(self):
        widget = self.main_window.input_widget.plot_structural_mode_shapes()
        self.add_widget(widget)

    def add_displacement_field_widget(self):
        widget = self.main_window.input_widget.plot_displacement_field()
        self.add_widget(widget)
        
    def add_acoustic_mode_shape_widget(self):
        widget = self.main_window.input_widget.plot_acoustic_mode_shapes()
        self.add_widget(widget)

    def add_acoustic_pressure_field_widget(self):
        widget = self.main_window.input_widget.plot_acoustic_pressure_field()
        self.add_widget(widget)

    def add_widget(self, widget):
        self.remove_widget()
        self.current_widget = widget
        if self.current_widget is None:
            return
        if self.grid_layout.indexOf(self.current_widget) == -1:
            self.grid_layout.addWidget(self.current_widget, 1, 0)
        self.animation_widget.setVisible(True)

    def remove_widget(self):
        if self.grid_layout.indexOf(self.current_widget) != -1:
            self.grid_layout.removeWidget(self.current_widget)
