from PyQt5.QtWidgets import QLabel, QStatusBar

from pulse import app

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)

        self._create_qt_variables()
        self._config_widgets()
        self._config_sizes()

    def _create_qt_variables(self):
        self.points_label = QLabel("Points: \t")
        self.lines_label = QLabel("Lines: \t")
        self.nodes_label = QLabel("Nodes: \t")
        self.acoustic_elements_label = QLabel("Acoustic elements: \t")
        self.structural_elements_label = QLabel("Structural elements: \t")

    def _config_widgets(self):
        self.addWidget(self.points_label)
        self.addWidget(self.lines_label)
        self.addWidget(self.nodes_label)
        self.addWidget(self.acoustic_elements_label)
        self.addWidget(self.structural_elements_label)
        self.reset_labels_visibility()

    def _config_sizes(self):
        self.points_label.setFixedWidth(80)
        self.lines_label.setFixedWidth(80)
        self.nodes_label.setFixedWidth(100)
        self.acoustic_elements_label.setFixedWidth(160)
        self.structural_elements_label.setFixedWidth(160)

    def update_geometry_information(self):
        points, curves = app().project.preprocessor.get_geometry_statistics()
        self.points_label.setText(f"Points: {points}")
        self.lines_label.setText(f"Lines: {curves}")
        self.reset_geometry_info_visibility(key=True)

    def update_mesh_information(self):
        nodes, acoustic_elements, structural_elements = app().project.preprocessor.get_mesh_statistics()
        self.nodes_label.setText(f"Nodes: {nodes}")
        self.acoustic_elements_label.setText(f"Acoustic elements: {acoustic_elements}")
        self.structural_elements_label.setText(f"Structural elements: {structural_elements}")
        self.reset_mesh_info_visibility(key=True)

    def reset_labels_visibility(self):
        self.reset_geometry_info_visibility()
        self.reset_mesh_info_visibility()

    def reset_geometry_info_visibility(self, key=False):
        self.points_label.setVisible(key)
        self.lines_label.setVisible(key)

    def reset_mesh_info_visibility(self, key=False):
        self.nodes_label.setVisible(key)
        self.acoustic_elements_label.setVisible(key)
        self.structural_elements_label.setVisible(key)