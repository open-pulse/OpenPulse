# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reciprocating_pump_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(537, 641)
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
        self.tabWidget_main.setMaximumSize(QSize(600, 1200))
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 476, 842))
        self.gridLayout_11 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setMaximumSize(QSize(16777215, 80))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_process_fluctuating_volume = QPushButton(self.frame_3)
        self.pushButton_process_fluctuating_volume.setObjectName(u"pushButton_process_fluctuating_volume")
        self.pushButton_process_fluctuating_volume.setMinimumSize(QSize(0, 28))
        self.pushButton_process_fluctuating_volume.setMaximumSize(QSize(140, 28))
        self.pushButton_process_fluctuating_volume.setFont(font4)
        self.pushButton_process_fluctuating_volume.setStyleSheet(u"")
        self.pushButton_process_fluctuating_volume.setAutoDefault(False)
        self.pushButton_process_fluctuating_volume.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_process_fluctuating_volume, 0, 1, 1, 1)

        self.pushButton_plot_fluctuating_volume = QPushButton(self.frame_3)
        self.pushButton_plot_fluctuating_volume.setObjectName(u"pushButton_plot_fluctuating_volume")
        self.pushButton_plot_fluctuating_volume.setMinimumSize(QSize(0, 28))
        self.pushButton_plot_fluctuating_volume.setMaximumSize(QSize(140, 28))
        self.pushButton_plot_fluctuating_volume.setFont(font4)
        self.pushButton_plot_fluctuating_volume.setStyleSheet(u"")
        self.pushButton_plot_fluctuating_volume.setAutoDefault(False)
        self.pushButton_plot_fluctuating_volume.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_plot_fluctuating_volume, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.pushButton_pulsation_damper_calculator = QPushButton(self.frame_6)
        self.pushButton_pulsation_damper_calculator.setObjectName(u"pushButton_pulsation_damper_calculator")
        self.pushButton_pulsation_damper_calculator.setMinimumSize(QSize(0, 28))
        self.pushButton_pulsation_damper_calculator.setMaximumSize(QSize(240, 28))
        self.pushButton_pulsation_damper_calculator.setFont(font4)
        self.pushButton_pulsation_damper_calculator.setStyleSheet(u"")
        self.pushButton_pulsation_damper_calculator.setAutoDefault(False)
        self.pushButton_pulsation_damper_calculator.setFlat(False)

        self.gridLayout_15.addWidget(self.pushButton_pulsation_damper_calculator, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 1, 0, 1, 2)


        self.gridLayout_11.addWidget(self.frame_3, 2, 0, 1, 1)

        self.frame_all_parameters = QFrame(self.scrollAreaWidgetContents)
        self.frame_all_parameters.setObjectName(u"frame_all_parameters")
        self.frame_all_parameters.setMaximumSize(QSize(16777215, 480))
        self.frame_all_parameters.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_all_parameters.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_all_parameters)
        self.gridLayout_14.setSpacing(6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.comboBox_cylinder_acting = QComboBox(self.frame_all_parameters)
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.addItem("")
        self.comboBox_cylinder_acting.setObjectName(u"comboBox_cylinder_acting")
        self.comboBox_cylinder_acting.setMinimumSize(QSize(0, 28))
        self.comboBox_cylinder_acting.setMaximumSize(QSize(140, 28))
        self.comboBox_cylinder_acting.setFont(font4)

        self.gridLayout_14.addWidget(self.comboBox_cylinder_acting, 4, 2, 1, 1)

        self.lineEdit_stroke = QLineEdit(self.frame_all_parameters)
        self.lineEdit_stroke.setObjectName(u"lineEdit_stroke")
        self.lineEdit_stroke.setMinimumSize(QSize(110, 28))
        self.lineEdit_stroke.setMaximumSize(QSize(140, 28))
        self.lineEdit_stroke.setFont(font4)
        self.lineEdit_stroke.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_stroke.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_stroke, 7, 2, 1, 1)

        self.spinBox_number_of_cylinders = QSpinBox(self.frame_all_parameters)
        self.spinBox_number_of_cylinders.setObjectName(u"spinBox_number_of_cylinders")
        self.spinBox_number_of_cylinders.setMinimumSize(QSize(0, 28))
        self.spinBox_number_of_cylinders.setMaximumSize(QSize(140, 28))
        self.spinBox_number_of_cylinders.setFont(font4)
        self.spinBox_number_of_cylinders.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_cylinders.setMinimum(1)
        self.spinBox_number_of_cylinders.setMaximum(20)
        self.spinBox_number_of_cylinders.setSingleStep(1)
        self.spinBox_number_of_cylinders.setValue(5)

        self.gridLayout_14.addWidget(self.spinBox_number_of_cylinders, 5, 2, 1, 1)

        self.label_22 = QLabel(self.frame_all_parameters)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(0, 28))
        self.label_22.setMaximumSize(QSize(16777215, 28))
        self.label_22.setFont(font4)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_22, 8, 1, 1, 1)

        self.label_46 = QLabel(self.frame_all_parameters)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(0, 28))
        self.label_46.setMaximumSize(QSize(16777215, 28))
        self.label_46.setFont(font4)
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_46, 5, 1, 1, 1)

        self.label_34 = QLabel(self.frame_all_parameters)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setMinimumSize(QSize(0, 28))
        self.label_34.setMaximumSize(QSize(16777215, 28))
        self.label_34.setFont(font4)
        self.label_34.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_34, 14, 3, 1, 1)

        self.label_13 = QLabel(self.frame_all_parameters)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 28))
        self.label_13.setMaximumSize(QSize(16777215, 28))
        self.label_13.setFont(font4)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_13, 6, 3, 1, 1)

        self.label_36 = QLabel(self.frame_all_parameters)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 28))
        self.label_36.setMaximumSize(QSize(16777215, 28))
        self.label_36.setFont(font4)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_36, 11, 3, 1, 1)

        self.label_16 = QLabel(self.frame_all_parameters)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        self.label_16.setFont(font4)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_16, 9, 3, 1, 1)

        self.label_35 = QLabel(self.frame_all_parameters)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(0, 28))
        self.label_35.setMaximumSize(QSize(16777215, 28))
        self.label_35.setFont(font4)
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_35, 11, 1, 1, 1)

        self.lineEdit_bore_diameter = QLineEdit(self.frame_all_parameters)
        self.lineEdit_bore_diameter.setObjectName(u"lineEdit_bore_diameter")
        self.lineEdit_bore_diameter.setMinimumSize(QSize(110, 28))
        self.lineEdit_bore_diameter.setMaximumSize(QSize(140, 28))
        self.lineEdit_bore_diameter.setFont(font4)
        self.lineEdit_bore_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_bore_diameter, 6, 2, 1, 1)

        self.lineEdit_rod_diameter = QLineEdit(self.frame_all_parameters)
        self.lineEdit_rod_diameter.setObjectName(u"lineEdit_rod_diameter")
        self.lineEdit_rod_diameter.setMinimumSize(QSize(110, 26))
        self.lineEdit_rod_diameter.setMaximumSize(QSize(140, 26))
        self.lineEdit_rod_diameter.setFont(font4)
        self.lineEdit_rod_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_rod_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_rod_diameter, 9, 2, 1, 1)

        self.label_23 = QLabel(self.frame_all_parameters)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(0, 26))
        self.label_23.setMaximumSize(QSize(16777215, 26))
        self.label_23.setFont(font4)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_23, 9, 1, 1, 1)

        self.label_28 = QLabel(self.frame_all_parameters)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 28))
        self.label_28.setMaximumSize(QSize(16777215, 28))
        self.label_28.setFont(font4)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_28, 13, 1, 1, 1)

        self.label_31 = QLabel(self.frame_all_parameters)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMinimumSize(QSize(0, 28))
        self.label_31.setMaximumSize(QSize(16777215, 28))
        self.label_31.setFont(font4)
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_31, 10, 3, 1, 1)

        self.label_21 = QLabel(self.frame_all_parameters)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 28))
        self.label_21.setMaximumSize(QSize(16777215, 28))
        self.label_21.setFont(font4)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_21, 7, 1, 1, 1)

        self.label_14 = QLabel(self.frame_all_parameters)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 28))
        self.label_14.setMaximumSize(QSize(16777215, 28))
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_14, 7, 3, 1, 1)

        self.label_48 = QLabel(self.frame_all_parameters)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(0, 28))
        self.label_48.setMaximumSize(QSize(16777215, 28))
        self.label_48.setFont(font4)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_48, 4, 1, 1, 1)

        self.spinBox_tdc_crank_angle_1 = QSpinBox(self.frame_all_parameters)
        self.spinBox_tdc_crank_angle_1.setObjectName(u"spinBox_tdc_crank_angle_1")
        self.spinBox_tdc_crank_angle_1.setMinimumSize(QSize(0, 28))
        self.spinBox_tdc_crank_angle_1.setMaximumSize(QSize(140, 28))
        self.spinBox_tdc_crank_angle_1.setFont(font4)
        self.spinBox_tdc_crank_angle_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_tdc_crank_angle_1.setMaximum(270)
        self.spinBox_tdc_crank_angle_1.setSingleStep(1)

        self.gridLayout_14.addWidget(self.spinBox_tdc_crank_angle_1, 13, 2, 1, 1)

        self.label_9 = QLabel(self.frame_all_parameters)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_9, 1, 1, 1, 1)

        self.label_30 = QLabel(self.frame_all_parameters)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(0, 28))
        self.label_30.setMaximumSize(QSize(16777215, 28))
        self.label_30.setFont(font4)
        self.label_30.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_30, 14, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_10, 1, 4, 1, 1)

        self.label_32 = QLabel(self.frame_all_parameters)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setMinimumSize(QSize(0, 28))
        self.label_32.setMaximumSize(QSize(16777215, 28))
        self.label_32.setFont(font4)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_32, 13, 3, 1, 1)

        self.label_27 = QLabel(self.frame_all_parameters)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(0, 28))
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setFont(font4)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_27, 10, 1, 1, 1)

        self.label_15 = QLabel(self.frame_all_parameters)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font4)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_15, 8, 3, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 1, 0, 1, 1)

        self.lineEdit_connecting_rod_length = QLineEdit(self.frame_all_parameters)
        self.lineEdit_connecting_rod_length.setObjectName(u"lineEdit_connecting_rod_length")
        self.lineEdit_connecting_rod_length.setMinimumSize(QSize(110, 28))
        self.lineEdit_connecting_rod_length.setMaximumSize(QSize(140, 28))
        self.lineEdit_connecting_rod_length.setFont(font4)
        self.lineEdit_connecting_rod_length.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_connecting_rod_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_connecting_rod_length, 8, 2, 1, 1)

        self.label_20 = QLabel(self.frame_all_parameters)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(0, 28))
        self.label_20.setMaximumSize(QSize(16777215, 28))
        self.label_20.setFont(font4)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_20, 6, 1, 1, 1)

        self.comboBox_connection_type = QComboBox(self.frame_all_parameters)
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.addItem("")
        self.comboBox_connection_type.setObjectName(u"comboBox_connection_type")
        self.comboBox_connection_type.setMinimumSize(QSize(140, 28))
        self.comboBox_connection_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_connection_type.setFont(font4)

        self.gridLayout_14.addWidget(self.comboBox_connection_type, 1, 2, 1, 1)

        self.label_6 = QLabel(self.frame_all_parameters)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 32))
        self.label_6.setMaximumSize(QSize(16777215, 32))
        self.label_6.setFont(font4)
        self.label_6.setFrameShape(QFrame.Shape.Box)
        self.label_6.setTextFormat(Qt.TextFormat.AutoText)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_6, 0, 1, 1, 3)

        self.pushButton_reset_entries = QPushButton(self.frame_all_parameters)
        self.pushButton_reset_entries.setObjectName(u"pushButton_reset_entries")
        self.pushButton_reset_entries.setMinimumSize(QSize(40, 28))
        self.pushButton_reset_entries.setMaximumSize(QSize(40, 28))
        icon = Icon(u":/icons/common/broom.png")
        self.pushButton_reset_entries.setIcon(icon)
        self.pushButton_reset_entries.setIconSize(QSize(22, 22))
        self.pushButton_reset_entries.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_reset_entries, 1, 3, 1, 1)

        self.doubleSpinBox_clearance_head_end = QDoubleSpinBox(self.frame_all_parameters)
        self.doubleSpinBox_clearance_head_end.setObjectName(u"doubleSpinBox_clearance_head_end")
        self.doubleSpinBox_clearance_head_end.setMinimumSize(QSize(110, 28))
        self.doubleSpinBox_clearance_head_end.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_clearance_head_end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_clearance_head_end.setDecimals(4)
        self.doubleSpinBox_clearance_head_end.setMinimum(0.000000000000000)
        self.doubleSpinBox_clearance_head_end.setMaximum(10000.000000000000000)
        self.doubleSpinBox_clearance_head_end.setSingleStep(10.000000000000000)
        self.doubleSpinBox_clearance_head_end.setValue(15.800000000000001)

        self.gridLayout_14.addWidget(self.doubleSpinBox_clearance_head_end, 10, 2, 1, 1)

        self.doubleSpinBox_clearance_crank_end = QDoubleSpinBox(self.frame_all_parameters)
        self.doubleSpinBox_clearance_crank_end.setObjectName(u"doubleSpinBox_clearance_crank_end")
        self.doubleSpinBox_clearance_crank_end.setMinimumSize(QSize(110, 28))
        self.doubleSpinBox_clearance_crank_end.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_clearance_crank_end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_clearance_crank_end.setDecimals(4)
        self.doubleSpinBox_clearance_crank_end.setMinimum(0.000000000000000)
        self.doubleSpinBox_clearance_crank_end.setMaximum(10000.000000000000000)
        self.doubleSpinBox_clearance_crank_end.setSingleStep(10.000000000000000)
        self.doubleSpinBox_clearance_crank_end.setValue(18.390000000000001)

        self.gridLayout_14.addWidget(self.doubleSpinBox_clearance_crank_end, 11, 2, 1, 1)

        self.doubleSpinBox_rotational_speed = QDoubleSpinBox(self.frame_all_parameters)
        self.doubleSpinBox_rotational_speed.setObjectName(u"doubleSpinBox_rotational_speed")
        self.doubleSpinBox_rotational_speed.setMinimumSize(QSize(110, 28))
        self.doubleSpinBox_rotational_speed.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_rotational_speed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_rotational_speed.setDecimals(6)
        self.doubleSpinBox_rotational_speed.setMinimum(0.010000000000000)
        self.doubleSpinBox_rotational_speed.setMaximum(10000.000000000000000)
        self.doubleSpinBox_rotational_speed.setSingleStep(10.000000000000000)
        self.doubleSpinBox_rotational_speed.setValue(178.000000000000000)

        self.gridLayout_14.addWidget(self.doubleSpinBox_rotational_speed, 14, 2, 1, 1)


        self.gridLayout_11.addWidget(self.frame_all_parameters, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_5)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.lineEdit_suction_pressure = QLineEdit(self.frame_5)
        self.lineEdit_suction_pressure.setObjectName(u"lineEdit_suction_pressure")
        self.lineEdit_suction_pressure.setMinimumSize(QSize(110, 28))
        self.lineEdit_suction_pressure.setMaximumSize(QSize(140, 28))
        self.lineEdit_suction_pressure.setFont(font4)
        self.lineEdit_suction_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_suction_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_suction_pressure, 4, 2, 1, 1)

        self.lineEdit_bulk_modulus = QLineEdit(self.frame_5)
        self.lineEdit_bulk_modulus.setObjectName(u"lineEdit_bulk_modulus")
        self.lineEdit_bulk_modulus.setMinimumSize(QSize(110, 28))
        self.lineEdit_bulk_modulus.setMaximumSize(QSize(140, 28))
        self.lineEdit_bulk_modulus.setFont(font4)
        self.lineEdit_bulk_modulus.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_bulk_modulus.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_bulk_modulus, 2, 2, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 32))
        self.label_10.setMaximumSize(QSize(16777215, 32))
        self.label_10.setFont(font4)
        self.label_10.setFrameShape(QFrame.Shape.Box)
        self.label_10.setTextFormat(Qt.TextFormat.AutoText)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.label_10, 0, 1, 1, 3)

        self.lineEdit_discharge_pressure = QLineEdit(self.frame_5)
        self.lineEdit_discharge_pressure.setObjectName(u"lineEdit_discharge_pressure")
        self.lineEdit_discharge_pressure.setMinimumSize(QSize(110, 28))
        self.lineEdit_discharge_pressure.setMaximumSize(QSize(140, 28))
        self.lineEdit_discharge_pressure.setFont(font4)
        self.lineEdit_discharge_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_discharge_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_discharge_pressure, 5, 2, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_5)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(110, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(140, 28))
        self.comboBox_temperature_units.setFont(font4)

        self.gridLayout_18.addWidget(self.comboBox_temperature_units, 6, 2, 1, 1)

        self.label_discharge_pressure_unit = QLabel(self.frame_5)
        self.label_discharge_pressure_unit.setObjectName(u"label_discharge_pressure_unit")
        self.label_discharge_pressure_unit.setMinimumSize(QSize(80, 26))
        self.label_discharge_pressure_unit.setMaximumSize(QSize(80, 26))
        self.label_discharge_pressure_unit.setFont(font4)
        self.label_discharge_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_discharge_pressure_unit, 5, 3, 1, 1)

        self.lineEdit_suction_temperature = QLineEdit(self.frame_5)
        self.lineEdit_suction_temperature.setObjectName(u"lineEdit_suction_temperature")
        self.lineEdit_suction_temperature.setMinimumSize(QSize(110, 28))
        self.lineEdit_suction_temperature.setMaximumSize(QSize(140, 28))
        self.lineEdit_suction_temperature.setFont(font4)
        self.lineEdit_suction_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_suction_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_suction_temperature, 7, 2, 1, 1)

        self.label_59 = QLabel(self.frame_5)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setMinimumSize(QSize(0, 28))
        self.label_59.setMaximumSize(QSize(16777215, 28))
        self.label_59.setFont(font4)
        self.label_59.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.label_59, 7, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_13, 1, 4, 1, 1)

        self.label_61 = QLabel(self.frame_5)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setMinimumSize(QSize(0, 28))
        self.label_61.setMaximumSize(QSize(16777215, 28))
        self.label_61.setFont(font4)
        self.label_61.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_61, 6, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_5)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(110, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(140, 28))
        self.lineEdit_selected_fluid.setFont(font4)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_selected_fluid, 1, 2, 1, 1)

        self.lineEdit_discharge_temperature = QLineEdit(self.frame_5)
        self.lineEdit_discharge_temperature.setObjectName(u"lineEdit_discharge_temperature")
        self.lineEdit_discharge_temperature.setMinimumSize(QSize(110, 28))
        self.lineEdit_discharge_temperature.setMaximumSize(QSize(140, 28))
        self.lineEdit_discharge_temperature.setFont(font4)
        self.lineEdit_discharge_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_discharge_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_discharge_temperature, 8, 2, 1, 1)

        self.lineEdit_fluctuating_volume = QLineEdit(self.frame_5)
        self.lineEdit_fluctuating_volume.setObjectName(u"lineEdit_fluctuating_volume")
        self.lineEdit_fluctuating_volume.setEnabled(True)
        self.lineEdit_fluctuating_volume.setMinimumSize(QSize(110, 28))
        self.lineEdit_fluctuating_volume.setMaximumSize(QSize(140, 28))
        self.lineEdit_fluctuating_volume.setFont(font4)
        self.lineEdit_fluctuating_volume.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_fluctuating_volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_fluctuating_volume, 9, 2, 1, 1)

        self.label_57 = QLabel(self.frame_5)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setMinimumSize(QSize(0, 28))
        self.label_57.setMaximumSize(QSize(16777215, 28))
        self.label_57.setFont(font4)
        self.label_57.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_57, 5, 1, 1, 1)

        self.label_60 = QLabel(self.frame_5)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setMinimumSize(QSize(0, 28))
        self.label_60.setMaximumSize(QSize(16777215, 28))
        self.label_60.setFont(font4)
        self.label_60.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_18.addWidget(self.label_60, 8, 1, 1, 1)

        self.label_suction_pressure_unit = QLabel(self.frame_5)
        self.label_suction_pressure_unit.setObjectName(u"label_suction_pressure_unit")
        self.label_suction_pressure_unit.setMinimumSize(QSize(80, 26))
        self.label_suction_pressure_unit.setMaximumSize(QSize(80, 26))
        self.label_suction_pressure_unit.setFont(font4)
        self.label_suction_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_suction_pressure_unit, 4, 3, 1, 1)

        self.label_58 = QLabel(self.frame_5)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setMinimumSize(QSize(0, 28))
        self.label_58.setMaximumSize(QSize(16777215, 28))
        self.label_58.setFont(font4)
        self.label_58.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_58, 4, 1, 1, 1)

        self.label_62 = QLabel(self.frame_5)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setMinimumSize(QSize(0, 28))
        self.label_62.setMaximumSize(QSize(16777215, 28))
        self.label_62.setFont(font4)
        self.label_62.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_62, 3, 1, 1, 1)

        self.label_discharge_temperature_unit = QLabel(self.frame_5)
        self.label_discharge_temperature_unit.setObjectName(u"label_discharge_temperature_unit")
        self.label_discharge_temperature_unit.setMinimumSize(QSize(80, 26))
        self.label_discharge_temperature_unit.setMaximumSize(QSize(80, 26))
        self.label_discharge_temperature_unit.setFont(font4)
        self.label_discharge_temperature_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_discharge_temperature_unit, 8, 3, 1, 1)

        self.pushButton_get_fluid = QPushButton(self.frame_5)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(0, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(16777215, 28))
        self.pushButton_get_fluid.setFont(font4)
        self.pushButton_get_fluid.setStyleSheet(u"")
        self.pushButton_get_fluid.setAutoDefault(False)
        self.pushButton_get_fluid.setFlat(False)

        self.gridLayout_18.addWidget(self.pushButton_get_fluid, 1, 3, 1, 1)

        self.label_suction_temperature_unit = QLabel(self.frame_5)
        self.label_suction_temperature_unit.setObjectName(u"label_suction_temperature_unit")
        self.label_suction_temperature_unit.setMinimumSize(QSize(80, 26))
        self.label_suction_temperature_unit.setMaximumSize(QSize(80, 26))
        self.label_suction_temperature_unit.setFont(font4)
        self.label_suction_temperature_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_suction_temperature_unit, 7, 3, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_14, 1, 0, 1, 1)

        self.label_isentropic_exp = QLabel(self.frame_5)
        self.label_isentropic_exp.setObjectName(u"label_isentropic_exp")
        self.label_isentropic_exp.setMinimumSize(QSize(0, 28))
        self.label_isentropic_exp.setMaximumSize(QSize(16777215, 28))
        self.label_isentropic_exp.setFont(font4)
        self.label_isentropic_exp.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_isentropic_exp, 2, 1, 1, 1)

        self.label_bulk_modulus_unit = QLabel(self.frame_5)
        self.label_bulk_modulus_unit.setObjectName(u"label_bulk_modulus_unit")
        self.label_bulk_modulus_unit.setMinimumSize(QSize(80, 28))
        self.label_bulk_modulus_unit.setMaximumSize(QSize(80, 28))
        self.label_bulk_modulus_unit.setFont(font4)
        self.label_bulk_modulus_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_bulk_modulus_unit, 2, 3, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_5)
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
        self.comboBox_pressure_units.setMinimumSize(QSize(110, 28))
        self.comboBox_pressure_units.setMaximumSize(QSize(140, 28))
        self.comboBox_pressure_units.setFont(font4)

        self.gridLayout_18.addWidget(self.comboBox_pressure_units, 3, 2, 1, 1)

        self.label_selected_fluid = QLabel(self.frame_5)
        self.label_selected_fluid.setObjectName(u"label_selected_fluid")
        self.label_selected_fluid.setMinimumSize(QSize(0, 28))
        self.label_selected_fluid.setMaximumSize(QSize(16777215, 28))
        self.label_selected_fluid.setFont(font4)
        self.label_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_selected_fluid, 1, 1, 1, 1)

        self.label_fluctuating_volume_unit = QLabel(self.frame_5)
        self.label_fluctuating_volume_unit.setObjectName(u"label_fluctuating_volume_unit")
        self.label_fluctuating_volume_unit.setMinimumSize(QSize(0, 28))
        self.label_fluctuating_volume_unit.setMaximumSize(QSize(16777215, 28))
        self.label_fluctuating_volume_unit.setFont(font4)
        self.label_fluctuating_volume_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_fluctuating_volume_unit, 9, 3, 1, 1)

        self.label_17 = QLabel(self.frame_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(152, 28))
        self.label_17.setMaximumSize(QSize(16777215, 28))
        self.label_17.setFont(font4)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_18.addWidget(self.label_17, 9, 1, 1, 1)


        self.gridLayout_11.addWidget(self.frame_5, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_32.addWidget(self.scrollArea, 0, 0, 1, 1)

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
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 480, 512))
        self.gridLayout_19 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
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
        self.spinBox_max_frequency.setValue(400)

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

        self.frame_8 = QFrame(self.frame_4)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(400, 40))
        self.frame_8.setMaximumSize(QSize(480, 40))
        self.frame_8.setFrameShape(QFrame.Shape.Box)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_8)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(2, 2, 2, 2)
        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_20.addWidget(self.label_4, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_8, 1, 1, 1, 3)

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


        self.gridLayout_19.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 260))
        self.frame_9.setMaximumSize(QSize(16777215, 260))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_9)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setVerticalSpacing(8)
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_15, 0, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(400, 40))
        self.frame_10.setMaximumSize(QSize(480, 40))
        self.frame_10.setFrameShape(QFrame.Shape.Box)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_10)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(2, 2, 2, 2)
        self.label_2 = QLabel(self.frame_10)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_22.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_10, 0, 1, 1, 2)

        self.tabWidget_plots_2 = QTabWidget(self.frame_9)
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

        self.gridLayout_21.addWidget(self.tabWidget_plots_2, 1, 1, 1, 2)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_16, 0, 3, 1, 1)


        self.gridLayout_19.addWidget(self.frame_9, 1, 0, 1, 1)

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
        self.frame_remove_selection.setMaximumSize(QSize(16777215, 40))
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

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)


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
        QWidget.setTabOrder(self.scrollArea, self.comboBox_cylinder_acting)
        QWidget.setTabOrder(self.comboBox_cylinder_acting, self.spinBox_number_of_cylinders)
        QWidget.setTabOrder(self.spinBox_number_of_cylinders, self.lineEdit_bore_diameter)
        QWidget.setTabOrder(self.lineEdit_bore_diameter, self.lineEdit_stroke)
        QWidget.setTabOrder(self.lineEdit_stroke, self.lineEdit_connecting_rod_length)
        QWidget.setTabOrder(self.lineEdit_connecting_rod_length, self.lineEdit_rod_diameter)
        QWidget.setTabOrder(self.lineEdit_rod_diameter, self.spinBox_tdc_crank_angle_1)
        QWidget.setTabOrder(self.spinBox_tdc_crank_angle_1, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.pushButton_confirm.setDefault(True)
        self.pushButton_exit.setDefault(False)
        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_process_fluctuating_volume.setDefault(True)
        self.pushButton_plot_fluctuating_volume.setDefault(True)
        self.pushButton_pulsation_damper_calculator.setDefault(True)
        self.comboBox_cylinder_acting.setCurrentIndex(1)
        self.comboBox_connection_type.setCurrentIndex(1)
        self.comboBox_temperature_units.setCurrentIndex(1)
        self.pushButton_get_fluid.setDefault(True)
        self.comboBox_pressure_units.setCurrentIndex(4)
        self.comboBox_frequency_resolution.setCurrentIndex(3)
        self.tabWidget_plots_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Reciprocating compressor excitation", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Reciprocating pump model setup", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_process_fluctuating_volume.setText(QCoreApplication.translate("Dialog", u"Process \u0394V", None))
        self.pushButton_plot_fluctuating_volume.setText(QCoreApplication.translate("Dialog", u"Plot \u0394V integral", None))
        self.pushButton_pulsation_damper_calculator.setText(QCoreApplication.translate("Dialog", u"Pulsation damper calculator", None))
        self.comboBox_cylinder_acting.setItemText(0, QCoreApplication.translate("Dialog", u"Both ends", None))
        self.comboBox_cylinder_acting.setItemText(1, QCoreApplication.translate("Dialog", u"Head end", None))
        self.comboBox_cylinder_acting.setItemText(2, QCoreApplication.translate("Dialog", u"Crank end", None))

        self.lineEdit_stroke.setText(QCoreApplication.translate("Dialog", u"0.205", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Connecting rod length:</p></body></html>", None))
        self.label_46.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Number of cylinders:</p></body></html>", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[rpm]</p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Clearance (CE):</p></body></html>", None))
        self.lineEdit_bore_diameter.setText(QCoreApplication.translate("Dialog", u"0.105", None))
        self.lineEdit_rod_diameter.setText(QCoreApplication.translate("Dialog", u"0.05", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Rod diameter:</p></body></html>", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">TDC crank angle (#1):</p></body></html>", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Stroke:</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_48.setText(QCoreApplication.translate("Dialog", u"Active cylinder setup:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Rotational speed:</p></body></html>", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[degree]</p></body></html>", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Clearance (HE):</p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.lineEdit_connecting_rod_length.setText(QCoreApplication.translate("Dialog", u"0.4", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Plunger diameter:</p></body></html>", None))
        self.comboBox_connection_type.setItemText(0, QCoreApplication.translate("Dialog", u"Suction", None))
        self.comboBox_connection_type.setItemText(1, QCoreApplication.translate("Dialog", u"Discharge", None))

        self.label_6.setText(QCoreApplication.translate("Dialog", u"Reciprocating pump parameters", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Reset entries</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setText("")
        self.lineEdit_suction_pressure.setText(QCoreApplication.translate("Dialog", u"2.18", None))
        self.lineEdit_bulk_modulus.setText(QCoreApplication.translate("Dialog", u"2.541031616e9", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Define the fluid properties", None))
        self.lineEdit_discharge_pressure.setText(QCoreApplication.translate("Dialog", u"322.18", None))
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"\u00b0C", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"\u00b0F", None))

        self.label_discharge_pressure_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[bar (g)]</p></body></html>", None))
        self.lineEdit_suction_temperature.setText(QCoreApplication.translate("Dialog", u"45", None))
        self.label_59.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Suction temperature:</p></body></html>", None))
        self.label_61.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Temperature unit:</p></body></html>", None))
        self.lineEdit_selected_fluid.setText("")
        self.lineEdit_discharge_temperature.setText(QCoreApplication.translate("Dialog", u"45", None))
        self.lineEdit_fluctuating_volume.setText("")
        self.label_57.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Discharge pressure:</p></body></html>", None))
        self.label_60.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Discharge temperature:</p></body></html>", None))
        self.label_suction_pressure_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[bar (g)]</p></body></html>", None))
        self.label_58.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Suction pressure:</p></body></html>", None))
        self.label_62.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Pressure unit:</p></body></html>", None))
        self.label_discharge_temperature_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[\u00b0C]</p></body></html>", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_suction_temperature_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[\u00b0C]</p></body></html>", None))
        self.label_isentropic_exp.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Bulk modulus:</p></body></html>", None))
        self.label_bulk_modulus_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[Pa]</p></body></html>", None))
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

        self.label_selected_fluid.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Selected working fluid:</p></body></html>", None))
        self.label_fluctuating_volume_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Fluctuating volume \u0394V:</p></body></html>", None))
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
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Selected node ID:", None))
    # retranslateUi



class ReciprocatingPumpInputs_UI(QDialog, Ui_Dialog):
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
                                                                        - frame_3: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - pushButton_process_fluctuating_volume: QPushButton
                                                                                    - pushButton_plot_fluctuating_volume: QPushButton
                                                                                    - frame_6: QFrame
                                                                                        - (Layout): QGridLayout
                                                                                                - pushButton_pulsation_damper_calculator: QPushButton
                                                                        - frame_all_parameters: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - comboBox_cylinder_acting: QComboBox
                                                                                    - lineEdit_stroke: QLineEdit
                                                                                    - spinBox_number_of_cylinders: QSpinBox
                                                                                    - label_22: QLabel
                                                                                    - label_46: QLabel
                                                                                    - label_34: QLabel
                                                                                    - label_13: QLabel
                                                                                    - label_36: QLabel
                                                                                    - label_16: QLabel
                                                                                    - label_35: QLabel
                                                                                    - lineEdit_bore_diameter: QLineEdit
                                                                                    - lineEdit_rod_diameter: QLineEdit
                                                                                    - label_23: QLabel
                                                                                    - label_28: QLabel
                                                                                    - label_31: QLabel
                                                                                    - label_21: QLabel
                                                                                    - label_14: QLabel
                                                                                    - label_48: QLabel
                                                                                    - spinBox_tdc_crank_angle_1: QSpinBox
                                                                                    - label_9: QLabel
                                                                                    - label_30: QLabel
                                                                                    - label_32: QLabel
                                                                                    - label_27: QLabel
                                                                                    - label_15: QLabel
                                                                                    - lineEdit_connecting_rod_length: QLineEdit
                                                                                    - label_20: QLabel
                                                                                    - comboBox_connection_type: QComboBox
                                                                                    - label_6: QLabel
                                                                                    - pushButton_reset_entries: QPushButton
                                                                                    - doubleSpinBox_clearance_head_end: QDoubleSpinBox
                                                                                    - doubleSpinBox_clearance_crank_end: QDoubleSpinBox
                                                                                    - doubleSpinBox_rotational_speed: QDoubleSpinBox
                                                                        - frame_5: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - lineEdit_suction_pressure: QLineEdit
                                                                                    - lineEdit_bulk_modulus: QLineEdit
                                                                                    - label_10: QLabel
                                                                                    - lineEdit_discharge_pressure: QLineEdit
                                                                                    - comboBox_temperature_units: QComboBox
                                                                                    - label_discharge_pressure_unit: QLabel
                                                                                    - lineEdit_suction_temperature: QLineEdit
                                                                                    - label_59: QLabel
                                                                                    - label_61: QLabel
                                                                                    - lineEdit_selected_fluid: QLineEdit
                                                                                    - lineEdit_discharge_temperature: QLineEdit
                                                                                    - lineEdit_fluctuating_volume: QLineEdit
                                                                                    - label_57: QLabel
                                                                                    - label_60: QLabel
                                                                                    - label_suction_pressure_unit: QLabel
                                                                                    - label_58: QLabel
                                                                                    - label_62: QLabel
                                                                                    - label_discharge_temperature_unit: QLabel
                                                                                    - pushButton_get_fluid: QPushButton
                                                                                    - label_suction_temperature_unit: QLabel
                                                                                    - label_isentropic_exp: QLabel
                                                                                    - label_bulk_modulus_unit: QLabel
                                                                                    - comboBox_pressure_units: QComboBox
                                                                                    - label_selected_fluid: QLabel
                                                                                    - label_fluctuating_volume_unit: QLabel
                                                                                    - label_17: QLabel
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
                                                                                    - frame_8: QFrame
                                                                                        - (Layout): QGridLayout
                                                                                                - label_4: QLabel
                                                                                    - pushButton_process_aquisition_parameters: QPushButton
                                                                                    - spinBox_number_of_points: QSpinBox
                                                                                    - label_37: QLabel
                                                                        - frame_9: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - frame_10: QFrame
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
