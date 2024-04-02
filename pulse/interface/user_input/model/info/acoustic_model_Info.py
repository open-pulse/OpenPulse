from PyQt5.QtWidgets import QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np

from pulse import UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon

class AcousticModelInfo(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/info/acoustic_model_info.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_nodes_info()
        self.project_info()
        self._load_icons()
        self._config_window()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.preprocessor = self.project.preprocessor

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_number_nodes : QLineEdit
        self.lineEdit_number_elements : QLineEdit

        # QTreeWidget
        self.treeWidget_acoustic_pressure : QTreeWidget
        self.treeWidget_volume_velocity : QTreeWidget
        self.treeWidget_specific_impedance : QTreeWidget
        self.treeWidget_radiation_impedance : QTreeWidget
        self.treeWidget_perforated_plate : QTreeWidget
        self.treeWidget_element_length_correction : QTreeWidget

    def _create_connections(self):
        pass

    def _config_widgets(self):
        self.treeWidget_acoustic_pressure.setColumnWidth(1, 20)
        self.treeWidget_acoustic_pressure.setColumnWidth(2, 80)

        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)

        self.treeWidget_specific_impedance.setColumnWidth(1, 20)
        self.treeWidget_specific_impedance.setColumnWidth(2, 80)

        self.treeWidget_radiation_impedance.setColumnWidth(1, 20)
        self.treeWidget_radiation_impedance.setColumnWidth(2, 80)

        self.treeWidget_perforated_plate.setColumnWidth(1, 20)
        self.treeWidget_perforated_plate.setColumnWidth(2, 80)

        self.treeWidget_element_length_correction.setColumnWidth(1, 20)
        self.treeWidget_element_length_correction.setColumnWidth(2, 80)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F4:
            self.close()