from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox
from data.user_input.project.printMessageInput import PrintMessageInput
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
import numpy as np

from PyQt5 import uic

class MeshSetupVisibilityInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Render/meshSetupVisibilityInput.ui', self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.opv = opv
        self.opv.setInputObject(self)

        self.checkBox_nodes_viewer = self.findChild(QCheckBox, 'checkBox_nodes_viewer')
        self.checkBox_elements_viewer = self.findChild(QCheckBox, 'checkBox_elements_viewer')
        self.checkBox_acoustic_symbols_viewer = self.findChild(QCheckBox, 'checkBox_acoustic_symbols_viewer')
        self.checkBox_structural_symbols_viewer = self.findChild(QCheckBox, 'checkBox_structural_symbols_viewer')

        self.checkBox_nodes_selector = self.findChild(QCheckBox, 'checkBox_nodes_selector')
        self.checkBox_elements_selector = self.findChild(QCheckBox, 'checkBox_elements_selector')
        self.checkBox_lines_selector = self.findChild(QCheckBox, 'checkBox_lines_selector')

        self.radioButton_black_color = self.findChild(QCheckBox, 'radioButton_black_color')
        self.radioButton_dark_gray_color = self.findChild(QCheckBox, 'radioButton_dark_gray_color')
        self.radioButton_light_gray_color = self.findChild(QCheckBox, 'radioButton_light_gray_color')
        self.radioButton_white_color = self.findChild(QCheckBox, 'radioButton_white_color')

        self.radioButton_OpenPulse_logo = self.findChild(QCheckBox, 'radioButton_OpenPulse_logo')
        self.radioButton_MOPT_logo = self.findChild(QCheckBox, 'radioButton_MOPT_logo')
        self.radioButton_reference_scale = self.findChild(QCheckBox, 'radioButton_reference_scale')
        
        self.toolButton_confirm = self.findChild(QToolButton, 'toolButton_confirm')

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_mesh_visibility()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def confirm_and_update_mesh_visibility(self):
        self.close()