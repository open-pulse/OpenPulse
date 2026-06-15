# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesher_setup_input.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(383, 342)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 150))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 2, 4, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 20))
        self.label_2.setMaximumSize(QSize(240, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame_2)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_geometry_tolerance, 2, 2, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 20))
        self.label.setMaximumSize(QSize(240, 16777215))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_element_size = QLineEdit(self.frame_2)
        self.lineEdit_element_size.setObjectName(u"lineEdit_element_size")
        self.lineEdit_element_size.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_element_size, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 3, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 2, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 1, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMaximumSize(QSize(16777215, 38))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.mesher_setup_label = QLabel(self.frame_title)
        self.mesher_setup_label.setObjectName(u"mesher_setup_label")
        self.mesher_setup_label.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setPointSize(11)
        self.mesher_setup_label.setFont(font1)
        self.mesher_setup_label.setFrameShape(QFrame.Shape.NoFrame)
        self.mesher_setup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.mesher_setup_label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 1, 1, 1, 1)

        self.frame_buttons_2 = QFrame(Dialog)
        self.frame_buttons_2.setObjectName(u"frame_buttons_2")
        self.frame_buttons_2.setMinimumSize(QSize(0, 48))
        self.frame_buttons_2.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_buttons_2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(0)
        self.gridLayout_12.setContentsMargins(6, 0, 6, 0)
        self.pushbutton_apply_and_close = QPushButton(self.frame_buttons_2)
        self.pushbutton_apply_and_close.setObjectName(u"pushbutton_apply_and_close")
        self.pushbutton_apply_and_close.setMinimumSize(QSize(72, 30))
        self.pushbutton_apply_and_close.setMaximumSize(QSize(72, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushbutton_apply_and_close.setFont(font2)
        self.pushbutton_apply_and_close.setStyleSheet(u"")
        self.pushbutton_apply_and_close.setAutoDefault(False)
        self.pushbutton_apply_and_close.setFlat(False)

        self.gridLayout_12.addWidget(self.pushbutton_apply_and_close, 0, 3, 1, 1)

        self.pushbutton_apply = QPushButton(self.frame_buttons_2)
        self.pushbutton_apply.setObjectName(u"pushbutton_apply")
        self.pushbutton_apply.setMinimumSize(QSize(72, 30))
        self.pushbutton_apply.setMaximumSize(QSize(72, 30))
        self.pushbutton_apply.setFont(font2)
        self.pushbutton_apply.setStyleSheet(u"")
        self.pushbutton_apply.setAutoDefault(False)
        self.pushbutton_apply.setFlat(False)

        self.gridLayout_12.addWidget(self.pushbutton_apply, 0, 2, 1, 1)

        self.pushbutton_cancel = QPushButton(self.frame_buttons_2)
        self.pushbutton_cancel.setObjectName(u"pushbutton_cancel")
        self.pushbutton_cancel.setMinimumSize(QSize(72, 30))
        self.pushbutton_cancel.setMaximumSize(QSize(72, 30))
        self.pushbutton_cancel.setFont(font2)
        self.pushbutton_cancel.setStyleSheet(u"")
        self.pushbutton_cancel.setAutoDefault(False)
        self.pushbutton_cancel.setFlat(False)

        self.gridLayout_12.addWidget(self.pushbutton_cancel, 0, 0, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_18, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons_2, 3, 1, 1, 1)


        self.retranslateUi(Dialog)

        self.pushbutton_apply_and_close.setDefault(False)
        self.pushbutton_apply.setDefault(False)
        self.pushbutton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Geometry Tolerance:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Element size:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.mesher_setup_label.setText(QCoreApplication.translate("Dialog", u"Mesher Setup", None))
        self.pushbutton_apply_and_close.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushbutton_apply.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushbutton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class MesherSetupInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_geometry_tolerance: QLineEdit
                                        - label: QLabel
                                        - lineEdit_element_size: QLineEdit
                                        - label_3: QLabel
                                        - label_4: QLabel
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - mesher_setup_label: QLabel
                - frame_buttons_2: QFrame
                    - (Layout): QGridLayout
                            - pushbutton_apply_and_close: QPushButton
                            - pushbutton_apply: QPushButton
                            - pushbutton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
