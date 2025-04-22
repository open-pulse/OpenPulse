from PySide6.QtWidgets import QDialog, QLineEdit, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt

from pulse import app, UI_DIR

from molde import load_ui

import numpy as np

class AcousticModelInfo(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/info/acoustic_model_info.ui"
        load_ui(ui_path, self, UI_DIR)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_nodal_properties()
        self.load_elements_properties()
        self.load_project_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.preprocessor = self.project.model.preprocessor

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

        for i, w in enumerate([70, 70]):
            self.treeWidget_acoustic_pressure.setColumnWidth(i, w)
            self.treeWidget_volume_velocity.setColumnWidth(i, w)
            self.treeWidget_specific_impedance.setColumnWidth(i, w)
            self.treeWidget_radiation_impedance.setColumnWidth(i, w)
            self.treeWidget_perforated_plate.setColumnWidth(i, w)
            self.treeWidget_element_length_correction.setColumnWidth(i, w)

            self.treeWidget_acoustic_pressure.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_volume_velocity.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_specific_impedance.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_radiation_impedance.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_perforated_plate.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_element_length_correction.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def text_label(self, value):

        text = ""
        if isinstance(value, (complex | int | float)):
            value_label = str(value)
        elif isinstance(value, list) and len(value) == 1:
            value_label = str(value[0])
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        elif isinstance(value, str):
            value_label = value
        else:
            return ""

        text = "{}".format(value_label)
        return text

    def load_nodal_properties(self):

        for (property, *args), data in app().project.model.properties.nodal_properties.items():
            if property == "acoustic_pressure":
                node_id = args[0]
                values = data["values"]
                item = QTreeWidgetItem([str(node_id), str(self.text_label(values))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_acoustic_pressure.addTopLevelItem(item)

            if property == "volume_velocity":
                node_id = args[0]
                values = data["values"]
                item = QTreeWidgetItem([str(node_id), str(self.text_label(values))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_volume_velocity.addTopLevelItem(item)

            if property == "specific_impedance":
                node_id = args[0]
                values = data["values"]
                item = QTreeWidgetItem([str(node_id), str(self.text_label(values))])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_specific_impedance.addTopLevelItem(item)

            if property == "radiation_impedance":
                node_id = args[0]
                index = data["impedance_type"]
                impedance_types = ["Anechoic", "Unflanged", "Flanged"]    
                item = QTreeWidgetItem([str(node_id), impedance_types[index]])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_radiation_impedance.addTopLevelItem(item)

    def load_elements_properties(self):

        for (property, *args), data in app().project.model.properties.element_properties.items():
            if property == "element_length_correction":
                element_id = args[0]
                correction_types = ["Expansion", "Side branch", "Loop"]
                index = data["correction_type"]
                item = QTreeWidgetItem([str(element_id), correction_types[index]])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_element_length_correction.addTopLevelItem(item)

            if property == "perforated_plate":
                element_id = args[0]
                hole_diameter = data.get("hole_diameter", "")
                thickness = data.get("plate_thickness", "")
                porosity = data.get("area_porosity", "")
                discharge_coefficient = data.get("discharge_coefficient", "")
                text = f"[{hole_diameter}, {thickness}, {round(porosity, 6)}, {discharge_coefficient}]"
                item = QTreeWidgetItem([str(element_id), text])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_perforated_plate.addTopLevelItem(item)

    def load_project_info(self):
        self.acoustic_elements = self.preprocessor.get_acoustic_elements()
        self.nodes = self.preprocessor.get_nodes_relative_to_acoustic_elements()
        self.lineEdit_number_nodes.setText(str(len(self.nodes)))
        self.lineEdit_number_elements.setText(str(len(self.acoustic_elements)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F4:
            self.close()