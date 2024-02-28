from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QAction, QDoubleSpinBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QToolBar

from pulse.interface.utils import check_inputs
from pulse.interface.toolbars.mesh_updater import MeshUpdater

class MeshToolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.main_window = parent
        self.project = parent.project
        self.mesh_updater = MeshUpdater(parent)

        self.define_qt_variables()
        self.create_connections()
        self.configure_layout()
        self.configure_appearance()
        self.update_mesh_attributes()

    def define_qt_variables(self):

        self.label_element_size = QLabel(" Element size [m]:")
        self.label_geometry_tolerance = QLabel(" Geometry tolerance [m]:")
        self.lineEdit_element_size = QLineEdit()
        self.lineEdit_geometry_tolerance = QLineEdit()
        self.pushButton_generate_mesh = QPushButton(" Generate mesh ")

        # self.label_element_size.setFixedWidth(80)
        # self.label_geometry_tolerance.setFixedWidth(120)
        self.lineEdit_element_size.setFixedWidth(60)
        self.lineEdit_geometry_tolerance.setFixedWidth(60)
        self.lineEdit_element_size.setText("0.01")
        self.lineEdit_geometry_tolerance.setText("1e-6")

        self.label_element_size.setAlignment(Qt.AlignRight)
        self.label_geometry_tolerance.setAlignment(Qt.AlignRight)
        self.label_element_size.setAlignment(Qt.AlignVCenter)
        self.label_geometry_tolerance.setAlignment(Qt.AlignVCenter)
        self.lineEdit_element_size.setAlignment(Qt.AlignCenter)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)

        self.lineEdit_element_size.setStyleSheet("background-color: rgb(255,255,255)")
        self.lineEdit_geometry_tolerance.setStyleSheet("background-color: rgb(255,255,255)")

    def configure_appearance(self):
        self.setMinimumHeight(32)
        self.setMovable(True)
        self.setFloatable(True)

    def create_connections(self):
        # generate_mesh_icon = QIcon(str(Path("data/icons/mesh.png")))
        # self.generate_mesh_action = QAction(generate_mesh_icon, "Mesh", self)
        # self.generate_mesh_action.setToolTip("Press to generate the mesh")
        # self.generate_mesh_action.triggered.connect(self.generate_mesh_callback)
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)
        self.lineEdit_element_size.editingFinished.connect(self.change_button_visibility)
        self.lineEdit_geometry_tolerance.editingFinished.connect(self.change_button_visibility)
        self.change_button_visibility()

    def configure_layout(self):
        #
        self.addWidget(self.label_element_size)
        self.addWidget(self.lineEdit_element_size)
        self.addWidget(self.label_geometry_tolerance)
        self.addWidget(self.lineEdit_geometry_tolerance)
        self.addSeparator()
        self.addWidget(self.pushButton_generate_mesh)
        # self.addAction(self.generate_mesh_action)
        #
        self.layout().setContentsMargins(0,0,6,0)
        self.layout().setSpacing(4)
        self.adjustSize()

    def change_button_visibility(self):
        self.pushButton_generate_mesh.setDisabled(True)
        current_element_size, current_geometry_tolerance = self.project.file.get_mesh_attributes_from_project_file()
        if self.check_input_values():
            return
        if current_element_size is not None:
            if self.element_size != current_element_size:
                self.pushButton_generate_mesh.setDisabled(False)
                return
        if current_geometry_tolerance is not None:
            if self.geometry_tolerance != current_geometry_tolerance:
                self.pushButton_generate_mesh.setDisabled(False)
                return

    def generate_mesh_callback(self):
        if self.check_input_values():
            return
        self.mesh_updater.set_project_attributes(self.element_size, self.geometry_tolerance)
        self.mesh_updater.process_mesh_and_load_project()
        self.change_button_visibility()

    def check_input_values(self):

        self.element_size = check_inputs(self.lineEdit_element_size, "'Element size'")
        if self.element_size is None:
            self.lineEdit_element_size.setFocus()
            return True
        
        self.geometry_tolerance = check_inputs(self.lineEdit_geometry_tolerance, "'Geometry tolerance'")
        if self.geometry_tolerance is None:
            self.lineEdit_geometry_tolerance.setFocus()
            return True
        
    def update_mesh_attributes(self):
        try:
            element_size, geometry_tolerance = self.project.file.get_mesh_attributes_from_project_file()
            if element_size is not None:
                self.lineEdit_element_size.setText(str(element_size))
            if geometry_tolerance is not None:
                self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
        except:
            pass