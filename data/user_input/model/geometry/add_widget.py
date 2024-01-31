from PyQt5.QtWidgets import QComboBox, QWidget, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTextEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from data.user_input.model.geometry.cross_section_inputs import CrossSectionInputs
from data.user_input.model.setup.structural.material_input_new import MaterialInputsNew
from data.user_input.project.print_message_input import PrintMessageInput

# from opps.io.cad_file.cad_handler import CADHandler
from pulse.interface.cad_handler import CADHandler
from pulse import app


class AddStructuresWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(Path('data/user_input/ui_files/Model/geometry/add_widget.ui'), self)

    def _reset_variables(self):
        self.complete = False
        self.cross_section_info = None
        self.bending_radius = 0
        self.bending_factor = 0
        self.segment_information = dict()

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_segment_id: QComboBox
        self.comboBox_length_unit: QComboBox
        self.comboBox_section_type: QComboBox
        self.comboBox_bending_type: QComboBox

        # QFrame
        # self.left_frame: QFrame
        # self.right_frame: QFrame
        self.information_frame: QFrame

        # QGridLayout
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        # self.right_frame.setLayout(self.grid_layout)
        self.load_cross_section_widget()
        self.load_material_widget()

        # QLabel
        self.label_unit_delta_x: QLabel
        self.label_unit_delta_y: QLabel
        self.label_unit_delta_z: QLabel
        self.label_unit_diameter: QLabel
        self.label_unit_bending_radius: QLabel

        # QLineEdit
        self.lineEdit_delta_x: QLineEdit
        self.lineEdit_delta_y: QLineEdit
        self.lineEdit_delta_z: QLineEdit
        self.lineEdit_bending_radius: QLineEdit
        self.lineEdit_section_diameter: QLineEdit
        self.create_list_of_unit_labels()
        
        # QPushButton
        self.pushButton_set_cross_section: QPushButton
        self.pushButton_set_material: QPushButton
        self.pushButton_create_segment: QPushButton
        self.pushButton_finalize: QPushButton
        self.pushButton_delete_segment: QPushButton

        self.pushButton_confirm_pipe: QPushButton
        # self.pushButton_confirm_beam: QPushButton
        self.pushButton_set_material: QPushButton
        # self.pushButton_process_geometry.setIcon(self.export_icon)

        # QTabWidget
        self.tabWidget_main: QTabWidget
        self.tabWidget_general: QTabWidget
        self.tabWidget_pipe_section: QTabWidget
        self.tabWidget_beam_section: QTabWidget

        # QTextEdit
        self.textEdit_segment_information: QTextEdit
        self.textEdit_segment_information.setText("Apenas para testar...\ne ver se consigo configurar corretamente.")
        self.textEdit_segment_information.setVisible(False)


    def load_cross_section_widget(self):
        self.cross_section_widget = CrossSectionInputs()
        self.cross_section_widget.show()
        # self.grid_layout.addWidget(self.cross_section_widget, 0, 0)
        # self.right_frame.setVisible(False)

    def load_material_widget(self):
        self.material_widget = MaterialInputsNew()
        self.material_widget.show()
        # self.grid_layout.addWidget(self.material_widget, 1, 0)
        # self.right_frame.setVisible(False)
