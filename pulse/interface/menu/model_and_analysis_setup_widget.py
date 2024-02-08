from PyQt5.QtWidgets import QFrame, QGridLayout, QTreeWidget, QTreeWidgetItem, QWidget

from pulse.interface.menu.model_and_analysis_setup_items import ModelAndAnalysisSetupItems
from pulse.interface.menu.results_viewer_items import ResultsViewerItems

class ModelAndAnalysisSetupWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self._define_qt_variables()
        self._config_widget()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.model_and_analysis_setup_items = ModelAndAnalysisSetupItems(self.main_window)

    def _config_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.model_and_analysis_setup_items, 0, 0)
        self.setLayout(self.grid_layout)
        self.adjustSize()

    def update_visibility_for_acoustic_analysis(self):
        print("update_acoustic_analysis_visibility_items")
        self.model_and_analysis_setup_items.update_acoustic_analysis_visibility_items()

    def update_visibility_for_structural_analysis(self):
        print("update_structural_analysis_visibility_items")
        self.model_and_analysis_setup_items.update_structural_analysis_visibility_items()
    
    def update_visibility_for_coupled_analysis(self):
        self.model_and_analysis_setup_items.update_coupled_analysis_visibility_items()