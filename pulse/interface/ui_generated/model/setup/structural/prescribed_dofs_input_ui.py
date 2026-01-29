# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prescribed_dofs_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(391, 435)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(391, 435))
        Dialog.setMaximumSize(QSize(391, 435))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(1000, 1000))
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_main)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_prescribed_dofs = QTabWidget(self.frame_main)
        self.tabWidget_prescribed_dofs.setObjectName(u"tabWidget_prescribed_dofs")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget_prescribed_dofs.setFont(font)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_9 = QGridLayout(self.tab_constant_values)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.tab_constant_values)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(8)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.label_imaginary = QLabel(self.frame_3)
        self.label_imaginary.setObjectName(u"label_imaginary")
        self.label_imaginary.setMinimumSize(QSize(80, 22))
        self.label_imaginary.setMaximumSize(QSize(80, 22))
        self.label_imaginary.setFont(font)
        self.label_imaginary.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_imaginary, 0, 3, 1, 1)

        self.label_Ux_constant = QLabel(self.frame_3)
        self.label_Ux_constant.setObjectName(u"label_Ux_constant")
        self.label_Ux_constant.setMinimumSize(QSize(70, 26))
        self.label_Ux_constant.setMaximumSize(QSize(70, 26))
        self.label_Ux_constant.setFont(font)
        self.label_Ux_constant.setStyleSheet(u"")
        self.label_Ux_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ux_constant, 1, 1, 1, 1)

        self.lineEdit_real_ux = QLineEdit(self.frame_3)
        self.lineEdit_real_ux.setObjectName(u"lineEdit_real_ux")
        self.lineEdit_real_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ux.setMaximumSize(QSize(80, 26))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.lineEdit_real_ux.setFont(font1)
        self.lineEdit_real_ux.setStyleSheet(u"")
        self.lineEdit_real_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_ux, 1, 2, 1, 1)

        self.lineEdit_imag_ux = QLineEdit(self.frame_3)
        self.lineEdit_imag_ux.setObjectName(u"lineEdit_imag_ux")
        self.lineEdit_imag_ux.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ux.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_ux.setFont(font1)
        self.lineEdit_imag_ux.setStyleSheet(u"")
        self.lineEdit_imag_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_ux, 1, 3, 1, 1)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(50, 26))
        self.label_13.setMaximumSize(QSize(50, 26))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_13, 1, 4, 1, 1)

        self.label_Uy_constant = QLabel(self.frame_3)
        self.label_Uy_constant.setObjectName(u"label_Uy_constant")
        self.label_Uy_constant.setMinimumSize(QSize(70, 26))
        self.label_Uy_constant.setMaximumSize(QSize(70, 26))
        self.label_Uy_constant.setFont(font)
        self.label_Uy_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uy_constant, 2, 1, 1, 1)

        self.lineEdit_imag_uy = QLineEdit(self.frame_3)
        self.lineEdit_imag_uy.setObjectName(u"lineEdit_imag_uy")
        self.lineEdit_imag_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_uy.setFont(font1)
        self.lineEdit_imag_uy.setStyleSheet(u"")
        self.lineEdit_imag_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_uy, 2, 3, 1, 1)

        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(50, 26))
        self.label_14.setMaximumSize(QSize(50, 26))
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_14, 2, 4, 1, 1)

        self.lineEdit_real_uy = QLineEdit(self.frame_3)
        self.lineEdit_real_uy.setObjectName(u"lineEdit_real_uy")
        self.lineEdit_real_uy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uy.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_uy.setFont(font1)
        self.lineEdit_real_uy.setStyleSheet(u"")
        self.lineEdit_real_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_uy, 2, 2, 1, 1)

        self.label_Uz_constant = QLabel(self.frame_3)
        self.label_Uz_constant.setObjectName(u"label_Uz_constant")
        self.label_Uz_constant.setMinimumSize(QSize(70, 26))
        self.label_Uz_constant.setMaximumSize(QSize(70, 26))
        self.label_Uz_constant.setFont(font)
        self.label_Uz_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uz_constant, 3, 1, 1, 1)

        self.label_real = QLabel(self.frame_3)
        self.label_real.setObjectName(u"label_real")
        self.label_real.setMinimumSize(QSize(80, 22))
        self.label_real.setMaximumSize(QSize(80, 22))
        self.label_real.setFont(font)
        self.label_real.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_real, 0, 2, 1, 1)

        self.label_17 = QLabel(self.frame_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(50, 26))
        self.label_17.setMaximumSize(QSize(50, 26))
        self.label_17.setFont(font2)
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_17, 5, 4, 1, 1)

        self.lineEdit_imag_ry = QLineEdit(self.frame_3)
        self.lineEdit_imag_ry.setObjectName(u"lineEdit_imag_ry")
        self.lineEdit_imag_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_ry.setFont(font1)
        self.lineEdit_imag_ry.setStyleSheet(u"")
        self.lineEdit_imag_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_ry, 5, 3, 1, 1)

        self.label_Rz_constant = QLabel(self.frame_3)
        self.label_Rz_constant.setObjectName(u"label_Rz_constant")
        self.label_Rz_constant.setMinimumSize(QSize(70, 26))
        self.label_Rz_constant.setMaximumSize(QSize(70, 26))
        self.label_Rz_constant.setFont(font)
        self.label_Rz_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rz_constant, 6, 1, 1, 1)

        self.label_15 = QLabel(self.frame_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(50, 26))
        self.label_15.setMaximumSize(QSize(50, 26))
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_15, 6, 4, 1, 1)

        self.lineEdit_real_rz = QLineEdit(self.frame_3)
        self.lineEdit_real_rz.setObjectName(u"lineEdit_real_rz")
        self.lineEdit_real_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_rz.setFont(font1)
        self.lineEdit_real_rz.setStyleSheet(u"")
        self.lineEdit_real_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_rz, 6, 2, 1, 1)

        self.lineEdit_imag_rz = QLineEdit(self.frame_3)
        self.lineEdit_imag_rz.setObjectName(u"lineEdit_imag_rz")
        self.lineEdit_imag_rz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_rz.setFont(font1)
        self.lineEdit_imag_rz.setStyleSheet(u"")
        self.lineEdit_imag_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_rz, 6, 3, 1, 1)

        self.label_18 = QLabel(self.frame_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(70, 26))
        self.label_18.setMaximumSize(QSize(70, 26))
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_18, 7, 1, 1, 1)

        self.lineEdit_imag_alldofs = QLineEdit(self.frame_3)
        self.lineEdit_imag_alldofs.setObjectName(u"lineEdit_imag_alldofs")
        self.lineEdit_imag_alldofs.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_alldofs.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_alldofs.setFont(font1)
        self.lineEdit_imag_alldofs.setStyleSheet(u"")
        self.lineEdit_imag_alldofs.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_alldofs, 7, 3, 1, 1)

        self.lineEdit_real_alldofs = QLineEdit(self.frame_3)
        self.lineEdit_real_alldofs.setObjectName(u"lineEdit_real_alldofs")
        self.lineEdit_real_alldofs.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_alldofs.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_alldofs.setFont(font1)
        self.lineEdit_real_alldofs.setStyleSheet(u"")
        self.lineEdit_real_alldofs.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_alldofs, 7, 2, 1, 1)

        self.label_27 = QLabel(self.frame_3)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(50, 26))
        self.label_27.setMaximumSize(QSize(50, 26))
        self.label_27.setFont(font2)
        self.label_27.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_27, 7, 4, 1, 1)

        self.lineEdit_real_uz = QLineEdit(self.frame_3)
        self.lineEdit_real_uz.setObjectName(u"lineEdit_real_uz")
        self.lineEdit_real_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_uz.setFont(font1)
        self.lineEdit_real_uz.setStyleSheet(u"")
        self.lineEdit_real_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_uz, 3, 2, 1, 1)

        self.lineEdit_imag_uz = QLineEdit(self.frame_3)
        self.lineEdit_imag_uz.setObjectName(u"lineEdit_imag_uz")
        self.lineEdit_imag_uz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_uz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_uz.setFont(font1)
        self.lineEdit_imag_uz.setStyleSheet(u"")
        self.lineEdit_imag_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_uz, 3, 3, 1, 1)

        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(50, 26))
        self.label_21.setMaximumSize(QSize(50, 26))
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_21, 3, 4, 1, 1)

        self.label_Rx_constant = QLabel(self.frame_3)
        self.label_Rx_constant.setObjectName(u"label_Rx_constant")
        self.label_Rx_constant.setMinimumSize(QSize(70, 26))
        self.label_Rx_constant.setMaximumSize(QSize(70, 26))
        self.label_Rx_constant.setFont(font)
        self.label_Rx_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rx_constant, 4, 1, 1, 1)

        self.lineEdit_real_rx = QLineEdit(self.frame_3)
        self.lineEdit_real_rx.setObjectName(u"lineEdit_real_rx")
        self.lineEdit_real_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_rx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_rx.setFont(font1)
        self.lineEdit_real_rx.setStyleSheet(u"")
        self.lineEdit_real_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_rx, 4, 2, 1, 1)

        self.lineEdit_imag_rx = QLineEdit(self.frame_3)
        self.lineEdit_imag_rx.setObjectName(u"lineEdit_imag_rx")
        self.lineEdit_imag_rx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_rx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_rx.setFont(font1)
        self.lineEdit_imag_rx.setStyleSheet(u"")
        self.lineEdit_imag_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_imag_rx, 4, 3, 1, 1)

        self.label_16 = QLabel(self.frame_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(50, 26))
        self.label_16.setMaximumSize(QSize(50, 26))
        self.label_16.setFont(font2)
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_16, 4, 4, 1, 1)

        self.label_Ry_constant = QLabel(self.frame_3)
        self.label_Ry_constant.setObjectName(u"label_Ry_constant")
        self.label_Ry_constant.setMinimumSize(QSize(70, 26))
        self.label_Ry_constant.setMaximumSize(QSize(70, 26))
        self.label_Ry_constant.setFont(font)
        self.label_Ry_constant.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ry_constant, 5, 1, 1, 1)

        self.lineEdit_real_ry = QLineEdit(self.frame_3)
        self.lineEdit_real_ry.setObjectName(u"lineEdit_real_ry")
        self.lineEdit_real_ry.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_ry.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_ry.setFont(font1)
        self.lineEdit_real_ry.setStyleSheet(u"")
        self.lineEdit_real_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_real_ry, 5, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 1, 5, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_constant_values)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.pushButton_constant_value_confirm = QPushButton(self.frame_2)
        self.pushButton_constant_value_confirm.setObjectName(u"pushButton_constant_value_confirm")
        self.pushButton_constant_value_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_constant_value_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_constant_value_confirm.setFont(font)
        self.pushButton_constant_value_confirm.setStyleSheet(u"")
        self.pushButton_constant_value_confirm.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_constant_value_confirm, 0, 1, 1, 1)

        self.pushButton_exit_tab0 = QPushButton(self.frame_2)
        self.pushButton_exit_tab0.setObjectName(u"pushButton_exit_tab0")
        self.pushButton_exit_tab0.setMinimumSize(QSize(100, 28))
        self.pushButton_exit_tab0.setMaximumSize(QSize(100, 28))
        self.pushButton_exit_tab0.setFont(font)
        self.pushButton_exit_tab0.setStyleSheet(u"")
        self.pushButton_exit_tab0.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_exit_tab0, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_2, 1, 0, 1, 1)

        self.tabWidget_prescribed_dofs.addTab(self.tab_constant_values, "")
        self.tab_table_values = QWidget()
        self.tab_table_values.setObjectName(u"tab_table_values")
        self.gridLayout_15 = QGridLayout(self.tab_table_values)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.tab_table_values)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 48))
        self.frame_8.setMaximumSize(QSize(16777215, 48))
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_8)
        self.gridLayout_16.setSpacing(4)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(4, 4, 4, 4)
        self.pushButton_table_values_confirm = QPushButton(self.frame_8)
        self.pushButton_table_values_confirm.setObjectName(u"pushButton_table_values_confirm")
        self.pushButton_table_values_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_table_values_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_table_values_confirm.setFont(font)
        self.pushButton_table_values_confirm.setStyleSheet(u"")
        self.pushButton_table_values_confirm.setAutoDefault(False)

        self.gridLayout_16.addWidget(self.pushButton_table_values_confirm, 0, 1, 1, 1)

        self.pushButton_exit_tab1 = QPushButton(self.frame_8)
        self.pushButton_exit_tab1.setObjectName(u"pushButton_exit_tab1")
        self.pushButton_exit_tab1.setMinimumSize(QSize(100, 28))
        self.pushButton_exit_tab1.setMaximumSize(QSize(100, 28))
        self.pushButton_exit_tab1.setFont(font)
        self.pushButton_exit_tab1.setStyleSheet(u"")
        self.pushButton_exit_tab1.setAutoDefault(False)

        self.gridLayout_16.addWidget(self.pushButton_exit_tab1, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_8, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.tab_table_values)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.lineEdit_path_table_ry = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ry.setObjectName(u"lineEdit_path_table_ry")
        self.lineEdit_path_table_ry.setEnabled(False)
        self.lineEdit_path_table_ry.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_ry.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ry, 4, 1, 1, 1)

        self.pushButton_load_ry_table = QPushButton(self.frame_9)
        self.pushButton_load_ry_table.setObjectName(u"pushButton_load_ry_table")
        self.pushButton_load_ry_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ry_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ry_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ry_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_ry_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_ry_table.setFont(font)
        self.pushButton_load_ry_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_ry_table, 4, 2, 1, 1)

        self.label_Ry_table = QLabel(self.frame_9)
        self.label_Ry_table.setObjectName(u"label_Ry_table")
        self.label_Ry_table.setEnabled(True)
        self.label_Ry_table.setMinimumSize(QSize(0, 26))
        self.label_Ry_table.setMaximumSize(QSize(38, 26))
        self.label_Ry_table.setFont(font)
        self.label_Ry_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ry_table, 4, 0, 1, 1)

        self.label_Rz_table = QLabel(self.frame_9)
        self.label_Rz_table.setObjectName(u"label_Rz_table")
        self.label_Rz_table.setEnabled(True)
        self.label_Rz_table.setMinimumSize(QSize(0, 26))
        self.label_Rz_table.setMaximumSize(QSize(38, 26))
        self.label_Rz_table.setFont(font)
        self.label_Rz_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rz_table, 5, 0, 1, 1)

        self.lineEdit_path_table_rz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rz.setObjectName(u"lineEdit_path_table_rz")
        self.lineEdit_path_table_rz.setEnabled(False)
        self.lineEdit_path_table_rz.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_rz.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rz, 5, 1, 1, 1)

        self.lineEdit_path_table_uy = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uy.setObjectName(u"lineEdit_path_table_uy")
        self.lineEdit_path_table_uy.setEnabled(False)
        self.lineEdit_path_table_uy.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_uy.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_uy.setStyleSheet(u"")
        self.lineEdit_path_table_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uy, 1, 1, 1, 1)

        self.pushButton_load_uz_table = QPushButton(self.frame_9)
        self.pushButton_load_uz_table.setObjectName(u"pushButton_load_uz_table")
        self.pushButton_load_uz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_uz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_uz_table.setFont(font)
        self.pushButton_load_uz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_uz_table, 2, 2, 1, 1)

        self.pushButton_load_uy_table = QPushButton(self.frame_9)
        self.pushButton_load_uy_table.setObjectName(u"pushButton_load_uy_table")
        self.pushButton_load_uy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_uy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_uy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_uy_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_uy_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_uy_table.setFont(font)
        self.pushButton_load_uy_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_uy_table, 1, 2, 1, 1)

        self.pushButton_load_rx_table = QPushButton(self.frame_9)
        self.pushButton_load_rx_table.setObjectName(u"pushButton_load_rx_table")
        self.pushButton_load_rx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_rx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_rx_table.setFont(font)
        self.pushButton_load_rx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_rx_table, 3, 2, 1, 1)

        self.label_Ux_table = QLabel(self.frame_9)
        self.label_Ux_table.setObjectName(u"label_Ux_table")
        self.label_Ux_table.setEnabled(True)
        self.label_Ux_table.setMinimumSize(QSize(0, 26))
        self.label_Ux_table.setMaximumSize(QSize(38, 26))
        self.label_Ux_table.setFont(font)
        self.label_Ux_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Ux_table, 0, 0, 1, 1)

        self.lineEdit_path_table_rx = QLineEdit(self.frame_9)
        self.lineEdit_path_table_rx.setObjectName(u"lineEdit_path_table_rx")
        self.lineEdit_path_table_rx.setEnabled(False)
        self.lineEdit_path_table_rx.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_rx.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_rx, 3, 1, 1, 1)

        self.label_Rx_table = QLabel(self.frame_9)
        self.label_Rx_table.setObjectName(u"label_Rx_table")
        self.label_Rx_table.setEnabled(True)
        self.label_Rx_table.setMinimumSize(QSize(0, 26))
        self.label_Rx_table.setMaximumSize(QSize(38, 26))
        self.label_Rx_table.setFont(font)
        self.label_Rx_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Rx_table, 3, 0, 1, 1)

        self.lineEdit_path_table_uz = QLineEdit(self.frame_9)
        self.lineEdit_path_table_uz.setObjectName(u"lineEdit_path_table_uz")
        self.lineEdit_path_table_uz.setEnabled(False)
        self.lineEdit_path_table_uz.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_uz.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_uz, 2, 1, 1, 1)

        self.label_Uy_table = QLabel(self.frame_9)
        self.label_Uy_table.setObjectName(u"label_Uy_table")
        self.label_Uy_table.setEnabled(True)
        self.label_Uy_table.setMinimumSize(QSize(0, 26))
        self.label_Uy_table.setMaximumSize(QSize(38, 26))
        self.label_Uy_table.setFont(font)
        self.label_Uy_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uy_table, 1, 0, 1, 1)

        self.pushButton_load_rz_table = QPushButton(self.frame_9)
        self.pushButton_load_rz_table.setObjectName(u"pushButton_load_rz_table")
        self.pushButton_load_rz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_rz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_rz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_rz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_rz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_rz_table.setFont(font)
        self.pushButton_load_rz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_rz_table, 5, 2, 1, 1)

        self.lineEdit_path_table_ux = QLineEdit(self.frame_9)
        self.lineEdit_path_table_ux.setObjectName(u"lineEdit_path_table_ux")
        self.lineEdit_path_table_ux.setEnabled(False)
        self.lineEdit_path_table_ux.setMinimumSize(QSize(210, 26))
        self.lineEdit_path_table_ux.setMaximumSize(QSize(240, 26))
        self.lineEdit_path_table_ux.setStyleSheet(u"")
        self.lineEdit_path_table_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_path_table_ux, 0, 1, 1, 1)

        self.label_Uz_table = QLabel(self.frame_9)
        self.label_Uz_table.setObjectName(u"label_Uz_table")
        self.label_Uz_table.setEnabled(True)
        self.label_Uz_table.setMinimumSize(QSize(0, 26))
        self.label_Uz_table.setMaximumSize(QSize(38, 26))
        self.label_Uz_table.setFont(font)
        self.label_Uz_table.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_Uz_table, 2, 0, 1, 1)

        self.pushButton_load_ux_table = QPushButton(self.frame_9)
        self.pushButton_load_ux_table.setObjectName(u"pushButton_load_ux_table")
        self.pushButton_load_ux_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_ux_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_ux_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_ux_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_ux_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_ux_table.setFont(font)
        self.pushButton_load_ux_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_ux_table, 0, 2, 1, 1)


        self.gridLayout_15.addWidget(self.frame_9, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.tab_table_values)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 42))
        self.frame_6.setMaximumSize(QSize(16777215, 42))
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(6, 0, 6, 0)
        self.comboBox_linear_data_type = QComboBox(self.frame_6)
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.addItem("")
        self.comboBox_linear_data_type.setObjectName(u"comboBox_linear_data_type")
        self.comboBox_linear_data_type.setFont(font)

        self.gridLayout_2.addWidget(self.comboBox_linear_data_type, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)

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
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 0, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 0, 6, 1, 1)


        self.gridLayout_15.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget_prescribed_dofs.addTab(self.tab_table_values, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_12 = QGridLayout(self.tab_remove)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.tab_remove)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.treeWidget_nodal_info = QTreeWidget(self.frame_5)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(9)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font3);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font3);
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(280, 180))
        self.treeWidget_nodal_info.setMaximumSize(QSize(280, 200))
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
        self.frame_4.setMinimumSize(QSize(0, 48))
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
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

        self.tabWidget_prescribed_dofs.addTab(self.tab_remove, "")

        self.gridLayout_6.addWidget(self.tabWidget_prescribed_dofs, 1, 0, 1, 2)

        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(8)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_node_ids = QLineEdit(self.frame)
        self.lineEdit_node_ids.setObjectName(u"lineEdit_node_ids")
        self.lineEdit_node_ids.setMinimumSize(QSize(160, 26))
        self.lineEdit_node_ids.setMaximumSize(QSize(160, 26))
        self.lineEdit_node_ids.setFont(font)
        self.lineEdit_node_ids.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_node_ids.setStyleSheet(u"")
        self.lineEdit_node_ids.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_node_ids, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 26))
        self.label_2.setMaximumSize(QSize(120, 26))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


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
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
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
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_title, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_prescribed_dofs, self.lineEdit_real_ux)
        QWidget.setTabOrder(self.lineEdit_real_ux, self.lineEdit_imag_ux)
        QWidget.setTabOrder(self.lineEdit_imag_ux, self.lineEdit_real_uy)
        QWidget.setTabOrder(self.lineEdit_real_uy, self.lineEdit_imag_uy)
        QWidget.setTabOrder(self.lineEdit_imag_uy, self.lineEdit_real_uz)
        QWidget.setTabOrder(self.lineEdit_real_uz, self.lineEdit_imag_uz)
        QWidget.setTabOrder(self.lineEdit_imag_uz, self.lineEdit_real_rx)
        QWidget.setTabOrder(self.lineEdit_real_rx, self.lineEdit_imag_rx)
        QWidget.setTabOrder(self.lineEdit_imag_rx, self.lineEdit_real_ry)
        QWidget.setTabOrder(self.lineEdit_real_ry, self.lineEdit_imag_ry)
        QWidget.setTabOrder(self.lineEdit_imag_ry, self.lineEdit_real_rz)
        QWidget.setTabOrder(self.lineEdit_real_rz, self.lineEdit_imag_rz)
        QWidget.setTabOrder(self.lineEdit_imag_rz, self.lineEdit_real_alldofs)
        QWidget.setTabOrder(self.lineEdit_real_alldofs, self.lineEdit_imag_alldofs)
        QWidget.setTabOrder(self.lineEdit_imag_alldofs, self.pushButton_constant_value_confirm)
        QWidget.setTabOrder(self.pushButton_constant_value_confirm, self.pushButton_exit_tab0)
        QWidget.setTabOrder(self.pushButton_exit_tab0, self.comboBox_linear_data_type)
        QWidget.setTabOrder(self.comboBox_linear_data_type, self.comboBox_angular_data_type)
        QWidget.setTabOrder(self.comboBox_angular_data_type, self.lineEdit_path_table_ux)
        QWidget.setTabOrder(self.lineEdit_path_table_ux, self.pushButton_load_ux_table)
        QWidget.setTabOrder(self.pushButton_load_ux_table, self.lineEdit_path_table_uy)
        QWidget.setTabOrder(self.lineEdit_path_table_uy, self.pushButton_load_uy_table)
        QWidget.setTabOrder(self.pushButton_load_uy_table, self.lineEdit_path_table_uz)
        QWidget.setTabOrder(self.lineEdit_path_table_uz, self.pushButton_load_uz_table)
        QWidget.setTabOrder(self.pushButton_load_uz_table, self.lineEdit_path_table_rx)
        QWidget.setTabOrder(self.lineEdit_path_table_rx, self.pushButton_load_rx_table)
        QWidget.setTabOrder(self.pushButton_load_rx_table, self.lineEdit_path_table_ry)
        QWidget.setTabOrder(self.lineEdit_path_table_ry, self.pushButton_load_ry_table)
        QWidget.setTabOrder(self.pushButton_load_ry_table, self.lineEdit_path_table_rz)
        QWidget.setTabOrder(self.lineEdit_path_table_rz, self.pushButton_load_rz_table)
        QWidget.setTabOrder(self.pushButton_load_rz_table, self.pushButton_table_values_confirm)
        QWidget.setTabOrder(self.pushButton_table_values_confirm, self.pushButton_exit_tab1)
        QWidget.setTabOrder(self.pushButton_exit_tab1, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_prescribed_dofs.setCurrentIndex(0)
        self.pushButton_constant_value_confirm.setDefault(True)
        self.pushButton_table_values_confirm.setDefault(True)
        self.pushButton_remove.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("")
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_imaginary.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_Ux_constant.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.lineEdit_real_ux.setText("")
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_Uy_constant.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_Uz_constant.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.label_real.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_Rz_constant.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"All DOFs:", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_Rx_constant.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[rad]", None))
        self.label_Ry_constant.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.pushButton_constant_value_confirm.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit_tab0.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_prescribed_dofs.setTabText(self.tabWidget_prescribed_dofs.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_table_values_confirm.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit_tab1.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_load_ry_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ry_table.setText(QCoreApplication.translate("Dialog", u"Ry:", None))
        self.label_Rz_table.setText(QCoreApplication.translate("Dialog", u"Rz:", None))
        self.pushButton_load_uz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_uy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_rx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ux_table.setText(QCoreApplication.translate("Dialog", u"Ux:", None))
        self.label_Rx_table.setText(QCoreApplication.translate("Dialog", u"Rx:", None))
        self.label_Uy_table.setText(QCoreApplication.translate("Dialog", u"Uy:", None))
        self.pushButton_load_rz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Uz_table.setText(QCoreApplication.translate("Dialog", u"Uz:", None))
        self.pushButton_load_ux_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.comboBox_linear_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_linear_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_linear_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Linear:", None))
        self.comboBox_angular_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Displacement", None))
        self.comboBox_angular_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Velocity", None))
        self.comboBox_angular_data_type.setItemText(2, QCoreApplication.translate("Dialog", u" Acceleration", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Angular:", None))
        self.tabWidget_prescribed_dofs.setTabText(self.tabWidget_prescribed_dofs.indexOf(self.tab_table_values), QCoreApplication.translate("Dialog", u"Load tables", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None));
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.tabWidget_prescribed_dofs.setTabText(self.tabWidget_prescribed_dofs.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Node IDs:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Degrees of freedom prescription setup", None))
    # retranslateUi



class PrescribedDofsInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_prescribed_dofs: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_imaginary: QLabel
                                                        - label_Ux_constant: QLabel
                                                        - lineEdit_real_ux: QLineEdit
                                                        - lineEdit_imag_ux: QLineEdit
                                                        - label_13: QLabel
                                                        - label_Uy_constant: QLabel
                                                        - lineEdit_imag_uy: QLineEdit
                                                        - label_14: QLabel
                                                        - lineEdit_real_uy: QLineEdit
                                                        - label_Uz_constant: QLabel
                                                        - label_real: QLabel
                                                        - label_17: QLabel
                                                        - lineEdit_imag_ry: QLineEdit
                                                        - label_Rz_constant: QLabel
                                                        - label_15: QLabel
                                                        - lineEdit_real_rz: QLineEdit
                                                        - lineEdit_imag_rz: QLineEdit
                                                        - label_18: QLabel
                                                        - lineEdit_imag_alldofs: QLineEdit
                                                        - lineEdit_real_alldofs: QLineEdit
                                                        - label_27: QLabel
                                                        - lineEdit_real_uz: QLineEdit
                                                        - lineEdit_imag_uz: QLineEdit
                                                        - label_21: QLabel
                                                        - label_Rx_constant: QLabel
                                                        - lineEdit_real_rx: QLineEdit
                                                        - lineEdit_imag_rx: QLineEdit
                                                        - label_16: QLabel
                                                        - label_Ry_constant: QLabel
                                                        - lineEdit_real_ry: QLineEdit
                                            - frame_2: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_constant_value_confirm: QPushButton
                                                        - pushButton_exit_tab0: QPushButton
                                - tab_table_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_table_values_confirm: QPushButton
                                                        - pushButton_exit_tab1: QPushButton
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_path_table_ry: QLineEdit
                                                        - pushButton_load_ry_table: QPushButton
                                                        - label_Ry_table: QLabel
                                                        - label_Rz_table: QLabel
                                                        - lineEdit_path_table_rz: QLineEdit
                                                        - lineEdit_path_table_uy: QLineEdit
                                                        - pushButton_load_uz_table: QPushButton
                                                        - pushButton_load_uy_table: QPushButton
                                                        - pushButton_load_rx_table: QPushButton
                                                        - label_Ux_table: QLabel
                                                        - lineEdit_path_table_rx: QLineEdit
                                                        - label_Rx_table: QLabel
                                                        - lineEdit_path_table_uz: QLineEdit
                                                        - label_Uy_table: QLabel
                                                        - pushButton_load_rz_table: QPushButton
                                                        - lineEdit_path_table_ux: QLineEdit
                                                        - label_Uz_table: QLabel
                                                        - pushButton_load_ux_table: QPushButton
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_linear_data_type: QComboBox
                                                        - label_3: QLabel
                                                        - comboBox_angular_data_type: QComboBox
                                                        - label_5: QLabel
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
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
