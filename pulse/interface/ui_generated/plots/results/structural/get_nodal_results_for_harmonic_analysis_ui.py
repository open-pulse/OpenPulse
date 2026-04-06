# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_nodal_results_for_harmonic_analysis.ui'
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
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 320)
        Form.setMaximumSize(QSize(16777215, 320))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(1, 4, 1, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(520, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
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


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 260))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_node_id = QLineEdit(self.frame_4)
        self.lineEdit_node_id.setObjectName(u"lineEdit_node_id")
        self.lineEdit_node_id.setMinimumSize(QSize(140, 26))
        self.lineEdit_node_id.setMaximumSize(QSize(140, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_node_id.setFont(font1)
        self.lineEdit_node_id.setStyleSheet(u"")
        self.lineEdit_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_node_id, 0, 2, 1, 1)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 26))
        self.label_10.setMaximumSize(QSize(16777215, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_10, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_12 = QFrame(self.frame_2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 40))
        self.frame_12.setMaximumSize(QSize(16777215, 40))
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_12)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(4)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_export_data = QPushButton(self.frame_12)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")
        self.pushButton_export_data.setMinimumSize(QSize(100, 28))
        self.pushButton_export_data.setMaximumSize(QSize(100, 28))
        self.pushButton_export_data.setFont(font2)
        self.pushButton_export_data.setStyleSheet(u"")
        self.pushButton_export_data.setFlat(False)

        self.gridLayout_9.addWidget(self.pushButton_export_data, 0, 0, 1, 1)

        self.pushButton_plot_data = QPushButton(self.frame_12)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 28))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 28))
        self.pushButton_plot_data.setFont(font2)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_plot_data, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_12, 2, 0, 1, 1)

        self.frame_20 = QFrame(self.frame_2)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 160))
        self.frame_20.setMaximumSize(QSize(16777215, 160))
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_20)
        self.gridLayout_20.setSpacing(4)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(10, 4, 10, 4)
        self.frame_19 = QFrame(self.frame_20)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(0, 32))
        self.frame_19.setMaximumSize(QSize(260, 32))
        self.frame_19.setFrameShape(QFrame.Box)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_19)
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(4, 0, 4, 0)
        self.label_3 = QLabel(self.frame_19)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(300, 32))
        self.label_3.setFont(font2)
        self.label_3.setFrameShape(QFrame.NoFrame)
        self.label_3.setFrameShadow(QFrame.Sunken)
        self.label_3.setTextFormat(Qt.AutoText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(False)
        self.label_3.setIndent(0)

        self.gridLayout_18.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_20.addWidget(self.frame_19, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_20)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 80))
        self.frame_5.setMaximumSize(QSize(260, 136))
        self.frame_5.setFrameShape(QFrame.Box)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_5)
        self.gridLayout_19.setSpacing(4)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(4, 4, 4, 4)
        self.radioButton_ry = QRadioButton(self.frame_5)
        self.radioButton_ry.setObjectName(u"radioButton_ry")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.radioButton_ry.sizePolicy().hasHeightForWidth())
        self.radioButton_ry.setSizePolicy(sizePolicy1)
        self.radioButton_ry.setMaximumSize(QSize(100, 16777215))
        self.radioButton_ry.setFont(font2)
        self.radioButton_ry.setChecked(False)

        self.gridLayout_19.addWidget(self.radioButton_ry, 1, 3, 1, 1)

        self.radioButton_rz = QRadioButton(self.frame_5)
        self.radioButton_rz.setObjectName(u"radioButton_rz")
        sizePolicy1.setHeightForWidth(self.radioButton_rz.sizePolicy().hasHeightForWidth())
        self.radioButton_rz.setSizePolicy(sizePolicy1)
        self.radioButton_rz.setMaximumSize(QSize(100, 16777215))
        self.radioButton_rz.setFont(font2)
        self.radioButton_rz.setChecked(False)

        self.gridLayout_19.addWidget(self.radioButton_rz, 2, 3, 1, 1)

        self.radioButton_uz = QRadioButton(self.frame_5)
        self.radioButton_uz.setObjectName(u"radioButton_uz")
        sizePolicy1.setHeightForWidth(self.radioButton_uz.sizePolicy().hasHeightForWidth())
        self.radioButton_uz.setSizePolicy(sizePolicy1)
        self.radioButton_uz.setMaximumSize(QSize(100, 16777215))
        self.radioButton_uz.setFont(font2)
        self.radioButton_uz.setChecked(False)

        self.gridLayout_19.addWidget(self.radioButton_uz, 2, 1, 1, 1)

        self.radioButton_ux = QRadioButton(self.frame_5)
        self.radioButton_ux.setObjectName(u"radioButton_ux")
        sizePolicy1.setHeightForWidth(self.radioButton_ux.sizePolicy().hasHeightForWidth())
        self.radioButton_ux.setSizePolicy(sizePolicy1)
        self.radioButton_ux.setMaximumSize(QSize(100, 16777215))
        self.radioButton_ux.setFont(font2)
        self.radioButton_ux.setChecked(True)

        self.gridLayout_19.addWidget(self.radioButton_ux, 0, 1, 1, 1)

        self.radioButton_uy = QRadioButton(self.frame_5)
        self.radioButton_uy.setObjectName(u"radioButton_uy")
        sizePolicy1.setHeightForWidth(self.radioButton_uy.sizePolicy().hasHeightForWidth())
        self.radioButton_uy.setSizePolicy(sizePolicy1)
        self.radioButton_uy.setMaximumSize(QSize(100, 16777215))
        self.radioButton_uy.setFont(font2)
        self.radioButton_uy.setChecked(False)

        self.gridLayout_19.addWidget(self.radioButton_uy, 1, 1, 1, 1)

        self.radioButton_rx = QRadioButton(self.frame_5)
        self.radioButton_rx.setObjectName(u"radioButton_rx")
        sizePolicy1.setHeightForWidth(self.radioButton_rx.sizePolicy().hasHeightForWidth())
        self.radioButton_rx.setSizePolicy(sizePolicy1)
        self.radioButton_rx.setMaximumSize(QSize(100, 16777215))
        self.radioButton_rx.setFont(font2)
        self.radioButton_rx.setChecked(False)

        self.gridLayout_19.addWidget(self.radioButton_rx, 0, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_9, 1, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_10, 1, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_11, 1, 4, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_12, 2, 0, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_13, 2, 2, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_19.addItem(self.horizontalSpacer_14, 2, 4, 1, 1)


        self.gridLayout_20.addWidget(self.frame_5, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_20, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_id, self.radioButton_ux)
        QWidget.setTabOrder(self.radioButton_ux, self.radioButton_rx)
        QWidget.setTabOrder(self.radioButton_rx, self.radioButton_uy)
        QWidget.setTabOrder(self.radioButton_uy, self.radioButton_ry)
        QWidget.setTabOrder(self.radioButton_ry, self.radioButton_uz)
        QWidget.setTabOrder(self.radioButton_uz, self.radioButton_rz)
        QWidget.setTabOrder(self.radioButton_rz, self.pushButton_export_data)
        QWidget.setTabOrder(self.pushButton_export_data, self.pushButton_plot_data)

        self.retranslateUi(Form)

        self.pushButton_plot_data.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot structural frequency response", None))
        self.lineEdit_node_id.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"Node ID:", None))
        self.pushButton_export_data.setText(QCoreApplication.translate("Form", u"Export data", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"  Select the DOF to get response  ", None))
        self.radioButton_ry.setText(QCoreApplication.translate("Form", u"Ry", None))
        self.radioButton_rz.setText(QCoreApplication.translate("Form", u"Rz", None))
        self.radioButton_uz.setText(QCoreApplication.translate("Form", u"Uz", None))
        self.radioButton_ux.setText(QCoreApplication.translate("Form", u"Ux", None))
        self.radioButton_uy.setText(QCoreApplication.translate("Form", u"Uy", None))
        self.radioButton_rx.setText(QCoreApplication.translate("Form", u"Rx", None))
    # retranslateUi



class GetNodalResultsForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_node_id: QLineEdit
                                        - label_10: QLabel
                            - frame_12: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_export_data: QPushButton
                                        - pushButton_plot_data: QPushButton
                            - frame_20: QFrame
                                - (Layout): QGridLayout
                                        - frame_19: QFrame
                                            - (Layout): QGridLayout
                                                    - label_3: QLabel
                                        - frame_5: QFrame
                                            - (Layout): QGridLayout
                                                    - radioButton_ry: QRadioButton
                                                    - radioButton_rz: QRadioButton
                                                    - radioButton_uz: QRadioButton
                                                    - radioButton_ux: QRadioButton
                                                    - radioButton_uy: QRadioButton
                                                    - radioButton_rx: QRadioButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
