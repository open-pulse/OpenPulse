# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsation_suppression_device_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1191, 663)
        Dialog.setMinimumSize(QSize(400, 0))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(400, 400))
        font = QFont()
        font.setPointSize(10)
        self.tabWidget_main.setFont(font)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_7 = QGridLayout(self.tab_setup)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(self.tab_setup)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scroll_main = QWidget()
        self.scroll_main.setObjectName(u"scroll_main")
        self.scroll_main.setGeometry(QRect(0, 0, 571, 688))
        self.gridLayout_8 = QGridLayout(self.scroll_main)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.scroll_main)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 44))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 2)
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_7, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 26))
        self.label_12.setMaximumSize(QSize(100, 26))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_12, 1, 1, 1, 1)

        self.lineEdit_device_label = QLineEdit(self.frame_5)
        self.lineEdit_device_label.setObjectName(u"lineEdit_device_label")
        self.lineEdit_device_label.setMinimumSize(QSize(252, 26))
        self.lineEdit_device_label.setMaximumSize(QSize(252, 26))
        self.lineEdit_device_label.setFont(font)
        self.lineEdit_device_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_device_label, 1, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 1, 3, 1, 1)


        self.gridLayout_8.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.scroll_main)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.comboBox_tuned_filter = QComboBox(self.frame_4)
        self.comboBox_tuned_filter.addItem("")
        self.comboBox_tuned_filter.addItem("")
        self.comboBox_tuned_filter.setObjectName(u"comboBox_tuned_filter")
        self.comboBox_tuned_filter.setMinimumSize(QSize(120, 26))
        self.comboBox_tuned_filter.setMaximumSize(QSize(140, 26))
        self.comboBox_tuned_filter.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_tuned_filter, 9, 2, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(200, 26))
        self.label_7.setMaximumSize(QSize(200, 26))
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_7, 8, 1, 1, 1)

        self.comboBox_connection_pipe = QComboBox(self.frame_4)
        self.comboBox_connection_pipe.addItem("")
        self.comboBox_connection_pipe.addItem("")
        self.comboBox_connection_pipe.setObjectName(u"comboBox_connection_pipe")
        self.comboBox_connection_pipe.setMinimumSize(QSize(120, 26))
        self.comboBox_connection_pipe.setMaximumSize(QSize(140, 26))
        self.comboBox_connection_pipe.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_connection_pipe, 0, 2, 1, 1)

        self.label_rotation_angle_pipe2_unit = QLabel(self.frame_4)
        self.label_rotation_angle_pipe2_unit.setObjectName(u"label_rotation_angle_pipe2_unit")
        self.label_rotation_angle_pipe2_unit.setMinimumSize(QSize(60, 26))
        self.label_rotation_angle_pipe2_unit.setMaximumSize(QSize(60, 26))
        self.label_rotation_angle_pipe2_unit.setFont(font)
        self.label_rotation_angle_pipe2_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_rotation_angle_pipe2_unit, 12, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 4, 0, 1, 1)

        self.comboBox_pipe1_connection = QComboBox(self.frame_4)
        self.comboBox_pipe1_connection.addItem("")
        self.comboBox_pipe1_connection.addItem("")
        self.comboBox_pipe1_connection.setObjectName(u"comboBox_pipe1_connection")
        self.comboBox_pipe1_connection.setMinimumSize(QSize(120, 26))
        self.comboBox_pipe1_connection.setMaximumSize(QSize(140, 26))
        self.comboBox_pipe1_connection.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_pipe1_connection, 7, 2, 1, 1)

        self.label_rotation_angle_pipe1_unit = QLabel(self.frame_4)
        self.label_rotation_angle_pipe1_unit.setObjectName(u"label_rotation_angle_pipe1_unit")
        self.label_rotation_angle_pipe1_unit.setMinimumSize(QSize(60, 26))
        self.label_rotation_angle_pipe1_unit.setMaximumSize(QSize(60, 26))
        self.label_rotation_angle_pipe1_unit.setFont(font)
        self.label_rotation_angle_pipe1_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_rotation_angle_pipe1_unit, 11, 3, 1, 1)

        self.spinBox_volumes_spacing = QDoubleSpinBox(self.frame_4)
        self.spinBox_volumes_spacing.setObjectName(u"spinBox_volumes_spacing")
        self.spinBox_volumes_spacing.setMinimumSize(QSize(0, 26))
        self.spinBox_volumes_spacing.setMaximumSize(QSize(16777215, 26))
        self.spinBox_volumes_spacing.setFont(font)
        self.spinBox_volumes_spacing.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_volumes_spacing.setDecimals(4)
        self.spinBox_volumes_spacing.setMaximum(200.000000000000000)
        self.spinBox_volumes_spacing.setSingleStep(0.001000000000000)
        self.spinBox_volumes_spacing.setValue(0.025000000000000)

        self.gridLayout_4.addWidget(self.spinBox_volumes_spacing, 4, 2, 1, 1)

        self.spinBox_pipe1_rotation_angle = QDoubleSpinBox(self.frame_4)
        self.spinBox_pipe1_rotation_angle.setObjectName(u"spinBox_pipe1_rotation_angle")
        self.spinBox_pipe1_rotation_angle.setMinimumSize(QSize(120, 26))
        self.spinBox_pipe1_rotation_angle.setMaximumSize(QSize(140, 26))
        self.spinBox_pipe1_rotation_angle.setFont(font)
        self.spinBox_pipe1_rotation_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_pipe1_rotation_angle.setMinimum(-180.000000000000000)
        self.spinBox_pipe1_rotation_angle.setMaximum(180.000000000000000)
        self.spinBox_pipe1_rotation_angle.setValue(90.000000000000000)

        self.gridLayout_4.addWidget(self.spinBox_pipe1_rotation_angle, 11, 2, 1, 1)

        self.label_rotation_plane = QLabel(self.frame_4)
        self.label_rotation_plane.setObjectName(u"label_rotation_plane")
        self.label_rotation_plane.setMinimumSize(QSize(200, 26))
        self.label_rotation_plane.setMaximumSize(QSize(200, 26))
        self.label_rotation_plane.setFont(font)
        self.label_rotation_plane.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_rotation_plane, 10, 1, 1, 1)

        self.comboBox_number_volumes = QComboBox(self.frame_4)
        self.comboBox_number_volumes.addItem("")
        self.comboBox_number_volumes.addItem("")
        self.comboBox_number_volumes.setObjectName(u"comboBox_number_volumes")
        self.comboBox_number_volumes.setMinimumSize(QSize(120, 26))
        self.comboBox_number_volumes.setMaximumSize(QSize(140, 26))
        self.comboBox_number_volumes.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_number_volumes, 3, 2, 1, 1)

        self.comboBox_pipe2_connection = QComboBox(self.frame_4)
        self.comboBox_pipe2_connection.addItem("")
        self.comboBox_pipe2_connection.addItem("")
        self.comboBox_pipe2_connection.setObjectName(u"comboBox_pipe2_connection")
        self.comboBox_pipe2_connection.setMinimumSize(QSize(120, 26))
        self.comboBox_pipe2_connection.setMaximumSize(QSize(140, 26))
        self.comboBox_pipe2_connection.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_pipe2_connection, 8, 2, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(200, 26))
        self.label_5.setMaximumSize(QSize(200, 26))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_volumes_spacing_unit = QLabel(self.frame_4)
        self.label_volumes_spacing_unit.setObjectName(u"label_volumes_spacing_unit")
        self.label_volumes_spacing_unit.setMinimumSize(QSize(60, 26))
        self.label_volumes_spacing_unit.setMaximumSize(QSize(60, 26))
        self.label_volumes_spacing_unit.setFont(font)
        self.label_volumes_spacing_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_volumes_spacing_unit, 4, 3, 1, 1)

        self.label_volumes_connection = QLabel(self.frame_4)
        self.label_volumes_connection.setObjectName(u"label_volumes_connection")
        self.label_volumes_connection.setMinimumSize(QSize(200, 26))
        self.label_volumes_connection.setMaximumSize(QSize(200, 26))
        self.label_volumes_connection.setFont(font)
        self.label_volumes_connection.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_volumes_connection, 5, 1, 1, 1)

        self.spinBox_pipe2_rotation_angle = QDoubleSpinBox(self.frame_4)
        self.spinBox_pipe2_rotation_angle.setObjectName(u"spinBox_pipe2_rotation_angle")
        self.spinBox_pipe2_rotation_angle.setMinimumSize(QSize(120, 26))
        self.spinBox_pipe2_rotation_angle.setMaximumSize(QSize(140, 26))
        self.spinBox_pipe2_rotation_angle.setFont(font)
        self.spinBox_pipe2_rotation_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_pipe2_rotation_angle.setMinimum(-180.000000000000000)
        self.spinBox_pipe2_rotation_angle.setMaximum(180.000000000000000)
        self.spinBox_pipe2_rotation_angle.setValue(0.000000000000000)

        self.gridLayout_4.addWidget(self.spinBox_pipe2_rotation_angle, 12, 2, 1, 1)

        self.label_20 = QLabel(self.frame_4)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(32, 26))
        self.label_20.setMaximumSize(QSize(32, 26))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_20, 3, 3, 1, 1)

        self.comboBox_volumes_connection = QComboBox(self.frame_4)
        self.comboBox_volumes_connection.addItem("")
        self.comboBox_volumes_connection.addItem("")
        self.comboBox_volumes_connection.addItem("")
        self.comboBox_volumes_connection.setObjectName(u"comboBox_volumes_connection")
        self.comboBox_volumes_connection.setMinimumSize(QSize(120, 26))
        self.comboBox_volumes_connection.setMaximumSize(QSize(140, 26))
        self.comboBox_volumes_connection.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_volumes_connection, 5, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(200, 26))
        self.label_2.setMaximumSize(QSize(200, 26))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 3, 1, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(200, 26))
        self.label_4.setMaximumSize(QSize(200, 26))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_volumes_spacing = QLabel(self.frame_4)
        self.label_volumes_spacing.setObjectName(u"label_volumes_spacing")
        self.label_volumes_spacing.setMinimumSize(QSize(200, 26))
        self.label_volumes_spacing.setMaximumSize(QSize(200, 26))
        self.label_volumes_spacing.setFont(font)
        self.label_volumes_spacing.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_volumes_spacing, 4, 1, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(200, 26))
        self.label_6.setMaximumSize(QSize(200, 26))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_6, 7, 1, 1, 1)

        self.lineEdit_rotation_plane = QLineEdit(self.frame_4)
        self.lineEdit_rotation_plane.setObjectName(u"lineEdit_rotation_plane")
        self.lineEdit_rotation_plane.setEnabled(False)
        self.lineEdit_rotation_plane.setMinimumSize(QSize(120, 26))
        self.lineEdit_rotation_plane.setMaximumSize(QSize(140, 26))
        self.lineEdit_rotation_plane.setFont(font)
        self.lineEdit_rotation_plane.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_rotation_plane, 10, 2, 1, 1)

        self.comboBox_main_axis = QComboBox(self.frame_4)
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.addItem("")
        self.comboBox_main_axis.setObjectName(u"comboBox_main_axis")
        self.comboBox_main_axis.setMinimumSize(QSize(120, 26))
        self.comboBox_main_axis.setMaximumSize(QSize(140, 26))
        self.comboBox_main_axis.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_main_axis, 1, 2, 1, 1)

        self.label_tunned_filter = QLabel(self.frame_4)
        self.label_tunned_filter.setObjectName(u"label_tunned_filter")
        self.label_tunned_filter.setMinimumSize(QSize(200, 26))
        self.label_tunned_filter.setMaximumSize(QSize(200, 26))
        self.label_tunned_filter.setFont(font)
        self.label_tunned_filter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_tunned_filter, 9, 1, 1, 1)

        self.label_rotation_angle_pipe2 = QLabel(self.frame_4)
        self.label_rotation_angle_pipe2.setObjectName(u"label_rotation_angle_pipe2")
        self.label_rotation_angle_pipe2.setMinimumSize(QSize(200, 26))
        self.label_rotation_angle_pipe2.setMaximumSize(QSize(200, 26))
        self.label_rotation_angle_pipe2.setFont(font)
        self.label_rotation_angle_pipe2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_rotation_angle_pipe2, 12, 1, 1, 1)

        self.label_rotation_angle_pipe1 = QLabel(self.frame_4)
        self.label_rotation_angle_pipe1.setObjectName(u"label_rotation_angle_pipe1")
        self.label_rotation_angle_pipe1.setMinimumSize(QSize(200, 26))
        self.label_rotation_angle_pipe1.setMaximumSize(QSize(200, 26))
        self.label_rotation_angle_pipe1.setFont(font)
        self.label_rotation_angle_pipe1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_rotation_angle_pipe1, 11, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 4, 4, 1, 1)


        self.gridLayout_8.addWidget(self.frame_4, 4, 0, 1, 1)

        self.frame_7 = QFrame(self.scroll_main)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 0))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_pipe2_diameter = QLineEdit(self.frame_7)
        self.lineEdit_pipe2_diameter.setObjectName(u"lineEdit_pipe2_diameter")
        self.lineEdit_pipe2_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe2_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe2_diameter.setFont(font)
        self.lineEdit_pipe2_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe2_diameter, 5, 3, 1, 1)

        self.label_42 = QLabel(self.frame_7)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(100, 26))
        self.label_42.setMaximumSize(QSize(100, 26))
        self.label_42.setFont(font)
        self.label_42.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_42, 5, 1, 1, 1)

        self.lineEdit_pipe2_wall_thickness = QLineEdit(self.frame_7)
        self.lineEdit_pipe2_wall_thickness.setObjectName(u"lineEdit_pipe2_wall_thickness")
        self.lineEdit_pipe2_wall_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe2_wall_thickness.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe2_wall_thickness.setFont(font)
        self.lineEdit_pipe2_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe2_wall_thickness, 5, 4, 1, 1)

        self.lineEdit_pipe1_wall_thickness = QLineEdit(self.frame_7)
        self.lineEdit_pipe1_wall_thickness.setObjectName(u"lineEdit_pipe1_wall_thickness")
        self.lineEdit_pipe1_wall_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe1_wall_thickness.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe1_wall_thickness.setFont(font)
        self.lineEdit_pipe1_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe1_wall_thickness, 4, 4, 1, 1)

        self.lineEdit_pipe1_diameter = QLineEdit(self.frame_7)
        self.lineEdit_pipe1_diameter.setObjectName(u"lineEdit_pipe1_diameter")
        self.lineEdit_pipe1_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe1_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe1_diameter.setFont(font)
        self.lineEdit_pipe1_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe1_diameter, 4, 3, 1, 1)

        self.lineEdit_pipe3_wall_thickness = QLineEdit(self.frame_7)
        self.lineEdit_pipe3_wall_thickness.setObjectName(u"lineEdit_pipe3_wall_thickness")
        self.lineEdit_pipe3_wall_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe3_wall_thickness.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe3_wall_thickness.setFont(font)
        self.lineEdit_pipe3_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe3_wall_thickness, 6, 4, 1, 1)

        self.label_pipe3 = QLabel(self.frame_7)
        self.label_pipe3.setObjectName(u"label_pipe3")
        self.label_pipe3.setMinimumSize(QSize(100, 26))
        self.label_pipe3.setMaximumSize(QSize(100, 26))
        self.label_pipe3.setFont(font)
        self.label_pipe3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_pipe3, 6, 1, 1, 1)

        self.lineEdit_pipe3_distance = QLineEdit(self.frame_7)
        self.lineEdit_pipe3_distance.setObjectName(u"lineEdit_pipe3_distance")
        self.lineEdit_pipe3_distance.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe3_distance.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe3_distance.setFont(font)
        self.lineEdit_pipe3_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe3_distance, 6, 6, 1, 1)

        self.lineEdit_pipe1_distance = QLineEdit(self.frame_7)
        self.lineEdit_pipe1_distance.setObjectName(u"lineEdit_pipe1_distance")
        self.lineEdit_pipe1_distance.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe1_distance.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe1_distance.setFont(font)
        self.lineEdit_pipe1_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe1_distance, 4, 6, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_2, 4, 7, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.lineEdit_volume1_distance = QLineEdit(self.frame_7)
        self.lineEdit_volume1_distance.setObjectName(u"lineEdit_volume1_distance")
        self.lineEdit_volume1_distance.setEnabled(False)
        self.lineEdit_volume1_distance.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume1_distance.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume1_distance.setFont(font)
        self.lineEdit_volume1_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume1_distance, 1, 6, 1, 1)

        self.lineEdit_pipe3_diameter = QLineEdit(self.frame_7)
        self.lineEdit_pipe3_diameter.setObjectName(u"lineEdit_pipe3_diameter")
        self.lineEdit_pipe3_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe3_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe3_diameter.setFont(font)
        self.lineEdit_pipe3_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe3_diameter, 6, 3, 1, 1)

        self.lineEdit_volume2_distance = QLineEdit(self.frame_7)
        self.lineEdit_volume2_distance.setObjectName(u"lineEdit_volume2_distance")
        self.lineEdit_volume2_distance.setEnabled(False)
        self.lineEdit_volume2_distance.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume2_distance.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume2_distance.setFont(font)
        self.lineEdit_volume2_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume2_distance, 2, 6, 1, 1)

        self.label_45 = QLabel(self.frame_7)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(100, 26))
        self.label_45.setMaximumSize(QSize(100, 27))
        self.label_45.setFont(font)
        self.label_45.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_45, 0, 6, 1, 1)

        self.lineEdit_pipe2_distance = QLineEdit(self.frame_7)
        self.lineEdit_pipe2_distance.setObjectName(u"lineEdit_pipe2_distance")
        self.lineEdit_pipe2_distance.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe2_distance.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe2_distance.setFont(font)
        self.lineEdit_pipe2_distance.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe2_distance, 5, 6, 1, 1)

        self.lineEdit_volume1_wall_thickness = QLineEdit(self.frame_7)
        self.lineEdit_volume1_wall_thickness.setObjectName(u"lineEdit_volume1_wall_thickness")
        self.lineEdit_volume1_wall_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume1_wall_thickness.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume1_wall_thickness.setFont(font)
        self.lineEdit_volume1_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume1_wall_thickness, 1, 4, 1, 1)

        self.lineEdit_volume1_diameter = QLineEdit(self.frame_7)
        self.lineEdit_volume1_diameter.setObjectName(u"lineEdit_volume1_diameter")
        self.lineEdit_volume1_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume1_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume1_diameter.setFont(font)
        self.lineEdit_volume1_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume1_diameter, 1, 3, 1, 1)

        self.label_43 = QLabel(self.frame_7)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(100, 26))
        self.label_43.setMaximumSize(QSize(100, 26))
        self.label_43.setFont(font)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_43, 0, 3, 1, 1)

        self.label_volume2 = QLabel(self.frame_7)
        self.label_volume2.setObjectName(u"label_volume2")
        self.label_volume2.setMinimumSize(QSize(100, 26))
        self.label_volume2.setMaximumSize(QSize(100, 26))
        self.label_volume2.setFont(font)
        self.label_volume2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_volume2, 2, 1, 1, 1)

        self.label_41 = QLabel(self.frame_7)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(100, 26))
        self.label_41.setMaximumSize(QSize(100, 26))
        self.label_41.setFont(font)
        self.label_41.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_41, 4, 1, 1, 1)

        self.lineEdit_volume2_wall_thickness = QLineEdit(self.frame_7)
        self.lineEdit_volume2_wall_thickness.setObjectName(u"lineEdit_volume2_wall_thickness")
        self.lineEdit_volume2_wall_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume2_wall_thickness.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume2_wall_thickness.setFont(font)
        self.lineEdit_volume2_wall_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume2_wall_thickness, 2, 4, 1, 1)

        self.lineEdit_volume2_diameter = QLineEdit(self.frame_7)
        self.lineEdit_volume2_diameter.setObjectName(u"lineEdit_volume2_diameter")
        self.lineEdit_volume2_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume2_diameter.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume2_diameter.setFont(font)
        self.lineEdit_volume2_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume2_diameter, 2, 3, 1, 1)

        self.label_volume1 = QLabel(self.frame_7)
        self.label_volume1.setObjectName(u"label_volume1")
        self.label_volume1.setMinimumSize(QSize(100, 26))
        self.label_volume1.setMaximumSize(QSize(100, 26))
        self.label_volume1.setFont(font)
        self.label_volume1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_volume1, 1, 1, 1, 1)

        self.label_44 = QLabel(self.frame_7)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(100, 26))
        self.label_44.setMaximumSize(QSize(100, 26))
        self.label_44.setFont(font)
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_44, 0, 4, 1, 1)

        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 26))
        self.label_3.setMaximumSize(QSize(100, 26))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_3, 0, 5, 1, 1)

        self.lineEdit_volume1_length = QLineEdit(self.frame_7)
        self.lineEdit_volume1_length.setObjectName(u"lineEdit_volume1_length")
        self.lineEdit_volume1_length.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume1_length.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume1_length.setFont(font)
        self.lineEdit_volume1_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume1_length, 1, 5, 1, 1)

        self.lineEdit_volume2_length = QLineEdit(self.frame_7)
        self.lineEdit_volume2_length.setObjectName(u"lineEdit_volume2_length")
        self.lineEdit_volume2_length.setMinimumSize(QSize(100, 26))
        self.lineEdit_volume2_length.setMaximumSize(QSize(100, 26))
        self.lineEdit_volume2_length.setFont(font)
        self.lineEdit_volume2_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volume2_length, 2, 5, 1, 1)

        self.lineEdit_pipe1_length = QLineEdit(self.frame_7)
        self.lineEdit_pipe1_length.setObjectName(u"lineEdit_pipe1_length")
        self.lineEdit_pipe1_length.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe1_length.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe1_length.setFont(font)
        self.lineEdit_pipe1_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe1_length, 4, 5, 1, 1)

        self.lineEdit_pipe2_length = QLineEdit(self.frame_7)
        self.lineEdit_pipe2_length.setObjectName(u"lineEdit_pipe2_length")
        self.lineEdit_pipe2_length.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe2_length.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe2_length.setFont(font)
        self.lineEdit_pipe2_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe2_length, 5, 5, 1, 1)

        self.lineEdit_pipe3_length = QLineEdit(self.frame_7)
        self.lineEdit_pipe3_length.setObjectName(u"lineEdit_pipe3_length")
        self.lineEdit_pipe3_length.setMinimumSize(QSize(100, 26))
        self.lineEdit_pipe3_length.setMaximumSize(QSize(100, 26))
        self.lineEdit_pipe3_length.setFont(font)
        self.lineEdit_pipe3_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_pipe3_length, 6, 5, 1, 1)


        self.gridLayout_8.addWidget(self.frame_7, 7, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 8, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_3, 6, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_5, 3, 0, 1, 1)

        self.frame_8 = QFrame(self.scroll_main)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 60))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_8)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(0, 20))
        self.label_8.setMaximumSize(QSize(80, 20))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_8, 0, 2, 1, 1)

        self.label_46 = QLabel(self.frame_8)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(100, 26))
        self.label_46.setMaximumSize(QSize(100, 26))
        self.label_46.setFont(font)
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_46, 1, 1, 1, 1)

        self.lineEdit_connecting_coord_x = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_x.setObjectName(u"lineEdit_connecting_coord_x")
        self.lineEdit_connecting_coord_x.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_x.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_x.setFont(font)
        self.lineEdit_connecting_coord_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_connecting_coord_x, 1, 2, 1, 1)

        self.label_9 = QLabel(self.frame_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 20))
        self.label_9.setMaximumSize(QSize(80, 20))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_9, 0, 3, 1, 1)

        self.label_10 = QLabel(self.frame_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 20))
        self.label_10.setMaximumSize(QSize(80, 20))
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_10, 0, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_7, 1, 0, 1, 1)

        self.lineEdit_connecting_coord_y = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_y.setObjectName(u"lineEdit_connecting_coord_y")
        self.lineEdit_connecting_coord_y.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_y.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_y.setFont(font)
        self.lineEdit_connecting_coord_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_connecting_coord_y, 1, 3, 1, 1)

        self.lineEdit_connecting_coord_z = QLineEdit(self.frame_8)
        self.lineEdit_connecting_coord_z.setObjectName(u"lineEdit_connecting_coord_z")
        self.lineEdit_connecting_coord_z.setMinimumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_z.setMaximumSize(QSize(80, 26))
        self.lineEdit_connecting_coord_z.setFont(font)
        self.lineEdit_connecting_coord_z.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_connecting_coord_z, 1, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_8, 1, 5, 1, 1)


        self.gridLayout_8.addWidget(self.frame_8, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scroll_main)

        self.gridLayout_7.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_devices = QWidget()
        self.tab_devices.setObjectName(u"tab_devices")
        self.gridLayout_9 = QGridLayout(self.tab_devices)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.frame_6 = QFrame(self.tab_devices)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.pushButton_edit = QPushButton(self.frame_6)
        self.pushButton_edit.setObjectName(u"pushButton_edit")
        self.pushButton_edit.setMinimumSize(QSize(100, 28))
        self.pushButton_edit.setMaximumSize(QSize(100, 28))
        self.pushButton_edit.setFont(font)
        self.pushButton_edit.setStyleSheet(u"")
        self.pushButton_edit.setAutoDefault(False)
        self.pushButton_edit.setFlat(False)

        self.gridLayout_10.addWidget(self.pushButton_edit, 0, 3, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_6)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)
        self.pushButton_remove.setFlat(False)

        self.gridLayout_10.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_6)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_10.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_copy = QPushButton(self.frame_6)
        self.pushButton_copy.setObjectName(u"pushButton_copy")
        self.pushButton_copy.setMinimumSize(QSize(100, 28))
        self.pushButton_copy.setMaximumSize(QSize(100, 28))
        self.pushButton_copy.setFont(font)
        self.pushButton_copy.setStyleSheet(u"")
        self.pushButton_copy.setAutoDefault(False)
        self.pushButton_copy.setFlat(False)

        self.gridLayout_10.addWidget(self.pushButton_copy, 0, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_6, 2, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_devices)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 40))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_9)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_9 = QSpacerItem(138, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(138, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_10, 0, 3, 1, 1)

        self.lineEdit_selection = QLineEdit(self.frame_9)
        self.lineEdit_selection.setObjectName(u"lineEdit_selection")
        self.lineEdit_selection.setMinimumSize(QSize(180, 26))
        self.lineEdit_selection.setMaximumSize(QSize(180, 26))
        self.lineEdit_selection.setFont(font)
        self.lineEdit_selection.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_selection, 0, 2, 1, 1)

        self.label_11 = QLabel(self.frame_9)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 26))
        self.label_11.setMaximumSize(QSize(16777215, 26))
        self.label_11.setFont(font)

        self.gridLayout_13.addWidget(self.label_11, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_9, 0, 0, 1, 1)

        self.treeWidget_psd_info = QTreeWidget(self.tab_devices)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"PSD label")
        self.treeWidget_psd_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_psd_info.setObjectName(u"treeWidget_psd_info")
        self.treeWidget_psd_info.setMinimumSize(QSize(0, 240))
        self.treeWidget_psd_info.setMaximumSize(QSize(16777215, 480))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        self.treeWidget_psd_info.setFont(font1)
        self.treeWidget_psd_info.setIndentation(0)

        self.gridLayout_9.addWidget(self.treeWidget_psd_info, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_devices, "")

        self.gridLayout_6.addWidget(self.tabWidget_main, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_10 = QFrame(Dialog)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(500, 0))
        self.frame_10.setFrameShape(QFrame.Shape.Box)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_10)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_13 = QLabel(self.frame_10)
        self.label_13.setObjectName(u"label_13")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QSize(0, 40))
        self.label_13.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setPointSize(11)
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_14.addWidget(self.label_13, 0, 0, 1, 1)

        self.preview_widget_placeholder = QWidget(self.frame_10)
        self.preview_widget_placeholder.setObjectName(u"preview_widget_placeholder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.preview_widget_placeholder.sizePolicy().hasHeightForWidth())
        self.preview_widget_placeholder.setSizePolicy(sizePolicy1)

        self.gridLayout_14.addWidget(self.preview_widget_placeholder, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_10, 1, 1, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)
        self.label.setLineWidth(0)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_3)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)
        self.pushButton_exit.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_create_psd = QPushButton(self.frame_3)
        self.pushButton_create_psd.setObjectName(u"pushButton_create_psd")
        self.pushButton_create_psd.setMinimumSize(QSize(100, 28))
        self.pushButton_create_psd.setMaximumSize(QSize(100, 28))
        self.pushButton_create_psd.setFont(font)
        self.pushButton_create_psd.setStyleSheet(u"")
        self.pushButton_create_psd.setAutoDefault(False)
        self.pushButton_create_psd.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_create_psd, 0, 2, 1, 1)

        self.pushButton_show_errors = QPushButton(self.frame_3)
        self.pushButton_show_errors.setObjectName(u"pushButton_show_errors")
        self.pushButton_show_errors.setEnabled(False)
        self.pushButton_show_errors.setMinimumSize(QSize(100, 28))
        self.pushButton_show_errors.setMaximumSize(QSize(100, 28))
        self.pushButton_show_errors.setFont(font)

        self.gridLayout_2.addWidget(self.pushButton_show_errors, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 3, 0, 1, 2)

        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_device_label)
        QWidget.setTabOrder(self.lineEdit_device_label, self.lineEdit_connecting_coord_x)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_x, self.lineEdit_connecting_coord_y)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_y, self.lineEdit_connecting_coord_z)
        QWidget.setTabOrder(self.lineEdit_connecting_coord_z, self.comboBox_connection_pipe)
        QWidget.setTabOrder(self.comboBox_connection_pipe, self.comboBox_main_axis)
        QWidget.setTabOrder(self.comboBox_main_axis, self.comboBox_number_volumes)
        QWidget.setTabOrder(self.comboBox_number_volumes, self.spinBox_volumes_spacing)
        QWidget.setTabOrder(self.spinBox_volumes_spacing, self.comboBox_volumes_connection)
        QWidget.setTabOrder(self.comboBox_volumes_connection, self.comboBox_pipe1_connection)
        QWidget.setTabOrder(self.comboBox_pipe1_connection, self.comboBox_pipe2_connection)
        QWidget.setTabOrder(self.comboBox_pipe2_connection, self.comboBox_tuned_filter)
        QWidget.setTabOrder(self.comboBox_tuned_filter, self.lineEdit_rotation_plane)
        QWidget.setTabOrder(self.lineEdit_rotation_plane, self.spinBox_pipe1_rotation_angle)
        QWidget.setTabOrder(self.spinBox_pipe1_rotation_angle, self.spinBox_pipe2_rotation_angle)
        QWidget.setTabOrder(self.spinBox_pipe2_rotation_angle, self.lineEdit_volume1_diameter)
        QWidget.setTabOrder(self.lineEdit_volume1_diameter, self.lineEdit_volume1_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_volume1_wall_thickness, self.lineEdit_volume1_length)
        QWidget.setTabOrder(self.lineEdit_volume1_length, self.lineEdit_volume2_diameter)
        QWidget.setTabOrder(self.lineEdit_volume2_diameter, self.lineEdit_volume2_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_volume2_wall_thickness, self.lineEdit_volume2_length)
        QWidget.setTabOrder(self.lineEdit_volume2_length, self.lineEdit_pipe1_diameter)
        QWidget.setTabOrder(self.lineEdit_pipe1_diameter, self.lineEdit_pipe1_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_pipe1_wall_thickness, self.lineEdit_pipe1_length)
        QWidget.setTabOrder(self.lineEdit_pipe1_length, self.lineEdit_pipe1_distance)
        QWidget.setTabOrder(self.lineEdit_pipe1_distance, self.lineEdit_pipe2_diameter)
        QWidget.setTabOrder(self.lineEdit_pipe2_diameter, self.lineEdit_pipe2_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_pipe2_wall_thickness, self.lineEdit_pipe2_length)
        QWidget.setTabOrder(self.lineEdit_pipe2_length, self.lineEdit_pipe2_distance)
        QWidget.setTabOrder(self.lineEdit_pipe2_distance, self.lineEdit_pipe3_diameter)
        QWidget.setTabOrder(self.lineEdit_pipe3_diameter, self.lineEdit_pipe3_wall_thickness)
        QWidget.setTabOrder(self.lineEdit_pipe3_wall_thickness, self.lineEdit_pipe3_length)
        QWidget.setTabOrder(self.lineEdit_pipe3_length, self.lineEdit_pipe3_distance)
        QWidget.setTabOrder(self.lineEdit_pipe3_distance, self.pushButton_create_psd)
        QWidget.setTabOrder(self.pushButton_create_psd, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.lineEdit_selection)
        QWidget.setTabOrder(self.lineEdit_selection, self.treeWidget_psd_info)
        QWidget.setTabOrder(self.treeWidget_psd_info, self.lineEdit_volume2_distance)
        QWidget.setTabOrder(self.lineEdit_volume2_distance, self.lineEdit_volume1_distance)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_number_volumes.setCurrentIndex(0)
        self.pushButton_edit.setDefault(False)
        self.pushButton_remove.setDefault(False)
        self.pushButton_reset.setDefault(False)
        self.pushButton_copy.setDefault(False)
        self.pushButton_exit.setDefault(False)
        self.pushButton_create_psd.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Device label:", None))
        self.lineEdit_device_label.setText("")
        self.comboBox_tuned_filter.setItemText(0, QCoreApplication.translate("Dialog", u"disabled", None))
        self.comboBox_tuned_filter.setItemText(1, QCoreApplication.translate("Dialog", u"double-tuned", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"Pipe #2 connection:", None))
        self.comboBox_connection_pipe.setItemText(0, QCoreApplication.translate("Dialog", u"pipe #1", None))
        self.comboBox_connection_pipe.setItemText(1, QCoreApplication.translate("Dialog", u"pipe #2", None))

        self.label_rotation_angle_pipe2_unit.setText(QCoreApplication.translate("Dialog", u"[deg]", None))
        self.comboBox_pipe1_connection.setItemText(0, QCoreApplication.translate("Dialog", u"radial type", None))
        self.comboBox_pipe1_connection.setItemText(1, QCoreApplication.translate("Dialog", u"axial type", None))

        self.label_rotation_angle_pipe1_unit.setText(QCoreApplication.translate("Dialog", u"[deg]", None))
        self.label_rotation_plane.setText(QCoreApplication.translate("Dialog", u"Rotation plane:", None))
        self.comboBox_number_volumes.setItemText(0, QCoreApplication.translate("Dialog", u"two volumes", None))
        self.comboBox_number_volumes.setItemText(1, QCoreApplication.translate("Dialog", u"one volume", None))

        self.comboBox_pipe2_connection.setItemText(0, QCoreApplication.translate("Dialog", u"radial type", None))
        self.comboBox_pipe2_connection.setItemText(1, QCoreApplication.translate("Dialog", u"axial type", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Device main axis:", None))
        self.label_volumes_spacing_unit.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_volumes_connection.setText(QCoreApplication.translate("Dialog", u"Volumes connection:", None))
        self.label_20.setText("")
        self.comboBox_volumes_connection.setItemText(0, QCoreApplication.translate("Dialog", u"pipe", None))
        self.comboBox_volumes_connection.setItemText(1, QCoreApplication.translate("Dialog", u"pipe-plate", None))
        self.comboBox_volumes_connection.setItemText(2, QCoreApplication.translate("Dialog", u"perf. plate", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Number of volumes:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Connection pipe:", None))
        self.label_volumes_spacing.setText(QCoreApplication.translate("Dialog", u"Volumes spacing:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Pipe #1 connection:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_rotation_plane.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Orthogonal plane to the main axis</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_rotation_plane.setText("")
        self.comboBox_main_axis.setItemText(0, QCoreApplication.translate("Dialog", u"x-axis (+)", None))
        self.comboBox_main_axis.setItemText(1, QCoreApplication.translate("Dialog", u"y-axis (+)", None))
        self.comboBox_main_axis.setItemText(2, QCoreApplication.translate("Dialog", u"z-axis (+)", None))
        self.comboBox_main_axis.setItemText(3, QCoreApplication.translate("Dialog", u"x-axis (-)", None))
        self.comboBox_main_axis.setItemText(4, QCoreApplication.translate("Dialog", u"y-axis (-)", None))
        self.comboBox_main_axis.setItemText(5, QCoreApplication.translate("Dialog", u"z-axis (-)", None))

        self.label_tunned_filter.setText(QCoreApplication.translate("Dialog", u"Tuned filter:", None))
        self.label_rotation_angle_pipe2.setText(QCoreApplication.translate("Dialog", u"Rotation angle (pipe #2):", None))
        self.label_rotation_angle_pipe1.setText(QCoreApplication.translate("Dialog", u"Rotation angle (pipe #1):", None))
        self.lineEdit_pipe2_diameter.setText(QCoreApplication.translate("Dialog", u"0.35", None))
        self.label_42.setText(QCoreApplication.translate("Dialog", u"Pipe #2:", None))
        self.lineEdit_pipe2_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.lineEdit_pipe1_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.lineEdit_pipe1_diameter.setText(QCoreApplication.translate("Dialog", u"0.35", None))
        self.lineEdit_pipe3_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.label_pipe3.setText(QCoreApplication.translate("Dialog", u"Pipe #3:", None))
        self.lineEdit_pipe3_distance.setText(QCoreApplication.translate("Dialog", u"1.125", None))
        self.lineEdit_pipe1_distance.setText(QCoreApplication.translate("Dialog", u"0.75", None))
        self.lineEdit_volume1_distance.setText(QCoreApplication.translate("Dialog", u"---", None))
        self.lineEdit_pipe3_diameter.setText(QCoreApplication.translate("Dialog", u"0.20", None))
        self.lineEdit_volume2_distance.setText(QCoreApplication.translate("Dialog", u"---", None))
        self.label_45.setText(QCoreApplication.translate("Dialog", u"distance [m]", None))
        self.lineEdit_pipe2_distance.setText(QCoreApplication.translate("Dialog", u"2.25", None))
        self.lineEdit_volume1_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.lineEdit_volume1_diameter.setText(QCoreApplication.translate("Dialog", u"1.15", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"diameter [m]", None))
        self.label_volume2.setText(QCoreApplication.translate("Dialog", u"Volume #2:", None))
        self.label_41.setText(QCoreApplication.translate("Dialog", u"Pipe #1:", None))
        self.lineEdit_volume2_wall_thickness.setText(QCoreApplication.translate("Dialog", u"0.023", None))
        self.lineEdit_volume2_diameter.setText(QCoreApplication.translate("Dialog", u"1.15", None))
        self.label_volume1.setText(QCoreApplication.translate("Dialog", u"Volume #1:", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"thickness [m]", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"length [m]", None))
        self.lineEdit_volume1_length.setText(QCoreApplication.translate("Dialog", u"1.5", None))
        self.lineEdit_volume2_length.setText(QCoreApplication.translate("Dialog", u"1.5", None))
        self.lineEdit_pipe1_length.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.lineEdit_pipe2_length.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.lineEdit_pipe3_length.setText(QCoreApplication.translate("Dialog", u"0.775", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"coord. x [m]", None))
        self.label_46.setText(QCoreApplication.translate("Dialog", u"Connection:", None))
        self.lineEdit_connecting_coord_x.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"coord. y [m]", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"coord. z [m]", None))
        self.lineEdit_connecting_coord_y.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.lineEdit_connecting_coord_z.setText(QCoreApplication.translate("Dialog", u"0.000", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_edit.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.pushButton_edit.setProperty(u"status", "")
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", "")
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_copy.setText(QCoreApplication.translate("Dialog", u"Copy", None))
        self.pushButton_copy.setProperty(u"status", "")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Selection label:", None))
        ___qtreewidgetitem = self.treeWidget_psd_info.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Lines", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Connection point", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Connection type", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_devices), QCoreApplication.translate("Dialog", u"Devices", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Pulsation supression device preview", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Pulsation suppression device editor", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_create_psd.setText(QCoreApplication.translate("Dialog", u"Create PSD", None))
        self.pushButton_show_errors.setText(QCoreApplication.translate("Dialog", u"Show errors", None))
    # retranslateUi



class PulsationSuppressionDeviceInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - scrollArea: QScrollArea
                                                - scroll_main: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_5: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_12: QLabel
                                                                        - lineEdit_device_label: QLineEdit
                                                            - frame_4: QFrame
                                                                - (Layout): QGridLayout
                                                                        - comboBox_tuned_filter: QComboBox
                                                                        - label_7: QLabel
                                                                        - comboBox_connection_pipe: QComboBox
                                                                        - label_rotation_angle_pipe2_unit: QLabel
                                                                        - comboBox_pipe1_connection: QComboBox
                                                                        - label_rotation_angle_pipe1_unit: QLabel
                                                                        - spinBox_volumes_spacing: QDoubleSpinBox
                                                                        - spinBox_pipe1_rotation_angle: QDoubleSpinBox
                                                                        - label_rotation_plane: QLabel
                                                                        - comboBox_number_volumes: QComboBox
                                                                        - comboBox_pipe2_connection: QComboBox
                                                                        - label_5: QLabel
                                                                        - label_volumes_spacing_unit: QLabel
                                                                        - label_volumes_connection: QLabel
                                                                        - spinBox_pipe2_rotation_angle: QDoubleSpinBox
                                                                        - label_20: QLabel
                                                                        - comboBox_volumes_connection: QComboBox
                                                                        - label_2: QLabel
                                                                        - label_4: QLabel
                                                                        - label_volumes_spacing: QLabel
                                                                        - label_6: QLabel
                                                                        - lineEdit_rotation_plane: QLineEdit
                                                                        - comboBox_main_axis: QComboBox
                                                                        - label_tunned_filter: QLabel
                                                                        - label_rotation_angle_pipe2: QLabel
                                                                        - label_rotation_angle_pipe1: QLabel
                                                            - frame_7: QFrame
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_pipe2_diameter: QLineEdit
                                                                        - label_42: QLabel
                                                                        - lineEdit_pipe2_wall_thickness: QLineEdit
                                                                        - lineEdit_pipe1_wall_thickness: QLineEdit
                                                                        - lineEdit_pipe1_diameter: QLineEdit
                                                                        - lineEdit_pipe3_wall_thickness: QLineEdit
                                                                        - label_pipe3: QLabel
                                                                        - lineEdit_pipe3_distance: QLineEdit
                                                                        - lineEdit_pipe1_distance: QLineEdit
                                                                        - lineEdit_volume1_distance: QLineEdit
                                                                        - lineEdit_pipe3_diameter: QLineEdit
                                                                        - lineEdit_volume2_distance: QLineEdit
                                                                        - label_45: QLabel
                                                                        - lineEdit_pipe2_distance: QLineEdit
                                                                        - lineEdit_volume1_wall_thickness: QLineEdit
                                                                        - lineEdit_volume1_diameter: QLineEdit
                                                                        - label_43: QLabel
                                                                        - label_volume2: QLabel
                                                                        - label_41: QLabel
                                                                        - lineEdit_volume2_wall_thickness: QLineEdit
                                                                        - lineEdit_volume2_diameter: QLineEdit
                                                                        - label_volume1: QLabel
                                                                        - label_44: QLabel
                                                                        - label_3: QLabel
                                                                        - lineEdit_volume1_length: QLineEdit
                                                                        - lineEdit_volume2_length: QLineEdit
                                                                        - lineEdit_pipe1_length: QLineEdit
                                                                        - lineEdit_pipe2_length: QLineEdit
                                                                        - lineEdit_pipe3_length: QLineEdit
                                                            - frame_8: QFrame
                                                                - (Layout): QGridLayout
                                                                        - label_8: QLabel
                                                                        - label_46: QLabel
                                                                        - lineEdit_connecting_coord_x: QLineEdit
                                                                        - label_9: QLabel
                                                                        - label_10: QLabel
                                                                        - lineEdit_connecting_coord_y: QLineEdit
                                                                        - lineEdit_connecting_coord_z: QLineEdit
                                - tab_devices: QWidget
                                    - (Layout): QGridLayout
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_edit: QPushButton
                                                        - pushButton_remove: QPushButton
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_copy: QPushButton
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selection: QLineEdit
                                                        - label_11: QLabel
                                            - treeWidget_psd_info: QTreeWidget
                - frame_10: QFrame
                    - (Layout): QGridLayout
                            - label_13: QLabel
                            - preview_widget_placeholder: QWidget
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_create_psd: QPushButton
                            - pushButton_show_errors: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
