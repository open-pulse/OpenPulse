from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QComboBox, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class MassSpringDamperInput(QDialog):
    def __init__(self, nodes, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/addMassSpringDamperInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.nodes = nodes

        self.mass = None
        self.spring = None
        self.damper = None
        self.nodes_typed = []

        self.input_mass = False
        self.input_spring = False
        self.input_damper = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_mx = self.findChild(QLineEdit, 'lineEdit_mx')
        self.lineEdit_my = self.findChild(QLineEdit, 'lineEdit_my')
        self.lineEdit_mz = self.findChild(QLineEdit, 'lineEdit_mz')
        self.lineEdit_ix = self.findChild(QLineEdit, 'lineEdit_ix')
        self.lineEdit_iy = self.findChild(QLineEdit, 'lineEdit_iy')
        self.lineEdit_iz = self.findChild(QLineEdit, 'lineEdit_iz')

        self.lineEdit_kx = self.findChild(QLineEdit, 'lineEdit_kx')
        self.lineEdit_ky = self.findChild(QLineEdit, 'lineEdit_ky')
        self.lineEdit_kz = self.findChild(QLineEdit, 'lineEdit_kz')
        self.lineEdit_krx = self.findChild(QLineEdit, 'lineEdit_krx')
        self.lineEdit_kry = self.findChild(QLineEdit, 'lineEdit_kry')
        self.lineEdit_krz = self.findChild(QLineEdit, 'lineEdit_krz')

        self.lineEdit_cx = self.findChild(QLineEdit, 'lineEdit_cx')
        self.lineEdit_cy = self.findChild(QLineEdit, 'lineEdit_cy')
        self.lineEdit_cz = self.findChild(QLineEdit, 'lineEdit_cz')
        self.lineEdit_crx = self.findChild(QLineEdit, 'lineEdit_crx')
        self.lineEdit_cry = self.findChild(QLineEdit, 'lineEdit_cry')
        self.lineEdit_crz = self.findChild(QLineEdit, 'lineEdit_crz')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.writeNodes(list_node_ids)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.nodes_typed = list(map(int, tokens))
        except Exception:
            error("Wrong input for Node ID's!", title="Error Node ID's")
            return

        try:
            for node in self.nodes_typed:
                self.nodes[node].external_index
        except:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return
        
        self.checkMass()
        self.checkSpring()
        self.checkDamper()

        if self.input_mass or self.input_spring or self.input_damper:
            self.close()
        else:
            error("You must to input at least one valid value before to confirm the input!", title = " ERROR ")
            return

    def checkDamper(self):
        cx = cy = cz = 0.0
        if self.lineEdit_cx.text() != "":
            if self.isFloat(self.lineEdit_cx.text()):
                cx = float(self.lineEdit_cx.text())
            else:
                error("Wrong input (cx)!", title="Error")
                return False
        
        if self.lineEdit_cy.text() != "":
            if self.isFloat(self.lineEdit_cy.text()):
                cy = float(self.lineEdit_cy.text())
            else:
                error("Wrong input (cy)!", title="Error")
                return False

        if self.lineEdit_cz.text() != "":
            if self.isFloat(self.lineEdit_cz.text()):
                cz = float(self.lineEdit_cz.text())
            else:
                error("Wrong input (cz)!", title="Error")
                return False

        crx = cry = crz = 0.0
        if self.lineEdit_crx.text() != "":
            if self.isFloat(self.lineEdit_crx.text()):
                crx = float(self.lineEdit_crx.text())
            else:
                error("Wrong input (crx)!", title="Error")
                return False
        
        if self.lineEdit_cry.text() != "":
            if self.isFloat(self.lineEdit_cry.text()):
                cry = float(self.lineEdit_cry.text())
            else:
                error("Wrong input (cry)!", title="Error")
                return False

        if self.lineEdit_crz.text() != "":
            if self.isFloat(self.lineEdit_crz.text()):
                crz = float(self.lineEdit_crz.text())
            else:
                error("Wrong input (crz)!", title="Error")
                return False
        
        if cx==cy==cz==crx==cry==crz==0.0:
            return False   
        else:
            self.damper = [cx, cy, cz, crx, cry, crz]
            self.input_damper = True

        return self.input_damper

    def checkSpring(self):

        kx = ky = kz = 0.0
        if self.lineEdit_kx.text() != "":
            if self.isFloat(self.lineEdit_kx.text()):
                kx = float(self.lineEdit_kx.text())
            else:
                error("Wrong input (kx)!", title="Error")
                return False
        
        if self.lineEdit_ky.text() != "":
            if self.isFloat(self.lineEdit_ky.text()):
                ky = float(self.lineEdit_ky.text())
            else:
                error("Wrong input (ky)!", title="Error")
                return False

        if self.lineEdit_kz.text() != "":
            if self.isFloat(self.lineEdit_kz.text()):
                kz = float(self.lineEdit_kz.text())
            else:
                error("Wrong input (kz)!", title="Error")
                return False

        krx = kry = krz = 0.0
        if self.lineEdit_krx.text() != "":
            if self.isFloat(self.lineEdit_krx.text()):
                krx = float(self.lineEdit_krx.text())
            else:
                error("Wrong input (krx)!", title="Error")
                return False
        
        if self.lineEdit_kry.text() != "":
            if self.isFloat(self.lineEdit_kry.text()):
                kry = float(self.lineEdit_kry.text())
            else:
                error("Wrong input (kry)!", title="Error")
                return False

        if self.lineEdit_krz.text() != "":
            if self.isFloat(self.lineEdit_krz.text()):
                krz = float(self.lineEdit_krz.text())
            else:
                error("Wrong input (krz)!", title="Error")
                return False
        
        if kx==ky==kz==krx==kry==krz==0.0:
            return False   
        else:
            self.spring = [kx, ky, kz, krx, kry, krz]
            self.input_spring = True

        return self.input_spring

    def checkMass(self):
        
        mx = my = mz = 0.0
        if self.lineEdit_mx.text() != "":
            if self.isFloat(self.lineEdit_mx.text()):
                mx = float(self.lineEdit_mx.text())
            else:
                error("Wrong input (mx)!", title="Error")
                return False
        
        if self.lineEdit_my.text() != "":
            if self.isFloat(self.lineEdit_my.text()):
                my = float(self.lineEdit_my.text())
            else:
                error("Wrong input (my)!", title="Error")
                return False

        if self.lineEdit_mz.text() != "":
            if self.isFloat(self.lineEdit_mz.text()):
                mz = float(self.lineEdit_mz.text())
            else:
                error("Wrong input (mz)!", title="Error")
                return False

        ix = iy = iz = 0.0
        if self.lineEdit_ix.text() != "":
            if self.isFloat(self.lineEdit_ix.text()):
                ix = float(self.lineEdit_ix.text())
            else:
                error("Wrong input (ix)!", title="Error")
                return False
        
        if self.lineEdit_iy.text() != "":
            if self.isFloat(self.lineEdit_iy.text()):
                iy = float(self.lineEdit_iy.text())
            else:
                error("Wrong input (iy)!", title="Error")
                return False

        if self.lineEdit_iz.text() != "":
            if self.isFloat(self.lineEdit_iz.text()):
                iz = float(self.lineEdit_iz.text())
            else:
                error("Wrong input (iz)!", title="Error")
                return False
        
        if mx==my==mz==ix==iy==iz==0.0:
            return False   
        else:
            self.mass = [mx, my, mz, ix, iy, iz]
            self.input_mass = True

        return self.input_mass

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def isFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False