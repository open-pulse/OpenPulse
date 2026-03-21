# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequency_response_plot.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QDialog, QFrame, QGridLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 740)
        Dialog.setMinimumSize(QSize(1000, 740))
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setMinimumSize(QSize(0, 200))
        self.frame_lower.setFrameShape(QFrame.Box)
        self.frame_lower.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_lower)
        self.gridLayout_20.setSpacing(2)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(2, 2, 2, 2)
        self.frame_left = QFrame(self.frame_lower)
        self.frame_left.setObjectName(u"frame_left")
        self.frame_left.setFrameShape(QFrame.NoFrame)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_left)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.widget_plot = QWidget(self.frame_left)
        self.widget_plot.setObjectName(u"widget_plot")

        self.gridLayout_2.addWidget(self.widget_plot, 0, 1, 1, 1)


        self.gridLayout_20.addWidget(self.frame_left, 0, 0, 1, 1)

        self.frame_right = QFrame(self.frame_lower)
        self.frame_right.setObjectName(u"frame_right")
        self.frame_right.setMinimumSize(QSize(200, 0))
        self.frame_right.setMaximumSize(QSize(240, 1677215))
        self.frame_right.setFrameShape(QFrame.NoFrame)
        self.frame_right.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_right)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(2, 4, 2, 4)
        self.frame_22 = QFrame(self.frame_right)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(0, 42))
        self.frame_22.setMaximumSize(QSize(16777215, 48))
        self.frame_22.setFrameShape(QFrame.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.gridLayout_24 = QGridLayout(self.frame_22)
        self.gridLayout_24.setSpacing(2)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(2, 2, 2, 2)
        self.pushButton_import_data = QPushButton(self.frame_22)
        self.pushButton_import_data.setObjectName(u"pushButton_import_data")
        self.pushButton_import_data.setEnabled(True)
        self.pushButton_import_data.setMinimumSize(QSize(120, 30))
        self.pushButton_import_data.setMaximumSize(QSize(120, 30))
        font = QFont()
        font.setPointSize(10)
        self.pushButton_import_data.setFont(font)
        self.pushButton_import_data.setStyleSheet(u"")
        self.pushButton_import_data.setAutoDefault(False)

        self.gridLayout_24.addWidget(self.pushButton_import_data, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_22, 3, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_right)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.frame_5)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMaximumSize(QSize(16777215, 140))
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_14)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setVerticalSpacing(2)
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.frame_14)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 32))
        self.frame_13.setMaximumSize(QSize(16777215, 32))
        self.frame_13.setFrameShape(QFrame.Box)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_13)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_13)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(120, 20))
        self.label_9.setMaximumSize(QSize(165, 32))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_9.setFont(font1)
        self.label_9.setFrameShape(QFrame.NoFrame)
        self.label_9.setFrameShadow(QFrame.Sunken)
        self.label_9.setTextFormat(Qt.AutoText)
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setWordWrap(False)
        self.label_9.setIndent(0)

        self.gridLayout_11.addWidget(self.label_9, 0, 0, 1, 1)


        self.gridLayout_18.addWidget(self.frame_13, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.frame_14)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 0))
        self.frame_9.setMaximumSize(QSize(220, 120))
        self.frame_9.setFrameShape(QFrame.Box)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_9)
        self.gridLayout_12.setSpacing(4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.frame_12 = QFrame(self.frame_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.frame_12.setFont(font2)
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_12)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(4)
        self.gridLayout_10.setVerticalSpacing(2)
        self.gridLayout_10.setContentsMargins(2, 0, 2, 0)
        self.comboBox_plot_type = QComboBox(self.frame_12)
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.addItem("")
        self.comboBox_plot_type.setObjectName(u"comboBox_plot_type")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_plot_type.sizePolicy().hasHeightForWidth())
        self.comboBox_plot_type.setSizePolicy(sizePolicy1)
        self.comboBox_plot_type.setMinimumSize(QSize(80, 0))
        self.comboBox_plot_type.setMaximumSize(QSize(100, 26))
        self.comboBox_plot_type.setFont(font1)
        self.comboBox_plot_type.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.label = QLabel(self.frame_12)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(16777215, 26))
        self.label.setFont(font)

        self.gridLayout_10.addWidget(self.label, 0, 1, 1, 1)

        self.frame_19 = QFrame(self.frame_12)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Raised)

        self.gridLayout_10.addWidget(self.frame_19, 0, 3, 1, 1)

        self.frame_21 = QFrame(self.frame_12)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)

        self.gridLayout_10.addWidget(self.frame_21, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_12, 0, 0, 1, 1)

        self.frame_legends_2 = QFrame(self.frame_9)
        self.frame_legends_2.setObjectName(u"frame_legends_2")
        self.frame_legends_2.setMaximumSize(QSize(16777215, 28))
        self.frame_legends_2.setFrameShape(QFrame.NoFrame)
        self.frame_legends_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_legends_2)
        self.gridLayout_19.setSpacing(2)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(2, 2, 2, 2)
        self.checkBox_legends = QCheckBox(self.frame_legends_2)
        self.checkBox_legends.setObjectName(u"checkBox_legends")
        self.checkBox_legends.setMinimumSize(QSize(75, 0))
        self.checkBox_legends.setMaximumSize(QSize(140, 26))
        self.checkBox_legends.setFont(font1)
        self.checkBox_legends.setChecked(True)

        self.gridLayout_19.addWidget(self.checkBox_legends, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_legends_2, 1, 0, 1, 1)

        self.frame_legends_3 = QFrame(self.frame_9)
        self.frame_legends_3.setObjectName(u"frame_legends_3")
        self.frame_legends_3.setMaximumSize(QSize(16777215, 28))
        self.frame_legends_3.setFrameShape(QFrame.NoFrame)
        self.frame_legends_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_legends_3)
        self.gridLayout_22.setSpacing(2)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(2, 2, 2, 2)
        self.checkBox_grid = QCheckBox(self.frame_legends_3)
        self.checkBox_grid.setObjectName(u"checkBox_grid")
        self.checkBox_grid.setMinimumSize(QSize(75, 0))
        self.checkBox_grid.setMaximumSize(QSize(140, 26))
        self.checkBox_grid.setFont(font1)
        self.checkBox_grid.setChecked(True)

        self.gridLayout_22.addWidget(self.checkBox_grid, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_legends_3, 2, 0, 1, 1)


        self.gridLayout_18.addWidget(self.frame_9, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_14, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMaximumSize(QSize(16777215, 200))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_7)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 32))
        self.frame_8.setMaximumSize(QSize(16777215, 32))
        self.frame_8.setFrameShape(QFrame.Box)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_8)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(120, 20))
        self.label_8.setMaximumSize(QSize(165, 32))
        self.label_8.setFont(font1)
        self.label_8.setFrameShape(QFrame.NoFrame)
        self.label_8.setFrameShadow(QFrame.Sunken)
        self.label_8.setTextFormat(Qt.AutoText)
        self.label_8.setScaledContents(False)
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setWordWrap(False)
        self.label_8.setIndent(0)

        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_7)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(220, 180))
        self.frame_4.setSizeIncrement(QSize(0, 0))
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 4, 4, 4)
        self.frame_20 = QFrame(self.frame_4)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMaximumSize(QSize(16777215, 28))
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_20)
        self.gridLayout_26.setSpacing(2)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(2, 2, 2, 2)
        self.radioButton_real = QRadioButton(self.frame_20)
        self.buttonGroup_y_data = QButtonGroup(Dialog)
        self.buttonGroup_y_data.setObjectName(u"buttonGroup_y_data")
        self.buttonGroup_y_data.addButton(self.radioButton_real)
        self.radioButton_real.setObjectName(u"radioButton_real")
        self.radioButton_real.setMinimumSize(QSize(140, 0))
        self.radioButton_real.setMaximumSize(QSize(140, 26))
        self.radioButton_real.setFont(font1)

        self.gridLayout_26.addWidget(self.radioButton_real, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_20, 2, 0, 1, 1)

        self.frame_25 = QFrame(self.frame_4)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMaximumSize(QSize(16777215, 28))
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_25)
        self.gridLayout_27.setSpacing(2)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(2, 2, 2, 2)
        self.radioButton_imaginary = QRadioButton(self.frame_25)
        self.buttonGroup_y_data.addButton(self.radioButton_imaginary)
        self.radioButton_imaginary.setObjectName(u"radioButton_imaginary")
        self.radioButton_imaginary.setMinimumSize(QSize(140, 0))
        self.radioButton_imaginary.setMaximumSize(QSize(140, 26))
        self.radioButton_imaginary.setFont(font1)

        self.gridLayout_27.addWidget(self.radioButton_imaginary, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_25, 3, 0, 1, 1)

        self.frame_26 = QFrame(self.frame_4)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMaximumSize(QSize(16777215, 28))
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.gridLayout_28 = QGridLayout(self.frame_26)
        self.gridLayout_28.setSpacing(2)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setContentsMargins(2, 2, 2, 2)
        self.radioButton_decibel_scale = QRadioButton(self.frame_26)
        self.buttonGroup_y_data.addButton(self.radioButton_decibel_scale)
        self.radioButton_decibel_scale.setObjectName(u"radioButton_decibel_scale")
        self.radioButton_decibel_scale.setMinimumSize(QSize(140, 0))
        self.radioButton_decibel_scale.setMaximumSize(QSize(140, 26))
        self.radioButton_decibel_scale.setFont(font1)
        self.radioButton_decibel_scale.setIconSize(QSize(30, 30))
        self.radioButton_decibel_scale.setChecked(False)

        self.gridLayout_28.addWidget(self.radioButton_decibel_scale, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_26, 4, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_4)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMaximumSize(QSize(16777215, 28))
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_25 = QGridLayout(self.frame_10)
        self.gridLayout_25.setSpacing(2)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(2, 2, 2, 2)
        self.radioButton_absolute = QRadioButton(self.frame_10)
        self.buttonGroup_y_data.addButton(self.radioButton_absolute)
        self.radioButton_absolute.setObjectName(u"radioButton_absolute")
        self.radioButton_absolute.setMinimumSize(QSize(140, 0))
        self.radioButton_absolute.setMaximumSize(QSize(140, 26))
        self.radioButton_absolute.setFont(font1)
        self.radioButton_absolute.setIconSize(QSize(30, 30))
        self.radioButton_absolute.setChecked(True)

        self.gridLayout_25.addWidget(self.radioButton_absolute, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_10, 1, 0, 1, 1)

        self.frame_27 = QFrame(self.frame_4)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMaximumSize(QSize(16777215, 28))
        self.frame_27.setFont(font2)
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.gridLayout_29 = QGridLayout(self.frame_27)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setHorizontalSpacing(4)
        self.gridLayout_29.setVerticalSpacing(2)
        self.gridLayout_29.setContentsMargins(2, 2, 2, 2)
        self.frame_28 = QFrame(self.frame_27)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Raised)

        self.gridLayout_29.addWidget(self.frame_28, 0, 2, 1, 1)

        self.label_4 = QLabel(self.frame_27)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 0))
        self.label_4.setMaximumSize(QSize(16777215, 26))
        self.label_4.setFont(font)

        self.gridLayout_29.addWidget(self.label_4, 0, 0, 1, 1)

        self.comboBox_differentiate_data = QComboBox(self.frame_27)
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.setObjectName(u"comboBox_differentiate_data")
        sizePolicy1.setHeightForWidth(self.comboBox_differentiate_data.sizePolicy().hasHeightForWidth())
        self.comboBox_differentiate_data.setSizePolicy(sizePolicy1)
        self.comboBox_differentiate_data.setMinimumSize(QSize(80, 0))
        self.comboBox_differentiate_data.setMaximumSize(QSize(100, 26))
        self.comboBox_differentiate_data.setFont(font1)
        self.comboBox_differentiate_data.setStyleSheet(u"")

        self.gridLayout_29.addWidget(self.comboBox_differentiate_data, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_27, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_7, 1, 0, 1, 1)

        self.frame_18 = QFrame(self.frame_5)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 200))
        self.frame_18.setMaximumSize(QSize(16777215, 220))
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_18)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setVerticalSpacing(2)
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.frame_18)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMinimumSize(QSize(85, 32))
        self.frame_32.setMaximumSize(QSize(240, 32))
        self.frame_32.setSizeIncrement(QSize(0, 110))
        self.frame_32.setFrameShape(QFrame.Box)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.gridLayout_32 = QGridLayout(self.frame_32)
        self.gridLayout_32.setSpacing(0)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.frame_32)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 20))
        self.label_13.setMaximumSize(QSize(16777215, 32))
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_32.addWidget(self.label_13, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_32, 0, 0, 1, 1)

        self.frame_30 = QFrame(self.frame_18)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setMinimumSize(QSize(85, 160))
        self.frame_30.setMaximumSize(QSize(220, 180))
        self.frame_30.setSizeIncrement(QSize(0, 110))
        self.frame_30.setFrameShape(QFrame.Box)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_30)
        self.gridLayout_31.setSpacing(4)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(8, 4, 4, 4)
        self.frame_15 = QFrame(self.frame_30)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(16777215, 28))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_15)
        self.gridLayout_15.setSpacing(2)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 2, 2, 2)
        self.radioButton_harmonic_cursor = QRadioButton(self.frame_15)
        self.buttonGroup_cursor = QButtonGroup(Dialog)
        self.buttonGroup_cursor.setObjectName(u"buttonGroup_cursor")
        self.buttonGroup_cursor.addButton(self.radioButton_harmonic_cursor)
        self.radioButton_harmonic_cursor.setObjectName(u"radioButton_harmonic_cursor")
        self.radioButton_harmonic_cursor.setMinimumSize(QSize(75, 0))
        self.radioButton_harmonic_cursor.setMaximumSize(QSize(200, 28))
        self.radioButton_harmonic_cursor.setFont(font1)
        self.radioButton_harmonic_cursor.setChecked(False)

        self.gridLayout_15.addWidget(self.radioButton_harmonic_cursor, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.frame_15, 3, 0, 1, 1)

        self.frame_17 = QFrame(self.frame_30)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMaximumSize(QSize(16777215, 28))
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.gridLayout_17 = QGridLayout(self.frame_17)
        self.gridLayout_17.setSpacing(2)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(2, 2, 2, 2)
        self.radioButton_disable_cursors = QRadioButton(self.frame_17)
        self.buttonGroup_cursor.addButton(self.radioButton_disable_cursors)
        self.radioButton_disable_cursors.setObjectName(u"radioButton_disable_cursors")
        self.radioButton_disable_cursors.setMinimumSize(QSize(75, 0))
        self.radioButton_disable_cursors.setMaximumSize(QSize(200, 26))
        self.radioButton_disable_cursors.setFont(font1)
        self.radioButton_disable_cursors.setChecked(True)

        self.gridLayout_17.addWidget(self.radioButton_disable_cursors, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.frame_17, 1, 0, 1, 1)

        self.frame_16 = QFrame(self.frame_30)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMaximumSize(QSize(16777215, 28))
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_16)
        self.gridLayout_16.setSpacing(2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.radioButton_cross_cursor = QRadioButton(self.frame_16)
        self.buttonGroup_cursor.addButton(self.radioButton_cross_cursor)
        self.radioButton_cross_cursor.setObjectName(u"radioButton_cross_cursor")
        self.radioButton_cross_cursor.setMinimumSize(QSize(75, 0))
        self.radioButton_cross_cursor.setMaximumSize(QSize(200, 28))
        self.radioButton_cross_cursor.setFont(font1)
        self.radioButton_cross_cursor.setChecked(False)

        self.gridLayout_16.addWidget(self.radioButton_cross_cursor, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.frame_16, 2, 0, 1, 1)

        self.frame_legends = QFrame(self.frame_30)
        self.frame_legends.setObjectName(u"frame_legends")
        self.frame_legends.setMaximumSize(QSize(16777215, 28))
        self.frame_legends.setFrameShape(QFrame.NoFrame)
        self.frame_legends.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_legends)
        self.gridLayout_14.setSpacing(2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(2, 2, 2, 2)
        self.checkBox_cursor_legends = QCheckBox(self.frame_legends)
        self.checkBox_cursor_legends.setObjectName(u"checkBox_cursor_legends")
        self.checkBox_cursor_legends.setMinimumSize(QSize(75, 0))
        self.checkBox_cursor_legends.setMaximumSize(QSize(200, 26))
        self.checkBox_cursor_legends.setFont(font1)
        self.checkBox_cursor_legends.setChecked(False)

        self.gridLayout_14.addWidget(self.checkBox_cursor_legends, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.frame_legends, 0, 0, 1, 1)

        self.frame_vertical_lines = QFrame(self.frame_30)
        self.frame_vertical_lines.setObjectName(u"frame_vertical_lines")
        self.frame_vertical_lines.setMaximumSize(QSize(16777215, 28))
        self.frame_vertical_lines.setFrameShape(QFrame.NoFrame)
        self.frame_vertical_lines.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_vertical_lines)
        self.gridLayout_13.setSpacing(2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(2, 2, 2, 2)
        self.spinBox_vertical_lines = QSpinBox(self.frame_vertical_lines)
        self.spinBox_vertical_lines.setObjectName(u"spinBox_vertical_lines")
        self.spinBox_vertical_lines.setMinimumSize(QSize(0, 0))
        self.spinBox_vertical_lines.setMaximumSize(QSize(16777215, 26))
        self.spinBox_vertical_lines.setFont(font)
        self.spinBox_vertical_lines.setAlignment(Qt.AlignCenter)
        self.spinBox_vertical_lines.setMinimum(2)
        self.spinBox_vertical_lines.setMaximum(20)
        self.spinBox_vertical_lines.setValue(12)

        self.gridLayout_13.addWidget(self.spinBox_vertical_lines, 0, 1, 1, 1)

        self.label_2 = QLabel(self.frame_vertical_lines)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 26))
        self.label_2.setBaseSize(QSize(0, 0))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_2, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_vertical_lines)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_13.addWidget(self.frame_6, 0, 2, 1, 1)


        self.gridLayout_31.addWidget(self.frame_vertical_lines, 4, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_30, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_18, 2, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_11 = QFrame(self.frame_right)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 44))
        self.frame_11.setMaximumSize(QSize(16777215, 48))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_11)
        self.gridLayout_8.setSpacing(2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.pushButton_export_data = QPushButton(self.frame_11)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setEnabled(True)
        self.pushButton_export_data.setMinimumSize(QSize(120, 30))
        self.pushButton_export_data.setMaximumSize(QSize(120, 30))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_export_data.setFont(font3)
        self.pushButton_export_data.setStyleSheet(u"")
        self.pushButton_export_data.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_export_data, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_11, 2, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_right, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_lower, 1, 0, 1, 2)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_14 = QLabel(self.frame_3)
        self.label_14.setObjectName(u"label_14")
        font4 = QFont()
        font4.setPointSize(11)
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 2)

        QWidget.setTabOrder(self.comboBox_plot_type, self.checkBox_legends)
        QWidget.setTabOrder(self.checkBox_legends, self.checkBox_grid)
        QWidget.setTabOrder(self.checkBox_grid, self.comboBox_differentiate_data)
        QWidget.setTabOrder(self.comboBox_differentiate_data, self.radioButton_absolute)
        QWidget.setTabOrder(self.radioButton_absolute, self.radioButton_real)
        QWidget.setTabOrder(self.radioButton_real, self.radioButton_imaginary)
        QWidget.setTabOrder(self.radioButton_imaginary, self.radioButton_decibel_scale)
        QWidget.setTabOrder(self.radioButton_decibel_scale, self.checkBox_cursor_legends)
        QWidget.setTabOrder(self.checkBox_cursor_legends, self.radioButton_disable_cursors)
        QWidget.setTabOrder(self.radioButton_disable_cursors, self.radioButton_cross_cursor)
        QWidget.setTabOrder(self.radioButton_cross_cursor, self.radioButton_harmonic_cursor)
        QWidget.setTabOrder(self.radioButton_harmonic_cursor, self.spinBox_vertical_lines)
        QWidget.setTabOrder(self.spinBox_vertical_lines, self.pushButton_export_data)
        QWidget.setTabOrder(self.pushButton_export_data, self.pushButton_import_data)

        self.retranslateUi(Dialog)

        self.pushButton_export_data.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton_import_data.setText(QCoreApplication.translate("Dialog", u"  Import data  ", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Plot type", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u" log-y", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u" log-x", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u" lin-lin", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u" log-log", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Axes scales:", None))
        self.checkBox_legends.setText(QCoreApplication.translate("Dialog", u"Show legends", None))
        self.checkBox_grid.setText(QCoreApplication.translate("Dialog", u"Show grid", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Y-axis data", None))
#if QT_CONFIG(whatsthis)
        self.frame_4.setWhatsThis(QCoreApplication.translate("Dialog", u"Y-axis data type", None))
#endif // QT_CONFIG(whatsthis)
        self.radioButton_real.setText(QCoreApplication.translate("Dialog", u"Real part", None))
        self.radioButton_imaginary.setText(QCoreApplication.translate("Dialog", u"Imaginary part", None))
        self.radioButton_decibel_scale.setText(QCoreApplication.translate("Dialog", u"Decibel scale", None))
        self.radioButton_absolute.setText(QCoreApplication.translate("Dialog", u"Absolute", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Differentiate:", None))
        self.comboBox_differentiate_data.setItemText(0, QCoreApplication.translate("Dialog", u" none", None))
        self.comboBox_differentiate_data.setItemText(1, QCoreApplication.translate("Dialog", u" single", None))
        self.comboBox_differentiate_data.setItemText(2, QCoreApplication.translate("Dialog", u" double", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Cursor controls", None))
        self.radioButton_harmonic_cursor.setText(QCoreApplication.translate("Dialog", u"Enable harmonic cursor", None))
        self.radioButton_disable_cursors.setText(QCoreApplication.translate("Dialog", u"Disable cursors", None))
        self.radioButton_cross_cursor.setText(QCoreApplication.translate("Dialog", u"Enable cross cursor", None))
        self.checkBox_cursor_legends.setText(QCoreApplication.translate("Dialog", u"Show cursor legends", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Vertical lines: ", None))
        self.pushButton_export_data.setText(QCoreApplication.translate("Dialog", u"  Export data  ", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Frequency response plotter", None))
    # retranslateUi



class FrequencyResponsePlot_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - frame_left: QFrame
                                - (Layout): QGridLayout
                                        - widget_plot: QWidget
                            - frame_right: QFrame
                                - (Layout): QGridLayout
                                        - frame_22: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_import_data: QPushButton
                                        - frame_5: QFrame
                                            - (Layout): QGridLayout
                                                    - frame_14: QFrame
                                                        - (Layout): QGridLayout
                                                                - frame_13: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - label_9: QLabel
                                                                - frame_9: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - frame_12: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - comboBox_plot_type: QComboBox
                                                                                        - label: QLabel
                                                                                        - frame_19: QFrame
                                                                                        - frame_21: QFrame
                                                                            - frame_legends_2: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - checkBox_legends: QCheckBox
                                                                            - frame_legends_3: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - checkBox_grid: QCheckBox
                                                    - frame_7: QFrame
                                                        - (Layout): QGridLayout
                                                                - frame_8: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - label_8: QLabel
                                                                - frame_4: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - frame_20: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_real: QRadioButton
                                                                            - frame_25: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_imaginary: QRadioButton
                                                                            - frame_26: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_decibel_scale: QRadioButton
                                                                            - frame_10: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_absolute: QRadioButton
                                                                            - frame_27: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - frame_28: QFrame
                                                                                        - label_4: QLabel
                                                                                        - comboBox_differentiate_data: QComboBox
                                                    - frame_18: QFrame
                                                        - (Layout): QGridLayout
                                                                - frame_32: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - label_13: QLabel
                                                                - frame_30: QFrame
                                                                    - (Layout): QGridLayout
                                                                            - frame_15: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_harmonic_cursor: QRadioButton
                                                                            - frame_17: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_disable_cursors: QRadioButton
                                                                            - frame_16: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - radioButton_cross_cursor: QRadioButton
                                                                            - frame_legends: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - checkBox_cursor_legends: QCheckBox
                                                                            - frame_vertical_lines: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - spinBox_vertical_lines: QSpinBox
                                                                                        - label_2: QLabel
                                                                                        - frame_6: QFrame
                                        - frame_11: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_export_data: QPushButton
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_14: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
