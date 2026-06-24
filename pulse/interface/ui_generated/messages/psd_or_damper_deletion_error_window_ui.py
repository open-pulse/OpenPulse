# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'psd_or_damper_deletion_error_window.ui'
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
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(333, 264)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(650, 42))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 0))
        self.label_title.setMaximumSize(QSize(620, 36))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"")
        self.label_title.setFrameShape(QFrame.NoFrame)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setMargin(6)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_message = QFrame(Dialog)
        self.frame_message.setObjectName(u"frame_message")
        font1 = QFont()
        font1.setPointSize(10)
        self.frame_message.setFont(font1)
        self.frame_message.setFrameShape(QFrame.Box)
        self.frame_message.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_message)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(self.frame_message)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 307, 136))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_message = QLabel(self.scrollAreaWidgetContents)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setMinimumSize(QSize(0, 0))
        self.label_message.setMaximumSize(QSize(650, 1200))
        font2 = QFont()
        font2.setPointSize(11)
        self.label_message.setFont(font2)
        self.label_message.setFrameShape(QFrame.NoFrame)
        self.label_message.setFrameShadow(QFrame.Raised)
        self.label_message.setTextFormat(Qt.AutoText)
        self.label_message.setAlignment(Qt.AlignCenter)
        self.label_message.setWordWrap(True)
        self.label_message.setMargin(2)
        self.label_message.setIndent(-1)

        self.gridLayout_5.addWidget(self.label_message, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_message, 1, 0, 1, 1)

        self.frame_button = QFrame(Dialog)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(650, 48))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_button)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_button)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(80, 28))
        self.pushButton_exit.setMaximumSize(QSize(80, 28))
        self.pushButton_exit.setSizeIncrement(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 2, 1, 1, 1)

        self.pushButton_open_editor = QPushButton(self.frame_button)
        self.pushButton_open_editor.setObjectName(u"pushButton_open_editor")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_editor.sizePolicy().hasHeightForWidth())
        self.pushButton_open_editor.setSizePolicy(sizePolicy)
        self.pushButton_open_editor.setMinimumSize(QSize(80, 28))
        self.pushButton_open_editor.setMaximumSize(QSize(100, 28))
        self.pushButton_open_editor.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButton_open_editor, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_button, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_exit.setDefault(False)
        self.pushButton_open_editor.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Error", None))
        self.label_message.setText("")
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_open_editor.setText(QCoreApplication.translate("Dialog", u"Open editor", None))
    # retranslateUi



class PsdOrDamperDeletionErrorWindow_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_message: QFrame
                    - (Layout): QGridLayout
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - label_message: QLabel
                - frame_button: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_open_editor: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
