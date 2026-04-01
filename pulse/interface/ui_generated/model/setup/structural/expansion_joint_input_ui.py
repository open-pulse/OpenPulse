# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'expansion_joint_input.ui'
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
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 572)
        Dialog.setMinimumSize(QSize(460, 480))
        Dialog.setMaximumSize(QSize(600, 800))
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
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
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
        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 52))
        self.selection_frame.setMaximumSize(QSize(16777215, 52))
        self.selection_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_30 = QGridLayout(self.selection_frame)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setHorizontalSpacing(6)
        self.gridLayout_30.setVerticalSpacing(4)
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(100, 26))
        self.label_selected_id.setMaximumSize(QSize(120, 26))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_30.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(148, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(148, 26))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setKerning(False)
        self.lineEdit_selected_id.setFont(font2)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_30.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.selection_frame, 0, 1, 2, 1)

        self.frame_tabWidgets = QFrame(self.main_frame)
        self.frame_tabWidgets.setObjectName(u"frame_tabWidgets")
        self.frame_tabWidgets.setMinimumSize(QSize(400, 300))
        self.frame_tabWidgets.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_tabWidgets.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_tabWidgets)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 4, 8, 4)
        self.tabWidget_main = QTabWidget(self.frame_tabWidgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(800, 800))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.tabWidget_main.setFont(font3)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_13 = QGridLayout(self.tab_setup)
        self.gridLayout_13.setSpacing(4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.tab_setup)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 418, 358))
        self.gridLayout_8 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_top_inputs = QFrame(self.scrollAreaWidgetContents)
        self.frame_top_inputs.setObjectName(u"frame_top_inputs")
        self.frame_top_inputs.setMinimumSize(QSize(0, 0))
        self.frame_top_inputs.setMaximumSize(QSize(451, 232))
        self.frame_top_inputs.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top_inputs.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_top_inputs)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(8)
        self.gridLayout_11.setVerticalSpacing(6)
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.label_94 = QLabel(self.frame_top_inputs)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setEnabled(True)
        self.label_94.setMinimumSize(QSize(148, 26))
        self.label_94.setMaximumSize(QSize(200, 26))
        self.label_94.setFont(font3)
        self.label_94.setMouseTracking(True)
        self.label_94.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_94, 1, 1, 1, 1)

        self.lineEdit_effective_diameter = QLineEdit(self.frame_top_inputs)
        self.lineEdit_effective_diameter.setObjectName(u"lineEdit_effective_diameter")
        self.lineEdit_effective_diameter.setEnabled(True)
        self.lineEdit_effective_diameter.setMinimumSize(QSize(160, 26))
        self.lineEdit_effective_diameter.setMaximumSize(QSize(160, 26))
        self.lineEdit_effective_diameter.setSizeIncrement(QSize(0, 0))
        self.lineEdit_effective_diameter.setFont(font3)
        self.lineEdit_effective_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_effective_diameter.setStyleSheet(u"")
        self.lineEdit_effective_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_effective_diameter, 1, 2, 1, 1)

        self.label_96 = QLabel(self.frame_top_inputs)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setEnabled(True)
        self.label_96.setMinimumSize(QSize(40, 26))
        self.label_96.setMaximumSize(QSize(200, 26))
        self.label_96.setFont(font3)
        self.label_96.setMouseTracking(True)
        self.label_96.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_96, 1, 3, 1, 1)

        self.lineEdit_joint_mass = QLineEdit(self.frame_top_inputs)
        self.lineEdit_joint_mass.setObjectName(u"lineEdit_joint_mass")
        self.lineEdit_joint_mass.setEnabled(True)
        self.lineEdit_joint_mass.setMinimumSize(QSize(160, 26))
        self.lineEdit_joint_mass.setMaximumSize(QSize(160, 26))
        self.lineEdit_joint_mass.setSizeIncrement(QSize(0, 0))
        self.lineEdit_joint_mass.setFont(font3)
        self.lineEdit_joint_mass.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_joint_mass.setStyleSheet(u"")
        self.lineEdit_joint_mass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_joint_mass, 2, 2, 1, 1)

        self.comboBox_axial_stop_rod = QComboBox(self.frame_top_inputs)
        self.comboBox_axial_stop_rod.addItem("")
        self.comboBox_axial_stop_rod.addItem("")
        self.comboBox_axial_stop_rod.setObjectName(u"comboBox_axial_stop_rod")
        self.comboBox_axial_stop_rod.setMinimumSize(QSize(160, 26))
        self.comboBox_axial_stop_rod.setMaximumSize(QSize(160, 26))
        self.comboBox_axial_stop_rod.setFont(font3)

        self.gridLayout_11.addWidget(self.comboBox_axial_stop_rod, 4, 2, 1, 1)

        self.label_selected_id_10 = QLabel(self.frame_top_inputs)
        self.label_selected_id_10.setObjectName(u"label_selected_id_10")
        self.label_selected_id_10.setEnabled(True)
        self.label_selected_id_10.setMinimumSize(QSize(140, 28))
        self.label_selected_id_10.setMaximumSize(QSize(200, 28))
        self.label_selected_id_10.setFont(font3)
        self.label_selected_id_10.setMouseTracking(True)
        self.label_selected_id_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_selected_id_10, 0, 1, 1, 1)

        self.lineEdit_expansion_joint_name = QLineEdit(self.frame_top_inputs)
        self.lineEdit_expansion_joint_name.setObjectName(u"lineEdit_expansion_joint_name")
        self.lineEdit_expansion_joint_name.setEnabled(True)
        self.lineEdit_expansion_joint_name.setMinimumSize(QSize(160, 28))
        self.lineEdit_expansion_joint_name.setMaximumSize(QSize(160, 28))
        self.lineEdit_expansion_joint_name.setSizeIncrement(QSize(0, 26))
        self.lineEdit_expansion_joint_name.setFont(font3)
        self.lineEdit_expansion_joint_name.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_expansion_joint_name.setStyleSheet(u"")
        self.lineEdit_expansion_joint_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_expansion_joint_name, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_6, 1, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.lineEdit_axial_locking_criteria = QLineEdit(self.frame_top_inputs)
        self.lineEdit_axial_locking_criteria.setObjectName(u"lineEdit_axial_locking_criteria")
        self.lineEdit_axial_locking_criteria.setEnabled(True)
        self.lineEdit_axial_locking_criteria.setMinimumSize(QSize(160, 26))
        self.lineEdit_axial_locking_criteria.setMaximumSize(QSize(160, 26))
        self.lineEdit_axial_locking_criteria.setSizeIncrement(QSize(0, 26))
        self.lineEdit_axial_locking_criteria.setFont(font3)
        self.lineEdit_axial_locking_criteria.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_axial_locking_criteria.setStyleSheet(u"")
        self.lineEdit_axial_locking_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_axial_locking_criteria, 3, 2, 1, 1)

        self.label_axial_lock_criteria = QLabel(self.frame_top_inputs)
        self.label_axial_lock_criteria.setObjectName(u"label_axial_lock_criteria")
        self.label_axial_lock_criteria.setEnabled(True)
        self.label_axial_lock_criteria.setMinimumSize(QSize(148, 26))
        self.label_axial_lock_criteria.setMaximumSize(QSize(200, 26))
        self.label_axial_lock_criteria.setFont(font3)
        self.label_axial_lock_criteria.setMouseTracking(True)
        self.label_axial_lock_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_axial_lock_criteria, 3, 1, 1, 1)

        self.label_95 = QLabel(self.frame_top_inputs)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setEnabled(True)
        self.label_95.setMinimumSize(QSize(148, 26))
        self.label_95.setMaximumSize(QSize(200, 26))
        self.label_95.setFont(font3)
        self.label_95.setMouseTracking(True)
        self.label_95.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_95, 2, 1, 1, 1)

        self.label_101 = QLabel(self.frame_top_inputs)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setEnabled(True)
        self.label_101.setMinimumSize(QSize(148, 26))
        self.label_101.setMaximumSize(QSize(200, 26))
        self.label_101.setFont(font3)
        self.label_101.setMouseTracking(True)
        self.label_101.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_101, 4, 1, 1, 1)

        self.label_97 = QLabel(self.frame_top_inputs)
        self.label_97.setObjectName(u"label_97")
        self.label_97.setEnabled(True)
        self.label_97.setMinimumSize(QSize(40, 26))
        self.label_97.setMaximumSize(QSize(200, 26))
        self.label_97.setFont(font3)
        self.label_97.setMouseTracking(True)
        self.label_97.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_97, 2, 3, 1, 1)


        self.gridLayout_8.addWidget(self.frame_top_inputs, 0, 0, 1, 1)

        self.tabWidget_inputs = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_inputs.setObjectName(u"tabWidget_inputs")
        self.tabWidget_inputs.setMinimumSize(QSize(380, 0))
        self.tabWidget_inputs.setMaximumSize(QSize(600, 200))
        self.tabWidget_inputs.setSizeIncrement(QSize(0, 0))
        self.tabWidget_inputs.setFont(font3)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_9 = QGridLayout(self.tab_constant_values)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 6, 4, 6)
        self.label_14 = QLabel(self.tab_constant_values)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(50, 0))
        self.label_14.setMaximumSize(QSize(120, 16777215))
        self.label_14.setFont(font3)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_14, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_91 = QLabel(self.tab_constant_values)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setEnabled(True)
        self.label_91.setMinimumSize(QSize(40, 26))
        self.label_91.setMaximumSize(QSize(120, 26))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_91.setFont(font4)
        self.label_91.setMouseTracking(True)
        self.label_91.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_91, 2, 1, 1, 1)

        self.label_92 = QLabel(self.tab_constant_values)
        self.label_92.setObjectName(u"label_92")
        self.label_92.setEnabled(True)
        self.label_92.setMinimumSize(QSize(40, 26))
        self.label_92.setMaximumSize(QSize(120, 26))
        self.label_92.setFont(font4)
        self.label_92.setMouseTracking(True)
        self.label_92.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_92, 3, 1, 1, 1)

        self.label_15 = QLabel(self.tab_constant_values)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(50, 0))
        self.label_15.setMaximumSize(QSize(120, 16777215))
        self.label_15.setFont(font3)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_15, 1, 3, 1, 1)

        self.lineEdit_Kryz = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kryz.setObjectName(u"lineEdit_Kryz")
        self.lineEdit_Kryz.setEnabled(True)
        self.lineEdit_Kryz.setMinimumSize(QSize(160, 26))
        self.lineEdit_Kryz.setMaximumSize(QSize(160, 26))
        self.lineEdit_Kryz.setFont(font3)
        self.lineEdit_Kryz.setStyleSheet(u"")
        self.lineEdit_Kryz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_Kryz, 3, 2, 1, 1)

        self.lineEdit_Kx = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kx.setObjectName(u"lineEdit_Kx")
        self.lineEdit_Kx.setEnabled(True)
        self.lineEdit_Kx.setMinimumSize(QSize(160, 26))
        self.lineEdit_Kx.setMaximumSize(QSize(160, 26))
        self.lineEdit_Kx.setFont(font3)
        self.lineEdit_Kx.setStyleSheet(u"")
        self.lineEdit_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_Kx, 0, 2, 1, 1)

        self.label_88 = QLabel(self.tab_constant_values)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setMinimumSize(QSize(50, 0))
        self.label_88.setMaximumSize(QSize(120, 16777215))
        self.label_88.setFont(font3)
        self.label_88.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_88, 2, 3, 1, 1)

        self.lineEdit_Krx = QLineEdit(self.tab_constant_values)
        self.lineEdit_Krx.setObjectName(u"lineEdit_Krx")
        self.lineEdit_Krx.setEnabled(True)
        self.lineEdit_Krx.setMinimumSize(QSize(160, 26))
        self.lineEdit_Krx.setMaximumSize(QSize(160, 26))
        self.lineEdit_Krx.setFont(font3)
        self.lineEdit_Krx.setStyleSheet(u"")
        self.lineEdit_Krx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_Krx, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.lineEdit_Kyz = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kyz.setObjectName(u"lineEdit_Kyz")
        self.lineEdit_Kyz.setEnabled(True)
        self.lineEdit_Kyz.setMinimumSize(QSize(160, 26))
        self.lineEdit_Kyz.setMaximumSize(QSize(160, 26))
        self.lineEdit_Kyz.setFont(font3)
        self.lineEdit_Kyz.setStyleSheet(u"")
        self.lineEdit_Kyz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_Kyz, 1, 2, 1, 1)

        self.label_87 = QLabel(self.tab_constant_values)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setMinimumSize(QSize(50, 0))
        self.label_87.setMaximumSize(QSize(120, 16777215))
        self.label_87.setFont(font3)
        self.label_87.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_87, 3, 3, 1, 1)

        self.label_89 = QLabel(self.tab_constant_values)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setEnabled(True)
        self.label_89.setMinimumSize(QSize(40, 26))
        self.label_89.setMaximumSize(QSize(120, 26))
        self.label_89.setFont(font4)
        self.label_89.setMouseTracking(True)
        self.label_89.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_89, 0, 1, 1, 1)

        self.label_90 = QLabel(self.tab_constant_values)
        self.label_90.setObjectName(u"label_90")
        self.label_90.setEnabled(True)
        self.label_90.setMinimumSize(QSize(40, 26))
        self.label_90.setMaximumSize(QSize(120, 26))
        self.label_90.setFont(font4)
        self.label_90.setMouseTracking(True)
        self.label_90.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_90, 1, 1, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_constant_values, "")
        self.tab_tabular_values = QWidget()
        self.tab_tabular_values.setObjectName(u"tab_tabular_values")
        self.gridLayout_10 = QGridLayout(self.tab_tabular_values)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 6, 4, 6)
        self.pushButton_load_table_Kx = QPushButton(self.tab_tabular_values)
        self.pushButton_load_table_Kx.setObjectName(u"pushButton_load_table_Kx")
        self.pushButton_load_table_Kx.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kx.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kx.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kx.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Kx.setMaximumSize(QSize(4052, 16777215))
        self.pushButton_load_table_Kx.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/new_file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_table_Kx.setIcon(icon)
        self.pushButton_load_table_Kx.setIconSize(QSize(20, 20))

        self.gridLayout_10.addWidget(self.pushButton_load_table_Kx, 0, 3, 1, 1)

        self.lineEdit_Kx_table_path = QLineEdit(self.tab_tabular_values)
        self.lineEdit_Kx_table_path.setObjectName(u"lineEdit_Kx_table_path")
        self.lineEdit_Kx_table_path.setEnabled(True)
        self.lineEdit_Kx_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_Kx_table_path.setMaximumSize(QSize(280, 26))
        self.lineEdit_Kx_table_path.setSizeIncrement(QSize(0, 0))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        self.lineEdit_Kx_table_path.setFont(font5)
        self.lineEdit_Kx_table_path.setStyleSheet(u"")
        self.lineEdit_Kx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kx_table_path.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_Kx_table_path, 0, 2, 1, 1)

        self.lineEdit_Kyz_table_path = QLineEdit(self.tab_tabular_values)
        self.lineEdit_Kyz_table_path.setObjectName(u"lineEdit_Kyz_table_path")
        self.lineEdit_Kyz_table_path.setEnabled(True)
        self.lineEdit_Kyz_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_Kyz_table_path.setMaximumSize(QSize(280, 26))
        self.lineEdit_Kyz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kyz_table_path.setFont(font5)
        self.lineEdit_Kyz_table_path.setStyleSheet(u"")
        self.lineEdit_Kyz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kyz_table_path.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_Kyz_table_path, 1, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.pushButton_load_table_Krx = QPushButton(self.tab_tabular_values)
        self.pushButton_load_table_Krx.setObjectName(u"pushButton_load_table_Krx")
        self.pushButton_load_table_Krx.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Krx.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Krx.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Krx.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Krx.setMaximumSize(QSize(4052, 16777215))
        self.pushButton_load_table_Krx.setStyleSheet(u"")
        self.pushButton_load_table_Krx.setIcon(icon)
        self.pushButton_load_table_Krx.setIconSize(QSize(20, 20))

        self.gridLayout_10.addWidget(self.pushButton_load_table_Krx, 2, 3, 1, 1)

        self.lineEdit_Kryz_table_path = QLineEdit(self.tab_tabular_values)
        self.lineEdit_Kryz_table_path.setObjectName(u"lineEdit_Kryz_table_path")
        self.lineEdit_Kryz_table_path.setEnabled(True)
        self.lineEdit_Kryz_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_Kryz_table_path.setMaximumSize(QSize(280, 26))
        self.lineEdit_Kryz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kryz_table_path.setFont(font5)
        self.lineEdit_Kryz_table_path.setStyleSheet(u"")
        self.lineEdit_Kryz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kryz_table_path.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_Kryz_table_path, 3, 2, 1, 1)

        self.lineEdit_Krx_table_path = QLineEdit(self.tab_tabular_values)
        self.lineEdit_Krx_table_path.setObjectName(u"lineEdit_Krx_table_path")
        self.lineEdit_Krx_table_path.setEnabled(True)
        self.lineEdit_Krx_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_Krx_table_path.setMaximumSize(QSize(280, 26))
        self.lineEdit_Krx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Krx_table_path.setFont(font5)
        self.lineEdit_Krx_table_path.setStyleSheet(u"")
        self.lineEdit_Krx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Krx_table_path.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_Krx_table_path, 2, 2, 1, 1)

        self.pushButton_load_table_Kryz = QPushButton(self.tab_tabular_values)
        self.pushButton_load_table_Kryz.setObjectName(u"pushButton_load_table_Kryz")
        self.pushButton_load_table_Kryz.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kryz.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kryz.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kryz.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Kryz.setMaximumSize(QSize(4052, 16777215))
        self.pushButton_load_table_Kryz.setStyleSheet(u"")
        self.pushButton_load_table_Kryz.setIcon(icon)
        self.pushButton_load_table_Kryz.setIconSize(QSize(20, 20))

        self.gridLayout_10.addWidget(self.pushButton_load_table_Kryz, 3, 3, 1, 1)

        self.label_100 = QLabel(self.tab_tabular_values)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setEnabled(True)
        self.label_100.setMinimumSize(QSize(32, 26))
        self.label_100.setMaximumSize(QSize(32, 26))
        self.label_100.setFont(font4)
        self.label_100.setMouseTracking(True)
        self.label_100.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_100, 0, 1, 1, 1)

        self.pushButton_load_table_Kyz = QPushButton(self.tab_tabular_values)
        self.pushButton_load_table_Kyz.setObjectName(u"pushButton_load_table_Kyz")
        self.pushButton_load_table_Kyz.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kyz.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kyz.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kyz.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Kyz.setMaximumSize(QSize(4052, 16777215))
        self.pushButton_load_table_Kyz.setStyleSheet(u"")
        self.pushButton_load_table_Kyz.setIcon(icon)
        self.pushButton_load_table_Kyz.setIconSize(QSize(20, 20))

        self.gridLayout_10.addWidget(self.pushButton_load_table_Kyz, 1, 3, 1, 1)

        self.label_104 = QLabel(self.tab_tabular_values)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setEnabled(True)
        self.label_104.setMinimumSize(QSize(32, 26))
        self.label_104.setMaximumSize(QSize(32, 26))
        self.label_104.setFont(font4)
        self.label_104.setMouseTracking(True)
        self.label_104.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_104, 1, 1, 1, 1)

        self.label_105 = QLabel(self.tab_tabular_values)
        self.label_105.setObjectName(u"label_105")
        self.label_105.setEnabled(True)
        self.label_105.setMinimumSize(QSize(32, 26))
        self.label_105.setMaximumSize(QSize(32, 26))
        self.label_105.setFont(font4)
        self.label_105.setMouseTracking(True)
        self.label_105.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_105, 2, 1, 1, 1)

        self.label_106 = QLabel(self.tab_tabular_values)
        self.label_106.setObjectName(u"label_106")
        self.label_106.setEnabled(True)
        self.label_106.setMinimumSize(QSize(32, 26))
        self.label_106.setMaximumSize(QSize(32, 26))
        self.label_106.setFont(font4)
        self.label_106.setMouseTracking(True)
        self.label_106.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_106, 3, 1, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_tabular_values, "")

        self.gridLayout_8.addWidget(self.tabWidget_inputs, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_13.addWidget(self.scrollArea, 2, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        font6 = QFont()
        font6.setFamilies([u"MS UI Gothic"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.tab_remove.setFont(font6)
        self.gridLayout_2 = QGridLayout(self.tab_remove)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_expansion_joints_info = QTreeWidget(self.tab_remove)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_expansion_joints_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_expansion_joints_info.setObjectName(u"treeWidget_expansion_joints_info")
        self.treeWidget_expansion_joints_info.setMinimumSize(QSize(320, 200))
        self.treeWidget_expansion_joints_info.setMaximumSize(QSize(460, 200))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(8)
        font7.setBold(False)
        font7.setItalic(False)
        self.treeWidget_expansion_joints_info.setFont(font7)
        self.treeWidget_expansion_joints_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.treeWidget_expansion_joints_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.treeWidget_expansion_joints_info.setIndentation(0)

        self.gridLayout_2.addWidget(self.treeWidget_expansion_joints_info, 1, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_5, 3, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.tab_remove)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 40))
        self.frame_buttons.setMaximumSize(QSize(16777215, 40))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_buttons)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        font8 = QFont()
        font8.setFamilies([u"MS Shell Dlg 2"])
        font8.setPointSize(10)
        font8.setBold(False)
        font8.setItalic(False)
        self.pushButton_reset.setFont(font8)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font8)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_tabWidgets, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        self.frame_confirm = QFrame(Dialog)
        self.frame_confirm.setObjectName(u"frame_confirm")
        self.frame_confirm.setMinimumSize(QSize(0, 48))
        self.frame_confirm.setMaximumSize(QSize(16777215, 48))
        self.frame_confirm.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_confirm.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_confirm)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_confirm)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        font9 = QFont()
        font9.setPointSize(10)
        self.pushButton_attribute.setFont(font9)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)
        self.pushButton_attribute.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_confirm)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font9)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_confirm, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_id, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_expansion_joint_name)
        QWidget.setTabOrder(self.lineEdit_expansion_joint_name, self.lineEdit_effective_diameter)
        QWidget.setTabOrder(self.lineEdit_effective_diameter, self.lineEdit_joint_mass)
        QWidget.setTabOrder(self.lineEdit_joint_mass, self.lineEdit_axial_locking_criteria)
        QWidget.setTabOrder(self.lineEdit_axial_locking_criteria, self.comboBox_axial_stop_rod)
        QWidget.setTabOrder(self.comboBox_axial_stop_rod, self.lineEdit_Kx)
        QWidget.setTabOrder(self.lineEdit_Kx, self.lineEdit_Kyz)
        QWidget.setTabOrder(self.lineEdit_Kyz, self.lineEdit_Krx)
        QWidget.setTabOrder(self.lineEdit_Krx, self.lineEdit_Kryz)
        QWidget.setTabOrder(self.lineEdit_Kryz, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.lineEdit_Kx_table_path)
        QWidget.setTabOrder(self.lineEdit_Kx_table_path, self.pushButton_load_table_Kx)
        QWidget.setTabOrder(self.pushButton_load_table_Kx, self.lineEdit_Kyz_table_path)
        QWidget.setTabOrder(self.lineEdit_Kyz_table_path, self.pushButton_load_table_Kyz)
        QWidget.setTabOrder(self.pushButton_load_table_Kyz, self.lineEdit_Krx_table_path)
        QWidget.setTabOrder(self.lineEdit_Krx_table_path, self.pushButton_load_table_Krx)
        QWidget.setTabOrder(self.pushButton_load_table_Krx, self.lineEdit_Kryz_table_path)
        QWidget.setTabOrder(self.lineEdit_Kryz_table_path, self.pushButton_load_table_Kryz)
        QWidget.setTabOrder(self.pushButton_load_table_Kryz, self.tabWidget_inputs)
        QWidget.setTabOrder(self.tabWidget_inputs, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.treeWidget_expansion_joints_info)
        QWidget.setTabOrder(self.treeWidget_expansion_joints_info, self.scrollArea)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_axial_stop_rod.setCurrentIndex(1)
        self.tabWidget_inputs.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(True)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Expansion joints configuration", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.label_94.setText(QCoreApplication.translate("Dialog", u"Effective diameter:", None))
        self.lineEdit_effective_diameter.setText("")
        self.label_96.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.lineEdit_joint_mass.setText("")
        self.comboBox_axial_stop_rod.setItemText(0, QCoreApplication.translate("Dialog", u" Not included", None))
        self.comboBox_axial_stop_rod.setItemText(1, QCoreApplication.translate("Dialog", u" Included", None))

        self.label_selected_id_10.setText(QCoreApplication.translate("Dialog", u"Expansion joint name:", None))
        self.lineEdit_axial_locking_criteria.setText(QCoreApplication.translate("Dialog", u"1.0", None))
        self.label_axial_lock_criteria.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">Axial locking criteria \u03b5:</span></p></body></html>", None))
        self.label_95.setText(QCoreApplication.translate("Dialog", u"Joint mass:", None))
        self.label_101.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Axial stop rods:</p></body></html>", None))
        self.label_97.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.label_91.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">rx</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_92.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">ryz</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.lineEdit_Kryz.setText("")
        self.lineEdit_Kx.setText("")
        self.label_88.setText(QCoreApplication.translate("Dialog", u"[N.m/rad]", None))
        self.lineEdit_Krx.setText("")
        self.lineEdit_Kyz.setText("")
        self.label_87.setText(QCoreApplication.translate("Dialog", u"[N.m/rad]", None))
        self.label_89.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">x</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_90.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">yz</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_load_table_Kx.setText("")
        self.pushButton_load_table_Krx.setText("")
        self.pushButton_load_table_Kryz.setText("")
        self.label_100.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-size:11pt;\">k</span><span style=\" font-size:11pt; vertical-align:sub;\">x</span><span style=\" font-size:11pt;\">:</span></p></body></html>", None))
        self.pushButton_load_table_Kyz.setText("")
        self.label_104.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-size:11pt;\">k</span><span style=\" font-size:11pt; vertical-align:sub;\">yz</span><span style=\" font-size:11pt;\">:</span></p></body></html>", None))
        self.label_105.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-size:11pt;\">k</span><span style=\" font-size:11pt; vertical-align:sub;\">rx</span><span style=\" font-size:11pt;\">:</span></p></body></html>", None))
        self.label_106.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-size:11pt;\">k</span><span style=\" font-size:11pt; vertical-align:sub;\">ryz</span><span style=\" font-size:11pt;\">:</span></p></body></html>", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_tabular_values), QCoreApplication.translate("Dialog", u"Tabular values", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_expansion_joints_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Joint parameters [L, d_eff, m, \u03b5, rods, kx, kyz, krx, kryz]", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Line ID", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class ExpansionJointInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - main_frame: QFrame
                    - (Layout): QGridLayout
                            - selection_frame: QFrame
                                - (Layout): QGridLayout
                                        - label_selected_id: QLabel
                                        - lineEdit_selected_id: QLineEdit
                            - frame_tabWidgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_setup: QWidget
                                                - (Layout): QGridLayout
                                                        - scrollArea: QScrollArea
                                                            - scrollAreaWidgetContents: QWidget
                                                                - (Layout): QGridLayout
                                                                        - frame_top_inputs: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - label_94: QLabel
                                                                                    - lineEdit_effective_diameter: QLineEdit
                                                                                    - label_96: QLabel
                                                                                    - lineEdit_joint_mass: QLineEdit
                                                                                    - comboBox_axial_stop_rod: QComboBox
                                                                                    - label_selected_id_10: QLabel
                                                                                    - lineEdit_expansion_joint_name: QLineEdit
                                                                                    - lineEdit_axial_locking_criteria: QLineEdit
                                                                                    - label_axial_lock_criteria: QLabel
                                                                                    - label_95: QLabel
                                                                                    - label_101: QLabel
                                                                                    - label_97: QLabel
                                                                        - tabWidget_inputs: QTabWidget
                                                                            - tab_constant_values: QWidget
                                                                                - (Layout): QGridLayout
                                                                                        - label_14: QLabel
                                                                                        - label_91: QLabel
                                                                                        - label_92: QLabel
                                                                                        - label_15: QLabel
                                                                                        - lineEdit_Kryz: QLineEdit
                                                                                        - lineEdit_Kx: QLineEdit
                                                                                        - label_88: QLabel
                                                                                        - lineEdit_Krx: QLineEdit
                                                                                        - lineEdit_Kyz: QLineEdit
                                                                                        - label_87: QLabel
                                                                                        - label_89: QLabel
                                                                                        - label_90: QLabel
                                                                            - tab_tabular_values: QWidget
                                                                                - (Layout): QGridLayout
                                                                                        - pushButton_load_table_Kx: QPushButton
                                                                                        - lineEdit_Kx_table_path: QLineEdit
                                                                                        - lineEdit_Kyz_table_path: QLineEdit
                                                                                        - pushButton_load_table_Krx: QPushButton
                                                                                        - lineEdit_Kryz_table_path: QLineEdit
                                                                                        - lineEdit_Krx_table_path: QLineEdit
                                                                                        - pushButton_load_table_Kryz: QPushButton
                                                                                        - label_100: QLabel
                                                                                        - pushButton_load_table_Kyz: QPushButton
                                                                                        - label_104: QLabel
                                                                                        - label_105: QLabel
                                                                                        - label_106: QLabel
                                            - tab_remove: QWidget
                                                - (Layout): QGridLayout
                                                        - treeWidget_expansion_joints_info: QTreeWidget
                                                        - frame_buttons: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
                - frame_confirm: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
