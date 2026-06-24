# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_fluid_composition.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 260)
        Dialog.setMinimumSize(QSize(460, 260))
        Dialog.setMaximumSize(QSize(460, 260))
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
        self.lineEdit_file_path = QLineEdit(self.frame_3)
        self.lineEdit_file_path.setObjectName(u"lineEdit_file_path")
        self.lineEdit_file_path.setMinimumSize(QSize(300, 30))
        self.lineEdit_file_path.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setPointSize(8)
        self.lineEdit_file_path.setFont(font1)
        self.lineEdit_file_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_file_path, 0, 0, 1, 1)

        self.pushButton_search = QPushButton(self.frame_3)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setMinimumSize(QSize(40, 30))
        self.pushButton_search.setMaximumSize(QSize(40, 30))
        font2 = QFont()
        font2.setPointSize(10)
        self.pushButton_search.setFont(font2)
        icon = QIcon()
        icon.addFile(u":/icons/common/document_search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setIconSize(QSize(22, 22))
        self.pushButton_search.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_search, 0, 1, 1, 1)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_sheet_name = QLabel(self.frame_4)
        self.label_sheet_name.setObjectName(u"label_sheet_name")
        self.label_sheet_name.setMinimumSize(QSize(0, 30))
        self.label_sheet_name.setMaximumSize(QSize(100, 30))
        self.label_sheet_name.setFont(font2)
        self.label_sheet_name.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_sheet_name, 0, 1, 1, 1)

        self.comboBox_sheet_names = QComboBox(self.frame_4)
        self.comboBox_sheet_names.setObjectName(u"comboBox_sheet_names")
        self.comboBox_sheet_names.setMinimumSize(QSize(160, 30))
        self.comboBox_sheet_names.setMaximumSize(QSize(200, 30))
        self.comboBox_sheet_names.setFont(font2)

        self.gridLayout_5.addWidget(self.comboBox_sheet_names, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 1, 0, 1, 2)


        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_exit = QPushButton(self.frame_2)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_confirm = QPushButton(self.frame_2)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 30))
        self.pushButton_confirm.setMaximumSize(QSize(100, 30))
        self.pushButton_confirm.setFont(font2)
        self.pushButton_confirm.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_confirm, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_file_path, self.pushButton_search)
        QWidget.setTabOrder(self.pushButton_search, self.comboBox_sheet_names)
        QWidget.setTabOrder(self.comboBox_sheet_names, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_confirm)

        self.retranslateUi(Dialog)

        self.pushButton_confirm.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Load fluid composition from file", None))
        self.pushButton_search.setText("")
        self.label_sheet_name.setText(QCoreApplication.translate("Dialog", u"Sheet name:", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
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
                            - lineEdit_file_path: QLineEdit
                            - pushButton_search: QPushButton
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_sheet_name: QLabel
                                        - comboBox_sheet_names: QComboBox
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
