from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class PlotAcousticPressureFieldInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui/Plots/Results/Acoustic/plotAcousticPressureFieldInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project

        self.frequencies = project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None

        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.button)

        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.load()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):
        if self.lineEdit.text() == "":
            window_title = "WARNING"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list \n\n"
            message += "before trying to plot the acoustic pressure field."
            PrintMessageInput([title, message, window_title])
            return
        else:
            frequency_selected = float(self.lineEdit.text())
            self.frequency = self.frequency_to_index[frequency_selected]
            self.opv.changeAndPlotAnalysis(self.frequency, pressure_field_plot=True)
        self.close()

    def load(self):
        for frequency in self.frequencies:
            new = QTreeWidgetItem([str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit.setText(item.text(0))
        self.check()

    def button(self):
        self.check()