# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getExpansionJointInformationInput.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(702, 522)
        Dialog.setMinimumSize(QSize(702, 522))
        Dialog.setMaximumSize(QSize(702, 522))
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 702, 39))
        self.frame.setMinimumSize(QSize(702, 0))
        self.frame.setMaximumSize(QSize(702, 16777215))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(100, 4, 502, 33))
        self.title_label.setMinimumSize(QSize(502, 33))
        self.title_label.setMaximumSize(QSize(502, 33))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        self.title_label.setFont(font)
        self.title_label.setTextFormat(Qt.AutoText)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 38, 702, 484))
        self.frame_2.setMinimumSize(QSize(702, 0))
        self.frame_2.setMaximumSize(QSize(702, 16777215))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.pushButton_close = QPushButton(self.frame_2)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setGeometry(QRect(300, 440, 102, 32))
        self.pushButton_close.setMinimumSize(QSize(102, 32))
        self.pushButton_close.setMaximumSize(QSize(102, 32))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(True)
        self.pushButton_close.setFont(font1)
        self.treeWidget_group_info = QTreeWidget(self.frame_2)
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font2);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font2);
        self.treeWidget_group_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setGeometry(QRect(10, 16, 682, 412))
        self.treeWidget_group_info.setMinimumSize(QSize(682, 370))
        self.treeWidget_group_info.setMaximumSize(QSize(382, 430))
        self.treeWidget_group_info.setFont(font2)
        self.treeWidget_group_info.setTextElideMode(Qt.ElideRight)
        self.treeWidget_group_info.setIndentation(0)
        self.treeWidget_group_info.setUniformRowHeights(False)
        self.treeWidget_group_info.setAnimated(False)
        self.treeWidget_group_info.setAllColumnsShowFocus(False)
        self.treeWidget_group_info.setHeaderHidden(False)
        self.treeWidget_group_info.setColumnCount(2)
        self.treeWidget_group_info.header().setVisible(True)
        QWidget.setTabOrder(self.treeWidget_group_info, self.pushButton_close)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Information of selected expansion joint</p></body></html>", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Parameters [length, effective diameter, mass, axial locking \u03b5,  rods, kx, kyz, krx, kryz]", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Line ID", None));
    # retranslateUi



class Getexpansionjointinformationinput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - frame: QFrame
            - title_label: QLabel
        - frame_2: QFrame
            - pushButton_close: QPushButton
            - treeWidget_group_info: QTreeWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
