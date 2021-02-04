from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
from time import time
import configparser

# from pulse.processing.solution_structural import *

class LogTimes(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/Analysis/runAnalysisInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.project = project
        self.label_title = self.findChild(QLabel, 'label_title')
        self.run()
        # self.show()
        self.exec_()

    def run(self):

        text = "Solution finished!\n\n"
        # text += "Time to check all entries: {} [s]\n".format(round(self.project.time_to_checking_entries, 6))
        text += "Time to process cross-sections: {} [s]\n".format(round(self.project.time_to_process_cross_sections, 6))
        text += "Time to solve the model: {} [s]\n".format(round(self.project.time_to_solve_model, 6))
        text += "Time elapsed in post-processing: {} [s]\n\n".format(round(self.project.time_to_postprocess, 6))
        text += "Press ESC to continue..."
        self.label_title.setText(text)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()