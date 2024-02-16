from PyQt5.QtWidgets import QComboBox, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
import numpy as np

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse import app, UI_DIR

class PlotStressesFieldForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/plots/results/structural/plot_stresses_field_for_static_analysis.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

    def _initialize(self):
        self.selected_index = None
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

        self.solve = self.project.structural_solve
        self.preprocessor = self.project.preprocessor

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_stress_type = self.findChild(QComboBox, 'comboBox_stress_type')
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')

    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.confirm_button)

    def get_stress_data(self):

        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]

        if self.stress_data == []:
            self.stress_data = self.solve.stress_calculate( pressure_external = 0, 
                                                            damping_flag = False )
            
        self.stress_field = { key:array[self.stress_key, self.selected_index] for key, array in self.stress_data.items() }
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses( np.min(list(self.stress_field.values())), 
                                                np.max(list(self.stress_field.values())), 
                                                self.stress_label )
        scaling_setup = {}
        self.opv.plot_stress_field(self.selected_index, scaling_setup)
        
    def check(self):
        self.selected_index = 0
        self.get_stress_data()

    def confirm_button(self):
        self.check()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()