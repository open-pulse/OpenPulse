# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_acoustic_frequency_response_function.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(364, 224)
        Form.setMinimumSize(QSize(0, 224))
        Form.setMaximumSize(QSize(16777215, 224))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(520, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(520, 460))
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_numerator = QFrame(self.frame_main)
        self.frame_numerator.setObjectName(u"frame_numerator")
        self.frame_numerator.setMinimumSize(QSize(0, 48))
        self.frame_numerator.setMaximumSize(QSize(16777215, 16777215))
        self.frame_numerator.setFrameShape(QFrame.NoFrame)
        self.frame_numerator.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_numerator)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_output_node_id = QLineEdit(self.frame_numerator)
        self.lineEdit_output_node_id.setObjectName(u"lineEdit_output_node_id")
        self.lineEdit_output_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_output_node_id.setMaximumSize(QSize(80, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_output_node_id.setFont(font1)
        self.lineEdit_output_node_id.setStyleSheet(u"")
        self.lineEdit_output_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_output_node_id, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_numerator)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 28))
        self.label_10.setMaximumSize(QSize(140, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 0, 5, 1, 1)

        self.lineEdit_input_node_id = QLineEdit(self.frame_numerator)
        self.lineEdit_input_node_id.setObjectName(u"lineEdit_input_node_id")
        self.lineEdit_input_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_input_node_id.setMaximumSize(QSize(80, 28))
        self.lineEdit_input_node_id.setFont(font1)
        self.lineEdit_input_node_id.setStyleSheet(u"")
        self.lineEdit_input_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_input_node_id, 1, 2, 1, 1)

        self.label_12 = QLabel(self.frame_numerator)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(100, 28))
        self.label_12.setMaximumSize(QSize(140, 28))
        self.label_12.setFont(font2)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_12, 1, 1, 1, 1)

        self.frame_3 = QFrame(self.frame_numerator)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(40, 28))
        self.frame_3.setMaximumSize(QSize(40, 28))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_3, 1, 3, 1, 1)

        self.pushButton_flip_nodes = QPushButton(self.frame_numerator)
        self.pushButton_flip_nodes.setObjectName(u"pushButton_flip_nodes")
        self.pushButton_flip_nodes.setMinimumSize(QSize(40, 28))
        self.pushButton_flip_nodes.setMaximumSize(QSize(40, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(True)
        font3.setItalic(False)
        self.pushButton_flip_nodes.setFont(font3)
        self.pushButton_flip_nodes.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/invert_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_flip_nodes.setIcon(icon)
        self.pushButton_flip_nodes.setIconSize(QSize(22, 22))
        self.pushButton_flip_nodes.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_flip_nodes, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_numerator, 1, 0, 1, 1)

        self.frame_buttons = QFrame(self.frame_main)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_buttons)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_data = QPushButton(self.frame_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 30))
        self.pushButton_plot_data.setFont(font2)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_12.addWidget(self.pushButton_plot_data, 0, 1, 1, 1)

        self.pushButton_export_data = QPushButton(self.frame_buttons)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(100, 30))
        self.pushButton_export_data.setMaximumSize(QSize(100, 30))
        self.pushButton_export_data.setFont(font2)
        self.pushButton_export_data.setStyleSheet(u"")
        self.pushButton_export_data.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_export_data, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_buttons, 2, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_output_node_id, self.pushButton_export_data)
        QWidget.setTabOrder(self.pushButton_export_data, self.pushButton_plot_data)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot acoustic frequency response function", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_output_node_id.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>It corresponds to the numerator node ID to get the acoustic response.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_output_node_id.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"Output Node ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_input_node_id.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>It corresponds to the denominator node ID to get the acoustic response.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_input_node_id.setText("")
        self.label_12.setText(QCoreApplication.translate("Form", u"Input Node ID:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setToolTip(QCoreApplication.translate("Form", u"Press to export the selected model result.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_flip_nodes.setText("")
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.pushButton_export_data.setText(QCoreApplication.translate("Form", u"Export data", None))
    # retranslateUi



class GetAcousticFrequencyResponseFunction_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_numerator: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_output_node_id: QLineEdit
                                        - label_10: QLabel
                                        - lineEdit_input_node_id: QLineEdit
                                        - label_12: QLabel
                                        - frame_3: QFrame
                                        - pushButton_flip_nodes: QPushButton
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                                        - pushButton_export_data: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
