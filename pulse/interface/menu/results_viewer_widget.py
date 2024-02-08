from PyQt5 import uic
from pathlib import Path

from PyQt5.QtWidgets import QFrame, QGridLayout, QTreeWidget, QTreeWidgetItem, QWidget

from pulse.interface.menu.model_and_analysis_setup_items import ModelAndAnalysisSetupItems
from pulse.interface.menu.results_viewer_items import ResultsViewerItems
from pulse.interface.user_input.plot.animation_widget import AnimationWidget
from pulse.interface.user_input.plot.structural.structural_mode_shape_widget import PlotStructuralModeShapeInput

class ResultsViewerWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self._define_qt_variables()
        self._config_widget()
        self._load_results_widgets()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.animation_widget = AnimationWidget(self.main_window)
        self.results_viewer_items = ResultsViewerItems(self.main_window)
        self.results_viewer_items.setObjectName("results_viewer_items")

    def _config_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.results_viewer_items, 0, 0)
        self.grid_layout.addWidget(self.animation_widget, 2, 0)
        self.setLayout(self.grid_layout)
        self.adjustSize()
        self.results_items = self.findChild(QTreeWidget, "results_viewer_items")
        self.results_items.itemClicked.connect(self.on_click_item)

    def udate_visibility_items(self):
        self.results_viewer_items._updateItems()
        self.results_viewer_items.update_TreeVisibility_after_solution()

    def _load_results_widgets(self):
        self.structural_mode_shape_widget = PlotStructuralModeShapeInput(self.main_window)

    def add_structural_mode_shape_widget(self):
        self.project = self.main_window.getProject()
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        
        if solution is None:
            return
       
        if self.project.analysis_ID in [2, 4]:
            
            if self.grid_layout.indexOf(self.structural_mode_shape_widget) == -1:
                self.grid_layout.addWidget(self.structural_mode_shape_widget, 1, 0)
            self.structural_mode_shape_widget.load_natural_frequencies()

    def on_click_item(self, item, column):

        if item == self.results_items.item_child_plotStructuralModeShapes:
            if not self.results_items.item_child_plotStructuralModeShapes.isDisabled():
                self.add_structural_mode_shape_widget()
                # self.main_window.getInputWidget().plotStructuralModeShapes()
