# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_acoustic_frequency_response.ui'
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
        Form.resize(338, 172)
        Form.setMinimumSize(QSize(0, 172))
        Form.setMaximumSize(QSize(16777215, 172))
        self.gridLayout_8 = QGridLayout(Form)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(520, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_7 = QGridLayout(self.frame_title)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
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
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(520, 460))
        font1 = QFont()
        font1.setPointSize(11)
        self.frame_main.setFont(font1)
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(4)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_numerator_2 = QFrame(self.frame_main)
        self.frame_numerator_2.setObjectName(u"frame_numerator_2")
        self.frame_numerator_2.setMinimumSize(QSize(0, 48))
        self.frame_numerator_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_numerator_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_numerator_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_numerator_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_11 = QLabel(self.frame_numerator_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(70, 28))
        self.label_11.setMaximumSize(QSize(70, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 0, 1, 1, 1)

        self.lineEdit_node_id = QLineEdit(self.frame_numerator_2)
        self.lineEdit_node_id.setObjectName(u"lineEdit_node_id")
        self.lineEdit_node_id.setMinimumSize(QSize(160, 28))
        self.lineEdit_node_id.setMaximumSize(QSize(160, 28))
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_node_id.setFont(font3)
        self.lineEdit_node_id.setStyleSheet(u"")
        self.lineEdit_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_node_id, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_numerator_2, 0, 1, 1, 1)

        self.frame_buttons = QFrame(self.frame_main)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 16777215))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_data = QPushButton(self.frame_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 30))
        self.pushButton_plot_data.setFont(font2)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_buttons, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_id, self.pushButton_plot_data)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot acoustic frequency response", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Node IDs:", None))
        self.lineEdit_node_id.setText("")
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
    # retranslateUi



class GetAcousticFrequencyResponse_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_numerator_2: QFrame
                                - (Layout): QGridLayout
                                        - label_11: QLabel
                                        - lineEdit_node_id: QLineEdit
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
