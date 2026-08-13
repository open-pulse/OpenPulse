# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_fluid_composition.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 260)
        Dialog.setMinimumSize(QSize(500, 260))
        Dialog.setMaximumSize(QSize(500, 260))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(12, 4, 12, 4)
        self.pushButton_search = QPushButton(self.frame_3)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setMinimumSize(QSize(40, 30))
        self.pushButton_search.setMaximumSize(QSize(40, 30))
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_search.setFont(font1)
        icon = Icon(u":/icons/common/new_file.png")
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setIconSize(QSize(22, 22))
        self.pushButton_search.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_search, 0, 1, 1, 1)

        self.lineEdit_file_path = QLineEdit(self.frame_3)
        self.lineEdit_file_path.setObjectName(u"lineEdit_file_path")
        self.lineEdit_file_path.setMinimumSize(QSize(300, 30))
        self.lineEdit_file_path.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(9)
        self.lineEdit_file_path.setFont(font2)
        self.lineEdit_file_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_file_path, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 80))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.comboBox_sheet_names = QComboBox(self.frame_4)
        self.comboBox_sheet_names.setObjectName(u"comboBox_sheet_names")
        self.comboBox_sheet_names.setMinimumSize(QSize(200, 28))
        self.comboBox_sheet_names.setMaximumSize(QSize(240, 28))
        self.comboBox_sheet_names.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_sheet_names, 0, 2, 1, 1)

        self.label_sheet_name = QLabel(self.frame_4)
        self.label_sheet_name.setObjectName(u"label_sheet_name")
        self.label_sheet_name.setMinimumSize(QSize(0, 28))
        self.label_sheet_name.setMaximumSize(QSize(160, 28))
        self.label_sheet_name.setFont(font1)
        self.label_sheet_name.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_sheet_name, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_sheet_name_2 = QLabel(self.frame_4)
        self.label_sheet_name_2.setObjectName(u"label_sheet_name_2")
        self.label_sheet_name_2.setMinimumSize(QSize(0, 28))
        self.label_sheet_name_2.setMaximumSize(QSize(160, 28))
        self.label_sheet_name_2.setFont(font1)
        self.label_sheet_name_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_sheet_name_2, 1, 1, 1, 1)

        self.comboBox_state_properties = QComboBox(self.frame_4)
        self.comboBox_state_properties.setObjectName(u"comboBox_state_properties")
        self.comboBox_state_properties.setMinimumSize(QSize(200, 28))
        self.comboBox_state_properties.setMaximumSize(QSize(240, 28))
        self.comboBox_state_properties.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_state_properties, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_cancel = QPushButton(self.frame_2)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(80, 30))
        self.pushButton_cancel.setMaximumSize(QSize(80, 30))
        self.pushButton_cancel.setFont(font1)

        self.gridLayout_3.addWidget(self.pushButton_cancel, 0, 0, 1, 1)

        self.pushButton_load_composition = QPushButton(self.frame_2)
        self.pushButton_load_composition.setObjectName(u"pushButton_load_composition")
        self.pushButton_load_composition.setMinimumSize(QSize(80, 30))
        self.pushButton_load_composition.setMaximumSize(QSize(80, 30))
        self.pushButton_load_composition.setFont(font1)

        self.gridLayout_3.addWidget(self.pushButton_load_composition, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Load fluid composition from file", None))
        self.pushButton_search.setText("")
        self.label_sheet_name.setText(QCoreApplication.translate("Dialog", u"Fluid composition:", None))
        self.label_sheet_name_2.setText(QCoreApplication.translate("Dialog", u"State properties:", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_load_composition.setText(QCoreApplication.translate("Dialog", u"Load", None))
    # retranslateUi



class LoadFluidComposition_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_search: QPushButton
                            - lineEdit_file_path: QLineEdit
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_sheet_names: QComboBox
                                        - label_sheet_name: QLabel
                                        - label_sheet_name_2: QLabel
                                        - comboBox_state_properties: QComboBox
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_cancel: QPushButton
                            - pushButton_load_composition: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
