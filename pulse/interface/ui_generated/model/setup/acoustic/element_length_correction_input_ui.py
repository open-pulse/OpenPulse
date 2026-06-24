# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'element_length_correction_input.ui'
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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 349)
        Dialog.setMinimumSize(QSize(400, 349))
        Dialog.setMaximumSize(QSize(400, 800))
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_9 = QGridLayout(self.frame)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.frame_selection = QFrame(self.frame_2)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setMinimumSize(QSize(0, 48))
        self.frame_selection.setFrameShape(QFrame.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_selection)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(8)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_element_id = QLineEdit(self.frame_selection)
        self.lineEdit_element_id.setObjectName(u"lineEdit_element_id")
        self.lineEdit_element_id.setMinimumSize(QSize(180, 26))
        self.lineEdit_element_id.setMaximumSize(QSize(180, 26))
        self.lineEdit_element_id.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_element_id.setFont(font1)
        self.lineEdit_element_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_element_id.setStyleSheet(u"")
        self.lineEdit_element_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_element_id, 0, 2, 1, 1)

        self.label_selection = QLabel(self.frame_selection)
        self.label_selection.setObjectName(u"label_selection")
        self.label_selection.setMaximumSize(QSize(16777215, 26))
        self.label_selection.setSizeIncrement(QSize(0, 26))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_selection.setFont(font2)
        self.label_selection.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selection, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 400))
        self.tabWidget_main.setFont(font2)
        self.tab_model = QWidget()
        self.tab_model.setObjectName(u"tab_model")
        self.gridLayout_6 = QGridLayout(self.tab_model)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_correction_type = QFrame(self.tab_model)
        self.frame_correction_type.setObjectName(u"frame_correction_type")
        self.frame_correction_type.setMinimumSize(QSize(0, 60))
        self.frame_correction_type.setMaximumSize(QSize(16777215, 16777215))
        self.frame_correction_type.setFrameShape(QFrame.NoFrame)
        self.frame_correction_type.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_correction_type)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_element_length_correction_type = QComboBox(self.frame_correction_type)
        self.comboBox_element_length_correction_type.addItem("")
        self.comboBox_element_length_correction_type.addItem("")
        self.comboBox_element_length_correction_type.addItem("")
        self.comboBox_element_length_correction_type.setObjectName(u"comboBox_element_length_correction_type")
        self.comboBox_element_length_correction_type.setMinimumSize(QSize(0, 26))
        self.comboBox_element_length_correction_type.setMaximumSize(QSize(16777215, 26))
        self.comboBox_element_length_correction_type.setFont(font1)

        self.gridLayout.addWidget(self.comboBox_element_length_correction_type, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_correction_type)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 26))
        self.label_2.setMaximumSize(QSize(16777215, 26))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_correction_type, 0, 0, 1, 1)

        self.frame_confirm = QFrame(self.tab_model)
        self.frame_confirm.setObjectName(u"frame_confirm")
        self.frame_confirm.setMinimumSize(QSize(0, 52))
        self.frame_confirm.setMaximumSize(QSize(16777215, 52))
        self.frame_confirm.setFrameShape(QFrame.NoFrame)
        self.frame_confirm.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_confirm)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_attribute = QPushButton(self.frame_confirm)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_confirm)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_confirm, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_model, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_8 = QGridLayout(self.tab_remove)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.treeWidget_elements_info = QTreeWidget(self.tab_remove)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_elements_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_elements_info.setObjectName(u"treeWidget_elements_info")
        self.treeWidget_elements_info.setMinimumSize(QSize(280, 0))
        self.treeWidget_elements_info.setMaximumSize(QSize(400, 150))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(9)
        self.treeWidget_elements_info.setFont(font4)
        self.treeWidget_elements_info.setIndentation(0)

        self.gridLayout_8.addWidget(self.treeWidget_elements_info, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.tab_remove)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_buttons)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_buttons, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_5.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_element_length_correction_type, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Element length correction setup", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Element length correction setup", None))
        self.lineEdit_element_id.setText("")
        self.label_selection.setText(QCoreApplication.translate("Dialog", u"Elements IDs:", None))
        self.comboBox_element_length_correction_type.setItemText(0, QCoreApplication.translate("Dialog", u" Expansion", None))
        self.comboBox_element_length_correction_type.setItemText(1, QCoreApplication.translate("Dialog", u" Side branch", None))
        self.comboBox_element_length_correction_type.setItemText(2, QCoreApplication.translate("Dialog", u" Loop", None))

#if QT_CONFIG(tooltip)
        self.comboBox_element_length_correction_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select the element length correction type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Correction type:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_model), QCoreApplication.translate("Dialog", u"Model", None))
        ___qtreewidgetitem = self.treeWidget_elements_info.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Elements", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Correction type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Group", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_elements_info.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:400; font-style:normal;\">Select a group to remove the length correction</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
    # retranslateUi



class ElementLengthCorrectionInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_selection: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_element_id: QLineEdit
                                        - label_selection: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_model: QWidget
                                    - (Layout): QGridLayout
                                            - frame_correction_type: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_element_length_correction_type: QComboBox
                                                        - label_2: QLabel
                                            - frame_confirm: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
                                - tab_remove: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_elements_info: QTreeWidget
                                            - frame_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_remove: QPushButton
                                                        - pushButton_reset: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
