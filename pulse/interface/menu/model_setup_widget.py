from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget
from pulse.interface.menu.model_setup_items import ModelSetupItems

class ModelSetupWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._define_qt_variables()
        self._config_widget()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.model_setup_items = ModelSetupItems()

    def _config_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.main_frame.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.model_setup_items, 0, 0)
        self.setLayout(self.grid_layout)
        self.adjustSize()