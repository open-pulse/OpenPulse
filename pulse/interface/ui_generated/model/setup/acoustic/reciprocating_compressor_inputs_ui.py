# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reciprocating_compressor_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(598, 783)
        Dialog.setMinimumSize(QSize(500, 500))
        Dialog.setMaximumSize(QSize(600, 800))
        Dialog.setSizeGripEnabled(True)
        self.gridLayout_13 = QGridLayout(Dialog)
        self.gridLayout_13.setSpacing(4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.frame_18 = QFrame(Dialog)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 48))
        self.frame_18.setMaximumSize(QSize(16777215, 48))
        font = QFont()
        font.setPointSize(8)
        self.frame_18.setFont(font)
        self.frame_18.setFrameShape(QFrame.Shape.Box)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_18)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_18)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 32))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame_18, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 52))
        self.frame_2.setMaximumSize(QSize(16777215, 52))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_confirm = QPushButton(self.frame_2)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 30))
        self.pushButton_confirm.setMaximumSize(QSize(100, 30))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_confirm.setFont(font2)
        self.pushButton_confirm.setStyleSheet(u"")
        self.pushButton_confirm.setAutoDefault(False)
        self.pushButton_confirm.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_confirm, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_2)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame_2, 2, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(600, 1400))
        font3 = QFont()
        font3.setPointSize(1)
        self.frame.setFont(font3)
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 0))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_7)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_main = QTabWidget(self.frame_7)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(600, 800))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.tabWidget_main.setFont(font4)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_32 = QGridLayout(self.tab_setup)
        self.gridLayout_32.setSpacing(4)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(4, 8, 4, 8)
        self.scrollArea = QScrollArea(self.tab_setup)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 537, 938))
        self.gridLayout_11 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_all_parameters = QFrame(self.scrollAreaWidgetContents)
        self.frame_all_parameters.setObjectName(u"frame_all_parameters")
        self.frame_all_parameters.setMinimumSize(QSize(120, 0))
        self.frame_all_parameters.setMaximumSize(QSize(16777215, 16777215))
        self.frame_all_parameters.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_all_parameters.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_all_parameters)
        self.gridLayout_14.setSpacing(6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.label_47 = QLabel(self.frame_all_parameters)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(0, 28))
        self.label_47.setMaximumSize(QSize(16777215, 28))
        self.label_47.setFont(font4)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_47, 18, 3, 1, 1)

        self.spinBox_tdc1_crank_angle = QSpinBox(self.frame_all_parameters)
        self.spinBox_tdc1_crank_angle.setObjectName(u"spinBox_tdc1_crank_angle")
        self.spinBox_tdc1_crank_angle.setMinimumSize(QSize(120, 28))
        self.spinBox_tdc1_crank_angle.setMaximumSize(QSize(120, 28))
        self.spinBox_tdc1_crank_angle.setFont(font4)
        self.spinBox_tdc1_crank_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_tdc1_crank_angle.setMaximum(270)
        self.spinBox_tdc1_crank_angle.setSingleStep(90)

        self.gridLayout_14.addWidget(self.spinBox_tdc1_crank_angle, 14, 2, 1, 1)

        self.label_14 = QLabel(self.frame_all_parameters)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 28))
        self.label_14.setMaximumSize(QSize(16777215, 28))
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_14, 7, 3, 1, 1)

        self.label_8 = QLabel(self.frame_all_parameters)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 28))
        self.label_8.setMaximumSize(QSize(16777215, 28))
        self.label_8.setFont(font4)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_8, 3, 1, 1, 1)

        self.label_33 = QLabel(self.frame_all_parameters)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setMinimumSize(QSize(0, 28))
        self.label_33.setMaximumSize(QSize(16777215, 28))
        self.label_33.setFont(font4)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_33, 18, 1, 1, 1)

        self.label_48 = QLabel(self.frame_all_parameters)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font4)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_48, 4, 1, 1, 1)

        self.label_43 = QLabel(self.frame_all_parameters)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(0, 28))
        self.label_43.setMaximumSize(QSize(16777215, 28))
        self.label_43.setFont(font4)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_43, 15, 1, 1, 1)

        self.label_36 = QLabel(self.frame_all_parameters)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font4)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_36, 12, 3, 1, 1)

        self.label_16 = QLabel(self.frame_all_parameters)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        self.label_16.setFont(font4)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_16, 9, 3, 1, 1)

        self.label_30 = QLabel(self.frame_all_parameters)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(0, 28))
        self.label_30.setMaximumSize(QSize(16777215, 28))
        self.label_30.setFont(font4)
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_30, 16, 1, 1, 1)

        self.label_23 = QLabel(self.frame_all_parameters)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(0, 26))
        self.label_23.setMaximumSize(QSize(16777215, 26))
        self.label_23.setFont(font4)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_23, 9, 1, 1, 1)

        self.lineEdit_clearance_head_end = QLineEdit(self.frame_all_parameters)
        self.lineEdit_clearance_head_end.setObjectName(u"lineEdit_clearance_head_end")
        self.lineEdit_clearance_head_end.setMinimumSize(QSize(120, 28))
        self.lineEdit_clearance_head_end.setMaximumSize(QSize(120, 28))
        self.lineEdit_clearance_head_end.setFont(font4)
        self.lineEdit_clearance_head_end.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_clearance_head_end.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_clearance_head_end, 11, 2, 1, 1)

        self.spinBox_tdc2_crank_angle = QSpinBox(self.frame_all_parameters)
        self.spinBox_tdc2_crank_angle.setObjectName(u"spinBox_tdc2_crank_angle")
        self.spinBox_tdc2_crank_angle.setMinimumSize(QSize(120, 28))
        self.spinBox_tdc2_crank_angle.setMaximumSize(QSize(120, 28))
        self.spinBox_tdc2_crank_angle.setFont(font4)
        self.spinBox_tdc2_crank_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_tdc2_crank_angle.setMaximum(270)
        self.spinBox_tdc2_crank_angle.setSingleStep(90)

        self.gridLayout_14.addWidget(self.spinBox_tdc2_crank_angle, 15, 2, 1, 1)

        self.lineEdit_bore_diameter = QLineEdit(self.frame_all_parameters)
        self.lineEdit_bore_diameter.setObjectName(u"lineEdit_bore_diameter")
        self.lineEdit_bore_diameter.setMinimumSize(QSize(120, 28))
        self.lineEdit_bore_diameter.setMaximumSize(QSize(120, 28))
        self.lineEdit_bore_diameter.setFont(font4)
        self.lineEdit_bore_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_bore_diameter, 6, 2, 1, 1)

        self.label_45 = QLabel(self.frame_all_parameters)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(0, 28))
        self.label_45.setMaximumSize(QSize(16777215, 28))
        self.label_45.setFont(font4)
        self.label_45.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_45, 15, 3, 1, 1)

        self.label_28 = QLabel(self.frame_all_parameters)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 28))
        self.label_28.setMaximumSize(QSize(16777215, 28))
        self.label_28.setFont(font4)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_28, 14, 1, 1, 1)

        self.label_13 = QLabel(self.frame_all_parameters)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 28))
        self.label_13.setMaximumSize(QSize(16777215, 28))
        self.label_13.setFont(font4)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_13, 6, 3, 1, 1)

        self.label_31 = QLabel(self.frame_all_parameters)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font4)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_31, 11, 3, 1, 1)

        self.lineEdit_stroke = QLineEdit(self.frame_all_parameters)
        self.lineEdit_stroke.setObjectName(u"lineEdit_stroke")
        self.lineEdit_stroke.setMinimumSize(QSize(120, 28))
        self.lineEdit_stroke.setMaximumSize(QSize(120, 28))
        self.lineEdit_stroke.setFont(font4)
        self.lineEdit_stroke.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_stroke.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_stroke, 7, 2, 1, 1)

        self.label_35 = QLabel(self.frame_all_parameters)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(0, 28))
        self.label_35.setMaximumSize(QSize(16777215, 28))
        self.label_35.setFont(font4)
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_35, 12, 1, 1, 1)

        self.label_26 = QLabel(self.frame_all_parameters)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(0, 28))
        self.label_26.setMaximumSize(QSize(16777215, 28))
        self.label_26.setFont(font4)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_26, 10, 1, 1, 1)

        self.label_21 = QLabel(self.frame_all_parameters)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 28))
        self.label_21.setMaximumSize(QSize(16777215, 28))
        self.label_21.setFont(font4)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_21, 7, 1, 1, 1)

        self.lineEdit_rod_diameter = QLineEdit(self.frame_all_parameters)
        self.lineEdit_rod_diameter.setObjectName(u"lineEdit_rod_diameter")
        self.lineEdit_rod_diameter.setMinimumSize(QSize(120, 26))
        self.lineEdit_rod_diameter.setMaximumSize(QSize(120, 26))
        self.lineEdit_rod_diameter.setFont(font4)
        self.lineEdit_rod_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_rod_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_rod_diameter, 9, 2, 1, 1)

        self.label_20 = QLabel(self.frame_all_parameters)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(0, 28))
        self.label_20.setMaximumSize(QSize(16777215, 28))
        self.label_20.setFont(font4)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_20, 6, 1, 1, 1)

        self.label_34 = QLabel(self.frame_all_parameters)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(0, 28))
        self.label_34.setMaximumSize(QSize(16777215, 28))
        self.label_34.setFont(font4)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_34, 16, 3, 1, 1)

        self.lineEdit_rotational_speed = QLineEdit(self.frame_all_parameters)
        self.lineEdit_rotational_speed.setObjectName(u"lineEdit_rotational_speed")
        self.lineEdit_rotational_speed.setMinimumSize(QSize(120, 28))
        self.lineEdit_rotational_speed.setMaximumSize(QSize(120, 28))
        self.lineEdit_rotational_speed.setFont(font4)
        self.lineEdit_rotational_speed.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_rotational_speed.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_rotational_speed, 16, 2, 1, 1)

        self.lineEdit_connecting_rod_length = QLineEdit(self.frame_all_parameters)
        self.lineEdit_connecting_rod_length.setObjectName(u"lineEdit_connecting_rod_length")
        self.lineEdit_connecting_rod_length.setMinimumSize(QSize(120, 28))
        self.lineEdit_connecting_rod_length.setMaximumSize(QSize(120, 28))
        self.lineEdit_connecting_rod_length.setFont(font4)
        self.lineEdit_connecting_rod_length.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_connecting_rod_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_connecting_rod_length, 8, 2, 1, 1)

        self.label_27 = QLabel(self.frame_all_parameters)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(0, 28))
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setFont(font4)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_27, 11, 1, 1, 1)

        self.lineEdit_clearance_crank_end = QLineEdit(self.frame_all_parameters)
        self.lineEdit_clearance_crank_end.setObjectName(u"lineEdit_clearance_crank_end")
        self.lineEdit_clearance_crank_end.setMinimumSize(QSize(120, 28))
        self.lineEdit_clearance_crank_end.setMaximumSize(QSize(120, 28))
        self.lineEdit_clearance_crank_end.setFont(font4)
        self.lineEdit_clearance_crank_end.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_clearance_crank_end.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_clearance_crank_end, 12, 2, 1, 1)

        self.spinBox_capacity = QSpinBox(self.frame_all_parameters)
        self.spinBox_capacity.setObjectName(u"spinBox_capacity")
        self.spinBox_capacity.setMinimumSize(QSize(120, 28))
        self.spinBox_capacity.setMaximumSize(QSize(120, 28))
        self.spinBox_capacity.setFont(font4)
        self.spinBox_capacity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_capacity.setMinimum(20)
        self.spinBox_capacity.setMaximum(100)
        self.spinBox_capacity.setSingleStep(1)
        self.spinBox_capacity.setValue(100)

        self.gridLayout_14.addWidget(self.spinBox_capacity, 18, 2, 1, 1)

        self.label_15 = QLabel(self.frame_all_parameters)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font4)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_15, 8, 3, 1, 1)

        self.label_32 = QLabel(self.frame_all_parameters)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(0, 28))
        self.label_32.setMaximumSize(QSize(16777215, 28))
        self.label_32.setFont(font4)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_32, 14, 3, 1, 1)

        self.label_22 = QLabel(self.frame_all_parameters)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(0, 28))
        self.label_22.setMaximumSize(QSize(16777215, 28))
        self.label_22.setFont(font4)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_22, 8, 1, 1, 1)

        self.comboBox_cylinder_acting = QComboBox(self.frame_all_parameters)
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.setObjectName(u"comboBox_cylinder_acting")
        self.comboBox_cylinder_acting.setMinimumSize(QSize(120, 28))
        self.comboBox_cylinder_acting.setMaximumSize(QSize(120, 28))
        self.comboBox_cylinder_acting.setFont(font4)

        self.gridLayout_14.addWidget(self.comboBox_cylinder_acting, 4, 2, 1, 1)

        self.spinBox_number_of_cylinders = QSpinBox(self.frame_all_parameters)
        self.spinBox_number_of_cylinders.setObjectName(u"spinBox_number_of_cylinders")
        self.spinBox_number_of_cylinders.setMinimumSize(QSize(120, 28))
        self.spinBox_number_of_cylinders.setMaximumSize(QSize(120, 28))
        self.spinBox_number_of_cylinders.setFont(font4)
        self.spinBox_number_of_cylinders.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_cylinders.setMinimum(1)
        self.spinBox_number_of_cylinders.setMaximum(2)
        self.spinBox_number_of_cylinders.setSingleStep(1)
        self.spinBox_number_of_cylinders.setValue(1)

        self.gridLayout_14.addWidget(self.spinBox_number_of_cylinders, 5, 2, 1, 1)

        self.comboBox_stage = QComboBox(self.frame_all_parameters)
        self.comboBox_stage.addItem("")
        self.comboBox_stage.addItem("")
        self.comboBox_stage.addItem("")
        self.comboBox_stage.setObjectName(u"comboBox_stage")
        self.comboBox_stage.setMinimumSize(QSize(120, 28))
        self.comboBox_stage.setMaximumSize(QSize(120, 28))
        self.comboBox_stage.setFont(font4)

        self.gridLayout_14.addWidget(self.comboBox_stage, 3, 2, 1, 1)

        self.label_46 = QLabel(self.frame_all_parameters)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(0, 28))
        self.label_46.setMaximumSize(QSize(16777215, 28))
        self.label_46.setFont(font4)
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_46, 5, 1, 1, 1)

        self.lineEdit_pressure_ratio = QLineEdit(self.frame_all_parameters)
        self.lineEdit_pressure_ratio.setObjectName(u"lineEdit_pressure_ratio")
        self.lineEdit_pressure_ratio.setMinimumSize(QSize(120, 28))
        self.lineEdit_pressure_ratio.setMaximumSize(QSize(120, 28))
        self.lineEdit_pressure_ratio.setFont(font4)
        self.lineEdit_pressure_ratio.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_pressure_ratio.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_pressure_ratio, 10, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 2, 0, 1, 1)

        self.label_9 = QLabel(self.frame_all_parameters)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_9, 2, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_10, 2, 4, 1, 1)

        self.label_6 = QLabel(self.frame_all_parameters)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 32))
        self.label_6.setFont(font4)
        self.label_6.setFrameShape(QFrame.Shape.Box)
        self.label_6.setTextFormat(Qt.TextFormat.AutoText)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_6, 1, 1, 1, 3)

        self.comboBox_connection_type = QComboBox(self.frame_all_parameters)
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.setObjectName(u"comboBox_connection_type")
        self.comboBox_connection_type.setMinimumSize(QSize(120, 28))
        self.comboBox_connection_type.setMaximumSize(QSize(120, 28))
        self.comboBox_connection_type.setFont(font4)

        self.gridLayout_14.addWidget(self.comboBox_connection_type, 2, 2, 1, 1)

        self.pushButton_reset_entries = QPushButton(self.frame_all_parameters)
        self.pushButton_reset_entries.setObjectName(u"pushButton_reset_entries")
        self.pushButton_reset_entries.setMinimumSize(QSize(40, 28))
        self.pushButton_reset_entries.setMaximumSize(QSize(40, 28))
        icon = QIcon()
        icon.addFile(u":/icons/common/broom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_reset_entries.setIcon(icon)
        self.pushButton_reset_entries.setIconSize(QSize(20, 20))
        self.pushButton_reset_entries.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_reset_entries, 2, 3, 1, 1)


        self.gridLayout_11.addWidget(self.frame_all_parameters, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_suction_temperature_unit = QLabel(self.frame_3)
        self.label_suction_temperature_unit.setObjectName(u"label_suction_temperature_unit")
        self.label_suction_temperature_unit.setMinimumSize(QSize(84, 28))
        self.label_suction_temperature_unit.setMaximumSize(QSize(84, 28))
        self.label_suction_temperature_unit.setFont(font4)
        self.label_suction_temperature_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_suction_temperature_unit, 9, 3, 1, 1)

        self.label_51 = QLabel(self.frame_3)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 28))
        self.label_51.setMaximumSize(QSize(16777215, 28))
        self.label_51.setFont(font4)
        self.label_51.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_51, 7, 1, 1, 1)

        self.label_52 = QLabel(self.frame_3)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setMinimumSize(QSize(0, 28))
        self.label_52.setMaximumSize(QSize(16777215, 28))
        self.label_52.setFont(font4)
        self.label_52.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_52, 8, 1, 1, 1)

        self.label_molar_mass = QLabel(self.frame_3)
        self.label_molar_mass.setObjectName(u"label_molar_mass")
        self.label_molar_mass.setMinimumSize(QSize(0, 28))
        self.label_molar_mass.setMaximumSize(QSize(16777215, 28))
        self.label_molar_mass.setFont(font4)
        self.label_molar_mass.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_molar_mass, 4, 1, 1, 1)

        self.label_molar_mass_2 = QLabel(self.frame_3)
        self.label_molar_mass_2.setObjectName(u"label_molar_mass_2")
        self.label_molar_mass_2.setMinimumSize(QSize(0, 28))
        self.label_molar_mass_2.setMaximumSize(QSize(16777215, 28))
        self.label_molar_mass_2.setFont(font4)
        self.label_molar_mass_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_molar_mass_2, 1, 1, 1, 1)

        self.lineEdit_isentropic_exponent = QLineEdit(self.frame_3)
        self.lineEdit_isentropic_exponent.setObjectName(u"lineEdit_isentropic_exponent")
        self.lineEdit_isentropic_exponent.setMinimumSize(QSize(120, 28))
        self.lineEdit_isentropic_exponent.setMaximumSize(QSize(120, 28))
        self.lineEdit_isentropic_exponent.setFont(font4)
        self.lineEdit_isentropic_exponent.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_isentropic_exponent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_isentropic_exponent, 3, 2, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_3)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(120, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(120, 28))
        self.lineEdit_selected_fluid.setFont(font4)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_selected_fluid, 2, 2, 1, 1)

        self.label_42 = QLabel(self.frame_3)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(0, 28))
        self.label_42.setMaximumSize(QSize(16777215, 28))
        self.label_42.setFont(font4)
        self.label_42.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_42, 6, 1, 1, 1)

        self.comboBox_fluid_data_source = QComboBox(self.frame_3)
        self.comboBox_fluid_data_source.addItem("")
        self.comboBox_fluid_data_source.addItem("")
        self.comboBox_fluid_data_source.setObjectName(u"comboBox_fluid_data_source")
        self.comboBox_fluid_data_source.setMinimumSize(QSize(120, 28))
        self.comboBox_fluid_data_source.setMaximumSize(QSize(120, 28))
        self.comboBox_fluid_data_source.setFont(font4)

        self.gridLayout_3.addWidget(self.comboBox_fluid_data_source, 1, 2, 1, 1)

        self.label_50 = QLabel(self.frame_3)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 28))
        self.label_50.setMaximumSize(QSize(16777215, 28))
        self.label_50.setFont(font4)
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_50, 5, 1, 1, 1)

        self.label_44 = QLabel(self.frame_3)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(0, 28))
        self.label_44.setMaximumSize(QSize(16777215, 28))
        self.label_44.setFont(font4)
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_44, 9, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_3)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(0, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(16777215, 28))
        self.pushButton_get_fluid.setFont(font4)
        self.pushButton_get_fluid.setStyleSheet(u"")
        self.pushButton_get_fluid.setAutoDefault(False)
        self.pushButton_get_fluid.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_get_fluid, 2, 3, 1, 1)

        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 32))
        self.label_7.setFont(font4)
        self.label_7.setFrameShape(QFrame.Shape.Box)
        self.label_7.setTextFormat(Qt.TextFormat.AutoText)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 3)

        self.lineEdit_suction_pressure = QLineEdit(self.frame_3)
        self.lineEdit_suction_pressure.setObjectName(u"lineEdit_suction_pressure")
        self.lineEdit_suction_pressure.setMinimumSize(QSize(120, 28))
        self.lineEdit_suction_pressure.setMaximumSize(QSize(120, 28))
        self.lineEdit_suction_pressure.setFont(font4)
        self.lineEdit_suction_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_suction_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_suction_pressure, 6, 2, 1, 1)

        self.label_isentropic_exp = QLabel(self.frame_3)
        self.label_isentropic_exp.setObjectName(u"label_isentropic_exp")
        self.label_isentropic_exp.setMinimumSize(QSize(0, 28))
        self.label_isentropic_exp.setMaximumSize(QSize(16777215, 28))
        self.label_isentropic_exp.setFont(font4)
        self.label_isentropic_exp.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_isentropic_exp, 3, 1, 1, 1)

        self.label_suction_pressure_unit = QLabel(self.frame_3)
        self.label_suction_pressure_unit.setObjectName(u"label_suction_pressure_unit")
        self.label_suction_pressure_unit.setMinimumSize(QSize(84, 28))
        self.label_suction_pressure_unit.setMaximumSize(QSize(84, 28))
        self.label_suction_pressure_unit.setFont(font4)
        self.label_suction_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_suction_pressure_unit, 6, 3, 1, 1)

        self.lineEdit_molar_mass = QLineEdit(self.frame_3)
        self.lineEdit_molar_mass.setObjectName(u"lineEdit_molar_mass")
        self.lineEdit_molar_mass.setMinimumSize(QSize(120, 28))
        self.lineEdit_molar_mass.setMaximumSize(QSize(120, 28))
        self.lineEdit_molar_mass.setFont(font4)
        self.lineEdit_molar_mass.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_molar_mass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_molar_mass, 4, 2, 1, 1)

        self.label_molar_mass_3 = QLabel(self.frame_3)
        self.label_molar_mass_3.setObjectName(u"label_molar_mass_3")
        self.label_molar_mass_3.setMinimumSize(QSize(0, 28))
        self.label_molar_mass_3.setMaximumSize(QSize(16777215, 28))
        self.label_molar_mass_3.setFont(font4)
        self.label_molar_mass_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_molar_mass_3, 2, 1, 1, 1)

        self.label_molar_mass_unit = QLabel(self.frame_3)
        self.label_molar_mass_unit.setObjectName(u"label_molar_mass_unit")
        self.label_molar_mass_unit.setMinimumSize(QSize(84, 28))
        self.label_molar_mass_unit.setMaximumSize(QSize(84, 28))
        self.label_molar_mass_unit.setFont(font4)
        self.label_molar_mass_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_molar_mass_unit, 4, 3, 1, 1)

        self.label_discharge_pressure_unit = QLabel(self.frame_3)
        self.label_discharge_pressure_unit.setObjectName(u"label_discharge_pressure_unit")
        self.label_discharge_pressure_unit.setMinimumSize(QSize(84, 28))
        self.label_discharge_pressure_unit.setMaximumSize(QSize(84, 28))
        self.label_discharge_pressure_unit.setFont(font4)
        self.label_discharge_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_discharge_pressure_unit, 7, 3, 1, 1)

        self.lineEdit_discharge_pressure = QLineEdit(self.frame_3)
        self.lineEdit_discharge_pressure.setObjectName(u"lineEdit_discharge_pressure")
        self.lineEdit_discharge_pressure.setEnabled(False)
        self.lineEdit_discharge_pressure.setMinimumSize(QSize(120, 28))
        self.lineEdit_discharge_pressure.setMaximumSize(QSize(120, 28))
        self.lineEdit_discharge_pressure.setFont(font4)
        self.lineEdit_discharge_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_discharge_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_discharge_pressure, 7, 2, 1, 1)

        self.lineEdit_suction_temperature = QLineEdit(self.frame_3)
        self.lineEdit_suction_temperature.setObjectName(u"lineEdit_suction_temperature")
        self.lineEdit_suction_temperature.setMinimumSize(QSize(120, 28))
        self.lineEdit_suction_temperature.setMaximumSize(QSize(120, 28))
        self.lineEdit_suction_temperature.setFont(font4)
        self.lineEdit_suction_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_suction_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_suction_temperature, 9, 2, 1, 1)

        self.label_discharge_temperature_unit = QLabel(self.frame_3)
        self.label_discharge_temperature_unit.setObjectName(u"label_discharge_temperature_unit")
        self.label_discharge_temperature_unit.setMinimumSize(QSize(84, 28))
        self.label_discharge_temperature_unit.setMaximumSize(QSize(84, 28))
        self.label_discharge_temperature_unit.setFont(font4)
        self.label_discharge_temperature_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_discharge_temperature_unit, 10, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 4, 1, 1)

        self.label_53 = QLabel(self.frame_3)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setMinimumSize(QSize(0, 28))
        self.label_53.setMaximumSize(QSize(16777215, 28))
        self.label_53.setFont(font4)
        self.label_53.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_53, 10, 1, 1, 1)

        self.lineEdit_discharge_temperature = QLineEdit(self.frame_3)
        self.lineEdit_discharge_temperature.setObjectName(u"lineEdit_discharge_temperature")
        self.lineEdit_discharge_temperature.setMinimumSize(QSize(120, 28))
        self.lineEdit_discharge_temperature.setMaximumSize(QSize(120, 28))
        self.lineEdit_discharge_temperature.setFont(font4)
        self.lineEdit_discharge_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_discharge_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_discharge_temperature, 10, 2, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_3)
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.setObjectName(u"comboBox_pressure_units")
        self.comboBox_pressure_units.setMinimumSize(QSize(120, 28))
        self.comboBox_pressure_units.setMaximumSize(QSize(120, 28))
        self.comboBox_pressure_units.setFont(font4)

        self.gridLayout_3.addWidget(self.comboBox_pressure_units, 5, 2, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_3)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(120, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(120, 28))
        self.comboBox_temperature_units.setFont(font4)

        self.gridLayout_3.addWidget(self.comboBox_temperature_units, 8, 2, 1, 1)


        self.gridLayout_11.addWidget(self.frame_3, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_32.addWidget(self.scrollArea, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_advanced_options = QWidget()
        self.tab_advanced_options.setObjectName(u"tab_advanced_options")
        self.gridLayout_26 = QGridLayout(self.tab_advanced_options)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setHorizontalSpacing(2)
        self.gridLayout_26.setVerticalSpacing(6)
        self.gridLayout_26.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_2 = QScrollArea(self.tab_advanced_options)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 448, 512))
        self.gridLayout_18 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.frame_4 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 228))
        self.frame_4.setMaximumSize(QSize(16777215, 228))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label_39 = QLabel(self.frame_4)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMinimumSize(QSize(180, 28))
        self.label_39.setMaximumSize(QSize(180, 28))
        self.label_39.setFont(font4)
        self.label_39.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_39, 5, 1, 1, 1)

        self.comboBox_frequency_resolution = QComboBox(self.frame_4)
        self.comboBox_frequency_resolution.addItem("")
        self.comboBox_frequency_resolution.addItem("")
        self.comboBox_frequency_resolution.addItem("")
        self.comboBox_frequency_resolution.addItem("")
        self.comboBox_frequency_resolution.addItem("")
        self.comboBox_frequency_resolution.setObjectName(u"comboBox_frequency_resolution")
        self.comboBox_frequency_resolution.setMinimumSize(QSize(120, 28))
        self.comboBox_frequency_resolution.setMaximumSize(QSize(120, 28))
        self.comboBox_frequency_resolution.setFont(font4)
        self.comboBox_frequency_resolution.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.comboBox_frequency_resolution, 4, 2, 1, 1)

        self.spinBox_max_frequency = QSpinBox(self.frame_4)
        self.spinBox_max_frequency.setObjectName(u"spinBox_max_frequency")
        self.spinBox_max_frequency.setMinimumSize(QSize(120, 28))
        self.spinBox_max_frequency.setMaximumSize(QSize(120, 28))
        self.spinBox_max_frequency.setFont(font4)
        self.spinBox_max_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_max_frequency.setMinimum(100)
        self.spinBox_max_frequency.setMaximum(1000)
        self.spinBox_max_frequency.setSingleStep(10)
        self.spinBox_max_frequency.setValue(600)

        self.gridLayout.addWidget(self.spinBox_max_frequency, 3, 2, 1, 1)

        self.lineEdit_number_of_revolutions = QLineEdit(self.frame_4)
        self.lineEdit_number_of_revolutions.setObjectName(u"lineEdit_number_of_revolutions")
        self.lineEdit_number_of_revolutions.setEnabled(False)
        self.lineEdit_number_of_revolutions.setMinimumSize(QSize(120, 28))
        self.lineEdit_number_of_revolutions.setMaximumSize(QSize(120, 28))
        self.lineEdit_number_of_revolutions.setFont(font4)
        self.lineEdit_number_of_revolutions.setStyleSheet(u"")
        self.lineEdit_number_of_revolutions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_number_of_revolutions, 6, 2, 1, 1)

        self.lineEdit_frequency_resolution = QLineEdit(self.frame_4)
        self.lineEdit_frequency_resolution.setObjectName(u"lineEdit_frequency_resolution")
        self.lineEdit_frequency_resolution.setEnabled(False)
        self.lineEdit_frequency_resolution.setMinimumSize(QSize(120, 28))
        self.lineEdit_frequency_resolution.setMaximumSize(QSize(120, 28))
        self.lineEdit_frequency_resolution.setFont(font4)
        self.lineEdit_frequency_resolution.setStyleSheet(u"")
        self.lineEdit_frequency_resolution.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_frequency_resolution, 5, 2, 1, 1)

        self.label_40 = QLabel(self.frame_4)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(180, 28))
        self.label_40.setMaximumSize(QSize(180, 28))
        self.label_40.setFont(font4)
        self.label_40.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_40, 6, 1, 1, 1)

        self.label_38 = QLabel(self.frame_4)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMinimumSize(QSize(180, 28))
        self.label_38.setMaximumSize(QSize(180, 28))
        self.label_38.setFont(font4)
        self.label_38.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_38, 4, 1, 1, 1)

        self.label_41 = QLabel(self.frame_4)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(180, 28))
        self.label_41.setMaximumSize(QSize(180, 28))
        self.label_41.setFont(font4)
        self.label_41.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_41, 3, 1, 1, 1)

        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(400, 40))
        self.frame_6.setMaximumSize(QSize(480, 40))
        self.frame_6.setFrameShape(QFrame.Shape.Box)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_6)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_4, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_6, 1, 1, 1, 3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 6, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 6, 0, 1, 1)

        self.pushButton_process_aquisition_parameters = QPushButton(self.frame_4)
        self.pushButton_process_aquisition_parameters.setObjectName(u"pushButton_process_aquisition_parameters")
        self.pushButton_process_aquisition_parameters.setMinimumSize(QSize(72, 28))
        self.pushButton_process_aquisition_parameters.setMaximumSize(QSize(72, 28))
        self.pushButton_process_aquisition_parameters.setFont(font4)
        self.pushButton_process_aquisition_parameters.setStyleSheet(u"")
        self.pushButton_process_aquisition_parameters.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_process_aquisition_parameters, 6, 3, 1, 1)

        self.spinBox_number_of_points = QSpinBox(self.frame_4)
        self.spinBox_number_of_points.setObjectName(u"spinBox_number_of_points")
        self.spinBox_number_of_points.setMinimumSize(QSize(120, 28))
        self.spinBox_number_of_points.setMaximumSize(QSize(120, 28))
        self.spinBox_number_of_points.setFont(font4)
        self.spinBox_number_of_points.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_points.setMinimum(60)
        self.spinBox_number_of_points.setMaximum(10000)
        self.spinBox_number_of_points.setSingleStep(1)
        self.spinBox_number_of_points.setValue(1000)

        self.gridLayout.addWidget(self.spinBox_number_of_points, 2, 2, 1, 1)

        self.label_37 = QLabel(self.frame_4)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(180, 28))
        self.label_37.setMaximumSize(QSize(180, 28))
        self.label_37.setFont(font4)
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_37, 2, 1, 1, 1)


        self.gridLayout_18.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 260))
        self.frame_8.setMaximumSize(QSize(16777215, 260))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_8)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setVerticalSpacing(8)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_8)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(400, 40))
        self.frame_5.setMaximumSize(QSize(480, 40))
        self.frame_5.setFrameShape(QFrame.Shape.Box)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_5)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_17.addWidget(self.frame_5, 0, 1, 1, 2)

        self.tabWidget_plots_2 = QTabWidget(self.frame_8)
        self.tabWidget_plots_2.setObjectName(u"tabWidget_plots_2")
        self.tabWidget_plots_2.setMinimumSize(QSize(0, 180))
        self.tabWidget_plots_2.setMaximumSize(QSize(480, 180))
        self.tabWidget_plots_2.setFont(font4)
        self.tab_time_2 = QWidget()
        self.tab_time_2.setObjectName(u"tab_time_2")
        self.gridLayout_28 = QGridLayout(self.tab_time_2)
        self.gridLayout_28.setSpacing(4)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setContentsMargins(4, 4, 4, 4)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time = QPushButton(self.tab_time_2)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setObjectName(u"pushButton_plot_volumetric_flow_rate_at_discharge_time")
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setFont(font4)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setStyleSheet(u"")
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setAutoDefault(False)

        self.gridLayout_28.addWidget(self.pushButton_plot_volumetric_flow_rate_at_discharge_time, 1, 1, 1, 1)

        self.pushButton_plot_volumetric_flow_rate_at_suction_time = QPushButton(self.tab_time_2)
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setObjectName(u"pushButton_plot_volumetric_flow_rate_at_suction_time")
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setFont(font4)
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setStyleSheet(u"")
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setAutoDefault(False)

        self.gridLayout_28.addWidget(self.pushButton_plot_volumetric_flow_rate_at_suction_time, 1, 0, 1, 1)

        self.pushButton_plot_piston_position_and_velocity_time = QPushButton(self.tab_time_2)
        self.pushButton_plot_piston_position_and_velocity_time.setObjectName(u"pushButton_plot_piston_position_and_velocity_time")
        self.pushButton_plot_piston_position_and_velocity_time.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_piston_position_and_velocity_time.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_piston_position_and_velocity_time.setFont(font4)
        self.pushButton_plot_piston_position_and_velocity_time.setStyleSheet(u"")
        self.pushButton_plot_piston_position_and_velocity_time.setAutoDefault(False)

        self.gridLayout_28.addWidget(self.pushButton_plot_piston_position_and_velocity_time, 0, 0, 1, 1)

        self.pushButton_plot_rod_pressure_load_time = QPushButton(self.tab_time_2)
        self.pushButton_plot_rod_pressure_load_time.setObjectName(u"pushButton_plot_rod_pressure_load_time")
        self.pushButton_plot_rod_pressure_load_time.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_rod_pressure_load_time.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_rod_pressure_load_time.setFont(font4)
        self.pushButton_plot_rod_pressure_load_time.setStyleSheet(u"")
        self.pushButton_plot_rod_pressure_load_time.setAutoDefault(False)

        self.gridLayout_28.addWidget(self.pushButton_plot_rod_pressure_load_time, 0, 1, 1, 1)

        self.tabWidget_plots_2.addTab(self.tab_time_2, "")
        self.tab_angle_2 = QWidget()
        self.tab_angle_2.setObjectName(u"tab_angle_2")
        self.gridLayout_29 = QGridLayout(self.tab_angle_2)
        self.gridLayout_29.setSpacing(4)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setContentsMargins(4, 4, 4, 4)
        self.pushButton_plot_pressure_head_end_angle = QPushButton(self.tab_angle_2)
        self.pushButton_plot_pressure_head_end_angle.setObjectName(u"pushButton_plot_pressure_head_end_angle")
        self.pushButton_plot_pressure_head_end_angle.setEnabled(True)
        self.pushButton_plot_pressure_head_end_angle.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_pressure_head_end_angle.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_pressure_head_end_angle.setFont(font4)
        self.pushButton_plot_pressure_head_end_angle.setStyleSheet(u"")
        self.pushButton_plot_pressure_head_end_angle.setAutoDefault(False)

        self.gridLayout_29.addWidget(self.pushButton_plot_pressure_head_end_angle, 0, 0, 1, 1)

        self.pushButton_plot_volume_head_end_angle = QPushButton(self.tab_angle_2)
        self.pushButton_plot_volume_head_end_angle.setObjectName(u"pushButton_plot_volume_head_end_angle")
        self.pushButton_plot_volume_head_end_angle.setEnabled(True)
        self.pushButton_plot_volume_head_end_angle.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volume_head_end_angle.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volume_head_end_angle.setFont(font4)
        self.pushButton_plot_volume_head_end_angle.setStyleSheet(u"")
        self.pushButton_plot_volume_head_end_angle.setAutoDefault(False)

        self.gridLayout_29.addWidget(self.pushButton_plot_volume_head_end_angle, 0, 1, 1, 1)

        self.pushButton_plot_pressure_crank_end_angle = QPushButton(self.tab_angle_2)
        self.pushButton_plot_pressure_crank_end_angle.setObjectName(u"pushButton_plot_pressure_crank_end_angle")
        self.pushButton_plot_pressure_crank_end_angle.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_pressure_crank_end_angle.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_pressure_crank_end_angle.setFont(font4)
        self.pushButton_plot_pressure_crank_end_angle.setStyleSheet(u"")
        self.pushButton_plot_pressure_crank_end_angle.setAutoDefault(False)

        self.gridLayout_29.addWidget(self.pushButton_plot_pressure_crank_end_angle, 1, 0, 1, 1)

        self.pushButton_plot_volume_crank_end_angle = QPushButton(self.tab_angle_2)
        self.pushButton_plot_volume_crank_end_angle.setObjectName(u"pushButton_plot_volume_crank_end_angle")
        self.pushButton_plot_volume_crank_end_angle.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volume_crank_end_angle.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volume_crank_end_angle.setFont(font4)
        self.pushButton_plot_volume_crank_end_angle.setStyleSheet(u"")
        self.pushButton_plot_volume_crank_end_angle.setAutoDefault(False)

        self.gridLayout_29.addWidget(self.pushButton_plot_volume_crank_end_angle, 1, 1, 1, 1)

        self.tabWidget_plots_2.addTab(self.tab_angle_2, "")
        self.tab_frequency_2 = QWidget()
        self.tab_frequency_2.setObjectName(u"tab_frequency_2")
        self.gridLayout_33 = QGridLayout(self.tab_frequency_2)
        self.gridLayout_33.setSpacing(4)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(4, 4, 4, 4)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency = QPushButton(self.tab_frequency_2)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setObjectName(u"pushButton_plot_volumetric_flow_rate_at_discharge_frequency")
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setFont(font4)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setStyleSheet(u"")
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setAutoDefault(False)

        self.gridLayout_33.addWidget(self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency, 1, 1, 1, 1)

        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency = QPushButton(self.tab_frequency_2)
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setObjectName(u"pushButton_plot_volumetric_flow_rate_at_suction_frequency")
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setFont(font4)
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setStyleSheet(u"")
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setAutoDefault(False)

        self.gridLayout_33.addWidget(self.pushButton_plot_volumetric_flow_rate_at_suction_frequency, 1, 0, 1, 1)

        self.pushButton_plot_rod_pressure_load_frequency = QPushButton(self.tab_frequency_2)
        self.pushButton_plot_rod_pressure_load_frequency.setObjectName(u"pushButton_plot_rod_pressure_load_frequency")
        self.pushButton_plot_rod_pressure_load_frequency.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_rod_pressure_load_frequency.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_rod_pressure_load_frequency.setFont(font4)
        self.pushButton_plot_rod_pressure_load_frequency.setStyleSheet(u"")
        self.pushButton_plot_rod_pressure_load_frequency.setAutoDefault(False)

        self.gridLayout_33.addWidget(self.pushButton_plot_rod_pressure_load_frequency, 2, 0, 1, 1)

        self.tabWidget_plots_2.addTab(self.tab_frequency_2, "")
        self.tab_plot_PV_2 = QWidget()
        self.tab_plot_PV_2.setObjectName(u"tab_plot_PV_2")
        self.gridLayout_36 = QGridLayout(self.tab_plot_PV_2)
        self.gridLayout_36.setSpacing(4)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.gridLayout_36.setContentsMargins(4, 4, 4, 4)
        self.pushButton_plot_PV_diagram_both_ends = QPushButton(self.tab_plot_PV_2)
        self.pushButton_plot_PV_diagram_both_ends.setObjectName(u"pushButton_plot_PV_diagram_both_ends")
        self.pushButton_plot_PV_diagram_both_ends.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_both_ends.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_both_ends.setFont(font4)
        self.pushButton_plot_PV_diagram_both_ends.setStyleSheet(u"")
        self.pushButton_plot_PV_diagram_both_ends.setAutoDefault(False)

        self.gridLayout_36.addWidget(self.pushButton_plot_PV_diagram_both_ends, 2, 0, 1, 1)

        self.pushButton_plot_PV_diagram_crank_end = QPushButton(self.tab_plot_PV_2)
        self.pushButton_plot_PV_diagram_crank_end.setObjectName(u"pushButton_plot_PV_diagram_crank_end")
        self.pushButton_plot_PV_diagram_crank_end.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_crank_end.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_crank_end.setFont(font4)
        self.pushButton_plot_PV_diagram_crank_end.setStyleSheet(u"")
        self.pushButton_plot_PV_diagram_crank_end.setAutoDefault(False)

        self.gridLayout_36.addWidget(self.pushButton_plot_PV_diagram_crank_end, 0, 0, 1, 1)

        self.pushButton_plot_PV_diagram_head_end = QPushButton(self.tab_plot_PV_2)
        self.pushButton_plot_PV_diagram_head_end.setObjectName(u"pushButton_plot_PV_diagram_head_end")
        self.pushButton_plot_PV_diagram_head_end.setMinimumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_head_end.setMaximumSize(QSize(160, 48))
        self.pushButton_plot_PV_diagram_head_end.setFont(font4)
        self.pushButton_plot_PV_diagram_head_end.setStyleSheet(u"")
        self.pushButton_plot_PV_diagram_head_end.setAutoDefault(False)

        self.gridLayout_36.addWidget(self.pushButton_plot_PV_diagram_head_end, 0, 1, 1, 1)

        self.tabWidget_plots_2.addTab(self.tab_plot_PV_2, "")

        self.gridLayout_17.addWidget(self.tabWidget_plots_2, 1, 1, 1, 2)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_12, 0, 3, 1, 1)


        self.gridLayout_18.addWidget(self.frame_8, 1, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_26.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_advanced_options, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_9 = QGridLayout(self.tab_remove)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 6, 2, 2)
        self.frame_remove_selection = QFrame(self.tab_remove)
        self.frame_remove_selection.setObjectName(u"frame_remove_selection")
        self.frame_remove_selection.setMinimumSize(QSize(0, 40))
        self.frame_remove_selection.setMaximumSize(QSize(16777215, 72))
        self.frame_remove_selection.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_remove_selection.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_remove_selection)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_connection_type = QLineEdit(self.frame_remove_selection)
        self.lineEdit_connection_type.setObjectName(u"lineEdit_connection_type")
        self.lineEdit_connection_type.setEnabled(False)
        self.lineEdit_connection_type.setMinimumSize(QSize(130, 0))
        self.lineEdit_connection_type.setMaximumSize(QSize(130, 26))
        self.lineEdit_connection_type.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_connection_type.setStyleSheet(u"")
        self.lineEdit_connection_type.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_connection_type, 1, 2, 1, 1)

        self.label_3 = QLabel(self.frame_remove_selection)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(130, 0))
        self.label_3.setMaximumSize(QSize(130, 16777215))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)


        self.gridLayout_9.addWidget(self.frame_remove_selection, 0, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.tab_remove)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 0)
        self.treeWidget_nodal_info = QTreeWidget(self.frame_treeWidget)
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font5)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font5)
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_nodal_info.setMaximumSize(QSize(1000, 1000))
        self.treeWidget_nodal_info.setFont(font5)
        self.treeWidget_nodal_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.treeWidget_nodal_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.treeWidget_nodal_info.setIndentation(0)

        self.gridLayout_8.addWidget(self.treeWidget_nodal_info, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_treeWidget, 1, 0, 1, 1)

        self.frame_remove_buttons = QFrame(self.tab_remove)
        self.frame_remove_buttons.setObjectName(u"frame_remove_buttons")
        self.frame_remove_buttons.setMinimumSize(QSize(0, 48))
        self.frame_remove_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_remove_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_remove_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_remove_buttons)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_remove = QPushButton(self.frame_remove_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 30))
        self.pushButton_remove.setMaximumSize(QSize(100, 30))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_remove_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 30))
        self.pushButton_reset.setMaximumSize(QSize(100, 30))
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_remove_buttons, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_10.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_7, 1, 0, 1, 1)

        self.frame_selection_id = QFrame(self.frame)
        self.frame_selection_id.setObjectName(u"frame_selection_id")
        self.frame_selection_id.setMinimumSize(QSize(360, 40))
        self.frame_selection_id.setMaximumSize(QSize(16777215, 40))
        self.frame_selection_id.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selection_id.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_selection_id)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(8)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.lineEdit_selected_node_id = QLineEdit(self.frame_selection_id)
        self.lineEdit_selected_node_id.setObjectName(u"lineEdit_selected_node_id")
        self.lineEdit_selected_node_id.setMinimumSize(QSize(160, 26))
        self.lineEdit_selected_node_id.setMaximumSize(QSize(160, 26))
        self.lineEdit_selected_node_id.setFont(font4)
        self.lineEdit_selected_node_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_node_id.setStyleSheet(u"")
        self.lineEdit_selected_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_selected_node_id, 0, 2, 1, 1)

        self.label_5 = QLabel(self.frame_selection_id)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 26))
        self.label_5.setMaximumSize(QSize(16777215, 26))
        self.label_5.setFont(font4)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_5, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_selection_id, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.comboBox_stage)
        QWidget.setTabOrder(self.comboBox_stage, self.comboBox_cylinder_acting)
        QWidget.setTabOrder(self.comboBox_cylinder_acting, self.spinBox_number_of_cylinders)
        QWidget.setTabOrder(self.spinBox_number_of_cylinders, self.lineEdit_bore_diameter)
        QWidget.setTabOrder(self.lineEdit_bore_diameter, self.lineEdit_stroke)
        QWidget.setTabOrder(self.lineEdit_stroke, self.lineEdit_connecting_rod_length)
        QWidget.setTabOrder(self.lineEdit_connecting_rod_length, self.lineEdit_rod_diameter)
        QWidget.setTabOrder(self.lineEdit_rod_diameter, self.lineEdit_pressure_ratio)
        QWidget.setTabOrder(self.lineEdit_pressure_ratio, self.lineEdit_clearance_head_end)
        QWidget.setTabOrder(self.lineEdit_clearance_head_end, self.lineEdit_clearance_crank_end)
        QWidget.setTabOrder(self.lineEdit_clearance_crank_end, self.spinBox_tdc1_crank_angle)
        QWidget.setTabOrder(self.spinBox_tdc1_crank_angle, self.spinBox_tdc2_crank_angle)
        QWidget.setTabOrder(self.spinBox_tdc2_crank_angle, self.lineEdit_rotational_speed)
        QWidget.setTabOrder(self.lineEdit_rotational_speed, self.spinBox_capacity)
        QWidget.setTabOrder(self.spinBox_capacity, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.spinBox_max_frequency)
        QWidget.setTabOrder(self.spinBox_max_frequency, self.comboBox_frequency_resolution)
        QWidget.setTabOrder(self.comboBox_frequency_resolution, self.lineEdit_frequency_resolution)
        QWidget.setTabOrder(self.lineEdit_frequency_resolution, self.lineEdit_number_of_revolutions)
        QWidget.setTabOrder(self.lineEdit_number_of_revolutions, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.pushButton_confirm.setDefault(False)
        self.pushButton_exit.setDefault(False)
        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_connection_type.setCurrentIndex(1)
        self.comboBox_fluid_data_source.setCurrentIndex(0)
        self.pushButton_get_fluid.setDefault(True)
        self.comboBox_pressure_units.setCurrentIndex(4)
        self.comboBox_temperature_units.setCurrentIndex(1)
        self.comboBox_frequency_resolution.setCurrentIndex(4)
        self.tabWidget_plots_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Reciprocating compressor excitation", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Reciprocating compressor model setup", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Compression stage:", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Capacity:</p></body></html>", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"Active cylinder setup:", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">TDC crank angle (#2):</p></body></html>", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Rotational speed:</p></body></html>", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Rod diameter:</p></body></html>", None))
        self.lineEdit_clearance_head_end.setText(QCoreApplication.translate("Dialog", u"15.80", None))
        self.lineEdit_bore_diameter.setText(QCoreApplication.translate("Dialog", u"0.78", None))
        self.label_45.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[degree]</p></body></html>", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">TDC crank angle (#1):</p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
        self.lineEdit_stroke.setText(QCoreApplication.translate("Dialog", u"0.33", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Clearance (CE):</p></body></html>", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Pressure ratio (P<span style=\" vertical-align:sub;\">d</span>/P<span style=\" vertical-align:sub;\">s)</span>:</p></body></html>", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Stroke:</p></body></html>", None))
        self.lineEdit_rod_diameter.setText(QCoreApplication.translate("Dialog", u"0.135", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Cylinder bore diameter:</p></body></html>", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[rpm]</p></body></html>", None))
        self.lineEdit_rotational_speed.setText(QCoreApplication.translate("Dialog", u"360", None))
        self.lineEdit_connecting_rod_length.setText(QCoreApplication.translate("Dialog", u"1.25", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Clearance (HE):</p></body></html>", None))
        self.lineEdit_clearance_crank_end.setText(QCoreApplication.translate("Dialog", u"18.39", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[degree]</p></body></html>", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Connecting rod length:</p></body></html>", None))
        self.comboBox_cylinder_acting.setItemText(0, QCoreApplication.translate("Dialog", u" Both ends", None))
        self.comboBox_cylinder_acting.setItemText(1, QCoreApplication.translate("Dialog", u" Head end", None))
        self.comboBox_cylinder_acting.setItemText(2, QCoreApplication.translate("Dialog", u" Crank end", None))

        self.comboBox_stage.setItemText(0, QCoreApplication.translate("Dialog", u" First stage", None))
        self.comboBox_stage.setItemText(1, QCoreApplication.translate("Dialog", u" Second stage", None))
        self.comboBox_stage.setItemText(2, QCoreApplication.translate("Dialog", u" Third stage", None))

        self.label_46.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Number of cylinders:</p></body></html>", None))
        self.lineEdit_pressure_ratio.setText(QCoreApplication.translate("Dialog", u"1.90788804", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Reciprocating compressor parameters", None))
        self.comboBox_connection_type.setItemText(0, QCoreApplication.translate("Dialog", u" Suction", None))
        self.comboBox_connection_type.setItemText(1, QCoreApplication.translate("Dialog", u" Discharge", None))

#if QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Reset entries</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setText("")
        self.label_suction_temperature_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[\u00baC]</p></body></html>", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Discharge pressure:</p></body></html>", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Temprature unit:</p></body></html>", None))
        self.label_molar_mass.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Molar mass:</p></body></html>", None))
        self.label_molar_mass_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Fluid data source:</p></body></html>", None))
        self.lineEdit_isentropic_exponent.setText(QCoreApplication.translate("Dialog", u"1.4", None))
        self.lineEdit_selected_fluid.setText("")
        self.label_42.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Suction pressure:</p></body></html>", None))
        self.comboBox_fluid_data_source.setItemText(0, QCoreApplication.translate("Dialog", u"RefProp", None))
        self.comboBox_fluid_data_source.setItemText(1, QCoreApplication.translate("Dialog", u"User-defined", None))

        self.label_50.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Pressure unit:</p></body></html>", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Suction temperature:</p></body></html>", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Define the fluid properties", None))
        self.lineEdit_suction_pressure.setText(QCoreApplication.translate("Dialog", u"19.65", None))
        self.label_isentropic_exp.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Isentropic exponent (C<span style=\" vertical-align:sub;\">p</span>/C<span style=\" vertical-align:sub;\">v</span>):</p></body></html>", None))
        self.label_suction_pressure_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[kgf/cm\u00b2 (a)]</p></body></html>", None))
        self.lineEdit_molar_mass.setText(QCoreApplication.translate("Dialog", u"2.0158", None))
        self.label_molar_mass_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Selected working fluid:</p></body></html>", None))
        self.label_molar_mass_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[kg/kmol]</p></body></html>", None))
        self.label_discharge_pressure_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[kgf/cm\u00b2 (a)]</p></body></html>", None))
        self.lineEdit_discharge_pressure.setText(QCoreApplication.translate("Dialog", u"37.49", None))
        self.lineEdit_suction_temperature.setText(QCoreApplication.translate("Dialog", u"45", None))
        self.label_discharge_temperature_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[\u00baC]</p></body></html>", None))
        self.label_53.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Discharge temperature:</p></body></html>", None))
        self.lineEdit_discharge_temperature.setText(QCoreApplication.translate("Dialog", u"--", None))
        self.comboBox_pressure_units.setItemText(0, QCoreApplication.translate("Dialog", u"Pa (a)", None))
        self.comboBox_pressure_units.setItemText(1, QCoreApplication.translate("Dialog", u"kPa (a)", None))
        self.comboBox_pressure_units.setItemText(2, QCoreApplication.translate("Dialog", u"atm (a)", None))
        self.comboBox_pressure_units.setItemText(3, QCoreApplication.translate("Dialog", u"bar (a)", None))
        self.comboBox_pressure_units.setItemText(4, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (a)", None))
        self.comboBox_pressure_units.setItemText(5, QCoreApplication.translate("Dialog", u"psi (a)", None))
        self.comboBox_pressure_units.setItemText(6, QCoreApplication.translate("Dialog", u"ksi (a)", None))
        self.comboBox_pressure_units.setItemText(7, QCoreApplication.translate("Dialog", u"Pa (g)", None))
        self.comboBox_pressure_units.setItemText(8, QCoreApplication.translate("Dialog", u"kPa (g)", None))
        self.comboBox_pressure_units.setItemText(9, QCoreApplication.translate("Dialog", u"atm (g)", None))
        self.comboBox_pressure_units.setItemText(10, QCoreApplication.translate("Dialog", u"bar (g)", None))
        self.comboBox_pressure_units.setItemText(11, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (g)", None))
        self.comboBox_pressure_units.setItemText(12, QCoreApplication.translate("Dialog", u"psi (g)", None))
        self.comboBox_pressure_units.setItemText(13, QCoreApplication.translate("Dialog", u"ksi (g)", None))

        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"\u00b0C", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"\u00b0F", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.label_39.setText(QCoreApplication.translate("Dialog", u"Final frequency resolution:", None))
        self.comboBox_frequency_resolution.setItemText(0, QCoreApplication.translate("Dialog", u"    0.1 Hz", None))
        self.comboBox_frequency_resolution.setItemText(1, QCoreApplication.translate("Dialog", u"    0.2 Hz", None))
        self.comboBox_frequency_resolution.setItemText(2, QCoreApplication.translate("Dialog", u"    0.5Hz", None))
        self.comboBox_frequency_resolution.setItemText(3, QCoreApplication.translate("Dialog", u"    1.0 Hz", None))
        self.comboBox_frequency_resolution.setItemText(4, QCoreApplication.translate("Dialog", u"    2.0 Hz", None))

        self.label_40.setText(QCoreApplication.translate("Dialog", u"Number of revolutions:", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"Initial frequency resolution:", None))
        self.label_41.setText(QCoreApplication.translate("Dialog", u"Maximum frequency:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Signal processing controls", None))
#if QT_CONFIG(tooltip)
        self.pushButton_process_aquisition_parameters.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Press to process the aquisition parameters</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_process_aquisition_parameters.setText(QCoreApplication.translate("Dialog", u"Process", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"Points per revolution:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Plot controls", None))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate \n"
"at discharge", None))
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate \n"
"at suction", None))
        self.pushButton_plot_piston_position_and_velocity_time.setText(QCoreApplication.translate("Dialog", u"Piston position and \n"
"velocity", None))
        self.pushButton_plot_rod_pressure_load_time.setText(QCoreApplication.translate("Dialog", u"Rod pressure load", None))
        self.tabWidget_plots_2.setTabText(self.tabWidget_plots_2.indexOf(self.tab_time_2), QCoreApplication.translate("Dialog", u"Time", None))
        self.pushButton_plot_pressure_head_end_angle.setText(QCoreApplication.translate("Dialog", u"Pressure head end", None))
        self.pushButton_plot_volume_head_end_angle.setText(QCoreApplication.translate("Dialog", u"Volume head end", None))
        self.pushButton_plot_pressure_crank_end_angle.setText(QCoreApplication.translate("Dialog", u"Pressure crank end", None))
        self.pushButton_plot_volume_crank_end_angle.setText(QCoreApplication.translate("Dialog", u"Volume crank end", None))
        self.tabWidget_plots_2.setTabText(self.tabWidget_plots_2.indexOf(self.tab_angle_2), QCoreApplication.translate("Dialog", u"Angle", None))
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate \n"
"at discharge", None))
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate \n"
"at suction", None))
        self.pushButton_plot_rod_pressure_load_frequency.setText(QCoreApplication.translate("Dialog", u"Rod pressure load", None))
        self.tabWidget_plots_2.setTabText(self.tabWidget_plots_2.indexOf(self.tab_frequency_2), QCoreApplication.translate("Dialog", u"Frequency", None))
        self.pushButton_plot_PV_diagram_both_ends.setText(QCoreApplication.translate("Dialog", u"P-V diagram \n"
" both ends", None))
        self.pushButton_plot_PV_diagram_crank_end.setText(QCoreApplication.translate("Dialog", u"P-V diagram \n"
" crank end", None))
        self.pushButton_plot_PV_diagram_head_end.setText(QCoreApplication.translate("Dialog", u"P-V diagram \n"
" head end", None))
        self.tabWidget_plots_2.setTabText(self.tabWidget_plots_2.indexOf(self.tab_plot_PV_2), QCoreApplication.translate("Dialog", u"Pressure-Volume", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_advanced_options), QCoreApplication.translate("Dialog", u"Advanced options", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Connection", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Node ID", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", "")
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Selected node ID:", None))
    # retranslateUi



class ReciprocatingCompressorInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_18: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
                            - pushButton_exit: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_7: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_setup: QWidget
                                                - (Layout): QGridLayout
                                                        - scrollArea: QScrollArea
                                                            - scrollAreaWidgetContents: QWidget
                                                                - (Layout): QGridLayout
                                                                        - frame_all_parameters: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - label_47: QLabel
                                                                                    - spinBox_tdc1_crank_angle: QSpinBox
                                                                                    - label_14: QLabel
                                                                                    - label_8: QLabel
                                                                                    - label_33: QLabel
                                                                                    - label_48: QLabel
                                                                                    - label_43: QLabel
                                                                                    - label_36: QLabel
                                                                                    - label_16: QLabel
                                                                                    - label_30: QLabel
                                                                                    - label_23: QLabel
                                                                                    - lineEdit_clearance_head_end: QLineEdit
                                                                                    - spinBox_tdc2_crank_angle: QSpinBox
                                                                                    - lineEdit_bore_diameter: QLineEdit
                                                                                    - label_45: QLabel
                                                                                    - label_28: QLabel
                                                                                    - label_13: QLabel
                                                                                    - label_31: QLabel
                                                                                    - lineEdit_stroke: QLineEdit
                                                                                    - label_35: QLabel
                                                                                    - label_26: QLabel
                                                                                    - label_21: QLabel
                                                                                    - lineEdit_rod_diameter: QLineEdit
                                                                                    - label_20: QLabel
                                                                                    - label_34: QLabel
                                                                                    - lineEdit_rotational_speed: QLineEdit
                                                                                    - lineEdit_connecting_rod_length: QLineEdit
                                                                                    - label_27: QLabel
                                                                                    - lineEdit_clearance_crank_end: QLineEdit
                                                                                    - spinBox_capacity: QSpinBox
                                                                                    - label_15: QLabel
                                                                                    - label_32: QLabel
                                                                                    - label_22: QLabel
                                                                                    - comboBox_cylinder_acting: QComboBox
                                                                                    - spinBox_number_of_cylinders: QSpinBox
                                                                                    - comboBox_stage: QComboBox
                                                                                    - label_46: QLabel
                                                                                    - lineEdit_pressure_ratio: QLineEdit
                                                                                    - label_9: QLabel
                                                                                    - label_6: QLabel
                                                                                    - comboBox_connection_type: QComboBox
                                                                                    - pushButton_reset_entries: QPushButton
                                                                        - frame_3: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - label_suction_temperature_unit: QLabel
                                                                                    - label_51: QLabel
                                                                                    - label_52: QLabel
                                                                                    - label_molar_mass: QLabel
                                                                                    - label_molar_mass_2: QLabel
                                                                                    - lineEdit_isentropic_exponent: QLineEdit
                                                                                    - lineEdit_selected_fluid: QLineEdit
                                                                                    - label_42: QLabel
                                                                                    - comboBox_fluid_data_source: QComboBox
                                                                                    - label_50: QLabel
                                                                                    - label_44: QLabel
                                                                                    - pushButton_get_fluid: QPushButton
                                                                                    - label_7: QLabel
                                                                                    - lineEdit_suction_pressure: QLineEdit
                                                                                    - label_isentropic_exp: QLabel
                                                                                    - label_suction_pressure_unit: QLabel
                                                                                    - lineEdit_molar_mass: QLineEdit
                                                                                    - label_molar_mass_3: QLabel
                                                                                    - label_molar_mass_unit: QLabel
                                                                                    - label_discharge_pressure_unit: QLabel
                                                                                    - lineEdit_discharge_pressure: QLineEdit
                                                                                    - lineEdit_suction_temperature: QLineEdit
                                                                                    - label_discharge_temperature_unit: QLabel
                                                                                    - label_53: QLabel
                                                                                    - lineEdit_discharge_temperature: QLineEdit
                                                                                    - comboBox_pressure_units: QComboBox
                                                                                    - comboBox_temperature_units: QComboBox
                                            - tab_advanced_options: QWidget
                                                - (Layout): QGridLayout
                                                        - scrollArea_2: QScrollArea
                                                            - scrollAreaWidgetContents_2: QWidget
                                                                - (Layout): QGridLayout
                                                                        - frame_4: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - label_39: QLabel
                                                                                    - comboBox_frequency_resolution: QComboBox
                                                                                    - spinBox_max_frequency: QSpinBox
                                                                                    - lineEdit_number_of_revolutions: QLineEdit
                                                                                    - lineEdit_frequency_resolution: QLineEdit
                                                                                    - label_40: QLabel
                                                                                    - label_38: QLabel
                                                                                    - label_41: QLabel
                                                                                    - frame_6: QFrame
                                                                                        - (Layout): QGridLayout
                                                                                                - label_4: QLabel
                                                                                    - pushButton_process_aquisition_parameters: QPushButton
                                                                                    - spinBox_number_of_points: QSpinBox
                                                                                    - label_37: QLabel
                                                                        - frame_8: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - frame_5: QFrame
                                                                                        - (Layout): QGridLayout
                                                                                                - label_2: QLabel
                                                                                    - tabWidget_plots_2: QTabWidget
                                                                                        - tab_time_2: QWidget
                                                                                            - (Layout): QGridLayout
                                                                                                    - pushButton_plot_volumetric_flow_rate_at_discharge_time: QPushButton
                                                                                                    - pushButton_plot_volumetric_flow_rate_at_suction_time: QPushButton
                                                                                                    - pushButton_plot_piston_position_and_velocity_time: QPushButton
                                                                                                    - pushButton_plot_rod_pressure_load_time: QPushButton
                                                                                        - tab_angle_2: QWidget
                                                                                            - (Layout): QGridLayout
                                                                                                    - pushButton_plot_pressure_head_end_angle: QPushButton
                                                                                                    - pushButton_plot_volume_head_end_angle: QPushButton
                                                                                                    - pushButton_plot_pressure_crank_end_angle: QPushButton
                                                                                                    - pushButton_plot_volume_crank_end_angle: QPushButton
                                                                                        - tab_frequency_2: QWidget
                                                                                            - (Layout): QGridLayout
                                                                                                    - pushButton_plot_volumetric_flow_rate_at_discharge_frequency: QPushButton
                                                                                                    - pushButton_plot_volumetric_flow_rate_at_suction_frequency: QPushButton
                                                                                                    - pushButton_plot_rod_pressure_load_frequency: QPushButton
                                                                                        - tab_plot_PV_2: QWidget
                                                                                            - (Layout): QGridLayout
                                                                                                    - pushButton_plot_PV_diagram_both_ends: QPushButton
                                                                                                    - pushButton_plot_PV_diagram_crank_end: QPushButton
                                                                                                    - pushButton_plot_PV_diagram_head_end: QPushButton
                                            - tab_remove: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_remove_selection: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_connection_type: QLineEdit
                                                                    - label_3: QLabel
                                                        - frame_treeWidget: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_nodal_info: QTreeWidget
                                                        - frame_remove_buttons: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_remove: QPushButton
                                                                    - pushButton_reset: QPushButton
                            - frame_selection_id: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_node_id: QLineEdit
                                        - label_5: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
