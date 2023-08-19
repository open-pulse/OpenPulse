from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

class PlotDisplacementFieldInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui/plots_/results_/structural_/plotDisplacementFieldInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.project = project
        
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies_vector()

    def _reset_variables(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None

    def _define_qt_variables(self):
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')

    def _create_connections(self):
        self.pushButton.clicked.connect(self.check_selected_frequency)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_selected_frequency()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check_selected_frequency(self):
        if self.lineEdit.text() == "":
            window_title = "WARNING"
            title = "Additional action required to plot the results"
            message = "You should select a frequency from the available list \n\n"
            message += "before trying to plot the displacement/rotation field."
            PrintMessageInput([title, message, window_title])
            return
        else:
            frequency_selected = float(self.lineEdit.text())
            if frequency_selected in self.frequencies:
                self.frequency = self.frequency_to_index[frequency_selected]
            
        self.close()

    def load_frequencies_vector(self):

        if self.project.analysis_ID == 7:
            self.frequency = 0
            return

        for frequency in self.frequencies:
            new = QTreeWidgetItem([str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget.addTopLevelItem(new)

        self.exec()

    def on_click_item(self, item):
        self.lineEdit.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit.setText(item.text(0))
        self.check_selected_frequency()