# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'valve_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 631)
        Dialog.setMinimumSize(QSize(480, 320))
        Dialog.setMaximumSize(QSize(480, 640))
        font = QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(1600, 48))
        self.top_frame.setFrameShape(QFrame.Shape.Box)
        self.top_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.top_frame)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        self.main_frame = QFrame(Dialog)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1600, 1600))
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.main_frame)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.main_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(132, 0))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
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
        self.tabWidget_main.setTabShape(QTabWidget.TabShape.Rounded)
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
        self.scrollArea.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 438, 417))
        self.gridLayout_10 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 8, 4, 2)
        self.label_valve_internal_length_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_valve_internal_length_unit.setObjectName(u"label_valve_internal_length_unit")
        self.label_valve_internal_length_unit.setEnabled(True)
        self.label_valve_internal_length_unit.setMinimumSize(QSize(40, 28))
        self.label_valve_internal_length_unit.setMaximumSize(QSize(40, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_valve_internal_length_unit.setFont(font2)
        self.label_valve_internal_length_unit.setMouseTracking(True)
        self.label_valve_internal_length_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_valve_internal_length_unit, 12, 3, 1, 1)

        self.lineEdit_flange_length = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_flange_length.setObjectName(u"lineEdit_flange_length")
        self.lineEdit_flange_length.setEnabled(True)
        self.lineEdit_flange_length.setMinimumSize(QSize(150, 28))
        self.lineEdit_flange_length.setMaximumSize(QSize(150, 28))
        self.lineEdit_flange_length.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_length.setFont(font)
        self.lineEdit_flange_length.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_flange_length.setStyleSheet(u"")
        self.lineEdit_flange_length.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_flange_length.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_flange_length, 11, 2, 1, 1)

        self.label_112 = QLabel(self.scrollAreaWidgetContents)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(40, 28))
        self.label_112.setMaximumSize(QSize(40, 28))
        self.label_112.setFont(font)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_112, 8, 3, 1, 1)

        self.lineEdit_valve_stiffening_factor = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_valve_stiffening_factor.setObjectName(u"lineEdit_valve_stiffening_factor")
        self.lineEdit_valve_stiffening_factor.setEnabled(True)
        self.lineEdit_valve_stiffening_factor.setMinimumSize(QSize(150, 28))
        self.lineEdit_valve_stiffening_factor.setMaximumSize(QSize(150, 28))
        self.lineEdit_valve_stiffening_factor.setSizeIncrement(QSize(0, 26))
        self.lineEdit_valve_stiffening_factor.setFont(font)
        self.lineEdit_valve_stiffening_factor.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_valve_stiffening_factor.setStyleSheet(u"")
        self.lineEdit_valve_stiffening_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_valve_stiffening_factor.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_valve_stiffening_factor, 8, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 8, 0, 1, 1)

        self.lineEdit_effective_diameter = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_effective_diameter.setObjectName(u"lineEdit_effective_diameter")
        self.lineEdit_effective_diameter.setEnabled(True)
        self.lineEdit_effective_diameter.setMinimumSize(QSize(150, 28))
        self.lineEdit_effective_diameter.setMaximumSize(QSize(150, 28))
        self.lineEdit_effective_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_effective_diameter.setFont(font)
        self.lineEdit_effective_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_effective_diameter.setStyleSheet(u"")
        self.lineEdit_effective_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_effective_diameter.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_effective_diameter, 4, 2, 1, 1)

        self.lineEdit_internal_valve_length = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_internal_valve_length.setObjectName(u"lineEdit_internal_valve_length")
        self.lineEdit_internal_valve_length.setEnabled(True)
        self.lineEdit_internal_valve_length.setMinimumSize(QSize(150, 28))
        self.lineEdit_internal_valve_length.setMaximumSize(QSize(150, 28))
        self.lineEdit_internal_valve_length.setSizeIncrement(QSize(0, 26))
        self.lineEdit_internal_valve_length.setFont(font)
        self.lineEdit_internal_valve_length.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_internal_valve_length.setStyleSheet(u"")
        self.lineEdit_internal_valve_length.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_internal_valve_length.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_internal_valve_length, 12, 2, 1, 1)

        self.pushButton_reset_entries = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_reset_entries.setObjectName(u"pushButton_reset_entries")
        self.pushButton_reset_entries.setMinimumSize(QSize(40, 28))
        self.pushButton_reset_entries.setMaximumSize(QSize(40, 28))
        icon = Icon(u":/icons/common/broom.png")
        self.pushButton_reset_entries.setIcon(icon)
        self.pushButton_reset_entries.setIconSize(QSize(20, 20))
        self.pushButton_reset_entries.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_reset_entries, 0, 3, 1, 1)

        self.label_flange_diameter = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter.setObjectName(u"label_flange_diameter")
        self.label_flange_diameter.setEnabled(True)
        self.label_flange_diameter.setMinimumSize(QSize(170, 28))
        self.label_flange_diameter.setMaximumSize(QSize(170, 28))
        self.label_flange_diameter.setFont(font2)
        self.label_flange_diameter.setMouseTracking(True)
        self.label_flange_diameter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter, 10, 1, 1, 1)

        self.label_108 = QLabel(self.scrollAreaWidgetContents)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setEnabled(True)
        self.label_108.setMinimumSize(QSize(40, 28))
        self.label_108.setMaximumSize(QSize(40, 28))
        self.label_108.setFont(font)
        self.label_108.setMouseTracking(True)
        self.label_108.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_108, 9, 3, 1, 1)

        self.label_flange_diameter_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit.setObjectName(u"label_flange_diameter_unit")
        self.label_flange_diameter_unit.setEnabled(True)
        self.label_flange_diameter_unit.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit.setFont(font2)
        self.label_flange_diameter_unit.setMouseTracking(True)
        self.label_flange_diameter_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit, 10, 3, 1, 1)

        self.label_flange_length = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_length.setObjectName(u"label_flange_length")
        self.label_flange_length.setEnabled(True)
        self.label_flange_length.setMinimumSize(QSize(170, 28))
        self.label_flange_length.setMaximumSize(QSize(170, 28))
        self.label_flange_length.setFont(font2)
        self.label_flange_length.setMouseTracking(True)
        self.label_flange_length.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_length, 11, 1, 1, 1)

        self.label_flange_length_unit = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_length_unit.setObjectName(u"label_flange_length_unit")
        self.label_flange_length_unit.setEnabled(True)
        self.label_flange_length_unit.setMinimumSize(QSize(40, 28))
        self.label_flange_length_unit.setMaximumSize(QSize(40, 28))
        self.label_flange_length_unit.setFont(font2)
        self.label_flange_length_unit.setMouseTracking(True)
        self.label_flange_length_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_length_unit, 11, 3, 1, 1)

        self.label_98 = QLabel(self.scrollAreaWidgetContents)
        self.label_98.setObjectName(u"label_98")
        self.label_98.setEnabled(True)
        self.label_98.setMinimumSize(QSize(170, 28))
        self.label_98.setMaximumSize(QSize(170, 28))
        self.label_98.setFont(font2)
        self.label_98.setMouseTracking(True)
        self.label_98.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_98, 6, 1, 1, 1)

        self.comboBox_flange_setup = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_flange_setup.addItem("")
        self.comboBox_flange_setup.addItem("")
        self.comboBox_flange_setup.setObjectName(u"comboBox_flange_setup")
        self.comboBox_flange_setup.setMinimumSize(QSize(150, 28))
        self.comboBox_flange_setup.setMaximumSize(QSize(150, 28))
        self.comboBox_flange_setup.setFont(font)

        self.gridLayout_10.addWidget(self.comboBox_flange_setup, 1, 2, 1, 1)

        self.label_selected_id_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_10.setObjectName(u"label_selected_id_10")
        self.label_selected_id_10.setEnabled(True)
        self.label_selected_id_10.setMinimumSize(QSize(170, 28))
        self.label_selected_id_10.setMaximumSize(QSize(170, 28))
        self.label_selected_id_10.setFont(font)
        self.label_selected_id_10.setMouseTracking(True)
        self.label_selected_id_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_10, 0, 1, 1, 1)

        self.label_flange_diameter_unit_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_3.setObjectName(u"label_flange_diameter_unit_3")
        self.label_flange_diameter_unit_3.setEnabled(True)
        self.label_flange_diameter_unit_3.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_3.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit_3.setFont(font2)
        self.label_flange_diameter_unit_3.setMouseTracking(True)
        self.label_flange_diameter_unit_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_3, 5, 3, 1, 1)

        self.lineEdit_flange_diameter = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_flange_diameter.setObjectName(u"lineEdit_flange_diameter")
        self.lineEdit_flange_diameter.setEnabled(True)
        self.lineEdit_flange_diameter.setMinimumSize(QSize(150, 28))
        self.lineEdit_flange_diameter.setMaximumSize(QSize(150, 28))
        self.lineEdit_flange_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_diameter.setFont(font)
        self.lineEdit_flange_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_flange_diameter.setStyleSheet(u"")
        self.lineEdit_flange_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_flange_diameter.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_flange_diameter, 10, 2, 1, 1)

        self.label_selected_id_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_13.setObjectName(u"label_selected_id_13")
        self.label_selected_id_13.setEnabled(True)
        self.label_selected_id_13.setMinimumSize(QSize(170, 28))
        self.label_selected_id_13.setMaximumSize(QSize(170, 28))
        self.label_selected_id_13.setFont(font)
        self.label_selected_id_13.setMouseTracking(True)
        self.label_selected_id_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_13, 9, 1, 1, 1)

        self.label_flange_diameter_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_3.setObjectName(u"label_flange_diameter_3")
        self.label_flange_diameter_3.setEnabled(True)
        self.label_flange_diameter_3.setMinimumSize(QSize(170, 28))
        self.label_flange_diameter_3.setMaximumSize(QSize(170, 28))
        self.label_flange_diameter_3.setFont(font2)
        self.label_flange_diameter_3.setMouseTracking(True)
        self.label_flange_diameter_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_3, 5, 1, 1, 1)

        self.label_flange_diameter_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_2.setObjectName(u"label_flange_diameter_2")
        self.label_flange_diameter_2.setEnabled(True)
        self.label_flange_diameter_2.setMinimumSize(QSize(170, 28))
        self.label_flange_diameter_2.setMaximumSize(QSize(170, 28))
        self.label_flange_diameter_2.setFont(font2)
        self.label_flange_diameter_2.setMouseTracking(True)
        self.label_flange_diameter_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_2, 4, 1, 1, 1)

        self.label_selected_id_14 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_14.setObjectName(u"label_selected_id_14")
        self.label_selected_id_14.setEnabled(True)
        self.label_selected_id_14.setMinimumSize(QSize(170, 28))
        self.label_selected_id_14.setMaximumSize(QSize(170, 28))
        self.label_selected_id_14.setFont(font)
        self.label_selected_id_14.setMouseTracking(True)
        self.label_selected_id_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_14, 8, 1, 1, 1)

        self.lineEdit_offset_y = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_offset_y.setObjectName(u"lineEdit_offset_y")
        self.lineEdit_offset_y.setEnabled(True)
        self.lineEdit_offset_y.setMinimumSize(QSize(150, 28))
        self.lineEdit_offset_y.setMaximumSize(QSize(150, 28))
        self.lineEdit_offset_y.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offset_y.setFont(font2)
        self.lineEdit_offset_y.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_y.setStyleSheet(u"")
        self.lineEdit_offset_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_y.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_offset_y, 6, 2, 1, 1)

        self.lineEdit_valve_mass = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_valve_mass.setObjectName(u"lineEdit_valve_mass")
        self.lineEdit_valve_mass.setEnabled(True)
        self.lineEdit_valve_mass.setMinimumSize(QSize(150, 28))
        self.lineEdit_valve_mass.setMaximumSize(QSize(150, 28))
        self.lineEdit_valve_mass.setSizeIncrement(QSize(0, 26))
        self.lineEdit_valve_mass.setFont(font)
        self.lineEdit_valve_mass.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_valve_mass.setStyleSheet(u"")
        self.lineEdit_valve_mass.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_valve_mass.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_valve_mass, 9, 2, 1, 1)

        self.label_selected_id_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_11.setObjectName(u"label_selected_id_11")
        self.label_selected_id_11.setEnabled(True)
        self.label_selected_id_11.setMinimumSize(QSize(170, 28))
        self.label_selected_id_11.setMaximumSize(QSize(170, 28))
        self.label_selected_id_11.setFont(font)
        self.label_selected_id_11.setMouseTracking(True)
        self.label_selected_id_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_11, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_2, 8, 4, 1, 1)

        self.comboBox_acoustic_behavior = QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.addItem("")
        self.comboBox_acoustic_behavior.setObjectName(u"comboBox_acoustic_behavior")
        self.comboBox_acoustic_behavior.setMinimumSize(QSize(150, 28))
        self.comboBox_acoustic_behavior.setMaximumSize(QSize(150, 28))
        self.comboBox_acoustic_behavior.setFont(font)

        self.gridLayout_10.addWidget(self.comboBox_acoustic_behavior, 2, 2, 1, 1)

        self.label_valve_internal_length = QLabel(self.scrollAreaWidgetContents)
        self.label_valve_internal_length.setObjectName(u"label_valve_internal_length")
        self.label_valve_internal_length.setEnabled(True)
        self.label_valve_internal_length.setMinimumSize(QSize(170, 28))
        self.label_valve_internal_length.setMaximumSize(QSize(170, 28))
        self.label_valve_internal_length.setFont(font2)
        self.label_valve_internal_length.setMouseTracking(True)
        self.label_valve_internal_length.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_valve_internal_length, 12, 1, 1, 1)

        self.label_selected_id_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_selected_id_12.setObjectName(u"label_selected_id_12")
        self.label_selected_id_12.setEnabled(True)
        self.label_selected_id_12.setMinimumSize(QSize(170, 28))
        self.label_selected_id_12.setMaximumSize(QSize(170, 28))
        self.label_selected_id_12.setFont(font)
        self.label_selected_id_12.setMouseTracking(True)
        self.label_selected_id_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_selected_id_12, 2, 1, 1, 1)

        self.lineEdit_wall_thickness = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_wall_thickness.setObjectName(u"lineEdit_wall_thickness")
        self.lineEdit_wall_thickness.setEnabled(True)
        self.lineEdit_wall_thickness.setMinimumSize(QSize(150, 28))
        self.lineEdit_wall_thickness.setMaximumSize(QSize(150, 28))
        self.lineEdit_wall_thickness.setSizeIncrement(QSize(0, 26))
        self.lineEdit_wall_thickness.setFont(font)
        self.lineEdit_wall_thickness.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness.setStyleSheet(u"")
        self.lineEdit_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_wall_thickness, 5, 2, 1, 1)

        self.lineEdit_valve_name = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_valve_name.setObjectName(u"lineEdit_valve_name")
        self.lineEdit_valve_name.setEnabled(True)
        self.lineEdit_valve_name.setMinimumSize(QSize(150, 28))
        self.lineEdit_valve_name.setMaximumSize(QSize(150, 28))
        self.lineEdit_valve_name.setSizeIncrement(QSize(0, 26))
        self.lineEdit_valve_name.setFont(font)
        self.lineEdit_valve_name.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_valve_name.setStyleSheet(u"")
        self.lineEdit_valve_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_valve_name.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_valve_name, 0, 2, 1, 1)

        self.label_flange_diameter_unit_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_4.setObjectName(u"label_flange_diameter_unit_4")
        self.label_flange_diameter_unit_4.setEnabled(True)
        self.label_flange_diameter_unit_4.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_4.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit_4.setFont(font2)
        self.label_flange_diameter_unit_4.setMouseTracking(True)
        self.label_flange_diameter_unit_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_4, 6, 3, 1, 1)

        self.label_flange_diameter_unit_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_2.setObjectName(u"label_flange_diameter_unit_2")
        self.label_flange_diameter_unit_2.setEnabled(True)
        self.label_flange_diameter_unit_2.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_2.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit_2.setFont(font2)
        self.label_flange_diameter_unit_2.setMouseTracking(True)
        self.label_flange_diameter_unit_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_2, 4, 3, 1, 1)

        self.label_99 = QLabel(self.scrollAreaWidgetContents)
        self.label_99.setObjectName(u"label_99")
        self.label_99.setEnabled(True)
        self.label_99.setMinimumSize(QSize(170, 28))
        self.label_99.setMaximumSize(QSize(170, 28))
        self.label_99.setFont(font2)
        self.label_99.setMouseTracking(True)
        self.label_99.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_99, 7, 1, 1, 1)

        self.lineEdit_offset_z = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_offset_z.setObjectName(u"lineEdit_offset_z")
        self.lineEdit_offset_z.setEnabled(True)
        self.lineEdit_offset_z.setMinimumSize(QSize(150, 28))
        self.lineEdit_offset_z.setMaximumSize(QSize(150, 28))
        self.lineEdit_offset_z.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offset_z.setFont(font2)
        self.lineEdit_offset_z.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_z.setStyleSheet(u"")
        self.lineEdit_offset_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_z.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_offset_z, 7, 2, 1, 1)

        self.label_flange_diameter_unit_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_flange_diameter_unit_5.setObjectName(u"label_flange_diameter_unit_5")
        self.label_flange_diameter_unit_5.setEnabled(True)
        self.label_flange_diameter_unit_5.setMinimumSize(QSize(40, 28))
        self.label_flange_diameter_unit_5.setMaximumSize(QSize(40, 28))
        self.label_flange_diameter_unit_5.setFont(font2)
        self.label_flange_diameter_unit_5.setMouseTracking(True)
        self.label_flange_diameter_unit_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_flange_diameter_unit_5, 7, 3, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_8.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_valve_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_2 = QGridLayout(self.tab_list)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 4)
        self.treeWidget_valves_info = QTreeWidget(self.tab_list)
        font3 = QFont()
        font3.setPointSize(9)
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setFont(2, font4)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font3)
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

        self.frame = QFrame(self.tab_list)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
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
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 2)

        self.frame_2 = QFrame(self.tab_list)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
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
        self.checkBox_remove_valve_acoustic_effects.setFont(font3)
        self.checkBox_remove_valve_acoustic_effects.setIconSize(QSize(16, 16))
        self.checkBox_remove_valve_acoustic_effects.setChecked(True)
        self.checkBox_remove_valve_acoustic_effects.setTristate(False)

        self.gridLayout_11.addWidget(self.checkBox_remove_valve_acoustic_effects, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_10, 0, 2, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 2)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 2, 0, 1, 2)

        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 52))
        self.selection_frame.setMaximumSize(QSize(16777215, 130))
        self.selection_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_30 = QGridLayout(self.selection_frame)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setHorizontalSpacing(6)
        self.gridLayout_30.setVerticalSpacing(4)
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(140, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(140, 28))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setKerning(False)
        self.lineEdit_selected_id.setFont(font5)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_selected_id.setClearButtonEnabled(True)

        self.gridLayout_30.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(120, 28))
        self.label_selected_id.setMaximumSize(QSize(120, 28))
        font6 = QFont()
        font6.setPointSize(10)
        font6.setBold(False)
        self.label_selected_id.setFont(font6)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_30.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.selection_frame, 0, 1, 2, 1)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
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


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_id, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_valve_name)
        QWidget.setTabOrder(self.lineEdit_valve_name, self.comboBox_flange_setup)
        QWidget.setTabOrder(self.comboBox_flange_setup, self.comboBox_acoustic_behavior)
        QWidget.setTabOrder(self.comboBox_acoustic_behavior, self.lineEdit_effective_diameter)
        QWidget.setTabOrder(self.lineEdit_effective_diameter, self.lineEdit_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_wall_thickness, self.lineEdit_offset_y)
        QWidget.setTabOrder(self.lineEdit_offset_y, self.lineEdit_offset_z)
        QWidget.setTabOrder(self.lineEdit_offset_z, self.lineEdit_valve_stiffening_factor)
        QWidget.setTabOrder(self.lineEdit_valve_stiffening_factor, self.lineEdit_valve_mass)
        QWidget.setTabOrder(self.lineEdit_valve_mass, self.lineEdit_flange_diameter)
        QWidget.setTabOrder(self.lineEdit_flange_diameter, self.lineEdit_flange_length)
        QWidget.setTabOrder(self.lineEdit_flange_length, self.lineEdit_internal_valve_length)
        QWidget.setTabOrder(self.lineEdit_internal_valve_length, self.checkBox_remove_valve_acoustic_effects)
        QWidget.setTabOrder(self.checkBox_remove_valve_acoustic_effects, self.treeWidget_valves_info)
        QWidget.setTabOrder(self.treeWidget_valves_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_reset_entries)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_flange_setup.setCurrentIndex(1)
        self.comboBox_acoustic_behavior.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Valves configuration", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Valves configuration", None))
        self.label_valve_internal_length_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_flange_length.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_flange_length.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.label_112.setText(QCoreApplication.translate("Dialog", u"[ - ]", None))
        self.lineEdit_valve_stiffening_factor.setText(QCoreApplication.translate("Dialog", u"10", None))
        self.lineEdit_effective_diameter.setText(QCoreApplication.translate("Dialog", u"0.180", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_internal_valve_length.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.lineEdit_internal_valve_length.setText(QCoreApplication.translate("Dialog", u"0.008", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Reset entries</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_entries.setText("")
        self.label_flange_diameter.setText(QCoreApplication.translate("Dialog", u"Flange diameter:", None))
        self.label_108.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.label_flange_diameter_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_flange_length.setText(QCoreApplication.translate("Dialog", u"Flange length:", None))
        self.label_flange_length_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_98.setText(QCoreApplication.translate("Dialog", u"Offset y:", None))
        self.comboBox_flange_setup.setItemText(0, QCoreApplication.translate("Dialog", u"Unflanged valve", None))
        self.comboBox_flange_setup.setItemText(1, QCoreApplication.translate("Dialog", u"Flanged valve", None))

        self.label_selected_id_10.setText(QCoreApplication.translate("Dialog", u"Valve name:", None))
        self.label_flange_diameter_unit_3.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.lineEdit_flange_diameter.setText(QCoreApplication.translate("Dialog", u"0.320", None))
        self.label_selected_id_13.setText(QCoreApplication.translate("Dialog", u"Valve mass:", None))
        self.label_flange_diameter_3.setText(QCoreApplication.translate("Dialog", u"Wall thickness:", None))
        self.label_flange_diameter_2.setText(QCoreApplication.translate("Dialog", u"Effective diameter:", None))
        self.label_selected_id_14.setText(QCoreApplication.translate("Dialog", u"Stiffening factor:", None))
        self.lineEdit_offset_y.setText("")
        self.lineEdit_valve_mass.setText(QCoreApplication.translate("Dialog", u"22.5", None))
        self.label_selected_id_11.setText(QCoreApplication.translate("Dialog", u"Flange setup:", None))
        self.comboBox_acoustic_behavior.setItemText(0, QCoreApplication.translate("Dialog", u"Valve open", None))
        self.comboBox_acoustic_behavior.setItemText(1, QCoreApplication.translate("Dialog", u"Partially closed", None))
        self.comboBox_acoustic_behavior.setItemText(2, QCoreApplication.translate("Dialog", u"Valve closed", None))

        self.label_valve_internal_length.setText(QCoreApplication.translate("Dialog", u"Orifice plate thickness:", None))
        self.label_selected_id_12.setText(QCoreApplication.translate("Dialog", u"Acoustic behavior:", None))
        self.lineEdit_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.010", None))
        self.lineEdit_valve_name.setText(QCoreApplication.translate("Dialog", u"valve_test", None))
        self.label_flange_diameter_unit_4.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_flange_diameter_unit_2.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_99.setText(QCoreApplication.translate("Dialog", u"Offset z:", None))
        self.lineEdit_offset_z.setText("")
        self.label_flange_diameter_unit_5.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_valve_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_valves_info.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Valve parameters", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Lines", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Name", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.checkBox_remove_valve_acoustic_effects.setText(QCoreApplication.translate("Dialog", u"Remove the acoustic effects", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class ValveInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
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
                                                                        - label_valve_internal_length_unit: QLabel
                                                                        - lineEdit_flange_length: QLineEdit
                                                                        - label_112: QLabel
                                                                        - lineEdit_valve_stiffening_factor: QLineEdit
                                                                        - lineEdit_effective_diameter: QLineEdit
                                                                        - lineEdit_internal_valve_length: QLineEdit
                                                                        - pushButton_reset_entries: QPushButton
                                                                        - label_flange_diameter: QLabel
                                                                        - label_108: QLabel
                                                                        - label_flange_diameter_unit: QLabel
                                                                        - label_flange_length: QLabel
                                                                        - label_flange_length_unit: QLabel
                                                                        - label_98: QLabel
                                                                        - comboBox_flange_setup: QComboBox
                                                                        - label_selected_id_10: QLabel
                                                                        - label_flange_diameter_unit_3: QLabel
                                                                        - lineEdit_flange_diameter: QLineEdit
                                                                        - label_selected_id_13: QLabel
                                                                        - label_flange_diameter_3: QLabel
                                                                        - label_flange_diameter_2: QLabel
                                                                        - label_selected_id_14: QLabel
                                                                        - lineEdit_offset_y: QLineEdit
                                                                        - lineEdit_valve_mass: QLineEdit
                                                                        - label_selected_id_11: QLabel
                                                                        - comboBox_acoustic_behavior: QComboBox
                                                                        - label_valve_internal_length: QLabel
                                                                        - label_selected_id_12: QLabel
                                                                        - lineEdit_wall_thickness: QLineEdit
                                                                        - lineEdit_valve_name: QLineEdit
                                                                        - label_flange_diameter_unit_4: QLabel
                                                                        - label_flange_diameter_unit_2: QLabel
                                                                        - label_99: QLabel
                                                                        - lineEdit_offset_z: QLineEdit
                                                                        - label_flange_diameter_unit_5: QLabel
                                            - tab_list: QWidget
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
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
