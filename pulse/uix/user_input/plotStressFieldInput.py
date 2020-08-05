from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QPushButton, QCheckBox
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np

# from pulse.postprocessing.plot_structural_data import get_stress_data

class PlotStressFieldInput(QDialog):
    def __init__(self, project, solve, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotStressFieldInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.solve = solve
        self.opv = opv
        self.mesh = self.project.mesh
        self.damping = self.project.get_damping()
        self.frequencies = project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.selected_index = None

        self.stress_field = []
        self.stress_data = []

        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        self.treeWidget_list_frequencies = self.findChild(QTreeWidget, 'treeWidget_list_frequencies')
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        self.checkBox_damping_effect = self.findChild(QCheckBox, 'checkBox_damping_effect')

        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()
        self.checkBox_damping_effect.clicked.connect(self._update_damping_effect)

        self.pushButton_plot.clicked.connect(self.confirm_button)

        self.radioButton_normal_axial = self.findChild(QRadioButton, 'radioButton_normal_axial')
        self.radioButton_normal_bending_y = self.findChild(QRadioButton, 'radioButton_normal_bending_y')
        self.radioButton_normal_bending_z = self.findChild(QRadioButton, 'radioButton_normal_bending_z')
        self.radioButton_hoop = self.findChild(QRadioButton, 'radioButton_hoop')
        self.radioButton_transv_shear_y = self.findChild(QRadioButton, 'radioButton_transv_shear_y')
        self.radioButton_transv_shear_z = self.findChild(QRadioButton, 'radioButton_transv_shear_z')
        self.radioButton_torsional_shear = self.findChild(QRadioButton, 'radioButton_torsional_shear')

        self.radioButton_normal_axial.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_hoop.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_torsional_shear.clicked.connect(self.radioButtonEvent)

        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_transv_shear_y = self.radioButton_transv_shear_y.isChecked()
        self.flag_transv_shear_z = self.radioButton_transv_shear_z.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, 
                    self.flag_hoop, self.flag_transv_shear_y, self.flag_transv_shear_z, self.flag_torsional_shear]

        self.treeWidget_list_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_list_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.load()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _update_damping_effect(self):
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()

    def radioButtonEvent(self):
        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_transv_shear_y = self.radioButton_transv_shear_y.isChecked()
        self.flag_transv_shear_z = self.radioButton_transv_shear_z.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, 
                    self.flag_hoop, self.flag_transv_shear_y, self.flag_transv_shear_z, self.flag_torsional_shear]
        
    def check(self):
        if self.lineEdit_selected_frequency.text() == "":
            error("Select a frequency")
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            if frequency_selected in self.frequencies:
                self.selected_index = self.frequency_to_index[frequency_selected]
            else:
                error("  You typed an invalid frequency!  ")
                return
            self.get_stress_data()
        # self.close()

    def get_stress_data(self):
        self.type_labels = np.array([0,1,2,3,4,5,6])
        _labes = np.array(["Normal axial", "Normal bending y", "Normal bending z", "Hoop", "Transversal shear y", "Transversal shear z", "Torsional shear"])
        selected_stress = self.type_labels[self.mask][0]
        if self.stress_data == []:
            self.stress_data = self.solve.stress_calculate(self.damping, pressure_external = 0, damping_flag = self.flag_damping_effect)
        self.stress_field = np.real([array[selected_stress, self.selected_index] for array in self.stress_data.values()])
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses(np.min(self.stress_field), np.max(self.stress_field), _labes[self.mask][0])
        self.opv.changeAndPlotAnalysis(self.selected_index, stressColor=True)

    def load(self):
        for frequency in self.frequencies:
            new = QTreeWidgetItem([str(frequency)])
            self.treeWidget_list_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.check()

    def confirm_button(self):
        self.check()