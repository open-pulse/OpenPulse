from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np
import configparser

from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class PlotStructuralModeShapeInput(QDialog):
    def __init__(self, opv, natural_frequencies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotStructuralModeShapeInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.natural_frequencies = natural_frequencies
        self.mode_index = None

        self.lineEdit_natural_frequency = self.findChild(QLineEdit, 'lineEdit_natural_frequency')
        self.lineEdit_natural_frequency.setDisabled(True)

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.setColumnWidth(0, 120)
        self.treeWidget.setColumnWidth(1, 140)
        self.treeWidget.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.confirm_selection)
        self.load()
        self.exec_()

    def get_dict_modes_frequencies(self):
        modes = np.arange(1,len(self.natural_frequencies)+1,1)
        self.dict_modes_frequencies = dict(zip(modes, self.natural_frequencies))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):
        if self.lineEdit_natural_frequency.text() == "":
            title = "UNSELECTED NATURAL FREQUENCY"
            message = "Select a natural frequency from list."
            self.text_data = [title, message, window_title2]
            return True
        else:
            try:
                frequency = self.selected_natural_frequency
                self.mode_index = self.natural_frequencies.index(frequency)
            except Exception as error:
                title = "ERROR IN NATURAL FREQUENCY SELECTION"
                message = str(error)
                self.text_data = [title, message, window_title1]
                return True
        return False

    def confirm_selection(self):
        if self.check():
            PrintMessageInput(self.text_data)
            return
        self.complete = True
        self.close()

    def load(self):
        self.get_dict_modes_frequencies()

        for mode, natural_frequency in self.dict_modes_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget.addTopLevelItem(new)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))

    def on_doubleclick_item(self, item):
        natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(natural_frequency))
        self.confirm_selection()