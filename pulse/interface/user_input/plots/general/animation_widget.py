from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from pulse import ICON_DIR, app
from pulse.interface import error_title
from pulse.interface.formatters import icons
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.ui_generated.plots.animation.animation_widget_ui import AnimationWidget_UI


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
        self._configure_icons()
        self.update_phase_slider_steps()

    def _create_connections(self):
        self.phase_slider.valueChanged.connect(self.slider_callback)
        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export.clicked.connect(self.export_animation_to_file)
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)
        app().main_window.theme_changed.connect(self._configure_icons)

    def _configure_icons(self, *args):
        icons.change_icon_color_for_widgets(self.findChildren(QPushButton), app().main_window.icon_color)

    @property
    def frames(self): return self.spinBox_frames.value()
    @property
    def cycles(self): return self.spinBox_cycles.value()

    def reset_sliders(self):
        self.phase_slider.blockSignals(True)
        self.phase_slider.setValue(0)
        self.phase_slider.blockSignals(False)

    def update_phase_slider_steps(self):
        self.phase_slider.setSingleStep(int(360 / self.frames))

    def frames_value_changed(self):
        self.update_phase_slider_steps()
        app().project.frames = self.frames
        app().main_window.results_widget.clear_cache()

    def cycles_value_changed(self):
        app().project.cycles = self.cycles
        app().main_window.results_widget.clear_cache()

    def slider_callback(self):
        self.pause_animation()
        app().main_window.results_widget.slider_callback(self.phase_slider.value())

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