# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_fluid_composition_input.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QDialog, QDoubleSpinBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 650)
        Dialog.setMinimumSize(QSize(1000, 650))
        Dialog.setMaximumSize(QSize(1200, 800))
        self.gridLayout_11 = QGridLayout(Dialog)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout_10 = QGridLayout(self.frame_title)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout_9 = QGridLayout(self.frame)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.frame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 980, 374))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_refprop_fluids = QTreeWidget(self.scrollAreaWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_refprop_fluids.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_refprop_fluids.setObjectName(u"treeWidget_refprop_fluids")
        self.treeWidget_refprop_fluids.setMinimumSize(QSize(390, 0))
        self.treeWidget_refprop_fluids.setMaximumSize(QSize(390, 16777215))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(8)
        self.treeWidget_refprop_fluids.setFont(font1)
        self.treeWidget_refprop_fluids.setStyleSheet(u"")
        self.treeWidget_refprop_fluids.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.treeWidget_refprop_fluids.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.treeWidget_refprop_fluids.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

        self.gridLayout_2.addWidget(self.treeWidget_refprop_fluids, 0, 0, 1, 1)

        self.frame_middle = QFrame(self.scrollAreaWidgetContents)
        self.frame_middle.setObjectName(u"frame_middle")
        self.frame_middle.setMinimumSize(QSize(140, 0))
        self.frame_middle.setMaximumSize(QSize(160, 16777215))
        self.frame_middle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_middle.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_middle)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.label_remaining_composition = QLabel(self.frame_middle)
        self.label_remaining_composition.setObjectName(u"label_remaining_composition")
        self.label_remaining_composition.setMinimumSize(QSize(130, 28))
        self.label_remaining_composition.setMaximumSize(QSize(140, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_remaining_composition.setFont(font2)
        self.label_remaining_composition.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.label_remaining_composition.setFrameShape(QFrame.Shape.Box)
        self.label_remaining_composition.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_remaining_composition.setWordWrap(True)

        self.gridLayout_18.addWidget(self.label_remaining_composition, 3, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_8, 1, 0, 1, 1)

        self.pushButton_add_gas = QPushButton(self.frame_middle)
        self.pushButton_add_gas.setObjectName(u"pushButton_add_gas")
        self.pushButton_add_gas.setMinimumSize(QSize(130, 30))
        self.pushButton_add_gas.setMaximumSize(QSize(140, 30))
        font3 = QFont()
        font3.setPointSize(10)
        self.pushButton_add_gas.setFont(font3)
        self.pushButton_add_gas.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.pushButton_add_gas, 5, 0, 1, 1)

        self.pushButton_fluid_configuration_mode = QPushButton(self.frame_middle)
        self.pushButton_fluid_configuration_mode.setObjectName(u"pushButton_fluid_configuration_mode")
        self.pushButton_fluid_configuration_mode.setMinimumSize(QSize(130, 30))
        self.pushButton_fluid_configuration_mode.setMaximumSize(QSize(140, 30))
        self.pushButton_fluid_configuration_mode.setFont(font3)
        self.pushButton_fluid_configuration_mode.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.pushButton_fluid_configuration_mode, 9, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_7, 4, 0, 1, 1)

        self.pushButton_load_composition = QPushButton(self.frame_middle)
        self.pushButton_load_composition.setObjectName(u"pushButton_load_composition")
        self.pushButton_load_composition.setMinimumSize(QSize(130, 30))
        self.pushButton_load_composition.setMaximumSize(QSize(140, 30))
        self.pushButton_load_composition.setFont(font3)
        self.pushButton_load_composition.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.pushButton_load_composition, 8, 0, 1, 1)

        self.pushButton_remove_gas = QPushButton(self.frame_middle)
        self.pushButton_remove_gas.setObjectName(u"pushButton_remove_gas")
        self.pushButton_remove_gas.setMinimumSize(QSize(130, 30))
        self.pushButton_remove_gas.setMaximumSize(QSize(140, 30))
        self.pushButton_remove_gas.setFont(font3)
        self.pushButton_remove_gas.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.pushButton_remove_gas, 6, 0, 1, 1)

        self.label_title_remaining_fraction = QLabel(self.frame_middle)
        self.label_title_remaining_fraction.setObjectName(u"label_title_remaining_fraction")
        self.label_title_remaining_fraction.setMinimumSize(QSize(130, 0))
        self.label_title_remaining_fraction.setMaximumSize(QSize(140, 36))
        font4 = QFont()
        font4.setPointSize(9)
        self.label_title_remaining_fraction.setFont(font4)
        self.label_title_remaining_fraction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title_remaining_fraction.setWordWrap(True)

        self.gridLayout_18.addWidget(self.label_title_remaining_fraction, 2, 0, 1, 1)

        self.pushButton_reset_fluid = QPushButton(self.frame_middle)
        self.pushButton_reset_fluid.setObjectName(u"pushButton_reset_fluid")
        self.pushButton_reset_fluid.setMinimumSize(QSize(130, 30))
        self.pushButton_reset_fluid.setMaximumSize(QSize(140, 30))
        self.pushButton_reset_fluid.setFont(font3)
        self.pushButton_reset_fluid.setStyleSheet(u"")

        self.gridLayout_18.addWidget(self.pushButton_reset_fluid, 7, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_middle, 0, 1, 1, 1)

        self.tableWidget_new_fluid = QTableWidget(self.scrollAreaWidgetContents)
        if (self.tableWidget_new_fluid.columnCount() < 2):
            self.tableWidget_new_fluid.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_new_fluid.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_new_fluid.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget_new_fluid.setObjectName(u"tableWidget_new_fluid")
        self.tableWidget_new_fluid.setMinimumSize(QSize(390, 0))
        self.tableWidget_new_fluid.setMaximumSize(QSize(390, 16777215))
        self.tableWidget_new_fluid.setFont(font1)
        self.tableWidget_new_fluid.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget_new_fluid.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.EditKeyPressed)
        self.tableWidget_new_fluid.setDragDropOverwriteMode(False)
        self.tableWidget_new_fluid.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.tableWidget_new_fluid.setAlternatingRowColors(False)
        self.tableWidget_new_fluid.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tableWidget_new_fluid.setSortingEnabled(True)
        self.tableWidget_new_fluid.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.tableWidget_new_fluid, 0, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_9.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.frame_states = QFrame(self.frame)
        self.frame_states.setObjectName(u"frame_states")
        self.frame_states.setMinimumSize(QSize(0, 110))
        self.frame_states.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_states.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_states)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.frame_states)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 60))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, 6, 6, 6)
        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 28))
        self.label_5.setMaximumSize(QSize(140, 28))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setKerning(False)
        self.label_5.setFont(font5)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_5, 1, 1, 1, 1)

        self.lineEdit_fluid_name = QLineEdit(self.frame_5)
        self.lineEdit_fluid_name.setObjectName(u"lineEdit_fluid_name")
        self.lineEdit_fluid_name.setMinimumSize(QSize(240, 28))
        self.lineEdit_fluid_name.setMaximumSize(QSize(350, 28))
        self.lineEdit_fluid_name.setStyleSheet(u"")
        self.lineEdit_fluid_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_fluid_name, 1, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_4, 1, 3, 1, 1)

        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(140, 28))
        self.label_3.setFont(font5)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_spacing = QLabel(self.frame_5)
        self.label_spacing.setObjectName(u"label_spacing")
        self.label_spacing.setMinimumSize(QSize(100, 20))
        self.label_spacing.setMaximumSize(QSize(1000, 20))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.label_spacing.setFont(font6)
        self.label_spacing.setFrameShape(QFrame.Shape.NoFrame)
        self.label_spacing.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_spacing, 0, 2, 1, 1)

        self.label_selected_fluid = QLabel(self.frame_5)
        self.label_selected_fluid.setObjectName(u"label_selected_fluid")
        self.label_selected_fluid.setMinimumSize(QSize(240, 28))
        self.label_selected_fluid.setMaximumSize(QSize(350, 28))
        font7 = QFont()
        font7.setPointSize(8)
        self.label_selected_fluid.setFont(font7)
        self.label_selected_fluid.setStyleSheet(u"")
        self.label_selected_fluid.setFrameShape(QFrame.Shape.Box)
        self.label_selected_fluid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_selected_fluid.setWordWrap(True)
        self.label_selected_fluid.setMargin(2)
        self.label_selected_fluid.setIndent(2)

        self.gridLayout_14.addWidget(self.label_selected_fluid, 2, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_states)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_10)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_2, 1, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.lineEdit_temperature_left = QLineEdit(self.frame_10)
        self.lineEdit_temperature_left.setObjectName(u"lineEdit_temperature_left")
        self.lineEdit_temperature_left.setMinimumSize(QSize(130, 28))
        self.lineEdit_temperature_left.setMaximumSize(QSize(180, 28))
        font8 = QFont()
        font8.setPointSize(10)
        font8.setBold(False)
        font8.setItalic(False)
        self.lineEdit_temperature_left.setFont(font8)
        self.lineEdit_temperature_left.setStyleSheet(u"")
        self.lineEdit_temperature_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_temperature_left, 1, 2, 1, 1)

        self.label_temperature = QLabel(self.frame_10)
        self.label_temperature.setObjectName(u"label_temperature")
        self.label_temperature.setMinimumSize(QSize(90, 28))
        self.label_temperature.setMaximumSize(QSize(400, 28))
        font9 = QFont()
        font9.setFamilies([u"MS Shell Dlg 2"])
        font9.setPointSize(10)
        font9.setBold(False)
        font9.setItalic(False)
        font9.setKerning(False)
        self.label_temperature.setFont(font9)
        self.label_temperature.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_temperature, 1, 1, 1, 1)

        self.lineEdit_temperature_right = QLineEdit(self.frame_10)
        self.lineEdit_temperature_right.setObjectName(u"lineEdit_temperature_right")
        self.lineEdit_temperature_right.setMinimumSize(QSize(130, 28))
        self.lineEdit_temperature_right.setMaximumSize(QSize(180, 28))
        self.lineEdit_temperature_right.setFont(font8)
        self.lineEdit_temperature_right.setStyleSheet(u"")
        self.lineEdit_temperature_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_temperature_right, 1, 3, 1, 1)

        self.label_pressure = QLabel(self.frame_10)
        self.label_pressure.setObjectName(u"label_pressure")
        self.label_pressure.setMinimumSize(QSize(90, 28))
        self.label_pressure.setMaximumSize(QSize(400, 28))
        self.label_pressure.setFont(font9)
        self.label_pressure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_pressure, 2, 1, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_10)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(100, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(100, 28))
        font10 = QFont()
        font10.setFamilies([u"MS Shell Dlg 2"])
        font10.setItalic(False)
        self.comboBox_temperature_units.setFont(font10)

        self.gridLayout_15.addWidget(self.comboBox_temperature_units, 1, 4, 1, 1)

        self.lineEdit_pressure_left = QLineEdit(self.frame_10)
        self.lineEdit_pressure_left.setObjectName(u"lineEdit_pressure_left")
        self.lineEdit_pressure_left.setEnabled(True)
        self.lineEdit_pressure_left.setMinimumSize(QSize(130, 28))
        self.lineEdit_pressure_left.setMaximumSize(QSize(180, 28))
        self.lineEdit_pressure_left.setFont(font8)
        self.lineEdit_pressure_left.setStyleSheet(u"")
        self.lineEdit_pressure_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_pressure_left, 2, 2, 1, 1)

        self.label_thermostate_left = QLabel(self.frame_10)
        self.label_thermostate_left.setObjectName(u"label_thermostate_left")
        self.label_thermostate_left.setMinimumSize(QSize(100, 20))
        self.label_thermostate_left.setMaximumSize(QSize(16777215, 20))
        self.label_thermostate_left.setFont(font6)
        self.label_thermostate_left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_thermostate_left, 0, 2, 1, 1)

        self.label_thermostate_right = QLabel(self.frame_10)
        self.label_thermostate_right.setObjectName(u"label_thermostate_right")
        self.label_thermostate_right.setMinimumSize(QSize(100, 20))
        self.label_thermostate_right.setMaximumSize(QSize(16777215, 20))
        self.label_thermostate_right.setFont(font6)
        self.label_thermostate_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_thermostate_right, 0, 3, 1, 1)

        self.lineEdit_pressure_right = QLineEdit(self.frame_10)
        self.lineEdit_pressure_right.setObjectName(u"lineEdit_pressure_right")
        self.lineEdit_pressure_right.setEnabled(True)
        self.lineEdit_pressure_right.setMinimumSize(QSize(130, 28))
        self.lineEdit_pressure_right.setMaximumSize(QSize(180, 28))
        self.lineEdit_pressure_right.setFont(font8)
        self.lineEdit_pressure_right.setStyleSheet(u"")
        self.lineEdit_pressure_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_pressure_right, 2, 3, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_10)
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
        self.comboBox_pressure_units.setFont(font10)

        self.gridLayout_15.addWidget(self.comboBox_pressure_units, 2, 4, 1, 1)


        self.gridLayout.addWidget(self.frame_10, 1, 1, 1, 1)

        self.frame_multiple_fluids = QFrame(self.frame_states)
        self.frame_multiple_fluids.setObjectName(u"frame_multiple_fluids")
        self.frame_multiple_fluids.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_multiple_fluids.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_multiple_fluids)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.spinBox_number_of_fluids = QSpinBox(self.frame_multiple_fluids)
        self.spinBox_number_of_fluids.setObjectName(u"spinBox_number_of_fluids")
        self.spinBox_number_of_fluids.setMinimumSize(QSize(100, 28))
        self.spinBox_number_of_fluids.setMaximumSize(QSize(16777215, 28))
        self.spinBox_number_of_fluids.setFont(font3)
        self.spinBox_number_of_fluids.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_number_of_fluids.setMinimum(1)
        self.spinBox_number_of_fluids.setMaximum(100)

        self.gridLayout_6.addWidget(self.spinBox_number_of_fluids, 0, 2, 1, 1)

        self.label_number_of_fluids = QLabel(self.frame_multiple_fluids)
        self.label_number_of_fluids.setObjectName(u"label_number_of_fluids")
        self.label_number_of_fluids.setMinimumSize(QSize(110, 28))
        self.label_number_of_fluids.setMaximumSize(QSize(400, 28))
        self.label_number_of_fluids.setFont(font9)
        self.label_number_of_fluids.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_number_of_fluids, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 10, 1, 1)

        self.label_decay_factor_2 = QLabel(self.frame_multiple_fluids)
        self.label_decay_factor_2.setObjectName(u"label_decay_factor_2")
        self.label_decay_factor_2.setMinimumSize(QSize(110, 28))
        self.label_decay_factor_2.setMaximumSize(QSize(400, 28))
        self.label_decay_factor_2.setFont(font9)
        self.label_decay_factor_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_decay_factor_2, 0, 8, 1, 1)

        self.label_decay_factor = QLabel(self.frame_multiple_fluids)
        self.label_decay_factor.setObjectName(u"label_decay_factor")
        self.label_decay_factor.setMinimumSize(QSize(110, 28))
        self.label_decay_factor.setMaximumSize(QSize(400, 28))
        self.label_decay_factor.setFont(font9)
        self.label_decay_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_decay_factor, 0, 6, 1, 1)

        self.label_distribution_type = QLabel(self.frame_multiple_fluids)
        self.label_distribution_type.setObjectName(u"label_distribution_type")
        self.label_distribution_type.setMinimumSize(QSize(110, 28))
        self.label_distribution_type.setMaximumSize(QSize(400, 28))
        self.label_distribution_type.setFont(font9)
        self.label_distribution_type.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_distribution_type, 0, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.comboBox_distribution_type = QComboBox(self.frame_multiple_fluids)
        self.comboBox_distribution_type.addItem("")
        self.comboBox_distribution_type.addItem("")
        self.comboBox_distribution_type.setObjectName(u"comboBox_distribution_type")
        self.comboBox_distribution_type.setMinimumSize(QSize(100, 28))
        self.comboBox_distribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_distribution_type.setFont(font3)

        self.gridLayout_6.addWidget(self.comboBox_distribution_type, 0, 5, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)

        self.doubleSpinBox_decay_factor = QDoubleSpinBox(self.frame_multiple_fluids)
        self.doubleSpinBox_decay_factor.setObjectName(u"doubleSpinBox_decay_factor")
        self.doubleSpinBox_decay_factor.setMinimumSize(QSize(100, 28))
        self.doubleSpinBox_decay_factor.setMaximumSize(QSize(16777215, 28))
        self.doubleSpinBox_decay_factor.setFont(font3)
        self.doubleSpinBox_decay_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_decay_factor.setDecimals(4)
        self.doubleSpinBox_decay_factor.setMaximum(0.900000000000000)
        self.doubleSpinBox_decay_factor.setSingleStep(0.010000000000000)
        self.doubleSpinBox_decay_factor.setValue(0.500000000000000)

        self.gridLayout_6.addWidget(self.doubleSpinBox_decay_factor, 0, 7, 1, 1)

        self.comboBox_color_scale = QComboBox(self.frame_multiple_fluids)
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.setObjectName(u"comboBox_color_scale")
        self.comboBox_color_scale.setMinimumSize(QSize(100, 28))
        self.comboBox_color_scale.setMaximumSize(QSize(16777215, 28))
        self.comboBox_color_scale.setFont(font3)

        self.gridLayout_6.addWidget(self.comboBox_color_scale, 0, 9, 1, 1)


        self.gridLayout.addWidget(self.frame_multiple_fluids, 0, 0, 1, 2)


        self.gridLayout_9.addWidget(self.frame_states, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_buttons)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(160, 30))
        self.pushButton_exit.setMaximumSize(QSize(160, 30))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_confirm = QPushButton(self.frame_buttons)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(160, 30))
        self.pushButton_confirm.setMaximumSize(QSize(160, 30))
        self.pushButton_confirm.setFont(font3)
        self.pushButton_confirm.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_confirm, 0, 1, 1, 1)


        self.gridLayout_11.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_fluid_name, self.lineEdit_temperature_left)
        QWidget.setTabOrder(self.lineEdit_temperature_left, self.lineEdit_temperature_right)
        QWidget.setTabOrder(self.lineEdit_temperature_right, self.lineEdit_pressure_left)
        QWidget.setTabOrder(self.lineEdit_pressure_left, self.lineEdit_pressure_right)
        QWidget.setTabOrder(self.lineEdit_pressure_right, self.comboBox_temperature_units)
        QWidget.setTabOrder(self.comboBox_temperature_units, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.treeWidget_refprop_fluids)
        QWidget.setTabOrder(self.treeWidget_refprop_fluids, self.tableWidget_new_fluid)

        self.retranslateUi(Dialog)

        self.comboBox_temperature_units.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set fluid mixture composition", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Set the fluid composition", None))
        ___qtreewidgetitem = self.treeWidget_refprop_fluids.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Fluids from refprop library", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_refprop_fluids.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>To add a new fluid to the mixture, you can either double-click or drag and drop.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_remaining_composition.setText("")
        self.pushButton_add_gas.setText(QCoreApplication.translate("Dialog", u"Add gas", None))
        self.pushButton_fluid_configuration_mode.setText(QCoreApplication.translate("Dialog", u"Single fluid mode", None))
        self.pushButton_load_composition.setText(QCoreApplication.translate("Dialog", u"Load composition", None))
        self.pushButton_remove_gas.setText(QCoreApplication.translate("Dialog", u"Remove gas", None))
        self.label_title_remaining_fraction.setText(QCoreApplication.translate("Dialog", u"Remaining molar \n"
"fraction [%]", None))
        self.pushButton_reset_fluid.setText(QCoreApplication.translate("Dialog", u"Reset fluid", None))
        ___qtablewidgetitem = self.tableWidget_new_fluid.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Fluid name", None))
        ___qtablewidgetitem1 = self.tableWidget_new_fluid.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Molar fraction [%]", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Fluid name:", None))
