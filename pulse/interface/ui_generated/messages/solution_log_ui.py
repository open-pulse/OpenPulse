# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solution_log.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QProgressBar, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(300, 240)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(300, 240))
        Dialog.setMaximumSize(QSize(600, 450))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(600, 42))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_message = QFrame(Dialog)
        self.frame_message.setObjectName(u"frame_message")
        self.frame_message.setMinimumSize(QSize(0, 0))
        self.frame_message.setMaximumSize(QSize(600, 400))
        self.frame_message.setFrameShape(QFrame.Box)
        self.frame_message.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_message)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_message = QLabel(self.frame_message)
        self.label_message.setObjectName(u"label_message")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_message.setFont(font1)
        self.label_message.setStyleSheet(u"")
        self.label_message.setAlignment(Qt.AlignCenter)
        self.label_message.setWordWrap(True)
        self.label_message.setMargin(6)

        self.gridLayout_2.addWidget(self.label_message, 0, 0, 1, 1)

        self.frame_progress_bar = QFrame(self.frame_message)
        self.frame_progress_bar.setObjectName(u"frame_progress_bar")
        self.frame_progress_bar.setMaximumSize(QSize(16777215, 40))
        self.frame_progress_bar.setFrameShape(QFrame.NoFrame)
        self.frame_progress_bar.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_progress_bar)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.progress_bar_timer = QProgressBar(self.frame_progress_bar)
        self.progress_bar_timer.setObjectName(u"progress_bar_timer")
        self.progress_bar_timer.setMaximumSize(QSize(240, 16777215))
        self.progress_bar_timer.setStyleSheet(u"QProgressBar { border-radius: 4px;  background-color: rgb(255,255,255);  border-width: 1px}\n"
"QProgressBar::chunk {border-radius: 4px;   background-color:  rgb(20,150,255);  border-width: 1px }")
        self.progress_bar_timer.setValue(0)
        self.progress_bar_timer.setTextVisible(False)

        self.gridLayout_4.addWidget(self.progress_bar_timer, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_progress_bar, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_message, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Run analysis", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Solution finished", None))
        self.label_message.setText(QCoreApplication.translate("Dialog", u"Solution in progress\u2026", None))
    # retranslateUi



class SolutionLog_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_message: QFrame
                    - (Layout): QGridLayout
                            - label_message: QLabel
                            - frame_progress_bar: QFrame
                                - (Layout): QGridLayout
                                        - progress_bar_timer: QProgressBar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
