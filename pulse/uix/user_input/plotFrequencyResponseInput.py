from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.postprocessing.plot_data import get_frf
import matplotlib.pyplot as plt
import numpy as np

class PlotFrequencyResponseInput(QDialog):
    def __init__(self, mesh, analyseMethod, frequencies, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotFrequencyResponseInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.mesh = mesh
        self.analyseMethod = analyseMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0

        self.localDof = 0

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.checkBox_ux = self.findChild(QCheckBox, 'checkBox_ux')
        self.checkBox_uy = self.findChild(QCheckBox, 'checkBox_uy')
        self.checkBox_uz = self.findChild(QCheckBox, 'checkBox_uz')
        self.checkBox_rx = self.findChild(QCheckBox, 'checkBox_rx')
        self.checkBox_ry = self.findChild(QCheckBox, 'checkBox_ry')
        self.checkBox_rz = self.findChild(QCheckBox, 'checkBox_rz')

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            nodes = list(map(int, tokens))
            if len(nodes) == 1:
                self.nodeID = nodes[0]
            else:
                self.error("Multiple Node IDs", "Error Node ID's")
                return
        except Exception:
            self.error("Wrong input for Node ID's!", "Error Node ID's")
            return


        self.localDof = 0
        if self.checkBox_ux.isChecked():
            self.localDof = 1

        if self.checkBox_uy.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 2
        
        if self.checkBox_uz.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 3

        if self.checkBox_rx.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 4

        if self.checkBox_ry.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 5

        if self.checkBox_rz.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 6
        
        self.plot()

    def plot(self):
        gr = get_frf(self.mesh, self.solution, self.nodeID, self.localDof)

        fig = plt.figure(figsize=[10,6])
        ax = fig.add_subplot(1,1,1)
        plt.semilogy(self.frequencies, np.abs(gr), color = [1,0,0], linewidth=3)
        ax.set_title(('FRF: {} Method').format(self.analyseMethod), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
        ax.set_ylabel(("FRF's magnitude [m/N]"), fontsize = 16, fontweight = 'bold')
        method = '{} - OpenPulse'.format(self.analyseMethod)
        ax.legend([method])
        plt.show()