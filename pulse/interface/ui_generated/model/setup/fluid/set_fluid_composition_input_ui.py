# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_fluid_composition_input.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QDialog, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 612)
        Dialog.setMinimumSize(QSize(1000, 612))
        Dialog.setMaximumSize(QSize(1000, 612))
        self.gridLayout_11 = QGridLayout(Dialog)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Sunken)
        self.gridLayout_10 = QGridLayout(self.frame_title)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 500))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.gridLayout_9 = QGridLayout(self.frame)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.frame_states = QFrame(self.frame)
        self.frame_states.setObjectName(u"frame_states")
        self.frame_states.setMinimumSize(QSize(0, 110))
        self.frame_states.setFrameShape(QFrame.NoFrame)
        self.frame_states.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_states)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.frame_states)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 60))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 28))
        self.label_5.setMaximumSize(QSize(140, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setKerning(False)
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_5, 1, 1, 1, 1)

        self.lineEdit_fluid_name = QLineEdit(self.frame_5)
        self.lineEdit_fluid_name.setObjectName(u"lineEdit_fluid_name")
        self.lineEdit_fluid_name.setMinimumSize(QSize(240, 28))
        self.lineEdit_fluid_name.setMaximumSize(QSize(350, 28))
        self.lineEdit_fluid_name.setStyleSheet(u"")
        self.lineEdit_fluid_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_fluid_name, 1, 2, 1, 1)

        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(140, 28))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_spacing = QLabel(self.frame_5)
        self.label_spacing.setObjectName(u"label_spacing")
        self.label_spacing.setMinimumSize(QSize(100, 20))
        self.label_spacing.setMaximumSize(QSize(1000, 20))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_spacing.setFont(font2)
        self.label_spacing.setFrameShape(QFrame.NoFrame)
        self.label_spacing.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.label_spacing, 0, 2, 1, 1)

        self.label_selected_fluid = QLabel(self.frame_5)
        self.label_selected_fluid.setObjectName(u"label_selected_fluid")
        self.label_selected_fluid.setMinimumSize(QSize(240, 28))
        self.label_selected_fluid.setMaximumSize(QSize(350, 28))
        font3 = QFont()
        font3.setPointSize(8)
        self.label_selected_fluid.setFont(font3)
        self.label_selected_fluid.setStyleSheet(u"")
        self.label_selected_fluid.setFrameShape(QFrame.Box)
        self.label_selected_fluid.setAlignment(Qt.AlignCenter)
        self.label_selected_fluid.setWordWrap(True)
        self.label_selected_fluid.setMargin(2)
        self.label_selected_fluid.setIndent(2)

        self.gridLayout_14.addWidget(self.label_selected_fluid, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_4, 1, 3, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_states)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_10)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.label_discharge = QLabel(self.frame_10)
        self.label_discharge.setObjectName(u"label_discharge")
        self.label_discharge.setMinimumSize(QSize(100, 20))
        self.label_discharge.setMaximumSize(QSize(100, 20))
        self.label_discharge.setFont(font2)
        self.label_discharge.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_discharge, 0, 3, 1, 1)

        self.comboBox_temperature_units = QComboBox(self.frame_10)
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.addItem("")
        self.comboBox_temperature_units.setObjectName(u"comboBox_temperature_units")
        self.comboBox_temperature_units.setMinimumSize(QSize(100, 28))
        self.comboBox_temperature_units.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setItalic(False)
        self.comboBox_temperature_units.setFont(font4)

        self.gridLayout_15.addWidget(self.comboBox_temperature_units, 1, 4, 1, 1)

        self.lineEdit_pressure_disch = QLineEdit(self.frame_10)
        self.lineEdit_pressure_disch.setObjectName(u"lineEdit_pressure_disch")
        self.lineEdit_pressure_disch.setEnabled(True)
        self.lineEdit_pressure_disch.setMinimumSize(QSize(130, 28))
        self.lineEdit_pressure_disch.setMaximumSize(QSize(180, 28))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        self.lineEdit_pressure_disch.setFont(font5)
        self.lineEdit_pressure_disch.setStyleSheet(u"")
        self.lineEdit_pressure_disch.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_pressure_disch, 2, 3, 1, 1)

        self.label_suction = QLabel(self.frame_10)
        self.label_suction.setObjectName(u"label_suction")
        self.label_suction.setMinimumSize(QSize(100, 20))
        self.label_suction.setMaximumSize(QSize(100, 20))
        self.label_suction.setFont(font2)
        self.label_suction.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_suction, 0, 2, 1, 1)

        self.lineEdit_pressure = QLineEdit(self.frame_10)
        self.lineEdit_pressure.setObjectName(u"lineEdit_pressure")
        self.lineEdit_pressure.setEnabled(True)
        self.lineEdit_pressure.setMinimumSize(QSize(130, 28))
        self.lineEdit_pressure.setMaximumSize(QSize(180, 28))
        self.lineEdit_pressure.setFont(font5)
        self.lineEdit_pressure.setStyleSheet(u"")
        self.lineEdit_pressure.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_pressure, 2, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.label_9 = QLabel(self.frame_10)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(90, 28))
        self.label_9.setMaximumSize(QSize(400, 28))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        font6.setKerning(False)
        self.label_9.setFont(font6)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_9, 2, 1, 1, 1)

        self.lineEdit_temperature = QLineEdit(self.frame_10)
        self.lineEdit_temperature.setObjectName(u"lineEdit_temperature")
        self.lineEdit_temperature.setMinimumSize(QSize(130, 28))
        self.lineEdit_temperature.setMaximumSize(QSize(180, 28))
        self.lineEdit_temperature.setFont(font5)
        self.lineEdit_temperature.setStyleSheet(u"")
        self.lineEdit_temperature.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_temperature, 1, 2, 1, 1)

        self.label_10 = QLabel(self.frame_10)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(90, 28))
        self.label_10.setMaximumSize(QSize(400, 28))
        self.label_10.setFont(font6)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_10, 1, 1, 1, 1)

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
        self.comboBox_pressure_units.setFont(font4)

        self.gridLayout_15.addWidget(self.comboBox_pressure_units, 2, 4, 1, 1)

        self.lineEdit_temperature_disch = QLineEdit(self.frame_10)
        self.lineEdit_temperature_disch.setObjectName(u"lineEdit_temperature_disch")
        self.lineEdit_temperature_disch.setMinimumSize(QSize(130, 28))
        self.lineEdit_temperature_disch.setMaximumSize(QSize(180, 28))
        self.lineEdit_temperature_disch.setFont(font5)
        self.lineEdit_temperature_disch.setStyleSheet(u"")
        self.lineEdit_temperature_disch.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_temperature_disch, 1, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_2, 1, 5, 1, 1)


        self.gridLayout.addWidget(self.frame_10, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_states, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(self.frame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 980, 374))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_reference_gases = QTreeWidget(self.scrollAreaWidgetContents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_reference_gases.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_reference_gases.setObjectName(u"treeWidget_reference_gases")
        self.treeWidget_reference_gases.setMinimumSize(QSize(390, 0))
        self.treeWidget_reference_gases.setMaximumSize(QSize(390, 350))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(8)
        self.treeWidget_reference_gases.setFont(font7)
        self.treeWidget_reference_gases.setStyleSheet(u"")
        self.treeWidget_reference_gases.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.treeWidget_reference_gases.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.treeWidget_reference_gases.setDragDropMode(QAbstractItemView.DragOnly)

        self.gridLayout_2.addWidget(self.treeWidget_reference_gases, 0, 0, 1, 1)

        self.tableWidget_new_fluid = QTableWidget(self.scrollAreaWidgetContents)
        if (self.tableWidget_new_fluid.columnCount() < 2):
            self.tableWidget_new_fluid.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_new_fluid.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_new_fluid.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget_new_fluid.setObjectName(u"tableWidget_new_fluid")
        self.tableWidget_new_fluid.setMinimumSize(QSize(390, 0))
        self.tableWidget_new_fluid.setMaximumSize(QSize(390, 350))
        self.tableWidget_new_fluid.setFont(font7)
        self.tableWidget_new_fluid.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_new_fluid.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableWidget_new_fluid.setDragDropOverwriteMode(False)
        self.tableWidget_new_fluid.setDragDropMode(QAbstractItemView.DropOnly)
        self.tableWidget_new_fluid.setAlternatingRowColors(False)
        self.tableWidget_new_fluid.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget_new_fluid.setSortingEnabled(True)
        self.tableWidget_new_fluid.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.tableWidget_new_fluid, 0, 2, 1, 1)

        self.frame_middle_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_middle_2.setObjectName(u"frame_middle_2")
        self.frame_middle_2.setMinimumSize(QSize(140, 0))
        self.frame_middle_2.setMaximumSize(QSize(160, 350))
        self.frame_middle_2.setFrameShape(QFrame.NoFrame)
        self.frame_middle_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_middle_2)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.pushButton_add_gas = QPushButton(self.frame_middle_2)
        self.pushButton_add_gas.setObjectName(u"pushButton_add_gas")
        self.pushButton_add_gas.setMinimumSize(QSize(120, 30))
        self.pushButton_add_gas.setMaximumSize(QSize(120, 30))
        font8 = QFont()
        font8.setPointSize(10)
        self.pushButton_add_gas.setFont(font8)
        self.pushButton_add_gas.setStyleSheet(u"")
        self.pushButton_add_gas.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_add_gas, 8, 0, 1, 1)

        self.lineEdit_composition = QLineEdit(self.frame_middle_2)
        self.lineEdit_composition.setObjectName(u"lineEdit_composition")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_composition.sizePolicy().hasHeightForWidth())
        self.lineEdit_composition.setSizePolicy(sizePolicy)
        self.lineEdit_composition.setMinimumSize(QSize(120, 28))
        self.lineEdit_composition.setMaximumSize(QSize(120, 28))
        self.lineEdit_composition.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.lineEdit_composition, 6, 0, 1, 1)

        self.label_6 = QLabel(self.frame_middle_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 26))
        self.label_6.setMaximumSize(QSize(120, 26))
        font9 = QFont()
        font9.setPointSize(9)
        self.label_6.setFont(font9)
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_18.addWidget(self.label_6, 5, 0, 1, 1)

        self.pushButton_load_composition = QPushButton(self.frame_middle_2)
        self.pushButton_load_composition.setObjectName(u"pushButton_load_composition")
        self.pushButton_load_composition.setMinimumSize(QSize(120, 30))
        self.pushButton_load_composition.setMaximumSize(QSize(120, 30))
        self.pushButton_load_composition.setFont(font8)
        self.pushButton_load_composition.setStyleSheet(u"")
        self.pushButton_load_composition.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_load_composition, 10, 0, 1, 1)

        self.pushButton_reset_fluid = QPushButton(self.frame_middle_2)
        self.pushButton_reset_fluid.setObjectName(u"pushButton_reset_fluid")
        self.pushButton_reset_fluid.setMinimumSize(QSize(120, 30))
        self.pushButton_reset_fluid.setMaximumSize(QSize(120, 30))
        self.pushButton_reset_fluid.setFont(font8)
        self.pushButton_reset_fluid.setStyleSheet(u"")
        self.pushButton_reset_fluid.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_reset_fluid, 11, 0, 1, 1)

        self.pushButton_remove_gas = QPushButton(self.frame_middle_2)
        self.pushButton_remove_gas.setObjectName(u"pushButton_remove_gas")
        self.pushButton_remove_gas.setMinimumSize(QSize(120, 30))
        self.pushButton_remove_gas.setMaximumSize(QSize(120, 30))
        self.pushButton_remove_gas.setFont(font8)
        self.pushButton_remove_gas.setStyleSheet(u"")
        self.pushButton_remove_gas.setAutoDefault(False)

        self.gridLayout_18.addWidget(self.pushButton_remove_gas, 9, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_7, 7, 0, 1, 1)

        self.label_title_remaining_fraction = QLabel(self.frame_middle_2)
        self.label_title_remaining_fraction.setObjectName(u"label_title_remaining_fraction")
        self.label_title_remaining_fraction.setMinimumSize(QSize(120, 0))
        self.label_title_remaining_fraction.setMaximumSize(QSize(120, 36))
        self.label_title_remaining_fraction.setFont(font9)
        self.label_title_remaining_fraction.setAlignment(Qt.AlignCenter)
        self.label_title_remaining_fraction.setWordWrap(True)

        self.gridLayout_18.addWidget(self.label_title_remaining_fraction, 2, 0, 1, 1)

        self.label_remaining_composition = QLabel(self.frame_middle_2)
        self.label_remaining_composition.setObjectName(u"label_remaining_composition")
        self.label_remaining_composition.setMinimumSize(QSize(120, 28))
        self.label_remaining_composition.setMaximumSize(QSize(120, 28))
        font10 = QFont()
        font10.setPointSize(10)
        font10.setItalic(False)
        self.label_remaining_composition.setFont(font10)
        self.label_remaining_composition.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.label_remaining_composition.setFrameShape(QFrame.Box)
        self.label_remaining_composition.setAlignment(Qt.AlignCenter)
        self.label_remaining_composition.setWordWrap(True)

        self.gridLayout_18.addWidget(self.label_remaining_composition, 3, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_6, 4, 0, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_8, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_middle_2, 0, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_9.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(160, 30))
        self.pushButton_exit.setMaximumSize(QSize(160, 30))
        self.pushButton_exit.setFont(font8)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_confirm = QPushButton(self.frame_3)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(160, 30))
        self.pushButton_confirm.setMaximumSize(QSize(160, 30))
        self.pushButton_confirm.setFont(font8)
        self.pushButton_confirm.setStyleSheet(u"")
        self.pushButton_confirm.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_confirm, 0, 1, 1, 1)


        self.gridLayout_11.addWidget(self.frame_3, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_fluid_name, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.treeWidget_reference_gases)
        QWidget.setTabOrder(self.treeWidget_reference_gases, self.lineEdit_temperature)
        QWidget.setTabOrder(self.lineEdit_temperature, self.lineEdit_temperature_disch)
        QWidget.setTabOrder(self.lineEdit_temperature_disch, self.comboBox_temperature_units)
        QWidget.setTabOrder(self.comboBox_temperature_units, self.lineEdit_pressure)
        QWidget.setTabOrder(self.lineEdit_pressure, self.lineEdit_pressure_disch)
        QWidget.setTabOrder(self.lineEdit_pressure_disch, self.comboBox_pressure_units)
        QWidget.setTabOrder(self.comboBox_pressure_units, self.tableWidget_new_fluid)
        QWidget.setTabOrder(self.tableWidget_new_fluid, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_confirm)

        self.retranslateUi(Dialog)

        self.comboBox_temperature_units.setCurrentIndex(1)
        self.pushButton_exit.setDefault(False)
        self.pushButton_confirm.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set fluid mixture composition", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Set the fluid composition", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Fluid name:", None))
