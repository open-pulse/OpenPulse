from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QAction, QDoubleSpinBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QToolBar

from pulse.interface.toolbars.mesh_updater import MeshUpdater
from pulse.interface.utils import check_inputs

from pulse import app

class MeshToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        
        self.main_window = app().main_window
        self.project = app().main_window.project
        self.mesh_updater = MeshUpdater()

        self._define_qt_variables()
        self._configure_widgets()
        self._create_connections()

        self._configure_layout()

        self._configure_appearance()
        self.update_mesh_attributes()

    def _define_qt_variables(self):

        # QLabel
        self.label_element_size = QLabel(" Element size [m]:")
        self.label_geometry_tolerance = QLabel(" Geometry tolerance [m]:")

        # QLineEdit
        self.lineEdit_element_size = QLineEdit()
        self.lineEdit_geometry_tolerance = QLineEdit()
        self.lineEdit_element_size.setText("0.01")
        self.lineEdit_geometry_tolerance.setText("1e-6")

        # QPushButton
        self.pushButton_generate_mesh = QPushButton(" Generate mesh ")

    def _configure_widgets(self):

        # self.label_element_size.setFixedWidth(80)
        # self.label_geometry_tolerance.setFixedWidth(120)

        self.label_element_size.setAlignment(Qt.AlignRight)
        self.label_geometry_tolerance.setAlignment(Qt.AlignRight)
        self.label_element_size.setAlignment(Qt.AlignVCenter)
        self.label_geometry_tolerance.setAlignment(Qt.AlignVCenter)

        self.lineEdit_element_size.setAlignment(Qt.AlignCenter)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)
        self.lineEdit_element_size.setFixedWidth(60)
        self.lineEdit_geometry_tolerance.setFixedWidth(60)

        self.lineEdit_element_size.setStyleSheet("""QLineEdit{ color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }
                                                    QLineEdit:disabled{ color: rgb(100, 100, 100); background-color: rgb(240, 240, 240) }
                                                 """)

        self.lineEdit_geometry_tolerance.setStyleSheet("""QLineEdit{ color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }
                                                          QLineEdit:disabled{ color: rgb(100, 100, 100); background-color: rgb(240, 240, 240) }
                                                       """)
        
        self.pushButton_generate_mesh.setStyleSheet(""" QPushButton{border-radius: 4px; border-color: rgb(255, 50, 50); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}
                                                        QPushButton:hover{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}
                                                        QPushButton:pressed{border-radius: 4px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255)}
                                                        QPushButton:disabled{border-radius: 4px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(150,150, 150); background-color: rgba(220, 220, 220, 50)}
                                                    """)

        self.pushButton_generate_mesh.setToolTip("Press to generate the mesh")
        self.pushButton_generate_mesh.setCursor(Qt.PointingHandCursor)
        self.pushButton_generate_mesh.setDisabled(True)

    def _create_connections(self):
        #
        self.lineEdit_element_size.textEdited.connect(self.change_button_visibility)
        self.lineEdit_geometry_tolerance.textEdited.connect(self.change_button_visibility)
        #
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)

    def _configure_layout(self):
        #
        self.addWidget(self.label_element_size)
        self.addWidget(self.lineEdit_element_size)
        self.addWidget(self.label_geometry_tolerance)
        self.addWidget(self.lineEdit_geometry_tolerance)
        self.addSeparator()
        self.addWidget(self.pushButton_generate_mesh)
        #
        self.layout().setContentsMargins(0,0,6,0)
        self.layout().setSpacing(4)
        self.adjustSize()

    def _configure_appearance(self):
        self.setMinimumHeight(32)
        self.setMovable(True)
        self.setFloatable(True)

    def change_button_visibility(self):

        self.pushButton_generate_mesh.setDisabled(True)
        current_element_size, current_geometry_tolerance = self.project.file.get_mesh_attributes_from_project_file()

        try:
            _element_size = float(self.lineEdit_element_size.text())
            _geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except:
            return
        
        if bool(_element_size) and bool(_geometry_tolerance):

            if _element_size != current_element_size:
                self.pushButton_generate_mesh.setDisabled(False)
                return

            if _geometry_tolerance != current_geometry_tolerance:
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
            self.change_button_visibility()
        except:
            pass