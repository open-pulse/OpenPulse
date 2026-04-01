# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_open_pulse.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 400)
        Dialog.setMinimumSize(QSize(500, 0))
        Dialog.setMaximumSize(QSize(500, 16777215))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(8)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 8)
        self.label_main_info = QLabel(self.frame)
        self.label_main_info.setObjectName(u"label_main_info")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        self.label_main_info.setFont(font)
        self.label_main_info.setAlignment(Qt.AlignCenter)
        self.label_main_info.setWordWrap(True)
        self.label_main_info.setMargin(10)

        self.gridLayout_2.addWidget(self.label_main_info, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 40))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_repository = QPushButton(self.frame_2)
        self.pushButton_repository.setObjectName(u"pushButton_repository")
        self.pushButton_repository.setMinimumSize(QSize(200, 30))
        self.pushButton_repository.setMaximumSize(QSize(200, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_repository.setFont(font1)
        self.pushButton_repository.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_repository, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 3, 0, 1, 3)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u":/icons/MOPT.PNG"))
        self.label_2.setScaledContents(True)

        self.gridLayout.addWidget(self.label_2, 4, 0, 2, 2)

        self.label_version_information = QLabel(Dialog)
        self.label_version_information.setObjectName(u"label_version_information")
        self.label_version_information.setMinimumSize(QSize(0, 25))
        self.label_version_information.setMaximumSize(QSize(16777215, 25))
        self.label_version_information.setFont(font1)
        self.label_version_information.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_version_information, 4, 2, 1, 1)

        self.label_licensing_information = QLabel(Dialog)
        self.label_licensing_information.setObjectName(u"label_licensing_information")
        self.label_licensing_information.setMinimumSize(QSize(0, 25))
        self.label_licensing_information.setMaximumSize(QSize(16777215, 25))
        self.label_licensing_information.setFont(font1)
        self.label_licensing_information.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_licensing_information, 5, 2, 1, 1)

        self.logo_label = QLabel(Dialog)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setMaximumSize(QSize(16777215, 48))
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.logo_label, 0, 0, 1, 3)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 25))
        self.label_3.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About OpenPulse", None))
        self.label_main_info.setText(QCoreApplication.translate("Dialog", u"Main_information", None))
        self.pushButton_repository.setText(QCoreApplication.translate("Dialog", u"Go to OpenPulse repository", None))
        self.label_2.setText("")
        self.label_version_information.setText(QCoreApplication.translate("Dialog", u"Version Information", None))
        self.label_licensing_information.setText(QCoreApplication.translate("Dialog", u"Licensing Information", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Open Source Software for Pulsation Analysis of Pipeline Systems", None))
    # retranslateUi



class AboutOpenPulse_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_main_info: QLabel
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_repository: QPushButton
                - line: Line
                - label_2: QLabel
                - label_version_information: QLabel
                - label_licensing_information: QLabel
                - logo_label: QLabel
                - label_3: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
