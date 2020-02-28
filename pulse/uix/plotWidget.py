from os.path import isfile
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QCheckBox

class PlotWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._create_widgets()
        self._add_widget_to_layout()

    def _create_widgets(self):
        self.plot_button = QPushButton('Plot')
        self.wireframe = QCheckBox('Wireframe')
        self.deformation = QCheckBox('Deformation')
        self.animate = QCheckBox('Animate')
        self.plot_button.clicked.connect(self._plot_function)

    def _add_widget_to_layout(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.layout.addRow(self.wireframe)
        self.layout.addRow(self.deformation)
        self.layout.addRow(self.animate)
        self.layout.addRow(self.plot_button)

    def _plot_function(self):
        self.main_window.draw()