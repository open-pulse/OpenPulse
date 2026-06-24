# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mass_spring_damper_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(440, 500)
        Dialog.setMinimumSize(QSize(440, 500))
        Dialog.setMaximumSize(QSize(440, 500))
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
        self.gridLayout_22 = QGridLayout(self.top_frame)
        self.gridLayout_22.setSpacing(0)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_22.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        self.main_frame = QFrame(Dialog)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1600, 1600))
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.main_frame)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 48))
        self.selection_frame.setMaximumSize(QSize(16777215, 140))
        self.selection_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_31 = QGridLayout(self.selection_frame)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setHorizontalSpacing(6)
        self.gridLayout_31.setVerticalSpacing(4)
        self.gridLayout_31.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)

        self.label_first_node_id = QLabel(self.selection_frame)
        self.label_first_node_id.setObjectName(u"label_first_node_id")
        self.label_first_node_id.setMinimumSize(QSize(120, 26))
        self.label_first_node_id.setMaximumSize(QSize(0, 26))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_first_node_id.setFont(font2)
        self.label_first_node_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_31.addWidget(self.label_first_node_id, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)

        self.lineEdit_node_ids = QLineEdit(self.selection_frame)
        self.lineEdit_node_ids.setObjectName(u"lineEdit_node_ids")
        self.lineEdit_node_ids.setMinimumSize(QSize(160, 26))
        self.lineEdit_node_ids.setMaximumSize(QSize(160, 26))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setKerning(False)
        self.lineEdit_node_ids.setFont(font3)
        self.lineEdit_node_ids.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_node_ids.setStyleSheet(u"")
        self.lineEdit_node_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_31.addWidget(self.lineEdit_node_ids, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.selection_frame, 0, 1, 2, 1)

        self.frame_tabWidgets = QFrame(self.main_frame)
        self.frame_tabWidgets.setObjectName(u"frame_tabWidgets")
        self.frame_tabWidgets.setMinimumSize(QSize(400, 300))
        self.frame_tabWidgets.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_tabWidgets.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_tabWidgets)
        self.gridLayout_14.setSpacing(4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(8, 4, 8, 4)
        self.tabWidget_main = QTabWidget(self.frame_tabWidgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(482, 700))
        self.tabWidget_main.setFont(font)
        self.tab_constant = QWidget()
        self.tab_constant.setObjectName(u"tab_constant")
        self.gridLayout_15 = QGridLayout(self.tab_constant)
        self.gridLayout_15.setSpacing(6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(6, 6, 6, 6)
        self.tabWidget_constant_values = QTabWidget(self.tab_constant)
        self.tabWidget_constant_values.setObjectName(u"tabWidget_constant_values")
        self.tabWidget_constant_values.setFont(font)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_2 = QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_141 = QLabel(self.tab_2)
        self.label_141.setObjectName(u"label_141")
        self.label_141.setEnabled(True)
        self.label_141.setMinimumSize(QSize(70, 26))
        self.label_141.setMaximumSize(QSize(70, 26))
        self.label_141.setFont(font)
        self.label_141.setMouseTracking(True)
        self.label_141.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_141, 5, 1, 1, 1)

        self.lineEdit_Jz = QLineEdit(self.tab_2)
        self.lineEdit_Jz.setObjectName(u"lineEdit_Jz")
        self.lineEdit_Jz.setEnabled(True)
        self.lineEdit_Jz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Jz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Jz.setFont(font)
        self.lineEdit_Jz.setStyleSheet(u"")
        self.lineEdit_Jz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_Jz, 5, 2, 1, 1)

        self.label_140 = QLabel(self.tab_2)
        self.label_140.setObjectName(u"label_140")
        self.label_140.setEnabled(True)
        self.label_140.setMinimumSize(QSize(70, 26))
        self.label_140.setMaximumSize(QSize(70, 26))
        self.label_140.setFont(font)
        self.label_140.setMouseTracking(True)
        self.label_140.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_140, 2, 1, 1, 1)

        self.lineEdit_Mz = QLineEdit(self.tab_2)
        self.lineEdit_Mz.setObjectName(u"lineEdit_Mz")
        self.lineEdit_Mz.setEnabled(True)
        self.lineEdit_Mz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Mz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Mz.setFont(font)
        self.lineEdit_Mz.setStyleSheet(u"")
        self.lineEdit_Mz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_Mz, 2, 2, 1, 1)

        self.lineEdit_Mx = QLineEdit(self.tab_2)
        self.lineEdit_Mx.setObjectName(u"lineEdit_Mx")
        self.lineEdit_Mx.setEnabled(True)
        self.lineEdit_Mx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Mx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Mx.setFont(font)
        self.lineEdit_Mx.setStyleSheet(u"")
        self.lineEdit_Mx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_Mx, 0, 2, 1, 1)

        self.label_147 = QLabel(self.tab_2)
        self.label_147.setObjectName(u"label_147")
        self.label_147.setMinimumSize(QSize(80, 26))
        self.label_147.setMaximumSize(QSize(80, 26))
        self.label_147.setFont(font)
        self.label_147.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_147, 3, 3, 1, 1)

        self.label_142 = QLabel(self.tab_2)
        self.label_142.setObjectName(u"label_142")
        self.label_142.setEnabled(True)
        self.label_142.setMinimumSize(QSize(70, 26))
        self.label_142.setMaximumSize(QSize(70, 26))
        self.label_142.setFont(font)
        self.label_142.setMouseTracking(True)
        self.label_142.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_142, 1, 1, 1, 1)

        self.lineEdit_Jy = QLineEdit(self.tab_2)
        self.lineEdit_Jy.setObjectName(u"lineEdit_Jy")
        self.lineEdit_Jy.setEnabled(True)
        self.lineEdit_Jy.setMinimumSize(QSize(120, 26))
        self.lineEdit_Jy.setMaximumSize(QSize(120, 26))
        self.lineEdit_Jy.setFont(font)
        self.lineEdit_Jy.setStyleSheet(u"")
        self.lineEdit_Jy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_Jy, 4, 2, 1, 1)

        self.label_23 = QLabel(self.tab_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 26))
        self.label_23.setMaximumSize(QSize(80, 26))
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_23, 0, 3, 1, 1)

        self.lineEdit_My = QLineEdit(self.tab_2)
        self.lineEdit_My.setObjectName(u"lineEdit_My")
        self.lineEdit_My.setEnabled(True)
        self.lineEdit_My.setMinimumSize(QSize(120, 26))
        self.lineEdit_My.setMaximumSize(QSize(120, 26))
        self.lineEdit_My.setFont(font)
        self.lineEdit_My.setStyleSheet(u"")
        self.lineEdit_My.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_My, 1, 2, 1, 1)

        self.label_144 = QLabel(self.tab_2)
        self.label_144.setObjectName(u"label_144")
        self.label_144.setEnabled(True)
        self.label_144.setMinimumSize(QSize(70, 26))
        self.label_144.setMaximumSize(QSize(70, 26))
        self.label_144.setFont(font)
        self.label_144.setMouseTracking(True)
        self.label_144.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_144, 4, 1, 1, 1)

        self.lineEdit_Jx = QLineEdit(self.tab_2)
        self.lineEdit_Jx.setObjectName(u"lineEdit_Jx")
        self.lineEdit_Jx.setEnabled(True)
        self.lineEdit_Jx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Jx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Jx.setFont(font)
        self.lineEdit_Jx.setStyleSheet(u"")
        self.lineEdit_Jx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_Jx, 3, 2, 1, 1)

        self.label_94 = QLabel(self.tab_2)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setEnabled(True)
        self.label_94.setMinimumSize(QSize(70, 26))
        self.label_94.setMaximumSize(QSize(70, 26))
        self.label_94.setFont(font)
        self.label_94.setMouseTracking(True)
        self.label_94.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_94, 3, 1, 1, 1)

        self.label_145 = QLabel(self.tab_2)
        self.label_145.setObjectName(u"label_145")
        self.label_145.setEnabled(True)
        self.label_145.setMinimumSize(QSize(70, 26))
        self.label_145.setMaximumSize(QSize(70, 26))
        self.label_145.setFont(font)
        self.label_145.setMouseTracking(True)
        self.label_145.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_145, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.label_24 = QLabel(self.tab_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(80, 26))
        self.label_24.setMaximumSize(QSize(80, 26))
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_24, 1, 3, 1, 1)

        self.label_25 = QLabel(self.tab_2)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(80, 26))
        self.label_25.setMaximumSize(QSize(80, 26))
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_25, 2, 3, 1, 1)

        self.label_148 = QLabel(self.tab_2)
        self.label_148.setObjectName(u"label_148")
        self.label_148.setMinimumSize(QSize(80, 26))
        self.label_148.setMaximumSize(QSize(80, 26))
        self.label_148.setFont(font)
        self.label_148.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_148, 4, 3, 1, 1)

        self.label_149 = QLabel(self.tab_2)
        self.label_149.setObjectName(u"label_149")
        self.label_149.setMinimumSize(QSize(80, 26))
        self.label_149.setMaximumSize(QSize(80, 26))
        self.label_149.setFont(font)
        self.label_149.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_149, 5, 3, 1, 1)

        self.tabWidget_constant_values.addTab(self.tab_2, "")
        self.tab_stiffness = QWidget()
        self.tab_stiffness.setObjectName(u"tab_stiffness")
        self.gridLayout_23 = QGridLayout(self.tab_stiffness)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.lineEdit_Krx = QLineEdit(self.tab_stiffness)
        self.lineEdit_Krx.setObjectName(u"lineEdit_Krx")
        self.lineEdit_Krx.setEnabled(True)
        self.lineEdit_Krx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Krx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Krx.setFont(font)
        self.lineEdit_Krx.setStyleSheet(u"")
        self.lineEdit_Krx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Krx, 3, 2, 1, 1)

        self.label_16 = QLabel(self.tab_stiffness)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(80, 26))
        self.label_16.setMaximumSize(QSize(80, 26))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_16, 0, 3, 1, 1)

        self.lineEdit_Ky = QLineEdit(self.tab_stiffness)
        self.lineEdit_Ky.setObjectName(u"lineEdit_Ky")
        self.lineEdit_Ky.setEnabled(True)
        self.lineEdit_Ky.setMinimumSize(QSize(120, 26))
        self.lineEdit_Ky.setMaximumSize(QSize(120, 26))
        self.lineEdit_Ky.setFont(font)
        self.lineEdit_Ky.setStyleSheet(u"")
        self.lineEdit_Ky.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Ky, 1, 2, 1, 1)

        self.label_115 = QLabel(self.tab_stiffness)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setEnabled(True)
        self.label_115.setMinimumSize(QSize(70, 26))
        self.label_115.setMaximumSize(QSize(70, 26))
        self.label_115.setFont(font)
        self.label_115.setMouseTracking(True)
        self.label_115.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_115, 0, 1, 1, 1)

        self.label_93 = QLabel(self.tab_stiffness)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setEnabled(True)
        self.label_93.setMinimumSize(QSize(70, 26))
        self.label_93.setMaximumSize(QSize(70, 26))
        self.label_93.setFont(font)
        self.label_93.setMouseTracking(True)
        self.label_93.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_93, 3, 1, 1, 1)

        self.label_113 = QLabel(self.tab_stiffness)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setMinimumSize(QSize(80, 26))
        self.label_113.setMaximumSize(QSize(80, 26))
        self.label_113.setFont(font)
        self.label_113.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_113, 3, 3, 1, 1)

        self.label_116 = QLabel(self.tab_stiffness)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setEnabled(True)
        self.label_116.setMinimumSize(QSize(70, 26))
        self.label_116.setMaximumSize(QSize(70, 26))
        self.label_116.setFont(font)
        self.label_116.setMouseTracking(True)
        self.label_116.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_116, 1, 1, 1, 1)

        self.label_123 = QLabel(self.tab_stiffness)
        self.label_123.setObjectName(u"label_123")
        self.label_123.setEnabled(True)
        self.label_123.setMinimumSize(QSize(70, 26))
        self.label_123.setMaximumSize(QSize(70, 26))
        self.label_123.setFont(font)
        self.label_123.setMouseTracking(True)
        self.label_123.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_123, 2, 1, 1, 1)

        self.lineEdit_Kz = QLineEdit(self.tab_stiffness)
        self.lineEdit_Kz.setObjectName(u"lineEdit_Kz")
        self.lineEdit_Kz.setEnabled(True)
        self.lineEdit_Kz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kz.setFont(font)
        self.lineEdit_Kz.setStyleSheet(u"")
        self.lineEdit_Kz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kz, 2, 2, 1, 1)

        self.label_18 = QLabel(self.tab_stiffness)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(80, 26))
        self.label_18.setMaximumSize(QSize(80, 26))
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_18, 2, 3, 1, 1)

        self.label_112 = QLabel(self.tab_stiffness)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(70, 26))
        self.label_112.setMaximumSize(QSize(70, 26))
        self.label_112.setFont(font)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_112, 4, 1, 1, 1)

        self.label_114 = QLabel(self.tab_stiffness)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setMinimumSize(QSize(80, 26))
        self.label_114.setMaximumSize(QSize(80, 26))
        self.label_114.setFont(font)
        self.label_114.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_114, 4, 3, 1, 1)

        self.lineEdit_Krz = QLineEdit(self.tab_stiffness)
        self.lineEdit_Krz.setObjectName(u"lineEdit_Krz")
        self.lineEdit_Krz.setEnabled(True)
        self.lineEdit_Krz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Krz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Krz.setFont(font)
        self.lineEdit_Krz.setStyleSheet(u"")
        self.lineEdit_Krz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Krz, 5, 2, 1, 1)

        self.label_122 = QLabel(self.tab_stiffness)
        self.label_122.setObjectName(u"label_122")
        self.label_122.setMinimumSize(QSize(80, 26))
        self.label_122.setMaximumSize(QSize(80, 26))
        self.label_122.setFont(font)
        self.label_122.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_122, 5, 3, 1, 1)

        self.label_17 = QLabel(self.tab_stiffness)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(80, 26))
        self.label_17.setMaximumSize(QSize(80, 26))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_17, 1, 3, 1, 1)

        self.lineEdit_Kx = QLineEdit(self.tab_stiffness)
        self.lineEdit_Kx.setObjectName(u"lineEdit_Kx")
        self.lineEdit_Kx.setEnabled(True)
        self.lineEdit_Kx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kx.setFont(font)
        self.lineEdit_Kx.setStyleSheet(u"")
        self.lineEdit_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kx, 0, 2, 1, 1)

        self.lineEdit_Kry = QLineEdit(self.tab_stiffness)
        self.lineEdit_Kry.setObjectName(u"lineEdit_Kry")
        self.lineEdit_Kry.setEnabled(True)
        self.lineEdit_Kry.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kry.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kry.setFont(font)
        self.lineEdit_Kry.setStyleSheet(u"")
        self.lineEdit_Kry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kry, 4, 2, 1, 1)

        self.label_121 = QLabel(self.tab_stiffness)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setEnabled(True)
        self.label_121.setMinimumSize(QSize(70, 26))
        self.label_121.setMaximumSize(QSize(70, 26))
        self.label_121.setFont(font)
        self.label_121.setMouseTracking(True)
        self.label_121.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.label_121, 5, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_14, 0, 4, 1, 1)

        self.tabWidget_constant_values.addTab(self.tab_stiffness, "")
        self.tab_damping = QWidget()
        self.tab_damping.setObjectName(u"tab_damping")
        self.gridLayout_24 = QGridLayout(self.tab_damping)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_17, 0, 0, 1, 1)

        self.lineEdit_Crz = QLineEdit(self.tab_damping)
        self.lineEdit_Crz.setObjectName(u"lineEdit_Crz")
        self.lineEdit_Crz.setEnabled(True)
        self.lineEdit_Crz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Crz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Crz.setFont(font)
        self.lineEdit_Crz.setStyleSheet(u"")
        self.lineEdit_Crz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Crz, 5, 2, 1, 1)

        self.label_131 = QLabel(self.tab_damping)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setMinimumSize(QSize(80, 26))
        self.label_131.setMaximumSize(QSize(80, 26))
        self.label_131.setFont(font)
        self.label_131.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_131, 5, 3, 1, 1)

        self.label_126 = QLabel(self.tab_damping)
        self.label_126.setObjectName(u"label_126")
        self.label_126.setEnabled(True)
        self.label_126.setMinimumSize(QSize(70, 26))
        self.label_126.setMaximumSize(QSize(70, 26))
        self.label_126.setFont(font)
        self.label_126.setMouseTracking(True)
        self.label_126.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_126, 5, 1, 1, 1)

        self.label_128 = QLabel(self.tab_damping)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setEnabled(True)
        self.label_128.setMinimumSize(QSize(70, 26))
        self.label_128.setMaximumSize(QSize(70, 26))
        self.label_128.setFont(font)
        self.label_128.setMouseTracking(True)
        self.label_128.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_128, 1, 1, 1, 1)

        self.lineEdit_Cy = QLineEdit(self.tab_damping)
        self.lineEdit_Cy.setObjectName(u"lineEdit_Cy")
        self.lineEdit_Cy.setEnabled(True)
        self.lineEdit_Cy.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cy.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cy.setFont(font)
        self.lineEdit_Cy.setStyleSheet(u"")
        self.lineEdit_Cy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cy, 1, 2, 1, 1)

        self.lineEdit_Cz = QLineEdit(self.tab_damping)
        self.lineEdit_Cz.setObjectName(u"lineEdit_Cz")
        self.lineEdit_Cz.setEnabled(True)
        self.lineEdit_Cz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cz.setFont(font)
        self.lineEdit_Cz.setStyleSheet(u"")
        self.lineEdit_Cz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cz, 2, 2, 1, 1)

        self.label_102 = QLabel(self.tab_damping)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setEnabled(True)
        self.label_102.setMinimumSize(QSize(70, 26))
        self.label_102.setMaximumSize(QSize(70, 26))
        self.label_102.setFont(font)
        self.label_102.setMouseTracking(True)
        self.label_102.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_102, 3, 1, 1, 1)

        self.label_19 = QLabel(self.tab_damping)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(80, 26))
        self.label_19.setMaximumSize(QSize(80, 26))
        self.label_19.setFont(font)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_19, 2, 3, 1, 1)

        self.label_21 = QLabel(self.tab_damping)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 26))
        self.label_21.setMaximumSize(QSize(80, 26))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_21, 1, 3, 1, 1)

        self.lineEdit_Crx = QLineEdit(self.tab_damping)
        self.lineEdit_Crx.setObjectName(u"lineEdit_Crx")
        self.lineEdit_Crx.setEnabled(True)
        self.lineEdit_Crx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Crx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Crx.setFont(font)
        self.lineEdit_Crx.setStyleSheet(u"")
        self.lineEdit_Crx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Crx, 3, 2, 1, 1)

        self.label_127 = QLabel(self.tab_damping)
        self.label_127.setObjectName(u"label_127")
        self.label_127.setEnabled(True)
        self.label_127.setMinimumSize(QSize(70, 26))
        self.label_127.setMaximumSize(QSize(70, 26))
        self.label_127.setFont(font)
        self.label_127.setMouseTracking(True)
        self.label_127.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_127, 2, 1, 1, 1)

        self.label_125 = QLabel(self.tab_damping)
        self.label_125.setObjectName(u"label_125")
        self.label_125.setEnabled(True)
        self.label_125.setMinimumSize(QSize(70, 26))
        self.label_125.setMaximumSize(QSize(70, 26))
        self.label_125.setFont(font)
        self.label_125.setMouseTracking(True)
        self.label_125.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_125, 4, 1, 1, 1)

        self.label_130 = QLabel(self.tab_damping)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setMinimumSize(QSize(80, 26))
        self.label_130.setMaximumSize(QSize(80, 26))
        self.label_130.setFont(font)
        self.label_130.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_130, 3, 3, 1, 1)

        self.label_124 = QLabel(self.tab_damping)
        self.label_124.setObjectName(u"label_124")
        self.label_124.setMinimumSize(QSize(80, 26))
        self.label_124.setMaximumSize(QSize(80, 26))
        self.label_124.setFont(font)
        self.label_124.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_124, 4, 3, 1, 1)

        self.lineEdit_Cry = QLineEdit(self.tab_damping)
        self.lineEdit_Cry.setObjectName(u"lineEdit_Cry")
        self.lineEdit_Cry.setEnabled(True)
        self.lineEdit_Cry.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cry.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cry.setFont(font)
        self.lineEdit_Cry.setStyleSheet(u"")
        self.lineEdit_Cry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cry, 4, 2, 1, 1)

        self.label_129 = QLabel(self.tab_damping)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setEnabled(True)
        self.label_129.setMinimumSize(QSize(70, 26))
        self.label_129.setMaximumSize(QSize(70, 26))
        self.label_129.setFont(font)
        self.label_129.setMouseTracking(True)
        self.label_129.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.label_129, 0, 1, 1, 1)

        self.lineEdit_Cx = QLineEdit(self.tab_damping)
        self.lineEdit_Cx.setObjectName(u"lineEdit_Cx")
        self.lineEdit_Cx.setEnabled(True)
        self.lineEdit_Cx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cx.setFont(font)
        self.lineEdit_Cx.setStyleSheet(u"")
        self.lineEdit_Cx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cx, 0, 2, 1, 1)

        self.label_20 = QLabel(self.tab_damping)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_20, 0, 3, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.tabWidget_constant_values.addTab(self.tab_damping, "")

        self.gridLayout_15.addWidget(self.tabWidget_constant_values, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant, "")
        self.tab_tabular = QWidget()
        self.tab_tabular.setObjectName(u"tab_tabular")
        self.gridLayout_10 = QGridLayout(self.tab_tabular)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.tabWidget_table_values = QTabWidget(self.tab_tabular)
        self.tabWidget_table_values.setObjectName(u"tabWidget_table_values")
        self.tabWidget_table_values.setFont(font)
        self.tab_mass_table = QWidget()
        self.tab_mass_table.setObjectName(u"tab_mass_table")
        self.gridLayout_9 = QGridLayout(self.tab_mass_table)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.label_143 = QLabel(self.tab_mass_table)
        self.label_143.setObjectName(u"label_143")
        self.label_143.setEnabled(True)
        self.label_143.setMinimumSize(QSize(30, 26))
        self.label_143.setMaximumSize(QSize(30, 26))
        self.label_143.setFont(font)
        self.label_143.setMouseTracking(True)
        self.label_143.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_143, 5, 1, 1, 1)

        self.label_152 = QLabel(self.tab_mass_table)
        self.label_152.setObjectName(u"label_152")
        self.label_152.setEnabled(True)
        self.label_152.setMinimumSize(QSize(30, 26))
        self.label_152.setMaximumSize(QSize(30, 26))
        self.label_152.setFont(font)
        self.label_152.setMouseTracking(True)
        self.label_152.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_152, 4, 1, 1, 1)

        self.label_153 = QLabel(self.tab_mass_table)
        self.label_153.setObjectName(u"label_153")
        self.label_153.setEnabled(True)
        self.label_153.setMinimumSize(QSize(30, 26))
        self.label_153.setMaximumSize(QSize(30, 26))
        self.label_153.setFont(font)
        self.label_153.setMouseTracking(True)
        self.label_153.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_153, 3, 1, 1, 1)

        self.pushButton_load_Mz_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_Mz_table.setObjectName(u"pushButton_load_Mz_table")
        self.pushButton_load_Mz_table.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_load_Mz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Mz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Mz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Mz_table.setFont(font)
        self.pushButton_load_Mz_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_Mz_table, 2, 3, 1, 1)

        self.label_150 = QLabel(self.tab_mass_table)
        self.label_150.setObjectName(u"label_150")
        self.label_150.setEnabled(True)
        self.label_150.setMinimumSize(QSize(30, 26))
        self.label_150.setMaximumSize(QSize(30, 26))
        self.label_150.setFont(font)
        self.label_150.setMouseTracking(True)
        self.label_150.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_150, 0, 1, 1, 1)

        self.pushButton_load_My_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_My_table.setObjectName(u"pushButton_load_My_table")
        self.pushButton_load_My_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_My_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_My_table.setSizePolicy(sizePolicy)
        self.pushButton_load_My_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_My_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_My_table.setFont(font)
        self.pushButton_load_My_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_My_table, 1, 3, 1, 1)

        self.lineEdit_Jx_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_Jx_table_path.setObjectName(u"lineEdit_Jx_table_path")
        self.lineEdit_Jx_table_path.setEnabled(True)
        self.lineEdit_Jx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Jx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Jx_table_path.setSizeIncrement(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(9)
        self.lineEdit_Jx_table_path.setFont(font4)
        self.lineEdit_Jx_table_path.setStyleSheet(u"")
        self.lineEdit_Jx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Jx_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_Jx_table_path, 3, 2, 1, 1)

        self.pushButton_load_Jx_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_Jx_table.setObjectName(u"pushButton_load_Jx_table")
        self.pushButton_load_Jx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Jx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Jx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Jx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Jx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Jx_table.setFont(font)
        self.pushButton_load_Jx_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_Jx_table, 3, 3, 1, 1)

        self.lineEdit_Jy_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_Jy_table_path.setObjectName(u"lineEdit_Jy_table_path")
        self.lineEdit_Jy_table_path.setEnabled(True)
        self.lineEdit_Jy_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Jy_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Jy_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Jy_table_path.setFont(font4)
        self.lineEdit_Jy_table_path.setStyleSheet(u"")
        self.lineEdit_Jy_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Jy_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_Jy_table_path, 4, 2, 1, 1)

        self.pushButton_load_Jy_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_Jy_table.setObjectName(u"pushButton_load_Jy_table")
        self.pushButton_load_Jy_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Jy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Jy_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Jy_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Jy_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Jy_table.setFont(font)
        self.pushButton_load_Jy_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_Jy_table, 4, 3, 1, 1)

        self.pushButton_load_Jz_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_Jz_table.setObjectName(u"pushButton_load_Jz_table")
        self.pushButton_load_Jz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Jz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Jz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Jz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Jz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Jz_table.setFont(font)
        self.pushButton_load_Jz_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_Jz_table, 5, 3, 1, 1)

        self.lineEdit_Mx_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_Mx_table_path.setObjectName(u"lineEdit_Mx_table_path")
        self.lineEdit_Mx_table_path.setEnabled(True)
        self.lineEdit_Mx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Mx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Mx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Mx_table_path.setFont(font4)
        self.lineEdit_Mx_table_path.setStyleSheet(u"")
        self.lineEdit_Mx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Mx_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_Mx_table_path, 0, 2, 1, 1)

        self.lineEdit_Jz_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_Jz_table_path.setObjectName(u"lineEdit_Jz_table_path")
        self.lineEdit_Jz_table_path.setEnabled(True)
        self.lineEdit_Jz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Jz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Jz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Jz_table_path.setFont(font4)
        self.lineEdit_Jz_table_path.setStyleSheet(u"")
        self.lineEdit_Jz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Jz_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_Jz_table_path, 5, 2, 1, 1)

        self.label_151 = QLabel(self.tab_mass_table)
        self.label_151.setObjectName(u"label_151")
        self.label_151.setEnabled(True)
        self.label_151.setMinimumSize(QSize(30, 26))
        self.label_151.setMaximumSize(QSize(30, 26))
        self.label_151.setFont(font)
        self.label_151.setMouseTracking(True)
        self.label_151.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_151, 1, 1, 1, 1)

        self.lineEdit_My_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_My_table_path.setObjectName(u"lineEdit_My_table_path")
        self.lineEdit_My_table_path.setEnabled(True)
        self.lineEdit_My_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_My_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_My_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_My_table_path.setFont(font4)
        self.lineEdit_My_table_path.setStyleSheet(u"")
        self.lineEdit_My_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_My_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_My_table_path, 1, 2, 1, 1)

        self.lineEdit_Mz_table_path = QLineEdit(self.tab_mass_table)
        self.lineEdit_Mz_table_path.setObjectName(u"lineEdit_Mz_table_path")
        self.lineEdit_Mz_table_path.setEnabled(True)
        self.lineEdit_Mz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Mz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Mz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Mz_table_path.setFont(font4)
        self.lineEdit_Mz_table_path.setStyleSheet(u"")
        self.lineEdit_Mz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Mz_table_path.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_Mz_table_path, 2, 2, 1, 1)

        self.pushButton_load_Mx_table = QPushButton(self.tab_mass_table)
        self.pushButton_load_Mx_table.setObjectName(u"pushButton_load_Mx_table")
        self.pushButton_load_Mx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Mx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Mx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Mx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Mx_table.setFont(font)
        self.pushButton_load_Mx_table.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_load_Mx_table, 0, 3, 1, 1)

        self.label_146 = QLabel(self.tab_mass_table)
        self.label_146.setObjectName(u"label_146")
        self.label_146.setEnabled(True)
        self.label_146.setMinimumSize(QSize(30, 26))
        self.label_146.setMaximumSize(QSize(30, 26))
        self.label_146.setFont(font)
        self.label_146.setMouseTracking(True)
        self.label_146.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_146, 2, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.tabWidget_table_values.addTab(self.tab_mass_table, "")
        self.tab_stiffness_table = QWidget()
        self.tab_stiffness_table.setObjectName(u"tab_stiffness_table")
        self.gridLayout_25 = QGridLayout(self.tab_stiffness_table)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_Kx_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Kx_table_path.setObjectName(u"lineEdit_Kx_table_path")
        self.lineEdit_Kx_table_path.setEnabled(True)
        self.lineEdit_Kx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Kx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Kx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kx_table_path.setFont(font4)
        self.lineEdit_Kx_table_path.setStyleSheet(u"")
        self.lineEdit_Kx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kx_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Kx_table_path, 0, 2, 1, 1)

        self.pushButton_load_Kx_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Kx_table.setObjectName(u"pushButton_load_Kx_table")
        self.pushButton_load_Kx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kx_table.setFont(font)
        self.pushButton_load_Kx_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kx_table, 0, 3, 1, 1)

        self.label_117 = QLabel(self.tab_stiffness_table)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setEnabled(True)
        self.label_117.setMinimumSize(QSize(30, 26))
        self.label_117.setMaximumSize(QSize(30, 26))
        self.label_117.setFont(font)
        self.label_117.setMouseTracking(True)
        self.label_117.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_117, 0, 1, 1, 1)

        self.pushButton_load_Ky_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Ky_table.setObjectName(u"pushButton_load_Ky_table")
        self.pushButton_load_Ky_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Ky_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Ky_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Ky_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Ky_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Ky_table.setFont(font)
        self.pushButton_load_Ky_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Ky_table, 1, 3, 1, 1)

        self.pushButton_load_Kz_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Kz_table.setObjectName(u"pushButton_load_Kz_table")
        self.pushButton_load_Kz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kz_table.setFont(font)
        self.pushButton_load_Kz_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kz_table, 2, 3, 1, 1)

        self.lineEdit_Kz_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Kz_table_path.setObjectName(u"lineEdit_Kz_table_path")
        self.lineEdit_Kz_table_path.setEnabled(True)
        self.lineEdit_Kz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Kz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Kz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kz_table_path.setFont(font4)
        self.lineEdit_Kz_table_path.setStyleSheet(u"")
        self.lineEdit_Kz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kz_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Kz_table_path, 2, 2, 1, 1)

        self.pushButton_load_Krx_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Krx_table.setObjectName(u"pushButton_load_Krx_table")
        self.pushButton_load_Krx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Krx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Krx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Krx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Krx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Krx_table.setFont(font)
        self.pushButton_load_Krx_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Krx_table, 3, 3, 1, 1)

        self.label_118 = QLabel(self.tab_stiffness_table)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setEnabled(True)
        self.label_118.setMinimumSize(QSize(30, 26))
        self.label_118.setMaximumSize(QSize(30, 26))
        self.label_118.setFont(font)
        self.label_118.setMouseTracking(True)
        self.label_118.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_118, 4, 1, 1, 1)

        self.lineEdit_Ky_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Ky_table_path.setObjectName(u"lineEdit_Ky_table_path")
        self.lineEdit_Ky_table_path.setEnabled(True)
        self.lineEdit_Ky_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Ky_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Ky_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Ky_table_path.setFont(font4)
        self.lineEdit_Ky_table_path.setStyleSheet(u"")
        self.lineEdit_Ky_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Ky_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Ky_table_path, 1, 2, 1, 1)

        self.label_132 = QLabel(self.tab_stiffness_table)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setEnabled(True)
        self.label_132.setMinimumSize(QSize(30, 26))
        self.label_132.setMaximumSize(QSize(30, 26))
        self.label_132.setFont(font)
        self.label_132.setMouseTracking(True)
        self.label_132.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_132, 1, 1, 1, 1)

        self.pushButton_load_Kry_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Kry_table.setObjectName(u"pushButton_load_Kry_table")
        self.pushButton_load_Kry_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kry_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kry_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kry_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kry_table.setFont(font)
        self.pushButton_load_Kry_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kry_table, 4, 3, 1, 1)

        self.label_119 = QLabel(self.tab_stiffness_table)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setEnabled(True)
        self.label_119.setMinimumSize(QSize(30, 26))
        self.label_119.setMaximumSize(QSize(30, 26))
        self.label_119.setFont(font)
        self.label_119.setMouseTracking(True)
        self.label_119.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_119, 5, 1, 1, 1)

        self.label_135 = QLabel(self.tab_stiffness_table)
        self.label_135.setObjectName(u"label_135")
        self.label_135.setEnabled(True)
        self.label_135.setMinimumSize(QSize(30, 26))
        self.label_135.setMaximumSize(QSize(30, 26))
        self.label_135.setFont(font)
        self.label_135.setMouseTracking(True)
        self.label_135.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_135, 3, 1, 1, 1)

        self.lineEdit_Krz_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Krz_table_path.setObjectName(u"lineEdit_Krz_table_path")
        self.lineEdit_Krz_table_path.setEnabled(True)
        self.lineEdit_Krz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Krz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Krz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Krz_table_path.setFont(font4)
        self.lineEdit_Krz_table_path.setStyleSheet(u"")
        self.lineEdit_Krz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Krz_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Krz_table_path, 5, 2, 1, 1)

        self.pushButton_load_Krz_table = QPushButton(self.tab_stiffness_table)
        self.pushButton_load_Krz_table.setObjectName(u"pushButton_load_Krz_table")
        self.pushButton_load_Krz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Krz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Krz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Krz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Krz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Krz_table.setFont(font)
        self.pushButton_load_Krz_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Krz_table, 5, 3, 1, 1)

        self.label_134 = QLabel(self.tab_stiffness_table)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setEnabled(True)
        self.label_134.setMinimumSize(QSize(30, 26))
        self.label_134.setMaximumSize(QSize(30, 26))
        self.label_134.setFont(font)
        self.label_134.setMouseTracking(True)
        self.label_134.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_25.addWidget(self.label_134, 2, 1, 1, 1)

        self.lineEdit_Krx_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Krx_table_path.setObjectName(u"lineEdit_Krx_table_path")
        self.lineEdit_Krx_table_path.setEnabled(True)
        self.lineEdit_Krx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Krx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Krx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Krx_table_path.setFont(font4)
        self.lineEdit_Krx_table_path.setStyleSheet(u"")
        self.lineEdit_Krx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Krx_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Krx_table_path, 3, 2, 1, 1)

        self.lineEdit_Kry_table_path = QLineEdit(self.tab_stiffness_table)
        self.lineEdit_Kry_table_path.setObjectName(u"lineEdit_Kry_table_path")
        self.lineEdit_Kry_table_path.setEnabled(True)
        self.lineEdit_Kry_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Kry_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Kry_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kry_table_path.setFont(font4)
        self.lineEdit_Kry_table_path.setStyleSheet(u"")
        self.lineEdit_Kry_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Kry_table_path.setClearButtonEnabled(True)

        self.gridLayout_25.addWidget(self.lineEdit_Kry_table_path, 4, 2, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_19, 0, 0, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_20, 0, 4, 1, 1)

        self.tabWidget_table_values.addTab(self.tab_stiffness_table, "")
        self.tab_damping_table = QWidget()
        self.tab_damping_table.setObjectName(u"tab_damping_table")
        self.gridLayout_17 = QGridLayout(self.tab_damping_table)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_21, 0, 4, 1, 1)

        self.label_138 = QLabel(self.tab_damping_table)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setEnabled(True)
        self.label_138.setMinimumSize(QSize(30, 26))
        self.label_138.setMaximumSize(QSize(30, 26))
        self.label_138.setFont(font)
        self.label_138.setMouseTracking(True)
        self.label_138.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_138, 0, 1, 1, 1)

        self.lineEdit_Cx_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Cx_table_path.setObjectName(u"lineEdit_Cx_table_path")
        self.lineEdit_Cx_table_path.setEnabled(True)
        self.lineEdit_Cx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Cx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Cx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Cx_table_path.setFont(font4)
        self.lineEdit_Cx_table_path.setStyleSheet(u"")
        self.lineEdit_Cx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Cx_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Cx_table_path, 0, 2, 1, 1)

        self.pushButton_load_Cx_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Cx_table.setObjectName(u"pushButton_load_Cx_table")
        self.pushButton_load_Cx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cx_table.setFont(font)
        self.pushButton_load_Cx_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cx_table, 0, 3, 1, 1)

        self.label_133 = QLabel(self.tab_damping_table)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setEnabled(True)
        self.label_133.setMinimumSize(QSize(30, 26))
        self.label_133.setMaximumSize(QSize(30, 26))
        self.label_133.setFont(font)
        self.label_133.setMouseTracking(True)
        self.label_133.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_133, 1, 1, 1, 1)

        self.label_136 = QLabel(self.tab_damping_table)
        self.label_136.setObjectName(u"label_136")
        self.label_136.setEnabled(True)
        self.label_136.setMinimumSize(QSize(30, 26))
        self.label_136.setMaximumSize(QSize(30, 26))
        self.label_136.setFont(font)
        self.label_136.setMouseTracking(True)
        self.label_136.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_136, 2, 1, 1, 1)

        self.lineEdit_Cy_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Cy_table_path.setObjectName(u"lineEdit_Cy_table_path")
        self.lineEdit_Cy_table_path.setEnabled(True)
        self.lineEdit_Cy_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Cy_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Cy_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Cy_table_path.setFont(font4)
        self.lineEdit_Cy_table_path.setStyleSheet(u"")
        self.lineEdit_Cy_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Cy_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Cy_table_path, 1, 2, 1, 1)

        self.pushButton_load_Cy_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Cy_table.setObjectName(u"pushButton_load_Cy_table")
        self.pushButton_load_Cy_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cy_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cy_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cy_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cy_table.setFont(font)
        self.pushButton_load_Cy_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cy_table, 1, 3, 1, 1)

        self.lineEdit_Cz_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Cz_table_path.setObjectName(u"lineEdit_Cz_table_path")
        self.lineEdit_Cz_table_path.setEnabled(True)
        self.lineEdit_Cz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Cz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Cz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Cz_table_path.setFont(font4)
        self.lineEdit_Cz_table_path.setStyleSheet(u"")
        self.lineEdit_Cz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Cz_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Cz_table_path, 2, 2, 1, 1)

        self.pushButton_load_Cz_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Cz_table.setObjectName(u"pushButton_load_Cz_table")
        self.pushButton_load_Cz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cz_table.setFont(font)
        self.pushButton_load_Cz_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cz_table, 2, 3, 1, 1)

        self.pushButton_load_Crx_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Crx_table.setObjectName(u"pushButton_load_Crx_table")
        self.pushButton_load_Crx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Crx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Crx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Crx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Crx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Crx_table.setFont(font)
        self.pushButton_load_Crx_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Crx_table, 3, 3, 1, 1)

        self.label_139 = QLabel(self.tab_damping_table)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setEnabled(True)
        self.label_139.setMinimumSize(QSize(30, 26))
        self.label_139.setMaximumSize(QSize(30, 26))
        self.label_139.setFont(font)
        self.label_139.setMouseTracking(True)
        self.label_139.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_139, 4, 1, 1, 1)

        self.lineEdit_Cry_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Cry_table_path.setObjectName(u"lineEdit_Cry_table_path")
        self.lineEdit_Cry_table_path.setEnabled(True)
        self.lineEdit_Cry_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Cry_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Cry_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Cry_table_path.setFont(font4)
        self.lineEdit_Cry_table_path.setStyleSheet(u"")
        self.lineEdit_Cry_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Cry_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Cry_table_path, 4, 2, 1, 1)

        self.label_137 = QLabel(self.tab_damping_table)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setEnabled(True)
        self.label_137.setMinimumSize(QSize(30, 26))
        self.label_137.setMaximumSize(QSize(30, 26))
        self.label_137.setFont(font)
        self.label_137.setMouseTracking(True)
        self.label_137.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_137, 3, 1, 1, 1)

        self.lineEdit_Crx_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Crx_table_path.setObjectName(u"lineEdit_Crx_table_path")
        self.lineEdit_Crx_table_path.setEnabled(True)
        self.lineEdit_Crx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Crx_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Crx_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Crx_table_path.setFont(font4)
        self.lineEdit_Crx_table_path.setStyleSheet(u"")
        self.lineEdit_Crx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Crx_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Crx_table_path, 3, 2, 1, 1)

        self.pushButton_load_Cry_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Cry_table.setObjectName(u"pushButton_load_Cry_table")
        self.pushButton_load_Cry_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cry_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cry_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cry_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cry_table.setFont(font)
        self.pushButton_load_Cry_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cry_table, 4, 3, 1, 1)

        self.label_120 = QLabel(self.tab_damping_table)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setEnabled(True)
        self.label_120.setMinimumSize(QSize(30, 26))
        self.label_120.setMaximumSize(QSize(30, 26))
        self.label_120.setFont(font)
        self.label_120.setMouseTracking(True)
        self.label_120.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.label_120, 5, 1, 1, 1)

        self.pushButton_load_Crz_table = QPushButton(self.tab_damping_table)
        self.pushButton_load_Crz_table.setObjectName(u"pushButton_load_Crz_table")
        self.pushButton_load_Crz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Crz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Crz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Crz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Crz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Crz_table.setFont(font)
        self.pushButton_load_Crz_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Crz_table, 5, 3, 1, 1)

        self.lineEdit_Crz_table_path = QLineEdit(self.tab_damping_table)
        self.lineEdit_Crz_table_path.setObjectName(u"lineEdit_Crz_table_path")
        self.lineEdit_Crz_table_path.setEnabled(True)
        self.lineEdit_Crz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Crz_table_path.setMaximumSize(QSize(250, 26))
        self.lineEdit_Crz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Crz_table_path.setFont(font4)
        self.lineEdit_Crz_table_path.setStyleSheet(u"")
        self.lineEdit_Crz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Crz_table_path.setClearButtonEnabled(True)

        self.gridLayout_17.addWidget(self.lineEdit_Crz_table_path, 5, 2, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_22, 0, 0, 1, 1)

        self.tabWidget_table_values.addTab(self.tab_damping_table, "")

        self.gridLayout_10.addWidget(self.tabWidget_table_values, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_tabular, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        font5 = QFont()
        font5.setFamilies([u"MS UI Gothic"])
        font5.setPointSize(10)
        self.tab_list.setFont(font5)
        self.gridLayout_20 = QGridLayout(self.tab_list)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.tab_list)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 160))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_remove = QTabWidget(self.frame_2)
        self.tabWidget_remove.setObjectName(u"tabWidget_remove")
        self.tabWidget_remove.setMinimumSize(QSize(0, 0))
        self.tabWidget_remove.setMaximumSize(QSize(400, 240))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        self.tabWidget_remove.setFont(font6)
        self.tab_multiple_remove = QWidget()
        self.tab_multiple_remove.setObjectName(u"tab_multiple_remove")
        self.gridLayout_8 = QGridLayout(self.tab_multiple_remove)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.checkBox_remove_stiffness = QCheckBox(self.tab_multiple_remove)
        self.checkBox_remove_stiffness.setObjectName(u"checkBox_remove_stiffness")
        self.checkBox_remove_stiffness.setMinimumSize(QSize(200, 25))
        self.checkBox_remove_stiffness.setMaximumSize(QSize(250, 25))
        self.checkBox_remove_stiffness.setFont(font6)
        self.checkBox_remove_stiffness.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_remove_stiffness, 1, 1, 1, 1)

        self.checkBox_remove_mass = QCheckBox(self.tab_multiple_remove)
        self.checkBox_remove_mass.setObjectName(u"checkBox_remove_mass")
        self.checkBox_remove_mass.setMinimumSize(QSize(200, 25))
        self.checkBox_remove_mass.setMaximumSize(QSize(250, 25))
        self.checkBox_remove_mass.setFont(font6)
        self.checkBox_remove_mass.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_remove_mass, 0, 1, 1, 1)

        self.checkBox_remove_damping = QCheckBox(self.tab_multiple_remove)
        self.checkBox_remove_damping.setObjectName(u"checkBox_remove_damping")
        self.checkBox_remove_damping.setMinimumSize(QSize(200, 25))
        self.checkBox_remove_damping.setMaximumSize(QSize(250, 25))
        self.checkBox_remove_damping.setFont(font6)
        self.checkBox_remove_damping.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_remove_damping, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.tabWidget_remove.addTab(self.tab_multiple_remove, "")
        self.tab_mass_remove = QWidget()
        self.tab_mass_remove.setObjectName(u"tab_mass_remove")
        self.gridLayout_4 = QGridLayout(self.tab_mass_remove)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_mass = QTreeWidget(self.tab_mass_remove)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_mass.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_mass.setObjectName(u"treeWidget_mass")
        self.treeWidget_mass.setMinimumSize(QSize(0, 0))
        self.treeWidget_mass.setMaximumSize(QSize(16777215, 16777215))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(9)
        self.treeWidget_mass.setFont(font7)
        self.treeWidget_mass.setIndentation(0)

        self.gridLayout_4.addWidget(self.treeWidget_mass, 0, 0, 1, 1)

        self.tabWidget_remove.addTab(self.tab_mass_remove, "")
        self.tab_stiffness_remove = QWidget()
        self.tab_stiffness_remove.setObjectName(u"tab_stiffness_remove")
        self.gridLayout_5 = QGridLayout(self.tab_stiffness_remove)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_stiffness = QTreeWidget(self.tab_stiffness_remove)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_stiffness.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_stiffness.setObjectName(u"treeWidget_stiffness")
        self.treeWidget_stiffness.setMinimumSize(QSize(0, 0))
        self.treeWidget_stiffness.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_stiffness.setFont(font7)
        self.treeWidget_stiffness.setIndentation(0)

        self.gridLayout_5.addWidget(self.treeWidget_stiffness, 0, 0, 1, 1)

        self.tabWidget_remove.addTab(self.tab_stiffness_remove, "")
        self.tab_damping_remove = QWidget()
        self.tab_damping_remove.setObjectName(u"tab_damping_remove")
        self.gridLayout_7 = QGridLayout(self.tab_damping_remove)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_damping = QTreeWidget(self.tab_damping_remove)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_damping.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_damping.setObjectName(u"treeWidget_damping")
        self.treeWidget_damping.setMinimumSize(QSize(0, 0))
        self.treeWidget_damping.setMaximumSize(QSize(16777215, 16777215))
        self.treeWidget_damping.setIndentation(0)

        self.gridLayout_7.addWidget(self.treeWidget_damping, 0, 0, 1, 1)

        self.tabWidget_remove.addTab(self.tab_damping_remove, "")

        self.gridLayout_3.addWidget(self.tabWidget_remove, 0, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.tab_list)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_buttons)
        self.gridLayout_21.setSpacing(4)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(2, 2, 2, 2)
        self.pushButton_reset = QPushButton(self.frame_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font6)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_21.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font6)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_21.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_20.addWidget(self.frame_buttons, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_14.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_tabWidgets, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        self.frame_confirm = QFrame(Dialog)
        self.frame_confirm.setObjectName(u"frame_confirm")
        self.frame_confirm.setMinimumSize(QSize(0, 48))
        self.frame_confirm.setMaximumSize(QSize(16777215, 48))
        self.frame_confirm.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_confirm.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_confirm)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_confirm)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)
        self.pushButton_attribute.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_confirm)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_confirm, 2, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_exit, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_Mx)
        QWidget.setTabOrder(self.lineEdit_Mx, self.lineEdit_My)
        QWidget.setTabOrder(self.lineEdit_My, self.lineEdit_Mz)
        QWidget.setTabOrder(self.lineEdit_Mz, self.lineEdit_Jx)
        QWidget.setTabOrder(self.lineEdit_Jx, self.lineEdit_Jy)
        QWidget.setTabOrder(self.lineEdit_Jy, self.lineEdit_Jz)
        QWidget.setTabOrder(self.lineEdit_Jz, self.lineEdit_Kx)
        QWidget.setTabOrder(self.lineEdit_Kx, self.lineEdit_Ky)
        QWidget.setTabOrder(self.lineEdit_Ky, self.lineEdit_Kz)
        QWidget.setTabOrder(self.lineEdit_Kz, self.lineEdit_Krx)
        QWidget.setTabOrder(self.lineEdit_Krx, self.lineEdit_Kry)
        QWidget.setTabOrder(self.lineEdit_Kry, self.lineEdit_Krz)
        QWidget.setTabOrder(self.lineEdit_Krz, self.lineEdit_Cx)
        QWidget.setTabOrder(self.lineEdit_Cx, self.lineEdit_Cy)
        QWidget.setTabOrder(self.lineEdit_Cy, self.lineEdit_Cz)
        QWidget.setTabOrder(self.lineEdit_Cz, self.lineEdit_Crx)
        QWidget.setTabOrder(self.lineEdit_Crx, self.lineEdit_Cry)
        QWidget.setTabOrder(self.lineEdit_Cry, self.lineEdit_Crz)
        QWidget.setTabOrder(self.lineEdit_Crz, self.lineEdit_Mx_table_path)
        QWidget.setTabOrder(self.lineEdit_Mx_table_path, self.lineEdit_My_table_path)
        QWidget.setTabOrder(self.lineEdit_My_table_path, self.lineEdit_Mz_table_path)
        QWidget.setTabOrder(self.lineEdit_Mz_table_path, self.lineEdit_Jx_table_path)
        QWidget.setTabOrder(self.lineEdit_Jx_table_path, self.lineEdit_Jy_table_path)
        QWidget.setTabOrder(self.lineEdit_Jy_table_path, self.lineEdit_Jz_table_path)
        QWidget.setTabOrder(self.lineEdit_Jz_table_path, self.lineEdit_Kx_table_path)
        QWidget.setTabOrder(self.lineEdit_Kx_table_path, self.lineEdit_Ky_table_path)
        QWidget.setTabOrder(self.lineEdit_Ky_table_path, self.lineEdit_Kz_table_path)
        QWidget.setTabOrder(self.lineEdit_Kz_table_path, self.lineEdit_Krx_table_path)
        QWidget.setTabOrder(self.lineEdit_Krx_table_path, self.lineEdit_Kry_table_path)
        QWidget.setTabOrder(self.lineEdit_Kry_table_path, self.lineEdit_Krz_table_path)
        QWidget.setTabOrder(self.lineEdit_Krz_table_path, self.lineEdit_Cx_table_path)
        QWidget.setTabOrder(self.lineEdit_Cx_table_path, self.lineEdit_Cy_table_path)
        QWidget.setTabOrder(self.lineEdit_Cy_table_path, self.lineEdit_Cz_table_path)
        QWidget.setTabOrder(self.lineEdit_Cz_table_path, self.lineEdit_Crx_table_path)
        QWidget.setTabOrder(self.lineEdit_Crx_table_path, self.lineEdit_Cry_table_path)
        QWidget.setTabOrder(self.lineEdit_Cry_table_path, self.lineEdit_Crz_table_path)
        QWidget.setTabOrder(self.lineEdit_Crz_table_path, self.pushButton_load_Mx_table)
        QWidget.setTabOrder(self.pushButton_load_Mx_table, self.pushButton_load_My_table)
        QWidget.setTabOrder(self.pushButton_load_My_table, self.pushButton_load_Mz_table)
        QWidget.setTabOrder(self.pushButton_load_Mz_table, self.pushButton_load_Jx_table)
        QWidget.setTabOrder(self.pushButton_load_Jx_table, self.pushButton_load_Jy_table)
        QWidget.setTabOrder(self.pushButton_load_Jy_table, self.pushButton_load_Jz_table)
        QWidget.setTabOrder(self.pushButton_load_Jz_table, self.pushButton_load_Kx_table)
        QWidget.setTabOrder(self.pushButton_load_Kx_table, self.pushButton_load_Ky_table)
        QWidget.setTabOrder(self.pushButton_load_Ky_table, self.pushButton_load_Kz_table)
        QWidget.setTabOrder(self.pushButton_load_Kz_table, self.pushButton_load_Krx_table)
        QWidget.setTabOrder(self.pushButton_load_Krx_table, self.pushButton_load_Kry_table)
        QWidget.setTabOrder(self.pushButton_load_Kry_table, self.pushButton_load_Krz_table)
        QWidget.setTabOrder(self.pushButton_load_Krz_table, self.pushButton_load_Cx_table)
        QWidget.setTabOrder(self.pushButton_load_Cx_table, self.pushButton_load_Cy_table)
        QWidget.setTabOrder(self.pushButton_load_Cy_table, self.pushButton_load_Cz_table)
        QWidget.setTabOrder(self.pushButton_load_Cz_table, self.pushButton_load_Crx_table)
        QWidget.setTabOrder(self.pushButton_load_Crx_table, self.pushButton_load_Cry_table)
        QWidget.setTabOrder(self.pushButton_load_Cry_table, self.pushButton_load_Crz_table)
        QWidget.setTabOrder(self.pushButton_load_Crz_table, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.tabWidget_table_values)
        QWidget.setTabOrder(self.tabWidget_table_values, self.tabWidget_constant_values)
        QWidget.setTabOrder(self.tabWidget_constant_values, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.treeWidget_stiffness)
        QWidget.setTabOrder(self.treeWidget_stiffness, self.treeWidget_mass)
        QWidget.setTabOrder(self.treeWidget_mass, self.checkBox_remove_damping)
        QWidget.setTabOrder(self.checkBox_remove_damping, self.treeWidget_damping)
        QWidget.setTabOrder(self.treeWidget_damping, self.checkBox_remove_stiffness)
        QWidget.setTabOrder(self.checkBox_remove_stiffness, self.checkBox_remove_mass)
        QWidget.setTabOrder(self.checkBox_remove_mass, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.tabWidget_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_constant_values.setCurrentIndex(0)
        self.tabWidget_table_values.setCurrentIndex(0)
        self.tabWidget_remove.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(True)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Lumped elements configuration", None))
        self.label_first_node_id.setText(QCoreApplication.translate("Dialog", u"Selected nodes:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_node_ids.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select or type the nodes IDs to apply the lumped elements</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_141.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.lineEdit_Jz.setText("")
        self.label_140.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.lineEdit_Mz.setText("")
        self.lineEdit_Mx.setText("")
        self.label_147.setText(QCoreApplication.translate("Dialog", u"[kg.m\u00b2]", None))
        self.label_142.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.lineEdit_Jy.setText("")
        self.label_23.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.lineEdit_My.setText("")
        self.label_144.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.lineEdit_Jx.setText("")
        self.label_94.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.label_145.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[kg]", None))
        self.label_148.setText(QCoreApplication.translate("Dialog", u"[kg.m\u00b2]", None))
        self.label_149.setText(QCoreApplication.translate("Dialog", u"[kg.m\u00b2]", None))
        self.tabWidget_constant_values.setTabText(self.tabWidget_constant_values.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Mass", None))
        self.lineEdit_Krx.setText("")
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.lineEdit_Ky.setText("")
        self.label_115.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">x</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_93.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">rx</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_113.setText(QCoreApplication.translate("Dialog", u"[N.m/rad]", None))
        self.label_116.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.label_123.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.lineEdit_Kz.setText("")
        self.label_18.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.label_112.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">ry</span>:</p></body></html>", None))
        self.label_114.setText(QCoreApplication.translate("Dialog", u"[N.m/rad]", None))
        self.lineEdit_Krz.setText("")
        self.label_122.setText(QCoreApplication.translate("Dialog", u"[N.m/rad]", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[N/m]", None))
        self.lineEdit_Kx.setText("")
        self.lineEdit_Kry.setText("")
        self.label_121.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">rz</span>:</p></body></html>", None))
        self.tabWidget_constant_values.setTabText(self.tabWidget_constant_values.indexOf(self.tab_stiffness), QCoreApplication.translate("Dialog", u"Stiffness", None))
        self.lineEdit_Crz.setText("")
        self.label_131.setText(QCoreApplication.translate("Dialog", u"[N.m/rad/s]", None))
        self.label_126.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">rz</span>:</p></body></html>", None))
        self.label_128.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.lineEdit_Cy.setText("")
        self.lineEdit_Cz.setText("")
        self.label_102.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">rx</span>:</p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.lineEdit_Crx.setText("")
        self.label_127.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.label_125.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">ry</span>:</p></body></html>", None))
        self.label_130.setText(QCoreApplication.translate("Dialog", u"[N.m/rad/s]", None))
        self.label_124.setText(QCoreApplication.translate("Dialog", u"[N.m/rad/s]", None))
        self.lineEdit_Cry.setText("")
        self.label_129.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.lineEdit_Cx.setText("")
        self.label_20.setText(QCoreApplication.translate("Dialog", u"[N.s/m]", None))
        self.tabWidget_constant_values.setTabText(self.tabWidget_constant_values.indexOf(self.tab_damping), QCoreApplication.translate("Dialog", u"Damping", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant), QCoreApplication.translate("Dialog", u"Constant", None))
        self.label_143.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.label_152.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.label_153.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">J<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.pushButton_load_Mz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_150.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.pushButton_load_My_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Jx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Jy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Jz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_151.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.pushButton_load_Mx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_146.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">m<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.tabWidget_table_values.setTabText(self.tabWidget_table_values.indexOf(self.tab_mass_table), QCoreApplication.translate("Dialog", u"Mass", None))
        self.pushButton_load_Kx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_117.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">x</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.pushButton_load_Ky_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Kz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Krx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_118.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">ry</span>:</p></body></html>", None))
        self.label_132.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.pushButton_load_Kry_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_119.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">rz</span>:</p></body></html>", None))
        self.label_135.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">rx</span>:</p></body></html>", None))
        self.pushButton_load_Krz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_134.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.tabWidget_table_values.setTabText(self.tabWidget_table_values.indexOf(self.tab_stiffness_table), QCoreApplication.translate("Dialog", u"Stiffness", None))
        self.label_138.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">x</span>:</p></body></html>", None))
        self.pushButton_load_Cx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_133.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">y</span>:</p></body></html>", None))
        self.label_136.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">z</span>:</p></body></html>", None))
        self.pushButton_load_Cy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Cz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Crx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_139.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">ry</span>:</p></body></html>", None))
        self.label_137.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">rx</span>:</p></body></html>", None))
        self.pushButton_load_Cry_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_120.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">c<span style=\" vertical-align:sub;\">rz</span>:</p></body></html>", None))
        self.pushButton_load_Crz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.tabWidget_table_values.setTabText(self.tabWidget_table_values.indexOf(self.tab_damping_table), QCoreApplication.translate("Dialog", u"Damping", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tabular), QCoreApplication.translate("Dialog", u"Tabular", None))
        self.checkBox_remove_stiffness.setText(QCoreApplication.translate("Dialog", u"Stiffness (translational/torsional)", None))
        self.checkBox_remove_mass.setText(QCoreApplication.translate("Dialog", u"Masses / Moments of inertia", None))
        self.checkBox_remove_damping.setText(QCoreApplication.translate("Dialog", u"Dampings (translational/torsional)", None))
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_multiple_remove), QCoreApplication.translate("Dialog", u"Multiple", None))
        ___qtreewidgetitem = self.treeWidget_mass.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_mass_remove), QCoreApplication.translate("Dialog", u"Mass", None))
        ___qtreewidgetitem1 = self.treeWidget_stiffness.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_stiffness_remove), QCoreApplication.translate("Dialog", u"Stiffness", None))
        ___qtreewidgetitem2 = self.treeWidget_damping.headerItem()
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None))
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_damping_remove), QCoreApplication.translate("Dialog", u"Damping", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class MassSpringDamperInput_UI(QDialog, Ui_Dialog):
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
                                        - label_first_node_id: QLabel
                                        - lineEdit_node_ids: QLineEdit
                            - frame_tabWidgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_constant: QWidget
                                                - (Layout): QGridLayout
                                                        - tabWidget_constant_values: QTabWidget
                                                            - tab_2: QWidget
                                                                - (Layout): QGridLayout
                                                                        - label_141: QLabel
                                                                        - lineEdit_Jz: QLineEdit
                                                                        - label_140: QLabel
                                                                        - lineEdit_Mz: QLineEdit
                                                                        - lineEdit_Mx: QLineEdit
                                                                        - label_147: QLabel
                                                                        - label_142: QLabel
                                                                        - lineEdit_Jy: QLineEdit
                                                                        - label_23: QLabel
                                                                        - lineEdit_My: QLineEdit
                                                                        - label_144: QLabel
                                                                        - lineEdit_Jx: QLineEdit
                                                                        - label_94: QLabel
                                                                        - label_145: QLabel
                                                                        - label_24: QLabel
                                                                        - label_25: QLabel
                                                                        - label_148: QLabel
                                                                        - label_149: QLabel
                                                            - tab_stiffness: QWidget
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_Krx: QLineEdit
                                                                        - label_16: QLabel
                                                                        - lineEdit_Ky: QLineEdit
                                                                        - label_115: QLabel
                                                                        - label_93: QLabel
                                                                        - label_113: QLabel
                                                                        - label_116: QLabel
                                                                        - label_123: QLabel
                                                                        - lineEdit_Kz: QLineEdit
                                                                        - label_18: QLabel
                                                                        - label_112: QLabel
                                                                        - label_114: QLabel
                                                                        - lineEdit_Krz: QLineEdit
                                                                        - label_122: QLabel
                                                                        - label_17: QLabel
                                                                        - lineEdit_Kx: QLineEdit
                                                                        - lineEdit_Kry: QLineEdit
                                                                        - label_121: QLabel
                                                            - tab_damping: QWidget
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_Crz: QLineEdit
                                                                        - label_131: QLabel
                                                                        - label_126: QLabel
                                                                        - label_128: QLabel
                                                                        - lineEdit_Cy: QLineEdit
                                                                        - lineEdit_Cz: QLineEdit
                                                                        - label_102: QLabel
                                                                        - label_19: QLabel
                                                                        - label_21: QLabel
                                                                        - lineEdit_Crx: QLineEdit
                                                                        - label_127: QLabel
                                                                        - label_125: QLabel
                                                                        - label_130: QLabel
                                                                        - label_124: QLabel
                                                                        - lineEdit_Cry: QLineEdit
                                                                        - label_129: QLabel
                                                                        - lineEdit_Cx: QLineEdit
                                                                        - label_20: QLabel
                                            - tab_tabular: QWidget
                                                - (Layout): QGridLayout
                                                        - tabWidget_table_values: QTabWidget
                                                            - tab_mass_table: QWidget
                                                                - (Layout): QGridLayout
                                                                        - label_143: QLabel
                                                                        - label_152: QLabel
                                                                        - label_153: QLabel
                                                                        - pushButton_load_Mz_table: QPushButton
                                                                        - label_150: QLabel
                                                                        - pushButton_load_My_table: QPushButton
                                                                        - lineEdit_Jx_table_path: QLineEdit
                                                                        - pushButton_load_Jx_table: QPushButton
                                                                        - lineEdit_Jy_table_path: QLineEdit
                                                                        - pushButton_load_Jy_table: QPushButton
                                                                        - pushButton_load_Jz_table: QPushButton
                                                                        - lineEdit_Mx_table_path: QLineEdit
                                                                        - lineEdit_Jz_table_path: QLineEdit
                                                                        - label_151: QLabel
                                                                        - lineEdit_My_table_path: QLineEdit
                                                                        - lineEdit_Mz_table_path: QLineEdit
                                                                        - pushButton_load_Mx_table: QPushButton
                                                                        - label_146: QLabel
                                                            - tab_stiffness_table: QWidget
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_Kx_table_path: QLineEdit
                                                                        - pushButton_load_Kx_table: QPushButton
                                                                        - label_117: QLabel
                                                                        - pushButton_load_Ky_table: QPushButton
                                                                        - pushButton_load_Kz_table: QPushButton
                                                                        - lineEdit_Kz_table_path: QLineEdit
                                                                        - pushButton_load_Krx_table: QPushButton
                                                                        - label_118: QLabel
                                                                        - lineEdit_Ky_table_path: QLineEdit
                                                                        - label_132: QLabel
                                                                        - pushButton_load_Kry_table: QPushButton
                                                                        - label_119: QLabel
                                                                        - label_135: QLabel
                                                                        - lineEdit_Krz_table_path: QLineEdit
                                                                        - pushButton_load_Krz_table: QPushButton
                                                                        - label_134: QLabel
                                                                        - lineEdit_Krx_table_path: QLineEdit
                                                                        - lineEdit_Kry_table_path: QLineEdit
                                                            - tab_damping_table: QWidget
                                                                - (Layout): QGridLayout
                                                                        - label_138: QLabel
                                                                        - lineEdit_Cx_table_path: QLineEdit
                                                                        - pushButton_load_Cx_table: QPushButton
                                                                        - label_133: QLabel
                                                                        - label_136: QLabel
                                                                        - lineEdit_Cy_table_path: QLineEdit
                                                                        - pushButton_load_Cy_table: QPushButton
                                                                        - lineEdit_Cz_table_path: QLineEdit
                                                                        - pushButton_load_Cz_table: QPushButton
                                                                        - pushButton_load_Crx_table: QPushButton
                                                                        - label_139: QLabel
                                                                        - lineEdit_Cry_table_path: QLineEdit
                                                                        - label_137: QLabel
                                                                        - lineEdit_Crx_table_path: QLineEdit
                                                                        - pushButton_load_Cry_table: QPushButton
                                                                        - label_120: QLabel
                                                                        - pushButton_load_Crz_table: QPushButton
                                                                        - lineEdit_Crz_table_path: QLineEdit
                                            - tab_list: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_2: QFrame
                                                            - (Layout): QGridLayout
                                                                    - tabWidget_remove: QTabWidget
                                                                        - tab_multiple_remove: QWidget
                                                                            - (Layout): QGridLayout
                                                                                    - checkBox_remove_stiffness: QCheckBox
                                                                                    - checkBox_remove_mass: QCheckBox
                                                                                    - checkBox_remove_damping: QCheckBox
                                                                        - tab_mass_remove: QWidget
                                                                            - (Layout): QGridLayout
                                                                                    - treeWidget_mass: QTreeWidget
                                                                        - tab_stiffness_remove: QWidget
                                                                            - (Layout): QGridLayout
                                                                                    - treeWidget_stiffness: QTreeWidget
                                                                        - tab_damping_remove: QWidget
                                                                            - (Layout): QGridLayout
                                                                                    - treeWidget_damping: QTreeWidget
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
