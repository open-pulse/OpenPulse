# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'valve_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 600)
        Dialog.setMinimumSize(QSize(480, 320))
        Dialog.setMaximumSize(QSize(480, 600))
        font = QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.main_frame = QFrame(Dialog)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1600, 1600))
        self.main_frame.setFrameShape(QFrame.Box)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.main_frame)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.main_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(132, 0))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 4, 8, 4)
        self.tabWidget_main = QTabWidget(self.frame_4)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setEnabled(True)
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(600, 600))
        self.tabWidget_main.setFont(font)
        self.tabWidget_main.setTabShape(QTabWidget.Rounded)
        self.tabWidget_main.setDocumentMode(False)
        self.tabWidget_main.setTabsClosable(False)
        self.tabWidget_main.setMovable(False)
        self.tabWidget_main.setTabBarAutoHide(False)
        self.tab_valve_setup = QWidget()
        self.tab_valve_setup.setObjectName(u"tab_valve_setup")
        self.tab_valve_setup.setEnabled(True)
        self.gridLayout_8 = QGridLayout(self.tab_valve_setup)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.tab_valve_setup)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFocusPolicy(Qt.NoFocus)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 432, 372))
        self.gridLayout_10 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 8, 4, 2)
        self.label_selected_id_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_11.setObjectName(u"label_selected_id_11")
        self.label_selected_id_11.setEnabled(True)
        self.label_selected_id_11.setMinimumSize(QSize(180, 28))
        self.label_selected_id_11.setMaximumSize(QSize(220, 28))
        self.label_selected_id_11.setFont(font)
        self.label_selected_id_11.setMouseTracking(True)
        self.label_selected_id_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_11, 1, 1, 1, 1)

        self.label_flange_diameter_unit_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_3.setObjectName(u"label_flange_diameter_unit_3")
        self.label_flange_diameter_unit_3.setEnabled(True)
        self.label_flange_diameter_unit_3.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_3.setMaximumSize(QSize(40, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_flange_diameter_unit_3.setFont(font1)
        self.label_flange_diameter_unit_3.setMouseTracking(True)
        self.label_flange_diameter_unit_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_3, 5, 3, 1, 1)

        self.comboBox_flange_setup = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_flange_setup.addItem("")
        self.comboBox_flange_setup.addItem("")
        self.comboBox_flange_setup.setObjectName(u"comboBox_flange_setup")
        self.comboBox_flange_setup.setMinimumSize(QSize(0, 28))
        self.comboBox_flange_setup.setMaximumSize(QSize(16777215, 28))
        self.comboBox_flange_setup.setFont(font)

        self.gridLayout_10.addWidget(self.comboBox_flange_setup, 1, 2, 1, 1)

        self.label_flange_diameter_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_2.setObjectName(u"label_flange_diameter_2")
        self.label_flange_diameter_2.setEnabled(True)
        self.label_flange_diameter_2.setMinimumSize(QSize(180, 28))
        self.label_flange_diameter_2.setMaximumSize(QSize(220, 28))
        self.label_flange_diameter_2.setFont(font1)
        self.label_flange_diameter_2.setMouseTracking(True)
        self.label_flange_diameter_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_2, 4, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_2, 6, 4, 1, 1)

        self.label_flange_length = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_length.setObjectName(u"label_flange_length")
        self.label_flange_length.setEnabled(True)
        self.label_flange_length.setMinimumSize(QSize(180, 28))
        self.label_flange_length.setMaximumSize(QSize(220, 28))
        self.label_flange_length.setFont(font1)
        self.label_flange_length.setMouseTracking(True)
        self.label_flange_length.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_length, 9, 1, 1, 1)

        self.label_valve_internal_length_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_valve_internal_length_unit.setObjectName(u"label_valve_internal_length_unit")
        self.label_valve_internal_length_unit.setEnabled(True)
        self.label_valve_internal_length_unit.setMinimumSize(QSize(40, 28))
        self.label_valve_internal_length_unit.setMaximumSize(QSize(40, 28))
        self.label_valve_internal_length_unit.setFont(font1)
        self.label_valve_internal_length_unit.setMouseTracking(True)
        self.label_valve_internal_length_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_valve_internal_length_unit, 10, 3, 1, 1)

        self.label_flange_diameter = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter.setObjectName(u"label_flange_diameter")
        self.label_flange_diameter.setEnabled(True)
        self.label_flange_diameter.setMinimumSize(QSize(180, 28))
        self.label_flange_diameter.setMaximumSize(QSize(220, 28))
        self.label_flange_diameter.setFont(font1)
        self.label_flange_diameter.setMouseTracking(True)
        self.label_flange_diameter.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter, 8, 1, 1, 1)

        self.label_112 = QLabel(self.scrollAreaWidgetContents)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(40, 28))
        self.label_112.setMaximumSize(QSize(40, 28))
        self.label_112.setFont(font)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_112, 6, 3, 1, 1)

        self.label_selected_id_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_14.setObjectName(u"label_selected_id_14")
        self.label_selected_id_14.setEnabled(True)
        self.label_selected_id_14.setMinimumSize(QSize(180, 28))
        self.label_selected_id_14.setMaximumSize(QSize(220, 28))
        self.label_selected_id_14.setFont(font)
        self.label_selected_id_14.setMouseTracking(True)
        self.label_selected_id_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_14, 6, 1, 1, 1)

        self.lineEdit_flange_length = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_flange_length.setObjectName(u"lineEdit_flange_length")
        self.lineEdit_flange_length.setEnabled(True)
        self.lineEdit_flange_length.setMinimumSize(QSize(132, 28))
        self.lineEdit_flange_length.setMaximumSize(QSize(300, 28))
        self.lineEdit_flange_length.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_length.setFont(font)
        self.lineEdit_flange_length.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_flange_length.setStyleSheet(u"")
        self.lineEdit_flange_length.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_flange_length, 9, 2, 1, 1)

        self.label_selected_id_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_13.setObjectName(u"label_selected_id_13")
        self.label_selected_id_13.setEnabled(True)
        self.label_selected_id_13.setMinimumSize(QSize(180, 28))
        self.label_selected_id_13.setMaximumSize(QSize(220, 28))
        self.label_selected_id_13.setFont(font)
        self.label_selected_id_13.setMouseTracking(True)
        self.label_selected_id_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_13, 7, 1, 1, 1)

        self.lineEdit_valve_mass = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_valve_mass.setObjectName(u"lineEdit_valve_mass")
        self.lineEdit_valve_mass.setEnabled(True)
        self.lineEdit_valve_mass.setMinimumSize(QSize(132, 28))
        self.lineEdit_valve_mass.setMaximumSize(QSize(300, 28))
        self.lineEdit_valve_mass.setSizeIncrement(QSize(0, 26))
        self.lineEdit_valve_mass.setFont(font)
        self.lineEdit_valve_mass.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_valve_mass.setStyleSheet(u"")
        self.lineEdit_valve_mass.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_valve_mass, 7, 2, 1, 1)

        self.lineEdit_stiffening_factor = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_stiffening_factor.setObjectName(u"lineEdit_stiffening_factor")
        self.lineEdit_stiffening_factor.setEnabled(True)
        self.lineEdit_stiffening_factor.setMinimumSize(QSize(132, 28))
        self.lineEdit_stiffening_factor.setMaximumSize(QSize(300, 28))
        self.lineEdit_stiffening_factor.setSizeIncrement(QSize(0, 26))
        self.lineEdit_stiffening_factor.setFont(font)
        self.lineEdit_stiffening_factor.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_stiffening_factor.setStyleSheet(u"")
        self.lineEdit_stiffening_factor.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_stiffening_factor, 6, 2, 1, 1)

        self.label_valve_internal_length = QLabel(self.scrollAreaWidgetContents)
        self.label_valve_internal_length.setObjectName(u"label_valve_internal_length")
        self.label_valve_internal_length.setEnabled(True)
        self.label_valve_internal_length.setMinimumSize(QSize(180, 28))
        self.label_valve_internal_length.setMaximumSize(QSize(220, 28))
        self.label_valve_internal_length.setFont(font1)
        self.label_valve_internal_length.setMouseTracking(True)
        self.label_valve_internal_length.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_valve_internal_length, 10, 1, 1, 1)

        self.label_flange_diameter_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit.setObjectName(u"label_flange_diameter_unit")
        self.label_flange_diameter_unit.setEnabled(True)
        self.label_flange_diameter_unit.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit.setFont(font1)
        self.label_flange_diameter_unit.setMouseTracking(True)
        self.label_flange_diameter_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit, 8, 3, 1, 1)

        self.label_flange_length_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_length_unit.setObjectName(u"label_flange_length_unit")
        self.label_flange_length_unit.setEnabled(True)
        self.label_flange_length_unit.setMinimumSize(QSize(40, 28))
        self.label_flange_length_unit.setMaximumSize(QSize(40, 28))
        self.label_flange_length_unit.setFont(font1)
        self.label_flange_length_unit.setMouseTracking(True)
        self.label_flange_length_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_length_unit, 9, 3, 1, 1)

        self.lineEdit_internal_valve_length = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_internal_valve_length.setObjectName(u"lineEdit_internal_valve_length")
        self.lineEdit_internal_valve_length.setEnabled(True)
        self.lineEdit_internal_valve_length.setMinimumSize(QSize(132, 28))
        self.lineEdit_internal_valve_length.setMaximumSize(QSize(300, 28))
        self.lineEdit_internal_valve_length.setSizeIncrement(QSize(0, 26))
        self.lineEdit_internal_valve_length.setFont(font)
        self.lineEdit_internal_valve_length.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_internal_valve_length.setStyleSheet(u"")
        self.lineEdit_internal_valve_length.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_internal_valve_length, 10, 2, 1, 1)

        self.label_108 = QLabel(self.scrollAreaWidgetContents)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setEnabled(True)
        self.label_108.setMinimumSize(QSize(40, 28))
        self.label_108.setMaximumSize(QSize(40, 28))
        self.label_108.setFont(font)
        self.label_108.setMouseTracking(True)
        self.label_108.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_108, 7, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 6, 0, 1, 1)

        self.label_selected_id_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_12.setObjectName(u"label_selected_id_12")
        self.label_selected_id_12.setEnabled(True)
        self.label_selected_id_12.setMinimumSize(QSize(180, 28))
        self.label_selected_id_12.setMaximumSize(QSize(220, 28))
        self.label_selected_id_12.setFont(font)
        self.label_selected_id_12.setMouseTracking(True)
        self.label_selected_id_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_12, 2, 1, 1, 1)

        self.comboBox_acoustic_behavior = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.setObjectName(u"comboBox_acoustic_behavior")
        self.comboBox_acoustic_behavior.setMinimumSize(QSize(0, 28))
        self.comboBox_acoustic_behavior.setMaximumSize(QSize(16777215, 28))
        self.comboBox_acoustic_behavior.setFont(font)

        self.gridLayout_10.addWidget(self.comboBox_acoustic_behavior, 2, 2, 1, 1)

        self.lineEdit_flange_diameter = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_flange_diameter.setObjectName(u"lineEdit_flange_diameter")
        self.lineEdit_flange_diameter.setEnabled(True)
        self.lineEdit_flange_diameter.setMinimumSize(QSize(132, 28))
        self.lineEdit_flange_diameter.setMaximumSize(QSize(300, 28))
        self.lineEdit_flange_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_diameter.setFont(font)
        self.lineEdit_flange_diameter.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_flange_diameter.setStyleSheet(u"")
        self.lineEdit_flange_diameter.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_flange_diameter, 8, 2, 1, 1)

        self.label_flange_diameter_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_3.setObjectName(u"label_flange_diameter_3")
        self.label_flange_diameter_3.setEnabled(True)
        self.label_flange_diameter_3.setMinimumSize(QSize(180, 28))
        self.label_flange_diameter_3.setMaximumSize(QSize(220, 28))
        self.label_flange_diameter_3.setFont(font1)
        self.label_flange_diameter_3.setMouseTracking(True)
        self.label_flange_diameter_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_3, 5, 1, 1, 1)

        self.label_flange_diameter_unit_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_2.setObjectName(u"label_flange_diameter_unit_2")
        self.label_flange_diameter_unit_2.setEnabled(True)
        self.label_flange_diameter_unit_2.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_2.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit_2.setFont(font1)
        self.label_flange_diameter_unit_2.setMouseTracking(True)
        self.label_flange_diameter_unit_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_2, 4, 3, 1, 1)

        self.lineEdit_wall_thickness = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_wall_thickness.setObjectName(u"lineEdit_wall_thickness")
        self.lineEdit_wall_thickness.setEnabled(True)
        self.lineEdit_wall_thickness.setMinimumSize(QSize(132, 28))
        self.lineEdit_wall_thickness.setMaximumSize(QSize(300, 28))
        self.lineEdit_wall_thickness.setSizeIncrement(QSize(0, 26))
        self.lineEdit_wall_thickness.setFont(font)
        self.lineEdit_wall_thickness.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_wall_thickness.setStyleSheet(u"")
        self.lineEdit_wall_thickness.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_wall_thickness, 5, 2, 1, 1)

        self.lineEdit_effective_diameter = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_effective_diameter.setObjectName(u"lineEdit_effective_diameter")
        self.lineEdit_effective_diameter.setEnabled(True)
        self.lineEdit_effective_diameter.setMinimumSize(QSize(132, 28))
        self.lineEdit_effective_diameter.setMaximumSize(QSize(300, 28))
        self.lineEdit_effective_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_effective_diameter.setFont(font)
        self.lineEdit_effective_diameter.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_effective_diameter.setStyleSheet(u"")
        self.lineEdit_effective_diameter.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_effective_diameter, 4, 2, 1, 1)

        self.label_selected_id_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_10.setObjectName(u"label_selected_id_10")
        self.label_selected_id_10.setEnabled(True)
        self.label_selected_id_10.setMinimumSize(QSize(180, 28))
        self.label_selected_id_10.setMaximumSize(QSize(220, 28))
        self.label_selected_id_10.setFont(font)
        self.label_selected_id_10.setMouseTracking(True)
        self.label_selected_id_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_10, 0, 1, 1, 1)

        self.lineEdit_valve_name = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_valve_name.setObjectName(u"lineEdit_valve_name")
        self.lineEdit_valve_name.setEnabled(True)
        self.lineEdit_valve_name.setMinimumSize(QSize(132, 28))
        self.lineEdit_valve_name.setMaximumSize(QSize(300, 28))
        self.lineEdit_valve_name.setSizeIncrement(QSize(0, 26))
        self.lineEdit_valve_name.setFont(font)
        self.lineEdit_valve_name.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_valve_name.setStyleSheet(u"")
        self.lineEdit_valve_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_valve_name, 0, 2, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_8.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.tab_valve_setup)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_buttons)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)
        self.pushButton_attribute.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_buttons, 5, 0, 1, 2)

        self.tabWidget_main.addTab(self.tab_valve_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_2 = QGridLayout(self.tab_remove)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 4)
        self.treeWidget_valves_info = QTreeWidget(self.tab_remove)
        font2 = QFont()
        font2.setPointSize(9)
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setFont(2, font3)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font2)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_valves_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_valves_info.setObjectName(u"treeWidget_valves_info")
        self.treeWidget_valves_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_valves_info.setMaximumSize(QSize(800, 600))
        self.treeWidget_valves_info.setIndentation(1)
        self.treeWidget_valves_info.setHeaderHidden(False)
        self.treeWidget_valves_info.header().setHighlightSections(False)
        self.treeWidget_valves_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_valves_info.header().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.treeWidget_valves_info, 1, 0, 1, 2)

        self.frame = QFrame(self.tab_remove)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setFlat(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 2)

        self.frame_2 = QFrame(self.tab_remove)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_2)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.checkBox_remove_valve_acoustic_effects = QCheckBox(self.frame_2)
        self.checkBox_remove_valve_acoustic_effects.setObjectName(u"checkBox_remove_valve_acoustic_effects")
        self.checkBox_remove_valve_acoustic_effects.setMinimumSize(QSize(0, 26))
        self.checkBox_remove_valve_acoustic_effects.setMaximumSize(QSize(16777215, 26))
        self.checkBox_remove_valve_acoustic_effects.setFont(font2)
        self.checkBox_remove_valve_acoustic_effects.setIconSize(QSize(16, 16))
        self.checkBox_remove_valve_acoustic_effects.setChecked(True)
        self.checkBox_remove_valve_acoustic_effects.setTristate(False)

        self.gridLayout_11.addWidget(self.checkBox_remove_valve_acoustic_effects, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_10, 0, 2, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 2)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 2, 0, 1, 2)

        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 60))
        self.selection_frame.setMaximumSize(QSize(16777215, 130))
        self.selection_frame.setFrameShape(QFrame.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_30 = QGridLayout(self.selection_frame)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setHorizontalSpacing(6)
        self.gridLayout_30.setVerticalSpacing(4)
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(140, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(140, 28))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setKerning(False)
        self.lineEdit_selected_id.setFont(font4)
        self.lineEdit_selected_id.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)
        self.lineEdit_selected_id.setClearButtonEnabled(True)

        self.gridLayout_30.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(120, 28))
        self.label_selected_id.setMaximumSize(QSize(120, 28))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_selected_id.setFont(font5)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_30.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.selection_frame, 0, 1, 2, 1)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(1600, 48))
        self.top_frame.setFrameShape(QFrame.Box)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.top_frame)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setPointSize(11)
        self.label.setFont(font6)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_id, self.lineEdit_valve_name)
        QWidget.setTabOrder(self.lineEdit_valve_name, self.comboBox_flange_setup)
        QWidget.setTabOrder(self.comboBox_flange_setup, self.comboBox_acoustic_behavior)
        QWidget.setTabOrder(self.comboBox_acoustic_behavior, self.lineEdit_effective_diameter)
        QWidget.setTabOrder(self.lineEdit_effective_diameter, self.lineEdit_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_wall_thickness, self.lineEdit_stiffening_factor)
        QWidget.setTabOrder(self.lineEdit_stiffening_factor, self.lineEdit_valve_mass)
        QWidget.setTabOrder(self.lineEdit_valve_mass, self.lineEdit_flange_diameter)
        QWidget.setTabOrder(self.lineEdit_flange_diameter, self.lineEdit_flange_length)
        QWidget.setTabOrder(self.lineEdit_flange_length, self.lineEdit_internal_valve_length)
        QWidget.setTabOrder(self.lineEdit_internal_valve_length, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.treeWidget_valves_info)
        QWidget.setTabOrder(self.treeWidget_valves_info, self.checkBox_remove_valve_acoustic_effects)
        QWidget.setTabOrder(self.checkBox_remove_valve_acoustic_effects, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.tabWidget_main)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_flange_setup.setCurrentIndex(1)
        self.comboBox_acoustic_behavior.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(True)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Valves configuration", None))
        self.label_selected_id_11.setText(QCoreApplication.translate("Dialog", u"Flange setup:", None))
        self.label_flange_diameter_unit_3.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.comboBox_flange_setup.setItemText(0, QCoreApplication.translate("Dialog", u" Unflanged valve", None))
        self.comboBox_flange_setup.setItemText(1, QCoreApplication.translate("Dialog", u" Flanged valve", None))

        self.label_flange_diameter_2.setText(QCoreApplication.translate("Dialog", u"Effective diameter:", None))
        self.label_flange_length.setText(QCoreApplication.translate("Dialog", u"Flange length:", None))
        self.label_valve_internal_length_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_flange_diameter.setText(QCoreApplication.translate("Dialog", u"Flange diameter:", None))
        self.label_112.setText(QCoreApplication.translate("Dialog", u"[ - ]", None))
        self.label_selected_id_14.setText(QCoreApplication.translate("Dialog", u"Stiffening factor:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_flange_length.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_flange_length.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.label_selected_id_13.setText(QCoreApplication.translate("Dialog", u"Valve mass:", None))
        self.lineEdit_valve_mass.setText(QCoreApplication.translate("Dialog", u"22.5", None))
        self.lineEdit_stiffening_factor.setText(QCoreApplication.translate("Dialog", u"10", None))
        self.label_valve_internal_length.setText(QCoreApplication.translate("Dialog", u"Orifice plate thickness:", None))
        self.label_flange_diameter_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_flange_length_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_internal_valve_length.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_internal_valve_length.setText(QCoreApplication.translate("Dialog", u"0.008", None))
        self.label_108.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.label_selected_id_12.setText(QCoreApplication.translate("Dialog", u"Acoustic behavior:", None))
        self.comboBox_acoustic_behavior.setItemText(0, QCoreApplication.translate("Dialog", u" Valve oppened", None))
        self.comboBox_acoustic_behavior.setItemText(1, QCoreApplication.translate("Dialog", u" Partially closed", None))
        self.comboBox_acoustic_behavior.setItemText(2, QCoreApplication.translate("Dialog", u" Valve closed", None))

        self.lineEdit_flange_diameter.setText(QCoreApplication.translate("Dialog", u"0.320", None))
        self.label_flange_diameter_3.setText(QCoreApplication.translate("Dialog", u"Wall thickness:", None))
        self.label_flange_diameter_unit_2.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.lineEdit_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.010", None))
        self.lineEdit_effective_diameter.setText(QCoreApplication.translate("Dialog", u"0.180", None))
        self.label_selected_id_10.setText(QCoreApplication.translate("Dialog", u"Valve name:", None))
        self.lineEdit_valve_name.setText(QCoreApplication.translate("Dialog", u"valve_test", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_valve_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_valves_info.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Valve parameters", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Lines", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.checkBox_remove_valve_acoustic_effects.setText(QCoreApplication.translate("Dialog", u"Remove the acoustic effects", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Valves configuration", None))
    # retranslateUi



class ValveInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - main_frame: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_valve_setup: QWidget
                                                - (Layout): QGridLayout
                                                        - scrollArea: QScrollArea
                                                            - scrollAreaWidgetContents: QWidget
                                                                - (Layout): QGridLayout
                                                                        - label_selected_id_11: QLabel
                                                                        - label_flange_diameter_unit_3: QLabel
                                                                        - comboBox_flange_setup: QComboBox
                                                                        - label_flange_diameter_2: QLabel
                                                                        - label_flange_length: QLabel
                                                                        - label_valve_internal_length_unit: QLabel
                                                                        - label_flange_diameter: QLabel
                                                                        - label_112: QLabel
                                                                        - label_selected_id_14: QLabel
                                                                        - lineEdit_flange_length: QLineEdit
                                                                        - label_selected_id_13: QLabel
                                                                        - lineEdit_valve_mass: QLineEdit
                                                                        - lineEdit_stiffening_factor: QLineEdit
                                                                        - label_valve_internal_length: QLabel
                                                                        - label_flange_diameter_unit: QLabel
                                                                        - label_flange_length_unit: QLabel
                                                                        - lineEdit_internal_valve_length: QLineEdit
                                                                        - label_108: QLabel
                                                                        - label_selected_id_12: QLabel
                                                                        - comboBox_acoustic_behavior: QComboBox
                                                                        - lineEdit_flange_diameter: QLineEdit
                                                                        - label_flange_diameter_3: QLabel
                                                                        - label_flange_diameter_unit_2: QLabel
                                                                        - lineEdit_wall_thickness: QLineEdit
                                                                        - lineEdit_effective_diameter: QLineEdit
                                                                        - label_selected_id_10: QLabel
                                                                        - lineEdit_valve_name: QLineEdit
                                                        - frame_buttons: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_attribute: QPushButton
                                                                    - pushButton_exit: QPushButton
                                            - tab_remove: QWidget
                                                - (Layout): QGridLayout
                                                        - treeWidget_valves_info: QTreeWidget
                                                        - frame: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                                                        - frame_2: QFrame
                                                            - (Layout): QGridLayout
                                                                    - checkBox_remove_valve_acoustic_effects: QCheckBox
                            - selection_frame: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - label_selected_id: QLabel
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
