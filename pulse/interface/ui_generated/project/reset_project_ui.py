# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reset_project.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(380, 300)
        Dialog.setMinimumSize(QSize(380, 300))
        Dialog.setMaximumSize(QSize(380, 300))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.reset_analysis_setup_checkbox = QCheckBox(self.frame_main)
        self.reset_analysis_setup_checkbox.setObjectName(u"reset_analysis_setup_checkbox")
        font1 = QFont()
        font1.setPointSize(10)
        self.reset_analysis_setup_checkbox.setFont(font1)
        self.reset_analysis_setup_checkbox.setChecked(True)

        self.gridLayout_3.addWidget(self.reset_analysis_setup_checkbox, 4, 1, 1, 1)

        self.reset_fluids_checkbox = QCheckBox(self.frame_main)
        self.reset_fluids_checkbox.setObjectName(u"reset_fluids_checkbox")
        self.reset_fluids_checkbox.setFont(font1)
        self.reset_fluids_checkbox.setChecked(True)

        self.gridLayout_3.addWidget(self.reset_fluids_checkbox, 0, 1, 1, 1)

        self.reset_materials_checkbox = QCheckBox(self.frame_main)
        self.reset_materials_checkbox.setObjectName(u"reset_materials_checkbox")
        self.reset_materials_checkbox.setFont(font1)
        self.reset_materials_checkbox.setChecked(True)

        self.gridLayout_3.addWidget(self.reset_materials_checkbox, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.reset_structural_model_checkbox = QCheckBox(self.frame_main)
        self.reset_structural_model_checkbox.setObjectName(u"reset_structural_model_checkbox")
        self.reset_structural_model_checkbox.setFont(font1)
        self.reset_structural_model_checkbox.setChecked(True)

        self.gridLayout_3.addWidget(self.reset_structural_model_checkbox, 3, 1, 1, 1)

        self.reset_acoustic_model_checkbox = QCheckBox(self.frame_main)
        self.reset_acoustic_model_checkbox.setObjectName(u"reset_acoustic_model_checkbox")
        self.reset_acoustic_model_checkbox.setFont(font1)
        self.reset_acoustic_model_checkbox.setChecked(True)

        self.gridLayout_3.addWidget(self.reset_acoustic_model_checkbox, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 52))
        self.frame_buttons.setMaximumSize(QSize(16777215, 52))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_buttons)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(10)
        self.gridLayout_6.setContentsMargins(10, 0, 10, 0)
        self.reset_project_button = QPushButton(self.frame_buttons)
        self.reset_project_button.setObjectName(u"reset_project_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_project_button.sizePolicy().hasHeightForWidth())
        self.reset_project_button.setSizePolicy(sizePolicy)
        self.reset_project_button.setMinimumSize(QSize(100, 30))
        self.reset_project_button.setMaximumSize(QSize(100, 30))
        self.reset_project_button.setSizeIncrement(QSize(0, 1))
        self.reset_project_button.setFont(font1)
        self.reset_project_button.setStyleSheet(u"")
        self.reset_project_button.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.reset_project_button, 0, 1, 1, 1)

        self.cancel_button = QPushButton(self.frame_buttons)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setMinimumSize(QSize(100, 30))
        self.cancel_button.setMaximumSize(QSize(100, 30))
        self.cancel_button.setSizeIncrement(QSize(0, 1))
        self.cancel_button.setFont(font1)
        self.cancel_button.setStyleSheet(u"")
        self.cancel_button.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.cancel_button, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        self.frame.raise_()
        self.frame_buttons.raise_()
        self.frame_main.raise_()
        QWidget.setTabOrder(self.reset_fluids_checkbox, self.reset_materials_checkbox)
        QWidget.setTabOrder(self.reset_materials_checkbox, self.reset_acoustic_model_checkbox)
        QWidget.setTabOrder(self.reset_acoustic_model_checkbox, self.reset_structural_model_checkbox)
        QWidget.setTabOrder(self.reset_structural_model_checkbox, self.reset_analysis_setup_checkbox)
        QWidget.setTabOrder(self.reset_analysis_setup_checkbox, self.cancel_button)
        QWidget.setTabOrder(self.cancel_button, self.reset_project_button)

        self.retranslateUi(Dialog)

        self.reset_project_button.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Reset Project Settings", None))
        self.reset_analysis_setup_checkbox.setText(QCoreApplication.translate("Dialog", u"Reset analysis setup", None))
        self.reset_fluids_checkbox.setText(QCoreApplication.translate("Dialog", u"Reset fluids", None))
        self.reset_materials_checkbox.setText(QCoreApplication.translate("Dialog", u"Reset materials", None))
        self.reset_structural_model_checkbox.setText(QCoreApplication.translate("Dialog", u"Reset structural model", None))
        self.reset_acoustic_model_checkbox.setText(QCoreApplication.translate("Dialog", u"Reset acoustic model", None))
        self.reset_project_button.setText(QCoreApplication.translate("Dialog", u"Reset project", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class ResetProject_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - reset_analysis_setup_checkbox: QCheckBox
                            - reset_fluids_checkbox: QCheckBox
                            - reset_materials_checkbox: QCheckBox
                            - reset_structural_model_checkbox: QCheckBox
                            - reset_acoustic_model_checkbox: QCheckBox
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - reset_project_button: QPushButton
                            - cancel_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
