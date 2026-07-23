import numpy as np
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from pulse import DARK_ICON_COLOR, ICON_DIR, LIGHT_ICON_COLOR, app
from pulse.interface import error_title
from pulse.interface.formatters import icons
from pulse.interface.ui_generated.plots.animation.animation_widget_ui import AnimationWidget_UI
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput


class AnimationWidget(AnimationWidget_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_icons()
        self._config_widgets()
        self._create_connections()

    def _load_icons(self):
        self.play_icon = QIcon(str(ICON_DIR / "common/play.png"))
        self.pause_icon = QIcon(str(ICON_DIR / "common/pause.png"))
        self.export_icon = QIcon(str(ICON_DIR / "common/save_as.png"))

    def _config_widgets(self):
        self.pushButton_animate.setIcon(self.play_icon)
        self.pushButton_animate.setIconSize(QSize(20, 20))
        self.pushButton_animate.setCursor(Qt.PointingHandCursor)
        self.pushButton_animate.setCheckable(True)
        self.pushButton_export.setIcon(self.export_icon)
        self.pushButton_export.setIconSize(QSize(20, 20))
        self.pushButton_export.setCursor(Qt.PointingHandCursor)
        self.spinBox_frames.setValue(app().project.frames)
        self.spinBox_cycles.setValue(app().project.cycles)

        # QSlider
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)
        self.phase_slider.setCursor(Qt.PointingHandCursor)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)
        self.magnification_factor_slider.setCursor(Qt.PointingHandCursor)
        self.magnification_factor_slider.setMinimum(0)
        self.magnification_factor_slider.setMaximum(64)
        self.magnification_factor_slider.setValue(16)
        self.magnification_factor_slider.setSingleStep(1)

        self._configure_icons()
        self.update_phase_slider_steps()

    def _create_connections(self):
        # self.phase_slider.sliderPressed.connect(self.pause_animation)
        self.phase_slider.valueChanged.connect(self.phase_slider_callback)
        self.magnification_factor_slider.valueChanged.connect(self.magnification_factor_slider_callback)

        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export.clicked.connect(self.export_animation_to_file)
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)
        app().main_window.theme_changed.connect(self._configure_icons)

    def _configure_icons(self, *args):

        icon_color = None
        theme = app().config.user_preferences.interface_theme
        if theme == "dark":
            icon_color = DARK_ICON_COLOR.to_qt()
        else:
            icon_color = LIGHT_ICON_COLOR.to_qt()

        icons.change_icon_color_for_widgets(self.findChildren(QPushButton), icon_color)

    @property
    def phase_in_radians(self):
        return np.radians(self.phase_slider.value())

    @property
    def magnification_factor(self):
        return self.magnification_factor_slider.value() / 16

    @property
    def frames(self): return self.spinBox_frames.value()

    @property
    def cycles(self): return self.spinBox_cycles.value()

    def set_magnification_slider_enabled(self, enabled: bool):
        self.magnification_factor_slider.setEnabled(enabled)
        self.label_magnification_factor.setEnabled(enabled)
        self.label_factor.setEnabled(enabled)

    def set_magnification_slider_visible(self, visible: bool):
        self.magnification_factor_slider.setVisible(visible)
        self.label_magnification_factor.setVisible(visible)
        self.label_factor.setVisible(visible)

    def reset_sliders(self):
        # block the slider signal to avoid multiple render updates
        self.phase_slider.blockSignals(True)

        # reset the phase slider value
        self.phase_slider.setValue(0)

        # update labels
        self.update_degree_label()

        # unblocking the slider signals
        self.phase_slider.blockSignals(False)

    def frames_value_changed(self):
        self.update_phase_slider_steps()
        app().project.frames = self.frames
        app().main_window.results_widget.clear_cache()

    def cycles_value_changed(self):
        app().project.cycles = self.cycles
        app().main_window.results_widget.clear_cache()

    def phase_slider_callback(self):
        self.update_degree_label()
        self.pause_animation()
        app().main_window.results_widget.slider_callback(self.phase_slider.value())

    def magnification_factor_slider_callback(self, value: int):
        self.update_factor_label()
        self.pause_animation()
        app().main_window.results_widget.slider_callback(self.phase_slider.value())
        app().main_window.results_widget.clear_cache()

    def pause_animation(self):
        if self.pushButton_animate.isChecked():
            self.pushButton_animate.blockSignals(True)
            self.pushButton_animate.setChecked(False)
            self.update_animate_button_icons(False)
            app().main_window.results_widget.stop_animation()
            self.pushButton_animate.blockSignals(False)

    def process_animation(self, state: bool):
        self.update_animate_button_icons(state)
        if state:
            app().main_window.results_widget.start_animation(frames=self.frames, cycles=self.cycles)
        else:
            app().main_window.results_widget.stop_animation()

    def update_animate_button_icons(self, state: bool):
        self.pushButton_animate.setIcon(self.pause_icon if state else self.play_icon)
        self._configure_icons()

    def update_degree_label(self):
        value = self.phase_slider.value()
        self.label_phase_angle.setText(f"{value}°")

    def update_factor_label(self, max_value=None):
        value = self.magnification_factor_slider.value() / 16
        if isinstance(max_value, float | int):
            if max_value:
                value /= (10 * max_value)
            else:
                value = 1
        self.label_factor.setText(f"{value : .2e}x")

    def update_phase_slider_steps(self):
        frames = self.spinBox_frames.value()
        single_step = int(360 / frames)
        self.phase_slider.setSingleStep(single_step)

    def export_animation_to_file(self):
        file_path = FileDialogService.save_file(["mp4", "webp", "gif"], "Save As")
        if file_path is None:
            return
        try:
            results = app().main_window.results_widget
            if file_path.suffix.lower() in [".gif", ".webp"]:
                LoadingWindow(results.save_animation).run(file_path)
            else:
                LoadingWindow(results.save_video).run(file_path)
        except Exception as error_log:
            PrintMessageInput([error_title, "Error while exporting animation",
                               "An error has occured while exporting the animation file.\n" + str(error_log)])