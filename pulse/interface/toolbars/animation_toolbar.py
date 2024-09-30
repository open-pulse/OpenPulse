from PyQt5.QtWidgets import QLabel, QFileDialog, QPushButton, QSlider, QSpinBox, QToolBar, QWidget
from PyQt5.QtCore import QSize, Qt 
from PyQt5.QtGui import  QIcon

from pulse import app, UI_DIR, ICON_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class AnimationToolbar(QToolBar):
    def __init__(self):
        super().__init__()

        self._initialize()
        self._load_icons()
        self._define_qt_variables()
        self._config_widgets()
        self._create_connections()
        self._configure_layout()
        self._configure_appearance()

    def _initialize(self):
        self.animating = False

    def _load_icons(self):
        self.play_icon = QIcon(str(ICON_DIR / "common/play.png"))
        self.pause_icon = QIcon(str(ICON_DIR / "common/pause.png"))
        self.export_icon = QIcon(str(ICON_DIR / "common/save_as.png"))

    def _define_qt_variables(self):

        # QLabel
        self.label_cycles = QLabel("Animation cycles:")
        self.label_frames = QLabel("Frames per cycle:")
        self.label_phase = QLabel("Animation phase:")

        # QPushButton
        self.pushButton_animate = QPushButton(self)
        self.pushButton_export = QPushButton(self)

        # QSlider
        self.phase_slider = QSlider(self)

        # QSpinBox
        self.spinBox_frames = QSpinBox(self)
        self.spinBox_cycles = QSpinBox(self)

    def _config_widgets(self):

        # QPushButton
        self.pushButton_animate.setFixedHeight(28)
        self.pushButton_animate.setFixedWidth(40)
        self.pushButton_animate.setIcon(self.play_icon)
        self.pushButton_animate.setIconSize(QSize(20,20))
        self.pushButton_animate.setCursor(Qt.PointingHandCursor)
        self.pushButton_animate.setToolTip("Play/Pause the animation")
        self.pushButton_animate.setCheckable(True)

        self.pushButton_export.setFixedHeight(28)
        self.pushButton_export.setFixedWidth(40)
        self.pushButton_export.setIcon(self.export_icon)
        self.pushButton_export.setIconSize(QSize(20,20))
        self.pushButton_export.setCursor(Qt.PointingHandCursor)
        self.pushButton_export.setToolTip("Export the animation")

        # QSlider
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)
        self.phase_slider.setMaximumWidth(300)
        self.phase_slider.setCursor(Qt.PointingHandCursor)
        self.phase_slider.setMinimum(0)
        self.phase_slider.setMaximum(360)

        # QSpinBox
        self.spinBox_cycles.setMinimum(1)
        self.spinBox_cycles.setMaximum(10)
        self.spinBox_cycles.setSingleStep(1)
        self.spinBox_cycles.setValue(app().project.cycles)
        self.spinBox_cycles.setMinimumWidth(60)
        self.spinBox_cycles.setAlignment(Qt.AlignHCenter)
        self.spinBox_cycles.setCursor(Qt.PointingHandCursor)

        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(app().project.frames)
        self.spinBox_frames.setMinimumWidth(60)
        self.spinBox_frames.setAlignment(Qt.AlignHCenter)
        self.spinBox_frames.setCursor(Qt.PointingHandCursor)

    def _create_connections(self):
        #
        self.phase_slider.valueChanged.connect(self.slider_callback)
        #
        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export.clicked.connect(self.export_animation_to_file)
        #
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)
        #
        self.update_phase_slider_steps()

    def get_spacer(self):
        spacer = QWidget()
        spacer.setFixedWidth(8)
        return spacer

    def _configure_layout(self):
        #
        self.addWidget(self.label_frames)
        self.addWidget(self.spinBox_frames)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_cycles)
        self.addWidget(self.spinBox_cycles)
        self.addWidget(self.get_spacer())
        #
        self.addWidget(self.label_phase)
        self.addWidget(self.phase_slider)
        self.addWidget(self.get_spacer())
        #
        self.addSeparator()
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_animate)
        self.addWidget(self.get_spacer())
        self.addWidget(self.pushButton_export)
        #
        self.adjustSize()

    def _configure_appearance(self):
        self.setMinimumHeight(32)
        self.setMovable(True)
        self.setFloatable(True)

    def frames_value_changed(self):
        self.frames = self.spinBox_frames.value()
        self.update_phase_slider_steps()
        app().project.frames = self.frames
        app().main_window.results_widget.clear_cache()

    def cycles_value_changed(self):
        self.cycles = self.spinBox_cycles.value()
        app().project.cycles = self.cycles
        app().main_window.results_widget.clear_cache()

    def slider_callback(self):
        self.pause_animation()      
        value = self.phase_slider.value()
        app().main_window.results_widget.slider_callback(value)

    def update_phase_slider_steps(self):
        frames = self.spinBox_frames.value()
        single_step = int(360 / frames)
        self.phase_slider.setSingleStep(single_step)

    def pause_animation(self):
        if self.pushButton_animate.isChecked(): 
            self.pushButton_animate.blockSignals(True)
            self.pushButton_animate.setChecked(False)
            self.update_animate_button_icons(False)
            app().main_window.results_widget.stop_animation()
            self.pushButton_animate.blockSignals(False)

    def process_animation(self, state: bool):

        self.update_animation_settings()
        self.update_animate_button_icons(state)

        if state:
            app().main_window.results_widget.start_animation(frames=self.frames, cycles=self.cycles)
        else:
            app().main_window.results_widget.stop_animation()

    def update_animate_button_icons(self, state: bool):
        if state:
            self.pushButton_animate.setIcon(self.pause_icon)
        else:
            self.pushButton_animate.setIcon(self.play_icon)

        widgets = self.findChildren((QPushButton))
        icons.change_icon_color_for_widgets(widgets, app().main_window.icon_color)

    def update_animation_settings(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()

    def export_animation_to_file(self):
        file_path, extension = QFileDialog.getSaveFileName(
            self, "Save As",
            filter = "Video (*.mp4);;WEBP (*.webp);;GIF (*.gif);; All Files ();;",
        )

        if not extension:
            return

        # Add default suffix if it does not have one
        file_path = Path(file_path)
        if extension == "Video (*.mp4)":
            suffix = ".mp4"
        elif extension == "WEBP (*.webp)":
            suffix = ".webp"
        elif extension == "GIF (*.gif)":
            suffix = ".gif"
        else:
            suffix = ".mp4"

        if not file_path.suffix:
            file_path = file_path.parent / (file_path.name + suffix)

        try:

            if file_path.suffix.lower() in [".gif", ".webp"]:
                LoadingWindow(app().main_window.results_widget.save_animation).run(file_path)
            else:
                LoadingWindow(app().main_window.results_widget.save_video).run(file_path)

        except Exception as error_log:
            title = "Error while exporting animation"
            message = "An error has occured while exporting the animation file.\n"
            message += str(error_log)
            PrintMessageInput([window_title_1, title, message])
