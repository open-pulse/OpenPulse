# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\OpenPulse\data\user_input\ui\Project\getDoubleConfirmationInput.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 300)
        Dialog.setMinimumSize(QtCore.QSize(600, 300))
        Dialog.setMaximumSize(QtCore.QSize(600, 300))
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 52, 600, 248))
        self.frame_2.setMinimumSize(QtCore.QSize(600, 248))
        self.frame_2.setMaximumSize(QtCore.QSize(600, 248))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.QLabel_message = QtWidgets.QLabel(self.frame_2)
        self.QLabel_message.setGeometry(QtCore.QRect(10, 12, 580, 180))
        self.QLabel_message.setMinimumSize(QtCore.QSize(580, 180))
        self.QLabel_message.setMaximumSize(QtCore.QSize(580, 180))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.QLabel_message.setFont(font)
        self.QLabel_message.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.QLabel_message.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.QLabel_message.setTextFormat(QtCore.Qt.AutoText)
        self.QLabel_message.setAlignment(QtCore.Qt.AlignCenter)
        self.QLabel_message.setObjectName("QLabel_message")
        self.pushButton_confirm = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_confirm.setGeometry(QtCore.QRect(370, 202, 100, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_confirm.setFont(font)
        self.pushButton_confirm.setDefault(False)
        self.pushButton_confirm.setFlat(False)
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.pushButton_cancel = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_cancel.setGeometry(QtCore.QRect(138, 202, 100, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setDefault(False)
        self.pushButton_cancel.setFlat(False)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.frame_4 = QtWidgets.QFrame(Dialog)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 600, 53))
        self.frame_4.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(600, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.frame = QtWidgets.QFrame(self.frame_4)
        self.frame.setGeometry(QtCore.QRect(10, 8, 580, 38))
        self.frame.setMinimumSize(QtCore.QSize(580, 0))
        self.frame.setMaximumSize(QtCore.QSize(580, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.QLabel_title = QtWidgets.QLabel(self.frame)
        self.QLabel_title.setGeometry(QtCore.QRect(40, 4, 500, 31))
        self.QLabel_title.setMinimumSize(QtCore.QSize(500, 10))
        self.QLabel_title.setMaximumSize(QtCore.QSize(500, 185))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.QLabel_title.setFont(font)
        self.QLabel_title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.QLabel_title.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.QLabel_title.setTextFormat(QtCore.Qt.AutoText)
        self.QLabel_title.setAlignment(QtCore.Qt.AlignCenter)
        self.QLabel_title.setObjectName("QLabel_title")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Double confirmation"))
        self.QLabel_message.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Are you sure you want to reset the project data?</span></p></body></html>"))
        self.pushButton_confirm.setText(_translate("Dialog", "Confirm"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))
        self.QLabel_title.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">CHANGE ELEMENT SIZE</span></p></body></html>"))