from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox
from data.user_input.project.printMessageInput import PrintMessageInput
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np

from pulse.interface.opvRenderer import PlotFilter, SelectionFilter

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
        self.toolButton_confirm.pressed.connect(self.confirm_and_update_mesh_visibility)

        self.set_current_state()

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_mesh_visibility()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def set_current_state(self):
        plot_filter = self.opv.opvRenderer._plotFilter
        selection_filter = self.opv.opvRenderer._selectionFilter

        self.checkBox_nodes_viewer.setChecked(
            PlotFilter.nodes & plot_filter
        )
        self.checkBox_elements_viewer.setChecked(
            PlotFilter.tubes & plot_filter
        )
        self.checkBox_acoustic_symbols_viewer.setChecked(
            PlotFilter.acoustic_symbols & plot_filter
        )
        self.checkBox_structural_symbols_viewer.setChecked(
            PlotFilter.structural_symbols & plot_filter
        )

        
        self.checkBox_nodes_selector.setChecked(
            SelectionFilter.nodes & selection_filter
        )
        self.checkBox_elements_selector.setChecked(
            SelectionFilter.elements & selection_filter
        )
        self.checkBox_lines_selector.setChecked(
            SelectionFilter.entities & selection_filter
        )
        

    def confirm_and_update_mesh_visibility(self):
        # gets the correspondent flag according to the checkbox then bitwise OR everything
        # and send the result to opvRenderer

        # convenience variables
        plt_nodes = self.checkBox_nodes_viewer.isChecked()
        plt_tubes = self.checkBox_elements_viewer.isChecked()
        plt_acoustic = self.checkBox_acoustic_symbols_viewer.isChecked()
        plt_structural = self.checkBox_structural_symbols_viewer.isChecked()
        slc_nodes = self.checkBox_nodes_selector.isChecked()
        slc_elements = self.checkBox_elements_selector.isChecked()
        slc_entities = self.checkBox_lines_selector.isChecked()

        self.opv.opvRenderer.setPlotFilter(
            (PlotFilter.lines)
            | (PlotFilter.nodes if plt_nodes else 0)
            | (PlotFilter.tubes if plt_tubes else 0)
            | (PlotFilter.acoustic_symbols if plt_acoustic else 0)
            | (PlotFilter.structural_symbols if plt_structural else 0)
            | (PlotFilter.transparent if (plt_nodes or plt_acoustic or plt_structural) else 0)
        )
        
        self.opv.opvRenderer.setSelectionFilter(
            (SelectionFilter.nodes if slc_nodes and plt_nodes else 0)
            | (SelectionFilter.elements if slc_elements else 0)
            | (SelectionFilter.entities if slc_entities else 0)
        )

        self.close()