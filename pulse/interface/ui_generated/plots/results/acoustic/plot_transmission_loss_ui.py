# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_transmission_loss.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(373, 264)
        Form.setMinimumSize(QSize(0, 264))
        Form.setMaximumSize(QSize(16777215, 264))
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(320, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.Title = QLabel(self.frame_title)
        self.Title.setObjectName(u"Title")
        self.Title.setMinimumSize(QSize(300, 30))
        self.Title.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.Title.setFont(font)
        self.Title.setTextFormat(Qt.TextFormat.AutoText)
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.Title, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(320, 0))
        self.frame_main.setMaximumSize(QSize(480, 360))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_main)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(4)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_main)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)

        self.comboBox_processing_selector = QComboBox(self.frame_3)
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.addItem("")
        self.comboBox_processing_selector.setObjectName(u"comboBox_processing_selector")
        self.comboBox_processing_selector.setMinimumSize(QSize(0, 28))
        self.comboBox_processing_selector.setMaximumSize(QSize(180, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_processing_selector.setFont(font1)

        self.gridLayout_5.addWidget(self.comboBox_processing_selector, 0, 2, 1, 1)

        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label, 0, 1, 1, 1)

        self.pushButton_help = QPushButton(self.frame_3)
        self.pushButton_help.setObjectName(u"pushButton_help")
        self.pushButton_help.setMinimumSize(QSize(40, 28))
        self.pushButton_help.setMaximumSize(QSize(40, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_help.setFont(font2)
        self.pushButton_help.setStyleSheet(u"")
        self.pushButton_help.setIconSize(QSize(22, 22))
        self.pushButton_help.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_help, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.frame_main)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_buttons)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_data = QPushButton(self.frame_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 30))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_plot_data.setFont(font3)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_12.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons, 2, 0, 1, 1)

        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(8)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_output_node_id = QLineEdit(self.frame)
        self.lineEdit_output_node_id.setObjectName(u"lineEdit_output_node_id")
        self.lineEdit_output_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_output_node_id.setMaximumSize(QSize(80, 28))
        self.lineEdit_output_node_id.setFont(font1)
        self.lineEdit_output_node_id.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_output_node_id.setStyleSheet(u"")
        self.lineEdit_output_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_output_node_id, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.Output_NodeID = QLabel(self.frame)
        self.Output_NodeID.setObjectName(u"Output_NodeID")
        self.Output_NodeID.setMinimumSize(QSize(100, 28))
        self.Output_NodeID.setMaximumSize(QSize(140, 28))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.Output_NodeID.setFont(font4)
        self.Output_NodeID.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.Output_NodeID, 0, 1, 1, 1)

        self.Input_NodeID = QLabel(self.frame)
        self.Input_NodeID.setObjectName(u"Input_NodeID")
        self.Input_NodeID.setMinimumSize(QSize(100, 28))
        self.Input_NodeID.setMaximumSize(QSize(140, 28))
        self.Input_NodeID.setFont(font4)
        self.Input_NodeID.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.Input_NodeID, 1, 1, 1, 1)

        self.lineEdit_input_node_id = QLineEdit(self.frame)
        self.lineEdit_input_node_id.setObjectName(u"lineEdit_input_node_id")
        self.lineEdit_input_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_input_node_id.setMaximumSize(QSize(80, 28))
        self.lineEdit_input_node_id.setFont(font1)
        self.lineEdit_input_node_id.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_input_node_id.setStyleSheet(u"")
        self.lineEdit_input_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_input_node_id, 1, 2, 1, 1)

        self.pushButton_flip_nodes = QPushButton(self.frame)
        self.pushButton_flip_nodes.setObjectName(u"pushButton_flip_nodes")
        self.pushButton_flip_nodes.setMinimumSize(QSize(40, 28))
        self.pushButton_flip_nodes.setMaximumSize(QSize(40, 28))
        self.pushButton_flip_nodes.setFont(font2)
        self.pushButton_flip_nodes.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/invert_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_flip_nodes.setIcon(icon)
        self.pushButton_flip_nodes.setIconSize(QSize(22, 22))
        self.pushButton_flip_nodes.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButton_flip_nodes, 0, 3, 1, 1)


        self.gridLayout_7.addWidget(self.frame, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_processing_selector, self.pushButton_help)
        QWidget.setTabOrder(self.pushButton_help, self.lineEdit_output_node_id)
        QWidget.setTabOrder(self.lineEdit_output_node_id, self.pushButton_plot_data)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title.setText(QCoreApplication.translate("Form", u"Plot the transmission loss or noise reduction", None))
        self.comboBox_processing_selector.setItemText(0, QCoreApplication.translate("Form", u" Transmission loss", None))
        self.comboBox_processing_selector.setItemText(1, QCoreApplication.translate("Form", u" Noise reduction", None))

        self.label.setText(QCoreApplication.translate("Form", u"Process:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_help.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Help</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_help.setText(QCoreApplication.translate("Form", u"?", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.Output_NodeID.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Output Node ID:</p></body></html>", None))
        self.Input_NodeID.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Input Node ID:</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setToolTip(QCoreApplication.translate("Form", u"Press to flip nodes.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setText("")
    # retranslateUi



class PlotTransmissionLoss_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - Title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_processing_selector: QComboBox
                                        - label: QLabel
                                        - pushButton_help: QPushButton
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_output_node_id: QLineEdit
                                        - Output_NodeID: QLabel
                                        - Input_NodeID: QLabel
                                        - lineEdit_input_node_id: QLineEdit
                                        - pushButton_flip_nodes: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
