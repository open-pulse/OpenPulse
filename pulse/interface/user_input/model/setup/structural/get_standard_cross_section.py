from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QBrush, QColor
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.libraries.standard_cross_sections import StandardCrossSections

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
        self._define_qt_variables()
        self._create_connections()
        self._load_cross_section_libraries()
        
        if section_data is None:
            self.load_treeWidget()
        else:
            if self.check_section(section_data):
                return
            self.load_treeWidget()

        self.exec()

    def _initialize(self):
        self.complete = False
        self.selected_id = None
        self.outside_diameter = 0.
        self.wall_thickness = 0.
        self.highlight_section = defaultdict(list)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_units : QComboBox

        # QRadioButton
        self.radioButton_carbon_steel : QRadioButton
        self.radioButton_stainless_steel : QRadioButton

        # QPushButton
        self.pushButton_confirm_selection : QPushButton

        # QTreeWidget
        self.treeWidget_section_data : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_units.currentIndexChanged.connect(self.load_treeWidget)
        #
        self.pushButton_confirm_selection.clicked.connect(self.confirm_selection)
        #
        self.radioButton_carbon_steel.clicked.connect(self.load_treeWidget)
        self.radioButton_stainless_steel.clicked.connect(self.load_treeWidget)
        #
        self.treeWidget_section_data.itemClicked.connect(self.on_click_item)
        self.treeWidget_section_data.itemDoubleClicked.connect(self.on_double_click_item)

    def _load_cross_section_libraries(self):
        std_data = StandardCrossSections()
        self.carbon_steel_cross_sections = std_data.carbon_steel_cross_sections
        self.stainless_steel_cross_sections = std_data.stainless_steel_cross_sections

    def reset_treeWidget_data(self):
        self.treeWidget_section_data.clear()
        for i in range(6):
            self.treeWidget_section_data.headerItem().setText(i, "")

    def load_treeWidget(self):

        self.std_data = dict()
        self.reset_treeWidget_data()

        if self.radioButton_carbon_steel.isChecked():
            self.std_data = self.carbon_steel_cross_sections
        else:
            self.std_data = self.stainless_steel_cross_sections

        widths = [50, 50, 50, 80, 80, 140, 140]
        if self.comboBox_units.currentIndex() == 0:
            unit = "in"
        else:
            unit = "mm"

        header_items = ["ID",
                        "NPS", 
                        "DN", 
                        "Identification", 
                        "Schedule", 
                        f"Outside diameter ({unit})", 
                        f"Wall thickness ({unit})"]
            
        for i, text in enumerate(header_items):
            self.treeWidget_section_data.headerItem().setText(i, text)
            self.treeWidget_section_data.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_section_data.setColumnWidth(i, widths[i])

        for index, data in self.std_data.items():
            item_values = [str(index)]
            for key, value in data.items():
                if key in header_items:
                    if "mm" in key:
                        item_values.append(str(round(value, 4)))
                    elif key == "Identification":
                        if self.radioButton_stainless_steel.isChecked():
                            item_values.append("--")
                        else:
                            item_values.append(str(value))
                    else:
                        item_values.append(str(value))

            new = QTreeWidgetItem(item_values)
            for i in range(len(item_values)):
                new.setTextAlignment(i, Qt.AlignCenter)
            
            self.treeWidget_section_data.addTopLevelItem(new)

        self.highlight_standard_section()

    def on_click_item(self, item):
        self.selected_id = int(item.text(0))  

    def on_double_click_item(self, item):
        _id = int(item.text(0))
        data = self.std_data[_id]
        self.outside_diameter = data["Outside diameter (in)"]*(25.4/1000)
        self.wall_thickness = data["Wall thickness (in)"]*(25.4/1000)
        self.complete = True
        self.close()

    def confirm_selection(self):
        if self.selected_id is not None:
            data = self.std_data[self.selected_id]
            self.outside_diameter = data["Outside diameter (in)"]*(25.4/1000)
            self.wall_thickness = data["Wall thickness (in)"]*(25.4/1000)
            self.complete = True
            self.close()

    def check_section(self, section_data):

        self.highlight_section = defaultdict(list)
        outside_diameter_1 = section_data["outside diameter"]
        thickness_1 = section_data["wall thickness"]

        self.std_data_CS = self.carbon_steel_cross_sections
        for index, data in self.std_data_CS.items():
            outside_diameter_2 = data["Outside diameter (in)"]*(25.4/1000)
            thickness_2 = data["Wall thickness (in)"]*(25.4/1000)
            if np.abs(outside_diameter_1 - outside_diameter_2) < 1e-4:
                if np.abs(thickness_1 - thickness_2) < 1e-4:
                    self.highlight_section["carbon steel pipe"].append(index-1)

        self.std_data_SS = self.stainless_steel_cross_sections
        for index, data in self.std_data_SS.items():
            outside_diameter_2 = data["Outside diameter (in)"]*(25.4/1000)
            thickness_2 = data["Wall thickness (in)"]*(25.4/1000)
            if np.abs(outside_diameter_1 - outside_diameter_2) < 1e-4:
                if np.abs(thickness_1 - thickness_2) < 1e-4:
                    self.highlight_section["stainless steel pipe"].append(index-1)

        if len(self.highlight_section) > 0:
            return False
        else:
            return True

    def highlight_standard_section(self):
        """
        """
        if len(self.highlight_section) > 0:
            self.pushButton_confirm_selection.setDisabled(True)
            for key, indexes in self.highlight_section.items():
                if key == "carbon steel pipe" and self.radioButton_carbon_steel.isChecked():
                    for index in indexes:
                        item = self.treeWidget_section_data.topLevelItem(index)
                        for i in range(7):
                            item.setForeground(i, QBrush(QColor(255,0,0)))
                            item.setBackground(i, QBrush(QColor(220,220,220)))
                        self.treeWidget_section_data.setCurrentItem(item)
                        self.treeWidget_section_data.setFocus()

                if key == "stainless steel pipe" and self.radioButton_stainless_steel.isChecked():
                    for index in indexes:
                        item = self.treeWidget_section_data.topLevelItem(index)
                        for i in range(7):
                            item.setForeground(i, QBrush(QColor(255,0,0)))
                            item.setBackground(i, QBrush(QColor(220,220,220)))
                        self.treeWidget_section_data.setCurrentItem(item)
                        self.treeWidget_section_data.setFocus()