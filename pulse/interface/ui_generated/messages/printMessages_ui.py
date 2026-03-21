# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'printMessages.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 400)
        Dialog.setMinimumSize(QSize(600, 400))
        Dialog.setMaximumSize(QSize(600, 400))
        self.frame_message = QFrame(Dialog)
        self.frame_message.setObjectName(u"frame_message")
        self.frame_message.setGeometry(QRect(0, 52, 600, 348))
        self.frame_message.setMinimumSize(QSize(600, 348))
        self.frame_message.setMaximumSize(QSize(600, 348))
        self.frame_message.setFrameShape(QFrame.Box)
        self.frame_message.setFrameShadow(QFrame.Plain)
        self._label_message = QLabel(self.frame_message)
        self._label_message.setObjectName(u"_label_message")
        self._label_message.setGeometry(QRect(10, 12, 580, 280))
        self._label_message.setMinimumSize(QSize(580, 280))
        self._label_message.setMaximumSize(QSize(580, 280))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        self._label_message.setFont(font)
        self._label_message.setFrameShape(QFrame.StyledPanel)
        self._label_message.setFrameShadow(QFrame.Sunken)
        self._label_message.setTextFormat(Qt.AutoText)
        self._label_message.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self._label_message.setWordWrap(True)
        self._label_message.setMargin(10)
        self._label_message.setIndent(-1)
        self.pushButton_close = QPushButton(self.frame_message)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setGeometry(QRect(250, 302, 100, 35))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(False)
        self.pushButton_close.setFont(font1)
        self.pushButton_close.setFlat(False)
        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(0, 0, 600, 53))
        self.frame_4.setMinimumSize(QSize(600, 0))
        self.frame_4.setMaximumSize(QSize(600, 16777215))
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Plain)
        self.frame = QFrame(self.frame_4)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 8, 580, 38))
        self.frame.setMinimumSize(QSize(580, 0))
        self.frame.setMaximumSize(QSize(580, 16777215))
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Raised)
        self._label_title = QLabel(self.frame)
        self._label_title.setObjectName(u"_label_title")
        self._label_title.setGeometry(QRect(4, 0, 573, 38))
        self._label_title.setMinimumSize(QSize(573, 0))
        self._label_title.setMaximumSize(QSize(573, 16777215))
        self._label_title.setFont(font)
        self._label_title.setTextFormat(Qt.AutoText)
        self._label_title.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self._label_message.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">message</span></p></body></html>", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self._label_title.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">TITLE</span></p></body></html>", None))
    # retranslateUi



class Printmessages_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - frame_message: QFrame
            - _label_message: QLabel
            - pushButton_close: QPushButton
        - frame_4: QFrame
            - frame: QFrame
                - _label_title: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
