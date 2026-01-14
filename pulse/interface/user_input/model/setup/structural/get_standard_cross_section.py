from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QBrush, QColor
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.libraries.standard_cross_sections import StandardCrossSections
from pulse.utils.unit_conversion import in_to_m

from molde import load_ui

import numpy as np
from collections import defaultdict

class GetStandardCrossSection(QDialog):
    def __init__(self, *args, **kwargs):
        super(GetStandardCrossSection, self).__init__()
        
        ui_path = UI_DIR / "model/setup/structural/standard_cross_section_input.ui"
        load_ui(ui_path, self, UI_DIR)

        section_data = kwargs.get("section_data", None)

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._define_qt_variables()
        self._create_connections()
        self._load_cross_section_libraries()
        
        if section_data is not None:
            if self.is_cross_section_standardized(section_data):
                return

        self.load_standardized_section_data()
        self.exec()

    def _initialize(self):
        self.outside_diameter = 0.
        self.wall_thickness = 0.
        self.nps = 0.

        self.std_data = dict()
        self.highlight_section = defaultdict(list)

        self.complete = False
        self.selected_id = None
        self.nps_to_filter = None
        self.cache_selected_nps = None

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_nps_filter : QCheckBox

        # QComboBox
        self.comboBox_pipe_material : QComboBox
        self.comboBox_nps_filter : QComboBox
        self.comboBox_units : QComboBox

        # QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_confirm_selection : QPushButton

        # QTreeWidget
        self.treeWidget_section_data : QTreeWidget

    def _create_connections(self):
        #
        self.checkBox_nps_filter.stateChanged.connect(self.nps_filter_callback)
        #
        self.comboBox_nps_filter.currentIndexChanged.connect(self.nps_filter_callback)
        self.comboBox_pipe_material.currentIndexChanged.connect(self.pipe_material_callback)
        self.comboBox_units.currentIndexChanged.connect(self.load_standardized_section_data)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm_selection.clicked.connect(self.confirm_selection)
        #
        self.treeWidget_section_data.itemClicked.connect(self.on_click_item)
        self.treeWidget_section_data.itemDoubleClicked.connect(self.on_double_click_item)

    def _config_widgets(self):
        self.comboBox_nps_filter.setDisabled(True)

    def update_available_sections(self):
        self.comboBox_nps_filter.blockSignals(True)
        self.comboBox_nps_filter.clear()

        # nominal pipe sizes for carbon steel pipes
        if self.comboBox_pipe_material.currentText() == "Carbon steel":

            nps_labels = [
                "0.125 (1/8)",
                "0.250 (1/4)",
                "0.375 (3/4)",
                "1",
                "1.25 (1 + 1/4)",
                "1.5 (1 + 1/2)",
                "2",
                "2.5 (2 + 1/2)",
                "3",
                "3.5 (3 + 1/2)",
                "4",
                "5",
                "6",
                "8",
                "10",
                "12",
                "14",
                "16",
                "18",
                "20",
                "22",
                "24",
                "26",
                "28",
                "30",
                "32",
                "34",
                "36",
                "38",
                "40",
                "42",
                "44",
                "46",
                "48",
                "52",
                "56",
                "60",
                "64",
                "68",
                "72",
                "76",
                "80",                
            ]

        # nominal pipe sizes for stainless steel pipes
        else:

            nps_labels = [
                "0.125 (1/8)",
                "0.250 (1/4)",
                "0.375 (3/4)",
                "1",
                "1.25 (1 + 1/4)",
                "1.5 (1 + 1/2)",
                "2",
                "2.5 (2 + 1/2)",
                "3",
                "3.5 (3 + 1/2)",
                "4",
                "5",
                "6",
                "8",
                "10",
                "12",
                "14",
                "16",
                "18",
                "20",
                "22",
                "24",
                "30",                
            ]

        self.comboBox_nps_filter.addItems(nps_labels)
        if self.cache_selected_nps is not None:
            self.comboBox_nps_filter.setCurrentText(self.cache_selected_nps)
            if self.checkBox_nps_filter.isChecked():
                self.cache_selected_nps = self.comboBox_nps_filter.currentText()
                self.nps_to_filter = float(self.cache_selected_nps.split(" (")[0])

        self.comboBox_nps_filter.blockSignals(False)

    def pipe_material_callback(self):
        self.update_available_sections()
        self.load_standardized_section_data()

    def _load_cross_section_libraries(self):
        std_data = StandardCrossSections()
        self.carbon_steel_cross_sections = std_data.carbon_steel_cross_sections
        self.stainless_steel_cross_sections = std_data.stainless_steel_cross_sections
        # self.filter_sections_based_on_nps()

    def filter_sections_based_on_nps(self):
        self.nps_based_cs_pipe_section = defaultdict(list)
        for index, data_cs in self.carbon_steel_cross_sections.items():
            NPS = data_cs.get("NPS")
            if NPS is None:
                continue

            self.nps_based_cs_pipe_section[NPS].append(index)

        self.nps_based_ss_pipe_section = defaultdict(list)
        for index, data_ss in self.stainless_steel_cross_sections.items():
            NPS = data_ss.get("NPS")
            if NPS is None:
                continue

            self.nps_based_ss_pipe_section[NPS].append(index)

    def nps_filter_callback(self):
        self.cache_selected_nps = None
        self.nps_to_filter = None
        nps_filter = self.checkBox_nps_filter.isChecked()
        self.comboBox_nps_filter.setEnabled(nps_filter)

        if nps_filter:
            selected_nps = self.comboBox_nps_filter.currentText()
            self.cache_selected_nps = selected_nps
            self.nps_to_filter = float(selected_nps.split(" (")[0])

        self.load_standardized_section_data()

    def load_standardized_section_data(self):

        self.treeWidget_section_data.clear()
        for i in range(6):
            self.treeWidget_section_data.headerItem().setText(i, "")

        carbon_steel = self.comboBox_pipe_material.currentText() == "Carbon steel"
        if carbon_steel:
            self.std_data = self.carbon_steel_cross_sections
        else:
            self.std_data = self.stainless_steel_cross_sections

        widths = [50, 50, 50, 80, 80, 140, 140]
        if self.comboBox_units.currentIndex() == 0:
            unit = "in"
        else:
            unit = "mm"

        header_items = [
            "ID",
            "NPS", 
            "DN", 
            "Identification", 
            "Schedule", 
            f"Outside diameter ({unit})", 
            f"Wall thickness ({unit})",
            ]
            
        for i, text in enumerate(header_items):
            self.treeWidget_section_data.headerItem().setText(i, text)
            self.treeWidget_section_data.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_section_data.setColumnWidth(i, widths[i])

        for index, data in self.std_data.items():
            if self.nps_to_filter is not None:
                if data.get("NPS") != self.nps_to_filter:
                    continue

            item_values = [str(index)]

            for key, value in data.items():
                if key in header_items:
                    if "mm" in key:
                        item_values.append(str(round(value, 4)))

                    elif key == "Identification":
                        if carbon_steel:
                            item_values.append(str(value))
                        else:
                            item_values.append("--")

                    else:
                        item_values.append(str(value))

            new = QTreeWidgetItem(item_values)
            for i in range(len(item_values)):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_section_data.addTopLevelItem(new)

        self.highlight_standard_section()

    def get_std_data(self, data: dict):
        outside_diameter = in_to_m(data.get("Outside diameter (in)", -1.0))
        wall_thickness = in_to_m(data.get("Wall thickness (in)", -1.0))
        nps = in_to_m(data.get("NPS", -1.0))
        return outside_diameter, wall_thickness, nps

    def on_click_item(self, item):
        self.selected_id = int(item.text(0))  

    def on_double_click_item(self, item):
        _id = int(item.text(0))
        data = self.std_data.get(_id)
        if not isinstance(data, dict):
            return

        self.outside_diameter,  self.wall_thickness, self.nps = self.get_std_data(data)
        self.complete = True
        self.close()

    def confirm_selection(self):
        if self.selected_id is None:
            return
    
        data = self.std_data.get(self.selected_id)
        if not isinstance(data, dict):
            return

        self.outside_diameter,  self.wall_thickness, self.nps = self.get_std_data(data)
        self.complete = True
        self.close()

    def is_cross_section_standardized(self, section_data: dict):

        self.highlight_section.clear()
        outside_diameter_req = section_data.get("outside diameter")
        thickness_req = section_data.get("wall thickness")

        for index, data_cs in self.carbon_steel_cross_sections.items():
            outside_diameter_cs, thickness_cs, _ = self.get_std_data(data_cs)
            if np.abs(outside_diameter_req - outside_diameter_cs) > 1e-4:
                continue
        
            if np.abs(thickness_req - thickness_cs) > 1e-4:
                continue

            self.highlight_section["carbon steel pipe"].append(index - 1)

        for index, data_ss in self.stainless_steel_cross_sections.items():
            outside_diameter_ss, thickness_ss, _ = self.get_std_data(data_ss)
            if np.abs(outside_diameter_req - outside_diameter_ss) > 1e-4:
                continue

            if np.abs(thickness_req - thickness_ss) > 1e-4:
                continue

            self.highlight_section["stainless steel pipe"].append(index - 1)

        if self.highlight_section:
            return False

        return True

    def highlight_standard_section(self):
        """
        """
        if not self.highlight_section:
            return

        carbon_steel = self.comboBox_pipe_material.currentText() == "Carbon steel"
        stainless_steel = self.comboBox_pipe_material.currentText() == "Stainless steel"

        self.checkBox_nps_filter.setDisabled(True)
        self.pushButton_confirm_selection.setDisabled(True)

        for key, indexes in self.highlight_section.items():
            if key == "carbon steel pipe" and carbon_steel:
                for index in indexes:
                    item = self.treeWidget_section_data.topLevelItem(index)
                    for i in range(7):
                        item.setForeground(i, QBrush(QColor(255,0,0)))
                        item.setBackground(i, QBrush(QColor(220,220,220)))
                    self.treeWidget_section_data.setCurrentItem(item)
                    self.treeWidget_section_data.setFocus()

            if key == "stainless steel pipe" and stainless_steel:
                for index in indexes:
                    item = self.treeWidget_section_data.topLevelItem(index)
                    for i in range(7):
                        item.setForeground(i, QBrush(QColor(255,0,0)))
                        item.setBackground(i, QBrush(QColor(220,220,220)))
                    self.treeWidget_section_data.setCurrentItem(item)
                    self.treeWidget_section_data.setFocus()