from PyQt5.QtWidgets import QFileDialog, QPushButton, QSlider, QSpinBox, QWidget
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"


class AnimationWidget(QWidget):
    def __init__(self):
        super().__init__()

        ui_path = UI_DIR / "plots/animation/animation_widget.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window
        self.main_window = main_window

        self._define_qt_variables()
        self._create_connections()

    def _define_qt_variables(self):
        # QPushButton
        self.pushButton_animate : QPushButton
        self.pushButton_export : QPushButton
        # QSlider
        self.phase_slider : QSlider
        # QSpinBox
        self.spinBox_frames : QSpinBox
        self.spinBox_cycles : QSpinBox

    def _create_connections(self):
        self.phase_slider.valueChanged.connect(self.slider_callback)
        self.pushButton_animate.clicked.connect(self.process_animation)
        self.pushButton_export.clicked.connect(self.export_animation_to_file)
        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)

    def frames_value_changed(self):
        # self.main_window.opv_widget.opvAnalysisRenderer._numberFramesHasChanged(True)
        self.frames = self.spinBox_frames.value()
        
    def cycles_value_changed(self):
        self.cycles = self.spinBox_cycles.value()

    def slider_callback(self):
        value = self.phase_slider.value()
        # self.main_window.opv_widget.opvAnalysisRenderer.slider_callback(value)
        self.main_window.results_widget.slider_callback(value)

    def process_animation(self):
        self.update_animation_settings()
        # self.main_window.opv_widget.opvAnalysisRenderer._setNumberFrames(self.frames)
        # self.main_window.opv_widget.opvAnalysisRenderer._setNumberCycles(self.cycles)
        # self.main_window.opv_widget.opvAnalysisRenderer.playAnimation()
        # self.main_window.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()
        self.main_window.results_widget.start_animation()

    def update_animation_settings(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()

    def export_animation_to_file(self):
        file_path, check = QFileDialog.getSaveFileName(
                                                        self,
                                                        "Save As",
                                                        filter = "All Files ();; Video (*.mp4);; GIF (*.gif);;",
                                                    )
        
        if not check:
            return
        
        try:
            self.process_animation()
            self.main_window.results_widget.generate_video(file_path)
            self.main_window.results_widget.stop_animation()
            
        except Exception as error_log:
            title = "Error while exporting animation"
            message = "An error has occured while exporting the animation file.\n"
            message += str(error_log)
            PrintMessageInput([window_title_1, title, message])

        
        
    