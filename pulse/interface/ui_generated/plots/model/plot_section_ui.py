# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_section.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(340, 260)
        Form.setMaximumSize(QSize(340, 260))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.selection_frame = QFrame(self.frame_2)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 80))
        self.selection_frame.setMaximumSize(QSize(16777215, 120))
        self.selection_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.selection_frame)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setHorizontalSpacing(6)
        self.gridLayout_26.setVerticalSpacing(2)
        self.gridLayout_26.setContentsMargins(2, 0, 2, 0)
        self.comboBox_selection = QComboBox(self.selection_frame)
        self.comboBox_selection.addItem("")
        self.comboBox_selection.addItem("")
        self.comboBox_selection.setObjectName(u"comboBox_selection")
        self.comboBox_selection.setMinimumSize(QSize(100, 28))
        self.comboBox_selection.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_selection.setFont(font1)

        self.gridLayout_26.addWidget(self.comboBox_selection, 0, 2, 1, 1)

        self.label_attribute = QLabel(self.selection_frame)
        self.label_attribute.setObjectName(u"label_attribute")
        self.label_attribute.setMinimumSize(QSize(100, 28))
        self.label_attribute.setMaximumSize(QSize(100, 28))
        self.label_attribute.setFont(font1)
        self.label_attribute.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_attribute, 0, 1, 1, 1)

        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(0, 28))
        self.label_selected_id.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_selected_id.setFont(font2)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_selected_id, 1, 1, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(100, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setKerning(False)
        self.lineEdit_selected_id.setFont(font3)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_26.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.selection_frame, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 42))
        self.frame_3.setMaximumSize(QSize(16777215, 42))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_section = QPushButton(self.frame_3)
        self.pushButton_plot_section.setObjectName(u"pushButton_plot_section")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_plot_section.sizePolicy().hasHeightForWidth())
        self.pushButton_plot_section.setSizePolicy(sizePolicy)
        self.pushButton_plot_section.setMinimumSize(QSize(100, 28))
        self.pushButton_plot_section.setMaximumSize(QSize(100, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.pushButton_plot_section.setFont(font4)
        self.pushButton_plot_section.setStyleSheet(u"")
        self.pushButton_plot_section.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_plot_section, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        sizePolicy.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy)
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font4)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)


        self.retranslateUi(Form)

        self.pushButton_plot_section.setDefault(False)
        self.pushButton_exit.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Cross-section plotter", None))
        self.comboBox_selection.setItemText(0, QCoreApplication.translate("Form", u"Lines", None))
        self.comboBox_selection.setItemText(1, QCoreApplication.translate("Form", u"Elements", None))

        self.label_attribute.setText(QCoreApplication.translate("Form", u"Selection type:", None))
        self.label_selected_id.setText(QCoreApplication.translate("Form", u"Selected ID:", None))
        self.pushButton_plot_section.setText(QCoreApplication.translate("Form", u"Plot section", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Form", u"Exit", None))
    # retranslateUi



class PlotSection_UI(QDialog, Ui_Form):
    """
    Component Hierarchy:
    - Form: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - selection_frame: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_selection: QComboBox
                                        - label_attribute: QLabel
                                        - label_selected_id: QLabel
                                        - lineEdit_selected_id: QLineEdit
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_plot_section: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
