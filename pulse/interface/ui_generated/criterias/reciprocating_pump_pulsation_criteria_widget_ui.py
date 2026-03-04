# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reciprocating_pump_pulsation_criteria_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(395, 340)
        Form.setMaximumSize(QSize(16777215, 340))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_14 = QFrame(self.frame_main)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_14)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 0)
        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 32))
        self.frame_15.setMaximumSize(QSize(16777215, 32))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_15)
        self.gridLayout_10.setSpacing(2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(2, 2, 2, 2)
        self.label_10 = QLabel(self.frame_15)
        self.label_10.setObjectName(u"label_10")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setWordWrap(False)

        self.gridLayout_10.addWidget(self.label_10, 0, 1, 1, 1)

        self.frame_16 = QFrame(self.frame_15)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)

        self.gridLayout_10.addWidget(self.frame_16, 0, 0, 1, 1)

        self.frame_17 = QFrame(self.frame_15)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Raised)

        self.gridLayout_10.addWidget(self.frame_17, 0, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_15, 1, 0, 1, 1)

        self.frame_18 = QFrame(self.frame_14)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 120))
        self.frame_18.setMaximumSize(QSize(16777215, 100))
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_18)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(4)
        self.gridLayout_11.setVerticalSpacing(2)
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.lineEdit_selected_id = QLineEdit(self.frame_18)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(120, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(120, 28))
        self.lineEdit_selected_id.setFont(font1)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_18)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(0, 28))
        self.label_selected_id.setMaximumSize(QSize(16777215, 28))
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.label_13 = QLabel(self.frame_18)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 28))
        self.label_13.setMaximumSize(QSize(16777215, 28))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_13, 2, 1, 1, 1)

        self.lineEdit_internal_diameter = QLineEdit(self.frame_18)
        self.lineEdit_internal_diameter.setObjectName(u"lineEdit_internal_diameter")
        self.lineEdit_internal_diameter.setMinimumSize(QSize(120, 28))
        self.lineEdit_internal_diameter.setMaximumSize(QSize(120, 28))
        self.lineEdit_internal_diameter.setFont(font1)
        self.lineEdit_internal_diameter.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_internal_diameter, 2, 2, 1, 1)

        self.frame_4 = QFrame(self.frame_18)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout_11.addWidget(self.frame_4, 0, 0, 1, 1)

        self.frame_24 = QFrame(self.frame_18)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Raised)

        self.gridLayout_11.addWidget(self.frame_24, 0, 3, 1, 1)

        self.label_11 = QLabel(self.frame_18)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_11, 1, 1, 1, 1)

        self.comboBox_line_ids = QComboBox(self.frame_18)
        self.comboBox_line_ids.setObjectName(u"comboBox_line_ids")
        self.comboBox_line_ids.setMinimumSize(QSize(120, 28))
        self.comboBox_line_ids.setMaximumSize(QSize(120, 28))
        self.comboBox_line_ids.setFont(font1)

        self.gridLayout_11.addWidget(self.comboBox_line_ids, 1, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_18, 2, 0, 1, 1)

        self.frame_21 = QFrame(self.frame_14)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMinimumSize(QSize(0, 48))
        self.frame_21.setMaximumSize(QSize(16777215, 48))
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_21)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.pushButton_plot_criteria = QPushButton(self.frame_21)
        self.pushButton_plot_criteria.setObjectName(u"pushButton_plot_criteria")
        self.pushButton_plot_criteria.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_criteria.setMaximumSize(QSize(120, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_plot_criteria.setFont(font2)
        self.pushButton_plot_criteria.setStyleSheet(u"")
        self.pushButton_plot_criteria.setFlat(False)

        self.gridLayout_12.addWidget(self.pushButton_plot_criteria, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame_21, 3, 0, 1, 1)

        self.label_second_criteria = QLabel(self.frame_14)
        self.label_second_criteria.setObjectName(u"label_second_criteria")
        self.label_second_criteria.setMinimumSize(QSize(0, 40))
        self.label_second_criteria.setMaximumSize(QSize(16777215, 52))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.label_second_criteria.setFont(font3)
        self.label_second_criteria.setFrameShape(QFrame.Box)
        self.label_second_criteria.setAlignment(Qt.AlignCenter)
        self.label_second_criteria.setWordWrap(True)
        self.label_second_criteria.setMargin(6)

        self.gridLayout_9.addWidget(self.label_second_criteria, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_14, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_id, self.lineEdit_internal_diameter)
        QWidget.setTabOrder(self.lineEdit_internal_diameter, self.pushButton_plot_criteria)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Recommended pulsation levels", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>P<span style=\" vertical-align:sub;\">1</span> = 3500 / (D<span style=\" vertical-align:sub;\">in</span> * F<span style=\" vertical-align:sub;\">n</span>)<span style=\" vertical-align:super;\">\u00bd</span></p></body></html>", None))
        self.label_selected_id.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Selected node ID:</p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>D<span style=\" vertical-align:sub;\">in</span> [mm]:</p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Line ID:</p></body></html>", None))
        self.pushButton_plot_criteria.setText(QCoreApplication.translate("Form", u"Plot criteria", None))
        self.label_second_criteria.setText(QCoreApplication.translate("Form", u"Allowable Pulsation Limits at and Beyond Line-side Connections of Pulsation Suppression Devices", None))
    # retranslateUi



class ReciprocatingPumpPulsationCriteriaWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_14: QFrame
                                - (Layout): QGridLayout
                                        - frame_15: QFrame
                                            - (Layout): QGridLayout
                                                    - label_10: QLabel
                                                    - frame_16: QFrame
                                                    - frame_17: QFrame
                                        - frame_18: QFrame
                                            - (Layout): QGridLayout
                                                    - lineEdit_selected_id: QLineEdit
                                                    - label_selected_id: QLabel
                                                    - label_13: QLabel
                                                    - lineEdit_internal_diameter: QLineEdit
                                                    - frame_4: QFrame
                                                    - frame_24: QFrame
                                                    - label_11: QLabel
                                                    - comboBox_line_ids: QComboBox
                                        - frame_21: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_plot_criteria: QPushButton
                                        - label_second_criteria: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
