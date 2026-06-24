# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getGroupInformationInput.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(650, 522)
        Dialog.setMinimumSize(QSize(650, 522))
        Dialog.setMaximumSize(QSize(650, 522))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lineEdit_selected_ID = QLineEdit(self.frame_3)
        self.lineEdit_selected_ID.setObjectName(u"lineEdit_selected_ID")
        self.lineEdit_selected_ID.setEnabled(True)
        self.lineEdit_selected_ID.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_ID.setMaximumSize(QSize(240, 28))
        font = QFont()
        font.setPointSize(10)
        self.lineEdit_selected_ID.setFont(font)
        self.lineEdit_selected_ID.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_ID.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_selected_ID.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_ID, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_3)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(100, 0))
        self.label_selected_id.setMaximumSize(QSize(100, 16777215))
        font1 = QFont()
        font1.setPointSize(11)
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.treeWidget_group_info = QTreeWidget(self.frame_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_group_info.setMaximumSize(QSize(600, 1000))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(True)
        self.treeWidget_group_info.setFont(font2)
        self.treeWidget_group_info.setTextElideMode(Qt.ElideRight)
        self.treeWidget_group_info.setIndentation(0)
        self.treeWidget_group_info.setUniformRowHeights(False)
        self.treeWidget_group_info.setAnimated(False)
        self.treeWidget_group_info.setAllColumnsShowFocus(False)
        self.treeWidget_group_info.setHeaderHidden(False)
        self.treeWidget_group_info.setColumnCount(2)
        self.treeWidget_group_info.header().setVisible(True)

        self.gridLayout_5.addWidget(self.treeWidget_group_info, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setPointSize(12)
        self.label.setFont(font3)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

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
        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remove.sizePolicy().hasHeightForWidth())
        self.pushButton_remove.setSizePolicy(sizePolicy)
        self.pushButton_remove.setMinimumSize(QSize(80, 30))
        self.pushButton_remove.setMaximumSize(QSize(80, 30))
        self.pushButton_remove.setSizeIncrement(QSize(0, 1))
        self.pushButton_remove.setStyleSheet(u"QPushButton{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240); font: 75 10pt \"MS Shell Dlg 2\"}\n"
"QPushButton:hover{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100); font: 75 10pt \"MS Shell Dlg 2\"}\n"
"QPushButton:pressed{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 3px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255); font: 75 10pt \"MS Shell Dlg 2\"}")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_close = QPushButton(self.frame_buttons)
        self.pushButton_close.setObjectName(u"pushButton_close")
        sizePolicy.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy)
        self.pushButton_close.setMinimumSize(QSize(80, 30))
        self.pushButton_close.setMaximumSize(QSize(80, 30))
        self.pushButton_close.setSizeIncrement(QSize(0, 1))
        self.pushButton_close.setStyleSheet(u"QPushButton{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240); font: 75 10pt \"MS Shell Dlg 2\"}\n"
"QPushButton:hover{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100); font: 75 10pt \"MS Shell Dlg 2\"}\n"
"QPushButton:pressed{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 3px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255); font: 75 10pt \"MS Shell Dlg 2\"}")
        self.pushButton_close.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_close, 0, 2, 1, 1)

        self.frame_5 = QFrame(self.frame_buttons)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_5, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.treeWidget_group_info, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_close)

        self.retranslateUi(Dialog)

        self.pushButton_remove.setDefault(True)
        self.pushButton_close.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.lineEdit_selected_ID.setText("")
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Elements", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi



class Getgroupinformationinput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_ID: QLineEdit
                                        - label_selected_id: QLabel
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_group_info: QTreeWidget
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_remove: QPushButton
                            - pushButton_close: QPushButton
                            - frame_5: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
