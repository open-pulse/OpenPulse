from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class PlotDisplacementFieldInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/structural_/plot_displacement_field_for_harmonic_analysis.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.project = project
        self.opv.setInputObject(self)
        
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        if self.load_frequencies_vector():
            self.exec()


    def _reset_variables(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None


    def _define_qt_variables(self):
        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        self.radioButton_absolute = self.findChild(QRadioButton, 'radioButton_absolute')
        self.radioButton_real_part_ux = self.findChild(QRadioButton, 'radioButton_real_part_ux')
        self.radioButton_real_part_uy = self.findChild(QRadioButton, 'radioButton_real_part_uy')
        self.radioButton_real_part_uz = self.findChild(QRadioButton, 'radioButton_real_part_uz')
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')


    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.check_selected_frequency)
        self.radioButton_real_part_ux.clicked.connect(self.radioButton_event)
        self.radioButton_real_part_uy.clicked.connect(self.radioButton_event)
        self.radioButton_real_part_uz.clicked.connect(self.radioButton_event)
        self.radioButton_absolute.clicked.connect(self.radioButton_event)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)


    def radioButton_event(self):
        if self.lineEdit_selected_frequency.text() != "":
            self.check_selected_frequency()


    def check_selected_frequency(self):
        if self.lineEdit_selected_frequency.text() == "":
            window_title = "WARNING"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list \n\n"
            message += "before trying to plot the displacement/rotation field."
            PrintMessageInput([title, message, window_title])
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            if frequency_selected in self.frequencies:
                self.frequency = self.frequency_to_index[frequency_selected]
                scaling_setup = {   "absolute" : self.radioButton_absolute.isChecked(),
                                    "real_ux" : self.radioButton_real_part_ux.isChecked(),
                                    "real_uy" : self.radioButton_real_part_uy.isChecked(),
                                    "real_uz" : self.radioButton_real_part_uz.isChecked()   }
                self.opv.plot_displacement_field(self.frequency, scaling_setup)


    def load_frequencies_vector(self):

        if self.project.analysis_ID == 7:
            self.plot_displacement_for_static_analysis()
            return False
    
        else:
    
            for index, frequency in enumerate(self.frequencies):
                new = QTreeWidgetItem([str(index+1), str(frequency)])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_frequencies.addTopLevelItem(new)
            return True


    def plot_displacement_for_static_analysis(self):
        self.frequency = 0
        scaling_setup = {   "absolute" : self.radioButton_absolute.isChecked(),
                            "real_ux" : self.radioButton_real_part_ux.isChecked(),
                            "real_uy" : self.radioButton_real_part_uy.isChecked(),
                            "real_uz" : self.radioButton_real_part_uz.isChecked()   }
        self.opv.plot_displacement_field(self.frequency, scaling_setup)


    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))


    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.check_selected_frequency()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_selected_frequency()
        elif event.key() == Qt.Key_Escape:
            self.close()