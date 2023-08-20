from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path
import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class PlotStressField(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/plots_/results_/structural_/plot_stress_field_for_harmonic_analysis.ui'), self)

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
        self.frequencies = project.frequencies
        self.dict_frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.selected_index = None
        self.update_damping = False

        self.stress_field = []
        self.stress_data = []

        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", "Normal bending y", "Normal bending z", "Hoop", "Torsional shear", "Transversal shear xy", "Transversal shear xz"])

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
        self.radioButton_transv_shear_xy = self.findChild(QRadioButton, 'radioButton_transv_shear_xy')
        self.radioButton_transv_shear_xz = self.findChild(QRadioButton, 'radioButton_transv_shear_xz')
        self.radioButton_torsional_shear = self.findChild(QRadioButton, 'radioButton_torsional_shear')

        self.radioButton_normal_axial.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_hoop.clicked.connect(self.radioButtonEvent)
        self.radioButton_torsional_shear.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xy.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xz.clicked.connect(self.radioButtonEvent)

        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, self.flag_hoop,
                    self.flag_torsional_shear, self.flag_transv_shear_xy, self.flag_transv_shear_xz]

        self.treeWidget_list_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_list_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.load()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _update_damping_effect(self):
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()
        self.update_damping = True

    def radioButtonEvent(self):
        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, self.flag_hoop,
                    self.flag_torsional_shear, self.flag_transv_shear_xy, self.flag_transv_shear_xz]
        
    def check(self):
        window_title = "WARNING"
        if self.lineEdit_selected_frequency.text() == "":
            title = "Aditional action required"
            message = "Select a frequency from the available list \n"
            message += "of frequencies to continue."
            PrintMessageInput([title, message, window_title])
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
            #     PrintMessageInput([title, message, window_title])
            #     return

    def get_stress_data(self):

        self.stress_label = self.labels[self.mask][0]
        self.stress_key = self.keys[self.mask][0]

        if self.stress_data == [] or self.update_damping:
            self.stress_data = self.solve.stress_calculate( pressure_external = 0, 
                                                            damping_flag = self.flag_damping_effect )
            self.update_damping = False
            
        self.stress_field = { key:array[self.stress_key, self.selected_index] for key, array in self.stress_data.items() }
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses( np.min(list(self.stress_field.values())), 
                                                np.max(list(self.stress_field.values())), 
                                                self.stress_label )
        self.opv.changeAndPlotAnalysis(self.selected_index, stress_field_plot=True)

    def load(self):
        for frequency in self.frequencies:
            new = QTreeWidgetItem([str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_list_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.check()

    def confirm_button(self):
        self.check()