# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'elastic_nodal_links_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 540)
        Dialog.setMinimumSize(QSize(460, 540))
        Dialog.setMaximumSize(QSize(460, 540))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(1600, 48))
        self.top_frame.setFrameShape(QFrame.Box)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout_22 = QGridLayout(self.top_frame)
        self.gridLayout_22.setSpacing(0)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_22.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        self.main_frame = QFrame(Dialog)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1600, 1600))
        self.main_frame.setFrameShape(QFrame.Box)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.main_frame)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 80))
        self.selection_frame.setMaximumSize(QSize(16777215, 140))
        self.selection_frame.setFrameShape(QFrame.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_31 = QGridLayout(self.selection_frame)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setHorizontalSpacing(6)
        self.gridLayout_31.setVerticalSpacing(4)
        self.gridLayout_31.setContentsMargins(4, 4, 4, 4)
        self.label_first_node_id = QLabel(self.selection_frame)
        self.label_first_node_id.setObjectName(u"label_first_node_id")
        self.label_first_node_id.setMinimumSize(QSize(90, 26))
        self.label_first_node_id.setMaximumSize(QSize(100, 26))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_first_node_id.setFont(font1)
        self.label_first_node_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_31.addWidget(self.label_first_node_id, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)

        self.lineEdit_first_node_id = QLineEdit(self.selection_frame)
        self.lineEdit_first_node_id.setObjectName(u"lineEdit_first_node_id")
        self.lineEdit_first_node_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_first_node_id.setMaximumSize(QSize(100, 26))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setKerning(False)
        self.lineEdit_first_node_id.setFont(font2)
        self.lineEdit_first_node_id.setTabletTracking(False)
        self.lineEdit_first_node_id.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_first_node_id.setStyleSheet(u"")
        self.lineEdit_first_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_31.addWidget(self.lineEdit_first_node_id, 0, 2, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_10, 0, 0, 1, 1)

        self.label_last_node_id = QLabel(self.selection_frame)
        self.label_last_node_id.setObjectName(u"label_last_node_id")
        self.label_last_node_id.setMinimumSize(QSize(90, 26))
        self.label_last_node_id.setMaximumSize(QSize(100, 26))
        self.label_last_node_id.setFont(font1)
        self.label_last_node_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_31.addWidget(self.label_last_node_id, 1, 1, 1, 1)

        self.lineEdit_last_node_id = QLineEdit(self.selection_frame)
        self.lineEdit_last_node_id.setObjectName(u"lineEdit_last_node_id")
        self.lineEdit_last_node_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_last_node_id.setMaximumSize(QSize(100, 26))
        self.lineEdit_last_node_id.setFont(font2)
        self.lineEdit_last_node_id.setTabletTracking(False)
        self.lineEdit_last_node_id.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_last_node_id.setStyleSheet(u"")
        self.lineEdit_last_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_31.addWidget(self.lineEdit_last_node_id, 1, 2, 1, 1)


        self.gridLayout_12.addWidget(self.selection_frame, 0, 1, 2, 1)

        self.frame_tabWidgets = QFrame(self.main_frame)
        self.frame_tabWidgets.setObjectName(u"frame_tabWidgets")
        self.frame_tabWidgets.setMinimumSize(QSize(400, 300))
        self.frame_tabWidgets.setFrameShape(QFrame.NoFrame)
        self.frame_tabWidgets.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_tabWidgets)
        self.gridLayout_14.setSpacing(4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(8, 4, 8, 4)
        self.tabWidget_main = QTabWidget(self.frame_tabWidgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(482, 700))
        font3 = QFont()
        font3.setPointSize(10)
        self.tabWidget_main.setFont(font3)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_15 = QGridLayout(self.tab_setup)
        self.gridLayout_15.setSpacing(4)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_inputs = QTabWidget(self.tab_setup)
        self.tabWidget_inputs.setObjectName(u"tabWidget_inputs")
        self.tabWidget_inputs.setMinimumSize(QSize(380, 0))
        self.tabWidget_inputs.setMaximumSize(QSize(420, 400))
        self.tabWidget_inputs.setSizeIncrement(QSize(0, 0))
        self.tabWidget_inputs.setFont(font3)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_18 = QGridLayout(self.tab_constant_values)
        self.gridLayout_18.setSpacing(4)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(4, 6, 4, 6)
        self.tabWidget_constant_values = QTabWidget(self.tab_constant_values)
        self.tabWidget_constant_values.setObjectName(u"tabWidget_constant_values")
        self.tabWidget_constant_values.setFont(font3)
        self.tab_spring_constant = QWidget()
        self.tab_spring_constant.setObjectName(u"tab_spring_constant")
        self.gridLayout_23 = QGridLayout(self.tab_spring_constant)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.lineEdit_Krx = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Krx.setObjectName(u"lineEdit_Krx")
        self.lineEdit_Krx.setEnabled(True)
        self.lineEdit_Krx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Krx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Krx.setFont(font3)
        self.lineEdit_Krx.setStyleSheet(u"")
        self.lineEdit_Krx.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Krx, 3, 2, 1, 1)

        self.label_16 = QLabel(self.tab_spring_constant)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(80, 26))
        self.label_16.setMaximumSize(QSize(80, 26))
        self.label_16.setFont(font3)
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_16, 0, 3, 1, 1)

        self.lineEdit_Ky = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Ky.setObjectName(u"lineEdit_Ky")
        self.lineEdit_Ky.setEnabled(True)
        self.lineEdit_Ky.setMinimumSize(QSize(120, 26))
        self.lineEdit_Ky.setMaximumSize(QSize(120, 26))
        self.lineEdit_Ky.setFont(font3)
        self.lineEdit_Ky.setStyleSheet(u"")
        self.lineEdit_Ky.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Ky, 1, 2, 1, 1)

        self.label_115 = QLabel(self.tab_spring_constant)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setEnabled(True)
        self.label_115.setMinimumSize(QSize(70, 26))
        self.label_115.setMaximumSize(QSize(70, 26))
        self.label_115.setFont(font3)
        self.label_115.setMouseTracking(True)
        self.label_115.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_115, 0, 1, 1, 1)

        self.label_93 = QLabel(self.tab_spring_constant)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setEnabled(True)
        self.label_93.setMinimumSize(QSize(70, 26))
        self.label_93.setMaximumSize(QSize(70, 26))
        self.label_93.setFont(font3)
        self.label_93.setMouseTracking(True)
        self.label_93.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_93, 3, 1, 1, 1)

        self.label_113 = QLabel(self.tab_spring_constant)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setMinimumSize(QSize(80, 26))
        self.label_113.setMaximumSize(QSize(80, 26))
        self.label_113.setFont(font3)
        self.label_113.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_113, 3, 3, 1, 1)

        self.label_116 = QLabel(self.tab_spring_constant)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setEnabled(True)
        self.label_116.setMinimumSize(QSize(70, 26))
        self.label_116.setMaximumSize(QSize(70, 26))
        self.label_116.setFont(font3)
        self.label_116.setMouseTracking(True)
        self.label_116.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_116, 1, 1, 1, 1)

        self.label_123 = QLabel(self.tab_spring_constant)
        self.label_123.setObjectName(u"label_123")
        self.label_123.setEnabled(True)
        self.label_123.setMinimumSize(QSize(70, 26))
        self.label_123.setMaximumSize(QSize(70, 26))
        self.label_123.setFont(font3)
        self.label_123.setMouseTracking(True)
        self.label_123.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_123, 2, 1, 1, 1)

        self.lineEdit_Kz = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Kz.setObjectName(u"lineEdit_Kz")
        self.lineEdit_Kz.setEnabled(True)
        self.lineEdit_Kz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kz.setFont(font3)
        self.lineEdit_Kz.setStyleSheet(u"")
        self.lineEdit_Kz.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kz, 2, 2, 1, 1)

        self.label_18 = QLabel(self.tab_spring_constant)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(80, 26))
        self.label_18.setMaximumSize(QSize(80, 26))
        self.label_18.setFont(font3)
        self.label_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_18, 2, 3, 1, 1)

        self.label_112 = QLabel(self.tab_spring_constant)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(70, 26))
        self.label_112.setMaximumSize(QSize(70, 26))
        self.label_112.setFont(font3)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_112, 4, 1, 1, 1)

        self.label_114 = QLabel(self.tab_spring_constant)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setMinimumSize(QSize(80, 26))
        self.label_114.setMaximumSize(QSize(80, 26))
        self.label_114.setFont(font3)
        self.label_114.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_114, 4, 3, 1, 1)

        self.lineEdit_Krz = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Krz.setObjectName(u"lineEdit_Krz")
        self.lineEdit_Krz.setEnabled(True)
        self.lineEdit_Krz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Krz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Krz.setFont(font3)
        self.lineEdit_Krz.setStyleSheet(u"")
        self.lineEdit_Krz.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Krz, 5, 2, 1, 1)

        self.label_122 = QLabel(self.tab_spring_constant)
        self.label_122.setObjectName(u"label_122")
        self.label_122.setMinimumSize(QSize(80, 26))
        self.label_122.setMaximumSize(QSize(80, 26))
        self.label_122.setFont(font3)
        self.label_122.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_122, 5, 3, 1, 1)

        self.label_17 = QLabel(self.tab_spring_constant)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(80, 26))
        self.label_17.setMaximumSize(QSize(80, 26))
        self.label_17.setFont(font3)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_17, 1, 3, 1, 1)

        self.lineEdit_Kx = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Kx.setObjectName(u"lineEdit_Kx")
        self.lineEdit_Kx.setEnabled(True)
        self.lineEdit_Kx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kx.setFont(font3)
        self.lineEdit_Kx.setStyleSheet(u"")
        self.lineEdit_Kx.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kx, 0, 2, 1, 1)

        self.lineEdit_Kry = QLineEdit(self.tab_spring_constant)
        self.lineEdit_Kry.setObjectName(u"lineEdit_Kry")
        self.lineEdit_Kry.setEnabled(True)
        self.lineEdit_Kry.setMinimumSize(QSize(120, 26))
        self.lineEdit_Kry.setMaximumSize(QSize(120, 26))
        self.lineEdit_Kry.setFont(font3)
        self.lineEdit_Kry.setStyleSheet(u"")
        self.lineEdit_Kry.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_Kry, 4, 2, 1, 1)

        self.label_121 = QLabel(self.tab_spring_constant)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setEnabled(True)
        self.label_121.setMinimumSize(QSize(70, 26))
        self.label_121.setMaximumSize(QSize(70, 26))
        self.label_121.setFont(font3)
        self.label_121.setMouseTracking(True)
        self.label_121.setAlignment(Qt.AlignCenter)

        self.gridLayout_23.addWidget(self.label_121, 5, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_14, 0, 4, 1, 1)

        self.tabWidget_constant_values.addTab(self.tab_spring_constant, "")
        self.tab_damper_constant = QWidget()
        self.tab_damper_constant.setObjectName(u"tab_damper_constant")
        self.gridLayout_24 = QGridLayout(self.tab_damper_constant)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_17, 0, 0, 1, 1)

        self.lineEdit_Crz = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Crz.setObjectName(u"lineEdit_Crz")
        self.lineEdit_Crz.setEnabled(True)
        self.lineEdit_Crz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Crz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Crz.setFont(font3)
        self.lineEdit_Crz.setStyleSheet(u"")
        self.lineEdit_Crz.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Crz, 5, 2, 1, 1)

        self.label_131 = QLabel(self.tab_damper_constant)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setMinimumSize(QSize(80, 26))
        self.label_131.setMaximumSize(QSize(80, 26))
        self.label_131.setFont(font3)
        self.label_131.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_131, 5, 3, 1, 1)

        self.label_126 = QLabel(self.tab_damper_constant)
        self.label_126.setObjectName(u"label_126")
        self.label_126.setEnabled(True)
        self.label_126.setMinimumSize(QSize(70, 26))
        self.label_126.setMaximumSize(QSize(70, 26))
        self.label_126.setFont(font3)
        self.label_126.setMouseTracking(True)
        self.label_126.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_126, 5, 1, 1, 1)

        self.label_128 = QLabel(self.tab_damper_constant)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setEnabled(True)
        self.label_128.setMinimumSize(QSize(70, 26))
        self.label_128.setMaximumSize(QSize(70, 26))
        self.label_128.setFont(font3)
        self.label_128.setMouseTracking(True)
        self.label_128.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_128, 1, 1, 1, 1)

        self.lineEdit_Cy = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Cy.setObjectName(u"lineEdit_Cy")
        self.lineEdit_Cy.setEnabled(True)
        self.lineEdit_Cy.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cy.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cy.setFont(font3)
        self.lineEdit_Cy.setStyleSheet(u"")
        self.lineEdit_Cy.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cy, 1, 2, 1, 1)

        self.lineEdit_Cz = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Cz.setObjectName(u"lineEdit_Cz")
        self.lineEdit_Cz.setEnabled(True)
        self.lineEdit_Cz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cz.setFont(font3)
        self.lineEdit_Cz.setStyleSheet(u"")
        self.lineEdit_Cz.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cz, 2, 2, 1, 1)

        self.label_102 = QLabel(self.tab_damper_constant)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setEnabled(True)
        self.label_102.setMinimumSize(QSize(70, 26))
        self.label_102.setMaximumSize(QSize(70, 26))
        self.label_102.setFont(font3)
        self.label_102.setMouseTracking(True)
        self.label_102.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_102, 3, 1, 1, 1)

        self.label_19 = QLabel(self.tab_damper_constant)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(80, 26))
        self.label_19.setMaximumSize(QSize(80, 26))
        self.label_19.setFont(font3)
        self.label_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_19, 2, 3, 1, 1)

        self.label_21 = QLabel(self.tab_damper_constant)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 26))
        self.label_21.setMaximumSize(QSize(80, 26))
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_21, 1, 3, 1, 1)

        self.lineEdit_Crx = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Crx.setObjectName(u"lineEdit_Crx")
        self.lineEdit_Crx.setEnabled(True)
        self.lineEdit_Crx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Crx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Crx.setFont(font3)
        self.lineEdit_Crx.setStyleSheet(u"")
        self.lineEdit_Crx.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Crx, 3, 2, 1, 1)

        self.label_127 = QLabel(self.tab_damper_constant)
        self.label_127.setObjectName(u"label_127")
        self.label_127.setEnabled(True)
        self.label_127.setMinimumSize(QSize(70, 26))
        self.label_127.setMaximumSize(QSize(70, 26))
        self.label_127.setFont(font3)
        self.label_127.setMouseTracking(True)
        self.label_127.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_127, 2, 1, 1, 1)

        self.label_125 = QLabel(self.tab_damper_constant)
        self.label_125.setObjectName(u"label_125")
        self.label_125.setEnabled(True)
        self.label_125.setMinimumSize(QSize(70, 26))
        self.label_125.setMaximumSize(QSize(70, 26))
        self.label_125.setFont(font3)
        self.label_125.setMouseTracking(True)
        self.label_125.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_125, 4, 1, 1, 1)

        self.label_130 = QLabel(self.tab_damper_constant)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setMinimumSize(QSize(80, 26))
        self.label_130.setMaximumSize(QSize(80, 26))
        self.label_130.setFont(font3)
        self.label_130.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_130, 3, 3, 1, 1)

        self.label_124 = QLabel(self.tab_damper_constant)
        self.label_124.setObjectName(u"label_124")
        self.label_124.setMinimumSize(QSize(80, 26))
        self.label_124.setMaximumSize(QSize(80, 26))
        self.label_124.setFont(font3)
        self.label_124.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_124, 4, 3, 1, 1)

        self.lineEdit_Cry = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Cry.setObjectName(u"lineEdit_Cry")
        self.lineEdit_Cry.setEnabled(True)
        self.lineEdit_Cry.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cry.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cry.setFont(font3)
        self.lineEdit_Cry.setStyleSheet(u"")
        self.lineEdit_Cry.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cry, 4, 2, 1, 1)

        self.label_129 = QLabel(self.tab_damper_constant)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setEnabled(True)
        self.label_129.setMinimumSize(QSize(70, 26))
        self.label_129.setMaximumSize(QSize(70, 26))
        self.label_129.setFont(font3)
        self.label_129.setMouseTracking(True)
        self.label_129.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.label_129, 0, 1, 1, 1)

        self.lineEdit_Cx = QLineEdit(self.tab_damper_constant)
        self.lineEdit_Cx.setObjectName(u"lineEdit_Cx")
        self.lineEdit_Cx.setEnabled(True)
        self.lineEdit_Cx.setMinimumSize(QSize(120, 26))
        self.lineEdit_Cx.setMaximumSize(QSize(120, 26))
        self.lineEdit_Cx.setFont(font3)
        self.lineEdit_Cx.setStyleSheet(u"")
        self.lineEdit_Cx.setAlignment(Qt.AlignCenter)

        self.gridLayout_24.addWidget(self.lineEdit_Cx, 0, 2, 1, 1)

        self.label_20 = QLabel(self.tab_damper_constant)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font3)
        self.label_20.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_24.addWidget(self.label_20, 0, 3, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer_18, 0, 4, 1, 1)

        self.tabWidget_constant_values.addTab(self.tab_damper_constant, "")

        self.gridLayout_18.addWidget(self.tabWidget_constant_values, 0, 0, 1, 2)

        self.tabWidget_inputs.addTab(self.tab_constant_values, "")
        self.tab_table_values = QWidget()
        self.tab_table_values.setObjectName(u"tab_table_values")
        self.gridLayout_19 = QGridLayout(self.tab_table_values)
        self.gridLayout_19.setSpacing(4)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(4, 6, 4, 6)
        self.tabWidget_table_values = QTabWidget(self.tab_table_values)
        self.tabWidget_table_values.setObjectName(u"tabWidget_table_values")
        self.tabWidget_table_values.setFont(font3)
        self.tab_spring_table = QWidget()
        self.tab_spring_table.setObjectName(u"tab_spring_table")
        self.gridLayout_25 = QGridLayout(self.tab_spring_table)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_path_table_Kx = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Kx.setObjectName(u"lineEdit_path_table_Kx")
        self.lineEdit_path_table_Kx.setEnabled(True)
        self.lineEdit_path_table_Kx.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Kx.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Kx.setSizeIncrement(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(9)
        self.lineEdit_path_table_Kx.setFont(font4)
        self.lineEdit_path_table_Kx.setStyleSheet(u"")
        self.lineEdit_path_table_Kx.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Kx, 0, 2, 1, 1)

        self.pushButton_load_Kx_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Kx_table.setObjectName(u"pushButton_load_Kx_table")
        self.pushButton_load_Kx_table.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kx_table.setFont(font3)
        self.pushButton_load_Kx_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kx_table, 0, 3, 1, 1)

        self.label_117 = QLabel(self.tab_spring_table)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setEnabled(True)
        self.label_117.setMinimumSize(QSize(30, 26))
        self.label_117.setMaximumSize(QSize(30, 26))
        self.label_117.setFont(font3)
        self.label_117.setMouseTracking(True)
        self.label_117.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_117, 0, 1, 1, 1)

        self.pushButton_load_Ky_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Ky_table.setObjectName(u"pushButton_load_Ky_table")
        self.pushButton_load_Ky_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Ky_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Ky_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Ky_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Ky_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Ky_table.setFont(font3)
        self.pushButton_load_Ky_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Ky_table, 1, 3, 1, 1)

        self.pushButton_load_Kz_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Kz_table.setObjectName(u"pushButton_load_Kz_table")
        self.pushButton_load_Kz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kz_table.setFont(font3)
        self.pushButton_load_Kz_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kz_table, 2, 3, 1, 1)

        self.lineEdit_path_table_Kz = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Kz.setObjectName(u"lineEdit_path_table_Kz")
        self.lineEdit_path_table_Kz.setEnabled(True)
        self.lineEdit_path_table_Kz.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Kz.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Kz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Kz.setFont(font4)
        self.lineEdit_path_table_Kz.setStyleSheet(u"")
        self.lineEdit_path_table_Kz.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Kz, 2, 2, 1, 1)

        self.pushButton_load_Krx_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Krx_table.setObjectName(u"pushButton_load_Krx_table")
        self.pushButton_load_Krx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Krx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Krx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Krx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Krx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Krx_table.setFont(font3)
        self.pushButton_load_Krx_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Krx_table, 3, 3, 1, 1)

        self.label_118 = QLabel(self.tab_spring_table)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setEnabled(True)
        self.label_118.setMinimumSize(QSize(30, 26))
        self.label_118.setMaximumSize(QSize(30, 26))
        self.label_118.setFont(font3)
        self.label_118.setMouseTracking(True)
        self.label_118.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_118, 4, 1, 1, 1)

        self.lineEdit_path_table_Ky = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Ky.setObjectName(u"lineEdit_path_table_Ky")
        self.lineEdit_path_table_Ky.setEnabled(True)
        self.lineEdit_path_table_Ky.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Ky.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Ky.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Ky.setFont(font4)
        self.lineEdit_path_table_Ky.setStyleSheet(u"")
        self.lineEdit_path_table_Ky.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Ky, 1, 2, 1, 1)

        self.label_132 = QLabel(self.tab_spring_table)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setEnabled(True)
        self.label_132.setMinimumSize(QSize(30, 26))
        self.label_132.setMaximumSize(QSize(30, 26))
        self.label_132.setFont(font3)
        self.label_132.setMouseTracking(True)
        self.label_132.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_132, 1, 1, 1, 1)

        self.pushButton_load_Kry_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Kry_table.setObjectName(u"pushButton_load_Kry_table")
        self.pushButton_load_Kry_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Kry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Kry_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Kry_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Kry_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Kry_table.setFont(font3)
        self.pushButton_load_Kry_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Kry_table, 4, 3, 1, 1)

        self.label_119 = QLabel(self.tab_spring_table)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setEnabled(True)
        self.label_119.setMinimumSize(QSize(30, 26))
        self.label_119.setMaximumSize(QSize(30, 26))
        self.label_119.setFont(font3)
        self.label_119.setMouseTracking(True)
        self.label_119.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_119, 5, 1, 1, 1)

        self.label_135 = QLabel(self.tab_spring_table)
        self.label_135.setObjectName(u"label_135")
        self.label_135.setEnabled(True)
        self.label_135.setMinimumSize(QSize(30, 26))
        self.label_135.setMaximumSize(QSize(30, 26))
        self.label_135.setFont(font3)
        self.label_135.setMouseTracking(True)
        self.label_135.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_135, 3, 1, 1, 1)

        self.lineEdit_path_table_Krz = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Krz.setObjectName(u"lineEdit_path_table_Krz")
        self.lineEdit_path_table_Krz.setEnabled(True)
        self.lineEdit_path_table_Krz.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Krz.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Krz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Krz.setFont(font4)
        self.lineEdit_path_table_Krz.setStyleSheet(u"")
        self.lineEdit_path_table_Krz.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Krz, 5, 2, 1, 1)

        self.pushButton_load_Krz_table = QPushButton(self.tab_spring_table)
        self.pushButton_load_Krz_table.setObjectName(u"pushButton_load_Krz_table")
        self.pushButton_load_Krz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Krz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Krz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Krz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Krz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Krz_table.setFont(font3)
        self.pushButton_load_Krz_table.setStyleSheet(u"")

        self.gridLayout_25.addWidget(self.pushButton_load_Krz_table, 5, 3, 1, 1)

        self.label_134 = QLabel(self.tab_spring_table)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setEnabled(True)
        self.label_134.setMinimumSize(QSize(30, 26))
        self.label_134.setMaximumSize(QSize(30, 26))
        self.label_134.setFont(font3)
        self.label_134.setMouseTracking(True)
        self.label_134.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.label_134, 2, 1, 1, 1)

        self.lineEdit_path_table_Krx = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Krx.setObjectName(u"lineEdit_path_table_Krx")
        self.lineEdit_path_table_Krx.setEnabled(True)
        self.lineEdit_path_table_Krx.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Krx.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Krx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Krx.setFont(font4)
        self.lineEdit_path_table_Krx.setStyleSheet(u"")
        self.lineEdit_path_table_Krx.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Krx, 3, 2, 1, 1)

        self.lineEdit_path_table_Kry = QLineEdit(self.tab_spring_table)
        self.lineEdit_path_table_Kry.setObjectName(u"lineEdit_path_table_Kry")
        self.lineEdit_path_table_Kry.setEnabled(True)
        self.lineEdit_path_table_Kry.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Kry.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Kry.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Kry.setFont(font4)
        self.lineEdit_path_table_Kry.setStyleSheet(u"")
        self.lineEdit_path_table_Kry.setAlignment(Qt.AlignCenter)

        self.gridLayout_25.addWidget(self.lineEdit_path_table_Kry, 4, 2, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_19, 0, 0, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_20, 0, 4, 1, 1)

        self.tabWidget_table_values.addTab(self.tab_spring_table, "")
        self.tab_damper_table = QWidget()
        self.tab_damper_table.setObjectName(u"tab_damper_table")
        self.gridLayout_17 = QGridLayout(self.tab_damper_table)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_21, 0, 4, 1, 1)

        self.label_138 = QLabel(self.tab_damper_table)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setEnabled(True)
        self.label_138.setMinimumSize(QSize(30, 26))
        self.label_138.setMaximumSize(QSize(30, 26))
        self.label_138.setFont(font3)
        self.label_138.setMouseTracking(True)
        self.label_138.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_138, 0, 1, 1, 1)

        self.lineEdit_path_table_Cx = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Cx.setObjectName(u"lineEdit_path_table_Cx")
        self.lineEdit_path_table_Cx.setEnabled(True)
        self.lineEdit_path_table_Cx.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Cx.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Cx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Cx.setFont(font4)
        self.lineEdit_path_table_Cx.setStyleSheet(u"")
        self.lineEdit_path_table_Cx.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Cx, 0, 2, 1, 1)

        self.pushButton_load_Cx_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Cx_table.setObjectName(u"pushButton_load_Cx_table")
        self.pushButton_load_Cx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cx_table.setFont(font3)
        self.pushButton_load_Cx_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cx_table, 0, 3, 1, 1)

        self.label_133 = QLabel(self.tab_damper_table)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setEnabled(True)
        self.label_133.setMinimumSize(QSize(30, 26))
        self.label_133.setMaximumSize(QSize(30, 26))
        self.label_133.setFont(font3)
        self.label_133.setMouseTracking(True)
        self.label_133.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_133, 1, 1, 1, 1)

        self.label_136 = QLabel(self.tab_damper_table)
        self.label_136.setObjectName(u"label_136")
        self.label_136.setEnabled(True)
        self.label_136.setMinimumSize(QSize(30, 26))
        self.label_136.setMaximumSize(QSize(30, 26))
        self.label_136.setFont(font3)
        self.label_136.setMouseTracking(True)
        self.label_136.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_136, 2, 1, 1, 1)

        self.lineEdit_path_table_Cy = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Cy.setObjectName(u"lineEdit_path_table_Cy")
        self.lineEdit_path_table_Cy.setEnabled(True)
        self.lineEdit_path_table_Cy.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Cy.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Cy.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Cy.setFont(font4)
        self.lineEdit_path_table_Cy.setStyleSheet(u"")
        self.lineEdit_path_table_Cy.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Cy, 1, 2, 1, 1)

        self.pushButton_load_Cy_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Cy_table.setObjectName(u"pushButton_load_Cy_table")
        self.pushButton_load_Cy_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cy_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cy_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cy_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cy_table.setFont(font3)
        self.pushButton_load_Cy_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cy_table, 1, 3, 1, 1)

        self.lineEdit_path_table_Cz = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Cz.setObjectName(u"lineEdit_path_table_Cz")
        self.lineEdit_path_table_Cz.setEnabled(True)
        self.lineEdit_path_table_Cz.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Cz.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Cz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Cz.setFont(font4)
        self.lineEdit_path_table_Cz.setStyleSheet(u"")
        self.lineEdit_path_table_Cz.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Cz, 2, 2, 1, 1)

        self.pushButton_load_Cz_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Cz_table.setObjectName(u"pushButton_load_Cz_table")
        self.pushButton_load_Cz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cz_table.setFont(font3)
        self.pushButton_load_Cz_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cz_table, 2, 3, 1, 1)

        self.pushButton_load_Crx_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Crx_table.setObjectName(u"pushButton_load_Crx_table")
        self.pushButton_load_Crx_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Crx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Crx_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Crx_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Crx_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Crx_table.setFont(font3)
        self.pushButton_load_Crx_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Crx_table, 3, 3, 1, 1)

        self.label_139 = QLabel(self.tab_damper_table)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setEnabled(True)
        self.label_139.setMinimumSize(QSize(30, 26))
        self.label_139.setMaximumSize(QSize(30, 26))
        self.label_139.setFont(font3)
        self.label_139.setMouseTracking(True)
        self.label_139.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_139, 4, 1, 1, 1)

        self.lineEdit_path_table_Cry = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Cry.setObjectName(u"lineEdit_path_table_Cry")
        self.lineEdit_path_table_Cry.setEnabled(True)
        self.lineEdit_path_table_Cry.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Cry.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Cry.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Cry.setFont(font4)
        self.lineEdit_path_table_Cry.setStyleSheet(u"")
        self.lineEdit_path_table_Cry.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Cry, 4, 2, 1, 1)

        self.label_137 = QLabel(self.tab_damper_table)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setEnabled(True)
        self.label_137.setMinimumSize(QSize(30, 26))
        self.label_137.setMaximumSize(QSize(30, 26))
        self.label_137.setFont(font3)
        self.label_137.setMouseTracking(True)
        self.label_137.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_137, 3, 1, 1, 1)

        self.lineEdit_path_table_Crx = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Crx.setObjectName(u"lineEdit_path_table_Crx")
        self.lineEdit_path_table_Crx.setEnabled(True)
        self.lineEdit_path_table_Crx.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Crx.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Crx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Crx.setFont(font4)
        self.lineEdit_path_table_Crx.setStyleSheet(u"")
        self.lineEdit_path_table_Crx.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Crx, 3, 2, 1, 1)

        self.pushButton_load_Cry_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Cry_table.setObjectName(u"pushButton_load_Cry_table")
        self.pushButton_load_Cry_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Cry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Cry_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Cry_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Cry_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Cry_table.setFont(font3)
        self.pushButton_load_Cry_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Cry_table, 4, 3, 1, 1)

        self.label_120 = QLabel(self.tab_damper_table)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setEnabled(True)
        self.label_120.setMinimumSize(QSize(30, 26))
        self.label_120.setMaximumSize(QSize(30, 26))
        self.label_120.setFont(font3)
        self.label_120.setMouseTracking(True)
        self.label_120.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.label_120, 5, 1, 1, 1)

        self.pushButton_load_Crz_table = QPushButton(self.tab_damper_table)
        self.pushButton_load_Crz_table.setObjectName(u"pushButton_load_Crz_table")
        self.pushButton_load_Crz_table.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_Crz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Crz_table.setSizePolicy(sizePolicy)
        self.pushButton_load_Crz_table.setMinimumSize(QSize(70, 26))
        self.pushButton_load_Crz_table.setMaximumSize(QSize(70, 16777215))
        self.pushButton_load_Crz_table.setFont(font3)
        self.pushButton_load_Crz_table.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.pushButton_load_Crz_table, 5, 3, 1, 1)

        self.lineEdit_path_table_Crz = QLineEdit(self.tab_damper_table)
        self.lineEdit_path_table_Crz.setObjectName(u"lineEdit_path_table_Crz")
        self.lineEdit_path_table_Crz.setEnabled(True)
        self.lineEdit_path_table_Crz.setMinimumSize(QSize(240, 26))
        self.lineEdit_path_table_Crz.setMaximumSize(QSize(250, 26))
        self.lineEdit_path_table_Crz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_path_table_Crz.setFont(font4)
        self.lineEdit_path_table_Crz.setStyleSheet(u"")
        self.lineEdit_path_table_Crz.setAlignment(Qt.AlignCenter)

        self.gridLayout_17.addWidget(self.lineEdit_path_table_Crz, 5, 2, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_22, 0, 0, 1, 1)

        self.tabWidget_table_values.addTab(self.tab_damper_table, "")

        self.gridLayout_19.addWidget(self.tabWidget_table_values, 0, 0, 1, 2)

        self.tabWidget_inputs.addTab(self.tab_table_values, "")

        self.gridLayout_15.addWidget(self.tabWidget_inputs, 0, 0, 1, 1)

        self.frame_confirm = QFrame(self.tab_setup)
        self.frame_confirm.setObjectName(u"frame_confirm")
        self.frame_confirm.setMinimumSize(QSize(0, 48))
        self.frame_confirm.setMaximumSize(QSize(16777215, 48))
        self.frame_confirm.setFrameShape(QFrame.NoFrame)
        self.frame_confirm.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_confirm)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_confirm)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)
        self.pushButton_attribute.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_confirm)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_confirm, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        font5 = QFont()
        font5.setFamilies([u"MS UI Gothic"])
        self.tab_remove.setFont(font5)
        self.gridLayout_20 = QGridLayout(self.tab_remove)
        self.gridLayout_20.setSpacing(4)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_remove = QTabWidget(self.tab_remove)
        self.tabWidget_remove.setObjectName(u"tabWidget_remove")
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        self.tabWidget_remove.setFont(font6)
        self.tab_multiple = QWidget()
        self.tab_multiple.setObjectName(u"tab_multiple")
        self.gridLayout_4 = QGridLayout(self.tab_multiple)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBox_link_dampings = QCheckBox(self.tab_multiple)
        self.checkBox_link_dampings.setObjectName(u"checkBox_link_dampings")
        self.checkBox_link_dampings.setMinimumSize(QSize(200, 26))
        self.checkBox_link_dampings.setMaximumSize(QSize(280, 26))
        self.checkBox_link_dampings.setFont(font3)
        self.checkBox_link_dampings.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_link_dampings, 1, 1, 1, 1)

        self.checkBox_link_stiffness = QCheckBox(self.tab_multiple)
        self.checkBox_link_stiffness.setObjectName(u"checkBox_link_stiffness")
        self.checkBox_link_stiffness.setMinimumSize(QSize(200, 26))
        self.checkBox_link_stiffness.setMaximumSize(QSize(280, 26))
        self.checkBox_link_stiffness.setFont(font3)
        self.checkBox_link_stiffness.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_link_stiffness, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.tabWidget_remove.addTab(self.tab_multiple, "")
        self.tab_stiffness_link = QWidget()
        self.tab_stiffness_link.setObjectName(u"tab_stiffness_link")
        self.gridLayout_2 = QGridLayout(self.tab_stiffness_link)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeWidget_structural_stiffness_links = QTreeWidget(self.tab_stiffness_link)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_structural_stiffness_links.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_structural_stiffness_links.setObjectName(u"treeWidget_structural_stiffness_links")
        self.treeWidget_structural_stiffness_links.setMinimumSize(QSize(320, 100))
        self.treeWidget_structural_stiffness_links.setMaximumSize(QSize(460, 260))
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(8)
        self.treeWidget_structural_stiffness_links.setFont(font7)
        self.treeWidget_structural_stiffness_links.setFrameShape(QFrame.StyledPanel)
        self.treeWidget_structural_stiffness_links.setFrameShadow(QFrame.Sunken)
        self.treeWidget_structural_stiffness_links.setIndentation(0)

        self.gridLayout_2.addWidget(self.treeWidget_structural_stiffness_links, 0, 0, 1, 1)

        self.tabWidget_remove.addTab(self.tab_stiffness_link, "")
        self.tab_dampings_link = QWidget()
        self.tab_dampings_link.setObjectName(u"tab_dampings_link")
        self.gridLayout_3 = QGridLayout(self.tab_dampings_link)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.treeWidget_structural_damping_links = QTreeWidget(self.tab_dampings_link)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_structural_damping_links.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_structural_damping_links.setObjectName(u"treeWidget_structural_damping_links")
        self.treeWidget_structural_damping_links.setMinimumSize(QSize(320, 100))
        self.treeWidget_structural_damping_links.setMaximumSize(QSize(460, 260))
        self.treeWidget_structural_damping_links.setFont(font7)
        self.treeWidget_structural_damping_links.setFrameShape(QFrame.StyledPanel)
        self.treeWidget_structural_damping_links.setFrameShadow(QFrame.Sunken)
        self.treeWidget_structural_damping_links.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_structural_damping_links, 0, 0, 1, 1)

        self.tabWidget_remove.addTab(self.tab_dampings_link, "")

        self.gridLayout_20.addWidget(self.tabWidget_remove, 0, 0, 1, 1)

        self.frame_buttons_2 = QFrame(self.tab_remove)
        self.frame_buttons_2.setObjectName(u"frame_buttons_2")
        self.frame_buttons_2.setMinimumSize(QSize(0, 48))
        self.frame_buttons_2.setMaximumSize(QSize(16777215, 48))
        font8 = QFont()
        font8.setFamilies([u"MS Shell Dlg 2"])
        self.frame_buttons_2.setFont(font8)
        self.frame_buttons_2.setFrameShape(QFrame.NoFrame)
        self.frame_buttons_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_buttons_2)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame_buttons_2)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_21.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_buttons_2)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_21.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_20.addWidget(self.frame_buttons_2, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_14.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_tabWidgets, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_first_node_id, self.lineEdit_last_node_id)
        QWidget.setTabOrder(self.lineEdit_last_node_id, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.tabWidget_inputs)
        QWidget.setTabOrder(self.tabWidget_inputs, self.tabWidget_constant_values)
        QWidget.setTabOrder(self.tabWidget_constant_values, self.lineEdit_Kx)
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
        QWidget.setTabOrder(self.lineEdit_Crz, self.tabWidget_table_values)
        QWidget.setTabOrder(self.tabWidget_table_values, self.lineEdit_path_table_Kx)
        QWidget.setTabOrder(self.lineEdit_path_table_Kx, self.pushButton_load_Kx_table)
        QWidget.setTabOrder(self.pushButton_load_Kx_table, self.lineEdit_path_table_Ky)
        QWidget.setTabOrder(self.lineEdit_path_table_Ky, self.pushButton_load_Ky_table)
        QWidget.setTabOrder(self.pushButton_load_Ky_table, self.lineEdit_path_table_Kz)
        QWidget.setTabOrder(self.lineEdit_path_table_Kz, self.pushButton_load_Kz_table)
        QWidget.setTabOrder(self.pushButton_load_Kz_table, self.lineEdit_path_table_Krx)
        QWidget.setTabOrder(self.lineEdit_path_table_Krx, self.pushButton_load_Krx_table)
        QWidget.setTabOrder(self.pushButton_load_Krx_table, self.lineEdit_path_table_Kry)
        QWidget.setTabOrder(self.lineEdit_path_table_Kry, self.pushButton_load_Kry_table)
        QWidget.setTabOrder(self.pushButton_load_Kry_table, self.lineEdit_path_table_Krz)
        QWidget.setTabOrder(self.lineEdit_path_table_Krz, self.pushButton_load_Krz_table)
        QWidget.setTabOrder(self.pushButton_load_Krz_table, self.lineEdit_path_table_Cx)
        QWidget.setTabOrder(self.lineEdit_path_table_Cx, self.pushButton_load_Cx_table)
        QWidget.setTabOrder(self.pushButton_load_Cx_table, self.lineEdit_path_table_Cy)
        QWidget.setTabOrder(self.lineEdit_path_table_Cy, self.pushButton_load_Cy_table)
        QWidget.setTabOrder(self.pushButton_load_Cy_table, self.lineEdit_path_table_Cz)
        QWidget.setTabOrder(self.lineEdit_path_table_Cz, self.pushButton_load_Cz_table)
        QWidget.setTabOrder(self.pushButton_load_Cz_table, self.lineEdit_path_table_Crx)
        QWidget.setTabOrder(self.lineEdit_path_table_Crx, self.pushButton_load_Crx_table)
        QWidget.setTabOrder(self.pushButton_load_Crx_table, self.lineEdit_path_table_Cry)
        QWidget.setTabOrder(self.lineEdit_path_table_Cry, self.pushButton_load_Cry_table)
        QWidget.setTabOrder(self.pushButton_load_Cry_table, self.lineEdit_path_table_Crz)
        QWidget.setTabOrder(self.lineEdit_path_table_Crz, self.pushButton_load_Crz_table)
        QWidget.setTabOrder(self.pushButton_load_Crz_table, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.checkBox_link_stiffness)
        QWidget.setTabOrder(self.checkBox_link_stiffness, self.checkBox_link_dampings)
        QWidget.setTabOrder(self.checkBox_link_dampings, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.tabWidget_remove)
        QWidget.setTabOrder(self.tabWidget_remove, self.treeWidget_structural_stiffness_links)
        QWidget.setTabOrder(self.treeWidget_structural_stiffness_links, self.treeWidget_structural_damping_links)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_inputs.setCurrentIndex(0)
        self.tabWidget_constant_values.setCurrentIndex(0)
        self.tabWidget_table_values.setCurrentIndex(1)
        self.pushButton_attribute.setDefault(True)
        self.pushButton_exit.setDefault(False)
        self.tabWidget_remove.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Elastic nodal links configuration", None))
        self.label_first_node_id.setText(QCoreApplication.translate("Dialog", u"First node id:", None))
        self.label_last_node_id.setText(QCoreApplication.translate("Dialog", u"Last node id:", None))
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
        self.tabWidget_constant_values.setTabText(self.tabWidget_constant_values.indexOf(self.tab_spring_constant), QCoreApplication.translate("Dialog", u"Spring", None))
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
        self.tabWidget_constant_values.setTabText(self.tabWidget_constant_values.indexOf(self.tab_damper_constant), QCoreApplication.translate("Dialog", u"Damper", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
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
        self.tabWidget_table_values.setTabText(self.tabWidget_table_values.indexOf(self.tab_spring_table), QCoreApplication.translate("Dialog", u"Spring", None))
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
        self.tabWidget_table_values.setTabText(self.tabWidget_table_values.indexOf(self.tab_damper_table), QCoreApplication.translate("Dialog", u"Damper", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_table_values), QCoreApplication.translate("Dialog", u"Table of values", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.checkBox_link_dampings.setText(QCoreApplication.translate("Dialog", u"Stiffness dampings (translational/torsional)", None))
        self.checkBox_link_stiffness.setText(QCoreApplication.translate("Dialog", u"Stiffness link (translational/torsional)", None))
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_multiple), QCoreApplication.translate("Dialog", u"Multiple", None))
        ___qtreewidgetitem = self.treeWidget_structural_stiffness_links.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Active parameters", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Linked nodes", None));
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_stiffness_link), QCoreApplication.translate("Dialog", u"Stiffness link", None))
        ___qtreewidgetitem1 = self.treeWidget_structural_damping_links.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"Active parameters", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Linked nodes", None));
        self.tabWidget_remove.setTabText(self.tabWidget_remove.indexOf(self.tab_dampings_link), QCoreApplication.translate("Dialog", u"Dampings link", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
    # retranslateUi



class ElasticNodalLinksInput_UI(QDialog, Ui_Dialog):
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
                                        - lineEdit_first_node_id: QLineEdit
                                        - label_last_node_id: QLabel
                                        - lineEdit_last_node_id: QLineEdit
                            - frame_tabWidgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_main: QTabWidget
                                            - tab_setup: QWidget
                                                - (Layout): QGridLayout
                                                        - tabWidget_inputs: QTabWidget
                                                            - tab_constant_values: QWidget
                                                                - (Layout): QGridLayout
                                                                        - tabWidget_constant_values: QTabWidget
                                                                            - tab_spring_constant: QWidget
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
                                                                            - tab_damper_constant: QWidget
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
                                                            - tab_table_values: QWidget
                                                                - (Layout): QGridLayout
                                                                        - tabWidget_table_values: QTabWidget
                                                                            - tab_spring_table: QWidget
                                                                                - (Layout): QGridLayout
                                                                                        - lineEdit_path_table_Kx: QLineEdit
                                                                                        - pushButton_load_Kx_table: QPushButton
                                                                                        - label_117: QLabel
                                                                                        - pushButton_load_Ky_table: QPushButton
                                                                                        - pushButton_load_Kz_table: QPushButton
                                                                                        - lineEdit_path_table_Kz: QLineEdit
                                                                                        - pushButton_load_Krx_table: QPushButton
                                                                                        - label_118: QLabel
                                                                                        - lineEdit_path_table_Ky: QLineEdit
                                                                                        - label_132: QLabel
                                                                                        - pushButton_load_Kry_table: QPushButton
                                                                                        - label_119: QLabel
                                                                                        - label_135: QLabel
                                                                                        - lineEdit_path_table_Krz: QLineEdit
                                                                                        - pushButton_load_Krz_table: QPushButton
                                                                                        - label_134: QLabel
                                                                                        - lineEdit_path_table_Krx: QLineEdit
                                                                                        - lineEdit_path_table_Kry: QLineEdit
                                                                            - tab_damper_table: QWidget
                                                                                - (Layout): QGridLayout
                                                                                        - label_138: QLabel
                                                                                        - lineEdit_path_table_Cx: QLineEdit
                                                                                        - pushButton_load_Cx_table: QPushButton
                                                                                        - label_133: QLabel
                                                                                        - label_136: QLabel
                                                                                        - lineEdit_path_table_Cy: QLineEdit
                                                                                        - pushButton_load_Cy_table: QPushButton
                                                                                        - lineEdit_path_table_Cz: QLineEdit
                                                                                        - pushButton_load_Cz_table: QPushButton
                                                                                        - pushButton_load_Crx_table: QPushButton
                                                                                        - label_139: QLabel
                                                                                        - lineEdit_path_table_Cry: QLineEdit
                                                                                        - label_137: QLabel
                                                                                        - lineEdit_path_table_Crx: QLineEdit
                                                                                        - pushButton_load_Cry_table: QPushButton
                                                                                        - label_120: QLabel
                                                                                        - pushButton_load_Crz_table: QPushButton
                                                                                        - lineEdit_path_table_Crz: QLineEdit
                                                        - frame_confirm: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_attribute: QPushButton
                                                                    - pushButton_exit: QPushButton
                                            - tab_remove: QWidget
                                                - (Layout): QGridLayout
                                                        - tabWidget_remove: QTabWidget
                                                            - tab_multiple: QWidget
                                                                - (Layout): QGridLayout
                                                                        - checkBox_link_dampings: QCheckBox
                                                                        - checkBox_link_stiffness: QCheckBox
                                                            - tab_stiffness_link: QWidget
                                                                - (Layout): QGridLayout
                                                                        - treeWidget_structural_stiffness_links: QTreeWidget
                                                            - tab_dampings_link: QWidget
                                                                - (Layout): QGridLayout
                                                                        - treeWidget_structural_damping_links: QTreeWidget
                                                        - frame_buttons_2: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_reset: QPushButton
                                                                    - pushButton_remove: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
