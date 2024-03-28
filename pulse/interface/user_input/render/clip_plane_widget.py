from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QGridLayout, QLabel, QProxyStyle, QSlider, QDialog
from pathlib import Path
from pulse.interface.formatters.icons import get_openpulse_icon


class ClipPlaneWidget(QDialog):
    value_changed = pyqtSignal(float, float, float, float, float, float)
    slider_released = pyqtSignal(float, float, float, float, float, float)
    slider_pressed = pyqtSignal(float, float, float, float, float, float)
    closed = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.configure_window()
        self._load_icons()
        self.create_sliders()
        # self.exec()

    def configure_window(self):
        self.setWindowTitle("Clip Plane")
        self.setGeometry(200, 200, 400, 350)
        
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )
        self.setWindowModality(Qt.WindowModal)

    def _load_icons(self):
        self.icon = get_openpulse_icon()
        self.setWindowIcon(self.icon)

    def create_sliders(self):
        #
        self.x_angle_title_label = QLabel("Rx")
        self.y_angle_title_label = QLabel("Ry")
        self.z_angle_title_label = QLabel("Rz")
        self.x_pos_tittle_label = QLabel("Px")
        self.y_pos_tittle_label = QLabel("Py")
        self.z_pos_tittle_label = QLabel("Pz")
        self.position_tittle_label = QLabel("Position")
        self.rotation_tittle_label = QLabel("Rotation")
        self.position_tittle_label.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.rotation_tittle_label.setFont(QFont("Helvetica", 12, QFont.Bold))

        self.v_angle_value_label = QLabel("0 °")
        self.h_angle_value_label = QLabel("0 °")
        self.position_value_label = QLabel("0 °")
        self.x_pos_tittle_value_label = QLabel("0 %")
        self.y_pos_tittle_value_label = QLabel("0 %")
        self.z_pos_tittle_value_label = QLabel("0 %")

        #
        self.y_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_angle_slider.setMaximum(360)
        self.y_angle_slider.setMinimum(0)
        self.y_angle_slider.valueChanged.connect(self.value_change_callback)
        self.y_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.y_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.x_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.x_angle_slider.setMaximum(360)
        self.x_angle_slider.setMinimum(0)
        self.x_angle_slider.valueChanged.connect(self.value_change_callback)
        self.x_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.x_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.z_angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_angle_slider.setMaximum(360)
        self.z_angle_slider.setMinimum(0)
        self.z_angle_slider.valueChanged.connect(self.value_change_callback)
        self.z_angle_slider.sliderReleased.connect(self.slider_release_callback)
        self.z_angle_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.x_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.x_pos_slider.setMaximum(100)
        self.x_pos_slider.setMinimum(0)
        self.x_pos_slider.setValue(50)
        self.x_pos_slider.valueChanged.connect(self.value_change_callback)
        self.x_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.x_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.y_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_pos_slider.setMaximum(100)
        self.y_pos_slider.setMinimum(0)
        self.y_pos_slider.setValue(50)
        self.y_pos_slider.valueChanged.connect(self.value_change_callback)
        self.y_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.y_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.z_pos_slider = QSlider(Qt.Orientation.Horizontal)
        self.z_pos_slider.setMaximum(100)
        self.z_pos_slider.setMinimum(0)
        self.z_pos_slider.setValue(50)
        self.z_pos_slider.valueChanged.connect(self.value_change_callback)
        self.z_pos_slider.sliderReleased.connect(self.slider_release_callback)
        self.z_pos_slider.sliderPressed.connect(self.slider_pressed_callback)

        self.v_angle_value_label.setFixedWidth(50)
        self.h_angle_value_label.setFixedWidth(50)
        self.position_value_label.setFixedWidth(50)
        self.x_pos_tittle_value_label.setFixedWidth(50)
        self.y_pos_tittle_value_label.setFixedWidth(50)
        self.z_pos_tittle_value_label.setFixedWidth(50)

        #
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.rotation_tittle_label, 4, 1)
        grid_layout.addWidget(self.y_angle_title_label, 6, 0)
        grid_layout.addWidget(self.y_angle_slider, 6, 1)
        grid_layout.addWidget(self.v_angle_value_label, 6, 2)

        grid_layout.addWidget(self.x_angle_title_label, 5, 0)
        grid_layout.addWidget(self.x_angle_slider, 5, 1)
        grid_layout.addWidget(self.h_angle_value_label, 5, 2)

        grid_layout.addWidget(self.z_angle_title_label, 7, 0)
        grid_layout.addWidget(self.z_angle_slider, 7, 1)
        grid_layout.addWidget(self.position_value_label, 7, 2)

        grid_layout.addWidget(self.position_tittle_label, 0, 1)
        grid_layout.addWidget(self.x_pos_tittle_label, 1, 0)
        grid_layout.addWidget(self.x_pos_slider, 1, 1)
        grid_layout.addWidget(self.x_pos_tittle_value_label, 1, 2)

        grid_layout.addWidget(self.y_pos_tittle_label, 2, 0)
        grid_layout.addWidget(self.y_pos_slider, 2, 1)
        grid_layout.addWidget(self.y_pos_tittle_value_label, 2, 2)

        grid_layout.addWidget(self.z_pos_tittle_label, 3, 0)
        grid_layout.addWidget(self.z_pos_slider, 3, 1)
        grid_layout.addWidget(self.z_pos_tittle_value_label, 3, 2)

        self.position_tittle_label.setAlignment(Qt.AlignCenter)
        self.rotation_tittle_label.setAlignment(Qt.AlignCenter)

        self.setLayout(grid_layout)
        self.setGeometry(1450, 150, 450, 200)

    def get_position(self):
        Px = self.x_pos_slider.value()
        Py = self.y_pos_slider.value()
        Pz = self.z_pos_slider.value()
        return Px, Py, Pz

    def get_rotation(self):
        Rx = self.y_angle_slider.value()
        Ry = self.x_angle_slider.value()
        Rz = self.z_angle_slider.value()
        return Rx, Ry, Rz

    def value_change_callback(self):
        self.setUpdatesEnabled(False)
        self.v_angle_value_label.setText(f"{self.y_angle_slider.value()} °")
        self.h_angle_value_label.setText(f"{self.x_angle_slider.value()} °")
        self.position_value_label.setText(f"{self.z_angle_slider.value()} °")
        self.x_pos_tittle_value_label.setText(f"{self.x_pos_slider.value()} %")
        self.y_pos_tittle_value_label.setText(f"{self.y_pos_slider.value()} %")
        self.z_pos_tittle_value_label.setText(f"{self.z_pos_slider.value()} %")
        self.setUpdatesEnabled(True)
        self.value_changed.emit(*self.get_position(), *self.get_rotation())

    def slider_release_callback(self):
        self.slider_released.emit(*self.get_position(), *self.get_rotation())

    def slider_pressed_callback(self):
        self.slider_pressed.emit(*self.get_position(), *self.get_rotation())

    def closeEvent(self, event):
        self.closed.emit()