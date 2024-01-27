from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from pulse.preprocessing.cross_section import get_beam_section_properties, get_points_to_plot_section
from data.user_input.model.setup.structural.get_standard_cross_section import GetStandardCrossSection
from data.user_input.project.print_message_input import PrintMessageInput

window_title = "Error"
window_title2 = "Warning"

class MaterialInputsNew(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/geometry/material_input_widget.ui'), self)

        self.reset()
        self.define_qt_variables()
        self.create_connections()
        # self.create_lists_of_entries()
        # self.config_treeWidget()
        

    def reset(self):
        pass
        

    def define_qt_variables(self):

        self.pushButton_attribute_material = self.findChild(QPushButton, 'pushButton_attribute_material')

        return

        # QFrame
        self.bottom_frame = self.findChild(QFrame, 'bottom_frame')
        self.top_frame = self.findChild(QFrame, 'top_frame')
        self.selection_frame = self.findChild(QFrame, 'selection_frame')
        # self.top_frame.setVisible(False)
        # self.selection_frame.setVisible(False)
        # self.adjustSize()

        self.lineEdit_element_id_initial = self.findChild(QLineEdit, 'lineEdit_element_id_initial')

    def create_connections(self):
        
        pass

    def load_materials(self):
        pass