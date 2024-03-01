from PyQt5.QtWidgets import QCheckBox, QComboBox, QFrame, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

class PlotStressesFieldForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/plots/results/structural/plot_stresses_field_for_harmonic_analysis.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project
        
        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connection()
        self.load_frequencies()

    def _initialize(self):

        self.selected_index = None
        self.update_damping = False

        self.stress_field = []
        self.stress_data = []

        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"])

        self.scaling_key = {0 : "absolute",
                            1 : "real"}

        self.solve = self.project.structural_solve
        self.preprocessor = self.project.preprocessor
        self.frequencies = self.project.frequencies
        self.dict_frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_damping_effect = self.findChild(QCheckBox, 'checkBox_damping_effect')
        # QComboBox
        self.comboBox_color_scaling = self.findChild(QComboBox, 'comboBox_color_scaling')
        self.comboBox_stress_type = self.findChild(QComboBox, 'comboBox_stress_type')
        # QFrame
        self.frame_button = self.findChild(QFrame, 'frame_button')
        self.frame_button.setVisible(False)
        # QLineEdit
        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
    
    def _create_connection(self):
        self.checkBox_damping_effect.stateChanged.connect(self._update_damping_effect)
        self.comboBox_color_scaling.currentIndexChanged.connect(self.plot_stress_field)
        self.comboBox_stress_type.currentIndexChanged.connect(self.plot_stress_field)
        self.pushButton_plot.clicked.connect(self.plot_stress_field)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

    def _update_damping_effect(self):
        self.update_damping = True
        self.plot_stress_field()
        
    def plot_stress_field(self):
        window_title = "WARNING"
        if self.lineEdit_selected_frequency.text() == "":
            title = "Aditional action required"
            message = "Select a frequency from the available list "
            message += "of frequencies to continue."
            PrintMessageInput([window_title, title, message])
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            if frequency_selected in self.frequencies:
                self.selected_index = self.dict_frequency_to_index[frequency_selected]
                self.get_stress_data()
            # else:
            #     title = "Aditional action required"
            #     message = "You have typed an invalid frequency. It's recommended "
            #     message += "to select a frequency from the available list of frequencies."
            #     PrintMessageInput([window_title, title, message])
            #     return

    def get_stress_data(self):

        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()

        if self.stress_data == [] or self.update_damping:
            self.stress_data = self.solve.stress_calculate( pressure_external = 0, 
                                                            damping_flag = self.flag_damping_effect )
            self.update_damping = False
            
        self.stress_field = { key:array[self.stress_key, self.selected_index] for key, array in self.stress_data.items() }
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses( np.min(list(self.stress_field.values())), 
                                                np.max(list(self.stress_field.values())), 
                                                self.stress_label )
        
        scale_index = self.comboBox_color_scaling.currentIndex()
        scaling_type = self.scaling_key[scale_index]
        self.opv.plot_stress_field(self.selected_index, scaling_type)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.plot_stress_field()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.plot_stress_field()

    def load_frequencies(self):
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_stress_field()
        elif event.key() == Qt.Key_Escape:
            self.close()