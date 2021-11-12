from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox, QRadioButton
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

        self.radioButton_black_color = self.findChild(QRadioButton, 'radioButton_black_color')
        self.radioButton_dark_gray_color = self.findChild(QRadioButton, 'radioButton_dark_gray_color')
        self.radioButton_light_gray_color = self.findChild(QRadioButton, 'radioButton_light_gray_color')
        self.radioButton_white_color = self.findChild(QRadioButton, 'radioButton_white_color')

        self.checkBox_OpenPulse_logo = self.findChild(QCheckBox, 'checkBox_OpenPulse_logo')
        self.checkBox_MOPT_logo = self.findChild(QCheckBox, 'checkBox_MOPT_logo')
        self.checkBox_reference_scale = self.findChild(QCheckBox, 'checkBox_reference_scale')
        
        self.toolButton_confirm = self.findChild(QToolButton, 'toolButton_confirm')
        self.toolButton_confirm.clicked.connect(self.confirm_and_update_mesh_visibility)
        self.load_background_color_state()
        self.load_logo_state()
        self.load_reference_scale_state()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_mesh_visibility()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def load_background_color_state(self):
        if self.opv.background_color == (0,0,0):
            self.radioButton_black_color.setChecked(True)
        elif self.opv.background_color == (0.25,0.25,0.25):
            self.radioButton_dark_gray_color.setChecked(True)
        elif self.opv.background_color == (0.7,0.7,0.7):
            self.radioButton_light_gray_color.setChecked(True)
        elif self.opv.background_color == (1,1,1):
            self.radioButton_white_color.setChecked(True)

    def update_background_color_state(self):

        if self.radioButton_black_color.isChecked():
            color = (0,0,0)
            font_color = (1,1,1)
        elif self.radioButton_dark_gray_color.isChecked():
            color = (0.25,0.25,0.25)
            font_color = (1,1,1)
        elif self.radioButton_light_gray_color.isChecked():
            color = (0.7,0.7,0.7)
            font_color = (0,0,0)
        elif self.radioButton_white_color.isChecked():
            color = (1,1,1)
            font_color = (0,0,0)
        self.opv.background_color = color
        self.opv.font_color = font_color

        self.opv.opvRenderer.changeBackgroundColor(color)
        self.opv.opvAnalysisRenderer.changeBackgroundColor(color)
        self.opv.opvRenderer.changeFontColor(font_color)
        self.opv.opvAnalysisRenderer.changeFontColor(font_color)
        self.opv.opvAnalysisRenderer._updateFontColor(font_color)
    
    def load_reference_scale_state(self):
        self.checkBox_reference_scale.setChecked(self.opv.show_reference_scale)

    def update_reference_scale_state(self):
        self.opv.show_reference_scale = self.checkBox_reference_scale.isChecked()
        self.opv.opvAnalysisRenderer._createScaleBar()

    def load_logo_state(self):
        self.checkBox_OpenPulse_logo.setChecked(self.opv.add_OpenPulse_logo)
        self.checkBox_MOPT_logo.setChecked(self.opv.add_MOPT_logo)
            
    def update_logo_state(self):        
        self.opv.add_OpenPulse_logo = self.checkBox_OpenPulse_logo.isChecked()
        self.opv.add_MOPT_logo = self.checkBox_MOPT_logo.isChecked()
        self.opv.opvRenderer._addLogosToRender(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)
        self.opv.opvAnalysisRenderer._addLogosToRender(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)

    def confirm_and_update_mesh_visibility(self):
        self.update_logo_state()
        self.update_background_color_state()
        self.update_reference_scale_state()
        # self.update_renders()
        self.close()

    def update_renders(self):
        self.opv.updateRendererMesh()
        if self.opv.change_plot_to_mesh:
            self.opv.changePlotToMesh()
        elif self.opv.change_plot_to_entities:
            self.opv.changePlotToEntities()
        elif self.opv.change_plot_to_entities_with_cross_section:
            self.opv.changePlotToEntitiesWithCrossSection()
