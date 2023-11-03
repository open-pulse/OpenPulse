from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class PlotAcousticPressureFieldInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_acoustic_pressure_field_input.ui'), self)

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
        self.load_frequencies_vector()
        self.exec()


    def _reset_variables(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None


    def _define_qt_variables(self):
        self.lineEdit_selected_frequency = self.findChild(QLineEdit, 'lineEdit_selected_frequency')
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        self.radioButton_real_part = self.findChild(QRadioButton, 'radioButton_real_part')
        self.radioButton_absolute = self.findChild(QRadioButton, 'radioButton_absolute')
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')


    def _create_connections(self):
        self.pushButton_plot.clicked.connect(self.check_selected_frequency)
        self.radioButton_absolute.clicked.connect(self.radioButtonEvent)
        self.radioButton_real_part.clicked.connect(self.radioButtonEvent)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)


    def radioButtonEvent(self):
        if self.lineEdit_selected_frequency.text() != "":
            self.check_selected_frequency()


    def check_selected_frequency(self):
        if self.lineEdit_selected_frequency.text() == "":
            window_title = "WARNING"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list \n\n"
            message += "before trying to plot the acoustic pressure field."
            PrintMessageInput([title, message, window_title])
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            self.frequency = self.frequency_to_index[frequency_selected]
            absolute = self.radioButton_absolute.isChecked()
            self.opv.plot_pressure_field(self.frequency, absolute=absolute)


    def load_frequencies_vector(self):
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)


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