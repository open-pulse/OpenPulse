# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cross_section_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(654, 536)
        Form.setMinimumSize(QSize(600, 500))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget_general = QTabWidget(Form)
        self.tabWidget_general.setObjectName(u"tabWidget_general")
        self.tabWidget_general.setMinimumSize(QSize(566, 475))
        self.tabWidget_general.setMaximumSize(QSize(620, 500))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.tabWidget_general.setFont(font)
        self.tabWidget_general.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabWidget_general.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget_general.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget_general.setDocumentMode(False)
        self.tabWidget_general.setTabsClosable(False)
        self.tabWidget_general.setMovable(False)
        self.tabWidget_general.setTabBarAutoHide(False)
        self.tab_pipe = QWidget()
        self.tab_pipe.setObjectName(u"tab_pipe")
        self.gridLayout_4 = QGridLayout(self.tab_pipe)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 4)
        self.bottom_frame_buttons = QFrame(self.tab_pipe)
        self.bottom_frame_buttons.setObjectName(u"bottom_frame_buttons")
        self.bottom_frame_buttons.setMinimumSize(QSize(0, 52))
        self.bottom_frame_buttons.setMaximumSize(QSize(16777215, 52))
        self.bottom_frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom_frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.bottom_frame_buttons)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.pushButton_confirm_pipe = QPushButton(self.bottom_frame_buttons)
        self.pushButton_confirm_pipe.setObjectName(u"pushButton_confirm_pipe")
        self.pushButton_confirm_pipe.setMinimumSize(QSize(140, 32))
        self.pushButton_confirm_pipe.setMaximumSize(QSize(140, 32))
        self.pushButton_confirm_pipe.setFont(font)
        self.pushButton_confirm_pipe.setStyleSheet(u"")
        self.pushButton_confirm_pipe.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_confirm_pipe, 0, 3, 1, 1)

        self.pushButton_exit_pipe = QPushButton(self.bottom_frame_buttons)
        self.pushButton_exit_pipe.setObjectName(u"pushButton_exit_pipe")
        self.pushButton_exit_pipe.setMinimumSize(QSize(140, 32))
        self.pushButton_exit_pipe.setMaximumSize(QSize(140, 32))
        self.pushButton_exit_pipe.setFont(font)
        self.pushButton_exit_pipe.setStyleSheet(u"")
        self.pushButton_exit_pipe.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_exit_pipe, 0, 0, 1, 1)

        self.pushButton_plot_pipe_cross_section = QPushButton(self.bottom_frame_buttons)
        self.pushButton_plot_pipe_cross_section.setObjectName(u"pushButton_plot_pipe_cross_section")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_plot_pipe_cross_section.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_pipe_cross_section.setSizePolicy(sizePolicy)
        self.pushButton_plot_pipe_cross_section.setMinimumSize(QSize(140, 32))
        self.pushButton_plot_pipe_cross_section.setMaximumSize(QSize(140, 32))
        self.pushButton_plot_pipe_cross_section.setFont(font)
        self.pushButton_plot_pipe_cross_section.setStyleSheet(u"")
        self.pushButton_plot_pipe_cross_section.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_plot_pipe_cross_section, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.bottom_frame_buttons, 1, 0, 1, 2)

        self.tabWidget_pipe_section = QTabWidget(self.tab_pipe)
        self.tabWidget_pipe_section.setObjectName(u"tabWidget_pipe_section")
        self.tabWidget_pipe_section.setMinimumSize(QSize(556, 380))
        self.tabWidget_pipe_section.setMaximumSize(QSize(600, 400))
        self.tabWidget_pipe_section.setFont(font)
        self.tab_constant_pipe_section = QWidget()
        self.tab_constant_pipe_section.setObjectName(u"tab_constant_pipe_section")
        self.gridLayout_32 = QGridLayout(self.tab_constant_pipe_section)
        self.gridLayout_32.setSpacing(4)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(4, 4, 4, 4)
        self.frame_31 = QFrame(self.tab_constant_pipe_section)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMinimumSize(QSize(0, 52))
        self.frame_31.setMaximumSize(QSize(16777215, 52))
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_31)
        self.gridLayout_31.setSpacing(4)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(4, 4, 4, 4)
        self.pushButton_select_standard_section = QPushButton(self.frame_31)
        self.pushButton_select_standard_section.setObjectName(u"pushButton_select_standard_section")
        self.pushButton_select_standard_section.setMinimumSize(QSize(220, 32))
        self.pushButton_select_standard_section.setMaximumSize(QSize(220, 32))
        self.pushButton_select_standard_section.setFont(font)
        self.pushButton_select_standard_section.setStyleSheet(u"")

        self.gridLayout_31.addWidget(self.pushButton_select_standard_section, 0, 0, 1, 1)

        self.pushButton_check_if_section_is_normalized = QPushButton(self.frame_31)
        self.pushButton_check_if_section_is_normalized.setObjectName(u"pushButton_check_if_section_is_normalized")
        self.pushButton_check_if_section_is_normalized.setMinimumSize(QSize(220, 32))
        self.pushButton_check_if_section_is_normalized.setMaximumSize(QSize(220, 32))
        self.pushButton_check_if_section_is_normalized.setFont(font)
        self.pushButton_check_if_section_is_normalized.setStyleSheet(u"")

        self.gridLayout_31.addWidget(self.pushButton_check_if_section_is_normalized, 0, 1, 1, 1)


        self.gridLayout_32.addWidget(self.frame_31, 0, 0, 1, 2)

        self.frame_2 = QFrame(self.tab_constant_pipe_section)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(320, 200))
        self.frame_2.setMaximumSize(QSize(360, 280))
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_17 = QLabel(self.frame_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(50, 26))
        self.label_17.setMaximumSize(QSize(60, 26))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_17, 0, 3, 1, 1)

        self.label_20 = QLabel(self.frame_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(150, 26))
        self.label_20.setMaximumSize(QSize(174, 26))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_20, 0, 1, 1, 1)

        self.lineEdit_offset_y = QLineEdit(self.frame_2)
        self.lineEdit_offset_y.setObjectName(u"lineEdit_offset_y")
        self.lineEdit_offset_y.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_y.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_y.setFont(font)
        self.lineEdit_offset_y.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_y.setStyleSheet(u"")
        self.lineEdit_offset_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_y.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_offset_y, 2, 2, 1, 1)

        self.label_22 = QLabel(self.frame_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(150, 26))
        self.label_22.setMaximumSize(QSize(174, 26))
        self.label_22.setFont(font)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_22, 2, 1, 1, 1)

        self.lineEdit_insulation_thickness = QLineEdit(self.frame_2)
        self.lineEdit_insulation_thickness.setObjectName(u"lineEdit_insulation_thickness")
        self.lineEdit_insulation_thickness.setMinimumSize(QSize(120, 26))
        self.lineEdit_insulation_thickness.setMaximumSize(QSize(120, 26))
        self.lineEdit_insulation_thickness.setFont(font)
        self.lineEdit_insulation_thickness.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_insulation_thickness.setStyleSheet(u"")
        self.lineEdit_insulation_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_insulation_thickness.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_insulation_thickness, 4, 2, 1, 1)

        self.label_42 = QLabel(self.frame_2)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(50, 26))
        self.label_42.setMaximumSize(QSize(60, 26))
        self.label_42.setFont(font)
        self.label_42.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_42, 4, 3, 1, 1)

        self.lineEdit_offset_z = QLineEdit(self.frame_2)
        self.lineEdit_offset_z.setObjectName(u"lineEdit_offset_z")
        self.lineEdit_offset_z.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_z.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_z.setFont(font)
        self.lineEdit_offset_z.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_z.setStyleSheet(u"")
        self.lineEdit_offset_z.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_z.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_offset_z, 3, 2, 1, 1)

        self.label_41 = QLabel(self.frame_2)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(50, 26))
        self.label_41.setMaximumSize(QSize(60, 26))
        self.label_41.setFont(font)
        self.label_41.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_41, 5, 3, 1, 1)

        self.lineEdit_insulation_density = QLineEdit(self.frame_2)
        self.lineEdit_insulation_density.setObjectName(u"lineEdit_insulation_density")
        self.lineEdit_insulation_density.setMinimumSize(QSize(120, 26))
        self.lineEdit_insulation_density.setMaximumSize(QSize(120, 26))
        self.lineEdit_insulation_density.setFont(font)
        self.lineEdit_insulation_density.setStyleSheet(u"")
        self.lineEdit_insulation_density.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_insulation_density.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_insulation_density, 5, 2, 1, 1)

        self.label_23 = QLabel(self.frame_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(150, 26))
        self.label_23.setMaximumSize(QSize(174, 26))
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_23, 3, 1, 1, 1)

        self.label_25 = QLabel(self.frame_2)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(150, 26))
        self.label_25.setMaximumSize(QSize(174, 26))
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_25, 5, 1, 1, 1)

        self.label_26 = QLabel(self.frame_2)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(150, 26))
        self.label_26.setMaximumSize(QSize(174, 26))
        self.label_26.setFont(font)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_26, 4, 1, 1, 1)

        self.lineEdit_outside_diameter = QLineEdit(self.frame_2)
        self.lineEdit_outside_diameter.setObjectName(u"lineEdit_outside_diameter")
        self.lineEdit_outside_diameter.setMinimumSize(QSize(120, 26))
        self.lineEdit_outside_diameter.setMaximumSize(QSize(120, 26))
        self.lineEdit_outside_diameter.setFont(font)
        self.lineEdit_outside_diameter.setStyleSheet(u"")
        self.lineEdit_outside_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_outside_diameter.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_outside_diameter, 0, 2, 1, 1)

        self.label_18 = QLabel(self.frame_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(50, 26))
        self.label_18.setMaximumSize(QSize(60, 26))
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_18, 1, 3, 1, 1)

        self.label_19 = QLabel(self.frame_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(50, 26))
        self.label_19.setMaximumSize(QSize(60, 26))
        self.label_19.setFont(font)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_19, 2, 3, 1, 1)

        self.lineEdit_wall_thickness = QLineEdit(self.frame_2)
        self.lineEdit_wall_thickness.setObjectName(u"lineEdit_wall_thickness")
        self.lineEdit_wall_thickness.setMinimumSize(QSize(120, 26))
        self.lineEdit_wall_thickness.setMaximumSize(QSize(120, 26))
        self.lineEdit_wall_thickness.setFont(font)
        self.lineEdit_wall_thickness.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness.setStyleSheet(u"")
        self.lineEdit_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.lineEdit_wall_thickness, 1, 2, 1, 1)

        self.label_24 = QLabel(self.frame_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(50, 26))
        self.label_24.setMaximumSize(QSize(60, 26))
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_24, 3, 3, 1, 1)

        self.label_21 = QLabel(self.frame_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(150, 26))
        self.label_21.setMaximumSize(QSize(174, 26))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_21, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.label_24.raise_()
        self.lineEdit_outside_diameter.raise_()
        self.lineEdit_offset_z.raise_()
        self.label_22.raise_()
        self.lineEdit_wall_thickness.raise_()
        self.lineEdit_offset_y.raise_()
        self.label_17.raise_()
        self.label_21.raise_()
        self.label_23.raise_()
        self.label_19.raise_()
        self.label_18.raise_()
        self.label_42.raise_()
        self.label_26.raise_()
        self.label_25.raise_()
        self.lineEdit_insulation_density.raise_()
        self.lineEdit_insulation_thickness.raise_()
        self.label_20.raise_()
        self.label_41.raise_()

        self.gridLayout_32.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_30 = QFrame(self.tab_constant_pipe_section)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_30 = QGridLayout(self.frame_30)
        self.gridLayout_30.setSpacing(4)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.label_14 = QLabel(self.frame_30)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(204, 218))
        self.label_14.setMaximumSize(QSize(200, 218))
        self.label_14.setPixmap(QPixmap(u":/icons/figures/Pipe.PNG"))
        self.label_14.setScaledContents(True)

        self.gridLayout_30.addWidget(self.label_14, 0, 0, 1, 1)


        self.gridLayout_32.addWidget(self.frame_30, 1, 1, 1, 1)

        self.tabWidget_pipe_section.addTab(self.tab_constant_pipe_section, "")
        self.tab_variable_pipe_section = QWidget()
        self.tab_variable_pipe_section.setObjectName(u"tab_variable_pipe_section")
        self.gridLayout_10 = QGridLayout(self.tab_variable_pipe_section)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 7, 0, 2)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.frame = QFrame(self.tab_variable_pipe_section)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_10)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.pushButton_select_standard_section_initial = QPushButton(self.frame_10)
        self.pushButton_select_standard_section_initial.setObjectName(u"pushButton_select_standard_section_initial")
        self.pushButton_select_standard_section_initial.setMinimumSize(QSize(90, 26))
        self.pushButton_select_standard_section_initial.setMaximumSize(QSize(90, 26))
        self.pushButton_select_standard_section_initial.setFont(font)
        self.pushButton_select_standard_section_initial.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.pushButton_select_standard_section_initial, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_10, 6, 2, 1, 1)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_4)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_select_standard_section_final = QPushButton(self.frame_4)
        self.pushButton_select_standard_section_final.setObjectName(u"pushButton_select_standard_section_final")
        self.pushButton_select_standard_section_final.setMinimumSize(QSize(90, 26))
        self.pushButton_select_standard_section_final.setMaximumSize(QSize(90, 26))
        self.pushButton_select_standard_section_final.setFont(font)
        self.pushButton_select_standard_section_final.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.pushButton_select_standard_section_final, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 6, 5, 1, 1)

        self.label_82 = QLabel(self.frame)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setMinimumSize(QSize(0, 32))
        self.label_82.setMaximumSize(QSize(16777215, 32))
        self.label_82.setFont(font)
        self.label_82.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_82, 4, 1, 1, 1)

        self.lineEdit_offset_y_final = QLineEdit(self.frame)
        self.lineEdit_offset_y_final.setObjectName(u"lineEdit_offset_y_final")
        self.lineEdit_offset_y_final.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_y_final.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_y_final.setFont(font)
        self.lineEdit_offset_y_final.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_y_final.setStyleSheet(u"")
        self.lineEdit_offset_y_final.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_y_final.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_offset_y_final, 4, 5, 1, 1)

        self.label_element_id = QLabel(self.frame)
        self.label_element_id.setObjectName(u"label_element_id")
        self.label_element_id.setMinimumSize(QSize(0, 32))
        self.label_element_id.setMaximumSize(QSize(16777215, 32))
        self.label_element_id.setFont(font)
        self.label_element_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_element_id, 1, 1, 1, 1)

        self.label_63 = QLabel(self.frame)
        self.label_63.setObjectName(u"label_63")
        self.label_63.setMinimumSize(QSize(40, 26))
        self.label_63.setMaximumSize(QSize(40, 26))
        self.label_63.setFont(font)
        self.label_63.setFrameShape(QFrame.Shape.NoFrame)
        self.label_63.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_63, 2, 3, 1, 1)

        self.lineEdit_outside_diameter_initial = QLineEdit(self.frame)
        self.lineEdit_outside_diameter_initial.setObjectName(u"lineEdit_outside_diameter_initial")
        self.lineEdit_outside_diameter_initial.setMinimumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_initial.setMaximumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_initial.setFont(font)
        self.lineEdit_outside_diameter_initial.setStyleSheet(u"")
        self.lineEdit_outside_diameter_initial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_outside_diameter_initial.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_outside_diameter_initial, 2, 2, 1, 1)

        self.label_62 = QLabel(self.frame)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setMinimumSize(QSize(40, 26))
        self.label_62.setMaximumSize(QSize(40, 26))
        self.label_62.setFont(font)
        self.label_62.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_62, 3, 3, 1, 1)

        self.label_89 = QLabel(self.frame)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setMinimumSize(QSize(0, 32))
        self.label_89.setMaximumSize(QSize(16777215, 32))
        self.label_89.setFont(font)
        self.label_89.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_89, 5, 1, 1, 1)

        self.label_86 = QLabel(self.frame)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setMinimumSize(QSize(0, 32))
        self.label_86.setMaximumSize(QSize(16777215, 32))
        self.label_86.setFont(font)
        self.label_86.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_86, 3, 1, 1, 1)

        self.label_90 = QLabel(self.frame)
        self.label_90.setObjectName(u"label_90")
        self.label_90.setMinimumSize(QSize(0, 32))
        self.label_90.setMaximumSize(QSize(16777215, 32))
        self.label_90.setFont(font)
        self.label_90.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_90, 2, 1, 1, 1)

        self.lineEdit_wall_thickness_final = QLineEdit(self.frame)
        self.lineEdit_wall_thickness_final.setObjectName(u"lineEdit_wall_thickness_final")
        self.lineEdit_wall_thickness_final.setMinimumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_final.setMaximumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_final.setFont(font)
        self.lineEdit_wall_thickness_final.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_final.setStyleSheet(u"")
        self.lineEdit_wall_thickness_final.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness_final.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_wall_thickness_final, 3, 5, 1, 1)

        self.label_80 = QLabel(self.frame)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setMinimumSize(QSize(40, 26))
        self.label_80.setMaximumSize(QSize(40, 26))
        self.label_80.setFont(font)
        self.label_80.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_80, 5, 6, 1, 1)

        self.label_66 = QLabel(self.frame)
        self.label_66.setObjectName(u"label_66")
        self.label_66.setMinimumSize(QSize(40, 26))
        self.label_66.setMaximumSize(QSize(40, 26))
        self.label_66.setFont(font)
        self.label_66.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_66, 5, 3, 1, 1)

        self.lineEdit_offset_z_initial = QLineEdit(self.frame)
        self.lineEdit_offset_z_initial.setObjectName(u"lineEdit_offset_z_initial")
        self.lineEdit_offset_z_initial.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_z_initial.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_z_initial.setFont(font)
        self.lineEdit_offset_z_initial.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_z_initial.setStyleSheet(u"")
        self.lineEdit_offset_z_initial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_z_initial.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_offset_z_initial, 5, 2, 1, 1)

        self.lineEdit_offset_y_initial = QLineEdit(self.frame)
        self.lineEdit_offset_y_initial.setObjectName(u"lineEdit_offset_y_initial")
        self.lineEdit_offset_y_initial.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_y_initial.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_y_initial.setFont(font)
        self.lineEdit_offset_y_initial.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_y_initial.setStyleSheet(u"")
        self.lineEdit_offset_y_initial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_y_initial.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_offset_y_initial, 4, 2, 1, 1)

        self.lineEdit_offset_z_final = QLineEdit(self.frame)
        self.lineEdit_offset_z_final.setObjectName(u"lineEdit_offset_z_final")
        self.lineEdit_offset_z_final.setMinimumSize(QSize(120, 26))
        self.lineEdit_offset_z_final.setMaximumSize(QSize(120, 26))
        self.lineEdit_offset_z_final.setFont(font)
        self.lineEdit_offset_z_final.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offset_z_final.setStyleSheet(u"")
        self.lineEdit_offset_z_final.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offset_z_final.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_offset_z_final, 5, 5, 1, 1)

        self.label_91 = QLabel(self.frame)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setMinimumSize(QSize(40, 26))
        self.label_91.setMaximumSize(QSize(40, 26))
        self.label_91.setFont(font)
        self.label_91.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_91, 4, 6, 1, 1)

        self.label_64 = QLabel(self.frame)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setMinimumSize(QSize(40, 26))
        self.label_64.setMaximumSize(QSize(40, 26))
        self.label_64.setFont(font)
        self.label_64.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_64, 4, 3, 1, 1)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(120, 30))
        self.frame_6.setMaximumSize(QSize(180, 30))
        self.frame_6.setFrameShape(QFrame.Shape.Box)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_6)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.frame_6)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(0, 0))
        self.label_36.setMaximumSize(QSize(16777215, 60))
        self.label_36.setFont(font)
        self.label_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.label_36, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_6, 0, 5, 1, 1)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(120, 30))
        self.frame_5.setMaximumSize(QSize(180, 30))
        self.frame_5.setFrameShape(QFrame.Shape.Box)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_5)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_37 = QLabel(self.frame_5)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(0, 0))
        self.label_37.setMaximumSize(QSize(16777215, 60))
        self.label_37.setFont(font)
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_37, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_5, 0, 2, 1, 1)

        self.lineEdit_element_id_initial = QLineEdit(self.frame)
        self.lineEdit_element_id_initial.setObjectName(u"lineEdit_element_id_initial")
        self.lineEdit_element_id_initial.setMinimumSize(QSize(120, 26))
        self.lineEdit_element_id_initial.setMaximumSize(QSize(120, 26))
        self.lineEdit_element_id_initial.setFont(font)
        self.lineEdit_element_id_initial.setStyleSheet(u"")
        self.lineEdit_element_id_initial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_element_id_initial.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_element_id_initial, 1, 2, 1, 1)

        self.lineEdit_element_id_final = QLineEdit(self.frame)
        self.lineEdit_element_id_final.setObjectName(u"lineEdit_element_id_final")
        self.lineEdit_element_id_final.setMinimumSize(QSize(120, 26))
        self.lineEdit_element_id_final.setMaximumSize(QSize(120, 26))
        self.lineEdit_element_id_final.setFont(font)
        self.lineEdit_element_id_final.setStyleSheet(u"")
        self.lineEdit_element_id_final.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_element_id_final.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_element_id_final, 1, 5, 1, 1)

        self.label_79 = QLabel(self.frame)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setMinimumSize(QSize(40, 26))
        self.label_79.setMaximumSize(QSize(40, 26))
        self.label_79.setFont(font)
        self.label_79.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_79, 2, 6, 1, 1)

        self.lineEdit_wall_thickness_initial = QLineEdit(self.frame)
        self.lineEdit_wall_thickness_initial.setObjectName(u"lineEdit_wall_thickness_initial")
        self.lineEdit_wall_thickness_initial.setMinimumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_initial.setMaximumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_initial.setFont(font)
        self.lineEdit_wall_thickness_initial.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_initial.setStyleSheet(u"")
        self.lineEdit_wall_thickness_initial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness_initial.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_wall_thickness_initial, 3, 2, 1, 1)

        self.lineEdit_outside_diameter_final = QLineEdit(self.frame)
        self.lineEdit_outside_diameter_final.setObjectName(u"lineEdit_outside_diameter_final")
        self.lineEdit_outside_diameter_final.setMinimumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_final.setMaximumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_final.setFont(font)
        self.lineEdit_outside_diameter_final.setStyleSheet(u"")
        self.lineEdit_outside_diameter_final.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_outside_diameter_final.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.lineEdit_outside_diameter_final, 2, 5, 1, 1)

        self.label_88 = QLabel(self.frame)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setMinimumSize(QSize(40, 26))
        self.label_88.setMaximumSize(QSize(40, 26))
        self.label_88.setFont(font)
        self.label_88.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_88, 3, 6, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_18, 2, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_17, 2, 7, 1, 1)

        self.frame_11 = QFrame(self.frame)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_11)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.pushButton_invert_input_values = QPushButton(self.frame_11)
        self.pushButton_invert_input_values.setObjectName(u"pushButton_invert_input_values")
        self.pushButton_invert_input_values.setMinimumSize(QSize(40, 26))
        self.pushButton_invert_input_values.setMaximumSize(QSize(40, 26))
        self.pushButton_invert_input_values.setFont(font)
        self.pushButton_invert_input_values.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/swap_horizontal_arrows.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_invert_input_values.setIcon(icon)
        self.pushButton_invert_input_values.setIconSize(QSize(22, 22))

        self.gridLayout_16.addWidget(self.pushButton_invert_input_values, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_11, 0, 3, 1, 1)


        self.gridLayout_10.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_20 = QFrame(self.tab_variable_pipe_section)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 72))
        self.frame_20.setMaximumSize(QSize(16777215, 72))
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_20)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(8)
        self.gridLayout_9.setVerticalSpacing(6)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_48 = QLabel(self.frame_20)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(132, 26))
        self.label_48.setMaximumSize(QSize(132, 26))
        self.label_48.setFont(font)
        self.label_48.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_48, 1, 1, 1, 1)

        self.lineEdit_insulation_density_variable_section = QLineEdit(self.frame_20)
        self.lineEdit_insulation_density_variable_section.setObjectName(u"lineEdit_insulation_density_variable_section")
        self.lineEdit_insulation_density_variable_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_insulation_density_variable_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_insulation_density_variable_section.setFont(font)
        self.lineEdit_insulation_density_variable_section.setStyleSheet(u"")
        self.lineEdit_insulation_density_variable_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_insulation_density_variable_section.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_insulation_density_variable_section, 1, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.label_46 = QLabel(self.frame_20)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(132, 26))
        self.label_46.setMaximumSize(QSize(132, 26))
        self.label_46.setFont(font)
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_46, 0, 1, 1, 1)

        self.label_45 = QLabel(self.frame_20)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(60, 26))
        self.label_45.setMaximumSize(QSize(60, 26))
        self.label_45.setFont(font)
        self.label_45.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_45, 0, 3, 1, 1)

        self.label_47 = QLabel(self.frame_20)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setMinimumSize(QSize(60, 26))
        self.label_47.setMaximumSize(QSize(60, 26))
        self.label_47.setFont(font)
        self.label_47.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_47, 1, 3, 1, 1)

        self.lineEdit_insulation_thickness_variable_section = QLineEdit(self.frame_20)
        self.lineEdit_insulation_thickness_variable_section.setObjectName(u"lineEdit_insulation_thickness_variable_section")
        self.lineEdit_insulation_thickness_variable_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_insulation_thickness_variable_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_insulation_thickness_variable_section.setFont(font)
        self.lineEdit_insulation_thickness_variable_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_insulation_thickness_variable_section.setStyleSheet(u"")
        self.lineEdit_insulation_thickness_variable_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_insulation_thickness_variable_section.setClearButtonEnabled(True)

        self.gridLayout_9.addWidget(self.lineEdit_insulation_thickness_variable_section, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)


        self.gridLayout_10.addWidget(self.frame_20, 3, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_4, 4, 0, 1, 1)

        self.tabWidget_pipe_section.addTab(self.tab_variable_pipe_section, "")

        self.gridLayout_4.addWidget(self.tabWidget_pipe_section, 0, 0, 1, 2)

        self.tabWidget_general.addTab(self.tab_pipe, "")
        self.tab_beam = QWidget()
        self.tab_beam.setObjectName(u"tab_beam")
        self.gridLayout_33 = QGridLayout(self.tab_beam)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.tabWidget_beam_section = QTabWidget(self.tab_beam)
        self.tabWidget_beam_section.setObjectName(u"tabWidget_beam_section")
        self.tabWidget_beam_section.setMinimumSize(QSize(554, 350))
        self.tabWidget_beam_section.setMaximumSize(QSize(620, 380))
        self.tabWidget_beam_section.setFont(font)
        self.tab_rectangular_section = QWidget()
        self.tab_rectangular_section.setObjectName(u"tab_rectangular_section")
        self.gridLayout_35 = QGridLayout(self.tab_rectangular_section)
        self.gridLayout_35.setSpacing(4)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.gridLayout_35.setContentsMargins(4, 4, 4, 4)
        self.frame_9 = QFrame(self.tab_rectangular_section)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_9)
        self.gridLayout_26.setSpacing(4)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(4, 4, 4, 4)
        self.label_109 = QLabel(self.frame_9)
        self.label_109.setObjectName(u"label_109")
        self.label_109.setMinimumSize(QSize(30, 26))
        self.label_109.setMaximumSize(QSize(30, 26))
        self.label_109.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_109, 2, 3, 1, 1)

        self.label_112 = QLabel(self.frame_9)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setMinimumSize(QSize(120, 26))
        self.label_112.setMaximumSize(QSize(132, 26))
        self.label_112.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_112, 2, 1, 1, 1)

        self.label_113 = QLabel(self.frame_9)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setMinimumSize(QSize(120, 26))
        self.label_113.setMaximumSize(QSize(132, 26))
        self.label_113.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_113, 3, 1, 1, 1)

        self.lineEdit_base_rectangular_section = QLineEdit(self.frame_9)
        self.lineEdit_base_rectangular_section.setObjectName(u"lineEdit_base_rectangular_section")
        self.lineEdit_base_rectangular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_base_rectangular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_base_rectangular_section.setFont(font)
        self.lineEdit_base_rectangular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_base_rectangular_section.setStyleSheet(u"")
        self.lineEdit_base_rectangular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_base_rectangular_section.setClearButtonEnabled(True)

        self.gridLayout_26.addWidget(self.lineEdit_base_rectangular_section, 0, 2, 1, 1)

        self.label_94 = QLabel(self.frame_9)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setMinimumSize(QSize(120, 26))
        self.label_94.setMaximumSize(QSize(132, 26))
        self.label_94.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_94, 1, 1, 1, 1)

        self.label_110 = QLabel(self.frame_9)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setMinimumSize(QSize(30, 26))
        self.label_110.setMaximumSize(QSize(30, 26))
        self.label_110.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_110, 3, 3, 1, 1)

        self.label_100 = QLabel(self.frame_9)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setMinimumSize(QSize(30, 26))
        self.label_100.setMaximumSize(QSize(30, 26))
        self.label_100.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_100, 0, 3, 1, 1)

        self.label_114 = QLabel(self.frame_9)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setMinimumSize(QSize(120, 26))
        self.label_114.setMaximumSize(QSize(132, 26))
        self.label_114.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_114, 4, 1, 1, 1)

        self.lineEdit_offsety_rectangular_section = QLineEdit(self.frame_9)
        self.lineEdit_offsety_rectangular_section.setObjectName(u"lineEdit_offsety_rectangular_section")
        self.lineEdit_offsety_rectangular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsety_rectangular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsety_rectangular_section.setFont(font)
        self.lineEdit_offsety_rectangular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsety_rectangular_section.setStyleSheet(u"")
        self.lineEdit_offsety_rectangular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsety_rectangular_section.setClearButtonEnabled(True)

        self.gridLayout_26.addWidget(self.lineEdit_offsety_rectangular_section, 3, 2, 1, 1)

        self.lineEdit_height_rectangular_section = QLineEdit(self.frame_9)
        self.lineEdit_height_rectangular_section.setObjectName(u"lineEdit_height_rectangular_section")
        self.lineEdit_height_rectangular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_height_rectangular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_height_rectangular_section.setFont(font)
        self.lineEdit_height_rectangular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_height_rectangular_section.setStyleSheet(u"")
        self.lineEdit_height_rectangular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_height_rectangular_section.setClearButtonEnabled(True)

        self.gridLayout_26.addWidget(self.lineEdit_height_rectangular_section, 1, 2, 1, 1)

        self.label_107 = QLabel(self.frame_9)
        self.label_107.setObjectName(u"label_107")
        self.label_107.setMinimumSize(QSize(30, 26))
        self.label_107.setMaximumSize(QSize(30, 26))
        self.label_107.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_107, 1, 3, 1, 1)

        self.label_72 = QLabel(self.frame_9)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setMinimumSize(QSize(120, 26))
        self.label_72.setMaximumSize(QSize(132, 26))
        self.label_72.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_72, 0, 1, 1, 1)

        self.label_111 = QLabel(self.frame_9)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setMinimumSize(QSize(30, 26))
        self.label_111.setMaximumSize(QSize(30, 26))
        self.label_111.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_111, 4, 3, 1, 1)

        self.lineEdit_offsetz_rectangular_section = QLineEdit(self.frame_9)
        self.lineEdit_offsetz_rectangular_section.setObjectName(u"lineEdit_offsetz_rectangular_section")
        self.lineEdit_offsetz_rectangular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsetz_rectangular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsetz_rectangular_section.setFont(font)
        self.lineEdit_offsetz_rectangular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsetz_rectangular_section.setStyleSheet(u"")
        self.lineEdit_offsetz_rectangular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsetz_rectangular_section.setClearButtonEnabled(True)

        self.gridLayout_26.addWidget(self.lineEdit_offsetz_rectangular_section, 4, 2, 1, 1)

        self.lineEdit_wall_thickness_rectangular_section = QLineEdit(self.frame_9)
        self.lineEdit_wall_thickness_rectangular_section.setObjectName(u"lineEdit_wall_thickness_rectangular_section")
        self.lineEdit_wall_thickness_rectangular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_rectangular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_rectangular_section.setFont(font)
        self.lineEdit_wall_thickness_rectangular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_rectangular_section.setStyleSheet(u"")
        self.lineEdit_wall_thickness_rectangular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness_rectangular_section.setClearButtonEnabled(True)

        self.gridLayout_26.addWidget(self.lineEdit_wall_thickness_rectangular_section, 2, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_5, 2, 0, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_16, 2, 4, 1, 1)


        self.gridLayout_35.addWidget(self.frame_9, 0, 0, 1, 1)

        self.frame_17 = QFrame(self.tab_rectangular_section)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_17)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_17)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(250, 310))
        self.label_4.setMaximumSize(QSize(250, 310))
        self.label_4.setPixmap(QPixmap(u":/icons/figures/Rectangular.PNG"))
        self.label_4.setScaledContents(True)

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)


        self.gridLayout_35.addWidget(self.frame_17, 0, 1, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_rectangular_section, "")
        self.tab_circular_section = QWidget()
        self.tab_circular_section.setObjectName(u"tab_circular_section")
        self.gridLayout_29 = QGridLayout(self.tab_circular_section)
        self.gridLayout_29.setSpacing(4)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setContentsMargins(4, 4, 4, 4)
        self.frame_14 = QFrame(self.tab_circular_section)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_14)
        self.gridLayout_27.setSpacing(4)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.label_43 = QLabel(self.frame_14)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(140, 26))
        self.label_43.setMaximumSize(QSize(160, 26))
        self.label_43.setFont(font)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_43, 0, 1, 1, 1)

        self.label_115 = QLabel(self.frame_14)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setMinimumSize(QSize(35, 26))
        self.label_115.setMaximumSize(QSize(35, 26))
        self.label_115.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_115, 0, 3, 1, 1)

        self.lineEdit_outside_diameter_circular_section = QLineEdit(self.frame_14)
        self.lineEdit_outside_diameter_circular_section.setObjectName(u"lineEdit_outside_diameter_circular_section")
        self.lineEdit_outside_diameter_circular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_circular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_outside_diameter_circular_section.setFont(font)
        self.lineEdit_outside_diameter_circular_section.setStyleSheet(u"")
        self.lineEdit_outside_diameter_circular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_outside_diameter_circular_section.setClearButtonEnabled(True)

        self.gridLayout_27.addWidget(self.lineEdit_outside_diameter_circular_section, 0, 2, 1, 1)

        self.lineEdit_wall_thickness_circular_section = QLineEdit(self.frame_14)
        self.lineEdit_wall_thickness_circular_section.setObjectName(u"lineEdit_wall_thickness_circular_section")
        self.lineEdit_wall_thickness_circular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_circular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_wall_thickness_circular_section.setFont(font)
        self.lineEdit_wall_thickness_circular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_wall_thickness_circular_section.setStyleSheet(u"")
        self.lineEdit_wall_thickness_circular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_wall_thickness_circular_section.setClearButtonEnabled(True)

        self.gridLayout_27.addWidget(self.lineEdit_wall_thickness_circular_section, 1, 2, 1, 1)

        self.label_65 = QLabel(self.frame_14)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setMinimumSize(QSize(100, 26))
        self.label_65.setMaximumSize(QSize(160, 26))
        self.label_65.setFont(font)
        self.label_65.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_65, 1, 1, 1, 1)

        self.label_118 = QLabel(self.frame_14)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setMinimumSize(QSize(35, 26))
        self.label_118.setMaximumSize(QSize(35, 26))
        self.label_118.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_118, 3, 3, 1, 1)

        self.label_116 = QLabel(self.frame_14)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setMinimumSize(QSize(35, 26))
        self.label_116.setMaximumSize(QSize(35, 26))
        self.label_116.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_116, 1, 3, 1, 1)

        self.label_119 = QLabel(self.frame_14)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setMinimumSize(QSize(100, 26))
        self.label_119.setMaximumSize(QSize(160, 26))
        self.label_119.setFont(font)
        self.label_119.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_119, 2, 1, 1, 1)

        self.label_120 = QLabel(self.frame_14)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setMinimumSize(QSize(35, 26))
        self.label_120.setMaximumSize(QSize(35, 26))
        self.label_120.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_120, 2, 3, 1, 1)

        self.label_117 = QLabel(self.frame_14)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setMinimumSize(QSize(100, 26))
        self.label_117.setMaximumSize(QSize(160, 26))
        self.label_117.setFont(font)
        self.label_117.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_27.addWidget(self.label_117, 3, 1, 1, 1)

        self.lineEdit_offsety_circular_section = QLineEdit(self.frame_14)
        self.lineEdit_offsety_circular_section.setObjectName(u"lineEdit_offsety_circular_section")
        self.lineEdit_offsety_circular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsety_circular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsety_circular_section.setFont(font)
        self.lineEdit_offsety_circular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsety_circular_section.setStyleSheet(u"")
        self.lineEdit_offsety_circular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsety_circular_section.setClearButtonEnabled(True)

        self.gridLayout_27.addWidget(self.lineEdit_offsety_circular_section, 2, 2, 1, 1)

        self.lineEdit_offsetz_circular_section = QLineEdit(self.frame_14)
        self.lineEdit_offsetz_circular_section.setObjectName(u"lineEdit_offsetz_circular_section")
        self.lineEdit_offsetz_circular_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsetz_circular_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsetz_circular_section.setFont(font)
        self.lineEdit_offsetz_circular_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsetz_circular_section.setStyleSheet(u"")
        self.lineEdit_offsetz_circular_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsetz_circular_section.setClearButtonEnabled(True)

        self.gridLayout_27.addWidget(self.lineEdit_offsetz_circular_section, 3, 2, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_15, 0, 4, 1, 1)


        self.gridLayout_29.addWidget(self.frame_14, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.tab_circular_section)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_28 = QGridLayout(self.frame_15)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.label_7 = QLabel(self.frame_15)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(204, 232))
        self.label_7.setMaximumSize(QSize(204, 232))
        self.label_7.setPixmap(QPixmap(u":/icons/figures/Circular.PNG"))
        self.label_7.setScaledContents(True)

        self.gridLayout_28.addWidget(self.label_7, 0, 0, 1, 1)


        self.gridLayout_29.addWidget(self.frame_15, 0, 1, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_circular_section, "")
        self.tab_C_section = QWidget()
        self.tab_C_section.setObjectName(u"tab_C_section")
        self.gridLayout_49 = QGridLayout(self.tab_C_section)
        self.gridLayout_49.setSpacing(4)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.gridLayout_49.setContentsMargins(4, 4, 4, 4)
        self.frame_26 = QFrame(self.tab_C_section)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_48 = QGridLayout(self.frame_26)
        self.gridLayout_48.setSpacing(4)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.gridLayout_48.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_48.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.label_67 = QLabel(self.frame_26)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setMinimumSize(QSize(90, 26))
        self.label_67.setMaximumSize(QSize(90, 26))
        self.label_67.setFont(font)
        self.label_67.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_67, 0, 1, 1, 1)

        self.label_68 = QLabel(self.frame_26)
        self.label_68.setObjectName(u"label_68")
        self.label_68.setMinimumSize(QSize(90, 26))
        self.label_68.setMaximumSize(QSize(90, 26))
        self.label_68.setFont(font)
        self.label_68.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_68, 1, 1, 1, 1)

        self.lineEdit_height_C_section = QLineEdit(self.frame_26)
        self.lineEdit_height_C_section.setObjectName(u"lineEdit_height_C_section")
        self.lineEdit_height_C_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_height_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_height_C_section.setSizeIncrement(QSize(0, 26))
        self.lineEdit_height_C_section.setFont(font)
        self.lineEdit_height_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_height_C_section.setStyleSheet(u"")
        self.lineEdit_height_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_height_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_height_C_section, 0, 2, 1, 1)

        self.label_121 = QLabel(self.frame_26)
        self.label_121.setObjectName(u"label_121")
        self.label_121.setMinimumSize(QSize(30, 26))
        self.label_121.setMaximumSize(QSize(30, 26))
        self.label_121.setFont(font)
        self.label_121.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_121, 0, 3, 1, 1)

        self.label_122 = QLabel(self.frame_26)
        self.label_122.setObjectName(u"label_122")
        self.label_122.setMinimumSize(QSize(30, 26))
        self.label_122.setMaximumSize(QSize(30, 26))
        self.label_122.setFont(font)
        self.label_122.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_122, 1, 3, 1, 1)

        self.label_69 = QLabel(self.frame_26)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setMinimumSize(QSize(90, 26))
        self.label_69.setMaximumSize(QSize(90, 26))
        self.label_69.setFont(font)
        self.label_69.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_69, 2, 1, 1, 1)

        self.lineEdit_w1_C_section = QLineEdit(self.frame_26)
        self.lineEdit_w1_C_section.setObjectName(u"lineEdit_w1_C_section")
        self.lineEdit_w1_C_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_w1_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_w1_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_w1_C_section.setFont(font)
        self.lineEdit_w1_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_w1_C_section.setStyleSheet(u"")
        self.lineEdit_w1_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_w1_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_w1_C_section, 1, 2, 1, 1)

        self.lineEdit_w2_C_section = QLineEdit(self.frame_26)
        self.lineEdit_w2_C_section.setObjectName(u"lineEdit_w2_C_section")
        self.lineEdit_w2_C_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_w2_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_w2_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_w2_C_section.setFont(font)
        self.lineEdit_w2_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_w2_C_section.setStyleSheet(u"")
        self.lineEdit_w2_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_w2_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_w2_C_section, 2, 2, 1, 1)

        self.label_123 = QLabel(self.frame_26)
        self.label_123.setObjectName(u"label_123")
        self.label_123.setMinimumSize(QSize(30, 26))
        self.label_123.setMaximumSize(QSize(30, 26))
        self.label_123.setFont(font)
        self.label_123.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_123, 2, 3, 1, 1)

        self.label_70 = QLabel(self.frame_26)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setMinimumSize(QSize(90, 26))
        self.label_70.setMaximumSize(QSize(90, 26))
        self.label_70.setFont(font)
        self.label_70.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_70, 3, 1, 1, 1)

        self.lineEdit_t1_C_section = QLineEdit(self.frame_26)
        self.lineEdit_t1_C_section.setObjectName(u"lineEdit_t1_C_section")
        self.lineEdit_t1_C_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_t1_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_t1_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_t1_C_section.setFont(font)
        self.lineEdit_t1_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_t1_C_section.setStyleSheet(u"")
        self.lineEdit_t1_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_t1_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_t1_C_section, 3, 2, 1, 1)

        self.lineEdit_t2_C_section = QLineEdit(self.frame_26)
        self.lineEdit_t2_C_section.setObjectName(u"lineEdit_t2_C_section")
        self.lineEdit_t2_C_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_t2_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_t2_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_t2_C_section.setFont(font)
        self.lineEdit_t2_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_t2_C_section.setStyleSheet(u"")
        self.lineEdit_t2_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_t2_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_t2_C_section, 4, 2, 1, 1)

        self.label_71 = QLabel(self.frame_26)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setMinimumSize(QSize(90, 26))
        self.label_71.setMaximumSize(QSize(90, 26))
        self.label_71.setFont(font)
        self.label_71.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_71, 4, 1, 1, 1)

        self.label_124 = QLabel(self.frame_26)
        self.label_124.setObjectName(u"label_124")
        self.label_124.setMinimumSize(QSize(30, 26))
        self.label_124.setMaximumSize(QSize(30, 26))
        self.label_124.setFont(font)
        self.label_124.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_124, 3, 3, 1, 1)

        self.lineEdit_tw_C_section = QLineEdit(self.frame_26)
        self.lineEdit_tw_C_section.setObjectName(u"lineEdit_tw_C_section")
        self.lineEdit_tw_C_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_tw_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_tw_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_tw_C_section.setFont(font)
        self.lineEdit_tw_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_tw_C_section.setStyleSheet(u"")
        self.lineEdit_tw_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_tw_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_tw_C_section, 5, 2, 1, 1)

        self.label_125 = QLabel(self.frame_26)
        self.label_125.setObjectName(u"label_125")
        self.label_125.setMinimumSize(QSize(30, 26))
        self.label_125.setMaximumSize(QSize(30, 26))
        self.label_125.setFont(font)
        self.label_125.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_125, 4, 3, 1, 1)

        self.label_73 = QLabel(self.frame_26)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setMinimumSize(QSize(90, 26))
        self.label_73.setMaximumSize(QSize(90, 26))
        self.label_73.setFont(font)
        self.label_73.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_48.addWidget(self.label_73, 5, 1, 1, 1)

        self.label_131 = QLabel(self.frame_26)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setMinimumSize(QSize(90, 26))
        self.label_131.setMaximumSize(QSize(90, 26))
        self.label_131.setFont(font)
        self.label_131.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_131, 6, 1, 1, 1)

        self.lineEdit_offsety_C_section = QLineEdit(self.frame_26)
        self.lineEdit_offsety_C_section.setObjectName(u"lineEdit_offsety_C_section")
        self.lineEdit_offsety_C_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsety_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsety_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offsety_C_section.setFont(font)
        self.lineEdit_offsety_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsety_C_section.setStyleSheet(u"")
        self.lineEdit_offsety_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsety_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_offsety_C_section, 6, 2, 1, 1)

        self.label_126 = QLabel(self.frame_26)
        self.label_126.setObjectName(u"label_126")
        self.label_126.setMinimumSize(QSize(30, 26))
        self.label_126.setMaximumSize(QSize(30, 26))
        self.label_126.setFont(font)
        self.label_126.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_126, 5, 3, 1, 1)

        self.lineEdit_offsetz_C_section = QLineEdit(self.frame_26)
        self.lineEdit_offsetz_C_section.setObjectName(u"lineEdit_offsetz_C_section")
        self.lineEdit_offsetz_C_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsetz_C_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsetz_C_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offsetz_C_section.setFont(font)
        self.lineEdit_offsetz_C_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsetz_C_section.setStyleSheet(u"")
        self.lineEdit_offsetz_C_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsetz_C_section.setClearButtonEnabled(True)

        self.gridLayout_48.addWidget(self.lineEdit_offsetz_C_section, 7, 2, 1, 1)

        self.label_128 = QLabel(self.frame_26)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setMinimumSize(QSize(30, 26))
        self.label_128.setMaximumSize(QSize(30, 26))
        self.label_128.setFont(font)
        self.label_128.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_128, 6, 3, 1, 1)

        self.label_130 = QLabel(self.frame_26)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setMinimumSize(QSize(90, 26))
        self.label_130.setMaximumSize(QSize(90, 26))
        self.label_130.setFont(font)
        self.label_130.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_130, 7, 1, 1, 1)

        self.label_129 = QLabel(self.frame_26)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setMinimumSize(QSize(30, 26))
        self.label_129.setMaximumSize(QSize(30, 26))
        self.label_129.setFont(font)
        self.label_129.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_48.addWidget(self.label_129, 7, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_48.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout_49.addWidget(self.frame_26, 0, 0, 1, 1)

        self.frame_25 = QFrame(self.tab_C_section)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_25)
        self.gridLayout_47.setSpacing(0)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_25)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(250, 310))
        self.label_9.setMaximumSize(QSize(250, 310))
        self.label_9.setPixmap(QPixmap(u":/icons/figures/C_profile.PNG"))
        self.label_9.setScaledContents(True)

        self.gridLayout_47.addWidget(self.label_9, 0, 0, 1, 1)


        self.gridLayout_49.addWidget(self.frame_25, 0, 1, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_C_section, "")
        self.tab_I_section = QWidget()
        self.tab_I_section.setObjectName(u"tab_I_section")
        self.gridLayout_51 = QGridLayout(self.tab_I_section)
        self.gridLayout_51.setSpacing(4)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.gridLayout_51.setContentsMargins(4, 4, 4, 4)
        self.frame_27 = QFrame(self.tab_I_section)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_50 = QGridLayout(self.frame_27)
        self.gridLayout_50.setSpacing(4)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.gridLayout_50.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_50.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)

        self.label_78 = QLabel(self.frame_27)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setMinimumSize(QSize(90, 26))
        self.label_78.setMaximumSize(QSize(90, 26))
        self.label_78.setFont(font)
        self.label_78.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_78, 0, 1, 1, 1)

        self.lineEdit_height_I_section = QLineEdit(self.frame_27)
        self.lineEdit_height_I_section.setObjectName(u"lineEdit_height_I_section")
        self.lineEdit_height_I_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_height_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_height_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_height_I_section.setFont(font)
        self.lineEdit_height_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_height_I_section.setStyleSheet(u"")
        self.lineEdit_height_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_height_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_height_I_section, 0, 2, 1, 1)

        self.lineEdit_w1_I_section = QLineEdit(self.frame_27)
        self.lineEdit_w1_I_section.setObjectName(u"lineEdit_w1_I_section")
        self.lineEdit_w1_I_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_w1_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_w1_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_w1_I_section.setFont(font)
        self.lineEdit_w1_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_w1_I_section.setStyleSheet(u"")
        self.lineEdit_w1_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_w1_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_w1_I_section, 1, 2, 1, 1)

        self.label_75 = QLabel(self.frame_27)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setMinimumSize(QSize(90, 26))
        self.label_75.setMaximumSize(QSize(90, 26))
        self.label_75.setFont(font)
        self.label_75.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_75, 1, 1, 1, 1)

        self.label_142 = QLabel(self.frame_27)
        self.label_142.setObjectName(u"label_142")
        self.label_142.setMinimumSize(QSize(30, 26))
        self.label_142.setMaximumSize(QSize(30, 26))
        self.label_142.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_142, 0, 3, 1, 1)

        self.lineEdit_w2_I_section = QLineEdit(self.frame_27)
        self.lineEdit_w2_I_section.setObjectName(u"lineEdit_w2_I_section")
        self.lineEdit_w2_I_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_w2_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_w2_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_w2_I_section.setFont(font)
        self.lineEdit_w2_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_w2_I_section.setStyleSheet(u"")
        self.lineEdit_w2_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_w2_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_w2_I_section, 2, 2, 1, 1)

        self.label_133 = QLabel(self.frame_27)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setMinimumSize(QSize(30, 26))
        self.label_133.setMaximumSize(QSize(30, 26))
        self.label_133.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_133, 1, 3, 1, 1)

        self.label_76 = QLabel(self.frame_27)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setMinimumSize(QSize(90, 26))
        self.label_76.setMaximumSize(QSize(90, 26))
        self.label_76.setFont(font)
        self.label_76.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_76, 2, 1, 1, 1)

        self.lineEdit_t1_I_section = QLineEdit(self.frame_27)
        self.lineEdit_t1_I_section.setObjectName(u"lineEdit_t1_I_section")
        self.lineEdit_t1_I_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_t1_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_t1_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_t1_I_section.setFont(font)
        self.lineEdit_t1_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_t1_I_section.setStyleSheet(u"")
        self.lineEdit_t1_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_t1_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_t1_I_section, 3, 2, 1, 1)

        self.label_138 = QLabel(self.frame_27)
        self.label_138.setObjectName(u"label_138")
        self.label_138.setMinimumSize(QSize(30, 26))
        self.label_138.setMaximumSize(QSize(30, 26))
        self.label_138.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_138, 3, 3, 1, 1)

        self.label_74 = QLabel(self.frame_27)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setMinimumSize(QSize(90, 26))
        self.label_74.setMaximumSize(QSize(90, 26))
        self.label_74.setFont(font)
        self.label_74.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_74, 3, 1, 1, 1)

        self.label_141 = QLabel(self.frame_27)
        self.label_141.setObjectName(u"label_141")
        self.label_141.setMinimumSize(QSize(30, 26))
        self.label_141.setMaximumSize(QSize(30, 26))
        self.label_141.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_141, 2, 3, 1, 1)

        self.label_77 = QLabel(self.frame_27)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setMinimumSize(QSize(90, 26))
        self.label_77.setMaximumSize(QSize(90, 26))
        self.label_77.setFont(font)
        self.label_77.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_77, 4, 1, 1, 1)

        self.lineEdit_t2_I_section = QLineEdit(self.frame_27)
        self.lineEdit_t2_I_section.setObjectName(u"lineEdit_t2_I_section")
        self.lineEdit_t2_I_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_t2_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_t2_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_t2_I_section.setFont(font)
        self.lineEdit_t2_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_t2_I_section.setStyleSheet(u"")
        self.lineEdit_t2_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_t2_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_t2_I_section, 4, 2, 1, 1)

        self.label_136 = QLabel(self.frame_27)
        self.label_136.setObjectName(u"label_136")
        self.label_136.setMinimumSize(QSize(30, 26))
        self.label_136.setMaximumSize(QSize(30, 26))
        self.label_136.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_136, 4, 3, 1, 1)

        self.lineEdit_tw_I_section = QLineEdit(self.frame_27)
        self.lineEdit_tw_I_section.setObjectName(u"lineEdit_tw_I_section")
        self.lineEdit_tw_I_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_tw_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_tw_I_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_tw_I_section.setFont(font)
        self.lineEdit_tw_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_tw_I_section.setStyleSheet(u"")
        self.lineEdit_tw_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_tw_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_tw_I_section, 5, 2, 1, 1)

        self.label_134 = QLabel(self.frame_27)
        self.label_134.setObjectName(u"label_134")
        self.label_134.setMinimumSize(QSize(30, 26))
        self.label_134.setMaximumSize(QSize(30, 26))
        self.label_134.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_134, 5, 3, 1, 1)

        self.label_84 = QLabel(self.frame_27)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setMinimumSize(QSize(90, 26))
        self.label_84.setMaximumSize(QSize(90, 26))
        self.label_84.setFont(font)
        self.label_84.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_50.addWidget(self.label_84, 5, 1, 1, 1)

        self.label_140 = QLabel(self.frame_27)
        self.label_140.setObjectName(u"label_140")
        self.label_140.setMinimumSize(QSize(30, 26))
        self.label_140.setMaximumSize(QSize(30, 26))
        self.label_140.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_140, 6, 3, 1, 1)

        self.lineEdit_offsety_I_section = QLineEdit(self.frame_27)
        self.lineEdit_offsety_I_section.setObjectName(u"lineEdit_offsety_I_section")
        self.lineEdit_offsety_I_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsety_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsety_I_section.setFont(font)
        self.lineEdit_offsety_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsety_I_section.setStyleSheet(u"")
        self.lineEdit_offsety_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsety_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_offsety_I_section, 6, 2, 1, 1)

        self.label_137 = QLabel(self.frame_27)
        self.label_137.setObjectName(u"label_137")
        self.label_137.setMinimumSize(QSize(90, 26))
        self.label_137.setMaximumSize(QSize(90, 26))
        self.label_137.setFont(font)
        self.label_137.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_137, 6, 1, 1, 1)

        self.lineEdit_offsetz_I_section = QLineEdit(self.frame_27)
        self.lineEdit_offsetz_I_section.setObjectName(u"lineEdit_offsetz_I_section")
        self.lineEdit_offsetz_I_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsetz_I_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsetz_I_section.setFont(font)
        self.lineEdit_offsetz_I_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsetz_I_section.setStyleSheet(u"")
        self.lineEdit_offsetz_I_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsetz_I_section.setClearButtonEnabled(True)

        self.gridLayout_50.addWidget(self.lineEdit_offsetz_I_section, 7, 2, 1, 1)

        self.label_132 = QLabel(self.frame_27)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setMinimumSize(QSize(90, 26))
        self.label_132.setMaximumSize(QSize(90, 26))
        self.label_132.setFont(font)
        self.label_132.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_132, 7, 1, 1, 1)

        self.label_139 = QLabel(self.frame_27)
        self.label_139.setObjectName(u"label_139")
        self.label_139.setMinimumSize(QSize(30, 26))
        self.label_139.setMaximumSize(QSize(30, 26))
        self.label_139.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_50.addWidget(self.label_139, 7, 3, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_50.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)


        self.gridLayout_51.addWidget(self.frame_27, 0, 0, 1, 1)

        self.frame_22 = QFrame(self.tab_I_section)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_46 = QGridLayout(self.frame_22)
        self.gridLayout_46.setSpacing(0)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.gridLayout_46.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.frame_22)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(250, 310))
        self.label_10.setMaximumSize(QSize(250, 310))
        self.label_10.setPixmap(QPixmap(u":/icons/figures/I_profile.PNG"))
        self.label_10.setScaledContents(True)

        self.gridLayout_46.addWidget(self.label_10, 0, 0, 1, 1)


        self.gridLayout_51.addWidget(self.frame_22, 0, 1, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_I_section, "")
        self.tab_T_section = QWidget()
        self.tab_T_section.setObjectName(u"tab_T_section")
        self.gridLayout_53 = QGridLayout(self.tab_T_section)
        self.gridLayout_53.setSpacing(4)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.gridLayout_53.setContentsMargins(4, 4, 4, 4)
        self.frame_28 = QFrame(self.tab_T_section)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_52 = QGridLayout(self.frame_28)
        self.gridLayout_52.setSpacing(4)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.gridLayout_52.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_52.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

        self.lineEdit_tw_T_section = QLineEdit(self.frame_28)
        self.lineEdit_tw_T_section.setObjectName(u"lineEdit_tw_T_section")
        self.lineEdit_tw_T_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_tw_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_tw_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_tw_T_section.setFont(font)
        self.lineEdit_tw_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_tw_T_section.setStyleSheet(u"")
        self.lineEdit_tw_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_tw_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_tw_T_section, 3, 2, 1, 1)

        self.label_85 = QLabel(self.frame_28)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setMinimumSize(QSize(90, 26))
        self.label_85.setMaximumSize(QSize(90, 26))
        self.label_85.setFont(font)
        self.label_85.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_52.addWidget(self.label_85, 3, 1, 1, 1)

        self.label_145 = QLabel(self.frame_28)
        self.label_145.setObjectName(u"label_145")
        self.label_145.setMinimumSize(QSize(30, 26))
        self.label_145.setMaximumSize(QSize(30, 26))
        self.label_145.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_145, 2, 3, 1, 1)

        self.label_148 = QLabel(self.frame_28)
        self.label_148.setObjectName(u"label_148")
        self.label_148.setMinimumSize(QSize(90, 26))
        self.label_148.setMaximumSize(QSize(90, 26))
        self.label_148.setFont(font)
        self.label_148.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_148, 4, 1, 1, 1)

        self.label_153 = QLabel(self.frame_28)
        self.label_153.setObjectName(u"label_153")
        self.label_153.setMinimumSize(QSize(30, 26))
        self.label_153.setMaximumSize(QSize(30, 26))
        self.label_153.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_153, 3, 3, 1, 1)

        self.lineEdit_offsety_T_section = QLineEdit(self.frame_28)
        self.lineEdit_offsety_T_section.setObjectName(u"lineEdit_offsety_T_section")
        self.lineEdit_offsety_T_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsety_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsety_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offsety_T_section.setFont(font)
        self.lineEdit_offsety_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsety_T_section.setStyleSheet(u"")
        self.lineEdit_offsety_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsety_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_offsety_T_section, 4, 2, 1, 1)

        self.lineEdit_offsetz_T_section = QLineEdit(self.frame_28)
        self.lineEdit_offsetz_T_section.setObjectName(u"lineEdit_offsetz_T_section")
        self.lineEdit_offsetz_T_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_offsetz_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_offsetz_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_offsetz_T_section.setFont(font)
        self.lineEdit_offsetz_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_offsetz_T_section.setStyleSheet(u"")
        self.lineEdit_offsetz_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_offsetz_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_offsetz_T_section, 5, 2, 1, 1)

        self.label_143 = QLabel(self.frame_28)
        self.label_143.setObjectName(u"label_143")
        self.label_143.setMinimumSize(QSize(30, 26))
        self.label_143.setMaximumSize(QSize(30, 26))
        self.label_143.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_143, 5, 3, 1, 1)

        self.label_144 = QLabel(self.frame_28)
        self.label_144.setObjectName(u"label_144")
        self.label_144.setMinimumSize(QSize(30, 26))
        self.label_144.setMaximumSize(QSize(30, 26))
        self.label_144.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_144, 4, 3, 1, 1)

        self.label_149 = QLabel(self.frame_28)
        self.label_149.setObjectName(u"label_149")
        self.label_149.setMinimumSize(QSize(90, 26))
        self.label_149.setMaximumSize(QSize(90, 26))
        self.label_149.setFont(font)
        self.label_149.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_149, 5, 1, 1, 1)

        self.label_87 = QLabel(self.frame_28)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setMinimumSize(QSize(90, 26))
        self.label_87.setMaximumSize(QSize(90, 26))
        self.label_87.setFont(font)
        self.label_87.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_52.addWidget(self.label_87, 0, 1, 1, 1)

        self.label_152 = QLabel(self.frame_28)
        self.label_152.setObjectName(u"label_152")
        self.label_152.setMinimumSize(QSize(30, 26))
        self.label_152.setMaximumSize(QSize(30, 26))
        self.label_152.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_152, 0, 3, 1, 1)

        self.lineEdit_height_T_section = QLineEdit(self.frame_28)
        self.lineEdit_height_T_section.setObjectName(u"lineEdit_height_T_section")
        self.lineEdit_height_T_section.setMinimumSize(QSize(120, 26))
        self.lineEdit_height_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_height_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_height_T_section.setFont(font)
        self.lineEdit_height_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_height_T_section.setStyleSheet(u"")
        self.lineEdit_height_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_height_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_height_T_section, 0, 2, 1, 1)

        self.label_151 = QLabel(self.frame_28)
        self.label_151.setObjectName(u"label_151")
        self.label_151.setMinimumSize(QSize(30, 26))
        self.label_151.setMaximumSize(QSize(30, 26))
        self.label_151.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_52.addWidget(self.label_151, 1, 3, 1, 1)

        self.lineEdit_w1_T_section = QLineEdit(self.frame_28)
        self.lineEdit_w1_T_section.setObjectName(u"lineEdit_w1_T_section")
        self.lineEdit_w1_T_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_w1_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_w1_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_w1_T_section.setFont(font)
        self.lineEdit_w1_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_w1_T_section.setStyleSheet(u"")
        self.lineEdit_w1_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_w1_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_w1_T_section, 1, 2, 1, 1)

        self.label_83 = QLabel(self.frame_28)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setMinimumSize(QSize(90, 26))
        self.label_83.setMaximumSize(QSize(90, 26))
        self.label_83.setFont(font)
        self.label_83.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_52.addWidget(self.label_83, 1, 1, 1, 1)

        self.lineEdit_t1_T_section = QLineEdit(self.frame_28)
        self.lineEdit_t1_T_section.setObjectName(u"lineEdit_t1_T_section")
        self.lineEdit_t1_T_section.setMinimumSize(QSize(120, 24))
        self.lineEdit_t1_T_section.setMaximumSize(QSize(120, 26))
        self.lineEdit_t1_T_section.setSizeIncrement(QSize(0, 0))
        self.lineEdit_t1_T_section.setFont(font)
        self.lineEdit_t1_T_section.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_t1_T_section.setStyleSheet(u"")
        self.lineEdit_t1_T_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_t1_T_section.setClearButtonEnabled(True)

        self.gridLayout_52.addWidget(self.lineEdit_t1_T_section, 2, 2, 1, 1)

        self.label_81 = QLabel(self.frame_28)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setMinimumSize(QSize(90, 26))
        self.label_81.setMaximumSize(QSize(90, 26))
        self.label_81.setFont(font)
        self.label_81.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_52.addWidget(self.label_81, 2, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_52.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)


        self.gridLayout_53.addWidget(self.frame_28, 0, 0, 1, 1)

        self.frame_21 = QFrame(self.tab_T_section)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_45 = QGridLayout(self.frame_21)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.gridLayout_45.setVerticalSpacing(0)
        self.gridLayout_45.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_21)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(250, 310))
        self.label_11.setMaximumSize(QSize(250, 310))
        self.label_11.setPixmap(QPixmap(u":/icons/figures/T_profile.PNG"))
        self.label_11.setScaledContents(True)

        self.gridLayout_45.addWidget(self.label_11, 0, 0, 1, 1)


        self.gridLayout_53.addWidget(self.frame_21, 0, 1, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_T_section, "")
        self.tab_generic_section = QWidget()
        self.tab_generic_section.setObjectName(u"tab_generic_section")
        self.gridLayout_8 = QGridLayout(self.tab_generic_section)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab_generic_section)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(100, 250))
        self.frame_7.setMaximumSize(QSize(800, 250))
        self.frame_7.setStyleSheet(u"")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(8)
        self.gridLayout_7.setVerticalSpacing(10)
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.label_12 = QLabel(self.frame_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_12, 4, 1, 1, 1)

        self.label_15 = QLabel(self.frame_7)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_15, 1, 3, 1, 1)

        self.label_13 = QLabel(self.frame_7)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_13, 0, 3, 1, 1)

        self.label_16 = QLabel(self.frame_7)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_16, 2, 3, 1, 1)

        self.label_31 = QLabel(self.frame_7)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_31, 3, 3, 1, 1)

        self.lineEdit_Izz = QLineEdit(self.frame_7)
        self.lineEdit_Izz.setObjectName(u"lineEdit_Izz")
        self.lineEdit_Izz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Izz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Izz.setFont(font)
        self.lineEdit_Izz.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_Izz.setStyleSheet(u"")
        self.lineEdit_Izz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Izz.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_Izz, 2, 2, 1, 1)

        self.lineEdit_area = QLineEdit(self.frame_7)
        self.lineEdit_area.setObjectName(u"lineEdit_area")
        self.lineEdit_area.setMinimumSize(QSize(120, 26))
        self.lineEdit_area.setMaximumSize(QSize(120, 26))
        self.lineEdit_area.setFont(font)
        self.lineEdit_area.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_area.setStyleSheet(u"")
        self.lineEdit_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_area.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_area, 0, 2, 1, 1)

        self.lineEdit_Iyy = QLineEdit(self.frame_7)
        self.lineEdit_Iyy.setObjectName(u"lineEdit_Iyy")
        self.lineEdit_Iyy.setMinimumSize(QSize(120, 26))
        self.lineEdit_Iyy.setMaximumSize(QSize(120, 26))
        self.lineEdit_Iyy.setFont(font)
        self.lineEdit_Iyy.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_Iyy.setStyleSheet(u"")
        self.lineEdit_Iyy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Iyy.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_Iyy, 1, 2, 1, 1)

        self.lineEdit_Iyz = QLineEdit(self.frame_7)
        self.lineEdit_Iyz.setObjectName(u"lineEdit_Iyz")
        self.lineEdit_Iyz.setMinimumSize(QSize(120, 26))
        self.lineEdit_Iyz.setMaximumSize(QSize(120, 26))
        self.lineEdit_Iyz.setFont(font)
        self.lineEdit_Iyz.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_Iyz.setStyleSheet(u"")
        self.lineEdit_Iyz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Iyz.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_Iyz, 3, 2, 1, 1)

        self.lineEdit_shear_coefficient = QLineEdit(self.frame_7)
        self.lineEdit_shear_coefficient.setObjectName(u"lineEdit_shear_coefficient")
        self.lineEdit_shear_coefficient.setMinimumSize(QSize(120, 26))
        self.lineEdit_shear_coefficient.setMaximumSize(QSize(120, 26))
        self.lineEdit_shear_coefficient.setFont(font)
        self.lineEdit_shear_coefficient.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_shear_coefficient.setStyleSheet(u"")
        self.lineEdit_shear_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_shear_coefficient.setClearButtonEnabled(True)

        self.gridLayout_7.addWidget(self.lineEdit_shear_coefficient, 4, 2, 1, 1)

        self.label = QLabel(self.frame_7)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_5 = QLabel(self.frame_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_5, 3, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.gridLayout_8.addWidget(self.frame_7, 1, 0, 1, 1)

        self.frame_8 = QFrame(self.tab_generic_section)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_8)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.label_44 = QLabel(self.frame_8)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(380, 40))
        self.label_44.setMaximumSize(QSize(420, 40))
        self.label_44.setFont(font)
        self.label_44.setFrameShape(QFrame.Shape.Box)
        self.label_44.setFrameShadow(QFrame.Shadow.Raised)
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_44, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_8, 0, 0, 1, 1)

        self.tabWidget_beam_section.addTab(self.tab_generic_section, "")

        self.gridLayout_33.addWidget(self.tabWidget_beam_section, 1, 0, 1, 1)

        self.frame_16 = QFrame(self.tab_beam)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 52))
        self.frame_16.setMaximumSize(QSize(16777215, 52))
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_34 = QGridLayout(self.frame_16)
        self.gridLayout_34.setSpacing(4)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setContentsMargins(4, 4, 4, 4)
        self.pushButton_confirm_beam = QPushButton(self.frame_16)
        self.pushButton_confirm_beam.setObjectName(u"pushButton_confirm_beam")
        self.pushButton_confirm_beam.setMinimumSize(QSize(140, 30))
        self.pushButton_confirm_beam.setMaximumSize(QSize(140, 30))
        self.pushButton_confirm_beam.setFont(font)
        self.pushButton_confirm_beam.setStyleSheet(u"")

        self.gridLayout_34.addWidget(self.pushButton_confirm_beam, 0, 3, 1, 1)

        self.pushButton_plot_beam_cross_section = QPushButton(self.frame_16)
        self.pushButton_plot_beam_cross_section.setObjectName(u"pushButton_plot_beam_cross_section")
        self.pushButton_plot_beam_cross_section.setMinimumSize(QSize(140, 30))
        self.pushButton_plot_beam_cross_section.setMaximumSize(QSize(140, 30))
        self.pushButton_plot_beam_cross_section.setFont(font)
        self.pushButton_plot_beam_cross_section.setStyleSheet(u"")

        self.gridLayout_34.addWidget(self.pushButton_plot_beam_cross_section, 0, 1, 1, 1)

        self.pushButton_exit_beam = QPushButton(self.frame_16)
        self.pushButton_exit_beam.setObjectName(u"pushButton_exit_beam")
        self.pushButton_exit_beam.setMinimumSize(QSize(140, 30))
        self.pushButton_exit_beam.setMaximumSize(QSize(140, 30))
        self.pushButton_exit_beam.setFont(font)
        self.pushButton_exit_beam.setStyleSheet(u"")

        self.gridLayout_34.addWidget(self.pushButton_exit_beam, 0, 0, 1, 1)


        self.gridLayout_33.addWidget(self.frame_16, 2, 0, 1, 1)

        self.tabWidget_general.addTab(self.tab_beam, "")
        self.tab_sections = QWidget()
        self.tab_sections.setObjectName(u"tab_sections")
        self.gridLayout_25 = QGridLayout(self.tab_sections)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(6, 6, 6, 6)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_25.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_25.addItem(self.verticalSpacer_5, 0, 0, 1, 1)

        self.frame_23 = QFrame(self.tab_sections)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(0, 52))
        self.frame_23.setMaximumSize(QSize(16777215, 52))
        self.frame_23.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_23)
        self.gridLayout_24.setSpacing(4)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(4, 4, 4, 4)
        self.pushButton_load_section_data = QPushButton(self.frame_23)
        self.pushButton_load_section_data.setObjectName(u"pushButton_load_section_data")
        self.pushButton_load_section_data.setMinimumSize(QSize(120, 30))
        self.pushButton_load_section_data.setMaximumSize(QSize(140, 30))
        self.pushButton_load_section_data.setFont(font)
        self.pushButton_load_section_data.setStyleSheet(u"")

        self.gridLayout_24.addWidget(self.pushButton_load_section_data, 0, 1, 1, 1)

        self.pushButton_edit_section_data = QPushButton(self.frame_23)
        self.pushButton_edit_section_data.setObjectName(u"pushButton_edit_section_data")
        self.pushButton_edit_section_data.setMinimumSize(QSize(120, 30))
        self.pushButton_edit_section_data.setMaximumSize(QSize(140, 30))
        self.pushButton_edit_section_data.setFont(font)
        self.pushButton_edit_section_data.setStyleSheet(u"")

        self.gridLayout_24.addWidget(self.pushButton_edit_section_data, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.frame_23, 3, 0, 1, 1)

        self.treeWidget_lines_info = QTreeWidget(self.tab_sections)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_lines_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_lines_info.setObjectName(u"treeWidget_lines_info")
        self.treeWidget_lines_info.setMinimumSize(QSize(500, 300))
        self.treeWidget_lines_info.setMaximumSize(QSize(580, 360))
        self.treeWidget_lines_info.setFont(font)
        self.treeWidget_lines_info.setIndentation(1)
        self.treeWidget_lines_info.setHeaderHidden(False)
        self.treeWidget_lines_info.header().setHighlightSections(False)
        self.treeWidget_lines_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_lines_info.header().setStretchLastSection(True)

        self.gridLayout_25.addWidget(self.treeWidget_lines_info, 1, 0, 1, 1)

        self.tabWidget_general.addTab(self.tab_sections, "")

        self.gridLayout.addWidget(self.tabWidget_general, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_general, self.tabWidget_pipe_section)
        QWidget.setTabOrder(self.tabWidget_pipe_section, self.pushButton_select_standard_section)
        QWidget.setTabOrder(self.pushButton_select_standard_section, self.lineEdit_outside_diameter)
        QWidget.setTabOrder(self.lineEdit_outside_diameter, self.lineEdit_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_wall_thickness, self.lineEdit_offset_y)
        QWidget.setTabOrder(self.lineEdit_offset_y, self.lineEdit_offset_z)
        QWidget.setTabOrder(self.lineEdit_offset_z, self.lineEdit_insulation_thickness)
        QWidget.setTabOrder(self.lineEdit_insulation_thickness, self.lineEdit_insulation_density)
        QWidget.setTabOrder(self.lineEdit_insulation_density, self.pushButton_check_if_section_is_normalized)
        QWidget.setTabOrder(self.pushButton_check_if_section_is_normalized, self.pushButton_plot_pipe_cross_section)
        QWidget.setTabOrder(self.pushButton_plot_pipe_cross_section, self.pushButton_confirm_pipe)
        QWidget.setTabOrder(self.pushButton_confirm_pipe, self.lineEdit_element_id_initial)
        QWidget.setTabOrder(self.lineEdit_element_id_initial, self.lineEdit_outside_diameter_initial)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_initial, self.lineEdit_wall_thickness_initial)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_initial, self.lineEdit_offset_y_initial)
        QWidget.setTabOrder(self.lineEdit_offset_y_initial, self.lineEdit_offset_z_initial)
        QWidget.setTabOrder(self.lineEdit_offset_z_initial, self.pushButton_select_standard_section_initial)
        QWidget.setTabOrder(self.pushButton_select_standard_section_initial, self.lineEdit_element_id_final)
        QWidget.setTabOrder(self.lineEdit_element_id_final, self.lineEdit_outside_diameter_final)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_final, self.lineEdit_wall_thickness_final)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_final, self.lineEdit_offset_y_final)
        QWidget.setTabOrder(self.lineEdit_offset_y_final, self.lineEdit_offset_z_final)
        QWidget.setTabOrder(self.lineEdit_offset_z_final, self.pushButton_select_standard_section_final)
        QWidget.setTabOrder(self.pushButton_select_standard_section_final, self.lineEdit_insulation_thickness_variable_section)
        QWidget.setTabOrder(self.lineEdit_insulation_thickness_variable_section, self.lineEdit_insulation_density_variable_section)
        QWidget.setTabOrder(self.lineEdit_insulation_density_variable_section, self.tabWidget_beam_section)
        QWidget.setTabOrder(self.tabWidget_beam_section, self.lineEdit_base_rectangular_section)
        QWidget.setTabOrder(self.lineEdit_base_rectangular_section, self.lineEdit_height_rectangular_section)
        QWidget.setTabOrder(self.lineEdit_height_rectangular_section, self.lineEdit_wall_thickness_rectangular_section)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_rectangular_section, self.lineEdit_offsety_rectangular_section)
        QWidget.setTabOrder(self.lineEdit_offsety_rectangular_section, self.lineEdit_offsetz_rectangular_section)
        QWidget.setTabOrder(self.lineEdit_offsetz_rectangular_section, self.pushButton_plot_beam_cross_section)
        QWidget.setTabOrder(self.pushButton_plot_beam_cross_section, self.pushButton_confirm_beam)
        QWidget.setTabOrder(self.pushButton_confirm_beam, self.lineEdit_outside_diameter_circular_section)
        QWidget.setTabOrder(self.lineEdit_outside_diameter_circular_section, self.lineEdit_wall_thickness_circular_section)
        QWidget.setTabOrder(self.lineEdit_wall_thickness_circular_section, self.lineEdit_offsety_circular_section)
        QWidget.setTabOrder(self.lineEdit_offsety_circular_section, self.lineEdit_offsetz_circular_section)
        QWidget.setTabOrder(self.lineEdit_offsetz_circular_section, self.lineEdit_height_C_section)
        QWidget.setTabOrder(self.lineEdit_height_C_section, self.lineEdit_w1_C_section)
        QWidget.setTabOrder(self.lineEdit_w1_C_section, self.lineEdit_w2_C_section)
        QWidget.setTabOrder(self.lineEdit_w2_C_section, self.lineEdit_t1_C_section)
        QWidget.setTabOrder(self.lineEdit_t1_C_section, self.lineEdit_t2_C_section)
        QWidget.setTabOrder(self.lineEdit_t2_C_section, self.lineEdit_tw_C_section)
        QWidget.setTabOrder(self.lineEdit_tw_C_section, self.lineEdit_offsety_C_section)
        QWidget.setTabOrder(self.lineEdit_offsety_C_section, self.lineEdit_offsetz_C_section)
        QWidget.setTabOrder(self.lineEdit_offsetz_C_section, self.lineEdit_height_I_section)
        QWidget.setTabOrder(self.lineEdit_height_I_section, self.lineEdit_w1_I_section)
        QWidget.setTabOrder(self.lineEdit_w1_I_section, self.lineEdit_w2_I_section)
        QWidget.setTabOrder(self.lineEdit_w2_I_section, self.lineEdit_t1_I_section)
        QWidget.setTabOrder(self.lineEdit_t1_I_section, self.lineEdit_t2_I_section)
        QWidget.setTabOrder(self.lineEdit_t2_I_section, self.lineEdit_tw_I_section)
        QWidget.setTabOrder(self.lineEdit_tw_I_section, self.lineEdit_offsety_I_section)
        QWidget.setTabOrder(self.lineEdit_offsety_I_section, self.lineEdit_offsetz_I_section)
        QWidget.setTabOrder(self.lineEdit_offsetz_I_section, self.lineEdit_height_T_section)
        QWidget.setTabOrder(self.lineEdit_height_T_section, self.lineEdit_w1_T_section)
        QWidget.setTabOrder(self.lineEdit_w1_T_section, self.lineEdit_t1_T_section)
        QWidget.setTabOrder(self.lineEdit_t1_T_section, self.lineEdit_tw_T_section)
        QWidget.setTabOrder(self.lineEdit_tw_T_section, self.lineEdit_offsety_T_section)
        QWidget.setTabOrder(self.lineEdit_offsety_T_section, self.lineEdit_offsetz_T_section)
        QWidget.setTabOrder(self.lineEdit_offsetz_T_section, self.lineEdit_area)
        QWidget.setTabOrder(self.lineEdit_area, self.lineEdit_Iyy)
        QWidget.setTabOrder(self.lineEdit_Iyy, self.lineEdit_Izz)
        QWidget.setTabOrder(self.lineEdit_Izz, self.lineEdit_Iyz)
        QWidget.setTabOrder(self.lineEdit_Iyz, self.lineEdit_shear_coefficient)
        QWidget.setTabOrder(self.lineEdit_shear_coefficient, self.pushButton_load_section_data)

        self.retranslateUi(Form)

        self.tabWidget_general.setCurrentIndex(0)
        self.pushButton_confirm_pipe.setDefault(False)
        self.pushButton_exit_pipe.setDefault(False)
        self.tabWidget_pipe_section.setCurrentIndex(0)
        self.tabWidget_beam_section.setCurrentIndex(0)
        self.pushButton_confirm_beam.setDefault(False)
        self.pushButton_exit_beam.setDefault(False)
        self.pushButton_load_section_data.setDefault(True)
        self.pushButton_edit_section_data.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_confirm_pipe.setText(QCoreApplication.translate("Form", u"Confirm", None))
