# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getInformationRotationDecouplingInput.ui'
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
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(1)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(54, 2, 293, 33))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setKerning(True)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 38, 400, 522))
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.frame_2.setLineWidth(1)
        self.treeWidget_group_info = QTreeWidget(self.frame_2)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setGeometry(QRect(22, 114, 352, 357))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setKerning(True)
        self.treeWidget_group_info.setFont(font2)
        self.pushButton_close = QPushButton(self.frame_2)
        self.pushButton_close.setObjectName(u"pushButton_close")
        self.pushButton_close.setGeometry(QRect(206, 480, 100, 32))
        self.pushButton_close.setFont(font1)
        self.pushButton_close.setAutoDefault(False)
        self.pushButton_remove = QPushButton(self.frame_2)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setGeometry(QRect(92, 480, 100, 32))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setAutoDefault(False)
        self.lineEdit_node_IDs = QLineEdit(self.frame_2)
        self.lineEdit_node_IDs.setObjectName(u"lineEdit_node_IDs")
        self.lineEdit_node_IDs.setEnabled(False)
        self.lineEdit_node_IDs.setGeometry(QRect(190, 78, 150, 26))
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setKerning(True)
        self.lineEdit_node_IDs.setFont(font3)
        self.lineEdit_node_IDs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_node_IDs.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_node_IDs.setAlignment(Qt.AlignCenter)
        self.lineEdit_id_labels_decoupled_DOFs = QLineEdit(self.frame_2)
        self.lineEdit_id_labels_decoupled_DOFs.setObjectName(u"lineEdit_id_labels_decoupled_DOFs")
        self.lineEdit_id_labels_decoupled_DOFs.setEnabled(False)
        self.lineEdit_id_labels_decoupled_DOFs.setGeometry(QRect(52, 10, 133, 26))
        self.lineEdit_id_labels_decoupled_DOFs.setFont(font3)
        self.lineEdit_id_labels_decoupled_DOFs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_id_labels_decoupled_DOFs.setAutoFillBackground(False)
        self.lineEdit_id_labels_decoupled_DOFs.setFrame(False)
        self.lineEdit_id_labels_decoupled_DOFs.setAlignment(Qt.AlignCenter)
        self.lineEdit_id_labels_node_IDs = QLineEdit(self.frame_2)
        self.lineEdit_id_labels_node_IDs.setObjectName(u"lineEdit_id_labels_node_IDs")
        self.lineEdit_id_labels_node_IDs.setEnabled(False)
        self.lineEdit_id_labels_node_IDs.setGeometry(QRect(76, 78, 110, 26))
        self.lineEdit_id_labels_node_IDs.setFont(font3)
        self.lineEdit_id_labels_node_IDs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_id_labels_node_IDs.setAutoFillBackground(False)
        self.lineEdit_id_labels_node_IDs.setFrame(False)
        self.lineEdit_id_labels_node_IDs.setAlignment(Qt.AlignCenter)
        self.lineEdit_element_IDs = QLineEdit(self.frame_2)
        self.lineEdit_element_IDs.setObjectName(u"lineEdit_element_IDs")
        self.lineEdit_element_IDs.setEnabled(False)
        self.lineEdit_element_IDs.setGeometry(QRect(190, 44, 150, 26))
        self.lineEdit_element_IDs.setFont(font3)
        self.lineEdit_element_IDs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_element_IDs.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_element_IDs.setAlignment(Qt.AlignCenter)
        self.lineEdit_decoupled_DOFs = QLineEdit(self.frame_2)
        self.lineEdit_decoupled_DOFs.setObjectName(u"lineEdit_decoupled_DOFs")
        self.lineEdit_decoupled_DOFs.setEnabled(False)
        self.lineEdit_decoupled_DOFs.setGeometry(QRect(190, 10, 150, 26))
        self.lineEdit_decoupled_DOFs.setFont(font3)
        self.lineEdit_decoupled_DOFs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_decoupled_DOFs.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.lineEdit_decoupled_DOFs.setAlignment(Qt.AlignCenter)
        self.lineEdit_id_labels_element_IDs = QLineEdit(self.frame_2)
        self.lineEdit_id_labels_element_IDs.setObjectName(u"lineEdit_id_labels_element_IDs")
        self.lineEdit_id_labels_element_IDs.setEnabled(False)
        self.lineEdit_id_labels_element_IDs.setGeometry(QRect(76, 44, 110, 26))
        self.lineEdit_id_labels_element_IDs.setFont(font3)
        self.lineEdit_id_labels_element_IDs.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_id_labels_element_IDs.setAutoFillBackground(False)
        self.lineEdit_id_labels_element_IDs.setFrame(False)
        self.lineEdit_id_labels_element_IDs.setAlignment(Qt.AlignCenter)
        self.pushButton_close.raise_()
        self.pushButton_remove.raise_()
        self.lineEdit_node_IDs.raise_()
        self.lineEdit_id_labels_decoupled_DOFs.raise_()
        self.lineEdit_id_labels_node_IDs.raise_()
        self.lineEdit_element_IDs.raise_()
        self.lineEdit_decoupled_DOFs.raise_()
        self.lineEdit_id_labels_element_IDs.raise_()
        self.treeWidget_group_info.raise_()
        QWidget.setTabOrder(self.treeWidget_group_info, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_close)

        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(True)
        self.pushButton_remove.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Node ID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Element ID", None));
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.lineEdit_id_labels_decoupled_DOFs.setText(QCoreApplication.translate("Dialog", u"Decoupled DOFs:", None))
        self.lineEdit_id_labels_node_IDs.setText(QCoreApplication.translate("Dialog", u"Node IDs:", None))
        self.lineEdit_id_labels_element_IDs.setText(QCoreApplication.translate("Dialog", u"Element IDs:", None))
    # retranslateUi



class Getinformationrotationdecouplinginput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - frame: QFrame
            - label: QLabel
        - frame_2: QFrame
            - treeWidget_group_info: QTreeWidget
            - pushButton_close: QPushButton
            - pushButton_remove: QPushButton
            - lineEdit_node_IDs: QLineEdit
            - lineEdit_id_labels_decoupled_DOFs: QLineEdit
            - lineEdit_id_labels_node_IDs: QLineEdit
            - lineEdit_element_IDs: QLineEdit
            - lineEdit_decoupled_DOFs: QLineEdit
            - lineEdit_id_labels_element_IDs: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
