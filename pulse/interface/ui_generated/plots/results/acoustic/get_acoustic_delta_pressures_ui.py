# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_acoustic_delta_pressures.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(340, 279)
        Form.setMinimumSize(QSize(0, 224))
        Form.setMaximumSize(QSize(16777215, 360))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(320, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_10 = QGridLayout(self.frame_title)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.frame_title)
        self.title.setObjectName(u"title")
        self.title.setMinimumSize(QSize(0, 30))
        self.title.setMaximumSize(QSize(410, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.title.setFont(font)
        self.title.setTextFormat(Qt.TextFormat.AutoText)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(320, 0))
        self.frame_main.setMaximumSize(QSize(480, 360))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_main)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(4)
        self.gridLayout_8.setVerticalSpacing(0)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_input = QFrame(self.frame_main)
        self.frame_input.setObjectName(u"frame_input")
        self.frame_input.setMinimumSize(QSize(0, 0))
        self.frame_input.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_input.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_input)
        self.gridLayout_5.setSpacing(8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 8, 2, 2)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.Output_NodeID = QLabel(self.frame_input)
        self.Output_NodeID.setObjectName(u"Output_NodeID")
        self.Output_NodeID.setMinimumSize(QSize(120, 28))
        self.Output_NodeID.setMaximumSize(QSize(140, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.Output_NodeID.setFont(font1)
        self.Output_NodeID.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.Output_NodeID, 1, 1, 1, 1)

        self.pushButton_flip_nodes = QPushButton(self.frame_input)
        self.pushButton_flip_nodes.setObjectName(u"pushButton_flip_nodes")
        self.pushButton_flip_nodes.setMinimumSize(QSize(40, 28))
        self.pushButton_flip_nodes.setMaximumSize(QSize(40, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_flip_nodes.setFont(font2)
        self.pushButton_flip_nodes.setStyleSheet(u"")
        icon = Icon(u":/icons/common/invert_icon.png")
        self.pushButton_flip_nodes.setIcon(icon)
        self.pushButton_flip_nodes.setIconSize(QSize(22, 22))
        self.pushButton_flip_nodes.setFlat(False)

        self.gridLayout_5.addWidget(self.pushButton_flip_nodes, 0, 3, 1, 1)

        self.Output_NodeID_3 = QLabel(self.frame_input)
        self.Output_NodeID_3.setObjectName(u"Output_NodeID_3")
        self.Output_NodeID_3.setMinimumSize(QSize(120, 28))
        self.Output_NodeID_3.setMaximumSize(QSize(140, 28))
        self.Output_NodeID_3.setFont(font1)
        self.Output_NodeID_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.Output_NodeID_3, 2, 1, 1, 1)

        self.comboBox_cutoff_frequency_options = QComboBox(self.frame_input)
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.addItem("")
        self.comboBox_cutoff_frequency_options.setObjectName(u"comboBox_cutoff_frequency_options")
        self.comboBox_cutoff_frequency_options.setMinimumSize(QSize(120, 28))
        self.comboBox_cutoff_frequency_options.setMaximumSize(QSize(120, 28))
        font3 = QFont()
        font3.setPointSize(10)
        self.comboBox_cutoff_frequency_options.setFont(font3)

        self.gridLayout_5.addWidget(self.comboBox_cutoff_frequency_options, 2, 2, 1, 1)

        self.lineEdit_output_node_id = QLineEdit(self.frame_input)
        self.lineEdit_output_node_id.setObjectName(u"lineEdit_output_node_id")
        self.lineEdit_output_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_output_node_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_output_node_id.setFont(font3)
        self.lineEdit_output_node_id.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_output_node_id.setStyleSheet(u"")
        self.lineEdit_output_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_output_node_id, 0, 2, 1, 1)

        self.lineEdit_input_node_id = QLineEdit(self.frame_input)
        self.lineEdit_input_node_id.setObjectName(u"lineEdit_input_node_id")
        self.lineEdit_input_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_input_node_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_input_node_id.setFont(font3)
        self.lineEdit_input_node_id.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_input_node_id.setStyleSheet(u"")
        self.lineEdit_input_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_input_node_id, 1, 2, 1, 1)

        self.Input_NodeID = QLabel(self.frame_input)
        self.Input_NodeID.setObjectName(u"Input_NodeID")
        self.Input_NodeID.setMinimumSize(QSize(120, 28))
        self.Input_NodeID.setMaximumSize(QSize(140, 28))
        self.Input_NodeID.setFont(font1)
        self.Input_NodeID.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.Input_NodeID, 0, 1, 1, 1)

        self.lineEdit_cutoff_frequency = QLineEdit(self.frame_input)
        self.lineEdit_cutoff_frequency.setObjectName(u"lineEdit_cutoff_frequency")
        self.lineEdit_cutoff_frequency.setEnabled(False)
        self.lineEdit_cutoff_frequency.setMinimumSize(QSize(120, 28))
        self.lineEdit_cutoff_frequency.setMaximumSize(QSize(120, 28))
        self.lineEdit_cutoff_frequency.setFont(font3)
        self.lineEdit_cutoff_frequency.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lineEdit_cutoff_frequency.setStyleSheet(u"")
        self.lineEdit_cutoff_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_cutoff_frequency, 3, 2, 1, 1)

        self.Output_NodeID_2 = QLabel(self.frame_input)
        self.Output_NodeID_2.setObjectName(u"Output_NodeID_2")
        self.Output_NodeID_2.setMinimumSize(QSize(120, 28))
        self.Output_NodeID_2.setMaximumSize(QSize(140, 28))
        self.Output_NodeID_2.setFont(font1)
        self.Output_NodeID_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.Output_NodeID_2, 3, 1, 1, 1)

        self.label_2 = QLabel(self.frame_input)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(40, 28))
        self.label_2.setMaximumSize(QSize(40, 28))

        self.gridLayout_5.addWidget(self.label_2, 3, 3, 1, 1)


        self.gridLayout_8.addWidget(self.frame_input, 0, 0, 1, 1)

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
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_plot_data.setFont(font4)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_12.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_buttons, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_output_node_id, self.pushButton_flip_nodes)
        QWidget.setTabOrder(self.pushButton_flip_nodes, self.pushButton_plot_data)

        self.retranslateUi(Form)

        self.pushButton_plot_data.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Plot delta pressures</p></body></html>", None))
        self.Output_NodeID.setText(QCoreApplication.translate("Form", u"Input Node ID:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setToolTip(QCoreApplication.translate("Form", u"Press to flip nodes.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setText("")
        self.Output_NodeID_3.setText(QCoreApplication.translate("Form", u"Cut-off frequency:", None))
        self.comboBox_cutoff_frequency_options.setItemText(0, QCoreApplication.translate("Form", u"Disabled", None))
        self.comboBox_cutoff_frequency_options.setItemText(1, QCoreApplication.translate("Form", u"User-defined", None))
        self.comboBox_cutoff_frequency_options.setItemText(2, QCoreApplication.translate("Form", u"Automatic", None))

        self.Input_NodeID.setText(QCoreApplication.translate("Form", u"Output Node ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_cutoff_frequency.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">f<span style=\" vertical-align:sub;\">c</span> = 1.8412 x C<span style=\" vertical-align:sub;\">o </span>/ (\u03c0 * D<span style=\" vertical-align:sub;\">in</span>), </p><p align=\"justify\">where C<span style=\" vertical-align:sub;\">0</span> is the fluid speed of sound in m/s, and D<span style=\" vertical-align:sub;\">in</span> is the pipe's internal diameter in m.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Output_NodeID_2.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:11pt;\">f</span><span style=\" font-size:11pt; vertical-align:sub;\">c</span> (circular section):</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
    # retranslateUi



class GetAcousticDeltaPressures_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_input: QFrame
                                - (Layout): QGridLayout
                                        - Output_NodeID: QLabel
                                        - pushButton_flip_nodes: QPushButton
                                        - Output_NodeID_3: QLabel
                                        - comboBox_cutoff_frequency_options: QComboBox
                                        - lineEdit_output_node_id: QLineEdit
                                        - lineEdit_input_node_id: QLineEdit
                                        - Input_NodeID: QLabel
                                        - lineEdit_cutoff_frequency: QLineEdit
                                        - Output_NodeID_2: QLabel
                                        - label_2: QLabel
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
