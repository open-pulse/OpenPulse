from os.path import isfile
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox

class GenerateWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._create_widgets()
        self._add_widget_to_layout()

    def _create_widgets(self):
        self.min_size_label = QLabel("Min Size")
        self.min_size_box = QLineEdit('1')
        self.max_size_label = QLabel("Max Size")
        self.max_size_box = QLineEdit('1')
        self.mesh_button = QPushButton('Mesh')
        self.mesh_button.clicked.connect(self._mesh_function)

    def _mesh_function(self):
        min_size = self.min_size_box.text()
        max_size = self.max_size_box.text()
        error = self.main_window.mesh.generate(min_size, max_size)

        if error == FileNotFoundError:
            QMessageBox.critical(
                self, 
                "ERROR",
                "Please select a valid file"
            )

    def _add_widget_to_layout(self):
        self.layout = QFormLayout()
        self.layout.addRow(self.min_size_label, self.max_size_label)
        self.layout.addRow(self.min_size_box, self.max_size_box)
        self.layout.addRow(self.mesh_button)
        self.setLayout(self.layout)