#if QT_CONFIG(whatsthis)
        self.lineEdit_fluid_name.setWhatsThis(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Insert a fluid name</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_fluid_name.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.label_spacing.setText("")
        self.label_selected_fluid.setText("")
        self.label_discharge.setText(QCoreApplication.translate("Dialog", u"Discharge", None))
        self.comboBox_temperature_units.setItemText(0, QCoreApplication.translate("Dialog", u"  K", None))
        self.comboBox_temperature_units.setItemText(1, QCoreApplication.translate("Dialog", u"  \u00baC", None))
        self.comboBox_temperature_units.setItemText(2, QCoreApplication.translate("Dialog", u"  \u00baF", None))

        self.lineEdit_pressure_disch.setText("")
        self.label_suction.setText(QCoreApplication.translate("Dialog", u"Suction", None))
        self.lineEdit_pressure.setText("")
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Pressure:", None))
        self.lineEdit_temperature.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Temperature:", None))
        self.comboBox_pressure_units.setItemText(0, QCoreApplication.translate("Dialog", u" Pa (a)", None))
        self.comboBox_pressure_units.setItemText(1, QCoreApplication.translate("Dialog", u" kPa (a)", None))
        self.comboBox_pressure_units.setItemText(2, QCoreApplication.translate("Dialog", u" atm (a)", None))
        self.comboBox_pressure_units.setItemText(3, QCoreApplication.translate("Dialog", u" bar (a)", None))
        self.comboBox_pressure_units.setItemText(4, QCoreApplication.translate("Dialog", u" kgf/cm\u00b2 (a)", None))
        self.comboBox_pressure_units.setItemText(5, QCoreApplication.translate("Dialog", u" psi (a)", None))
        self.comboBox_pressure_units.setItemText(6, QCoreApplication.translate("Dialog", u" ksi (a)", None))
        self.comboBox_pressure_units.setItemText(7, QCoreApplication.translate("Dialog", u" Pa (g)", None))
        self.comboBox_pressure_units.setItemText(8, QCoreApplication.translate("Dialog", u" kPa (g)", None))
        self.comboBox_pressure_units.setItemText(9, QCoreApplication.translate("Dialog", u" atm (g)", None))
        self.comboBox_pressure_units.setItemText(10, QCoreApplication.translate("Dialog", u" bar (g)", None))
        self.comboBox_pressure_units.setItemText(11, QCoreApplication.translate("Dialog", u" kgf/cm\u00b2 (g)", None))
        self.comboBox_pressure_units.setItemText(12, QCoreApplication.translate("Dialog", u" psi (g)", None))
        self.comboBox_pressure_units.setItemText(13, QCoreApplication.translate("Dialog", u" ksi (g)", None))

        self.lineEdit_temperature_disch.setText("")
        ___qtreewidgetitem = self.treeWidget_reference_gases.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Default fluid library", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_reference_gases.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Press double-click to add fluid to the mixture</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.tableWidget_new_fluid.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Fluid name", None));
        ___qtablewidgetitem1 = self.tableWidget_new_fluid.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Molar fraction [%]", None));
        self.pushButton_add_gas.setText(QCoreApplication.translate("Dialog", u"Add gas", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Molar fraction [%]", None))
        self.pushButton_load_composition.setText(QCoreApplication.translate("Dialog", u"Load composition", None))
        self.pushButton_reset_fluid.setText(QCoreApplication.translate("Dialog", u"Reset fluid", None))
        self.pushButton_remove_gas.setText(QCoreApplication.translate("Dialog", u"Remove gas", None))
        self.label_title_remaining_fraction.setText(QCoreApplication.translate("Dialog", u"Remaining molar \n"
"fraction [%]", None))
        self.label_remaining_composition.setText("")
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
                                                    - label_discharge: QLabel
                                                    - comboBox_temperature_units: QComboBox
                                                    - lineEdit_pressure_disch: QLineEdit
                                                    - label_suction: QLabel
                                                    - lineEdit_pressure: QLineEdit
                                                    - label_9: QLabel
                                                    - lineEdit_temperature: QLineEdit
                                                    - label_10: QLabel
                                                    - comboBox_pressure_units: QComboBox
                                                    - lineEdit_temperature_disch: QLineEdit
                            - scrollArea: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_reference_gases: QTreeWidget
                                            - tableWidget_new_fluid: QTableWidget
                                            - frame_middle_2: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_add_gas: QPushButton
                                                        - lineEdit_composition: QLineEdit
                                                        - label_6: QLabel
                                                        - pushButton_load_composition: QPushButton
                                                        - pushButton_reset_fluid: QPushButton
                                                        - pushButton_remove_gas: QPushButton
                                                        - label_title_remaining_fraction: QLabel
                                                        - label_remaining_composition: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
