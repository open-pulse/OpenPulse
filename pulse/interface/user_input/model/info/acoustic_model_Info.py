from PyQt5.QtWidgets import QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse import UI_DIR
from pulse.interface.formatters.icons import *

class AcousticModelInfo(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "model/info/acoustic_model_info.ui", self)

        self.project = project
        self.preprocessor = project.preprocessor
        self.opv = opv
        self.opv.setInputObject(self)

        self.lineEdit_number_nodes = self.findChild(QLineEdit, 'lineEdit_number_nodes')
        self.lineEdit_number_elements = self.findChild(QLineEdit, 'lineEdit_number_elements')

        self.treeWidget_acoustic_pressure = self.findChild(QTreeWidget, 'treeWidget_acoustic_pressure')
        self.treeWidget_acoustic_pressure.setColumnWidth(1, 20)
        self.treeWidget_acoustic_pressure.setColumnWidth(2, 80)

        self.treeWidget_volume_velocity = self.findChild(QTreeWidget, 'treeWidget_volume_velocity')
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)

        self.treeWidget_specific_impedance = self.findChild(QTreeWidget, 'treeWidget_specific_impedance')
        self.treeWidget_specific_impedance.setColumnWidth(1, 20)
        self.treeWidget_specific_impedance.setColumnWidth(2, 80)

        self.treeWidget_radiation_impedance = self.findChild(QTreeWidget, 'treeWidget_radiation_impedance')
        self.treeWidget_radiation_impedance.setColumnWidth(1, 20)
        self.treeWidget_radiation_impedance.setColumnWidth(2, 80)

        self.treeWidget_perforated_plate = self.findChild(QTreeWidget, 'treeWidget_perforated_plate')
        self.treeWidget_perforated_plate.setColumnWidth(1, 20)
        self.treeWidget_perforated_plate.setColumnWidth(2, 80)

        self.treeWidget_element_length_correction = self.findChild(QTreeWidget, 'treeWidget_element_length_correction')
        self.treeWidget_element_length_correction.setColumnWidth(1, 20)
        self.treeWidget_element_length_correction.setColumnWidth(2, 80)

        self.load_nodes_info()
        self.project_info()
        self._load_icons()
        self._config_window()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()
    
    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F4:
            self.close()

    def project_info(self):
        self.acoustic_elements = self.preprocessor.get_acoustic_elements()
        self.nodes = self.preprocessor.get_nodes_relative_to_acoustic_elements()
        self.lineEdit_number_nodes.setText(str(len(self.nodes)))
        self.lineEdit_number_elements.setText(str(len(self.acoustic_elements)))
        
    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def load_nodes_info(self):
        
        for node in self.project.preprocessor.nodes_with_acoustic_pressure:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.acoustic_pressure))])
            self.treeWidget_acoustic_pressure.addTopLevelItem(new)
        
        for node in self.project.preprocessor.nodes_with_volume_velocity:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.volume_velocity))])
            self.treeWidget_volume_velocity.addTopLevelItem(new)

        for node in self.project.preprocessor.nodes_with_specific_impedance:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.specific_impedance))])
            self.treeWidget_specific_impedance.addTopLevelItem(new)
        
        for node in self.project.preprocessor.nodes_with_radiation_impedance:
            if node.radiation_impedance_type == 0:
                text = "Anechoic"
            elif node.radiation_impedance_type == 1:
                text = "Unflanged"
            elif node.radiation_impedance_type == 2:
                text = "Flanged"
            new = QTreeWidgetItem([str(node.external_index), text])
            self.treeWidget_radiation_impedance.addTopLevelItem(new)

        for element in self.project.preprocessor.element_with_length_correction:
            if element.acoustic_length_correction == 0:
                text = "Expansion"
            if element.acoustic_length_correction == 1:
                text = "Side branch"
            if element.acoustic_length_correction == 2:
                text = "Loop"
            new = QTreeWidgetItem([str(element.index), text])
            self.treeWidget_element_length_correction.addTopLevelItem(new)