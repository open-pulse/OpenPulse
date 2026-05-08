# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'allowable_pulsations_for_reciprocating_compressor_inputs.ui'
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
        Form.resize(345, 623)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_14 = QFrame(self.frame_main)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_14)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 0)
        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 32))
        self.frame_15.setMaximumSize(QSize(16777215, 32))
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_15)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.label_10 = QLabel(self.frame_15)
        self.label_10.setObjectName(u"label_10")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_10.setWordWrap(False)

        self.gridLayout_10.addWidget(self.label_10, 0, 1, 1, 1)

        self.frame_16 = QFrame(self.frame_15)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_16, 0, 0, 1, 1)

        self.frame_17 = QFrame(self.frame_15)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_10.addWidget(self.frame_17, 0, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_15, 1, 0, 1, 1)

        self.frame_18 = QFrame(self.frame_14)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_18)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(4)
        self.gridLayout_11.setVerticalSpacing(6)
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_15 = QLabel(self.frame_18)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_15, 0, 1, 1, 1)

        self.label_14 = QLabel(self.frame_18)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_14, 2, 1, 1, 1)

        self.lineEdit_nozzle_id = QLineEdit(self.frame_18)
        self.lineEdit_nozzle_id.setObjectName(u"lineEdit_nozzle_id")
        self.lineEdit_nozzle_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_nozzle_id.setMaximumSize(QSize(100, 26))
        self.lineEdit_nozzle_id.setFont(font1)
        self.lineEdit_nozzle_id.setStyleSheet(u"")
        self.lineEdit_nozzle_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_nozzle_id, 0, 2, 1, 1)

        self.lineEdit_line_pressure = QLineEdit(self.frame_18)
        self.lineEdit_line_pressure.setObjectName(u"lineEdit_line_pressure")
        self.lineEdit_line_pressure.setMinimumSize(QSize(100, 26))
        self.lineEdit_line_pressure.setMaximumSize(QSize(100, 26))
        self.lineEdit_line_pressure.setFont(font1)
        self.lineEdit_line_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_line_pressure, 2, 2, 1, 1)

        self.lineEdit_internal_diameter = QLineEdit(self.frame_18)
        self.lineEdit_internal_diameter.setObjectName(u"lineEdit_internal_diameter")
        self.lineEdit_internal_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_internal_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_internal_diameter.setFont(font1)
        self.lineEdit_internal_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_internal_diameter, 3, 2, 1, 1)

        self.lineEdit_speed_of_sound = QLineEdit(self.frame_18)
        self.lineEdit_speed_of_sound.setObjectName(u"lineEdit_speed_of_sound")
        self.lineEdit_speed_of_sound.setMinimumSize(QSize(100, 26))
        self.lineEdit_speed_of_sound.setMaximumSize(QSize(100, 26))
        self.lineEdit_speed_of_sound.setFont(font1)
        self.lineEdit_speed_of_sound.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_speed_of_sound, 1, 2, 1, 1)

        self.label_13 = QLabel(self.frame_18)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_13, 3, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_12 = QLabel(self.frame_18)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_12, 1, 1, 1, 1)

        self.frame_19 = QFrame(self.frame_18)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_19)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_18, 0, 2, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_17, 0, 0, 1, 1)

        self.checkBox_prestudy_analysis = QCheckBox(self.frame_19)
        self.checkBox_prestudy_analysis.setObjectName(u"checkBox_prestudy_analysis")
        self.checkBox_prestudy_analysis.setFont(font1)

        self.gridLayout_16.addWidget(self.checkBox_prestudy_analysis, 0, 1, 1, 1)


        self.gridLayout_11.addWidget(self.frame_19, 4, 1, 1, 2)


        self.gridLayout_9.addWidget(self.frame_18, 2, 0, 1, 1)

        self.frame_21 = QFrame(self.frame_14)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMinimumSize(QSize(0, 40))
        self.frame_21.setMaximumSize(QSize(16777215, 40))
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_21)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_filtered_criteria = QPushButton(self.frame_21)
        self.pushButton_plot_filtered_criteria.setObjectName(u"pushButton_plot_filtered_criteria")
        self.pushButton_plot_filtered_criteria.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_filtered_criteria.setMaximumSize(QSize(100, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_plot_filtered_criteria.setFont(font2)
        self.pushButton_plot_filtered_criteria.setStyleSheet(u"")
        self.pushButton_plot_filtered_criteria.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_plot_filtered_criteria, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_21, 3, 0, 1, 1)

        self.label_second_criteria = QLabel(self.frame_14)
        self.label_second_criteria.setObjectName(u"label_second_criteria")
        self.label_second_criteria.setMinimumSize(QSize(0, 40))
        self.label_second_criteria.setMaximumSize(QSize(16777215, 52))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.label_second_criteria.setFont(font3)
        self.label_second_criteria.setFrameShape(QFrame.Shape.Box)
        self.label_second_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_second_criteria.setWordWrap(True)
        self.label_second_criteria.setMargin(6)

        self.gridLayout_9.addWidget(self.label_second_criteria, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_14, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_main)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 230))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 0)
        self.label_first_criteria = QLabel(self.frame_3)
        self.label_first_criteria.setObjectName(u"label_first_criteria")
        self.label_first_criteria.setMinimumSize(QSize(0, 40))
        self.label_first_criteria.setMaximumSize(QSize(16777215, 52))
        self.label_first_criteria.setFont(font3)
        self.label_first_criteria.setFrameShape(QFrame.Shape.Box)
        self.label_first_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_first_criteria.setWordWrap(True)
        self.label_first_criteria.setMargin(6)

        self.gridLayout_8.addWidget(self.label_first_criteria, 0, 0, 1, 1)

        self.frame_11 = QFrame(self.frame_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 32))
        self.frame_11.setMaximumSize(QSize(16777215, 32))
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_11)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_4 = QLabel(self.frame_11)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setWordWrap(True)

        self.gridLayout_7.addWidget(self.label_4, 0, 1, 1, 1)

        self.frame_12 = QFrame(self.frame_11)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_7.addWidget(self.frame_12, 0, 0, 1, 1)

        self.frame_13 = QFrame(self.frame_11)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_7.addWidget(self.frame_13, 0, 2, 1, 1)


        self.gridLayout_8.addWidget(self.frame_11, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(4)
        self.gridLayout_4.setVerticalSpacing(6)
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_7, 2, 1, 1, 1)

        self.lineEdit_compressor_node_id = QLineEdit(self.frame_5)
        self.lineEdit_compressor_node_id.setObjectName(u"lineEdit_compressor_node_id")
        self.lineEdit_compressor_node_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_compressor_node_id.setMaximumSize(QSize(100, 26))
        self.lineEdit_compressor_node_id.setFont(font1)
        self.lineEdit_compressor_node_id.setStyleSheet(u"")
        self.lineEdit_compressor_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_compressor_node_id, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_8, 0, 1, 1, 1)

        self.lineEdit_unfiltered_criteria = QLineEdit(self.frame_5)
        self.lineEdit_unfiltered_criteria.setObjectName(u"lineEdit_unfiltered_criteria")
        self.lineEdit_unfiltered_criteria.setMinimumSize(QSize(100, 26))
        self.lineEdit_unfiltered_criteria.setMaximumSize(QSize(100, 26))
        self.lineEdit_unfiltered_criteria.setFont(font1)
        self.lineEdit_unfiltered_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_unfiltered_criteria, 2, 2, 1, 1)

        self.lineEdit_pressure_ratio = QLineEdit(self.frame_5)
        self.lineEdit_pressure_ratio.setObjectName(u"lineEdit_pressure_ratio")
        self.lineEdit_pressure_ratio.setMinimumSize(QSize(100, 26))
        self.lineEdit_pressure_ratio.setMaximumSize(QSize(100, 26))
        self.lineEdit_pressure_ratio.setFont(font1)
        self.lineEdit_pressure_ratio.setStyleSheet(u"")
        self.lineEdit_pressure_ratio.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_pressure_ratio, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_8.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 40))
        self.frame_6.setMaximumSize(QSize(16777215, 40))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_6)
        self.gridLayout_6.setSpacing(2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_unfiltered_criteria = QPushButton(self.frame_6)
        self.pushButton_plot_unfiltered_criteria.setObjectName(u"pushButton_plot_unfiltered_criteria")
        self.pushButton_plot_unfiltered_criteria.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_unfiltered_criteria.setMaximumSize(QSize(100, 30))
        self.pushButton_plot_unfiltered_criteria.setFont(font2)
        self.pushButton_plot_unfiltered_criteria.setStyleSheet(u"")
        self.pushButton_plot_unfiltered_criteria.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_plot_unfiltered_criteria, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_6, 3, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_compressor_node_id, self.lineEdit_pressure_ratio)
        QWidget.setTabOrder(self.lineEdit_pressure_ratio, self.lineEdit_unfiltered_criteria)
        QWidget.setTabOrder(self.lineEdit_unfiltered_criteria, self.pushButton_plot_unfiltered_criteria)
        QWidget.setTabOrder(self.pushButton_plot_unfiltered_criteria, self.lineEdit_nozzle_id)
        QWidget.setTabOrder(self.lineEdit_nozzle_id, self.lineEdit_speed_of_sound)
        QWidget.setTabOrder(self.lineEdit_speed_of_sound, self.lineEdit_line_pressure)
        QWidget.setTabOrder(self.lineEdit_line_pressure, self.lineEdit_internal_diameter)
        QWidget.setTabOrder(self.lineEdit_internal_diameter, self.pushButton_plot_filtered_criteria)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Allowable pulsation levels", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">1</span> = (400 * a<span style=\" vertical-align:super;\">\u00bd</span>) / (350 * P<span style=\" vertical-align:sub;\">L </span>* D<span style=\" vertical-align:sub;\">in</span> * F<span style=\" vertical-align:sub;\">n</span>)<span style=\" vertical-align:super;\">\u00bd</span></p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Nozzle/Line node ID:</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">L</span> [bar abs.]:</p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>D<span style=\" vertical-align:sub;\">in</span> [mm]:</p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>a [m/s]:</p></body></html>", None))
        self.checkBox_prestudy_analysis.setText(QCoreApplication.translate("Form", u"Prestudy analysis", None))
        self.pushButton_plot_filtered_criteria.setText(QCoreApplication.translate("Form", u"Plot criteria", None))
        self.label_second_criteria.setText(QCoreApplication.translate("Form", u"Maximum Allowable Pulsation Limits at and Beyond Line-side Connections of Pulsation Suppression Devices", None))
        self.label_first_criteria.setText(QCoreApplication.translate("Form", u"Maximum Allowable Compressor Cylinder Flange Pressure Pulsation", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">cf</span> = min{3*R; 7}</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>R = P<span style=\" vertical-align:sub;\">disc</span>/P<span style=\" vertical-align:sub;\">suc</span>:</p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">cf</span> [%]:</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Compressor node ID:</p></body></html>", None))
        self.pushButton_plot_unfiltered_criteria.setText(QCoreApplication.translate("Form", u"Plot criteria", None))
    # retranslateUi



class AllowablePulsationsForReciprocatingCompressorInputs_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_14: QFrame
                                - (Layout): QGridLayout
                                        - frame_15: QFrame
                                            - (Layout): QGridLayout
                                                    - label_10: QLabel
                                                    - frame_16: QFrame
                                                    - frame_17: QFrame
                                        - frame_18: QFrame
                                            - (Layout): QGridLayout
                                                    - label_15: QLabel
                                                    - label_14: QLabel
                                                    - lineEdit_nozzle_id: QLineEdit
                                                    - lineEdit_line_pressure: QLineEdit
                                                    - lineEdit_internal_diameter: QLineEdit
                                                    - lineEdit_speed_of_sound: QLineEdit
                                                    - label_13: QLabel
                                                    - label_12: QLabel
                                                    - frame_19: QFrame
                                                        - (Layout): QGridLayout
                                                                - checkBox_prestudy_analysis: QCheckBox
                                        - frame_21: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_plot_filtered_criteria: QPushButton
                                        - label_second_criteria: QLabel
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label_first_criteria: QLabel
                                        - frame_11: QFrame
                                            - (Layout): QGridLayout
                                                    - label_4: QLabel
                                                    - frame_12: QFrame
                                                    - frame_13: QFrame
                                        - frame_5: QFrame
                                            - (Layout): QGridLayout
                                                    - label_5: QLabel
                                                    - label_7: QLabel
                                                    - lineEdit_compressor_node_id: QLineEdit
                                                    - label_8: QLabel
                                                    - lineEdit_unfiltered_criteria: QLineEdit
                                                    - lineEdit_pressure_ratio: QLineEdit
                                        - frame_6: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_plot_unfiltered_criteria: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