#if QT_CONFIG(whatsthis)
        self.lineEdit_fluid_name.setWhatsThis(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Insert a fluid name</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_fluid_name.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.label_spacing.setText("")
        self.label_selected_fluid.setText("")
        self.lineEdit_temperature_left.setText("")
        self.label_temperature.setText(QCoreApplication.translate("Dialog", u"Temperature:", None))
        self.lineEdit_temperature_right.setText("")
        self.label_pressure.setText(QCoreApplication.translate("Dialog", u"Pressure:", None))
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"\u00b0C", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"\u00b0F", None))

        self.lineEdit_pressure_left.setText("")
        self.label_thermostate_left.setText(QCoreApplication.translate("Dialog", u"Suction", None))
        self.label_thermostate_right.setText(QCoreApplication.translate("Dialog", u"Discharge", None))
        self.lineEdit_pressure_right.setText("")
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

        self.label_number_of_fluids.setText(QCoreApplication.translate("Dialog", u"Number of fluids:", None))
        self.label_decay_factor_2.setText(QCoreApplication.translate("Dialog", u"Color scale:", None))
        self.label_decay_factor.setText(QCoreApplication.translate("Dialog", u"Decay factor:", None))
        self.label_distribution_type.setText(QCoreApplication.translate("Dialog", u"Distribution type:", None))
        self.comboBox_distribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"Linear", None))
        self.comboBox_distribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Exponential", None))

