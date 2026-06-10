# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsation_damper_calculator_inputs.ui'
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
    QFrame, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(492, 532)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_get_fluid = QPushButton(self.frame_2)
        self.pushButton_get_fluid.setObjectName(u"pushButton_get_fluid")
        self.pushButton_get_fluid.setMinimumSize(QSize(100, 28))
        self.pushButton_get_fluid.setMaximumSize(QSize(100, 28))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_get_fluid.setFont(font)
        self.pushButton_get_fluid.setStyleSheet(u"")
        self.pushButton_get_fluid.setAutoDefault(False)
        self.pushButton_get_fluid.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_get_fluid, 0, 3, 1, 1)

        self.lineEdit_temperature = QLineEdit(self.frame_2)
        self.lineEdit_temperature.setObjectName(u"lineEdit_temperature")
        self.lineEdit_temperature.setMinimumSize(QSize(110, 28))
        self.lineEdit_temperature.setMaximumSize(QSize(140, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_temperature.setFont(font1)
        self.lineEdit_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_temperature, 2, 2, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(152, 28))
        self.label_11.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 9, 1, 1, 1)

        self.label_12 = QLabel(self.frame_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(152, 28))
        self.label_12.setMaximumSize(QSize(16777215, 28))
        self.label_12.setFont(font2)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_12, 5, 1, 1, 1)

        self.label_36 = QLabel(self.frame_2)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(72, 28))
        self.label_36.setMaximumSize(QSize(72, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_36.setFont(font3)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_36, 9, 3, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_2)
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
        self.comboBox_pressure_units.setMinimumSize(QSize(100, 28))
        self.comboBox_pressure_units.setMaximumSize(QSize(100, 28))
        self.comboBox_pressure_units.setFont(font3)

        self.gridLayout_2.addWidget(self.comboBox_pressure_units, 1, 3, 1, 1)

        self.lineEdit_fluctuating_volume = QLineEdit(self.frame_2)
        self.lineEdit_fluctuating_volume.setObjectName(u"lineEdit_fluctuating_volume")
        self.lineEdit_fluctuating_volume.setMinimumSize(QSize(140, 28))
        self.lineEdit_fluctuating_volume.setMaximumSize(QSize(140, 28))
        self.lineEdit_fluctuating_volume.setFont(font1)
        self.lineEdit_fluctuating_volume.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_fluctuating_volume.setStyleSheet(u"")
        self.lineEdit_fluctuating_volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_fluctuating_volume, 8, 2, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_2)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(100, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(100, 28))
        self.comboBox_temperature_units.setFont(font3)

        self.gridLayout_2.addWidget(self.comboBox_temperature_units, 2, 3, 1, 1)

        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(72, 28))
        self.label_13.setMaximumSize(QSize(72, 28))
        self.label_13.setFont(font3)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 8, 3, 1, 1)

        self.doubleSpinBox_pressure_ratio = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_pressure_ratio.setObjectName(u"doubleSpinBox_pressure_ratio")
        self.doubleSpinBox_pressure_ratio.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_pressure_ratio.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_pressure_ratio.setFont(font1)
        self.doubleSpinBox_pressure_ratio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_pressure_ratio.setDecimals(3)
        self.doubleSpinBox_pressure_ratio.setMinimum(0.001000000000000)
        self.doubleSpinBox_pressure_ratio.setMaximum(0.999000000000000)
        self.doubleSpinBox_pressure_ratio.setSingleStep(0.050000000000000)
        self.doubleSpinBox_pressure_ratio.setValue(0.800000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_pressure_ratio, 5, 2, 1, 1)

        self.label_polytropic_exponent = QLabel(self.frame_2)
        self.label_polytropic_exponent.setObjectName(u"label_polytropic_exponent")
        self.label_polytropic_exponent.setMinimumSize(QSize(152, 28))
        self.label_polytropic_exponent.setMaximumSize(QSize(16777215, 28))
        self.label_polytropic_exponent.setFont(font2)
        self.label_polytropic_exponent.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_polytropic_exponent, 4, 1, 1, 1)

        self.lineEdit_selected_fluid = QLineEdit(self.frame_2)
        self.lineEdit_selected_fluid.setObjectName(u"lineEdit_selected_fluid")
        self.lineEdit_selected_fluid.setEnabled(False)
        self.lineEdit_selected_fluid.setMinimumSize(QSize(110, 28))
        self.lineEdit_selected_fluid.setMaximumSize(QSize(140, 28))
        self.lineEdit_selected_fluid.setFont(font1)
        self.lineEdit_selected_fluid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_selected_fluid, 0, 2, 1, 1)

        self.label_molar_mass = QLabel(self.frame_2)
        self.label_molar_mass.setObjectName(u"label_molar_mass")
        self.label_molar_mass.setMinimumSize(QSize(0, 28))
        self.label_molar_mass.setMaximumSize(QSize(16777215, 28))
        self.label_molar_mass.setFont(font3)
        self.label_molar_mass.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_molar_mass, 0, 1, 1, 1)

        self.comboBox_compression_type = QComboBox(self.frame_2)
        self.comboBox_compression_type.addItem("")
        self.comboBox_compression_type.addItem("")
        self.comboBox_compression_type.setObjectName(u"comboBox_compression_type")
        self.comboBox_compression_type.setMinimumSize(QSize(140, 28))
        self.comboBox_compression_type.setMaximumSize(QSize(140, 28))
        self.comboBox_compression_type.setFont(font1)

        self.gridLayout_2.addWidget(self.comboBox_compression_type, 3, 2, 1, 1)

        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(152, 28))
        self.label_10.setMaximumSize(QSize(16777215, 28))
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 8, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 8, 4, 1, 1)

        self.doubleSpinBox_isentropic_exponent = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_isentropic_exponent.setObjectName(u"doubleSpinBox_isentropic_exponent")
        self.doubleSpinBox_isentropic_exponent.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_isentropic_exponent.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_isentropic_exponent.setFont(font1)
        self.doubleSpinBox_isentropic_exponent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_isentropic_exponent.setDecimals(3)
        self.doubleSpinBox_isentropic_exponent.setMinimum(0.001000000000000)
        self.doubleSpinBox_isentropic_exponent.setMaximum(10.000000000000000)
        self.doubleSpinBox_isentropic_exponent.setSingleStep(0.050000000000000)
        self.doubleSpinBox_isentropic_exponent.setValue(1.400000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_isentropic_exponent, 4, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 8, 0, 1, 1)

        self.label_42 = QLabel(self.frame_2)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(0, 28))
        self.label_42.setMaximumSize(QSize(16777215, 28))
        self.label_42.setFont(font3)
        self.label_42.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_42, 1, 1, 1, 1)

        self.doubleSpinBox_residual_pulsation = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_residual_pulsation.setObjectName(u"doubleSpinBox_residual_pulsation")
        self.doubleSpinBox_residual_pulsation.setMinimumSize(QSize(140, 28))
        self.doubleSpinBox_residual_pulsation.setMaximumSize(QSize(140, 28))
        self.doubleSpinBox_residual_pulsation.setFont(font1)
        self.doubleSpinBox_residual_pulsation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_residual_pulsation.setDecimals(3)
        self.doubleSpinBox_residual_pulsation.setMinimum(0.010000000000000)
        self.doubleSpinBox_residual_pulsation.setSingleStep(0.250000000000000)
        self.doubleSpinBox_residual_pulsation.setValue(1.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_residual_pulsation, 9, 2, 1, 1)

        self.label_44 = QLabel(self.frame_2)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(0, 28))
        self.label_44.setMaximumSize(QSize(16777215, 28))
        self.label_44.setFont(font3)
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_44, 2, 1, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(152, 28))
        self.label_9.setMaximumSize(QSize(16777215, 28))
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 3, 1, 1, 1)

        self.lineEdit_pressure = QLineEdit(self.frame_2)
        self.lineEdit_pressure.setObjectName(u"lineEdit_pressure")
        self.lineEdit_pressure.setMinimumSize(QSize(110, 28))
        self.lineEdit_pressure.setMaximumSize(QSize(140, 28))
        self.lineEdit_pressure.setFont(font1)
        self.lineEdit_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_pressure, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_16 = QLabel(self.frame_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(152, 28))
        self.label_16.setMaximumSize(QSize(16777215, 28))
        self.label_16.setFont(font2)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_16, 0, 1, 1, 1)

        self.comboBox_volume_units = QComboBox(self.frame_3)
        self.comboBox_volume_units.addItem("")
        self.comboBox_volume_units.addItem("")
        self.comboBox_volume_units.addItem("")
        self.comboBox_volume_units.setObjectName(u"comboBox_volume_units")
        self.comboBox_volume_units.setMinimumSize(QSize(72, 28))
        self.comboBox_volume_units.setMaximumSize(QSize(140, 28))
        self.comboBox_volume_units.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBox_volume_units, 0, 2, 1, 1)

        self.label_15 = QLabel(self.frame_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(152, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_15, 1, 1, 1, 1)

        self.lineEdit_effective_volume = QLineEdit(self.frame_3)
        self.lineEdit_effective_volume.setObjectName(u"lineEdit_effective_volume")
        self.lineEdit_effective_volume.setMinimumSize(QSize(140, 28))
        self.lineEdit_effective_volume.setMaximumSize(QSize(140, 28))
        self.lineEdit_effective_volume.setFont(font1)
        self.lineEdit_effective_volume.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_effective_volume.setStyleSheet(u"")
        self.lineEdit_effective_volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_effective_volume, 1, 2, 1, 1)

        self.label_17 = QLabel(self.frame_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(152, 28))
        self.label_17.setMaximumSize(QSize(16777215, 28))
        self.label_17.setFont(font2)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_17, 2, 1, 1, 1)

        self.lineEdit_volume_at_average_pressure = QLineEdit(self.frame_3)
        self.lineEdit_volume_at_average_pressure.setObjectName(u"lineEdit_volume_at_average_pressure")
        self.lineEdit_volume_at_average_pressure.setMinimumSize(QSize(140, 28))
        self.lineEdit_volume_at_average_pressure.setMaximumSize(QSize(140, 28))
        self.lineEdit_volume_at_average_pressure.setFont(font1)
        self.lineEdit_volume_at_average_pressure.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_volume_at_average_pressure.setStyleSheet(u"")
        self.lineEdit_volume_at_average_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_volume_at_average_pressure, 2, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 4, 1, 1)

        self.label_effective_volume_unit = QLabel(self.frame_3)
        self.label_effective_volume_unit.setObjectName(u"label_effective_volume_unit")
        self.label_effective_volume_unit.setMinimumSize(QSize(72, 28))
        self.label_effective_volume_unit.setMaximumSize(QSize(72, 28))
        self.label_effective_volume_unit.setFont(font3)
        self.label_effective_volume_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_effective_volume_unit, 1, 3, 1, 1)

        self.label_volume_avg_pressure_unit = QLabel(self.frame_3)
        self.label_volume_avg_pressure_unit.setObjectName(u"label_volume_avg_pressure_unit")
        self.label_volume_avg_pressure_unit.setMinimumSize(QSize(72, 28))
        self.label_volume_avg_pressure_unit.setMaximumSize(QSize(72, 28))
        self.label_volume_avg_pressure_unit.setFont(font3)
        self.label_volume_avg_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_volume_avg_pressure_unit, 2, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_18 = QFrame(Dialog)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 48))
        self.frame_18.setMaximumSize(QSize(16777215, 48))
        font4 = QFont()
        font4.setPointSize(8)
        self.frame_18.setFont(font4)
        self.frame_18.setFrameShape(QFrame.Shape.Box)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_18)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_18)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 32))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label.setFont(font5)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_18, 0, 0, 1, 1)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 52))
        self.frame_4.setMaximumSize(QSize(16777215, 52))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_confirm = QPushButton(self.frame_4)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 30))
        self.pushButton_confirm.setMaximumSize(QSize(100, 30))
        self.pushButton_confirm.setFont(font)
        self.pushButton_confirm.setStyleSheet(u"")
        self.pushButton_confirm.setAutoDefault(False)
        self.pushButton_confirm.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_confirm, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_4)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_get_fluid.setDefault(True)
        self.comboBox_pressure_units.setCurrentIndex(4)
        self.comboBox_temperature_units.setCurrentIndex(1)
        self.pushButton_confirm.setDefault(True)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_get_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.lineEdit_temperature.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Residual pulsation:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Pressure ratio factor \u03a6:</p></body></html>", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[%]</p></body></html>", None))
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

        self.lineEdit_fluctuating_volume.setText("")
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"\u00b0C", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"\u00b0F", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label_polytropic_exponent.setText(QCoreApplication.translate("Dialog", u"Isentropic exponent:", None))
        self.lineEdit_selected_fluid.setText("")
        self.label_molar_mass.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Selected fluid:</p></body></html>", None))
        self.comboBox_compression_type.setItemText(0, QCoreApplication.translate("Dialog", u"Isentropic", None))
        self.comboBox_compression_type.setItemText(1, QCoreApplication.translate("Dialog", u"Isothermal", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Fluctuating volume \u0394V:</p></body></html>", None))
        self.label_42.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Pressure:</p></body></html>", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Temperature:</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Compression type:", None))
        self.lineEdit_pressure.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Volume unit:", None))
        self.comboBox_volume_units.setItemText(0, QCoreApplication.translate("Dialog", u"m\u00b3", None))
        self.comboBox_volume_units.setItemText(1, QCoreApplication.translate("Dialog", u"cm\u00b3", None))
        self.comboBox_volume_units.setItemText(2, QCoreApplication.translate("Dialog", u"L", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Effective volume:", None))
        self.lineEdit_effective_volume.setText("")
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Volume (avg. pressure):", None))
        self.lineEdit_volume_at_average_pressure.setText("")
        self.label_effective_volume_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label_volume_avg_pressure_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Pulsation damper calculator", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class PulsationDamperCalculatorInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_get_fluid: QPushButton
                                        - lineEdit_temperature: QLineEdit
                                        - label_11: QLabel
                                        - label_12: QLabel
                                        - label_36: QLabel
                                        - comboBox_pressure_units: QComboBox
                                        - lineEdit_fluctuating_volume: QLineEdit
                                        - comboBox_temperature_units: QComboBox
                                        - label_13: QLabel
                                        - doubleSpinBox_pressure_ratio: QDoubleSpinBox
                                        - label_polytropic_exponent: QLabel
                                        - lineEdit_selected_fluid: QLineEdit
                                        - label_molar_mass: QLabel
                                        - comboBox_compression_type: QComboBox
                                        - label_10: QLabel
                                        - doubleSpinBox_isentropic_exponent: QDoubleSpinBox
                                        - label_42: QLabel
                                        - doubleSpinBox_residual_pulsation: QDoubleSpinBox
                                        - label_44: QLabel
                                        - label_9: QLabel
                                        - lineEdit_pressure: QLineEdit
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label_16: QLabel
                                        - comboBox_volume_units: QComboBox
                                        - label_15: QLabel
                                        - lineEdit_effective_volume: QLineEdit
                                        - label_17: QLabel
                                        - lineEdit_volume_at_average_pressure: QLineEdit
                                        - label_effective_volume_unit: QLabel
                                        - label_volume_avg_pressure_unit: QLabel
                - frame_18: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
