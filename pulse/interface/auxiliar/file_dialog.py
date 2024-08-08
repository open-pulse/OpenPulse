from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt

from pulse import app

class FileDialog(QFileDialog):

    def __init__(self):
        super().__init__()

        desktop_geometry = app().desktop().screenGeometry()
        width = self.width()
        height = self.height()
        pos_x = int((desktop_geometry.width() - width)/2)
        pos_y = int((desktop_geometry.height() - height)/2)
        self.setGeometry(pos_x, pos_y, width, height)
        self.config_window()

    def config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        # self.setWindowTitle("OpenPulse")

    def get_open_file_name(self, caption, directory, filter):
        return self.getOpenFileName(self, caption, directory, filter)

    def get_save_file_name(self, caption, directory, filter):
        return self.getSaveFileName(self, caption, directory, filter)