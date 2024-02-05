
from PyQt5.QtWidgets import QFrame, QGridLayout, QTreeWidget, QTreeWidgetItem, QWidget

from pulse.interface.menu.model_and_analysis_setup_items import ModelAndAnalysisSetupItems
from pulse.interface.menu.results_viewer_items import ResultsViewerItems

class MenuItemsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self._define_qt_variables()
        self._config_widget()
        self.show()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.treeWidget_model_setup = QTreeWidget()
        self.treeWidget_model_and_analysis_setup = ModelAndAnalysisSetupItems(self.main_window)
        self.treeWidget_results_viewer = ResultsViewerItems(self.main_window)

    def _config_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.treeWidget_model_and_analysis_setup, 0, 0)
        self.grid_layout.addWidget(self.treeWidget_results_viewer, 1, 0)
        self.setLayout(self.grid_layout)
        self.adjustSize()