#if QT_CONFIG(tooltip)
        self.doubleSpinBox_decay_factor.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>This factor represents the amount of decay </p><p>reached in the middle of the distribution.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_color_scale.setItemText(0, QCoreApplication.translate("Dialog", u"Red-to-blue", None))
        self.comboBox_color_scale.setItemText(1, QCoreApplication.translate("Dialog", u"Blue-to-red", None))

        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Get fluid properties", None))
    # retranslateUi



class SetFluidCompositionInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_refprop_fluids: QTreeWidget
                                            - frame_middle: QFrame
                                                - (Layout): QGridLayout
                                                        - label_remaining_composition: QLabel
                                                        - pushButton_add_gas: QPushButton
                                                        - pushButton_fluid_configuration_mode: QPushButton
                                                        - pushButton_load_composition: QPushButton
                                                        - pushButton_remove_gas: QPushButton
                                                        - label_title_remaining_fraction: QLabel
                                                        - pushButton_reset_fluid: QPushButton
                                            - tableWidget_new_fluid: QTableWidget
                            - frame_states: QFrame
                                - (Layout): QGridLayout
                                        - frame_5: QFrame
                                            - (Layout): QGridLayout
                                                    - label_5: QLabel
                                                    - lineEdit_fluid_name: QLineEdit
                                                    - label_3: QLabel
                                                    - label_spacing: QLabel
                                                    - label_selected_fluid: QLabel
                                        - frame_10: QFrame
                                            - (Layout): QGridLayout
                                                    - lineEdit_temperature_left: QLineEdit
                                                    - label_temperature: QLabel
                                                    - lineEdit_temperature_right: QLineEdit
                                                    - label_pressure: QLabel
                                                    - comboBox_temperature_units: QComboBox
                                                    - lineEdit_pressure_left: QLineEdit
                                                    - label_thermostate_left: QLabel
                                                    - label_thermostate_right: QLabel
                                                    - lineEdit_pressure_right: QLineEdit
                                                    - comboBox_pressure_units: QComboBox
                                        - frame_multiple_fluids: QFrame
                                            - (Layout): QGridLayout
                                                    - spinBox_number_of_fluids: QSpinBox
                                                    - label_number_of_fluids: QLabel
                                                    - label_decay_factor_2: QLabel
                                                    - label_decay_factor: QLabel
                                                    - label_distribution_type: QLabel
                                                    - comboBox_distribution_type: QComboBox
                                                    - doubleSpinBox_decay_factor: QDoubleSpinBox
                                                    - comboBox_color_scale: QComboBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
