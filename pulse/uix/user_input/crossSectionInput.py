from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.utils import error

from pulse.preprocessing.cross_section import CrossSection

class CrossSectionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/crossSectionInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

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

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()
        self.currentTab = self.tabWidget.currentIndex()

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def check(self):
        if self.currentTab == 0 or True:
            #Pipe
            if self.lineEdit_outerDiameter.text() == "":
                error("Insert some value (OUTER DIAMETER)!", title="INPUT CROSS-SECTION ERROR")
                return
            elif self.lineEdit_thickness.text() == "":
                error("Insert some value (THICKENSS)!", title="INPUT CROSS-SECTION ERROR")
                return
            elif self.lineEdit_offset_y.text() == "":
                # error("Insert some value (Offset y)!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                pass
            elif self.lineEdit_offset_z.text() == "":
                # error("Insert some value (Offset z)!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                pass

            outerDiameter = 0
            thickness = 0
            offset_y = 0
            offset_z = 0

            try:
                outerDiameter = float(self.lineEdit_outerDiameter.text())
            except Exception:
                error("Wrong input for OUTER DIAMETER!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            try:
                thickness = float(self.lineEdit_thickness.text())
            except Exception:
                error("Wrong input for THICKENSS!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return

            try:
                offset_y = float(self.lineEdit_offset_y.text())
            except Exception:
                error("Wrong input for OFFSET Y!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            try:
                offset_z = float(self.lineEdit_offset_z.text())
            except Exception:
                error("Wrong input for OFFSET Z!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
        
            if outerDiameter<thickness:
                error("The OUTER DIAMETER must be greater than THICKNESS!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return

            elif thickness == 0.0:
                error("The THICKNESS must be greater than zero!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            elif abs(offset_y) > (outerDiameter/2):
                error("The OFFSET_Y must be less than external radius!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
            
            elif abs(offset_z) > (outerDiameter/2):
                error("The OFFSET_Y must be less than external radius!", title=">>> INPUT CROSS-SECTION ERROR <<<")
                return
                      
            self.section = CrossSection(outerDiameter, thickness, offset_y=offset_y, offset_z=offset_z)
            self.close()
        else:
            pass
