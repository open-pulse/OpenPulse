# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_fluid_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QScrollArea,
    QSizePolicy, QSpacerItem, QWidget)

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
        self.comboBox_attribution_type = QComboBox(self.frame_2)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 26))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 26))
        font = QFont()
        font.setPointSize(10)
        self.comboBox_attribution_type.setFont(font)

        self.gridLayout_4.addWidget(self.comboBox_attribution_type, 0, 3, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_4.setFont(font1)
        self.label_4.setTextFormat(Qt.AutoText)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.frame_2)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(True)
        self.lineEdit_selected_id.setMinimumSize(QSize(200, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(200, 26))
        self.lineEdit_selected_id.setFont(font)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_2, 0, 1, 1, 1)

        self.lineEdit_selected_fluid_name = QLineEdit(self.frame_2)
        self.lineEdit_selected_fluid_name.setObjectName(u"lineEdit_selected_fluid_name")
        self.lineEdit_selected_fluid_name.setEnabled(False)
        self.lineEdit_selected_fluid_name.setMinimumSize(QSize(200, 26))
        self.lineEdit_selected_fluid_name.setMaximumSize(QSize(200, 26))
        self.lineEdit_selected_fluid_name.setFont(font)
        self.lineEdit_selected_fluid_name.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_fluid_name.setStyleSheet(u"")
        self.lineEdit_selected_fluid_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_fluid_name, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


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

        QWidget.setTabOrder(self.comboBox_attribution_type, self.scrollArea_table_of_fluids)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All lines", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected lines", None))

        self.label_4.setText(QCoreApplication.translate("Dialog", u"Selected fluid:", None))
        self.lineEdit_selected_id.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.lineEdit_selected_fluid_name.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Set fluid configuration", None))
    # retranslateUi



class SetFluidInput_UI(QDialog, Ui_Dialog):
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
                                        - comboBox_attribution_type: QComboBox
                                        - label_4: QLabel
                                        - lineEdit_selected_id: QLineEdit
                                        - label_2: QLabel
                                        - lineEdit_selected_fluid_name: QLineEdit
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
