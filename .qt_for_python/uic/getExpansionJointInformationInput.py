# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\OpenPulse\data\user_input\ui\Model\Info\getExpansionJointInformationInput.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(702, 522)
        Dialog.setMinimumSize(QtCore.QSize(702, 522))
        Dialog.setMaximumSize(QtCore.QSize(702, 522))
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 702, 39))
        self.frame.setMinimumSize(QtCore.QSize(702, 0))
        self.frame.setMaximumSize(QtCore.QSize(702, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.title_label = QtWidgets.QLabel(self.frame)
        self.title_label.setGeometry(QtCore.QRect(100, 4, 502, 33))
        self.title_label.setMinimumSize(QtCore.QSize(502, 33))
        self.title_label.setMaximumSize(QtCore.QSize(502, 33))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setTextFormat(QtCore.Qt.AutoText)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 38, 702, 484))
        self.frame_2.setMinimumSize(QtCore.QSize(702, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(702, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.pushButton_close = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_close.setGeometry(QtCore.QRect(300, 440, 102, 32))
        self.pushButton_close.setMinimumSize(QtCore.QSize(102, 32))
        self.pushButton_close.setMaximumSize(QtCore.QSize(102, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setObjectName("pushButton_close")
        self.treeWidget_group_info = QtWidgets.QTreeWidget(self.frame_2)
        self.treeWidget_group_info.setGeometry(QtCore.QRect(10, 16, 682, 412))
        self.treeWidget_group_info.setMinimumSize(QtCore.QSize(682, 370))
        self.treeWidget_group_info.setMaximumSize(QtCore.QSize(382, 430))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.treeWidget_group_info.setFont(font)
        self.treeWidget_group_info.setTextElideMode(QtCore.Qt.ElideRight)
        self.treeWidget_group_info.setIndentation(0)
        self.treeWidget_group_info.setUniformRowHeights(False)
        self.treeWidget_group_info.setAnimated(False)
        self.treeWidget_group_info.setAllColumnsShowFocus(False)
        self.treeWidget_group_info.setHeaderHidden(False)
        self.treeWidget_group_info.setColumnCount(2)
        self.treeWidget_group_info.setObjectName("treeWidget_group_info")
        self.treeWidget_group_info.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.treeWidget_group_info.headerItem().setFont(0, font)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.treeWidget_group_info.headerItem().setFont(1, font)
        self.treeWidget_group_info.header().setVisible(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Information of selected group"))
        self.title_label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Information of selected expansion joint</p></body></html>"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.treeWidget_group_info.headerItem().setText(0, _translate("Dialog", "Line ID"))
        self.treeWidget_group_info.headerItem().setText(1, _translate("Dialog", "Parameters [length, effective diameter, mass, axial locking ε,  rods, kx, kyz, krx, kryz]"))