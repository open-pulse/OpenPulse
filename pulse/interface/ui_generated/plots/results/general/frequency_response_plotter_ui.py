# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequency_response_plotter.ui'
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
    QFrame, QGridLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1050, 744)
        Dialog.setMinimumSize(QSize(900, 600))
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_content = QFrame(Dialog)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setMinimumSize(QSize(0, 200))
        self.frame_content.setFrameShape(QFrame.Shape.Box)
        self.frame_content.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_content)
        self.gridLayout_20.setSpacing(2)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(2, 2, 2, 2)
        self.frame_widget = QFrame(self.frame_content)
        self.frame_widget.setObjectName(u"frame_widget")
        self.frame_widget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_widget)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.widget_plot = QWidget(self.frame_widget)
        self.widget_plot.setObjectName(u"widget_plot")

        self.gridLayout_2.addWidget(self.widget_plot, 0, 1, 1, 1)


        self.gridLayout_20.addWidget(self.frame_widget, 0, 0, 1, 1)

        self.frame_configs = QFrame(self.frame_content)
        self.frame_configs.setObjectName(u"frame_configs")
        self.frame_configs.setMinimumSize(QSize(200, 0))
        self.frame_configs.setMaximumSize(QSize(290, 1677215))
        self.frame_configs.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_configs.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_configs)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.frame_configs)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 282, 620))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.frame_content_data = QFrame(self.scrollAreaWidgetContents)
        self.frame_content_data.setObjectName(u"frame_content_data")
        self.frame_content_data.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_content_data.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_content_data)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.frame_plot_type = QFrame(self.frame_content_data)
        self.frame_plot_type.setObjectName(u"frame_plot_type")
        self.frame_plot_type.setMaximumSize(QSize(16777215, 140))
        self.frame_plot_type.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_plot_type.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_plot_type)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setVerticalSpacing(2)
        self.gridLayout_18.setContentsMargins(4, 4, 4, 4)
        self.title_frame = QFrame(self.frame_plot_type)
        self.title_frame.setObjectName(u"title_frame")
        self.title_frame.setMinimumSize(QSize(0, 32))
        self.title_frame.setMaximumSize(QSize(16777215, 32))
        self.title_frame.setFrameShape(QFrame.Shape.Box)
        self.title_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.title_frame)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.label_9 = QLabel(self.title_frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(120, 20))
        self.label_9.setMaximumSize(QSize(165, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_9.setFont(font)
        self.label_9.setFrameShape(QFrame.Shape.NoFrame)
        self.label_9.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_9.setTextFormat(Qt.TextFormat.AutoText)
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_9.setWordWrap(False)
        self.label_9.setIndent(0)

        self.gridLayout_11.addWidget(self.label_9, 0, 0, 1, 1)


        self.gridLayout_18.addWidget(self.title_frame, 0, 0, 1, 1)

        self.frame_plot_type_content = QFrame(self.frame_plot_type)
        self.frame_plot_type_content.setObjectName(u"frame_plot_type_content")
        self.frame_plot_type_content.setMinimumSize(QSize(0, 0))
        self.frame_plot_type_content.setFrameShape(QFrame.Shape.Box)
        self.frame_plot_type_content.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_plot_type_content)
        self.gridLayout_12.setSpacing(4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.frame_12 = QFrame(self.frame_plot_type_content)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.frame_12.setFont(font1)
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_12)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(4)
        self.gridLayout_10.setVerticalSpacing(2)
        self.gridLayout_10.setContentsMargins(2, 0, 2, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 0, 0, 1, 1)

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
        self.comboBox_plot_type.setMinimumSize(QSize(80, 26))
        self.comboBox_plot_type.setMaximumSize(QSize(100, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.comboBox_plot_type.setFont(font2)
        self.comboBox_plot_type.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.comboBox_plot_type, 0, 2, 1, 1)

        self.label = QLabel(self.frame_12)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(16777215, 26))
        self.label.setFont(font1)

        self.gridLayout_10.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)


        self.gridLayout_12.addWidget(self.frame_12, 0, 0, 1, 1)

        self.frame_legends_2 = QFrame(self.frame_plot_type_content)
        self.frame_legends_2.setObjectName(u"frame_legends_2")
        self.frame_legends_2.setMaximumSize(QSize(16777215, 28))
        self.frame_legends_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_legends_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_legends_2)
        self.gridLayout_19.setSpacing(0)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.checkBox_legends = QCheckBox(self.frame_legends_2)
        self.checkBox_legends.setObjectName(u"checkBox_legends")
        self.checkBox_legends.setMinimumSize(QSize(75, 0))
        self.checkBox_legends.setMaximumSize(QSize(140, 26))
        self.checkBox_legends.setFont(font2)
        self.checkBox_legends.setChecked(True)

        self.gridLayout_19.addWidget(self.checkBox_legends, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_legends_2, 1, 0, 1, 1)

        self.frame_legends_3 = QFrame(self.frame_plot_type_content)
        self.frame_legends_3.setObjectName(u"frame_legends_3")
        self.frame_legends_3.setMaximumSize(QSize(16777215, 28))
        self.frame_legends_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_legends_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_22 = QGridLayout(self.frame_legends_3)
        self.gridLayout_22.setSpacing(0)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.checkBox_grid = QCheckBox(self.frame_legends_3)
        self.checkBox_grid.setObjectName(u"checkBox_grid")
        self.checkBox_grid.setMinimumSize(QSize(75, 0))
        self.checkBox_grid.setMaximumSize(QSize(140, 26))
        self.checkBox_grid.setFont(font2)
        self.checkBox_grid.setChecked(True)

        self.gridLayout_22.addWidget(self.checkBox_grid, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_legends_3, 2, 0, 1, 1)


        self.gridLayout_18.addWidget(self.frame_plot_type_content, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_plot_type, 0, 0, 1, 1)

        self.frame_y_axis_data = QFrame(self.frame_content_data)
        self.frame_y_axis_data.setObjectName(u"frame_y_axis_data")
        self.frame_y_axis_data.setMinimumSize(QSize(0, 140))
        self.frame_y_axis_data.setMaximumSize(QSize(16777215, 140))
        self.frame_y_axis_data.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_y_axis_data.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_y_axis_data)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.frame_y_axis_data)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 32))
        self.frame_8.setMaximumSize(QSize(16777215, 32))
        font3 = QFont()
        font3.setPointSize(10)
        self.frame_8.setFont(font3)
        self.frame_8.setFrameShape(QFrame.Shape.Box)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(120, 20))
        self.label_8.setMaximumSize(QSize(165, 32))
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QFrame.Shape.NoFrame)
        self.label_8.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_8.setTextFormat(Qt.TextFormat.AutoText)
        self.label_8.setScaledContents(False)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_8.setWordWrap(False)
        self.label_8.setIndent(0)

        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_y_axis_data)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setSizeIncrement(QSize(0, 0))
        self.frame_4.setFrameShape(QFrame.Shape.Box)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.comboBox_data_format = QComboBox(self.frame_4)
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.addItem("")
        self.comboBox_data_format.setObjectName(u"comboBox_data_format")
        self.comboBox_data_format.setMinimumSize(QSize(132, 26))
        self.comboBox_data_format.setMaximumSize(QSize(140, 26))
        self.comboBox_data_format.setFont(font3)

        self.gridLayout_4.addWidget(self.comboBox_data_format, 1, 2, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 0))
        self.label_5.setMaximumSize(QSize(16777215, 26))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 0))
        self.label_4.setMaximumSize(QSize(16777215, 26))
        self.label_4.setFont(font1)

        self.gridLayout_4.addWidget(self.label_4, 2, 1, 1, 1)

        self.comboBox_differentiate_data = QComboBox(self.frame_4)
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.addItem("")
        self.comboBox_differentiate_data.setObjectName(u"comboBox_differentiate_data")
        sizePolicy1.setHeightForWidth(self.comboBox_differentiate_data.sizePolicy().hasHeightForWidth())
        self.comboBox_differentiate_data.setSizePolicy(sizePolicy1)
        self.comboBox_differentiate_data.setMinimumSize(QSize(132, 26))
        self.comboBox_differentiate_data.setMaximumSize(QSize(140, 26))
        self.comboBox_differentiate_data.setFont(font2)
        self.comboBox_differentiate_data.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.comboBox_differentiate_data, 2, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 1, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_y_axis_data, 1, 0, 1, 1)

        self.frame_cursor_controls = QFrame(self.frame_content_data)
        self.frame_cursor_controls.setObjectName(u"frame_cursor_controls")
        self.frame_cursor_controls.setMinimumSize(QSize(0, 160))
        self.frame_cursor_controls.setMaximumSize(QSize(16777215, 160))
        self.frame_cursor_controls.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_cursor_controls.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_cursor_controls)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setVerticalSpacing(2)
        self.gridLayout_21.setContentsMargins(4, 4, 4, 0)
        self.frame_32 = QFrame(self.frame_cursor_controls)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMinimumSize(QSize(0, 32))
        self.frame_32.setMaximumSize(QSize(16777215, 32))
        self.frame_32.setSizeIncrement(QSize(0, 110))
        self.frame_32.setFrameShape(QFrame.Shape.Box)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_32 = QGridLayout(self.frame_32)
        self.gridLayout_32.setSpacing(0)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(4, 4, 4, 4)
        self.label_13 = QLabel(self.frame_32)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 20))
        self.label_13.setMaximumSize(QSize(16777215, 32))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(False)
        self.label_13.setFont(font4)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_32.addWidget(self.label_13, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_32, 0, 0, 1, 1)

        self.frame_cursor_controls_content = QFrame(self.frame_cursor_controls)
        self.frame_cursor_controls_content.setObjectName(u"frame_cursor_controls_content")
        self.frame_cursor_controls_content.setMinimumSize(QSize(0, 0))
        self.frame_cursor_controls_content.setMaximumSize(QSize(16777215, 140))
        self.frame_cursor_controls_content.setSizeIncrement(QSize(0, 110))
        self.frame_cursor_controls_content.setFrameShape(QFrame.Shape.Box)
        self.frame_cursor_controls_content.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_cursor_controls_content)
        self.gridLayout_31.setSpacing(4)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(8, 4, 4, 4)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_8, 2, 0, 1, 1)

        self.frame_legends = QFrame(self.frame_cursor_controls_content)
        self.frame_legends.setObjectName(u"frame_legends")
        self.frame_legends.setMaximumSize(QSize(16777215, 28))
        self.frame_legends.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_legends.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_legends)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.checkBox_cursor_legends = QCheckBox(self.frame_legends)
        self.checkBox_cursor_legends.setObjectName(u"checkBox_cursor_legends")
        self.checkBox_cursor_legends.setMinimumSize(QSize(75, 0))
        self.checkBox_cursor_legends.setMaximumSize(QSize(200, 26))
        self.checkBox_cursor_legends.setFont(font2)
        self.checkBox_cursor_legends.setChecked(True)

        self.gridLayout_14.addWidget(self.checkBox_cursor_legends, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.frame_legends, 1, 1, 1, 1)

        self.frame_vertical_lines = QFrame(self.frame_cursor_controls_content)
        self.frame_vertical_lines.setObjectName(u"frame_vertical_lines")
        self.frame_vertical_lines.setMaximumSize(QSize(16777215, 28))
        self.frame_vertical_lines.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_vertical_lines.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_vertical_lines)
        self.gridLayout_13.setSpacing(2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(2, 2, 2, 2)
        self.spinBox_vertical_lines = QSpinBox(self.frame_vertical_lines)
        self.spinBox_vertical_lines.setObjectName(u"spinBox_vertical_lines")
        self.spinBox_vertical_lines.setMinimumSize(QSize(60, 26))
        self.spinBox_vertical_lines.setMaximumSize(QSize(100, 26))
        self.spinBox_vertical_lines.setFont(font3)
        self.spinBox_vertical_lines.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_vertical_lines.setMinimum(2)
        self.spinBox_vertical_lines.setMaximum(20)
        self.spinBox_vertical_lines.setValue(10)

        self.gridLayout_13.addWidget(self.spinBox_vertical_lines, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_vertical_lines)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setBaseSize(QSize(0, 0))
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_2, 0, 0, 1, 2)


        self.gridLayout_31.addWidget(self.frame_vertical_lines, 3, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.comboBox_cursor_control = QComboBox(self.frame_cursor_controls_content)
        self.comboBox_cursor_control.addItem("")
        self.comboBox_cursor_control.addItem("")
        self.comboBox_cursor_control.addItem("")
        self.comboBox_cursor_control.setObjectName(u"comboBox_cursor_control")
        self.comboBox_cursor_control.setMinimumSize(QSize(0, 26))
        self.comboBox_cursor_control.setFont(font3)

        self.gridLayout_31.addWidget(self.comboBox_cursor_control, 2, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_9, 2, 2, 1, 1)


        self.gridLayout_21.addWidget(self.frame_cursor_controls_content, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_cursor_controls, 3, 0, 1, 1)

        self.frame_harmonic_lines = QFrame(self.frame_content_data)
        self.frame_harmonic_lines.setObjectName(u"frame_harmonic_lines")
        self.frame_harmonic_lines.setMaximumSize(QSize(16777215, 160))
        self.frame_harmonic_lines.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_harmonic_lines.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_30 = QGridLayout(self.frame_harmonic_lines)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setVerticalSpacing(2)
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.frame_hlines_title = QFrame(self.frame_harmonic_lines)
        self.frame_hlines_title.setObjectName(u"frame_hlines_title")
        self.frame_hlines_title.setMinimumSize(QSize(0, 32))
        self.frame_hlines_title.setMaximumSize(QSize(16777215, 32))
        self.frame_hlines_title.setFrameShape(QFrame.Shape.Box)
        self.frame_hlines_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_hlines_title)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label_title_3 = QLabel(self.frame_hlines_title)
        self.label_title_3.setObjectName(u"label_title_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_title_3.sizePolicy().hasHeightForWidth())
        self.label_title_3.setSizePolicy(sizePolicy2)
        font5 = QFont()
        font5.setPointSize(11)
        self.label_title_3.setFont(font5)
        self.label_title_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_title_3)


        self.gridLayout_30.addWidget(self.frame_hlines_title, 0, 0, 1, 1)

        self.frame_hlines_main = QFrame(self.frame_harmonic_lines)
        self.frame_hlines_main.setObjectName(u"frame_hlines_main")
        self.frame_hlines_main.setFrameShape(QFrame.Shape.Box)
        self.frame_hlines_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_hlines_main)
        self.gridLayout_23.setSpacing(4)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(4, 4, 4, 4)
        self.label_14 = QLabel(self.frame_hlines_main)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_14, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_4, 1, 5, 1, 1)

        self.comboBox_harmonic_lines_control = QComboBox(self.frame_hlines_main)
        self.comboBox_harmonic_lines_control.addItem("")
        self.comboBox_harmonic_lines_control.addItem("")
        self.comboBox_harmonic_lines_control.setObjectName(u"comboBox_harmonic_lines_control")
        self.comboBox_harmonic_lines_control.setMinimumSize(QSize(0, 26))
        self.comboBox_harmonic_lines_control.setFont(font3)

        self.gridLayout_23.addWidget(self.comboBox_harmonic_lines_control, 0, 2, 1, 1)

        self.lineEdit_harmonic_lines_1st_freq = QLineEdit(self.frame_hlines_main)
        self.lineEdit_harmonic_lines_1st_freq.setObjectName(u"lineEdit_harmonic_lines_1st_freq")
        self.lineEdit_harmonic_lines_1st_freq.setMinimumSize(QSize(0, 26))
        self.lineEdit_harmonic_lines_1st_freq.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_harmonic_lines_1st_freq.setFont(font3)
        self.lineEdit_harmonic_lines_1st_freq.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_23.addWidget(self.lineEdit_harmonic_lines_1st_freq, 1, 2, 1, 1)

        self.pushButton_display_hfrequencies = QPushButton(self.frame_hlines_main)
        self.pushButton_display_hfrequencies.setObjectName(u"pushButton_display_hfrequencies")
        self.pushButton_display_hfrequencies.setMinimumSize(QSize(30, 0))
        icon = QIcon()
        icon.addFile(u":/icons/common/visibility.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_display_hfrequencies.setIcon(icon)
        self.pushButton_display_hfrequencies.setIconSize(QSize(20, 20))
        self.pushButton_display_hfrequencies.setCheckable(False)
        self.pushButton_display_hfrequencies.setChecked(False)
        self.pushButton_display_hfrequencies.setAutoDefault(False)

        self.gridLayout_23.addWidget(self.pushButton_display_hfrequencies, 0, 3, 1, 1)

        self.spinBox_harmonic_lines_number = QSpinBox(self.frame_hlines_main)
        self.spinBox_harmonic_lines_number.setObjectName(u"spinBox_harmonic_lines_number")
        self.spinBox_harmonic_lines_number.setMinimumSize(QSize(0, 26))
        self.spinBox_harmonic_lines_number.setMaximumSize(QSize(16777215, 16777215))
        self.spinBox_harmonic_lines_number.setFont(font3)
        self.spinBox_harmonic_lines_number.setWrapping(False)
        self.spinBox_harmonic_lines_number.setFrame(True)
        self.spinBox_harmonic_lines_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_harmonic_lines_number.setMinimum(1)
        self.spinBox_harmonic_lines_number.setValue(5)

        self.gridLayout_23.addWidget(self.spinBox_harmonic_lines_number, 2, 2, 1, 1)

        self.label_10 = QLabel(self.frame_hlines_main)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font3)

        self.gridLayout_23.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_12 = QLabel(self.frame_hlines_main)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font3)

        self.gridLayout_23.addWidget(self.label_12, 1, 3, 1, 1)

        self.label_11 = QLabel(self.frame_hlines_main)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font3)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_11, 2, 1, 1, 1)


        self.gridLayout_30.addWidget(self.frame_hlines_main, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_harmonic_lines, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_content_data)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_9.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.frame_import_export = QFrame(self.frame_configs)
        self.frame_import_export.setObjectName(u"frame_import_export")
        self.frame_import_export.setMinimumSize(QSize(0, 44))
        self.frame_import_export.setMaximumSize(QSize(16777215, 16777215))
        self.frame_import_export.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_import_export.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_import_export)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.pushButton_export_data = QPushButton(self.frame_import_export)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setEnabled(True)
        self.pushButton_export_data.setMinimumSize(QSize(110, 32))
        self.pushButton_export_data.setMaximumSize(QSize(120, 32))
        font6 = QFont()
        font6.setFamilies([u"Ubuntu Sans"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.pushButton_export_data.setFont(font6)
        self.pushButton_export_data.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/common/save_as_2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_export_data.setIcon(icon1)
        self.pushButton_export_data.setIconSize(QSize(20, 20))
        self.pushButton_export_data.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_export_data, 0, 0, 1, 1)

        self.pushButton_import_data = QPushButton(self.frame_import_export)
        self.pushButton_import_data.setObjectName(u"pushButton_import_data")
        self.pushButton_import_data.setEnabled(True)
        self.pushButton_import_data.setMinimumSize(QSize(110, 32))
        self.pushButton_import_data.setMaximumSize(QSize(120, 32))
        self.pushButton_import_data.setFont(font6)
        self.pushButton_import_data.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/common/document_search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_import_data.setIcon(icon2)
        self.pushButton_import_data.setIconSize(QSize(20, 20))
        self.pushButton_import_data.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_import_data, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_import_export, 2, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_configs, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_content, 1, 0, 1, 2)

        self.big_title_frame = QFrame(Dialog)
        self.big_title_frame.setObjectName(u"big_title_frame")
        self.big_title_frame.setMinimumSize(QSize(0, 48))
        self.big_title_frame.setMaximumSize(QSize(16777215, 48))
        self.big_title_frame.setFrameShape(QFrame.Shape.Box)
        self.big_title_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.big_title_frame)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.big_title_frame)
        self.label_title.setObjectName(u"label_title")
        font7 = QFont()
        font7.setPointSize(12)
        font7.setBold(False)
        self.label_title.setFont(font7)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.big_title_frame, 0, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Plot type", None))
        self.comboBox_plot_type.setItemText(0, QCoreApplication.translate("Dialog", u"log-y", None))
        self.comboBox_plot_type.setItemText(1, QCoreApplication.translate("Dialog", u"log-x", None))
        self.comboBox_plot_type.setItemText(2, QCoreApplication.translate("Dialog", u"lin-lin", None))
        self.comboBox_plot_type.setItemText(3, QCoreApplication.translate("Dialog", u"log-log", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Axes scales:", None))
        self.checkBox_legends.setText(QCoreApplication.translate("Dialog", u"Show legends", None))
        self.checkBox_grid.setText(QCoreApplication.translate("Dialog", u"Show grid", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Y-axis data", None))
#if QT_CONFIG(whatsthis)
        self.frame_4.setWhatsThis(QCoreApplication.translate("Dialog", u"Y-axis data type", None))
#endif // QT_CONFIG(whatsthis)
        self.comboBox_data_format.setItemText(0, QCoreApplication.translate("Dialog", u"absolute values", None))
        self.comboBox_data_format.setItemText(1, QCoreApplication.translate("Dialog", u"real values", None))
        self.comboBox_data_format.setItemText(2, QCoreApplication.translate("Dialog", u"imaginary values", None))
        self.comboBox_data_format.setItemText(3, QCoreApplication.translate("Dialog", u"decibel scale", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Data format:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Differentiate:", None))
        self.comboBox_differentiate_data.setItemText(0, QCoreApplication.translate("Dialog", u"none", None))
        self.comboBox_differentiate_data.setItemText(1, QCoreApplication.translate("Dialog", u"single", None))
        self.comboBox_differentiate_data.setItemText(2, QCoreApplication.translate("Dialog", u"double", None))

        self.label_13.setText(QCoreApplication.translate("Dialog", u"Cursor controls", None))
        self.checkBox_cursor_legends.setText(QCoreApplication.translate("Dialog", u"Show cursor legends", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Vertical lines: ", None))
        self.comboBox_cursor_control.setItemText(0, QCoreApplication.translate("Dialog", u"disable cursors", None))
        self.comboBox_cursor_control.setItemText(1, QCoreApplication.translate("Dialog", u"enable cursor", None))
        self.comboBox_cursor_control.setItemText(2, QCoreApplication.translate("Dialog", u"enable h-cursor", None))

        self.label_title_3.setText(QCoreApplication.translate("Dialog", u"Harmonic lines plot", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"H-lines plot:", None))
        self.comboBox_harmonic_lines_control.setItemText(0, QCoreApplication.translate("Dialog", u"disabled", None))
        self.comboBox_harmonic_lines_control.setItemText(1, QCoreApplication.translate("Dialog", u"enabled", None))

        self.lineEdit_harmonic_lines_1st_freq.setText(QCoreApplication.translate("Dialog", u"250", None))
#if QT_CONFIG(tooltip)
        self.pushButton_display_hfrequencies.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Display harmonic line frequencies</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_display_hfrequencies.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Frequency (1x):", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Vertical lines:", None))
        self.pushButton_export_data.setText(QCoreApplication.translate("Dialog", u"Export data", None))
        self.pushButton_import_data.setText(QCoreApplication.translate("Dialog", u"Import data", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Frequency response plotter", None))
    # retranslateUi



class FrequencyResponsePlotter_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_content: QFrame
                    - (Layout): QGridLayout
                            - frame_widget: QFrame
                                - (Layout): QGridLayout
                                        - widget_plot: QWidget
                            - frame_configs: QFrame
                                - (Layout): QGridLayout
                                        - scrollArea: QScrollArea
                                            - scrollAreaWidgetContents: QWidget
                                                - (Layout): QVBoxLayout
                                                        - frame_content_data: QFrame
                                                            - (Layout): QGridLayout
                                                                    - frame_plot_type: QFrame
                                                                        - (Layout): QGridLayout
                                                                                - title_frame: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - label_9: QLabel
                                                                                - frame_plot_type_content: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - frame_12: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - comboBox_plot_type: QComboBox
                                                                                                        - label: QLabel
                                                                                            - frame_legends_2: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - checkBox_legends: QCheckBox
                                                                                            - frame_legends_3: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - checkBox_grid: QCheckBox
                                                                    - frame_y_axis_data: QFrame
                                                                        - (Layout): QGridLayout
                                                                                - frame_8: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - label_8: QLabel
                                                                                - frame_4: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - comboBox_data_format: QComboBox
                                                                                            - label_5: QLabel
                                                                                            - label_4: QLabel
                                                                                            - comboBox_differentiate_data: QComboBox
                                                                    - frame_cursor_controls: QFrame
                                                                        - (Layout): QGridLayout
                                                                                - frame_32: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - label_13: QLabel
                                                                                - frame_cursor_controls_content: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - frame_legends: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - checkBox_cursor_legends: QCheckBox
                                                                                            - frame_vertical_lines: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - spinBox_vertical_lines: QSpinBox
                                                                                                        - label_2: QLabel
                                                                                            - comboBox_cursor_control: QComboBox
                                                                    - frame_harmonic_lines: QFrame
                                                                        - (Layout): QGridLayout
                                                                                - frame_hlines_title: QFrame
                                                                                    - (Layout): QVBoxLayout
                                                                                            - label_title_3: QLabel
                                                                                - frame_hlines_main: QFrame
                                                                                    - (Layout): QGridLayout
                                                                                            - label_14: QLabel
                                                                                            - comboBox_harmonic_lines_control: QComboBox
                                                                                            - lineEdit_harmonic_lines_1st_freq: QLineEdit
                                                                                            - pushButton_display_hfrequencies: QPushButton
                                                                                            - spinBox_harmonic_lines_number: QSpinBox
                                                                                            - label_10: QLabel
                                                                                            - label_12: QLabel
                                                                                            - label_11: QLabel
                                        - frame_import_export: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_export_data: QPushButton
                                                    - pushButton_import_data: QPushButton
                - big_title_frame: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
