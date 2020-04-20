from PyQt5.QtWidgets import QDialog, QPushButton, QTreeWidget, QTreeWidgetItem, QDialogButtonBox, QMessageBox
from pulse.uix.user_input.materialInput import MaterialInput
from os.path import basename
import numpy as np
from PyQt5 import uic

class FrequencyList(QDialog):
    def __init__(self, frequency_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frequency_list = frequency_list
        self.current_item = None
        uic.loadUi('pulse/uix/user_input/ui/frequencyList.ui', self)

        self.button_save = self.findChild(QDialogButtonBox, 'button_save')
        self.button_save.accepted.connect(self.accept_frequency)
        self.button_save.rejected.connect(self.reject_frequency)

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.itemClicked.connect(self.on_click_item)

        self.load()

        self.exec_()

    def accept_frequency(self):
        if self.current_item is None:
            self.error("Nenhuma frequencia selecionada")
            return
        self.close()

    def reject_frequency(self):
        self.close()

    def on_click_item(self, item):
        self.current_item = int(item.text(0))

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        #msg_box.setInformativeText('More information')
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def load(self):
        for i in range(len(self.frequency_list)):
            freq = QTreeWidgetItem([str(i), str(self.frequency_list[i])])
            self.treeWidget.addTopLevelItem(freq)