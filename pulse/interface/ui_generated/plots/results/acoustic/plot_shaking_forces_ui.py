# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_shaking_forces.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(302, 312)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_selection_id = QFrame(self.frame)
        self.frame_selection_id.setObjectName(u"frame_selection_id")
        self.frame_selection_id.setMinimumSize(QSize(0, 40))
        self.frame_selection_id.setMaximumSize(QSize(380, 40))
        self.frame_selection_id.setFrameShape(QFrame.NoFrame)
        self.frame_selection_id.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_selection_id)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_selection_id = QLineEdit(self.frame_selection_id)
        self.lineEdit_selection_id.setObjectName(u"lineEdit_selection_id")
        self.lineEdit_selection_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_selection_id.setMaximumSize(QSize(160, 26))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_selection_id.setFont(font1)
        self.lineEdit_selection_id.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_selection_id.setStyleSheet(u"")
        self.lineEdit_selection_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selection_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_selection_id)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 26))
        self.label_2.setMaximumSize(QSize(100, 26))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_selection_id, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBox_resultant_force = QCheckBox(self.frame_2)
        self.checkBox_resultant_force.setObjectName(u"checkBox_resultant_force")
        font2 = QFont()
        font2.setPointSize(10)
        self.checkBox_resultant_force.setFont(font2)
        self.checkBox_resultant_force.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_resultant_force, 3, 2, 1, 1)

        self.checkBox_force_Fx = QCheckBox(self.frame_2)
        self.checkBox_force_Fx.setObjectName(u"checkBox_force_Fx")
        self.checkBox_force_Fx.setFont(font2)
        self.checkBox_force_Fx.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_force_Fx, 0, 2, 1, 1)

        self.checkBox_force_Fz = QCheckBox(self.frame_2)
        self.checkBox_force_Fz.setObjectName(u"checkBox_force_Fz")
        self.checkBox_force_Fz.setFont(font2)
        self.checkBox_force_Fz.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_force_Fz, 2, 2, 1, 1)

        self.checkBox_force_Fy = QCheckBox(self.frame_2)
        self.checkBox_force_Fy.setObjectName(u"checkBox_force_Fy")
        self.checkBox_force_Fy.setFont(font2)
        self.checkBox_force_Fy.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_force_Fy, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 48))
        self.frame_7.setMaximumSize(QSize(400, 48))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_confirm = QPushButton(self.frame_7)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_confirm.setFont(font1)
        self.pushButton_confirm.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.pushButton_confirm, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_7, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selection_id, self.checkBox_force_Fx)
        QWidget.setTabOrder(self.checkBox_force_Fx, self.checkBox_force_Fy)
        QWidget.setTabOrder(self.checkBox_force_Fy, self.checkBox_force_Fz)
        QWidget.setTabOrder(self.checkBox_force_Fz, self.checkBox_resultant_force)
        QWidget.setTabOrder(self.checkBox_resultant_force, self.pushButton_confirm)

        self.retranslateUi(Form)

        self.pushButton_confirm.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot the shaking forces", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Selection ID:", None))
        self.checkBox_resultant_force.setText(QCoreApplication.translate("Form", u"Resultant", None))
        self.checkBox_force_Fx.setText(QCoreApplication.translate("Form", u"Force x", None))
        self.checkBox_force_Fz.setText(QCoreApplication.translate("Form", u"Force z", None))
        self.checkBox_force_Fy.setText(QCoreApplication.translate("Form", u"Force y", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Form", u"Confirm", None))
    # retranslateUi



class PlotShakingForces_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_selection_id: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selection_id: QLineEdit
                                        - label_2: QLabel
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_resultant_force: QCheckBox
                                        - checkBox_force_Fx: QCheckBox
                                        - checkBox_force_Fz: QCheckBox
                                        - checkBox_force_Fy: QCheckBox
                            - frame_7: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
