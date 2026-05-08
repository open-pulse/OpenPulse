# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_stresses_for_static_analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 352)
        Form.setMinimumSize(QSize(0, 352))
        Form.setMaximumSize(QSize(16777215, 352))
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 2, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 32))
        self.label.setMaximumSize(QSize(300, 32))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_responses = QFrame(Form)
        self.frame_responses.setObjectName(u"frame_responses")
        self.frame_responses.setMinimumSize(QSize(0, 0))
        self.frame_responses.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(7)
        self.frame_responses.setFont(font1)
        self.frame_responses.setFrameShape(QFrame.Box)
        self.frame_responses.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_responses)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_responses)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.frame_4, 0, 4, 1, 1)

        self.lineEdit_element_id = QLineEdit(self.frame_responses)
        self.lineEdit_element_id.setObjectName(u"lineEdit_element_id")
        self.lineEdit_element_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_element_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_element_id.setSizeIncrement(QSize(0, 0))
        self.lineEdit_element_id.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.lineEdit_element_id.setFont(font2)
        self.lineEdit_element_id.setStyleSheet(u"")
        self.lineEdit_element_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_element_id, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_responses)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 28))
        self.label_3.setMaximumSize(QSize(80, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 1)

        self.lineEdit_axial_stress = QLineEdit(self.frame_responses)
        self.lineEdit_axial_stress.setObjectName(u"lineEdit_axial_stress")
        self.lineEdit_axial_stress.setMinimumSize(QSize(120, 28))
        self.lineEdit_axial_stress.setMaximumSize(QSize(120, 28))
        self.lineEdit_axial_stress.setSizeIncrement(QSize(0, 0))
        self.lineEdit_axial_stress.setBaseSize(QSize(0, 0))
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_axial_stress.setFont(font3)
        self.lineEdit_axial_stress.setStyleSheet(u"")
        self.lineEdit_axial_stress.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_axial_stress, 1, 2, 1, 1)

        self.lineEdit_hoop_stress = QLineEdit(self.frame_responses)
        self.lineEdit_hoop_stress.setObjectName(u"lineEdit_hoop_stress")
        self.lineEdit_hoop_stress.setMinimumSize(QSize(120, 28))
        self.lineEdit_hoop_stress.setMaximumSize(QSize(120, 28))
        self.lineEdit_hoop_stress.setSizeIncrement(QSize(0, 0))
        self.lineEdit_hoop_stress.setBaseSize(QSize(0, 0))
        self.lineEdit_hoop_stress.setFont(font3)
        self.lineEdit_hoop_stress.setStyleSheet(u"")
        self.lineEdit_hoop_stress.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_hoop_stress, 4, 2, 1, 1)

        self.frame = QFrame(self.frame_responses)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(60, 28))
        self.frame.setMaximumSize(QSize(60, 28))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 4, 0)
        self.pushButton_reset = QPushButton(self.frame)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(50, 26))
        self.pushButton_reset.setMaximumSize(QSize(50, 26))
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 3, 1, 1)

        self.lineEdit_bending_stress_y = QLineEdit(self.frame_responses)
        self.lineEdit_bending_stress_y.setObjectName(u"lineEdit_bending_stress_y")
        self.lineEdit_bending_stress_y.setMinimumSize(QSize(120, 28))
        self.lineEdit_bending_stress_y.setMaximumSize(QSize(120, 28))
        self.lineEdit_bending_stress_y.setSizeIncrement(QSize(0, 0))
        self.lineEdit_bending_stress_y.setBaseSize(QSize(0, 0))
        self.lineEdit_bending_stress_y.setFont(font3)
        self.lineEdit_bending_stress_y.setStyleSheet(u"")
        self.lineEdit_bending_stress_y.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_bending_stress_y, 2, 2, 1, 1)

        self.label_2 = QLabel(self.frame_responses)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 28))
        self.label_2.setMaximumSize(QSize(80, 28))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_responses)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(80, 28))
        self.label_5.setMaximumSize(QSize(80, 28))
        self.label_5.setFont(font2)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 4, 1, 1, 1)

        self.label_18 = QLabel(self.frame_responses)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(60, 28))
        self.label_18.setMaximumSize(QSize(60, 28))
        self.label_18.setFont(font2)
        self.label_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_18, 4, 3, 1, 1)

        self.label_19 = QLabel(self.frame_responses)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(60, 28))
        self.label_19.setMaximumSize(QSize(60, 28))
        self.label_19.setFont(font2)
        self.label_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_19, 3, 3, 1, 1)

        self.label_16 = QLabel(self.frame_responses)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(60, 28))
        self.label_16.setMaximumSize(QSize(60, 28))
        self.label_16.setFont(font2)
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 6, 3, 1, 1)

        self.label_17 = QLabel(self.frame_responses)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(60, 28))
        self.label_17.setMaximumSize(QSize(60, 28))
        self.label_17.setFont(font2)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_17, 5, 3, 1, 1)

        self.label_20 = QLabel(self.frame_responses)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(60, 28))
        self.label_20.setMaximumSize(QSize(60, 28))
        self.label_20.setFont(font2)
        self.label_20.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 2, 3, 1, 1)

        self.label_21 = QLabel(self.frame_responses)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(60, 28))
        self.label_21.setMaximumSize(QSize(60, 28))
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_21, 1, 3, 1, 1)

        self.label_13 = QLabel(self.frame_responses)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(60, 28))
        self.label_13.setMaximumSize(QSize(60, 28))
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 7, 3, 1, 1)

        self.label_6 = QLabel(self.frame_responses)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(80, 28))
        self.label_6.setMaximumSize(QSize(80, 28))
        self.label_6.setFont(font2)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 6, 1, 1, 1)

        self.label_7 = QLabel(self.frame_responses)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(80, 28))
        self.label_7.setMaximumSize(QSize(80, 28))
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 7, 1, 1, 1)

        self.label_4 = QLabel(self.frame_responses)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 28))
        self.label_4.setMaximumSize(QSize(80, 28))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_4, 3, 1, 1, 1)

        self.lineEdit_torsional_stress = QLineEdit(self.frame_responses)
        self.lineEdit_torsional_stress.setObjectName(u"lineEdit_torsional_stress")
        self.lineEdit_torsional_stress.setMinimumSize(QSize(120, 28))
        self.lineEdit_torsional_stress.setMaximumSize(QSize(120, 28))
        self.lineEdit_torsional_stress.setSizeIncrement(QSize(0, 0))
        self.lineEdit_torsional_stress.setBaseSize(QSize(0, 0))
        self.lineEdit_torsional_stress.setFont(font3)
        self.lineEdit_torsional_stress.setStyleSheet(u"")
        self.lineEdit_torsional_stress.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_torsional_stress, 5, 2, 1, 1)

        self.label_15 = QLabel(self.frame_responses)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(80, 28))
        self.label_15.setMaximumSize(QSize(80, 28))
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_15, 5, 1, 1, 1)

        self.lineEdit_shear_stress_yz = QLineEdit(self.frame_responses)
        self.lineEdit_shear_stress_yz.setObjectName(u"lineEdit_shear_stress_yz")
        self.lineEdit_shear_stress_yz.setMinimumSize(QSize(120, 28))
        self.lineEdit_shear_stress_yz.setMaximumSize(QSize(120, 28))
        self.lineEdit_shear_stress_yz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_shear_stress_yz.setBaseSize(QSize(0, 0))
        self.lineEdit_shear_stress_yz.setFont(font3)
        self.lineEdit_shear_stress_yz.setStyleSheet(u"")
        self.lineEdit_shear_stress_yz.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_shear_stress_yz, 7, 2, 1, 1)

        self.label_14 = QLabel(self.frame_responses)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(80, 28))
        self.label_14.setMaximumSize(QSize(80, 28))
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 0, 1, 1, 1)

        self.lineEdit_shear_stress_xy = QLineEdit(self.frame_responses)
        self.lineEdit_shear_stress_xy.setObjectName(u"lineEdit_shear_stress_xy")
        self.lineEdit_shear_stress_xy.setMinimumSize(QSize(120, 28))
        self.lineEdit_shear_stress_xy.setMaximumSize(QSize(120, 28))
        self.lineEdit_shear_stress_xy.setSizeIncrement(QSize(0, 0))
        self.lineEdit_shear_stress_xy.setBaseSize(QSize(0, 0))
        self.lineEdit_shear_stress_xy.setFont(font3)
        self.lineEdit_shear_stress_xy.setStyleSheet(u"")
        self.lineEdit_shear_stress_xy.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_shear_stress_xy, 6, 2, 1, 1)

        self.lineEdit_bending_stress_z = QLineEdit(self.frame_responses)
        self.lineEdit_bending_stress_z.setObjectName(u"lineEdit_bending_stress_z")
        self.lineEdit_bending_stress_z.setMinimumSize(QSize(120, 28))
        self.lineEdit_bending_stress_z.setMaximumSize(QSize(120, 28))
        self.lineEdit_bending_stress_z.setSizeIncrement(QSize(0, 0))
        self.lineEdit_bending_stress_z.setBaseSize(QSize(0, 0))
        self.lineEdit_bending_stress_z.setFont(font3)
        self.lineEdit_bending_stress_z.setStyleSheet(u"")
        self.lineEdit_bending_stress_z.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_bending_stress_z, 3, 2, 1, 1)

        self.frame_3 = QFrame(self.frame_responses)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setMaximumSize(QSize(48, 16777215))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_responses, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_element_id, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.lineEdit_axial_stress)
        QWidget.setTabOrder(self.lineEdit_axial_stress, self.lineEdit_bending_stress_y)
        QWidget.setTabOrder(self.lineEdit_bending_stress_y, self.lineEdit_bending_stress_z)
        QWidget.setTabOrder(self.lineEdit_bending_stress_z, self.lineEdit_hoop_stress)
        QWidget.setTabOrder(self.lineEdit_hoop_stress, self.lineEdit_torsional_stress)
        QWidget.setTabOrder(self.lineEdit_torsional_stress, self.lineEdit_shear_stress_xy)
        QWidget.setTabOrder(self.lineEdit_shear_stress_xy, self.lineEdit_shear_stress_yz)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Static analysis stresses", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Bending y: ", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Axial: ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Hoop: ", None))
        self.label_18.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_19.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_16.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_17.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_20.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_21.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_13.setText(QCoreApplication.translate("Form", u" [MPa]", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Shear xy : ", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Shear yz: ", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Bending z: ", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Torsional: ", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Element ID: ", None))
    # retranslateUi



class GetStressesForStaticAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_responses: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                            - lineEdit_element_id: QLineEdit
                            - label_3: QLabel
                            - lineEdit_axial_stress: QLineEdit
                            - lineEdit_hoop_stress: QLineEdit
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_reset: QPushButton
                            - lineEdit_bending_stress_y: QLineEdit
                            - label_2: QLabel
                            - label_5: QLabel
                            - label_18: QLabel
                            - label_19: QLabel
                            - label_16: QLabel
                            - label_17: QLabel
                            - label_20: QLabel
                            - label_21: QLabel
                            - label_13: QLabel
                            - label_6: QLabel
                            - label_7: QLabel
                            - label_4: QLabel
                            - lineEdit_torsional_stress: QLineEdit
                            - label_15: QLabel
                            - lineEdit_shear_stress_yz: QLineEdit
                            - label_14: QLabel
                            - lineEdit_shear_stress_xy: QLineEdit
                            - lineEdit_bending_stress_z: QLineEdit
                            - frame_3: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
