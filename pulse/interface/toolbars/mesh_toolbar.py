from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QToolBar, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QKeyEvent, QFont

from pulse import app
from pulse.interface.toolbars.mesh_updater import MeshUpdater
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.utils.interface_utils import check_inputs

class MeshToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        
        self.main_window = app().main_window
        self.project = app().main_window.project
        self.mesh_updater = MeshUpdater()

        self._define_qt_variables()
        self._config_widgets()
        self._create_connections()

        self._configure_layout()

        self._configure_appearance()
        self.update_mesh_attributes()

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowTitle("Mesh toolbar")

    def _define_qt_variables(self):

        # QLabel
        self.label_element_size = QLabel("Element size [m]:")
        self.label_geometry_tolerance = QLabel("Geometry tolerance [m]:")
        # self.label_element_size.setFont(font)
        # self.label_geometry_tolerance.setFont(font)

        # QLineEdit
        self.lineEdit_element_size = QLineEdit()
        self.lineEdit_geometry_tolerance = QLineEdit()
        self.lineEdit_element_size.setText("0.01")
        self.lineEdit_geometry_tolerance.setText("1e-6")
        # self.lineEdit_element_size.setFont(font)
        # self.lineEdit_geometry_tolerance.setFont(font)

        # QPushButton
        self.pushButton_generate_mesh = QPushButton(" Generate mesh ")
        # self.pushButton_generate_mesh.setFont(font)

        # for w_type in [QPushButton, QLabel, QLineEdit]:
        #     for widget in self.findChildren(w_type):
        #         widget.setFont(font)

    def _config_widgets(self):

        self.label_element_size.setAlignment(Qt.AlignRight)
        self.label_geometry_tolerance.setAlignment(Qt.AlignRight)
        self.label_element_size.setAlignment(Qt.AlignVCenter)
        self.label_geometry_tolerance.setAlignment(Qt.AlignVCenter)

        self.lineEdit_element_size.setAlignment(Qt.AlignCenter)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)
        self.lineEdit_element_size.setFixedSize(70, 28)
        self.lineEdit_geometry_tolerance.setFixedSize(70, 28)

        self.pushButton_generate_mesh.setToolTip("Press to generate the mesh")
        self.pushButton_generate_mesh.setCursor(Qt.PointingHandCursor)
        self.pushButton_generate_mesh.setDisabled(True)
        self.pushButton_generate_mesh.setFixedSize(120, 30)

    def _create_connections(self):
        #
        self.lineEdit_element_size.textEdited.connect(self.change_button_visibility)
        self.lineEdit_geometry_tolerance.textEdited.connect(self.change_button_visibility)
        #
        self.pushButton_generate_mesh.clicked.connect(self.generate_mesh_callback)

    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addWidget(self.label_element_size)
        self.addWidget(self.lineEdit_element_size)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_geometry_tolerance)
        self.addWidget(self.lineEdit_geometry_tolerance)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_generate_mesh)
        #
        self.adjustSize()

    def _configure_appearance(self):
        self.setMinimumHeight(40)
        self.setMovable(True)
        self.setFloatable(True)

        font = QFont()
        font.setPointSize(10)

        for widget in self.findChildren((QPushButton, QLabel, QLineEdit)):
            widget.setFont(font)

    def change_button_visibility(self):

        self.pushButton_generate_mesh.setDisabled(True)
        current_element_size, current_geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

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

        element_size, geometry_tolerance = self.mesh_updater.get_mesh_attributes_from_project_file()

        if element_size is not None:
            self.lineEdit_element_size.setText(str(element_size))

        if geometry_tolerance is not None:
            self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))

        self.change_button_visibility()

    # def keyPressEvent(self, event: QKeyEvent | None) -> None:
    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         self.mesh_updater.process_mesh_and_load_project()
    #     return super().keyPressEvent(event)