# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getGroupInformationPerforatedPlate.ui'
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
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(438, 579)
        Dialog.setMinimumSize(QSize(0, 0))
        Dialog.setMaximumSize(QSize(800, 800))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(420, 48))
        self.frame.setMaximumSize(QSize(420, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMinimumSize(QSize(0, 0))
        self.title_label.setMaximumSize(QSize(446, 16777215))
        font = QFont()
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setTextFormat(Qt.AutoText)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.title_label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(420, 0))
        self.frame_2.setMaximumSize(QSize(420, 16777215))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.treeWidget_group_info = QTreeWidget(self.frame_2)
        font1 = QFont()
        font1.setPointSize(9)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font1);
        self.treeWidget_group_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_group_info.setMaximumSize(QSize(402, 430))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setBold(False)
        self.treeWidget_group_info.setFont(font2)
        self.treeWidget_group_info.setTextElideMode(Qt.ElideRight)
        self.treeWidget_group_info.setIndentation(0)
        self.treeWidget_group_info.setUniformRowHeights(False)
        self.treeWidget_group_info.setAnimated(False)
        self.treeWidget_group_info.setAllColumnsShowFocus(False)
        self.treeWidget_group_info.setHeaderHidden(False)
        self.treeWidget_group_info.setColumnCount(1)
        self.treeWidget_group_info.header().setVisible(True)

        self.gridLayout_4.addWidget(self.treeWidget_group_info, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(40, 26))
        self.label_21.setMaximumSize(QSize(40, 26))
        font3 = QFont()
        font3.setPointSize(10)
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_21, 1, 2, 1, 1)

        self.label_20 = QLabel(self.frame_4)
        self.label_20.setObjectName(u"label_20")
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QSize(40, 26))
        self.label_20.setMaximumSize(QSize(40, 26))
        self.label_20.setFont(font3)
        self.label_20.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_20, 0, 2, 1, 1)

        self.lineEdit_hole_diameter = QLineEdit(self.frame_4)
        self.lineEdit_hole_diameter.setObjectName(u"lineEdit_hole_diameter")

        self.gridLayout_2.addWidget(self.lineEdit_hole_diameter, 0, 1, 1, 1)

        self.lineEdit_plate_thickness = QLineEdit(self.frame_4)
        self.lineEdit_plate_thickness.setObjectName(u"lineEdit_plate_thickness")

        self.gridLayout_2.addWidget(self.lineEdit_plate_thickness, 1, 1, 1, 1)

        self.label_porosity = QLabel(self.frame_4)
        self.label_porosity.setObjectName(u"label_porosity")
        sizePolicy.setHeightForWidth(self.label_porosity.sizePolicy().hasHeightForWidth())
        self.label_porosity.setSizePolicy(sizePolicy)
        self.label_porosity.setMinimumSize(QSize(200, 26))
        self.label_porosity.setMaximumSize(QSize(200, 26))
        self.label_porosity.setFont(font3)
        self.label_porosity.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_porosity, 2, 0, 1, 1)

        self.label_discharge = QLabel(self.frame_4)
        self.label_discharge.setObjectName(u"label_discharge")
        sizePolicy.setHeightForWidth(self.label_discharge.sizePolicy().hasHeightForWidth())
        self.label_discharge.setSizePolicy(sizePolicy)
        self.label_discharge.setMinimumSize(QSize(200, 26))
        self.label_discharge.setMaximumSize(QSize(200, 26))
        self.label_discharge.setFont(font3)
        self.label_discharge.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_discharge, 3, 0, 1, 1)

        self.label_bias = QLabel(self.frame_4)
        self.label_bias.setObjectName(u"label_bias")
        sizePolicy.setHeightForWidth(self.label_bias.sizePolicy().hasHeightForWidth())
        self.label_bias.setSizePolicy(sizePolicy)
        self.label_bias.setMinimumSize(QSize(200, 26))
        self.label_bias.setMaximumSize(QSize(200, 26))
        self.label_bias.setFont(font3)
        self.label_bias.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_bias, 9, 0, 1, 1)

        self.label_nonlinDischarge_2 = QLabel(self.frame_4)
        self.label_nonlinDischarge_2.setObjectName(u"label_nonlinDischarge_2")
        sizePolicy.setHeightForWidth(self.label_nonlinDischarge_2.sizePolicy().hasHeightForWidth())
        self.label_nonlinDischarge_2.setSizePolicy(sizePolicy)
        self.label_nonlinDischarge_2.setMinimumSize(QSize(200, 26))
        self.label_nonlinDischarge_2.setMaximumSize(QSize(200, 26))
        self.label_nonlinDischarge_2.setFont(font3)
        self.label_nonlinDischarge_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_nonlinDischarge_2, 6, 0, 1, 1)

        self.label_bias_3 = QLabel(self.frame_4)
        self.label_bias_3.setObjectName(u"label_bias_3")
        sizePolicy.setHeightForWidth(self.label_bias_3.sizePolicy().hasHeightForWidth())
        self.label_bias_3.setSizePolicy(sizePolicy)
        self.label_bias_3.setMinimumSize(QSize(200, 26))
        self.label_bias_3.setMaximumSize(QSize(200, 26))
        self.label_bias_3.setFont(font3)
        self.label_bias_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_bias_3, 7, 0, 1, 1)

        self.label_correction_2 = QLabel(self.frame_4)
        self.label_correction_2.setObjectName(u"label_correction_2")
        sizePolicy.setHeightForWidth(self.label_correction_2.sizePolicy().hasHeightForWidth())
        self.label_correction_2.setSizePolicy(sizePolicy)
        self.label_correction_2.setMinimumSize(QSize(200, 26))
        self.label_correction_2.setMaximumSize(QSize(200, 26))
        self.label_correction_2.setFont(font3)
        self.label_correction_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_correction_2, 8, 0, 1, 1)

        self.label_thickness = QLabel(self.frame_4)
        self.label_thickness.setObjectName(u"label_thickness")
        sizePolicy.setHeightForWidth(self.label_thickness.sizePolicy().hasHeightForWidth())
        self.label_thickness.setSizePolicy(sizePolicy)
        self.label_thickness.setMinimumSize(QSize(200, 26))
        self.label_thickness.setMaximumSize(QSize(200, 26))
        self.label_thickness.setFont(font3)
        self.label_thickness.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_thickness, 1, 0, 1, 1)

        self.label_HoleDiameter = QLabel(self.frame_4)
        self.label_HoleDiameter.setObjectName(u"label_HoleDiameter")
        sizePolicy.setHeightForWidth(self.label_HoleDiameter.sizePolicy().hasHeightForWidth())
        self.label_HoleDiameter.setSizePolicy(sizePolicy)
        self.label_HoleDiameter.setMinimumSize(QSize(200, 26))
        self.label_HoleDiameter.setMaximumSize(QSize(200, 26))
        self.label_HoleDiameter.setFont(font3)
        self.label_HoleDiameter.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_HoleDiameter, 0, 0, 1, 1)

        self.label_discharge_2 = QLabel(self.frame_4)
        self.label_discharge_2.setObjectName(u"label_discharge_2")
        sizePolicy.setHeightForWidth(self.label_discharge_2.sizePolicy().hasHeightForWidth())
        self.label_discharge_2.setSizePolicy(sizePolicy)
        self.label_discharge_2.setMinimumSize(QSize(200, 26))
        self.label_discharge_2.setMaximumSize(QSize(200, 26))
        self.label_discharge_2.setFont(font3)
        self.label_discharge_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_discharge_2, 4, 0, 1, 1)

        self.label_porosity_2 = QLabel(self.frame_4)
        self.label_porosity_2.setObjectName(u"label_porosity_2")
        sizePolicy.setHeightForWidth(self.label_porosity_2.sizePolicy().hasHeightForWidth())
        self.label_porosity_2.setSizePolicy(sizePolicy)
        self.label_porosity_2.setMinimumSize(QSize(200, 26))
        self.label_porosity_2.setMaximumSize(QSize(200, 26))
        self.label_porosity_2.setFont(font3)
        self.label_porosity_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_porosity_2, 5, 0, 1, 1)

        self.label_bias_2 = QLabel(self.frame_4)
        self.label_bias_2.setObjectName(u"label_bias_2")
        sizePolicy.setHeightForWidth(self.label_bias_2.sizePolicy().hasHeightForWidth())
        self.label_bias_2.setSizePolicy(sizePolicy)
        self.label_bias_2.setMinimumSize(QSize(200, 26))
        self.label_bias_2.setMaximumSize(QSize(200, 26))
        self.label_bias_2.setSizeIncrement(QSize(0, 0))
        self.label_bias_2.setFont(font3)
        self.label_bias_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_bias_2, 10, 0, 1, 1)

        self.lineEdit_area_porosity = QLineEdit(self.frame_4)
        self.lineEdit_area_porosity.setObjectName(u"lineEdit_area_porosity")

        self.gridLayout_2.addWidget(self.lineEdit_area_porosity, 2, 1, 1, 1)

        self.lineEdit_discharge_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_discharge_coefficient.setObjectName(u"lineEdit_discharge_coefficient")

        self.gridLayout_2.addWidget(self.lineEdit_discharge_coefficient, 3, 1, 1, 1)

        self.lineEdit_single_hole = QLineEdit(self.frame_4)
        self.lineEdit_single_hole.setObjectName(u"lineEdit_single_hole")

        self.gridLayout_2.addWidget(self.lineEdit_single_hole, 4, 1, 1, 1)

        self.lineEdit_non_linear_effects = QLineEdit(self.frame_4)
        self.lineEdit_non_linear_effects.setObjectName(u"lineEdit_non_linear_effects")

        self.gridLayout_2.addWidget(self.lineEdit_non_linear_effects, 5, 1, 1, 1)

        self.lineEdit_non_linear_discharge_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_non_linear_discharge_coefficient.setObjectName(u"lineEdit_non_linear_discharge_coefficient")

        self.gridLayout_2.addWidget(self.lineEdit_non_linear_discharge_coefficient, 6, 1, 1, 1)

        self.lineEdit_correction_factor = QLineEdit(self.frame_4)
        self.lineEdit_correction_factor.setObjectName(u"lineEdit_correction_factor")

        self.gridLayout_2.addWidget(self.lineEdit_correction_factor, 7, 1, 1, 1)

        self.lineEdit_bias_flow_effects = QLineEdit(self.frame_4)
        self.lineEdit_bias_flow_effects.setObjectName(u"lineEdit_bias_flow_effects")

        self.gridLayout_2.addWidget(self.lineEdit_bias_flow_effects, 8, 1, 1, 1)

        self.lineEdit_bias_flow_coefficient = QLineEdit(self.frame_4)
        self.lineEdit_bias_flow_coefficient.setObjectName(u"lineEdit_bias_flow_coefficient")

        self.gridLayout_2.addWidget(self.lineEdit_bias_flow_coefficient, 9, 1, 1, 1)

        self.lineEdit_dimensionless_impedance = QLineEdit(self.frame_4)
        self.lineEdit_dimensionless_impedance.setObjectName(u"lineEdit_dimensionless_impedance")

        self.gridLayout_2.addWidget(self.lineEdit_dimensionless_impedance, 10, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 48))
        self.frame_7.setMaximumSize(QSize(800, 48))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_close = QPushButton(self.frame_7)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setMinimumSize(QSize(80, 30))
        self.pushButton_close.setMaximumSize(QSize(80, 30))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_close.setFont(font4)
        self.pushButton_close.setStyleSheet(u"QPushButton{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}\n"
"QPushButton:hover{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}\n"
"QPushButton:pressed{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255)}\n"
"QPushButton:disabled{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(150,150, 150); background-color: rgb(220, 220, 220)}")

        self.gridLayout_11.addWidget(self.pushButton_close, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_7, 2, 0, 1, 1)

        QWidget.setTabOrder(self.treeWidget_group_info, self.lineEdit_hole_diameter)
        QWidget.setTabOrder(self.lineEdit_hole_diameter, self.lineEdit_plate_thickness)
        QWidget.setTabOrder(self.lineEdit_plate_thickness, self.lineEdit_area_porosity)
        QWidget.setTabOrder(self.lineEdit_area_porosity, self.lineEdit_discharge_coefficient)
        QWidget.setTabOrder(self.lineEdit_discharge_coefficient, self.lineEdit_single_hole)
        QWidget.setTabOrder(self.lineEdit_single_hole, self.lineEdit_non_linear_effects)
        QWidget.setTabOrder(self.lineEdit_non_linear_effects, self.lineEdit_non_linear_discharge_coefficient)
        QWidget.setTabOrder(self.lineEdit_non_linear_discharge_coefficient, self.lineEdit_correction_factor)
        QWidget.setTabOrder(self.lineEdit_correction_factor, self.lineEdit_bias_flow_effects)
        QWidget.setTabOrder(self.lineEdit_bias_flow_effects, self.lineEdit_bias_flow_coefficient)
        QWidget.setTabOrder(self.lineEdit_bias_flow_coefficient, self.lineEdit_dimensionless_impedance)
        QWidget.setTabOrder(self.lineEdit_dimensionless_impedance, self.pushButton_close)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Information of selected perforated plate</span></p></body></html>", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Elements", None));
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_porosity.setText(QCoreApplication.translate("Dialog", u"Area porosity:", None))
        self.label_discharge.setText(QCoreApplication.translate("Dialog", u"Discharge coefficient:", None))
        self.label_bias.setText(QCoreApplication.translate("Dialog", u"Bias flow coefficient:", None))
        self.label_nonlinDischarge_2.setText(QCoreApplication.translate("Dialog", u"Nonlinear discharge coefficient:", None))
        self.label_bias_3.setText(QCoreApplication.translate("Dialog", u"Correction factor:", None))
        self.label_correction_2.setText(QCoreApplication.translate("Dialog", u"Bias flow effects:", None))
        self.label_thickness.setText(QCoreApplication.translate("Dialog", u"Plate thickness:", None))
        self.label_HoleDiameter.setText(QCoreApplication.translate("Dialog", u"Hole diameter:", None))
        self.label_discharge_2.setText(QCoreApplication.translate("Dialog", u"Single hole", None))
        self.label_porosity_2.setText(QCoreApplication.translate("Dialog", u" Nonlinear effects:", None))
        self.label_bias_2.setText(QCoreApplication.translate("Dialog", u"Dimensionless impedance:", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi



class Getgroupinformationperforatedplate_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - title_label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - treeWidget_group_info: QTreeWidget
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_21: QLabel
                                        - label_20: QLabel
                                        - lineEdit_hole_diameter: QLineEdit
                                        - lineEdit_plate_thickness: QLineEdit
                                        - label_porosity: QLabel
                                        - label_discharge: QLabel
                                        - label_bias: QLabel
                                        - label_nonlinDischarge_2: QLabel
                                        - label_bias_3: QLabel
                                        - label_correction_2: QLabel
                                        - label_thickness: QLabel
                                        - label_HoleDiameter: QLabel
                                        - label_discharge_2: QLabel
                                        - label_porosity_2: QLabel
                                        - label_bias_2: QLabel
                                        - lineEdit_area_porosity: QLineEdit
                                        - lineEdit_discharge_coefficient: QLineEdit
                                        - lineEdit_single_hole: QLineEdit
                                        - lineEdit_non_linear_effects: QLineEdit
                                        - lineEdit_non_linear_discharge_coefficient: QLineEdit
                                        - lineEdit_correction_factor: QLineEdit
                                        - lineEdit_bias_flow_effects: QLineEdit
                                        - lineEdit_bias_flow_coefficient: QLineEdit
                                        - lineEdit_dimensionless_impedance: QLineEdit
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_close: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
