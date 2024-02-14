from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
import numpy as np

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

class PlotStressFieldForStaticAnalysis(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/structural_/plot_stress_field_for_static_analysis.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.solve = self.project.structural_solve
        self.preprocessor = self.project.preprocessor

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.exec()


    def _reset_variables(self):
        self.selected_index = None
        self.stress_field = []
        self.stress_data = []
        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", "Normal bending y", "Normal bending z", "Hoop", "Torsional shear", "Transversal shear xy", "Transversal shear xz"])


    def _define_qt_variables(self):
        # QPushButton object
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QRadioButton objects
        self.radioButton_normal_axial = self.findChild(QRadioButton, 'radioButton_normal_axial')
        self.radioButton_normal_bending_y = self.findChild(QRadioButton, 'radioButton_normal_bending_y')
        self.radioButton_normal_bending_z = self.findChild(QRadioButton, 'radioButton_normal_bending_z')
        self.radioButton_hoop = self.findChild(QRadioButton, 'radioButton_hoop')
        self.radioButton_transv_shear_xy = self.findChild(QRadioButton, 'radioButton_transv_shear_xy')
        self.radioButton_transv_shear_xz = self.findChild(QRadioButton, 'radioButton_transv_shear_xz')
        self.radioButton_torsional_shear = self.findChild(QRadioButton, 'radioButton_torsional_shear')
        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()


    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.confirm_button)
        self.radioButton_normal_axial.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_hoop.clicked.connect(self.radioButtonEvent)
        self.radioButton_torsional_shear.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xy.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xz.clicked.connect(self.radioButtonEvent)
        self.radioButtonEvent()


    def radioButtonEvent(self):
        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()
        #
        self.masks = [  self.flag_normal_axial, 
                        self.flag_normal_bending_y, 
                        self.flag_normal_bending_z, 
                        self.flag_hoop,
                        self.flag_torsional_shear, 
                        self.flag_transv_shear_xy, 
                        self.flag_transv_shear_xz  ]


    def get_stress_data(self):

        self.stress_label = self.labels[self.masks][0]
        self.stress_key = self.keys[self.masks][0]

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