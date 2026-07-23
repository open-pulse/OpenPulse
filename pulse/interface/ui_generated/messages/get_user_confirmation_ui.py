# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_user_confirmation.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(360, 240)
        Dialog.setMinimumSize(QSize(300, 240))
        Dialog.setMaximumSize(QSize(650, 600))
        Dialog.setModal(True)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(630, 42))
        font = QFont()
        font.setPointSize(8)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 42))
        self.label_title.setMaximumSize(QSize(630, 42))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_title.setFont(font1)
        self.label_title.setStyleSheet(u"")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setLineWidth(1)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.label_message = QLabel(Dialog)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setMinimumSize(QSize(0, 0))
        self.label_message.setMaximumSize(QSize(630, 500))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_message.setFont(font2)
        self.label_message.setFrameShape(QFrame.Box)
        self.label_message.setFrameShadow(QFrame.Raised)
        self.label_message.setLineWidth(1)
        self.label_message.setTextFormat(Qt.AutoText)
        self.label_message.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_message, 1, 0, 1, 1)

        self.frame_tile = QFrame(Dialog)
        self.frame_tile.setObjectName(u"frame_tile")
        self.frame_tile.setMinimumSize(QSize(0, 52))
        self.frame_tile.setMaximumSize(QSize(630, 52))
        self.frame_tile.setSizeIncrement(QSize(0, 0))
        self.frame_tile.setFrameShape(QFrame.NoFrame)
        self.frame_tile.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_tile)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 0)
        self.pushButton_rightButton = QPushButton(self.frame_tile)
        self.pushButton_rightButton.setObjectName(u"pushButton_rightButton")
        self.pushButton_rightButton.setMinimumSize(QSize(100, 30))
        self.pushButton_rightButton.setMaximumSize(QSize(100, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_rightButton.setFont(font3)
        self.pushButton_rightButton.setStyleSheet(u"")
        self.pushButton_rightButton.setAutoDefault(True)
        self.pushButton_rightButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_rightButton, 0, 3, 1, 1)

        self.pushButton_leftButton = QPushButton(self.frame_tile)
        self.pushButton_leftButton.setObjectName(u"pushButton_leftButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_leftButton.sizePolicy().hasHeightForWidth())
        self.pushButton_leftButton.setSizePolicy(sizePolicy)
        self.pushButton_leftButton.setMinimumSize(QSize(100, 30))
        self.pushButton_leftButton.setMaximumSize(QSize(100, 30))
        self.pushButton_leftButton.setFont(font3)
        self.pushButton_leftButton.setStyleSheet(u"")
        self.pushButton_leftButton.setAutoDefault(False)
        self.pushButton_leftButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_leftButton, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_tile, 2, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_leftButton, self.pushButton_rightButton)

        self.retranslateUi(Dialog)

        self.pushButton_rightButton.setDefault(False)
        self.pushButton_leftButton.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Message", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.label_message.setText(QCoreApplication.translate("Dialog", u"< message >", None))
        self.pushButton_rightButton.setText(QCoreApplication.translate("Dialog", u"Right button", None))
        self.pushButton_leftButton.setText(QCoreApplication.translate("Dialog", u"Left button", None))
    # retranslateUi



class GetUserConfirmation_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - label_message: QLabel
                - frame_tile: QFrame
                    - (Layout): QGridLayout
                            - pushButton_rightButton: QPushButton
                            - pushButton_leftButton: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
