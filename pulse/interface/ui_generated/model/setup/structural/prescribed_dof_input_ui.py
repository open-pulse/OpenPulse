# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prescribed_dof_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.NonModal)
        Dialog.resize(450, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(450, 500))
        Dialog.setMaximumSize(QSize(450, 500))
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        icon = Icon(u"../../../../../../../../../Downloads/load - Copia.png")
        Dialog.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(1000, 1000))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_main)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget_main.setFont(font)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_9 = QGridLayout(self.tab_constant_values)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.tab_constant_values)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(8)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_imag_Ux = QLineEdit(self.frame_3)
        self.lineEdit_imag_Ux.setObjectName(u"lineEdit_imag_Ux")
        self.lineEdit_imag_Ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Ux.setMaximumSize(QSize(80, 26))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.lineEdit_imag_Ux.setFont(font1)
        self.lineEdit_imag_Ux.setStyleSheet(u"")
        self.lineEdit_imag_Ux.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Ux, 1, 3, 1, 1)

        self.label_imaginary = QLabel(self.frame_3)
        self.label_imaginary.setObjectName(u"label_imaginary")
        self.label_imaginary.setMinimumSize(QSize(80, 22))
        self.label_imaginary.setMaximumSize(QSize(80, 22))
        self.label_imaginary.setFont(font)
        self.label_imaginary.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_imaginary, 0, 3, 1, 1)

        self.lineEdit_real_Rz = QLineEdit(self.frame_3)
        self.lineEdit_real_Rz.setObjectName(u"lineEdit_real_Rz")
        self.lineEdit_real_Rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Rz.setFont(font1)
        self.lineEdit_real_Rz.setStyleSheet(u"")
        self.lineEdit_real_Rz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Rz, 6, 2, 1, 1)

        self.label_real = QLabel(self.frame_3)
        self.label_real.setObjectName(u"label_real")
        self.label_real.setMinimumSize(QSize(80, 22))
        self.label_real.setMaximumSize(QSize(80, 22))
        self.label_real.setFont(font)
        self.label_real.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_real, 0, 2, 1, 1)

        self.lineEdit_real_Uz = QLineEdit(self.frame_3)
        self.lineEdit_real_Uz.setObjectName(u"lineEdit_real_Uz")
        self.lineEdit_real_Uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Uz.setFont(font1)
        self.lineEdit_real_Uz.setStyleSheet(u"")
        self.lineEdit_real_Uz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Uz, 3, 2, 1, 1)

        self.lineEdit_real_Ry = QLineEdit(self.frame_3)
        self.lineEdit_real_Ry.setObjectName(u"lineEdit_real_Ry")
        self.lineEdit_real_Ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Ry.setFont(font1)
        self.lineEdit_real_Ry.setStyleSheet(u"")
        self.lineEdit_real_Ry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Ry, 5, 2, 1, 1)

        self.lineEdit_real_Ux = QLineEdit(self.frame_3)
        self.lineEdit_real_Ux.setObjectName(u"lineEdit_real_Ux")
        self.lineEdit_real_Ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Ux.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Ux.setFont(font1)
        self.lineEdit_real_Ux.setStyleSheet(u"")
        self.lineEdit_real_Ux.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Ux, 1, 2, 1, 1)

        self.lineEdit_imag_Uz = QLineEdit(self.frame_3)
        self.lineEdit_imag_Uz.setObjectName(u"lineEdit_imag_Uz")
        self.lineEdit_imag_Uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Uz.setFont(font1)
        self.lineEdit_imag_Uz.setStyleSheet(u"")
        self.lineEdit_imag_Uz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Uz, 3, 3, 1, 1)

        self.label_Uz_constant = QLabel(self.frame_3)
        self.label_Uz_constant.setObjectName(u"label_Uz_constant")
        self.label_Uz_constant.setMinimumSize(QSize(32, 26))
        self.label_Uz_constant.setMaximumSize(QSize(32, 26))
        self.label_Uz_constant.setFont(font)
        self.label_Uz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uz_constant, 3, 1, 1, 1)

        self.comboBox_displacement_uy = QComboBox(self.frame_3)
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.addItem("")
        self.comboBox_displacement_uy.setObjectName(u"comboBox_displacement_uy")
        self.comboBox_displacement_uy.setMinimumSize(QSize(90, 26))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.comboBox_displacement_uy.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_displacement_uy, 2, 4, 1, 1)

        self.label_Ry_constant = QLabel(self.frame_3)
        self.label_Ry_constant.setObjectName(u"label_Ry_constant")
        self.label_Ry_constant.setMinimumSize(QSize(32, 26))
        self.label_Ry_constant.setMaximumSize(QSize(32, 26))
        self.label_Ry_constant.setFont(font)
        self.label_Ry_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ry_constant, 5, 1, 1, 1)

        self.label_Ux_constant = QLabel(self.frame_3)
        self.label_Ux_constant.setObjectName(u"label_Ux_constant")
        self.label_Ux_constant.setMinimumSize(QSize(32, 26))
        self.label_Ux_constant.setMaximumSize(QSize(32, 26))
        self.label_Ux_constant.setFont(font)
        self.label_Ux_constant.setStyleSheet(u"")
        self.label_Ux_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ux_constant, 1, 1, 1, 1)

        self.lineEdit_imag_Ry = QLineEdit(self.frame_3)
        self.lineEdit_imag_Ry.setObjectName(u"lineEdit_imag_Ry")
        self.lineEdit_imag_Ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Ry.setFont(font1)
        self.lineEdit_imag_Ry.setStyleSheet(u"")
        self.lineEdit_imag_Ry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Ry, 5, 3, 1, 1)

        self.frame_10 = QFrame(self.frame_3)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 0))
        self.frame_10.setMaximumSize(QSize(16777215, 40))
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_14 = QGridLayout(self.frame_10)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(2, 2, 2, 2)
        self.pushButton_all_dof_fixed = QPushButton(self.frame_10)
        self.pushButton_all_dof_fixed.setObjectName(u"pushButton_all_dof_fixed")
        self.pushButton_all_dof_fixed.setMinimumSize(QSize(100, 28))
        self.pushButton_all_dof_fixed.setMaximumSize(QSize(100, 28))
        self.pushButton_all_dof_fixed.setFont(font1)
        self.pushButton_all_dof_fixed.setStyleSheet(u"")
        self.pushButton_all_dof_fixed.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_all_dof_fixed, 0, 1, 1, 1)

        self.pushButton_all_dof_free = QPushButton(self.frame_10)
        self.pushButton_all_dof_free.setObjectName(u"pushButton_all_dof_free")
        self.pushButton_all_dof_free.setMinimumSize(QSize(40, 28))
        self.pushButton_all_dof_free.setMaximumSize(QSize(100, 28))
        self.pushButton_all_dof_free.setFont(font1)
        self.pushButton_all_dof_free.setStyleSheet(u"")
        self.pushButton_all_dof_free.setIconSize(QSize(22, 22))
        self.pushButton_all_dof_free.setAutoDefault(False)

        self.gridLayout_14.addWidget(self.pushButton_all_dof_free, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_10, 7, 0, 1, 6)

        self.comboBox_rotation_rx = QComboBox(self.frame_3)
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.addItem("")
        self.comboBox_rotation_rx.setObjectName(u"comboBox_rotation_rx")
        self.comboBox_rotation_rx.setMinimumSize(QSize(90, 26))
        self.comboBox_rotation_rx.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_rotation_rx, 4, 4, 1, 1)

        self.label_Uy_constant = QLabel(self.frame_3)
        self.label_Uy_constant.setObjectName(u"label_Uy_constant")
        self.label_Uy_constant.setMinimumSize(QSize(32, 26))
        self.label_Uy_constant.setMaximumSize(QSize(32, 26))
        self.label_Uy_constant.setFont(font)
        self.label_Uy_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uy_constant, 2, 1, 1, 1)

        self.comboBox_displacement_ux = QComboBox(self.frame_3)
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.addItem("")
        self.comboBox_displacement_ux.setObjectName(u"comboBox_displacement_ux")
        self.comboBox_displacement_ux.setMinimumSize(QSize(90, 26))
        self.comboBox_displacement_ux.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_displacement_ux, 1, 4, 1, 1)

        self.label_Rz_constant = QLabel(self.frame_3)
        self.label_Rz_constant.setObjectName(u"label_Rz_constant")
        self.label_Rz_constant.setMinimumSize(QSize(32, 26))
        self.label_Rz_constant.setMaximumSize(QSize(32, 26))
        self.label_Rz_constant.setFont(font)
        self.label_Rz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rz_constant, 6, 1, 1, 1)

        self.comboBox_displacement_uz = QComboBox(self.frame_3)
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.addItem("")
        self.comboBox_displacement_uz.setObjectName(u"comboBox_displacement_uz")
        self.comboBox_displacement_uz.setMinimumSize(QSize(90, 26))
        self.comboBox_displacement_uz.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_displacement_uz, 3, 4, 1, 1)

        self.lineEdit_real_Rx = QLineEdit(self.frame_3)
        self.lineEdit_real_Rx.setObjectName(u"lineEdit_real_Rx")
        self.lineEdit_real_Rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Rx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Rx.setFont(font1)
        self.lineEdit_real_Rx.setStyleSheet(u"")
        self.lineEdit_real_Rx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Rx, 4, 2, 1, 1)

        self.lineEdit_imag_Rz = QLineEdit(self.frame_3)
        self.lineEdit_imag_Rz.setObjectName(u"lineEdit_imag_Rz")
        self.lineEdit_imag_Rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Rz.setFont(font1)
        self.lineEdit_imag_Rz.setStyleSheet(u"")
        self.lineEdit_imag_Rz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Rz, 6, 3, 1, 1)

        self.label_Rx_constant = QLabel(self.frame_3)
        self.label_Rx_constant.setObjectName(u"label_Rx_constant")
        self.label_Rx_constant.setMinimumSize(QSize(32, 26))
        self.label_Rx_constant.setMaximumSize(QSize(32, 26))
        self.label_Rx_constant.setFont(font)
        self.label_Rx_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rx_constant, 4, 1, 1, 1)

        self.lineEdit_imag_Rx = QLineEdit(self.frame_3)
        self.lineEdit_imag_Rx.setObjectName(u"lineEdit_imag_Rx")
        self.lineEdit_imag_Rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Rx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Rx.setFont(font1)
        self.lineEdit_imag_Rx.setStyleSheet(u"")
        self.lineEdit_imag_Rx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Rx, 4, 3, 1, 1)

        self.comboBox_rotation_ry = QComboBox(self.frame_3)
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.addItem("")
        self.comboBox_rotation_ry.setObjectName(u"comboBox_rotation_ry")
        self.comboBox_rotation_ry.setMinimumSize(QSize(90, 26))
        self.comboBox_rotation_ry.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_rotation_ry, 5, 4, 1, 1)

        self.lineEdit_imag_Uy = QLineEdit(self.frame_3)
        self.lineEdit_imag_Uy.setObjectName(u"lineEdit_imag_Uy")
        self.lineEdit_imag_Uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Uy.setFont(font1)
        self.lineEdit_imag_Uy.setStyleSheet(u"")
        self.lineEdit_imag_Uy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_Uy, 2, 3, 1, 1)

        self.comboBox_rotation_rz = QComboBox(self.frame_3)
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.addItem("")
        self.comboBox_rotation_rz.setObjectName(u"comboBox_rotation_rz")
        self.comboBox_rotation_rz.setMinimumSize(QSize(90, 26))
        self.comboBox_rotation_rz.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_rotation_rz, 6, 4, 1, 1)

        self.lineEdit_real_Uy = QLineEdit(self.frame_3)
        self.lineEdit_real_Uy.setObjectName(u"lineEdit_real_Uy")
        self.lineEdit_real_Uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Uy.setFont(font1)
        self.lineEdit_real_Uy.setStyleSheet(u"")
        self.lineEdit_real_Uy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_Uy, 2, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 1, 5, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constant_values, "")
        self.tab_table_values = QWidget()
        self.tab_table_values.setObjectName(u"tab_table_values")
        self.gridLayout_15 = QGridLayout(self.tab_table_values)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.tab_table_values)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.lineEdit_Uz_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Uz_table_path.setObjectName(u"lineEdit_Uz_table_path")
        self.lineEdit_Uz_table_path.setEnabled(True)
        self.lineEdit_Uz_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Uz_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Uz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Uz_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Uz_table_path, 2, 2, 1, 1)

        self.pushButton_load_Ux_table = QPushButton(self.frame_9)
        self.pushButton_load_Ux_table.setObjectName(u"pushButton_load_Ux_table")
        self.pushButton_load_Ux_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Ux_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Ux_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Ux_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Ux_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Ux_table.setFont(font)
        self.pushButton_load_Ux_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Ux_table, 0, 3, 1, 1)

        self.label_Uz_table = QLabel(self.frame_9)
        self.label_Uz_table.setObjectName(u"label_Uz_table")
        self.label_Uz_table.setEnabled(True)
        self.label_Uz_table.setMinimumSize(QSize(0, 26))
        self.label_Uz_table.setMaximumSize(QSize(38, 26))
        self.label_Uz_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Uz_table, 2, 1, 1, 1)

        self.pushButton_load_Rx_table = QPushButton(self.frame_9)
        self.pushButton_load_Rx_table.setObjectName(u"pushButton_load_Rx_table")
        self.pushButton_load_Rx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Rx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Rx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Rx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Rx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Rx_table.setFont(font)
        self.pushButton_load_Rx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Rx_table, 3, 3, 1, 1)

        self.pushButton_load_Rz_table = QPushButton(self.frame_9)
        self.pushButton_load_Rz_table.setObjectName(u"pushButton_load_Rz_table")
        self.pushButton_load_Rz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Rz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Rz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Rz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Rz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Rz_table.setFont(font)
        self.pushButton_load_Rz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Rz_table, 5, 3, 1, 1)

        self.label_Rz_table = QLabel(self.frame_9)
        self.label_Rz_table.setObjectName(u"label_Rz_table")
        self.label_Rz_table.setEnabled(True)
        self.label_Rz_table.setMinimumSize(QSize(0, 26))
        self.label_Rz_table.setMaximumSize(QSize(38, 26))
        self.label_Rz_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Rz_table, 5, 1, 1, 1)

        self.label_Ry_table = QLabel(self.frame_9)
        self.label_Ry_table.setObjectName(u"label_Ry_table")
        self.label_Ry_table.setEnabled(True)
        self.label_Ry_table.setMinimumSize(QSize(0, 26))
        self.label_Ry_table.setMaximumSize(QSize(38, 26))
        self.label_Ry_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Ry_table, 4, 1, 1, 1)

        self.pushButton_load_Ry_table = QPushButton(self.frame_9)
        self.pushButton_load_Ry_table.setObjectName(u"pushButton_load_Ry_table")
        self.pushButton_load_Ry_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Ry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Ry_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Ry_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Ry_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Ry_table.setFont(font)
        self.pushButton_load_Ry_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Ry_table, 4, 3, 1, 1)

        self.lineEdit_Ry_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Ry_table_path.setObjectName(u"lineEdit_Ry_table_path")
        self.lineEdit_Ry_table_path.setEnabled(True)
        self.lineEdit_Ry_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Ry_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Ry_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Ry_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Ry_table_path, 4, 2, 1, 1)

        self.label_Ux_table = QLabel(self.frame_9)
        self.label_Ux_table.setObjectName(u"label_Ux_table")
        self.label_Ux_table.setEnabled(True)
        self.label_Ux_table.setMinimumSize(QSize(0, 26))
        self.label_Ux_table.setMaximumSize(QSize(38, 26))
        self.label_Ux_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Ux_table, 0, 1, 1, 1)

        self.lineEdit_Uy_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Uy_table_path.setObjectName(u"lineEdit_Uy_table_path")
        self.lineEdit_Uy_table_path.setEnabled(True)
        self.lineEdit_Uy_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Uy_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Uy_table_path.setStyleSheet(u"")
        self.lineEdit_Uy_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Uy_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Uy_table_path, 1, 2, 1, 1)

        self.lineEdit_Rx_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Rx_table_path.setObjectName(u"lineEdit_Rx_table_path")
        self.lineEdit_Rx_table_path.setEnabled(True)
        self.lineEdit_Rx_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Rx_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Rx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Rx_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Rx_table_path, 3, 2, 1, 1)

        self.label_Uy_table = QLabel(self.frame_9)
        self.label_Uy_table.setObjectName(u"label_Uy_table")
        self.label_Uy_table.setEnabled(True)
        self.label_Uy_table.setMinimumSize(QSize(0, 26))
        self.label_Uy_table.setMaximumSize(QSize(38, 26))
        self.label_Uy_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Uy_table, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.label_Rx_table = QLabel(self.frame_9)
        self.label_Rx_table.setObjectName(u"label_Rx_table")
        self.label_Rx_table.setEnabled(True)
        self.label_Rx_table.setMinimumSize(QSize(0, 26))
        self.label_Rx_table.setMaximumSize(QSize(38, 26))
        self.label_Rx_table.setFont(font)

        self.gridLayout_3.addWidget(self.label_Rx_table, 3, 1, 1, 1)

        self.pushButton_load_Uy_table = QPushButton(self.frame_9)
        self.pushButton_load_Uy_table.setObjectName(u"pushButton_load_Uy_table")
        self.pushButton_load_Uy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Uy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Uy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Uy_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Uy_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Uy_table.setFont(font)
        self.pushButton_load_Uy_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Uy_table, 1, 3, 1, 1)

        self.lineEdit_Rz_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Rz_table_path.setObjectName(u"lineEdit_Rz_table_path")
        self.lineEdit_Rz_table_path.setEnabled(True)
        self.lineEdit_Rz_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Rz_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Rz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Rz_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Rz_table_path, 5, 2, 1, 1)

        self.lineEdit_Ux_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Ux_table_path.setObjectName(u"lineEdit_Ux_table_path")
        self.lineEdit_Ux_table_path.setEnabled(True)
        self.lineEdit_Ux_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_Ux_table_path.setMaximumSize(QSize(300, 26))
        self.lineEdit_Ux_table_path.setStyleSheet(u"")
        self.lineEdit_Ux_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_Ux_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Ux_table_path, 0, 2, 1, 1)

        self.pushButton_load_Uz_table = QPushButton(self.frame_9)
        self.pushButton_load_Uz_table.setObjectName(u"pushButton_load_Uz_table")
        self.pushButton_load_Uz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Uz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Uz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Uz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Uz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Uz_table.setFont(font)
        self.pushButton_load_Uz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Uz_table, 2, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_9, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.tab_table_values)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 42))
        self.frame_6.setMaximumSize(QSize(16777215, 42))
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_2 = QGridLayout(self.frame_6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(6, 0, 6, 0)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.comboBox_angular_data_type = QComboBox(self.frame_6)
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.addItem("")
        self.comboBox_angular_data_type.setObjectName(u"comboBox_angular_data_type")
        self.comboBox_angular_data_type.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_angular_data_type, 0, 5, 1, 1)

        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout_2.addWidget(self.label_5, 0, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 0, 6, 1, 1)

        self.comboBox_linear_data_type = QComboBox(self.frame_6)
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.setObjectName(u"comboBox_linear_data_type")
        self.comboBox_linear_data_type.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_linear_data_type, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)


        self.gridLayout_15.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_table_values, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_12 = QGridLayout(self.tab_remove)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.tab_remove)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.treeWidget_nodal_info = QTreeWidget(self.frame_5)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(9)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font3)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font3)
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(280, 180))
        self.treeWidget_nodal_info.setMaximumSize(QSize(320, 240))
        self.treeWidget_nodal_info.setFont(font3)
        self.treeWidget_nodal_info.setIndentation(1)
        self.treeWidget_nodal_info.setHeaderHidden(False)
        self.treeWidget_nodal_info.header().setHighlightSections(False)
        self.treeWidget_nodal_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_nodal_info.header().setStretchLastSection(True)

        self.gridLayout_11.addWidget(self.treeWidget_nodal_info, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.tab_remove)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_10 = QGridLayout(self.frame_4)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_4)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(80, 28))
        self.pushButton_reset.setMaximumSize(QSize(80, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_4)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setEnabled(True)
        self.pushButton_remove.setMinimumSize(QSize(80, 28))
        self.pushButton_remove.setMaximumSize(QSize(80, 28))
        self.pushButton_remove.setFont(font4)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_4, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_6.addWidget(self.tabWidget_main, 1, 0, 1, 2)

        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_7 = QGridLayout(self.frame)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(8)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_node_ids = QLineEdit(self.frame)
        self.lineEdit_node_ids.setObjectName(u"lineEdit_node_ids")
        self.lineEdit_node_ids.setMinimumSize(QSize(160, 26))
        self.lineEdit_node_ids.setMaximumSize(QSize(160, 26))
        self.lineEdit_node_ids.setFont(font)
        self.lineEdit_node_ids.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_node_ids.setStyleSheet(u"")
        self.lineEdit_node_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_node_ids, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 26))
        self.label_2.setMaximumSize(QSize(120, 26))
        self.label_2.setFont(font)

        self.gridLayout_7.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 2)


        self.gridLayout_4.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(16777215, 42))
        self.frame_title.setSizeIncrement(QSize(0, 0))
        self.frame_title.setBaseSize(QSize(0, 0))
        font5 = QFont()
        font5.setPointSize(1)
        self.frame_title.setFont(font5)
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.frame_title)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font6 = QFont()
        font6.setPointSize(11)
        self.label.setFont(font6)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setTextFormat(Qt.TextFormat.PlainText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 40))
        self.frame_7.setMaximumSize(QSize(16777215, 40))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.pushButton_exit_tab0 = QPushButton(self.frame_7)
        self.pushButton_exit_tab0.setObjectName(u"pushButton_exit_tab0")
        self.pushButton_exit_tab0.setMinimumSize(QSize(100, 28))
        self.pushButton_exit_tab0.setMaximumSize(QSize(100, 28))
        self.pushButton_exit_tab0.setFont(font)
        self.pushButton_exit_tab0.setStyleSheet(u"")
        self.pushButton_exit_tab0.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_exit_tab0, 0, 0, 1, 1)

        self.pushButton_attribute = QPushButton(self.frame_7)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_attribute, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_7, 2, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_real_Ux)
        QWidget.setTabOrder(self.lineEdit_real_Ux, self.lineEdit_imag_Ux)
        QWidget.setTabOrder(self.lineEdit_imag_Ux, self.lineEdit_real_Uy)
        QWidget.setTabOrder(self.lineEdit_real_Uy, self.lineEdit_imag_Uy)
        QWidget.setTabOrder(self.lineEdit_imag_Uy, self.lineEdit_real_Uz)
        QWidget.setTabOrder(self.lineEdit_real_Uz, self.lineEdit_imag_Uz)
        QWidget.setTabOrder(self.lineEdit_imag_Uz, self.lineEdit_real_Rx)
        QWidget.setTabOrder(self.lineEdit_real_Rx, self.lineEdit_imag_Rx)
        QWidget.setTabOrder(self.lineEdit_imag_Rx, self.lineEdit_real_Ry)
        QWidget.setTabOrder(self.lineEdit_real_Ry, self.lineEdit_imag_Ry)
        QWidget.setTabOrder(self.lineEdit_imag_Ry, self.lineEdit_real_Rz)
        QWidget.setTabOrder(self.lineEdit_real_Rz, self.lineEdit_imag_Rz)
        QWidget.setTabOrder(self.lineEdit_imag_Rz, self.comboBox_linear_data_type)
        QWidget.setTabOrder(self.comboBox_linear_data_type, self.comboBox_angular_data_type)
        QWidget.setTabOrder(self.comboBox_angular_data_type, self.lineEdit_Ux_table_path)
        QWidget.setTabOrder(self.lineEdit_Ux_table_path, self.pushButton_load_Ux_table)
        QWidget.setTabOrder(self.pushButton_load_Ux_table, self.lineEdit_Uy_table_path)
        QWidget.setTabOrder(self.lineEdit_Uy_table_path, self.pushButton_load_Uy_table)
        QWidget.setTabOrder(self.pushButton_load_Uy_table, self.lineEdit_Uz_table_path)
        QWidget.setTabOrder(self.lineEdit_Uz_table_path, self.pushButton_load_Uz_table)
        QWidget.setTabOrder(self.pushButton_load_Uz_table, self.lineEdit_Rx_table_path)
        QWidget.setTabOrder(self.lineEdit_Rx_table_path, self.pushButton_load_Rx_table)
        QWidget.setTabOrder(self.pushButton_load_Rx_table, self.lineEdit_Ry_table_path)
        QWidget.setTabOrder(self.lineEdit_Ry_table_path, self.pushButton_load_Ry_table)
        QWidget.setTabOrder(self.pushButton_load_Ry_table, self.lineEdit_Rz_table_path)
        QWidget.setTabOrder(self.lineEdit_Rz_table_path, self.pushButton_load_Rz_table)
        QWidget.setTabOrder(self.pushButton_load_Rz_table, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_remove.setDefault(True)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("")
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_imaginary.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_real.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.lineEdit_real_Ux.setText("")
        self.label_Uz_constant.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.comboBox_displacement_uy.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_uy.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_uy.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.label_Ry_constant.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.label_Ux_constant.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.pushButton_all_dof_fixed.setText(QCoreApplication.translate("Dialog", u"All DOF fixed", None))
        self.pushButton_all_dof_free.setText(QCoreApplication.translate("Dialog", u"All DOF free", None))
        self.comboBox_rotation_rx.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_rx.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_rx.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.label_Uy_constant.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.comboBox_displacement_ux.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_ux.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_ux.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.label_Rz_constant.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.comboBox_displacement_uz.setItemText(0, QCoreApplication.translate("Dialog", u"Value (m)", None))
        self.comboBox_displacement_uz.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_displacement_uz.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.label_Rx_constant.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.comboBox_rotation_ry.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_ry.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_ry.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.comboBox_rotation_rz.setItemText(0, QCoreApplication.translate("Dialog", u"Value (rad)", None))
        self.comboBox_rotation_rz.setItemText(1, QCoreApplication.translate("Dialog", u"Free", None))
        self.comboBox_rotation_rz.setItemText(2, QCoreApplication.translate("Dialog", u"Fixed", None))

        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant", None))
        self.pushButton_load_Ux_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Uz_table.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.pushButton_load_Rx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Rz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Rz_table.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.label_Ry_table.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.pushButton_load_Ry_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ux_table.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.label_Uy_table.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.label_Rx_table.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.pushButton_load_Uy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Uz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.comboBox_angular_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_angular_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_angular_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Angular:", None))
        self.comboBox_linear_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_linear_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_linear_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Linear:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_table_values), QCoreApplication.translate("Dialog", u"Tabular", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"List", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selected nodes:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of freedom prescription setup", None))
        self.pushButton_exit_tab0.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
    # retranslateUi



class PrescribedDofInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_imag_Ux: QLineEdit
                                                        - label_imaginary: QLabel
                                                        - lineEdit_real_Rz: QLineEdit
                                                        - label_real: QLabel
                                                        - lineEdit_real_Uz: QLineEdit
                                                        - lineEdit_real_Ry: QLineEdit
                                                        - lineEdit_real_Ux: QLineEdit
                                                        - lineEdit_imag_Uz: QLineEdit
                                                        - label_Uz_constant: QLabel
                                                        - comboBox_displacement_uy: QComboBox
                                                        - label_Ry_constant: QLabel
                                                        - label_Ux_constant: QLabel
                                                        - lineEdit_imag_Ry: QLineEdit
                                                        - frame_10: QFrame
                                                            - (Layout): QGridLayout
                                                                    - pushButton_all_dof_fixed: QPushButton
                                                                    - pushButton_all_dof_free: QPushButton
                                                        - comboBox_rotation_rx: QComboBox
                                                        - label_Uy_constant: QLabel
                                                        - comboBox_displacement_ux: QComboBox
                                                        - label_Rz_constant: QLabel
                                                        - comboBox_displacement_uz: QComboBox
                                                        - lineEdit_real_Rx: QLineEdit
                                                        - lineEdit_imag_Rz: QLineEdit
                                                        - label_Rx_constant: QLabel
                                                        - lineEdit_imag_Rx: QLineEdit
                                                        - comboBox_rotation_ry: QComboBox
                                                        - lineEdit_imag_Uy: QLineEdit
                                                        - comboBox_rotation_rz: QComboBox
                                                        - lineEdit_real_Uy: QLineEdit
                                - tab_table_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_Uz_table_path: QLineEdit
                                                        - pushButton_load_Ux_table: QPushButton
                                                        - label_Uz_table: QLabel
                                                        - pushButton_load_Rx_table: QPushButton
                                                        - pushButton_load_Rz_table: QPushButton
                                                        - label_Rz_table: QLabel
                                                        - label_Ry_table: QLabel
                                                        - pushButton_load_Ry_table: QPushButton
                                                        - lineEdit_Ry_table_path: QLineEdit
                                                        - label_Ux_table: QLabel
                                                        - lineEdit_Uy_table_path: QLineEdit
                                                        - lineEdit_Rx_table_path: QLineEdit
                                                        - label_Uy_table: QLabel
                                                        - label_Rx_table: QLabel
                                                        - pushButton_load_Uy_table: QPushButton
                                                        - lineEdit_Rz_table_path: QLineEdit
                                                        - lineEdit_Ux_table_path: QLineEdit
                                                        - pushButton_load_Uz_table: QPushButton
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_angular_data_type: QComboBox
                                                        - label_5: QLabel
                                                        - comboBox_linear_data_type: QComboBox
                                                        - label_3: QLabel
                                - tab_remove: QWidget
                                    - (Layout): QGridLayout
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_nodal_info: QTreeWidget
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_node_ids: QLineEdit
                                        - label_2: QLabel
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit_tab0: QPushButton
                            - pushButton_attribute: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
