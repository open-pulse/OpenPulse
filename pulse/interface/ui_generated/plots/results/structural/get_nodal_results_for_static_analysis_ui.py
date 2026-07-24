# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_nodal_results_for_static_analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(358, 366)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 2, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(300, 32))
        self.label.setMaximumSize(QSize(300, 32))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 272))
        self.frame_2.setMaximumSize(QSize(16777215, 320))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_responses = QFrame(self.frame_2)
        self.frame_responses.setObjectName(u"frame_responses")
        self.frame_responses.setMinimumSize(QSize(0, 260))
        self.frame_responses.setMaximumSize(QSize(16777215, 320))
        self.frame_responses.setFrameShape(QFrame.NoFrame)
        self.frame_responses.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_responses)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.lineEdit_response_ux = QLineEdit(self.frame_responses)
        self.lineEdit_response_ux.setObjectName(u"lineEdit_response_ux")
        self.lineEdit_response_ux.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_ux.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_ux.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_ux.setBaseSize(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_response_ux.setFont(font1)
        self.lineEdit_response_ux.setStyleSheet(u"")
        self.lineEdit_response_ux.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_ux, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame_responses)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(72, 28))
        self.label_2.setMaximumSize(QSize(72, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)

        self.frame = QFrame(self.frame_responses)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(60, 28))
        self.frame.setMaximumSize(QSize(60, 28))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(52, 26))
        self.pushButton_reset.setMaximumSize(QSize(52, 26))
        font3 = QFont()
        font3.setPointSize(9)
        self.pushButton_reset.setFont(font3)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 3, 1, 1)

        self.label_8 = QLabel(self.frame_responses)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(48, 28))
        self.label_8.setMaximumSize(QSize(48, 28))
        self.label_8.setFont(font2)
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 1, 3, 1, 1)

        self.lineEdit_node_id = QLineEdit(self.frame_responses)
        self.lineEdit_node_id.setObjectName(u"lineEdit_node_id")
        self.lineEdit_node_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_node_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_node_id.setSizeIncrement(QSize(0, 0))
        self.lineEdit_node_id.setBaseSize(QSize(0, 0))
        self.lineEdit_node_id.setFont(font2)
        self.lineEdit_node_id.setStyleSheet(u"")
        self.lineEdit_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_node_id, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_responses)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(72, 28))
        self.label_3.setMaximumSize(QSize(72, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_9 = QLabel(self.frame_responses)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(48, 28))
        self.label_9.setMaximumSize(QSize(48, 28))
        self.label_9.setFont(font2)
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 2, 3, 1, 1)

        self.label_4 = QLabel(self.frame_responses)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(72, 28))
        self.label_4.setMaximumSize(QSize(72, 28))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_4, 3, 1, 1, 1)

        self.label_5 = QLabel(self.frame_responses)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(72, 28))
        self.label_5.setMaximumSize(QSize(72, 28))
        self.label_5.setFont(font2)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 4, 1, 1, 1)

        self.label_10 = QLabel(self.frame_responses)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(48, 28))
        self.label_10.setMaximumSize(QSize(48, 28))
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 3, 3, 1, 1)

        self.lineEdit_response_rz = QLineEdit(self.frame_responses)
        self.lineEdit_response_rz.setObjectName(u"lineEdit_response_rz")
        self.lineEdit_response_rz.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_rz.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_rz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_rz.setBaseSize(QSize(0, 0))
        self.lineEdit_response_rz.setFont(font1)
        self.lineEdit_response_rz.setStyleSheet(u"")
        self.lineEdit_response_rz.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_rz, 6, 2, 1, 1)

        self.lineEdit_response_uy = QLineEdit(self.frame_responses)
        self.lineEdit_response_uy.setObjectName(u"lineEdit_response_uy")
        self.lineEdit_response_uy.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_uy.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_uy.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_uy.setBaseSize(QSize(0, 0))
        self.lineEdit_response_uy.setFont(font1)
        self.lineEdit_response_uy.setStyleSheet(u"")
        self.lineEdit_response_uy.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_uy, 2, 2, 1, 1)

        self.label_14 = QLabel(self.frame_responses)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(72, 28))
        self.label_14.setMaximumSize(QSize(72, 28))
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 0, 1, 1, 1)

        self.lineEdit_response_uz = QLineEdit(self.frame_responses)
        self.lineEdit_response_uz.setObjectName(u"lineEdit_response_uz")
        self.lineEdit_response_uz.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_uz.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_uz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_uz.setBaseSize(QSize(0, 0))
        self.lineEdit_response_uz.setFont(font1)
        self.lineEdit_response_uz.setStyleSheet(u"")
        self.lineEdit_response_uz.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_uz, 3, 2, 1, 1)

        self.label_6 = QLabel(self.frame_responses)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(72, 28))
        self.label_6.setMaximumSize(QSize(72, 28))
        self.label_6.setFont(font2)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 5, 1, 1, 1)

        self.lineEdit_response_rx = QLineEdit(self.frame_responses)
        self.lineEdit_response_rx.setObjectName(u"lineEdit_response_rx")
        self.lineEdit_response_rx.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_rx.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_rx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_rx.setBaseSize(QSize(0, 0))
        self.lineEdit_response_rx.setFont(font1)
        self.lineEdit_response_rx.setStyleSheet(u"")
        self.lineEdit_response_rx.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_rx, 4, 2, 1, 1)

        self.label_13 = QLabel(self.frame_responses)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(48, 28))
        self.label_13.setMaximumSize(QSize(48, 28))
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 6, 3, 1, 1)

        self.label_12 = QLabel(self.frame_responses)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(48, 28))
        self.label_12.setMaximumSize(QSize(48, 28))
        self.label_12.setFont(font2)
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_12, 5, 3, 1, 1)

        self.label_7 = QLabel(self.frame_responses)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(72, 28))
        self.label_7.setMaximumSize(QSize(72, 28))
        self.label_7.setFont(font2)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 6, 1, 1, 1)

        self.label_11 = QLabel(self.frame_responses)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(48, 28))
        self.label_11.setMaximumSize(QSize(48, 28))
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 4, 3, 1, 1)

        self.lineEdit_response_ry = QLineEdit(self.frame_responses)
        self.lineEdit_response_ry.setObjectName(u"lineEdit_response_ry")
        self.lineEdit_response_ry.setMinimumSize(QSize(120, 28))
        self.lineEdit_response_ry.setMaximumSize(QSize(120, 28))
        self.lineEdit_response_ry.setSizeIncrement(QSize(0, 0))
        self.lineEdit_response_ry.setBaseSize(QSize(0, 0))
        self.lineEdit_response_ry.setFont(font1)
        self.lineEdit_response_ry.setStyleSheet(u"")
        self.lineEdit_response_ry.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_response_ry, 5, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_responses, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_id, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.lineEdit_response_ux)
        QWidget.setTabOrder(self.lineEdit_response_ux, self.lineEdit_response_uy)
        QWidget.setTabOrder(self.lineEdit_response_uy, self.lineEdit_response_uz)
        QWidget.setTabOrder(self.lineEdit_response_uz, self.lineEdit_response_rx)
        QWidget.setTabOrder(self.lineEdit_response_rx, self.lineEdit_response_ry)
        QWidget.setTabOrder(self.lineEdit_response_ry, self.lineEdit_response_rz)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Structural nodal response", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Ux: ", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label_8.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Uy: ", None))
        self.label_9.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Uz: ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Rx: ", None))
        self.label_10.setText(QCoreApplication.translate("Form", u" [m]", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Node ID: ", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Ry: ", None))
        self.label_13.setText(QCoreApplication.translate("Form", u" [rad]", None))
        self.label_12.setText(QCoreApplication.translate("Form", u" [rad]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Rz: ", None))
        self.label_11.setText(QCoreApplication.translate("Form", u" [rad]", None))
    # retranslateUi



class GetNodalResultsForStaticAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_responses: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_response_ux: QLineEdit
                                        - label_2: QLabel
                                        - frame: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_reset: QPushButton
                                        - label_8: QLabel
                                        - lineEdit_node_id: QLineEdit
                                        - label_3: QLabel
                                        - label_9: QLabel
                                        - label_4: QLabel
                                        - label_5: QLabel
                                        - label_10: QLabel
                                        - lineEdit_response_rz: QLineEdit
                                        - lineEdit_response_uy: QLineEdit
                                        - label_14: QLabel
                                        - lineEdit_response_uz: QLineEdit
                                        - label_6: QLabel
                                        - lineEdit_response_rx: QLineEdit
                                        - label_13: QLabel
                                        - label_12: QLabel
                                        - label_7: QLabel
                                        - label_11: QLabel
                                        - lineEdit_response_ry: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
