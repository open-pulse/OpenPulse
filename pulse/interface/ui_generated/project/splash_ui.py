# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QProgressBar, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 280)
        Form.setMinimumSize(QSize(500, 280))
        Form.setMaximumSize(QSize(500, 280))
        Form.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.506, y1:0, x2:0.494318, y2:1, stop:0 rgba(155, 155, 155, 207), stop:0.823864 rgba(0, 0, 0, 203), stop:1 rgba(0, 0, 0, 230));")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMaximumSize(QSize(16777215, 180))
        self.frame_main.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.logo_label = QLabel(self.frame_main)
        self.logo_label.setObjectName(u"logo_label")
        font = QFont()
        font.setFamilies([u"Bauhaus 93"])
        font.setPointSize(27)
        font.setBold(False)
        font.setKerning(False)
        self.logo_label.setFont(font)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.logo_label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 1, 1, 1)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setValue(5)
        self.progressBar.setTextVisible(False)

        self.gridLayout_2.addWidget(self.progressBar, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 3, 1, 1, 1)

        self.label_loading = QLabel(Form)
        self.label_loading.setObjectName(u"label_loading")
        self.label_loading.setMaximumSize(QSize(16777215, 32))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        self.label_loading.setFont(font1)
        self.label_loading.setStyleSheet(u"background-color: rgba(0,0,0,0);")
        self.label_loading.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_loading, 2, 1, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 20))
        self.frame_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.logo_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:60pt; color:#2d6ebe;\">O</span><span style=\" font-size:60pt; color:#b9b9b9;\">pen</span><span style=\" font-size:60pt; color:#2d6ebe;\">P</span><span style=\" font-size:60pt; color:#b9b9b9;\">ulse</span></p></body></html>", None))
        self.label_loading.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-style:italic; color:#b9b9b9;\">loading application...</span></p></body></html>", None))
    # retranslateUi



class Splash_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - logo_label: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - progressBar: QProgressBar
                - label_loading: QLabel
                - frame_2: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
