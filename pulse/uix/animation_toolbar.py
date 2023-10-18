from pathlib import Path
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QFont
from PyQt5.QtWidgets import QAction, QToolBar, QLabel, QSpinBox

class AnimationToolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        self.create_actions()
        self._create_frames_control()
        self._create_cycles_control()
        self.configure_layout()
        self.configure_appearance()

    def configure_appearance(self):
        # self.setContentsMargins(4,4,4,4)
        self.setMovable(True)
        self.setFloatable(True)

    def create_actions(self):
        self.playpause_icon = QIcon(str(Path("data/icons/play_pause.png")))
        self.play_pause_animaton_action = QAction(self.playpause_icon, '&Play/Pause Animation', self)
        self.play_pause_animaton_action.setStatusTip('Play/Pause Animation')
        self.play_pause_animaton_action.setShortcut('Space')
        self.play_pause_animaton_action.triggered.connect(self.toggle_button_callback)

    def _create_frames_control(self):
        self.spinBox_frames = QSpinBox(self)
        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(60)
        self.spinBox_frames.setValue(40)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setMinimumWidth(40)
        self.spinBox_frames.setMinimumHeight(30)
        self.spinBox_frames.setAlignment(Qt.AlignCenter)
        # self.spinBox_frames.setContentsMargins(6,0,6,0)
        self.spinBox_frames.valueChanged.connect(self.update_frames)
        self.spinBox_frames.setToolTip("Controls the animation frames per cycle.")

    def _create_cycles_control(self):
        self.spinBox_cycles = QSpinBox(self)
        self.spinBox_cycles.setMinimum(3)
        self.spinBox_cycles.setMaximum(10)
        self.spinBox_cycles.setSingleStep(1)
        self.spinBox_cycles.setMinimumWidth(40)
        self.spinBox_cycles.setMinimumHeight(30)
        self.spinBox_cycles.setAlignment(Qt.AlignCenter)
        # self.spinBox_cycles.setContentsMargins(6,0,6,0)
        self.spinBox_cycles.setToolTip("Controls the animation number of cycles.")

    def configure_layout(self):
        label_font = self._getFont(10, bold=True, italic=False)#, family_type="Arial")
        # radioButton_font = self._getFont(9, bold=True, italic=True, family_type="Arial")
        self.label_animation_controls = QLabel(' Animation controls:  ', self)
        self.label_animation_controls.setFont(label_font)

        self.addWidget(self.label_animation_controls)
        self.addSeparator()
        self.addWidget(self.spinBox_frames)
        self.addWidget(self.spinBox_cycles)
        self.addSeparator()
        self.addAction(self.play_pause_animaton_action)
        self.addSeparator()

    def update_frames(self):
        self.main_window.opv_widget.opvAnalysisRenderer._numberFramesHasChanged(True)

    def toggle_button_callback(self):
        frames = self.spinBox_frames.value()
        cycles = self.spinBox_cycles.value()
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberFrames(frames)
        self.main_window.opv_widget.opvAnalysisRenderer._setNumberCycles(cycles)
        self.main_window.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()

    def _getFont(self, fontSize, bold=False, italic=False, family_type="Arial"):
        font = QFont()
        font.setFamily(family_type)
        font.setPointSize(fontSize)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(75)  
        return font