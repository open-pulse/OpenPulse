from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QProxyStyle, QSlider, QDialog
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *


class ClipPlaneWidget(QDialog):

    value_changed = pyqtSignal(float, float, float, float, float, float)
    slider_released = pyqtSignal(float, float, float, float, float, float)
    slider_pressed = pyqtSignal(float, float, float, float, float, float)
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        ui_path = UI_DIR / "render/cutting_plane_inputs.ui"
        uic.loadUi(ui_path, self)

        self.opv = app().main_window.opv_widget

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        # self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):

        self.setWindowFlags(
                            Qt.Window
                            | Qt.CustomizeWindowHint
                            | Qt.WindowTitleHint
                            | Qt.WindowStaysOnTopHint
                            | Qt.WindowCloseButtonHint
                            | Qt.FramelessWindowHint
                            | Qt.WindowShadeButtonHint
                        )

        self.setGeometry(200, 200, 400, 350)        
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Clip Plane")

    def _define_qt_variables(self):

        # QLabel
        self.label_delta_x_value : QLabel
        self.label_delta_y_value : QLabel
        self.label_delta_z_value : QLabel
        self.label_rotation_x_value : QLabel
        self.label_rotation_y_value : QLabel
        self.label_rotation_z_value : QLabel

        # QSlider
        self.slider_delta_x : QSlider
        self.slider_delta_y : QSlider
        self.slider_delta_z : QSlider
        self.slider_rotation_about_x_axis : QSlider
        self.slider_rotation_about_y_axis : QSlider
        self.slider_rotation_about_z_axis : QSlider

    def _create_connections(self):

        self.slider_delta_x.valueChanged.connect(self.value_change_callback)
        self.slider_delta_x.sliderReleased.connect(self.slider_release_callback)
        self.slider_delta_x.sliderPressed.connect(self.slider_pressed_callback)
        
        self.slider_delta_y.valueChanged.connect(self.value_change_callback)
        self.slider_delta_y.sliderReleased.connect(self.slider_release_callback)
        self.slider_delta_y.sliderPressed.connect(self.slider_pressed_callback)
        
        self.slider_delta_z.valueChanged.connect(self.value_change_callback)
        self.slider_delta_z.sliderReleased.connect(self.slider_release_callback)
        self.slider_delta_z.sliderPressed.connect(self.slider_pressed_callback)

        self.slider_rotation_about_x_axis.valueChanged.connect(self.value_change_callback)
        self.slider_rotation_about_x_axis.sliderReleased.connect(self.slider_release_callback)
        self.slider_rotation_about_x_axis.sliderPressed.connect(self.slider_pressed_callback)

        self.slider_rotation_about_y_axis.valueChanged.connect(self.value_change_callback)
        self.slider_rotation_about_y_axis.sliderReleased.connect(self.slider_release_callback)
        self.slider_rotation_about_y_axis.sliderPressed.connect(self.slider_pressed_callback)
        
        self.slider_rotation_about_z_axis.valueChanged.connect(self.value_change_callback)
        self.slider_rotation_about_z_axis.sliderReleased.connect(self.slider_release_callback)
        self.slider_rotation_about_z_axis.sliderPressed.connect(self.slider_pressed_callback)

    def get_position(self):
        Px = self.slider_delta_x.value()
        Py = self.slider_delta_y.value()
        Pz = self.slider_delta_z.value()
        return Px, Py, Pz

    def get_rotation(self):
        Rx = self.slider_rotation_about_x_axis.value()
        Ry = self.slider_rotation_about_y_axis.value() 
        Rz = self.slider_rotation_about_z_axis.value()
        return Rx, Ry, Rz

    def value_change_callback(self):
        self.setUpdatesEnabled(False)

        Px, Py, Pz = self.get_position()
        self.label_delta_x_value.setText(f"{Px} %")
        self.label_delta_y_value.setText(f"{Py} %")
        self.label_delta_z_value.setText(f"{Pz} %")

        Rx, Ry, Rz = self.get_rotation()
        self.label_rotation_x_value.setText(f"{Rx} °")
        self.label_rotation_y_value.setText(f"{Ry} °")
        self.label_rotation_z_value.setText(f"{Rz} °")

        self.setUpdatesEnabled(True)
        self.value_changed.emit(*self.get_position(), *self.get_rotation())

    def slider_release_callback(self):
        self.slider_released.emit(*self.get_position(), *self.get_rotation())

    def slider_pressed_callback(self):
        self.slider_pressed.emit(*self.get_position(), *self.get_rotation())

    def closeEvent(self, event):
        self.closed.emit()