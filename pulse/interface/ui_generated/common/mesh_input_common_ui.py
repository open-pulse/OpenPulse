# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesh_input_common.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModal)
        Form.resize(450, 550)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title_label = QLabel(self.frame_3)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.title_label)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.selected_lineedit = QLineEdit(self.frame)
        self.selected_lineedit.setObjectName(u"selected_lineedit")

        self.gridLayout.addWidget(self.selected_lineedit, 1, 2, 1, 1)

        self.attribute_to_label = QLabel(self.frame)
        self.attribute_to_label.setObjectName(u"attribute_to_label")

        self.gridLayout.addWidget(self.attribute_to_label, 0, 1, 1, 1)

        self.selected_label = QLabel(self.frame)
        self.selected_label.setObjectName(u"selected_label")

        self.gridLayout.addWidget(self.selected_label, 1, 1, 1, 1)

        self.attribute_to_combobox = QComboBox(self.frame)
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.addItem("")
        self.attribute_to_combobox.setObjectName(u"attribute_to_combobox")

        self.gridLayout.addWidget(self.attribute_to_combobox, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.template_frame = QFrame(Form)
        self.template_frame.setObjectName(u"template_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.template_frame.sizePolicy().hasHeightForWidth())
        self.template_frame.setSizePolicy(sizePolicy)
        self.template_frame.setFrameShape(QFrame.StyledPanel)
        self.template_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.template_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout.addWidget(self.template_frame)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cancel_button = QPushButton(Form)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout_2.addWidget(self.cancel_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.apply_button = QPushButton(Form)
        self.apply_button.setObjectName(u"apply_button")

        self.horizontalLayout_2.addWidget(self.apply_button)

        self.confirm_button = QPushButton(Form)
        self.confirm_button.setObjectName(u"confirm_button")

        self.horizontalLayout_2.addWidget(self.confirm_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.attribute_to_combobox, self.selected_lineedit)
        QWidget.setTabOrder(self.selected_lineedit, self.cancel_button)
        QWidget.setTabOrder(self.cancel_button, self.apply_button)
        QWidget.setTabOrder(self.apply_button, self.confirm_button)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title_label.setText(QCoreApplication.translate("Form", u"Window title", None))
        self.attribute_to_label.setText(QCoreApplication.translate("Form", u"Attribute to:", None))
        self.selected_label.setText(QCoreApplication.translate("Form", u"Selected lines:", None))
        self.attribute_to_combobox.setItemText(0, QCoreApplication.translate("Form", u"All nodes", None))
        self.attribute_to_combobox.setItemText(1, QCoreApplication.translate("Form", u"All lines", None))
        self.attribute_to_combobox.setItemText(2, QCoreApplication.translate("Form", u"All elements", None))
        self.attribute_to_combobox.setItemText(3, QCoreApplication.translate("Form", u"Selected nodes", None))
        self.attribute_to_combobox.setItemText(4, QCoreApplication.translate("Form", u"Selected lines", None))
        self.attribute_to_combobox.setItemText(5, QCoreApplication.translate("Form", u"Selected elements", None))

        self.cancel_button.setText(QCoreApplication.translate("Form", u"Exit", None))
        self.apply_button.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.confirm_button.setText(QCoreApplication.translate("Form", u"Confirm", None))
    # retranslateUi



class MeshInputCommon_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QVBoxLayout
                - frame_3: QFrame
                    - (Layout): QVBoxLayout
                            - title_label: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - selected_lineedit: QLineEdit
                            - attribute_to_label: QLabel
                            - selected_label: QLabel
                            - attribute_to_combobox: QComboBox
                - template_frame: QFrame
                    - (Layout): QVBoxLayout
                - (Layout): QHBoxLayout
                        - cancel_button: QPushButton
                        - apply_button: QPushButton
                        - confirm_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
