from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.cross_section import CrossSection

class CrossSectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/crossSectionInput.ui', self)

        self.section = None
        self.flagAll = False
        self.flagEntity = False
        self.currentTab = 0

        self.lineEdit_outerDiameter = self.findChild(QLineEdit, 'lineEdit_outerDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')

        self.lineEdit_area = self.findChild(QLineEdit, 'lineEdit_area')
        self.lineEdit_iyy = self.findChild(QLineEdit, 'lineEdit_iyy')
        self.lineEdit_izz = self.findChild(QLineEdit, 'lineEdit_izz')
        self.lineEdit_iyz = self.findChild(QLineEdit, 'lineEdit_iyz')

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()
        self.currentTab = self.tabWidget.currentIndex()

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

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def check(self):
        if self.currentTab == 0 or True:
            #Pipe
            if self.lineEdit_outerDiameter.text() == "":
                self.error("Insert some value (Outer Diameter)!", "Pipe Error")
                return
            elif self.lineEdit_thickness.text() == "":
                pass
            elif self.lineEdit_offset_y.text() == "":
                pass
            elif self.lineEdit_offset_z.text() == "":
                pass

            outerDiameter = 0
            thickness = 0
            offset_y = 0
            offset_z = 0
            try:
                outerDiameter = float(self.lineEdit_outerDiameter.text())
                thickness = float(self.lineEdit_thickness.text())
            except Exception:
                self.error("Wrong input!", "Pipe Error")
                return

            self.section = CrossSection(outerDiameter, thickness)
            self.close()

        else:
            pass