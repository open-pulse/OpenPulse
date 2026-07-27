# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_perforated_plate_info.ui'
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
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(428, 505)
        Dialog.setMinimumSize(QSize(0, 400))
        Dialog.setMaximumSize(QSize(428, 600))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(420, 48))
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMinimumSize(QSize(0, 0))
        self.title_label.setMaximumSize(QSize(446, 16777215))
        font = QFont()
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setTextFormat(Qt.TextFormat.AutoText)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.title_label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(420, 0))
        self.frame_2.setMaximumSize(QSize(420, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 408, 381))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_plate_thickness = QLineEdit(self.frame_4)
        self.lineEdit_plate_thickness.setObjectName(u"lineEdit_plate_thickness")
        self.lineEdit_plate_thickness.setMinimumSize(QSize(120, 26))
        self.lineEdit_plate_thickness.setMaximumSize(QSize(120, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_plate_thickness.setFont(font1)
        self.lineEdit_plate_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_plate_thickness, 2, 2, 1, 1)

        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(50, 26))
        self.label_21.setMaximumSize(QSize(50, 26))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_21, 2, 3, 1, 1)

        self.label_area_porosity = QLabel(self.frame_4)
        self.label_area_porosity.setObjectName(u"label_area_porosity")
        sizePolicy.setHeightForWidth(self.label_area_porosity.sizePolicy().hasHeightForWidth())
        self.label_area_porosity.setSizePolicy(sizePolicy)
        self.label_area_porosity.setMinimumSize(QSize(0, 26))
        self.label_area_porosity.setMaximumSize(QSize(190, 26))
        self.label_area_porosity.setFont(font1)
        self.label_area_porosity.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_area_porosity, 3, 1, 1, 1)

        self.lineEdit_hole_diameter = QLineEdit(self.frame_4)
        self.lineEdit_hole_diameter.setObjectName(u"lineEdit_hole_diameter")
        self.lineEdit_hole_diameter.setMinimumSize(QSize(120, 26))
        self.lineEdit_hole_diameter.setMaximumSize(QSize(120, 26))
        self.lineEdit_hole_diameter.setFont(font1)
        self.lineEdit_hole_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_hole_diameter, 1, 2, 1, 1)

        self.lineEdit_correction_factor = QLineEdit(self.frame_4)
        self.lineEdit_correction_factor.setObjectName(u"lineEdit_correction_factor")
        self.lineEdit_correction_factor.setMinimumSize(QSize(120, 26))
        self.lineEdit_correction_factor.setMaximumSize(QSize(120, 26))
        self.lineEdit_correction_factor.setFont(font1)
        self.lineEdit_correction_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_correction_factor, 7, 2, 1, 1)

        self.lineEdit_non_linear_discharge_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_non_linear_discharge_coefficient.setObjectName(u"lineEdit_non_linear_discharge_coefficient")
        self.lineEdit_non_linear_discharge_coefficient.setMinimumSize(QSize(120, 26))
        self.lineEdit_non_linear_discharge_coefficient.setMaximumSize(QSize(120, 26))
        self.lineEdit_non_linear_discharge_coefficient.setFont(font1)
        self.lineEdit_non_linear_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_non_linear_discharge_coefficient, 6, 2, 1, 1)

        self.lineEdit_dimensionless_impedance = QLineEdit(self.frame_4)
        self.lineEdit_dimensionless_impedance.setObjectName(u"lineEdit_dimensionless_impedance")
        self.lineEdit_dimensionless_impedance.setMinimumSize(QSize(120, 26))
        self.lineEdit_dimensionless_impedance.setMaximumSize(QSize(120, 26))
        self.lineEdit_dimensionless_impedance.setFont(font1)
        self.lineEdit_dimensionless_impedance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_dimensionless_impedance, 9, 2, 1, 1)

        self.lineEdit_area_porosity = QLineEdit(self.frame_4)
        self.lineEdit_area_porosity.setObjectName(u"lineEdit_area_porosity")
        self.lineEdit_area_porosity.setMinimumSize(QSize(120, 26))
        self.lineEdit_area_porosity.setMaximumSize(QSize(120, 26))
        self.lineEdit_area_porosity.setFont(font1)
        self.lineEdit_area_porosity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_area_porosity, 3, 2, 1, 1)

        self.lineEdit_single_hole = QLineEdit(self.frame_4)
        self.lineEdit_single_hole.setObjectName(u"lineEdit_single_hole")
        self.lineEdit_single_hole.setMinimumSize(QSize(120, 26))
        self.lineEdit_single_hole.setMaximumSize(QSize(120, 26))
        self.lineEdit_single_hole.setFont(font1)
        self.lineEdit_single_hole.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_single_hole, 5, 2, 1, 1)

        self.label_discharge_coefficient = QLabel(self.frame_4)
        self.label_discharge_coefficient.setObjectName(u"label_discharge_coefficient")
        sizePolicy.setHeightForWidth(self.label_discharge_coefficient.sizePolicy().hasHeightForWidth())
        self.label_discharge_coefficient.setSizePolicy(sizePolicy)
        self.label_discharge_coefficient.setMinimumSize(QSize(0, 26))
        self.label_discharge_coefficient.setMaximumSize(QSize(190, 26))
        self.label_discharge_coefficient.setFont(font1)
        self.label_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_discharge_coefficient, 4, 1, 1, 1)

        self.label_bias_flow_coefficient = QLabel(self.frame_4)
        self.label_bias_flow_coefficient.setObjectName(u"label_bias_flow_coefficient")
        sizePolicy.setHeightForWidth(self.label_bias_flow_coefficient.sizePolicy().hasHeightForWidth())
        self.label_bias_flow_coefficient.setSizePolicy(sizePolicy)
        self.label_bias_flow_coefficient.setMinimumSize(QSize(0, 26))
        self.label_bias_flow_coefficient.setMaximumSize(QSize(190, 26))
        self.label_bias_flow_coefficient.setFont(font1)
        self.label_bias_flow_coefficient.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_bias_flow_coefficient, 8, 1, 1, 1)

        self.lineEdit_perforated_plate_elements = QLineEdit(self.frame_4)
        self.lineEdit_perforated_plate_elements.setObjectName(u"lineEdit_perforated_plate_elements")
        self.lineEdit_perforated_plate_elements.setMinimumSize(QSize(120, 26))
        self.lineEdit_perforated_plate_elements.setMaximumSize(QSize(120, 26))
        self.lineEdit_perforated_plate_elements.setFont(font1)
        self.lineEdit_perforated_plate_elements.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_perforated_plate_elements, 0, 2, 1, 1)

        self.label_20 = QLabel(self.frame_4)
        self.label_20.setObjectName(u"label_20")
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QSize(50, 26))
        self.label_20.setMaximumSize(QSize(50, 26))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_20, 1, 3, 1, 1)

        self.label_selection_label = QLabel(self.frame_4)
        self.label_selection_label.setObjectName(u"label_selection_label")
        sizePolicy.setHeightForWidth(self.label_selection_label.sizePolicy().hasHeightForWidth())
        self.label_selection_label.setSizePolicy(sizePolicy)
        self.label_selection_label.setMinimumSize(QSize(0, 26))
        self.label_selection_label.setMaximumSize(QSize(190, 26))
        self.label_selection_label.setFont(font1)
        self.label_selection_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_selection_label, 0, 1, 1, 1)

        self.label_dimensionless_impedance = QLabel(self.frame_4)
        self.label_dimensionless_impedance.setObjectName(u"label_dimensionless_impedance")
        sizePolicy.setHeightForWidth(self.label_dimensionless_impedance.sizePolicy().hasHeightForWidth())
        self.label_dimensionless_impedance.setSizePolicy(sizePolicy)
        self.label_dimensionless_impedance.setMinimumSize(QSize(0, 26))
        self.label_dimensionless_impedance.setMaximumSize(QSize(190, 26))
        self.label_dimensionless_impedance.setSizeIncrement(QSize(0, 0))
        self.label_dimensionless_impedance.setFont(font1)
        self.label_dimensionless_impedance.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_dimensionless_impedance, 9, 1, 1, 1)

        self.label_thickness = QLabel(self.frame_4)
        self.label_thickness.setObjectName(u"label_thickness")
        sizePolicy.setHeightForWidth(self.label_thickness.sizePolicy().hasHeightForWidth())
        self.label_thickness.setSizePolicy(sizePolicy)
        self.label_thickness.setMinimumSize(QSize(0, 26))
        self.label_thickness.setMaximumSize(QSize(190, 26))
        self.label_thickness.setFont(font1)
        self.label_thickness.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_thickness, 2, 1, 1, 1)

        self.label_non_linear_discharge_coefficient = QLabel(self.frame_4)
        self.label_non_linear_discharge_coefficient.setObjectName(u"label_non_linear_discharge_coefficient")
        sizePolicy.setHeightForWidth(self.label_non_linear_discharge_coefficient.sizePolicy().hasHeightForWidth())
        self.label_non_linear_discharge_coefficient.setSizePolicy(sizePolicy)
        self.label_non_linear_discharge_coefficient.setMinimumSize(QSize(0, 26))
        self.label_non_linear_discharge_coefficient.setMaximumSize(QSize(190, 26))
        self.label_non_linear_discharge_coefficient.setFont(font1)
        self.label_non_linear_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_non_linear_discharge_coefficient, 6, 1, 1, 1)

        self.label_correction_factor = QLabel(self.frame_4)
        self.label_correction_factor.setObjectName(u"label_correction_factor")
        sizePolicy.setHeightForWidth(self.label_correction_factor.sizePolicy().hasHeightForWidth())
        self.label_correction_factor.setSizePolicy(sizePolicy)
        self.label_correction_factor.setMinimumSize(QSize(0, 26))
        self.label_correction_factor.setMaximumSize(QSize(190, 26))
        self.label_correction_factor.setFont(font1)
        self.label_correction_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_correction_factor, 7, 1, 1, 1)

        self.label_hole_diameter = QLabel(self.frame_4)
        self.label_hole_diameter.setObjectName(u"label_hole_diameter")
        sizePolicy.setHeightForWidth(self.label_hole_diameter.sizePolicy().hasHeightForWidth())
        self.label_hole_diameter.setSizePolicy(sizePolicy)
        self.label_hole_diameter.setMinimumSize(QSize(0, 26))
        self.label_hole_diameter.setMaximumSize(QSize(190, 26))
        self.label_hole_diameter.setFont(font1)
        self.label_hole_diameter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_hole_diameter, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.lineEdit_bias_flow_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_bias_flow_coefficient.setObjectName(u"lineEdit_bias_flow_coefficient")
        self.lineEdit_bias_flow_coefficient.setMinimumSize(QSize(120, 26))
        self.lineEdit_bias_flow_coefficient.setMaximumSize(QSize(120, 26))
        self.lineEdit_bias_flow_coefficient.setFont(font1)
        self.lineEdit_bias_flow_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_bias_flow_coefficient, 8, 2, 1, 1)

        self.lineEdit_discharge_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_discharge_coefficient.setObjectName(u"lineEdit_discharge_coefficient")
        self.lineEdit_discharge_coefficient.setMinimumSize(QSize(120, 26))
        self.lineEdit_discharge_coefficient.setMaximumSize(QSize(120, 26))
        self.lineEdit_discharge_coefficient.setFont(font1)
        self.lineEdit_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_discharge_coefficient, 4, 2, 1, 1)

        self.label_single_hole = QLabel(self.frame_4)
        self.label_single_hole.setObjectName(u"label_single_hole")
        sizePolicy.setHeightForWidth(self.label_single_hole.sizePolicy().hasHeightForWidth())
        self.label_single_hole.setSizePolicy(sizePolicy)
        self.label_single_hole.setMinimumSize(QSize(0, 26))
        self.label_single_hole.setMaximumSize(QSize(190, 26))
        self.label_single_hole.setFont(font1)
        self.label_single_hole.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_single_hole, 5, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_4.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 48))
        self.frame_7.setMaximumSize(QSize(800, 48))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_close = QPushButton(self.frame_7)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setMinimumSize(QSize(100, 30))
        self.pushButton_close.setMaximumSize(QSize(100, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_close.setFont(font2)
        self.pushButton_close.setStyleSheet(u"")
        self.pushButton_close.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_close, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_7, 2, 0, 1, 1)

        QWidget.setTabOrder(self.scrollArea, self.lineEdit_perforated_plate_elements)
        QWidget.setTabOrder(self.lineEdit_perforated_plate_elements, self.lineEdit_hole_diameter)
        QWidget.setTabOrder(self.lineEdit_hole_diameter, self.lineEdit_plate_thickness)
        QWidget.setTabOrder(self.lineEdit_plate_thickness, self.lineEdit_area_porosity)
        QWidget.setTabOrder(self.lineEdit_area_porosity, self.lineEdit_discharge_coefficient)
        QWidget.setTabOrder(self.lineEdit_discharge_coefficient, self.lineEdit_single_hole)
        QWidget.setTabOrder(self.lineEdit_single_hole, self.lineEdit_non_linear_discharge_coefficient)
        QWidget.setTabOrder(self.lineEdit_non_linear_discharge_coefficient, self.lineEdit_correction_factor)
        QWidget.setTabOrder(self.lineEdit_correction_factor, self.lineEdit_bias_flow_coefficient)
        QWidget.setTabOrder(self.lineEdit_bias_flow_coefficient, self.lineEdit_dimensionless_impedance)
        QWidget.setTabOrder(self.lineEdit_dimensionless_impedance, self.pushButton_close)

        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"Information of selected perforated plate", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_area_porosity.setText(QCoreApplication.translate("Dialog", u"Area porosity:", None))
        self.label_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"Discharge coefficient:", None))
        self.label_bias_flow_coefficient.setText(QCoreApplication.translate("Dialog", u"Bias flow coefficient:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_selection_label.setText(QCoreApplication.translate("Dialog", u"Element ID:", None))
        self.label_dimensionless_impedance.setText(QCoreApplication.translate("Dialog", u"Dimensionless impedance:", None))
        self.label_thickness.setText(QCoreApplication.translate("Dialog", u"Plate thickness:", None))
        self.label_non_linear_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"Nonlinear discharge coefficient:", None))
        self.label_correction_factor.setText(QCoreApplication.translate("Dialog", u"Correction factor:", None))
        self.label_hole_diameter.setText(QCoreApplication.translate("Dialog", u"Hole diameter:", None))
        self.label_single_hole.setText(QCoreApplication.translate("Dialog", u"Single hole", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi



class GetPerforatedPlateInfo_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - title_label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_plate_thickness: QLineEdit
                                                        - label_21: QLabel
                                                        - label_area_porosity: QLabel
                                                        - lineEdit_hole_diameter: QLineEdit
                                                        - lineEdit_correction_factor: QLineEdit
                                                        - lineEdit_non_linear_discharge_coefficient: QLineEdit
                                                        - lineEdit_dimensionless_impedance: QLineEdit
                                                        - lineEdit_area_porosity: QLineEdit
                                                        - lineEdit_single_hole: QLineEdit
                                                        - label_discharge_coefficient: QLabel
                                                        - label_bias_flow_coefficient: QLabel
                                                        - lineEdit_perforated_plate_elements: QLineEdit
                                                        - label_20: QLabel
                                                        - label_selection_label: QLabel
                                                        - label_dimensionless_impedance: QLabel
                                                        - label_thickness: QLabel
                                                        - label_non_linear_discharge_coefficient: QLabel
                                                        - label_correction_factor: QLabel
                                                        - label_hole_diameter: QLabel
                                                        - lineEdit_bias_flow_coefficient: QLineEdit
                                                        - lineEdit_discharge_coefficient: QLineEdit
                                                        - label_single_hole: QLabel
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_close: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
