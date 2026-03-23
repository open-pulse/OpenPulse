# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsation_damper_editor_inputs.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1056, 769)
        self.gridLayout_6 = QGridLayout(Dialog)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(500, 0))
        self.frame.setMaximumSize(QSize(16777215, 1400))
        font = QFont()
        font.setPointSize(1)
        self.frame.setFont(font)
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
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.tabWidget_main.setFont(font1)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 496, 658))
        self.gridLayout_11 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_all_parameters = QFrame(self.scrollAreaWidgetContents)
        self.frame_all_parameters.setObjectName(u"frame_all_parameters")
        self.frame_all_parameters.setMaximumSize(QSize(16777215, 16777215))
        self.frame_all_parameters.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_all_parameters.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_all_parameters)
        self.gridLayout_14.setSpacing(6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)

        self.pushButton_reset_entries = QPushButton(self.frame_all_parameters)
        self.pushButton_reset_entries.setObjectName(u"pushButton_reset_entries")
        self.pushButton_reset_entries.setMinimumSize(QSize(40, 28))
        self.pushButton_reset_entries.setMaximumSize(QSize(40, 28))
        icon = QIcon()
        icon.addFile(u":/icons/common/broom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_reset_entries.setIcon(icon)
        self.pushButton_reset_entries.setIconSize(QSize(20, 20))
        self.pushButton_reset_entries.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_reset_entries, 0, 3, 1, 1)

        self.label_21 = QLabel(self.frame_all_parameters)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(152, 28))
        self.label_21.setMaximumSize(QSize(152, 28))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_21, 6, 1, 1, 1)

        self.lineEdit_wall_thickness_gas = QLineEdit(self.frame_all_parameters)
        self.lineEdit_wall_thickness_gas.setObjectName(u"lineEdit_wall_thickness_gas")
        self.lineEdit_wall_thickness_gas.setMinimumSize(QSize(140, 26))
        self.lineEdit_wall_thickness_gas.setMaximumSize(QSize(140, 26))
        self.lineEdit_wall_thickness_gas.setFont(font1)
        self.lineEdit_wall_thickness_gas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_gas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_wall_thickness_gas, 12, 2, 1, 1)

        self.label_28 = QLabel(self.frame_all_parameters)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(100, 26))
        self.label_28.setMaximumSize(QSize(100, 26))
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_28, 12, 3, 1, 1)

        self.lineEdit_neck_height = QLineEdit(self.frame_all_parameters)
        self.lineEdit_neck_height.setObjectName(u"lineEdit_neck_height")
        self.lineEdit_neck_height.setMinimumSize(QSize(140, 28))
        self.lineEdit_neck_height.setMaximumSize(QSize(140, 28))
        self.lineEdit_neck_height.setFont(font1)
        self.lineEdit_neck_height.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_neck_height.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_neck_height, 14, 2, 1, 1)

        self.label_15 = QLabel(self.frame_all_parameters)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(100, 28))
        self.label_15.setMaximumSize(QSize(100, 28))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_15, 8, 3, 1, 1)

        self.lineEdit_damper_volume = QLineEdit(self.frame_all_parameters)
        self.lineEdit_damper_volume.setObjectName(u"lineEdit_damper_volume")
        self.lineEdit_damper_volume.setMinimumSize(QSize(140, 28))
        self.lineEdit_damper_volume.setMaximumSize(QSize(140, 28))
        self.lineEdit_damper_volume.setFont(font1)
        self.lineEdit_damper_volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_damper_volume, 5, 2, 1, 1)

        self.lineEdit_outside_diameter_neck = QLineEdit(self.frame_all_parameters)
        self.lineEdit_outside_diameter_neck.setObjectName(u"lineEdit_outside_diameter_neck")
        self.lineEdit_outside_diameter_neck.setMinimumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_neck.setMaximumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_neck.setFont(font1)
        self.lineEdit_outside_diameter_neck.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_outside_diameter_neck.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_outside_diameter_neck, 13, 2, 1, 1)

        self.lineEdit_outside_diameter_liquid = QLineEdit(self.frame_all_parameters)
        self.lineEdit_outside_diameter_liquid.setObjectName(u"lineEdit_outside_diameter_liquid")
        self.lineEdit_outside_diameter_liquid.setMinimumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_liquid.setMaximumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_liquid.setFont(font1)
        self.lineEdit_outside_diameter_liquid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_outside_diameter_liquid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_outside_diameter_liquid, 8, 2, 1, 1)

        self.label_22 = QLabel(self.frame_all_parameters)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(152, 28))
        self.label_22.setMaximumSize(QSize(152, 28))
        self.label_22.setFont(font1)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_22, 8, 1, 1, 1)

        self.label_damper_volume_unit = QLabel(self.frame_all_parameters)
        self.label_damper_volume_unit.setObjectName(u"label_damper_volume_unit")
        self.label_damper_volume_unit.setMinimumSize(QSize(100, 28))
        self.label_damper_volume_unit.setMaximumSize(QSize(100, 28))
        self.label_damper_volume_unit.setFont(font1)
        self.label_damper_volume_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_damper_volume_unit, 5, 3, 1, 1)

        self.label_19 = QLabel(self.frame_all_parameters)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(152, 28))
        self.label_19.setMaximumSize(QSize(152, 28))
        self.label_19.setFont(font1)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_19, 4, 1, 1, 1)

        self.label_35 = QLabel(self.frame_all_parameters)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMinimumSize(QSize(152, 28))
        self.label_35.setMaximumSize(QSize(152, 28))
        self.label_35.setFont(font1)
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_35, 14, 1, 1, 1)

        self.label_20 = QLabel(self.frame_all_parameters)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(152, 28))
        self.label_20.setMaximumSize(QSize(152, 28))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_20, 5, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)

        self.label_gas_volume_unit = QLabel(self.frame_all_parameters)
        self.label_gas_volume_unit.setObjectName(u"label_gas_volume_unit")
        self.label_gas_volume_unit.setMinimumSize(QSize(100, 28))
        self.label_gas_volume_unit.setMaximumSize(QSize(100, 28))
        self.label_gas_volume_unit.setFont(font1)
        self.label_gas_volume_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_gas_volume_unit, 6, 3, 1, 1)

        self.label_5 = QLabel(self.frame_all_parameters)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(152, 26))
        self.label_5.setMaximumSize(QSize(152, 26))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_5, 3, 1, 1, 1)

        self.label_9 = QLabel(self.frame_all_parameters)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(152, 28))
        self.label_9.setMaximumSize(QSize(152, 28))
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_9, 0, 1, 1, 1)

        self.label_26 = QLabel(self.frame_all_parameters)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(152, 26))
        self.label_26.setMaximumSize(QSize(152, 26))
        self.label_26.setFont(font1)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_26, 12, 1, 1, 1)

        self.label_25 = QLabel(self.frame_all_parameters)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(100, 28))
        self.label_25.setMaximumSize(QSize(100, 28))
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_25, 10, 3, 1, 1)

        self.comboBox_volume_unit = QComboBox(self.frame_all_parameters)
        self.comboBox_volume_unit.addItem("")
        self.comboBox_volume_unit.addItem("")
        self.comboBox_volume_unit.addItem("")
        self.comboBox_volume_unit.setObjectName(u"comboBox_volume_unit")
        self.comboBox_volume_unit.setMinimumSize(QSize(140, 28))
        self.comboBox_volume_unit.setMaximumSize(QSize(140, 28))
        self.comboBox_volume_unit.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_volume_unit, 4, 2, 1, 1)

        self.comboBox_damper_type = QComboBox(self.frame_all_parameters)
        self.comboBox_damper_type.addItem("")
        self.comboBox_damper_type.addItem("")
        self.comboBox_damper_type.setObjectName(u"comboBox_damper_type")
        self.comboBox_damper_type.setMinimumSize(QSize(140, 28))
        self.comboBox_damper_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_damper_type.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_damper_type, 0, 2, 1, 1)

        self.label_18 = QLabel(self.frame_all_parameters)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(100, 26))
        self.label_18.setMaximumSize(QSize(100, 26))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_18, 14, 3, 1, 1)

        self.lineEdit_gas_volume = QLineEdit(self.frame_all_parameters)
        self.lineEdit_gas_volume.setObjectName(u"lineEdit_gas_volume")
        self.lineEdit_gas_volume.setMinimumSize(QSize(140, 28))
        self.lineEdit_gas_volume.setMaximumSize(QSize(140, 28))
        self.lineEdit_gas_volume.setFont(font1)
        self.lineEdit_gas_volume.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_gas_volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_gas_volume, 6, 2, 1, 1)

        self.label_29 = QLabel(self.frame_all_parameters)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(152, 28))
        self.label_29.setMaximumSize(QSize(152, 28))
        self.label_29.setFont(font1)
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_29, 7, 1, 1, 1)

        self.comboBox_volume_sections = QComboBox(self.frame_all_parameters)
        self.comboBox_volume_sections.addItem("")
        self.comboBox_volume_sections.addItem("")
        self.comboBox_volume_sections.setObjectName(u"comboBox_volume_sections")
        self.comboBox_volume_sections.setMinimumSize(QSize(140, 28))
        self.comboBox_volume_sections.setMaximumSize(QSize(140, 28))
        self.comboBox_volume_sections.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_volume_sections, 7, 2, 1, 1)

        self.label_24 = QLabel(self.frame_all_parameters)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(152, 28))
        self.label_24.setMaximumSize(QSize(152, 28))
        self.label_24.setFont(font1)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_24, 10, 1, 1, 1)

        self.label_27 = QLabel(self.frame_all_parameters)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(152, 28))
        self.label_27.setMaximumSize(QSize(152, 28))
        self.label_27.setFont(font1)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_27, 13, 1, 1, 1)

        self.lineEdit_outside_diameter_gas = QLineEdit(self.frame_all_parameters)
        self.lineEdit_outside_diameter_gas.setObjectName(u"lineEdit_outside_diameter_gas")
        self.lineEdit_outside_diameter_gas.setMinimumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_gas.setMaximumSize(QSize(140, 28))
        self.lineEdit_outside_diameter_gas.setFont(font1)
        self.lineEdit_outside_diameter_gas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_outside_diameter_gas.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_outside_diameter_gas, 10, 2, 1, 1)

        self.label_17 = QLabel(self.frame_all_parameters)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(100, 26))
        self.label_17.setMaximumSize(QSize(100, 26))
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_17, 13, 3, 1, 1)

        self.comboBox_main_axis = QComboBox(self.frame_all_parameters)
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.setObjectName(u"comboBox_main_axis")
        self.comboBox_main_axis.setMinimumSize(QSize(140, 26))
        self.comboBox_main_axis.setMaximumSize(QSize(140, 26))
        self.comboBox_main_axis.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_main_axis, 3, 2, 1, 1)

        self.label_23 = QLabel(self.frame_all_parameters)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(152, 26))
        self.label_23.setMaximumSize(QSize(152, 26))
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_23, 9, 1, 1, 1)

        self.lineEdit_wall_thickness_liquid = QLineEdit(self.frame_all_parameters)
        self.lineEdit_wall_thickness_liquid.setObjectName(u"lineEdit_wall_thickness_liquid")
        self.lineEdit_wall_thickness_liquid.setMinimumSize(QSize(140, 26))
        self.lineEdit_wall_thickness_liquid.setMaximumSize(QSize(140, 26))
        self.lineEdit_wall_thickness_liquid.setFont(font1)
        self.lineEdit_wall_thickness_liquid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_liquid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_wall_thickness_liquid, 9, 2, 1, 1)

        self.label_16 = QLabel(self.frame_all_parameters)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(100, 26))
        self.label_16.setMaximumSize(QSize(100, 26))
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_16, 9, 3, 1, 1)


        self.gridLayout_11.addWidget(self.frame_all_parameters, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_polytropic_exponent = QLineEdit(self.frame_3)
        self.lineEdit_polytropic_exponent.setObjectName(u"lineEdit_polytropic_exponent")
        self.lineEdit_polytropic_exponent.setMinimumSize(QSize(140, 28))
        self.lineEdit_polytropic_exponent.setMaximumSize(QSize(140, 28))
        self.lineEdit_polytropic_exponent.setFont(font1)
        self.lineEdit_polytropic_exponent.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_polytropic_exponent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_polytropic_exponent, 4, 2, 1, 1)

        self.label_molar_mass_2 = QLabel(self.frame_3)
        self.label_molar_mass_2.setObjectName(u"label_molar_mass_2")
        self.label_molar_mass_2.setMinimumSize(QSize(152, 28))
        self.label_molar_mass_2.setMaximumSize(QSize(152, 28))
        self.label_molar_mass_2.setFont(font1)
        self.label_molar_mass_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_molar_mass_2, 1, 1, 1, 1)

        self.lineEdit_selected_liquid_fluid = QLineEdit(self.frame_3)
        self.lineEdit_selected_liquid_fluid.setObjectName(u"lineEdit_selected_liquid_fluid")
        self.lineEdit_selected_liquid_fluid.setEnabled(False)
        self.lineEdit_selected_liquid_fluid.setMinimumSize(QSize(140, 28))
        self.lineEdit_selected_liquid_fluid.setMaximumSize(QSize(140, 28))
        self.lineEdit_selected_liquid_fluid.setFont(font1)
        self.lineEdit_selected_liquid_fluid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_liquid_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selected_liquid_fluid, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 32))
        self.label_13.setMaximumSize(QSize(16777215, 32))
        self.label_13.setFont(font1)
        self.label_13.setFrameShape(QFrame.Shape.Box)
        self.label_13.setTextFormat(Qt.TextFormat.AutoText)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_13, 0, 1, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 4, 1, 1)

        self.label_bulk_modulus_unit = QLabel(self.frame_3)
        self.label_bulk_modulus_unit.setObjectName(u"label_bulk_modulus_unit")
        self.label_bulk_modulus_unit.setMinimumSize(QSize(80, 28))
        self.label_bulk_modulus_unit.setMaximumSize(QSize(80, 28))
        self.label_bulk_modulus_unit.setFont(font1)
        self.label_bulk_modulus_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_bulk_modulus_unit, 4, 3, 1, 1)

        self.lineEdit_gas_pressure = QLineEdit(self.frame_3)
        self.lineEdit_gas_pressure.setObjectName(u"lineEdit_gas_pressure")
        self.lineEdit_gas_pressure.setMinimumSize(QSize(140, 28))
        self.lineEdit_gas_pressure.setMaximumSize(QSize(140, 28))
        self.lineEdit_gas_pressure.setFont(font1)
        self.lineEdit_gas_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_gas_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_gas_pressure, 5, 2, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_3)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(100, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(100, 28))
        self.comboBox_temperature_units.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_temperature_units, 6, 3, 1, 1)

        self.label_molar_mass = QLabel(self.frame_3)
        self.label_molar_mass.setObjectName(u"label_molar_mass")
        self.label_molar_mass.setMinimumSize(QSize(152, 28))
        self.label_molar_mass.setMaximumSize(QSize(152, 28))
        self.label_molar_mass.setFont(font1)
        self.label_molar_mass.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_molar_mass, 2, 1, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_3)
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
        self.comboBox_pressure_units.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_pressure_units, 5, 3, 1, 1)

        self.label_45 = QLabel(self.frame_3)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(152, 28))
        self.label_45.setMaximumSize(QSize(152, 28))
        self.label_45.setFont(font1)
        self.label_45.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_45, 6, 1, 1, 1)

        self.lineEdit_gas_temperature = QLineEdit(self.frame_3)
        self.lineEdit_gas_temperature.setObjectName(u"lineEdit_gas_temperature")
        self.lineEdit_gas_temperature.setMinimumSize(QSize(140, 28))
        self.lineEdit_gas_temperature.setMaximumSize(QSize(140, 28))
        self.lineEdit_gas_temperature.setFont(font1)
        self.lineEdit_gas_temperature.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_gas_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_gas_temperature, 6, 2, 1, 1)

        self.pushButton_get_liquid_fluid = QPushButton(self.frame_3)
        self.pushButton_get_liquid_fluid.setObjectName(u"pushButton_get_liquid_fluid")
        self.pushButton_get_liquid_fluid.setMinimumSize(QSize(100, 28))
        self.pushButton_get_liquid_fluid.setMaximumSize(QSize(100, 28))
        self.pushButton_get_liquid_fluid.setFont(font1)
        self.pushButton_get_liquid_fluid.setStyleSheet(u"")
        self.pushButton_get_liquid_fluid.setAutoDefault(False)
        self.pushButton_get_liquid_fluid.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_get_liquid_fluid, 2, 3, 1, 1)

        self.label_43 = QLabel(self.frame_3)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(152, 28))
        self.label_43.setMaximumSize(QSize(152, 28))
        self.label_43.setFont(font1)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_43, 5, 1, 1, 1)

        self.comboBox_fluid_data_source = QComboBox(self.frame_3)
        self.comboBox_fluid_data_source.addItem("")
        self.comboBox_fluid_data_source.addItem("")
        self.comboBox_fluid_data_source.setObjectName(u"comboBox_fluid_data_source")
        self.comboBox_fluid_data_source.setMinimumSize(QSize(140, 28))
        self.comboBox_fluid_data_source.setMaximumSize(QSize(16777215, 28))
        self.comboBox_fluid_data_source.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_fluid_data_source, 1, 2, 1, 1)

        self.label_molar_mass_3 = QLabel(self.frame_3)
        self.label_molar_mass_3.setObjectName(u"label_molar_mass_3")
        self.label_molar_mass_3.setMinimumSize(QSize(152, 28))
        self.label_molar_mass_3.setMaximumSize(QSize(152, 28))
        self.label_molar_mass_3.setFont(font1)
        self.label_molar_mass_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_molar_mass_3, 3, 1, 1, 1)

        self.label_isentropic_exp = QLabel(self.frame_3)
        self.label_isentropic_exp.setObjectName(u"label_isentropic_exp")
        self.label_isentropic_exp.setMinimumSize(QSize(152, 28))
        self.label_isentropic_exp.setMaximumSize(QSize(152, 28))
        self.label_isentropic_exp.setFont(font1)
        self.label_isentropic_exp.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_isentropic_exp, 4, 1, 1, 1)

        self.lineEdit_selected_gas_fluid = QLineEdit(self.frame_3)
        self.lineEdit_selected_gas_fluid.setObjectName(u"lineEdit_selected_gas_fluid")
        self.lineEdit_selected_gas_fluid.setEnabled(False)
        self.lineEdit_selected_gas_fluid.setMinimumSize(QSize(140, 28))
        self.lineEdit_selected_gas_fluid.setMaximumSize(QSize(140, 28))
        self.lineEdit_selected_gas_fluid.setFont(font1)
        self.lineEdit_selected_gas_fluid.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_gas_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_selected_gas_fluid, 3, 2, 1, 1)

        self.pushButton_get_gas_fluid = QPushButton(self.frame_3)
        self.pushButton_get_gas_fluid.setObjectName(u"pushButton_get_gas_fluid")
        self.pushButton_get_gas_fluid.setMinimumSize(QSize(100, 28))
        self.pushButton_get_gas_fluid.setMaximumSize(QSize(100, 28))
        self.pushButton_get_gas_fluid.setFont(font1)
        self.pushButton_get_gas_fluid.setStyleSheet(u"")
        self.pushButton_get_gas_fluid.setAutoDefault(False)
        self.pushButton_get_gas_fluid.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_get_gas_fluid, 3, 3, 1, 1)


        self.gridLayout_11.addWidget(self.frame_3, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_32.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_9 = QGridLayout(self.tab_remove)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 6, 2, 2)
        self.frame_remove_selection = QFrame(self.tab_remove)
        self.frame_remove_selection.setObjectName(u"frame_remove_selection")
        self.frame_remove_selection.setMinimumSize(QSize(0, 72))
        self.frame_remove_selection.setMaximumSize(QSize(16777215, 72))
        self.frame_remove_selection.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_remove_selection.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_remove_selection)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.lineEdit_selected_damper_label = QLineEdit(self.frame_remove_selection)
        self.lineEdit_selected_damper_label.setObjectName(u"lineEdit_selected_damper_label")
        self.lineEdit_selected_damper_label.setEnabled(False)
        self.lineEdit_selected_damper_label.setMinimumSize(QSize(200, 26))
        self.lineEdit_selected_damper_label.setMaximumSize(QSize(200, 26))
        self.lineEdit_selected_damper_label.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_damper_label.setStyleSheet(u"")
        self.lineEdit_selected_damper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_selected_damper_label, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_remove_selection)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_remove_selection)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(16777215, 16777215))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_3, 1, 1, 1, 1)

        self.lineEdit_damper_type = QLineEdit(self.frame_remove_selection)
        self.lineEdit_damper_type.setObjectName(u"lineEdit_damper_type")
        self.lineEdit_damper_type.setEnabled(False)
        self.lineEdit_damper_type.setMinimumSize(QSize(200, 0))
        self.lineEdit_damper_type.setMaximumSize(QSize(200, 26))
        self.lineEdit_damper_type.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_damper_type.setStyleSheet(u"")
        self.lineEdit_damper_type.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_damper_type, 1, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_remove_selection, 0, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.tab_remove)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 0)
        self.treeWidget_pulsation_damper_info = QTreeWidget(self.frame_treeWidget)
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setFont(2, font2);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_pulsation_damper_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_pulsation_damper_info.setObjectName(u"treeWidget_pulsation_damper_info")
        self.treeWidget_pulsation_damper_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_pulsation_damper_info.setMaximumSize(QSize(1000, 1000))
        self.treeWidget_pulsation_damper_info.setFont(font2)
        self.treeWidget_pulsation_damper_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.treeWidget_pulsation_damper_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.treeWidget_pulsation_damper_info.setIndentation(0)

        self.gridLayout_8.addWidget(self.treeWidget_pulsation_damper_info, 1, 0, 1, 1)


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
        self.pushButton_reset = QPushButton(self.frame_remove_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 30))
        self.pushButton_reset.setMaximumSize(QSize(100, 30))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_remove_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 30))
        self.pushButton_remove.setMaximumSize(QSize(100, 30))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_edit = QPushButton(self.frame_remove_buttons)
        self.pushButton_edit.setObjectName(u"pushButton_edit")
        self.pushButton_edit.setMinimumSize(QSize(100, 30))
        self.pushButton_edit.setMaximumSize(QSize(100, 30))
        self.pushButton_edit.setFont(font1)
        self.pushButton_edit.setStyleSheet(u"")
        self.pushButton_edit.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_edit, 0, 2, 1, 1)

        self.pushButton_copy = QPushButton(self.frame_remove_buttons)
        self.pushButton_copy.setObjectName(u"pushButton_copy")
        self.pushButton_copy.setMinimumSize(QSize(100, 30))
        self.pushButton_copy.setMaximumSize(QSize(100, 30))
        self.pushButton_copy.setFont(font1)
        self.pushButton_copy.setStyleSheet(u"")
        self.pushButton_copy.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_copy, 0, 3, 1, 1)


        self.gridLayout_9.addWidget(self.frame_remove_buttons, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_10.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_7, 3, 0, 1, 1)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setPointSize(10)
        self.frame_5.setFont(font3)
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 2)
        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 26))
        self.label_12.setMaximumSize(QSize(100, 26))
        self.label_12.setFont(font3)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_12)

        self.lineEdit_damper_label = QLineEdit(self.frame_5)
        self.lineEdit_damper_label.setObjectName(u"lineEdit_damper_label")
        self.lineEdit_damper_label.setMinimumSize(QSize(300, 26))
        self.lineEdit_damper_label.setMaximumSize(QSize(400, 26))
        self.lineEdit_damper_label.setFont(font3)
        self.lineEdit_damper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_damper_label)


        self.gridLayout_4.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 60))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_8)
        self.gridLayout_15.setSpacing(6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.label_11 = QLabel(self.frame_8)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 20))
        self.label_11.setMaximumSize(QSize(80, 20))
        self.label_11.setFont(font3)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_11, 0, 3, 1, 1)

        self.lineEdit_connecting_coord_y = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_y.setObjectName(u"lineEdit_connecting_coord_y")
        self.lineEdit_connecting_coord_y.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_y.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_y.setFont(font3)
        self.lineEdit_connecting_coord_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_connecting_coord_y, 1, 2, 1, 1)

        self.lineEdit_connecting_coord_z = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_z.setObjectName(u"lineEdit_connecting_coord_z")
        self.lineEdit_connecting_coord_z.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_z.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_z.setFont(font3)
        self.lineEdit_connecting_coord_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_connecting_coord_z, 1, 3, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setMaximumSize(QSize(80, 20))
        self.label_10.setFont(font3)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_10, 0, 2, 1, 1)

        self.label_46 = QLabel(self.frame_8)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(100, 26))
        self.label_46.setMaximumSize(QSize(100, 26))
        self.label_46.setFont(font3)
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_46, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setMaximumSize(QSize(80, 20))
        self.label_8.setFont(font3)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_8, 0, 1, 1, 1)

        self.lineEdit_connecting_coord_x = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_x.setObjectName(u"lineEdit_connecting_coord_x")
        self.lineEdit_connecting_coord_x.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_x.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_x.setFont(font3)
        self.lineEdit_connecting_coord_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_connecting_coord_x, 1, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_8, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(500, 400))
        self.frame_4.setFont(font)
        self.frame_4.setFrameShape(QFrame.Shape.Box)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)
        self.label_4.setMinimumSize(QSize(0, 40))
        self.label_4.setMaximumSize(QSize(16777215, 40))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setStrikeOut(False)
        font4.setKerning(True)
        self.label_4.setFont(font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setWordWrap(False)

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.preview_widget_placeholder = QWidget(self.frame_4)
        self.preview_widget_placeholder.setObjectName(u"preview_widget_placeholder")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_widget_placeholder.sizePolicy().hasHeightForWidth())
        self.preview_widget_placeholder.setSizePolicy(sizePolicy)
        self.preview_widget_placeholder.setMinimumSize(QSize(400, 400))

        self.gridLayout_3.addWidget(self.preview_widget_placeholder, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 1, 1, 1, 1)

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
        self.pushButton_exit = QPushButton(self.frame_2)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.pushButton_exit.setFont(font5)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_create = QPushButton(self.frame_2)
        self.pushButton_create.setObjectName(u"pushButton_create")
        self.pushButton_create.setMinimumSize(QSize(100, 30))
        self.pushButton_create.setMaximumSize(QSize(100, 30))
        self.pushButton_create.setFont(font5)
        self.pushButton_create.setStyleSheet(u"")
        self.pushButton_create.setAutoDefault(False)
        self.pushButton_create.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_create, 0, 2, 1, 1)

        self.pushButton_show_errors = QPushButton(self.frame_2)
        self.pushButton_show_errors.setObjectName(u"pushButton_show_errors")
        self.pushButton_show_errors.setEnabled(False)
        self.pushButton_show_errors.setMinimumSize(QSize(100, 30))
        self.pushButton_show_errors.setMaximumSize(QSize(100, 30))
        self.pushButton_show_errors.setFont(font3)

        self.gridLayout_2.addWidget(self.pushButton_show_errors, 0, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_2, 2, 0, 1, 2)

        self.frame_18 = QFrame(Dialog)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 48))
        self.frame_18.setMaximumSize(QSize(16777215, 48))
        font6 = QFont()
        font6.setPointSize(8)
        self.frame_18.setFont(font6)
        self.frame_18.setFrameShape(QFrame.Shape.Box)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_18)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.frame_18)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 32))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(11)
        font7.setBold(False)
        font7.setItalic(False)
        self.label.setFont(font7)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_18, 0, 0, 1, 2)

        QWidget.setTabOrder(self.lineEdit_damper_label, self.lineEdit_connecting_coord_x)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_x, self.lineEdit_connecting_coord_y)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_y, self.lineEdit_connecting_coord_z)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_z, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.comboBox_damper_type)
        QWidget.setTabOrder(self.comboBox_damper_type, self.pushButton_reset_entries)
        QWidget.setTabOrder(self.pushButton_reset_entries, self.comboBox_main_axis)
        QWidget.setTabOrder(self.comboBox_main_axis, self.comboBox_volume_unit)
        QWidget.setTabOrder(self.comboBox_volume_unit, self.lineEdit_damper_volume)
        QWidget.setTabOrder(self.lineEdit_damper_volume, self.lineEdit_gas_volume)
        QWidget.setTabOrder(self.lineEdit_gas_volume, self.comboBox_volume_sections)
        QWidget.setTabOrder(self.comboBox_volume_sections, self.lineEdit_outside_diameter_liquid)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_liquid, self.lineEdit_wall_thickness_liquid)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_liquid, self.lineEdit_outside_diameter_gas)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_gas, self.lineEdit_wall_thickness_gas)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_gas, self.lineEdit_outside_diameter_neck)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_neck, self.lineEdit_neck_height)
        QWidget.setTabOrder(self.lineEdit_neck_height, self.comboBox_fluid_data_source)
        QWidget.setTabOrder(self.comboBox_fluid_data_source, self.lineEdit_selected_liquid_fluid)
        QWidget.setTabOrder(self.lineEdit_selected_liquid_fluid, self.pushButton_get_liquid_fluid)
        QWidget.setTabOrder(self.pushButton_get_liquid_fluid, self.lineEdit_selected_gas_fluid)
        QWidget.setTabOrder(self.lineEdit_selected_gas_fluid, self.pushButton_get_gas_fluid)
        QWidget.setTabOrder(self.pushButton_get_gas_fluid, self.lineEdit_polytropic_exponent)
        QWidget.setTabOrder(self.lineEdit_polytropic_exponent, self.lineEdit_gas_pressure)
        QWidget.setTabOrder(self.lineEdit_gas_pressure, self.comboBox_pressure_units)
        QWidget.setTabOrder(self.comboBox_pressure_units, self.lineEdit_gas_temperature)
        QWidget.setTabOrder(self.lineEdit_gas_temperature, self.comboBox_temperature_units)
        QWidget.setTabOrder(self.comboBox_temperature_units, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_show_errors)
        QWidget.setTabOrder(self.pushButton_show_errors, self.pushButton_create)
        QWidget.setTabOrder(self.pushButton_create, self.treeWidget_pulsation_damper_info)
        QWidget.setTabOrder(self.treeWidget_pulsation_damper_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_edit)
        QWidget.setTabOrder(self.pushButton_edit, self.pushButton_copy)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_damper_type.setCurrentIndex(0)
        self.comboBox_main_axis.setCurrentIndex(1)
        self.comboBox_pressure_units.setCurrentIndex(5)
        self.pushButton_get_liquid_fluid.setDefault(True)
        self.comboBox_fluid_data_source.setCurrentIndex(1)
        self.pushButton_get_gas_fluid.setDefault(True)
        self.pushButton_exit.setDefault(False)
        self.pushButton_create.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Reset entries</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setText("")
        self.label_21.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Gas volume:</p></body></html>", None))
        self.lineEdit_wall_thickness_gas.setText(QCoreApplication.translate("Dialog", u"0.010", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.lineEdit_neck_height.setText(QCoreApplication.translate("Dialog", u"0.04", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.lineEdit_damper_volume.setText(QCoreApplication.translate("Dialog", u"0.014957", None))
        self.lineEdit_outside_diameter_neck.setText(QCoreApplication.translate("Dialog", u"0.085", None))
        self.lineEdit_outside_diameter_liquid.setText(QCoreApplication.translate("Dialog", u"0.250", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outside diameter (liquid):</p></body></html>", None))
        self.label_damper_volume_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Volume unit:", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Neck height:</p></body></html>", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Damper volume:</p></body></html>", None))
        self.label_gas_volume_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m\u00b3]</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Damper main axis:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Damper type:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Wall thickness (gas):</p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.comboBox_volume_unit.setItemText(0, QCoreApplication.translate("Dialog", u" cubic meters", None))
        self.comboBox_volume_unit.setItemText(1, QCoreApplication.translate("Dialog", u" cubic centimeters", None))
        self.comboBox_volume_unit.setItemText(2, QCoreApplication.translate("Dialog", u" liters", None))

        self.comboBox_damper_type.setItemText(0, QCoreApplication.translate("Dialog", u"Bladder", None))
        self.comboBox_damper_type.setItemText(1, QCoreApplication.translate("Dialog", u"Diaphragm", None))

        self.label_18.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.lineEdit_gas_volume.setText(QCoreApplication.translate("Dialog", u"0.012464", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"Sections (liquid/gas):", None))
        self.comboBox_volume_sections.setItemText(0, QCoreApplication.translate("Dialog", u" equal sections", None))
        self.comboBox_volume_sections.setItemText(1, QCoreApplication.translate("Dialog", u" different sections", None))

        self.label_24.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outside diameter (gas):</p></body></html>", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outside diameter (neck):</p></body></html>", None))
        self.lineEdit_outside_diameter_gas.setText(QCoreApplication.translate("Dialog", u"0.250", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.comboBox_main_axis.setItemText(0, QCoreApplication.translate("Dialog", u" x-axis (+)", None))
        self.comboBox_main_axis.setItemText(1, QCoreApplication.translate("Dialog", u" y-axis (+)", None))
        self.comboBox_main_axis.setItemText(2, QCoreApplication.translate("Dialog", u" z-axis (+)", None))
        self.comboBox_main_axis.setItemText(3, QCoreApplication.translate("Dialog", u" x-axis (-)", None))
        self.comboBox_main_axis.setItemText(4, QCoreApplication.translate("Dialog", u" y-axis (-)", None))
        self.comboBox_main_axis.setItemText(5, QCoreApplication.translate("Dialog", u" z-axis (-)", None))

        self.label_23.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Wall thickness (liquid):</p></body></html>", None))
        self.lineEdit_wall_thickness_liquid.setText(QCoreApplication.translate("Dialog", u"0.010", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.lineEdit_polytropic_exponent.setText(QCoreApplication.translate("Dialog", u"1.40", None))
        self.label_molar_mass_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Fluid data source:</p></body></html>", None))
        self.lineEdit_selected_liquid_fluid.setText("")
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Define the fluid properties", None))
        self.label_bulk_modulus_unit.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>[--]</p></body></html>", None))
        self.lineEdit_gas_pressure.setText(QCoreApplication.translate("Dialog", u"120", None))
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"\u00baC", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u" K", None))

        self.label_molar_mass.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Selected liquid fluid:</p></body></html>", None))
        self.comboBox_pressure_units.setItemText(0, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (a)", None))
        self.comboBox_pressure_units.setItemText(1, QCoreApplication.translate("Dialog", u"bar (a)", None))
        self.comboBox_pressure_units.setItemText(2, QCoreApplication.translate("Dialog", u"kPa (a)", None))
        self.comboBox_pressure_units.setItemText(3, QCoreApplication.translate("Dialog", u"Pa (a)", None))
        self.comboBox_pressure_units.setItemText(4, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (g)", None))
        self.comboBox_pressure_units.setItemText(5, QCoreApplication.translate("Dialog", u"bar (g)", None))
        self.comboBox_pressure_units.setItemText(6, QCoreApplication.translate("Dialog", u"kPa (g)", None))
        self.comboBox_pressure_units.setItemText(7, QCoreApplication.translate("Dialog", u"Pa (g)", None))

        self.label_45.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Gas temperature:</p></body></html>", None))
        self.lineEdit_gas_temperature.setText(QCoreApplication.translate("Dialog", u"45", None))
        self.pushButton_get_liquid_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Gas pressure:</p></body></html>", None))
        self.comboBox_fluid_data_source.setItemText(0, QCoreApplication.translate("Dialog", u"RefProp", None))
        self.comboBox_fluid_data_source.setItemText(1, QCoreApplication.translate("Dialog", u"User-defined", None))

        self.label_molar_mass_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Selected gas fluid:</p></body></html>", None))
        self.label_isentropic_exp.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Polytropic exponent:</p></body></html>", None))
        self.lineEdit_selected_gas_fluid.setText("")
        self.pushButton_get_gas_fluid.setText(QCoreApplication.translate("Dialog", u"Get fluid", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Damper label:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Damper type:", None))
        ___qtreewidgetitem = self.treeWidget_pulsation_damper_info.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Lines", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Gas volume [m\u00b3]", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Damper type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Label", None));
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", "")
        self.pushButton_edit.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.pushButton_edit.setProperty(u"status", "")
        self.pushButton_copy.setText(QCoreApplication.translate("Dialog", u"Copy", None))
        self.pushButton_copy.setProperty(u"status", "")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Devices list", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Damper label:", None))
        self.lineEdit_damper_label.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"coord. z [m]", None))
        self.lineEdit_connecting_coord_y.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.lineEdit_connecting_coord_z.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"coord. y [m]", None))
        self.label_46.setText(QCoreApplication.translate("Dialog", u"Connection:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"coord. x [m]", None))
        self.lineEdit_connecting_coord_x.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Damper preview", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_create.setText(QCoreApplication.translate("Dialog", u"Create", None))
        self.pushButton_show_errors.setText(QCoreApplication.translate("Dialog", u"Show errors", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Pulsation damper editor", None))
    # retranslateUi



class PulsationDamperEditorInputs_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
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
                                                                                    - pushButton_reset_entries: QPushButton
                                                                                    - label_21: QLabel
                                                                                    - lineEdit_wall_thickness_gas: QLineEdit
                                                                                    - label_28: QLabel
                                                                                    - lineEdit_neck_height: QLineEdit
                                                                                    - label_15: QLabel
                                                                                    - lineEdit_damper_volume: QLineEdit
                                                                                    - lineEdit_outside_diameter_neck: QLineEdit
                                                                                    - lineEdit_outside_diameter_liquid: QLineEdit
                                                                                    - label_22: QLabel
                                                                                    - label_damper_volume_unit: QLabel
                                                                                    - label_19: QLabel
                                                                                    - label_35: QLabel
                                                                                    - label_20: QLabel
                                                                                    - label_gas_volume_unit: QLabel
                                                                                    - label_5: QLabel
                                                                                    - label_9: QLabel
                                                                                    - label_26: QLabel
                                                                                    - label_25: QLabel
                                                                                    - comboBox_volume_unit: QComboBox
                                                                                    - comboBox_damper_type: QComboBox
                                                                                    - label_18: QLabel
                                                                                    - lineEdit_gas_volume: QLineEdit
                                                                                    - label_29: QLabel
                                                                                    - comboBox_volume_sections: QComboBox
                                                                                    - label_24: QLabel
                                                                                    - label_27: QLabel
                                                                                    - lineEdit_outside_diameter_gas: QLineEdit
                                                                                    - label_17: QLabel
                                                                                    - comboBox_main_axis: QComboBox
                                                                                    - label_23: QLabel
                                                                                    - lineEdit_wall_thickness_liquid: QLineEdit
                                                                                    - label_16: QLabel
                                                                        - frame_3: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - lineEdit_polytropic_exponent: QLineEdit
                                                                                    - label_molar_mass_2: QLabel
                                                                                    - lineEdit_selected_liquid_fluid: QLineEdit
                                                                                    - label_13: QLabel
                                                                                    - label_bulk_modulus_unit: QLabel
                                                                                    - lineEdit_gas_pressure: QLineEdit
                                                                                    - comboBox_temperature_units: QComboBox
                                                                                    - label_molar_mass: QLabel
                                                                                    - comboBox_pressure_units: QComboBox
                                                                                    - label_45: QLabel
                                                                                    - lineEdit_gas_temperature: QLineEdit
                                                                                    - pushButton_get_liquid_fluid: QPushButton
                                                                                    - label_43: QLabel
                                                                                    - comboBox_fluid_data_source: QComboBox
                                                                                    - label_molar_mass_3: QLabel
                                                                                    - label_isentropic_exp: QLabel
                                                                                    - lineEdit_selected_gas_fluid: QLineEdit
                                                                                    - pushButton_get_gas_fluid: QPushButton
                                            - tab_remove: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_remove_selection: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_selected_damper_label: QLineEdit
                                                                    - label_2: QLabel
                                                                    - label_3: QLabel
                                                                    - lineEdit_damper_type: QLineEdit
                                                        - frame_treeWidget: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_pulsation_damper_info: QTreeWidget
                                                        - frame_remove_buttons: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                                                                    - pushButton_edit: QPushButton
                                                                    - pushButton_copy: QPushButton
                            - frame_5: QFrame
                                - (Layout): QHBoxLayout
                                        - label_12: QLabel
                                        - lineEdit_damper_label: QLineEdit
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - label_11: QLabel
                                        - lineEdit_connecting_coord_y: QLineEdit
                                        - lineEdit_connecting_coord_z: QLineEdit
                                        - label_10: QLabel
                                        - label_46: QLabel
                                        - label_8: QLabel
                                        - lineEdit_connecting_coord_x: QLineEdit
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - label_4: QLabel
                            - preview_widget_placeholder: QWidget
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_create: QPushButton
                            - pushButton_show_errors: QPushButton
                - frame_18: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
