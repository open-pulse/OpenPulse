# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getGroupInformationAndRemoveInput.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 560)
        Dialog.setMinimumSize(QSize(400, 560))
        Dialog.setMaximumSize(QSize(400, 560))
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 400, 39))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(54, 2, 293, 33))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 38, 400, 522))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.frame_2.setLineWidth(1)
        self.lineEdit_selected_ID = QLineEdit(self.frame_2)
        self.lineEdit_selected_ID.setObjectName(u"lineEdit_selected_ID")
        self.lineEdit_selected_ID.setGeometry(QRect(144, 14, 200, 26))
        self.lineEdit_selected_ID.setMinimumSize(QSize(200, 0))
        self.lineEdit_selected_ID.setMaximumSize(QSize(200, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setItalic(False)
        self.lineEdit_selected_ID.setFont(font1)
        self.lineEdit_selected_ID.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_ID.setAlignment(Qt.AlignCenter)
        self.treeWidget_group_info = QTreeWidget(self.frame_2)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setGeometry(QRect(24, 54, 352, 412))
        self.treeWidget_group_info.setMinimumSize(QSize(352, 412))
        self.treeWidget_group_info.setMaximumSize(QSize(352, 412))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(True)
        self.treeWidget_group_info.setFont(font2)
        self.pushButton_close = QPushButton(self.frame_2)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setGeometry(QRect(206, 478, 100, 32))
        self.pushButton_close.setMinimumSize(QSize(100, 32))
        self.pushButton_close.setMaximumSize(QSize(100, 32))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setItalic(True)
        self.pushButton_close.setFont(font3)
        self.pushButton_remove = QPushButton(self.frame_2)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setGeometry(QRect(92, 478, 100, 32))
        self.pushButton_remove.setMinimumSize(QSize(100, 32))
        self.pushButton_remove.setMaximumSize(QSize(100, 32))
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"background-color: rgb(170, 255, 255);")
        self.lineEdit_id_labels = QLineEdit(self.frame_2)
        self.lineEdit_id_labels.setObjectName(u"lineEdit_id_labels")
        self.lineEdit_id_labels.setEnabled(False)
        self.lineEdit_id_labels.setGeometry(QRect(32, 14, 110, 26))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        self.lineEdit_id_labels.setPalette(palette)
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(12)
        font4.setBold(True)
        font4.setItalic(False)
        self.lineEdit_id_labels.setFont(font4)
        self.lineEdit_id_labels.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_id_labels.setAutoFillBackground(False)
        self.lineEdit_id_labels.setFrame(False)
        self.lineEdit_id_labels.setAlignment(Qt.AlignCenter)
        QWidget.setTabOrder(self.treeWidget_group_info, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_close)

        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.lineEdit_selected_ID.setText("")
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Elements", None));
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.lineEdit_id_labels.setText(QCoreApplication.translate("Dialog", u"Selected ID", None))
    # retranslateUi



class Getgroupinformationandremoveinput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - frame: QFrame
            - label: QLabel
        - frame_2: QFrame
            - lineEdit_selected_ID: QLineEdit
            - treeWidget_group_info: QTreeWidget
            - pushButton_close: QPushButton
            - pushButton_remove: QPushButton
            - lineEdit_id_labels: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
