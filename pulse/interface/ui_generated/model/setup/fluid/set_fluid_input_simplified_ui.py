# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_fluid_input_simplified.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QScrollArea, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(780, 650)
        Dialog.setMinimumSize(QSize(600, 300))
        Dialog.setMaximumSize(QSize(1000, 720))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main_widget = QFrame(Dialog)
        self.frame_main_widget.setObjectName(u"frame_main_widget")
        self.frame_main_widget.setMinimumSize(QSize(0, 0))
        self.frame_main_widget.setMaximumSize(QSize(16777215, 16777215))
        self.frame_main_widget.setFrameShape(QFrame.Box)
        self.frame_main_widget.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main_widget)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_table_of_fluids = QScrollArea(self.frame_main_widget)
        self.scrollArea_table_of_fluids.setObjectName(u"scrollArea_table_of_fluids")
        self.scrollArea_table_of_fluids.setFrameShape(QFrame.NoFrame)
        self.scrollArea_table_of_fluids.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 764, 510))
        self.scrollArea_table_of_fluids.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea_table_of_fluids, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_main_widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(400, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 80))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(Qt.AutoText)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 1, 3, 1, 1)

        self.lineEdit_selected_fluid_name = QLineEdit(self.frame_2)
        self.lineEdit_selected_fluid_name.setObjectName(u"lineEdit_selected_fluid_name")
        self.lineEdit_selected_fluid_name.setEnabled(False)
        self.lineEdit_selected_fluid_name.setMinimumSize(QSize(180, 26))
        self.lineEdit_selected_fluid_name.setMaximumSize(QSize(180, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_selected_fluid_name.setFont(font1)
        self.lineEdit_selected_fluid_name.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_fluid_name.setStyleSheet(u"")
        self.lineEdit_selected_fluid_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_fluid_name, 1, 2, 1, 1)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setTextFormat(Qt.AutoText)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_5, 2, 1, 1, 1)

        self.lineEdit_fluid_identifier = QLineEdit(self.frame_2)
        self.lineEdit_fluid_identifier.setObjectName(u"lineEdit_fluid_identifier")
        self.lineEdit_fluid_identifier.setEnabled(False)
        self.lineEdit_fluid_identifier.setMinimumSize(QSize(180, 26))
        self.lineEdit_fluid_identifier.setMaximumSize(QSize(180, 26))
        self.lineEdit_fluid_identifier.setFont(font1)
        self.lineEdit_fluid_identifier.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_fluid_identifier.setStyleSheet(u"")
        self.lineEdit_fluid_identifier.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_fluid_identifier, 2, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main_widget, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(400, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(False)
        self.label.setFont(font2)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.lineEdit_selected_fluid_name.setText("")
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Fluid identifier:", None))
        self.lineEdit_fluid_identifier.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Set fluid configuration", None))
    # retranslateUi



class SetFluidInputSimplified_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main_widget: QFrame
                    - (Layout): QGridLayout
                            - scrollArea_table_of_fluids: QScrollArea
                                - scrollAreaWidgetContents: QWidget
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_4: QLabel
                                        - lineEdit_selected_fluid_name: QLineEdit
                                        - label_5: QLabel
                                        - lineEdit_fluid_identifier: QLineEdit
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
