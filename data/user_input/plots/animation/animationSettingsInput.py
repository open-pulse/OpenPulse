from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox, QSpinBox, QPushButton, QWidget, QFileDialog, QComboBox
import os
from os.path import basename
from data.user_input.project.printMessageInput import PrintMessageInput
from pulse.utils import get_new_path
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
import numpy as np

from PyQt5 import uic

class AnimationSettingsInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Animation/animationSettingsInput.ui', self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        icons_path = 'data\\icons\\'
        self.icon_pulse = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon_pulse)

        self.icon_animate = QIcon(icons_path + 'play_pause.png')

        self.project = project
        self.opv = opv
        self.opv.setInputObject(self)

        self.save_path = ""
        self.export_file_path = ""
        self.userPath = os.path.expanduser('~')

        self.lineEdit_FileName = self.findChild(QLineEdit, 'lineEdit_FileName')
        self.checkBox_export = self.findChild(QCheckBox, 'checkBox_export')
        
        self.label_export_path = self.findChild(QLabel, 'label_export_path')
        
        self.spinBox_frames = self.findChild(QSpinBox, 'spinBox_frames')
        self.spinBox_cycles = self.findChild(QSpinBox, 'spinBox_cycles')

        self.spinBox_frames.valueChanged.connect(self.frames_value_changed)
        self.spinBox_cycles.valueChanged.connect(self.cycles_value_changed)
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()

        self.pushButton_animate = self.findChild(QPushButton, 'pushButton_animate')
        # self.pushButton_animate.setIcon(self.icon_animate)
        self.pushButton_animate.clicked.connect(self.process_animation)

        self.pushButton_ChooseFolderExport = self.findChild(QPushButton, 'pushButton_ChooseFolderExport')
        self.pushButton_ChooseFolderExport.clicked.connect(self.choose_path_export_animation)

        self.pushButton_clean = self.findChild(QPushButton, 'pushButton_clean')
        self.pushButton_clean.setVisible(False)
        # self.pushButton_clean.clicked.connect(self.reset_input_field)

        self.pushButton_export_animation = self.findChild(QPushButton, 'pushButton_export_animation')
        self.pushButton_export_animation.clicked.connect(self.export_animation_to_file)

        self.comboBox_file_format = self.findChild(QComboBox, 'comboBox_file_format')

        self.tabWidget_animation = self.findChild(QTabWidget, 'tabWidget_animation')
        self.tab_main = self.tabWidget_animation.findChild(QWidget, 'tab_main')
        self.tab_export = self.tabWidget_animation.findChild(QWidget, 'tab_export')

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.process_animation()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def reset_input_field(self):
        self.lineEdit_FileName.setText("")

    def frames_value_changed(self):
        self.opv.opvAnalysisRenderer._numberFramesHasChanged(True)
        self.frames = self.spinBox_frames.value()
        
    def cycles_value_changed(self):
        self.cycles = self.spinBox_cycles.value()

    def choose_path_export_animation(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.label_export_path.setText(str(self.save_path))

    def get_file_format(self):
        index = self.comboBox_file_format.currentIndex()
        _formats = [".avi", ".mp4", ".ogv", ".mpeg"]
        return _formats[index]

    def export_animation_to_file(self):
        if self.lineEdit_FileName.text() != "":
            file_format = self.get_file_format()
            filename = self.lineEdit_FileName.text() + file_format
            if os.path.exists(self.save_path):
                self.export_file_path = get_new_path(self.save_path, filename)
                self.opv.opvAnalysisRenderer.start_export_animation_to_file(self.export_file_path, self.frames)
                self.process_animation()
            else:
                title = "Invalid folder path"
                message = "Inform a valid folder path before trying export the animation.\n\n"
                message += f"{self.label_export_path.text()}"
                PrintMessageInput([title, message, "ERROR"])
                self.label_export_path.setText("<Folder path>")
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the animation."
            PrintMessageInput([title, message, "ERROR"])
            self.lineEdit_FileName.setFocus()

    def process_animation(self):
        self.frames = self.spinBox_frames.value()
        self.cycles = self.spinBox_cycles.value()
        self.opv.opvAnalysisRenderer._setNumberFrames(self.frames)
        self.opv.opvAnalysisRenderer._setNumberCycles(self.cycles)
        self.opv.opvAnalysisRenderer.playAnimation()
