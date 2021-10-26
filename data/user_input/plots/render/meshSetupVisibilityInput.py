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

        self.checkBox_nodes = self.findChild(QCheckBox, 'checkBox_nodes')
        self.checkBox_elements = self.findChild(QCheckBox, 'checkBox_elements')
        self.checkBox_acoustic_symbols = self.findChild(QCheckBox, 'checkBox_acoustic_symbols')
        self.checkBox_structural_symbols = self.findChild(QCheckBox, 'checkBox_structural_symbols')

        self.toolButton_confirm = self.findChild(QToolButton, 'toolButton_confirm')
        self.toolButton_confirm.pressed.connect(self.confirm_and_update_mesh_visibility)

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_mesh_visibility()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def confirm_and_update_mesh_visibility(self):
        # gets the correspondent flag according to the checkbox then bitwise OR everything
        # and send the result to opvRenderer
        plot_flags = (
            (PlotFlags.SHOW_LINES)
            | (PlotFlags.SHOW_NODES if self.checkBox_nodes.isChecked() else 0)
            | (PlotFlags.SHOW_TUBES if self.checkBox_elements.isChecked() else 0)
            | (PlotFlags.SHOW_SYMBOLS if self.checkBox_acoustic_symbols.isChecked() else 0)
        )

        selection_flags = 0

        self.opv.opvRenderer.setPlotFlags(plot_flags)
        self.opv.opvRenderer.setSelectionFlags(selection_flags)
        self.close()