#if QT_CONFIG(shortcut)
        self.pushButton_confirm_pipe.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_exit_pipe.setText(QCoreApplication.translate("Form", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.pushButton_exit_pipe.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_plot_pipe_cross_section.setText(QCoreApplication.translate("Form", u"Plot cross-section", None))
        self.pushButton_select_standard_section.setText(QCoreApplication.translate("Form", u"Get a standardized section", None))
        self.pushButton_check_if_section_is_normalized.setText(QCoreApplication.translate("Form", u"Check if section is normalized", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>[m]</p></body></html>", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Outside diameter (d<span style=\" vertical-align:sub;\">out</span>):</p></body></html>", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_42.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_41.setText(QCoreApplication.translate("Form", u"[kg/m\u00b3]", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Insulation density:</p></body></html>", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Insulation thickness (t<span style=\" vertical-align:sub;\">i</span>):</p></body></html>", None))
        self.lineEdit_outside_diameter.setText("")
        self.label_18.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Wall thickness (t):</p></body></html>", None))
        self.label_14.setText("")
        self.tabWidget_pipe_section.setTabText(self.tabWidget_pipe_section.indexOf(self.tab_constant_pipe_section), QCoreApplication.translate("Form", u"Constant section", None))
        self.pushButton_select_standard_section_initial.setText(QCoreApplication.translate("Form", u"Get section", None))
        self.pushButton_select_standard_section_final.setText(QCoreApplication.translate("Form", u"Get section", None))
        self.label_82.setText(QCoreApplication.translate("Form", u"Offset y:", None))
        self.label_element_id.setText(QCoreApplication.translate("Form", u"Element id:", None))
        self.label_63.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.lineEdit_outside_diameter_initial.setText("")
        self.label_62.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_89.setText(QCoreApplication.translate("Form", u"Offset z:", None))
        self.label_86.setText(QCoreApplication.translate("Form", u"Wall thickness:", None))
        self.label_90.setText(QCoreApplication.translate("Form", u"Outside diameter:", None))
        self.label_80.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_66.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_91.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_64.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_36.setText(QCoreApplication.translate("Form", u"Final section data", None))
        self.label_37.setText(QCoreApplication.translate("Form", u"Initial section data", None))
        self.lineEdit_element_id_initial.setText("")
        self.lineEdit_element_id_final.setText("")
        self.label_79.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.lineEdit_outside_diameter_final.setText("")
        self.label_88.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.pushButton_invert_input_values.setText("")
        self.label_48.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Insulation density:</p></body></html>", None))
        self.label_46.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Insulation thickness:</p></body></html>", None))
        self.label_45.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"[kg/m\u00b3]", None))
        self.tabWidget_pipe_section.setTabText(self.tabWidget_pipe_section.indexOf(self.tab_variable_pipe_section), QCoreApplication.translate("Form", u"Variable section", None))
        self.tabWidget_general.setTabText(self.tabWidget_general.indexOf(self.tab_pipe), QCoreApplication.translate("Form", u"Pipe", None))
        self.label_109.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_112.setText(QCoreApplication.translate("Form", u"wall thickness (t):", None))
        self.label_113.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_94.setText(QCoreApplication.translate("Form", u"height (h):", None))
        self.label_110.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_100.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_114.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_107.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_72.setText(QCoreApplication.translate("Form", u"base (b):", None))
        self.label_111.setText(QCoreApplication.translate("Form", u"[m]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_wall_thickness_rectangular_section.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Insert a value for wall thickness.</p><p>(*) Let the input field blank for massive beam.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText("")
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_rectangular_section), QCoreApplication.translate("Form", u"Rectangular", None))
        self.label_43.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">outside diameter (d<span style=\" vertical-align:sub;\">out</span>):</p></body></html>", None))
        self.label_115.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.lineEdit_outside_diameter_circular_section.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_wall_thickness_circular_section.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Insert a value for wall thickness.</p><p>(*) Let the input field blank for massive beam.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_65.setText(QCoreApplication.translate("Form", u"wall thickness (t):", None))
        self.label_118.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_116.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_119.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_120.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_117.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_7.setText("")
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_circular_section), QCoreApplication.translate("Form", u"Circular", None))
        self.label_67.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">h:</p></body></html>", None))
        self.label_68.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">w<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_121.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_122.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_69.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">w<span style=\" vertical-align:sub;\">2</span>:</p></body></html>", None))
        self.label_123.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_70.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_71.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">2</span>:</p></body></html>", None))
        self.label_124.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_125.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_73.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">w</span>:</p></body></html>", None))
        self.label_131.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_126.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_128.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_130.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_129.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_9.setText("")
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_C_section), QCoreApplication.translate("Form", u"C-beam", None))
        self.label_78.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">h:</p></body></html>", None))
        self.label_75.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">w<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_142.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_133.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_76.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">w<span style=\" vertical-align:sub;\">2</span>:</p></body></html>", None))
        self.label_138.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_74.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_141.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_77.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">2</span>:</p></body></html>", None))
        self.label_136.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_134.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_84.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">w</span>:</p></body></html>", None))
        self.label_140.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_137.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_132.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_139.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_10.setText("")
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_I_section), QCoreApplication.translate("Form", u"I-beam", None))
        self.label_85.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">w</span>:</p></body></html>", None))
        self.label_145.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_148.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset y (e<span style=\" vertical-align:sub;\">y</span>):</p></body></html>", None))
        self.label_153.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_143.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_144.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_149.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">offset z (e<span style=\" vertical-align:sub;\">z</span>):</p></body></html>", None))
        self.label_87.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">h:</p></body></html>", None))
        self.label_152.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_151.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_83.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">w<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_81.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">t<span style=\" vertical-align:sub;\">1</span>:</p></body></html>", None))
        self.label_11.setText("")
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_T_section), QCoreApplication.translate("Form", u"T-beam", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Shear factor:", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"[m^4]", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"[m^2]", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"[m^4]", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"[m^4]", None))
        self.lineEdit_shear_coefficient.setText(QCoreApplication.translate("Form", u"1", None))
        self.label.setText(QCoreApplication.translate("Form", u"Area:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Izz:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Iyy:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Iyz:", None))
        self.label_44.setText(QCoreApplication.translate("Form", u"Insert the section properties of generic beam element", None))
        self.tabWidget_beam_section.setTabText(self.tabWidget_beam_section.indexOf(self.tab_generic_section), QCoreApplication.translate("Form", u"Generic", None))
        self.pushButton_confirm_beam.setText(QCoreApplication.translate("Form", u"Confirm", None))
#if QT_CONFIG(shortcut)
        self.pushButton_confirm_beam.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_plot_beam_cross_section.setText(QCoreApplication.translate("Form", u"Plot cross-section", None))
        self.pushButton_exit_beam.setText(QCoreApplication.translate("Form", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.pushButton_exit_beam.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget_general.setTabText(self.tabWidget_general.indexOf(self.tab_beam), QCoreApplication.translate("Form", u"Beam", None))
        self.pushButton_load_section_data.setText(QCoreApplication.translate("Form", u"Load section data", None))
        self.pushButton_edit_section_data.setText(QCoreApplication.translate("Form", u"Edit section data", None))
        ___qtreewidgetitem = self.treeWidget_lines_info.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Form", u"Section parameters", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"Section type", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Element type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"ID", None))
        self.tabWidget_general.setTabText(self.tabWidget_general.indexOf(self.tab_sections), QCoreApplication.translate("Form", u"Active sections", None))
    # retranslateUi



class CrossSectionWidget_UI(QDialog, Ui_Form):
    """
    Component Hierarchy:
    - Form: QDialog
        - (Layout): QGridLayout
                - tabWidget_general: QTabWidget
                    - tab_pipe: QWidget
                        - (Layout): QGridLayout
                                - bottom_frame_buttons: QFrame
                                    - (Layout): QGridLayout
                                            - pushButton_confirm_pipe: QPushButton
                                            - pushButton_exit_pipe: QPushButton
                                            - pushButton_plot_pipe_cross_section: QPushButton
                                - tabWidget_pipe_section: QTabWidget
                                    - tab_constant_pipe_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_31: QFrame
                                                    - (Layout): QGridLayout
                                                            - pushButton_select_standard_section: QPushButton
                                                            - pushButton_check_if_section_is_normalized: QPushButton
                                                - frame_2: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_17: QLabel
                                                            - label_20: QLabel
                                                            - lineEdit_offset_y: QLineEdit
                                                            - label_22: QLabel
                                                            - lineEdit_insulation_thickness: QLineEdit
                                                            - label_42: QLabel
                                                            - lineEdit_offset_z: QLineEdit
                                                            - label_41: QLabel
                                                            - lineEdit_insulation_density: QLineEdit
                                                            - label_23: QLabel
                                                            - label_25: QLabel
                                                            - label_26: QLabel
                                                            - lineEdit_outside_diameter: QLineEdit
                                                            - label_18: QLabel
                                                            - label_19: QLabel
                                                            - lineEdit_wall_thickness: QLineEdit
                                                            - label_24: QLabel
                                                            - label_21: QLabel
                                                - frame_30: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_14: QLabel
                                    - tab_variable_pipe_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame: QFrame
                                                    - (Layout): QGridLayout
                                                            - frame_10: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_select_standard_section_initial: QPushButton
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_select_standard_section_final: QPushButton
                                                            - label_82: QLabel
                                                            - lineEdit_offset_y_final: QLineEdit
                                                            - label_element_id: QLabel
                                                            - label_63: QLabel
                                                            - lineEdit_outside_diameter_initial: QLineEdit
                                                            - label_62: QLabel
                                                            - label_89: QLabel
                                                            - label_86: QLabel
                                                            - label_90: QLabel
                                                            - lineEdit_wall_thickness_final: QLineEdit
                                                            - label_80: QLabel
                                                            - label_66: QLabel
                                                            - lineEdit_offset_z_initial: QLineEdit
                                                            - lineEdit_offset_y_initial: QLineEdit
                                                            - lineEdit_offset_z_final: QLineEdit
                                                            - label_91: QLabel
                                                            - label_64: QLabel
                                                            - frame_6: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_36: QLabel
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_37: QLabel
                                                            - lineEdit_element_id_initial: QLineEdit
                                                            - lineEdit_element_id_final: QLineEdit
                                                            - label_79: QLabel
                                                            - lineEdit_wall_thickness_initial: QLineEdit
                                                            - lineEdit_outside_diameter_final: QLineEdit
                                                            - label_88: QLabel
                                                            - frame_11: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_invert_input_values: QPushButton
                                                - frame_20: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_48: QLabel
                                                            - lineEdit_insulation_density_variable_section: QLineEdit
                                                            - label_46: QLabel
                                                            - label_45: QLabel
                                                            - label_47: QLabel
                                                            - lineEdit_insulation_thickness_variable_section: QLineEdit
                    - tab_beam: QWidget
                        - (Layout): QGridLayout
                                - tabWidget_beam_section: QTabWidget
                                    - tab_rectangular_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_9: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_109: QLabel
                                                            - label_112: QLabel
                                                            - label_113: QLabel
                                                            - lineEdit_base_rectangular_section: QLineEdit
                                                            - label_94: QLabel
                                                            - label_110: QLabel
                                                            - label_100: QLabel
                                                            - label_114: QLabel
                                                            - lineEdit_offsety_rectangular_section: QLineEdit
                                                            - lineEdit_height_rectangular_section: QLineEdit
                                                            - label_107: QLabel
                                                            - label_72: QLabel
                                                            - label_111: QLabel
                                                            - lineEdit_offsetz_rectangular_section: QLineEdit
                                                            - lineEdit_wall_thickness_rectangular_section: QLineEdit
                                                - frame_17: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_4: QLabel
                                    - tab_circular_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_14: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_43: QLabel
                                                            - label_115: QLabel
                                                            - lineEdit_outside_diameter_circular_section: QLineEdit
                                                            - lineEdit_wall_thickness_circular_section: QLineEdit
                                                            - label_65: QLabel
                                                            - label_118: QLabel
                                                            - label_116: QLabel
                                                            - label_119: QLabel
                                                            - label_120: QLabel
                                                            - label_117: QLabel
                                                            - lineEdit_offsety_circular_section: QLineEdit
                                                            - lineEdit_offsetz_circular_section: QLineEdit
                                                - frame_15: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_7: QLabel
                                    - tab_C_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_26: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_67: QLabel
                                                            - label_68: QLabel
                                                            - lineEdit_height_C_section: QLineEdit
                                                            - label_121: QLabel
                                                            - label_122: QLabel
                                                            - label_69: QLabel
                                                            - lineEdit_w1_C_section: QLineEdit
                                                            - lineEdit_w2_C_section: QLineEdit
                                                            - label_123: QLabel
                                                            - label_70: QLabel
                                                            - lineEdit_t1_C_section: QLineEdit
                                                            - lineEdit_t2_C_section: QLineEdit
                                                            - label_71: QLabel
                                                            - label_124: QLabel
                                                            - lineEdit_tw_C_section: QLineEdit
                                                            - label_125: QLabel
                                                            - label_73: QLabel
                                                            - label_131: QLabel
                                                            - lineEdit_offsety_C_section: QLineEdit
                                                            - label_126: QLabel
                                                            - lineEdit_offsetz_C_section: QLineEdit
                                                            - label_128: QLabel
                                                            - label_130: QLabel
                                                            - label_129: QLabel
                                                - frame_25: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_9: QLabel
                                    - tab_I_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_27: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_78: QLabel
                                                            - lineEdit_height_I_section: QLineEdit
                                                            - lineEdit_w1_I_section: QLineEdit
                                                            - label_75: QLabel
                                                            - label_142: QLabel
                                                            - lineEdit_w2_I_section: QLineEdit
                                                            - label_133: QLabel
                                                            - label_76: QLabel
                                                            - lineEdit_t1_I_section: QLineEdit
                                                            - label_138: QLabel
                                                            - label_74: QLabel
                                                            - label_141: QLabel
                                                            - label_77: QLabel
                                                            - lineEdit_t2_I_section: QLineEdit
                                                            - label_136: QLabel
                                                            - lineEdit_tw_I_section: QLineEdit
                                                            - label_134: QLabel
                                                            - label_84: QLabel
                                                            - label_140: QLabel
                                                            - lineEdit_offsety_I_section: QLineEdit
                                                            - label_137: QLabel
                                                            - lineEdit_offsetz_I_section: QLineEdit
                                                            - label_132: QLabel
                                                            - label_139: QLabel
                                                - frame_22: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_10: QLabel
                                    - tab_T_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_28: QFrame
                                                    - (Layout): QGridLayout
                                                            - lineEdit_tw_T_section: QLineEdit
                                                            - label_85: QLabel
                                                            - label_145: QLabel
                                                            - label_148: QLabel
                                                            - label_153: QLabel
                                                            - lineEdit_offsety_T_section: QLineEdit
                                                            - lineEdit_offsetz_T_section: QLineEdit
                                                            - label_143: QLabel
                                                            - label_144: QLabel
                                                            - label_149: QLabel
                                                            - label_87: QLabel
                                                            - label_152: QLabel
                                                            - lineEdit_height_T_section: QLineEdit
                                                            - label_151: QLabel
                                                            - lineEdit_w1_T_section: QLineEdit
                                                            - label_83: QLabel
                                                            - lineEdit_t1_T_section: QLineEdit
                                                            - label_81: QLabel
                                                - frame_21: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_11: QLabel
                                    - tab_generic_section: QWidget
                                        - (Layout): QGridLayout
                                                - frame_7: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_12: QLabel
                                                            - label_15: QLabel
                                                            - label_13: QLabel
                                                            - label_16: QLabel
                                                            - label_31: QLabel
                                                            - lineEdit_Izz: QLineEdit
                                                            - lineEdit_area: QLineEdit
                                                            - lineEdit_Iyy: QLineEdit
                                                            - lineEdit_Iyz: QLineEdit
                                                            - lineEdit_shear_coefficient: QLineEdit
                                                            - label: QLabel
                                                            - label_3: QLabel
                                                            - label_2: QLabel
                                                            - label_5: QLabel
                                                - frame_8: QFrame
                                                    - (Layout): QGridLayout
                                                            - label_44: QLabel
                                - frame_16: QFrame
                                    - (Layout): QGridLayout
                                            - pushButton_confirm_beam: QPushButton
                                            - pushButton_plot_beam_cross_section: QPushButton
                                            - pushButton_exit_beam: QPushButton
                    - tab_sections: QWidget
                        - (Layout): QGridLayout
                                - frame_23: QFrame
                                    - (Layout): QGridLayout
                                            - pushButton_load_section_data: QPushButton
                                            - pushButton_edit_section_data: QPushButton
                                - treeWidget_lines_info: QTreeWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
