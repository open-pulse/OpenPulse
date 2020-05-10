from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class AnalyseOutputResultsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analyseOutputResultInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.checkBox_nodal_dof_solution = self.findChild(QCheckBox, 'checkBox_nodal_dof_solution')
        self.checkBox_stress_field = self.findChild(QCheckBox, 'checkBox_stress_field')
        self.checkBox_reactions = self.findChild(QCheckBox, 'checkBox_reactions')
        self.checkBox_reactions_due = self.findChild(QCheckBox, 'checkBox_reactions_due')
        self.checkBox_pressure_field = self.findChild(QCheckBox, 'checkBox_pressure_field')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

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
        self.close()
