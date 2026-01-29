# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pipe_option_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 479)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.set_section_button = QPushButton(Form)
        self.set_section_button.setObjectName(u"set_section_button")

        self.verticalLayout.addWidget(self.set_section_button)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.bending_radius_unity_label = QLabel(Form)
        self.bending_radius_unity_label.setObjectName(u"bending_radius_unity_label")

        self.gridLayout_5.addWidget(self.bending_radius_unity_label, 2, 3, 1, 1)

        self.bending_radius_label = QLabel(Form)
        self.bending_radius_label.setObjectName(u"bending_radius_label")

        self.gridLayout_5.addWidget(self.bending_radius_label, 2, 1, 1, 1)

        self.bending_radius_line_edit = QLineEdit(Form)
        self.bending_radius_line_edit.setObjectName(u"bending_radius_line_edit")

        self.gridLayout_5.addWidget(self.bending_radius_line_edit, 2, 2, 1, 1)

        self.bending_options_label = QLabel(Form)
        self.bending_options_label.setObjectName(u"bending_options_label")

        self.gridLayout_5.addWidget(self.bending_options_label, 1, 1, 1, 1)

        self.bending_options_combobox = QComboBox(Form)
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.setObjectName(u"bending_options_combobox")

        self.gridLayout_5.addWidget(self.bending_options_combobox, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.set_section_button, self.bending_options_combobox)
        QWidget.setTabOrder(self.bending_options_combobox, self.bending_radius_line_edit)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.set_section_button.setText(QCoreApplication.translate("Form", u"Set Section", None))
        self.set_section_button.setProperty(u"status", QCoreApplication.translate("Form", u"danger", None))
        self.bending_radius_unity_label.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.bending_radius_label.setText(QCoreApplication.translate("Form", u"Bending Radius", None))
        self.bending_options_label.setText(QCoreApplication.translate("Form", u"Bending Options", None))
        self.bending_options_combobox.setItemText(0, QCoreApplication.translate("Form", u"Long Radius", None))
        self.bending_options_combobox.setItemText(1, QCoreApplication.translate("Form", u"Short Radius", None))
        self.bending_options_combobox.setItemText(2, QCoreApplication.translate("Form", u"User-Defined", None))
        self.bending_options_combobox.setItemText(3, QCoreApplication.translate("Form", u"Disabled", None))

    # retranslateUi



class PipeOptionWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QVBoxLayout
                - set_section_button: QPushButton
                - (Layout): QGridLayout
                        - bending_radius_unity_label: QLabel
                        - bending_radius_label: QLabel
                        - bending_radius_line_edit: QLineEdit
                        - bending_options_label: QLabel
                        - bending_options_combobox: QComboBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
