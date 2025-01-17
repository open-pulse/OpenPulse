from PySide6.QtWidgets import QDialog, QPushButton, QSlider, QSpinBox
from PySide6.QtCore import Qt, Signal

from pulse import app, UI_DIR

from molde import load_ui


class SectionPlaneWidget(QDialog):
    value_changed_2 = Signal()

    value_changed = Signal(float, float, float, float, float, float)
    slider_released = Signal(float, float, float, float, float, float)
    slider_pressed = Signal(float, float, float, float, float, float)
    closed = Signal()

    def __init__(self):
        super().__init__()

        ui_path = UI_DIR / "render/section_plane_inputs.ui"
        load_ui(ui_path, self)

        self.editing = False
        self.cutting = False
        self.invert_value = False
        self.keep_section_plane = False

        self._config_window()
        self._define_qt_variables()
        self._create_connections()

    def _config_window(self):

        self.setWindowFlags(
            Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )

        self.setGeometry(200, 200, 400, 350)
        self.setModal(1)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Section Plane")

    def _define_qt_variables(self):
        # QPushButton
        self.pushButton_apply: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_invert: QPushButton
        self.pushButton_reset: QPushButton

        # QSlider
        self.relative_plane_position_x_slider: QSlider
        self.relative_plane_position_y_slider: QSlider
        self.relative_plane_position_z_slider: QSlider

        self.plane_rotation_x_slider: QSlider
        self.plane_rotation_y_slider: QSlider
        self.plane_rotation_z_slider: QSlider

        # QSpinBox
        self.relative_plane_position_x_spinbox: QSpinBox
        self.relative_plane_position_y_spinbox: QSpinBox
        self.relative_plane_position_z_spinbox: QSpinBox

        self.plane_rotation_x_spinbox: QSpinBox
        self.plane_rotation_y_spinbox: QSpinBox
        self.plane_rotation_z_spinbox: QSpinBox

    def _create_connections(self):
        for slider in self._sliders():
            slider.valueChanged.connect(self.value_change_callback)
            slider.sliderReleased.connect(self.slider_release_callback)
            slider.sliderPressed.connect(self.slider_pressed_callback)

        self.pushButton_apply.clicked.connect(self.apply_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_reset.clicked.connect(self.reset_button_callback)
        self.pushButton_invert.clicked.connect(self.invert_button_callback)

    def show(self):
        super().show()
        self.cutting = True
        self.keep_section_plane = False
        self.value_changed_2.emit()

    def closeEvent(self, event):
        if not self.keep_section_plane:
            app().main_window.action_section_plane.blockSignals(True)
            app().main_window.action_section_plane.setChecked(False)
            app().main_window.action_section_plane.blockSignals(False)
            self.cutting = False
        else:
            self.cutting = True
        self.value_changed_2.emit()
        # self.closed.emit()

    def get_position(self):
        Px = self.relative_plane_position_x_slider.value()
        Py = self.relative_plane_position_y_slider.value()
        Pz = self.relative_plane_position_z_slider.value()
        return Px, Py, Pz

    def get_rotation(self):
        Rx = self.plane_rotation_x_slider.value()
        Ry = self.plane_rotation_y_slider.value()
        Rz = self.plane_rotation_z_slider.value()
        return Rx, Ry, Rz

    def get_inverted(self):
        return self.invert_value

    def value_change_callback(self):
        self.value_changed_2.emit()

    def slider_pressed_callback(self):
        self.editing = True
        self.cutting = True
        self.value_changed_2.emit()

    def slider_release_callback(self):
        self.editing = False
        self.cutting = True
        self.value_changed_2.emit()

    def reset_button_callback(self):
        self.relative_plane_position_x_slider.setValue(50),
        self.relative_plane_position_y_slider.setValue(50),
        self.relative_plane_position_z_slider.setValue(50),
        self.plane_rotation_x_slider.setValue(0),
        self.plane_rotation_y_slider.setValue(90),
        self.plane_rotation_z_slider.setValue(0),

        self.invert_value = False
        self.value_changed_2.emit()

    def invert_button_callback(self):
        self.invert_value = not self.invert_value
        self.value_changed_2.emit()

    def apply_callback(self):
        self.keep_section_plane = True
        self.close()

    def _sliders(self):
        return (
            self.relative_plane_position_x_slider,
            self.relative_plane_position_y_slider,
            self.relative_plane_position_z_slider,
            self.plane_rotation_x_slider,
            self.plane_rotation_y_slider,
            self.plane_rotation_z_slider,
        )

    def _spinboxes(self):
        return (
            self.relative_plane_position_x_spinbox,
            self.relative_plane_position_y_spinbox,
            self.relative_plane_position_z_spinbox,
            self.plane_rotation_x_spinbox,
            self.plane_rotation_y_spinbox,
            self.plane_rotation_z_spinbox,
        )
