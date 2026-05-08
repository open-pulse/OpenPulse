# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cross_section_plotter.ui'
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
        Dialog.resize(700, 800)
        Dialog.setMinimumSize(QSize(700, 800))
        Dialog.setMaximumSize(QSize(700, 800))
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_title)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_14 = QLabel(self.frame_title)
        self.label_14.setObjectName(u"label_14")
        font = QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 2)

        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setMinimumSize(QSize(0, 0))
        self.frame_lower.setFrameShape(QFrame.Box)
        self.frame_lower.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_lower)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_plot = QWidget(self.frame_lower)
        self.widget_plot.setObjectName(u"widget_plot")
        self.widget_plot.setMinimumSize(QSize(660, 660))
        self.widget_plot.setMaximumSize(QSize(660, 660))

        self.gridLayout_2.addWidget(self.widget_plot, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_lower, 1, 0, 1, 2)

        self.frame_bottom = QFrame(Dialog)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setEnabled(True)
        self.frame_bottom.setMinimumSize(QSize(0, 40))
        self.frame_bottom.setMaximumSize(QSize(16777215, 40))
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_bottom)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.close_button = QPushButton(self.frame_bottom)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setEnabled(True)
        self.close_button.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.close_button.setFont(font1)

        self.gridLayout_4.addWidget(self.close_button, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_bottom, 2, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Cross-section plotter", None))
        self.close_button.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi



class CrossSectionPlotter_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_14: QLabel
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - widget_plot: QWidget
                - frame_bottom: QFrame
                    - (Layout): QGridLayout
                            - close_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
