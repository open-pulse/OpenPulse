# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nodal_loads_input.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.NonModal)
        Dialog.resize(391, 435)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(391, 435))
        Dialog.setMaximumSize(QSize(391, 435))
        Dialog.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(16777215, 42))
        self.frame_title.setSizeIncrement(QSize(0, 0))
        self.frame_title.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(1)
        self.frame_title.setFont(font)
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.frame_title)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setTextFormat(Qt.TextFormat.PlainText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_title, 0, 0, 1, 1)

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
        self.tabWidget_nodal_loads = QTabWidget(self.frame_main)
        self.tabWidget_nodal_loads.setObjectName(u"tabWidget_nodal_loads")
        font2 = QFont()
        font2.setPointSize(10)
        self.tabWidget_nodal_loads.setFont(font2)
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_9 = QGridLayout(self.tab_constant_values)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.tab_constant_values)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFont(font2)
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(8)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.label_Uz_constant = QLabel(self.frame_3)
        self.label_Uz_constant.setObjectName(u"label_Uz_constant")
        self.label_Uz_constant.setMinimumSize(QSize(48, 26))
        self.label_Uz_constant.setMaximumSize(QSize(48, 26))
        self.label_Uz_constant.setFont(font2)
        self.label_Uz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uz_constant, 3, 1, 1, 1)

        self.label_21 = QLabel(self.frame_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(48, 26))
        self.label_21.setMaximumSize(QSize(48, 26))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_21.setFont(font3)

        self.gridLayout_8.addWidget(self.label_21, 3, 4, 1, 1)

        self.label_16 = QLabel(self.frame_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(48, 26))
        self.label_16.setMaximumSize(QSize(48, 26))
        self.label_16.setFont(font3)

        self.gridLayout_8.addWidget(self.label_16, 4, 4, 1, 1)

        self.label_imaginary = QLabel(self.frame_3)
        self.label_imaginary.setObjectName(u"label_imaginary")
        self.label_imaginary.setMinimumSize(QSize(80, 22))
        self.label_imaginary.setMaximumSize(QSize(80, 22))
        self.label_imaginary.setFont(font2)
        self.label_imaginary.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_imaginary, 0, 3, 1, 1)

        self.lineEdit_real_Fy = QLineEdit(self.frame_3)
        self.lineEdit_real_Fy.setObjectName(u"lineEdit_real_Fy")
        self.lineEdit_real_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fy.setMaximumSize(QSize(80, 26))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.lineEdit_real_Fy.setFont(font4)
        self.lineEdit_real_Fy.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_Fy, 2, 2, 1, 1)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(48, 26))
        self.label_13.setMaximumSize(QSize(48, 26))
        self.label_13.setFont(font3)

        self.gridLayout_8.addWidget(self.label_13, 1, 4, 1, 1)

        self.lineEdit_imag_Mx = QLineEdit(self.frame_3)
        self.lineEdit_imag_Mx.setObjectName(u"lineEdit_imag_Mx")
        self.lineEdit_imag_Mx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Mx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Mx.setFont(font4)
        self.lineEdit_imag_Mx.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_Mx, 4, 3, 1, 1)

        self.label_17 = QLabel(self.frame_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(48, 26))
        self.label_17.setMaximumSize(QSize(48, 26))
        self.label_17.setFont(font3)

        self.gridLayout_8.addWidget(self.label_17, 5, 4, 1, 1)

        self.label_Uy_constant = QLabel(self.frame_3)
        self.label_Uy_constant.setObjectName(u"label_Uy_constant")
        self.label_Uy_constant.setMinimumSize(QSize(48, 26))
        self.label_Uy_constant.setMaximumSize(QSize(48, 26))
        self.label_Uy_constant.setFont(font2)
        self.label_Uy_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Uy_constant, 2, 1, 1, 1)

        self.label_real = QLabel(self.frame_3)
        self.label_real.setObjectName(u"label_real")
        self.label_real.setMinimumSize(QSize(80, 22))
        self.label_real.setMaximumSize(QSize(80, 22))
        self.label_real.setFont(font2)
        self.label_real.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_real, 0, 2, 1, 1)

        self.lineEdit_imag_Fx = QLineEdit(self.frame_3)
        self.lineEdit_imag_Fx.setObjectName(u"lineEdit_imag_Fx")
        self.lineEdit_imag_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fx.setFont(font4)
        self.lineEdit_imag_Fx.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_Fx, 1, 3, 1, 1)

        self.lineEdit_imag_Fz = QLineEdit(self.frame_3)
        self.lineEdit_imag_Fz.setObjectName(u"lineEdit_imag_Fz")
        self.lineEdit_imag_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fz.setFont(font4)
        self.lineEdit_imag_Fz.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_Fz, 3, 3, 1, 1)

        self.lineEdit_imag_Mz = QLineEdit(self.frame_3)
        self.lineEdit_imag_Mz.setObjectName(u"lineEdit_imag_Mz")
        self.lineEdit_imag_Mz.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Mz.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Mz.setFont(font4)
        self.lineEdit_imag_Mz.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_Mz, 6, 3, 1, 1)

        self.label_Ry_constant = QLabel(self.frame_3)
        self.label_Ry_constant.setObjectName(u"label_Ry_constant")
        self.label_Ry_constant.setMinimumSize(QSize(48, 26))
        self.label_Ry_constant.setMaximumSize(QSize(48, 26))
        self.label_Ry_constant.setFont(font2)
        self.label_Ry_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ry_constant, 5, 1, 1, 1)

        self.lineEdit_imag_My = QLineEdit(self.frame_3)
        self.lineEdit_imag_My.setObjectName(u"lineEdit_imag_My")
        self.lineEdit_imag_My.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_My.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_My.setFont(font4)
        self.lineEdit_imag_My.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_My, 5, 3, 1, 1)

        self.lineEdit_real_Fz = QLineEdit(self.frame_3)
        self.lineEdit_real_Fz.setObjectName(u"lineEdit_real_Fz")
        self.lineEdit_real_Fz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fz.setFont(font4)
        self.lineEdit_real_Fz.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_Fz, 3, 2, 1, 1)

        self.label_Rz_constant = QLabel(self.frame_3)
        self.label_Rz_constant.setObjectName(u"label_Rz_constant")
        self.label_Rz_constant.setMinimumSize(QSize(48, 26))
        self.label_Rz_constant.setMaximumSize(QSize(48, 26))
        self.label_Rz_constant.setFont(font2)
        self.label_Rz_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rz_constant, 6, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_5, 1, 5, 1, 1)

        self.lineEdit_real_Fx = QLineEdit(self.frame_3)
        self.lineEdit_real_Fx.setObjectName(u"lineEdit_real_Fx")
        self.lineEdit_real_Fx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Fx.setFont(font4)
        self.lineEdit_real_Fx.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_Fx, 1, 2, 1, 1)

        self.label_15 = QLabel(self.frame_3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(48, 26))
        self.label_15.setMaximumSize(QSize(48, 26))
        self.label_15.setFont(font3)

        self.gridLayout_8.addWidget(self.label_15, 6, 4, 1, 1)

        self.lineEdit_imag_Fy = QLineEdit(self.frame_3)
        self.lineEdit_imag_Fy.setObjectName(u"lineEdit_imag_Fy")
        self.lineEdit_imag_Fy.setMinimumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setMaximumSize(QSize(80, 26))
        self.lineEdit_imag_Fy.setFont(font4)
        self.lineEdit_imag_Fy.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_imag_Fy, 2, 3, 1, 1)

        self.label_Ux_constant = QLabel(self.frame_3)
        self.label_Ux_constant.setObjectName(u"label_Ux_constant")
        self.label_Ux_constant.setMinimumSize(QSize(48, 26))
        self.label_Ux_constant.setMaximumSize(QSize(48, 26))
        self.label_Ux_constant.setFont(font2)
        self.label_Ux_constant.setStyleSheet(u"")
        self.label_Ux_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Ux_constant, 1, 1, 1, 1)

        self.lineEdit_real_Mz = QLineEdit(self.frame_3)
        self.lineEdit_real_Mz.setObjectName(u"lineEdit_real_Mz")
        self.lineEdit_real_Mz.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Mz.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Mz.setFont(font4)
        self.lineEdit_real_Mz.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_Mz, 6, 2, 1, 1)

        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(48, 26))
        self.label_14.setMaximumSize(QSize(48, 26))
        self.label_14.setFont(font3)

        self.gridLayout_8.addWidget(self.label_14, 2, 4, 1, 1)

        self.lineEdit_real_Mx = QLineEdit(self.frame_3)
        self.lineEdit_real_Mx.setObjectName(u"lineEdit_real_Mx")
        self.lineEdit_real_Mx.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_Mx.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_Mx.setFont(font4)
        self.lineEdit_real_Mx.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_Mx, 4, 2, 1, 1)

        self.lineEdit_real_My = QLineEdit(self.frame_3)
        self.lineEdit_real_My.setObjectName(u"lineEdit_real_My")
        self.lineEdit_real_My.setMinimumSize(QSize(80, 26))
        self.lineEdit_real_My.setMaximumSize(QSize(80, 26))
        self.lineEdit_real_My.setFont(font4)
        self.lineEdit_real_My.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.lineEdit_real_My, 5, 2, 1, 1)

        self.label_Rx_constant = QLabel(self.frame_3)
        self.label_Rx_constant.setObjectName(u"label_Rx_constant")
        self.label_Rx_constant.setMinimumSize(QSize(48, 26))
        self.label_Rx_constant.setMaximumSize(QSize(48, 26))
        self.label_Rx_constant.setFont(font2)
        self.label_Rx_constant.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_Rx_constant, 4, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_3, 0, 0, 1, 1)

        self.tabWidget_nodal_loads.addTab(self.tab_constant_values, "")
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
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(7)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 2)
        self.pushButton_load_Mz_table = QPushButton(self.frame_9)
        self.pushButton_load_Mz_table.setObjectName(u"pushButton_load_Mz_table")
        self.pushButton_load_Mz_table.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Mz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Mz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Mz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Mz_table.setFont(font2)
        self.pushButton_load_Mz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Mz_table, 5, 3, 1, 1)

        self.lineEdit_Fz_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Fz_table_path.setObjectName(u"lineEdit_Fz_table_path")
        self.lineEdit_Fz_table_path.setEnabled(True)
        self.lineEdit_Fz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Fz_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_Fz_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Fz_table_path, 2, 2, 1, 1)

        self.pushButton_load_My_table = QPushButton(self.frame_9)
        self.pushButton_load_My_table.setObjectName(u"pushButton_load_My_table")
        self.pushButton_load_My_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_My_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_My_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_My_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_My_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_My_table.setFont(font2)
        self.pushButton_load_My_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_My_table, 4, 3, 1, 1)

        self.label_Rz_table = QLabel(self.frame_9)
        self.label_Rz_table.setObjectName(u"label_Rz_table")
        self.label_Rz_table.setEnabled(True)
        self.label_Rz_table.setMinimumSize(QSize(0, 26))
        self.label_Rz_table.setMaximumSize(QSize(38, 26))
        self.label_Rz_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Rz_table, 5, 1, 1, 1)

        self.lineEdit_My_table_path = QLineEdit(self.frame_9)
        self.lineEdit_My_table_path.setObjectName(u"lineEdit_My_table_path")
        self.lineEdit_My_table_path.setEnabled(True)
        self.lineEdit_My_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_My_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_My_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_My_table_path, 4, 2, 1, 1)

        self.label_Ux_table = QLabel(self.frame_9)
        self.label_Ux_table.setObjectName(u"label_Ux_table")
        self.label_Ux_table.setEnabled(True)
        self.label_Ux_table.setMinimumSize(QSize(0, 26))
        self.label_Ux_table.setMaximumSize(QSize(38, 26))
        self.label_Ux_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Ux_table, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.lineEdit_Mz_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Mz_table_path.setObjectName(u"lineEdit_Mz_table_path")
        self.lineEdit_Mz_table_path.setEnabled(True)
        self.lineEdit_Mz_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Mz_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_Mz_table_path.setStyleSheet(u"")
        self.lineEdit_Mz_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Mz_table_path, 5, 2, 1, 1)

        self.label_Rx_table = QLabel(self.frame_9)
        self.label_Rx_table.setObjectName(u"label_Rx_table")
        self.label_Rx_table.setEnabled(True)
        self.label_Rx_table.setMinimumSize(QSize(0, 26))
        self.label_Rx_table.setMaximumSize(QSize(38, 26))
        self.label_Rx_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Rx_table, 3, 1, 1, 1)

        self.lineEdit_Mx_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Mx_table_path.setObjectName(u"lineEdit_Mx_table_path")
        self.lineEdit_Mx_table_path.setEnabled(True)
        self.lineEdit_Mx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Mx_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_Mx_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Mx_table_path, 3, 2, 1, 1)

        self.pushButton_load_Fx_table = QPushButton(self.frame_9)
        self.pushButton_load_Fx_table.setObjectName(u"pushButton_load_Fx_table")
        self.pushButton_load_Fx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fx_table.setFont(font2)
        self.pushButton_load_Fx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fx_table, 0, 3, 1, 1)

        self.lineEdit_Fx_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Fx_table_path.setObjectName(u"lineEdit_Fx_table_path")
        self.lineEdit_Fx_table_path.setEnabled(True)
        self.lineEdit_Fx_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Fx_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_Fx_table_path.setStyleSheet(u"")
        self.lineEdit_Fx_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Fx_table_path, 0, 2, 1, 1)

        self.label_Uy_table = QLabel(self.frame_9)
        self.label_Uy_table.setObjectName(u"label_Uy_table")
        self.label_Uy_table.setEnabled(True)
        self.label_Uy_table.setMinimumSize(QSize(0, 26))
        self.label_Uy_table.setMaximumSize(QSize(38, 26))
        self.label_Uy_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Uy_table, 1, 1, 1, 1)

        self.lineEdit_Fy_table_path = QLineEdit(self.frame_9)
        self.lineEdit_Fy_table_path.setObjectName(u"lineEdit_Fy_table_path")
        self.lineEdit_Fy_table_path.setEnabled(True)
        self.lineEdit_Fy_table_path.setMinimumSize(QSize(240, 26))
        self.lineEdit_Fy_table_path.setMaximumSize(QSize(240, 26))
        self.lineEdit_Fy_table_path.setStyleSheet(u"")
        self.lineEdit_Fy_table_path.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.lineEdit_Fy_table_path, 1, 2, 1, 1)

        self.pushButton_load_Mx_table = QPushButton(self.frame_9)
        self.pushButton_load_Mx_table.setObjectName(u"pushButton_load_Mx_table")
        self.pushButton_load_Mx_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Mx_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Mx_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Mx_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Mx_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Mx_table.setFont(font2)
        self.pushButton_load_Mx_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Mx_table, 3, 3, 1, 1)

        self.label_Ry_table = QLabel(self.frame_9)
        self.label_Ry_table.setObjectName(u"label_Ry_table")
        self.label_Ry_table.setEnabled(True)
        self.label_Ry_table.setMinimumSize(QSize(0, 26))
        self.label_Ry_table.setMaximumSize(QSize(38, 26))
        self.label_Ry_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Ry_table, 4, 1, 1, 1)

        self.pushButton_load_Fz_table = QPushButton(self.frame_9)
        self.pushButton_load_Fz_table.setObjectName(u"pushButton_load_Fz_table")
        self.pushButton_load_Fz_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fz_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fz_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fz_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fz_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fz_table.setFont(font2)
        self.pushButton_load_Fz_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fz_table, 2, 3, 1, 1)

        self.pushButton_load_Fy_table = QPushButton(self.frame_9)
        self.pushButton_load_Fy_table.setObjectName(u"pushButton_load_Fy_table")
        self.pushButton_load_Fy_table.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.pushButton_load_Fy_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_Fy_table.setSizePolicy(sizePolicy1)
        self.pushButton_load_Fy_table.setMinimumSize(QSize(62, 26))
        self.pushButton_load_Fy_table.setMaximumSize(QSize(62, 26))
        self.pushButton_load_Fy_table.setFont(font2)
        self.pushButton_load_Fy_table.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_load_Fy_table, 1, 3, 1, 1)

        self.label_Uz_table = QLabel(self.frame_9)
        self.label_Uz_table.setObjectName(u"label_Uz_table")
        self.label_Uz_table.setEnabled(True)
        self.label_Uz_table.setMinimumSize(QSize(0, 26))
        self.label_Uz_table.setMaximumSize(QSize(38, 26))
        self.label_Uz_table.setFont(font2)

        self.gridLayout_3.addWidget(self.label_Uz_table, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_9, 0, 0, 1, 1)

        self.tabWidget_nodal_loads.addTab(self.tab_table_values, "")
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
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(9)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font5)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font5)
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(280, 120))
        self.treeWidget_nodal_info.setMaximumSize(QSize(280, 200))
        self.treeWidget_nodal_info.setFont(font5)
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
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.pushButton_reset.setFont(font6)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_4)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setEnabled(True)
        self.pushButton_remove.setMinimumSize(QSize(80, 28))
        self.pushButton_remove.setMaximumSize(QSize(80, 28))
        self.pushButton_remove.setFont(font6)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_4, 1, 0, 1, 1)

        self.tabWidget_nodal_loads.addTab(self.tab_remove, "")

        self.gridLayout_6.addWidget(self.tabWidget_nodal_loads, 1, 0, 1, 2)

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
        self.lineEdit_node_ids.setMinimumSize(QSize(160, 30))
        self.lineEdit_node_ids.setMaximumSize(QSize(160, 30))
        self.lineEdit_node_ids.setFont(font2)
        self.lineEdit_node_ids.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_node_ids.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.lineEdit_node_ids, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setMaximumSize(QSize(120, 30))
        self.label_2.setFont(font2)

        self.gridLayout_7.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 2)


        self.gridLayout_4.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_bottom_buttons = QFrame(Dialog)
        self.frame_bottom_buttons.setObjectName(u"frame_bottom_buttons")
        self.frame_bottom_buttons.setMinimumSize(QSize(0, 40))
        self.frame_bottom_buttons.setMaximumSize(QSize(16777215, 40))
        self.frame_bottom_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout = QGridLayout(self.frame_bottom_buttons)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_bottom_buttons)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_bottom_buttons)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_bottom_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_ids, self.tabWidget_nodal_loads)
        QWidget.setTabOrder(self.tabWidget_nodal_loads, self.lineEdit_real_Fx)
        QWidget.setTabOrder(self.lineEdit_real_Fx, self.lineEdit_imag_Fx)
        QWidget.setTabOrder(self.lineEdit_imag_Fx, self.lineEdit_real_Fy)
        QWidget.setTabOrder(self.lineEdit_real_Fy, self.lineEdit_imag_Fy)
        QWidget.setTabOrder(self.lineEdit_imag_Fy, self.lineEdit_real_Fz)
        QWidget.setTabOrder(self.lineEdit_real_Fz, self.lineEdit_imag_Fz)
        QWidget.setTabOrder(self.lineEdit_imag_Fz, self.lineEdit_real_Mx)
        QWidget.setTabOrder(self.lineEdit_real_Mx, self.lineEdit_imag_Mx)
        QWidget.setTabOrder(self.lineEdit_imag_Mx, self.lineEdit_real_My)
        QWidget.setTabOrder(self.lineEdit_real_My, self.lineEdit_imag_My)
        QWidget.setTabOrder(self.lineEdit_imag_My, self.lineEdit_real_Mz)
        QWidget.setTabOrder(self.lineEdit_real_Mz, self.lineEdit_imag_Mz)
        QWidget.setTabOrder(self.lineEdit_imag_Mz, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.lineEdit_Fx_table_path)
        QWidget.setTabOrder(self.lineEdit_Fx_table_path, self.pushButton_load_Fx_table)
        QWidget.setTabOrder(self.pushButton_load_Fx_table, self.lineEdit_Fy_table_path)
        QWidget.setTabOrder(self.lineEdit_Fy_table_path, self.pushButton_load_Fy_table)
        QWidget.setTabOrder(self.pushButton_load_Fy_table, self.lineEdit_Fz_table_path)
        QWidget.setTabOrder(self.lineEdit_Fz_table_path, self.pushButton_load_Fz_table)
        QWidget.setTabOrder(self.pushButton_load_Fz_table, self.lineEdit_Mx_table_path)
        QWidget.setTabOrder(self.lineEdit_Mx_table_path, self.pushButton_load_Mx_table)
        QWidget.setTabOrder(self.pushButton_load_Mx_table, self.lineEdit_My_table_path)
        QWidget.setTabOrder(self.lineEdit_My_table_path, self.pushButton_load_My_table)
        QWidget.setTabOrder(self.pushButton_load_My_table, self.lineEdit_Mz_table_path)
        QWidget.setTabOrder(self.lineEdit_Mz_table_path, self.pushButton_load_Mz_table)
        QWidget.setTabOrder(self.pushButton_load_Mz_table, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_reset)

        self.retranslateUi(Dialog)

        self.tabWidget_nodal_loads.setCurrentIndex(0)
        self.pushButton_remove.setDefault(False)
        self.pushButton_attribute.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("")
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"External nodal loads setup", None))
        self.label_Uz_constant.setText(QCoreApplication.translate("Dialog", u"Fz:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_imaginary.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_Uy_constant.setText(QCoreApplication.translate("Dialog", u"Fy:", None))
        self.label_real.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_Ry_constant.setText(QCoreApplication.translate("Dialog", u"My:", None))
        self.label_Rz_constant.setText(QCoreApplication.translate("Dialog", u"Mz:", None))
        self.lineEdit_real_Fx.setText("")
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[N.m]", None))
        self.label_Ux_constant.setText(QCoreApplication.translate("Dialog", u"Fx:", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[N]", None))
        self.label_Rx_constant.setText(QCoreApplication.translate("Dialog", u"Mx:", None))
        self.tabWidget_nodal_loads.setTabText(self.tabWidget_nodal_loads.indexOf(self.tab_constant_values), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_load_Mz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_My_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Rz_table.setText(QCoreApplication.translate("Dialog", u"Mz:", None))
        self.label_Ux_table.setText(QCoreApplication.translate("Dialog", u"Fx:", None))
        self.label_Rx_table.setText(QCoreApplication.translate("Dialog", u"Mx:", None))
        self.pushButton_load_Fx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Uy_table.setText(QCoreApplication.translate("Dialog", u"Fy:", None))
        self.pushButton_load_Mx_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Ry_table.setText(QCoreApplication.translate("Dialog", u"My:", None))
        self.pushButton_load_Fz_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_load_Fy_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_Uz_table.setText(QCoreApplication.translate("Dialog", u"Fz:", None))
        self.tabWidget_nodal_loads.setTabText(self.tabWidget_nodal_loads.indexOf(self.tab_table_values), QCoreApplication.translate("Dialog", u"Load tables", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"DOFs", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_nodal_loads.setTabText(self.tabWidget_nodal_loads.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Node IDs:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class NodalLoadsInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_nodal_loads: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_Uz_constant: QLabel
                                                        - label_21: QLabel
                                                        - label_16: QLabel
                                                        - label_imaginary: QLabel
                                                        - lineEdit_real_Fy: QLineEdit
                                                        - label_13: QLabel
                                                        - lineEdit_imag_Mx: QLineEdit
                                                        - label_17: QLabel
                                                        - label_Uy_constant: QLabel
                                                        - label_real: QLabel
                                                        - lineEdit_imag_Fx: QLineEdit
                                                        - lineEdit_imag_Fz: QLineEdit
                                                        - lineEdit_imag_Mz: QLineEdit
                                                        - label_Ry_constant: QLabel
                                                        - lineEdit_imag_My: QLineEdit
                                                        - lineEdit_real_Fz: QLineEdit
                                                        - label_Rz_constant: QLabel
                                                        - lineEdit_real_Fx: QLineEdit
                                                        - label_15: QLabel
                                                        - lineEdit_imag_Fy: QLineEdit
                                                        - label_Ux_constant: QLabel
                                                        - lineEdit_real_Mz: QLineEdit
                                                        - label_14: QLabel
                                                        - lineEdit_real_Mx: QLineEdit
                                                        - lineEdit_real_My: QLineEdit
                                                        - label_Rx_constant: QLabel
                                - tab_table_values: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_load_Mz_table: QPushButton
                                                        - lineEdit_Fz_table_path: QLineEdit
                                                        - pushButton_load_My_table: QPushButton
                                                        - label_Rz_table: QLabel
                                                        - lineEdit_My_table_path: QLineEdit
                                                        - label_Ux_table: QLabel
                                                        - lineEdit_Mz_table_path: QLineEdit
                                                        - label_Rx_table: QLabel
                                                        - lineEdit_Mx_table_path: QLineEdit
                                                        - pushButton_load_Fx_table: QPushButton
                                                        - lineEdit_Fx_table_path: QLineEdit
                                                        - label_Uy_table: QLabel
                                                        - lineEdit_Fy_table_path: QLineEdit
                                                        - pushButton_load_Mx_table: QPushButton
                                                        - label_Ry_table: QLabel
                                                        - pushButton_load_Fz_table: QPushButton
                                                        - pushButton_load_Fy_table: QPushButton
                                                        - label_Uz_table: QLabel
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
                - frame_bottom_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
