from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialog, QTabWidget, QLabel, QCheckBox
from data.user_input.project.printMessageInput import PrintMessageInput
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np

from pulse.interface.opvRenderer import PlotFlags, SelectionFlags

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
        plot_flags = self.opv.opvRenderer._plotFlags
        selection_flags = self.opv.opvRenderer._selectionFlags

        self.checkBox_nodes_viewer.setChecked(
            PlotFlags.SHOW_NODES & plot_flags
        )
        self.checkBox_elements_viewer.setChecked(
            PlotFlags.SHOW_TUBES & plot_flags
        )
        self.checkBox_acoustic_symbols_viewer.setChecked(
            PlotFlags.SHOW_SYMBOLS & plot_flags
        )
        
        self.checkBox_nodes_selector.setChecked(
            SelectionFlags.SELECT_NODES & selection_flags
        )
        self.checkBox_elements_selector.setChecked(
            SelectionFlags.SELECT_ELEMENTS & selection_flags
        )
        self.checkBox_lines_selector.setChecked(
            SelectionFlags.SELECT_ENTITIES & selection_flags
        )
        

    def confirm_and_update_mesh_visibility(self):
        # gets the correspondent flag according to the checkbox then bitwise OR everything
        # and send the result to opvRenderer

        plt_nodes = self.checkBox_nodes_viewer.isChecked()
        plt_tubes = self.checkBox_elements_viewer.isChecked()
        plt_symbols = self.checkBox_acoustic_symbols_viewer.isChecked()
        
        slc_nodes = self.checkBox_nodes_selector.isChecked()
        slc_elements = self.checkBox_elements_selector.isChecked()
        slc_entities = self.checkBox_lines_selector.isChecked()

        plot_flags = (
            (PlotFlags.SHOW_LINES)
            | (PlotFlags.SHOW_NODES if plt_nodes else 0)
            | (PlotFlags.SHOW_TUBES if plt_tubes else 0)
            | (PlotFlags.SHOW_SYMBOLS if plt_symbols else 0)
            | (PlotFlags.SHOW_TRANSP if plt_nodes else 0)
        )

        selection_flags = (
            (SelectionFlags.SELECT_NODES if slc_nodes and plt_nodes else 0)
            | (SelectionFlags.SELECT_ELEMENTS if slc_elements else 0)
            | (SelectionFlags.SELECT_ENTITIES if slc_entities else 0)
        )

        self.opv.opvRenderer.setPlotFlags(plot_flags)
        self.opv.opvRenderer.setSelectionFlags(selection_flags)
        self.close()