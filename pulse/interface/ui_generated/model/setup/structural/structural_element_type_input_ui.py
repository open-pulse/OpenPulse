# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'structural_element_type_input.ui'
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
        Dialog.resize(400, 400)
        Dialog.setMinimumSize(QSize(400, 400))
        Dialog.setMaximumSize(QSize(400, 400))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.frame_selection = QFrame(self.frame_main)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setMinimumSize(QSize(0, 76))
        self.frame_selection.setFrameShape(QFrame.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_selection)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(7)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.frame_selection)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(True)
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(240, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_selected_id.setFont(font1)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_selected_id, 2, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_selection)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(100, 26))
        self.label_selected_id.setMaximumSize(QSize(100, 26))
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id, 2, 1, 1, 1)

        self.label_attribute_to = QLabel(self.frame_selection)
        self.label_attribute_to.setObjectName(u"label_attribute_to")
        self.label_attribute_to.setMinimumSize(QSize(100, 26))
        self.label_attribute_to.setMaximumSize(QSize(100, 26))
        self.label_attribute_to.setFont(font1)
        self.label_attribute_to.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_attribute_to, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 2, 4, 1, 1)

        self.comboBox_selection = QComboBox(self.frame_selection)
        self.comboBox_selection.addItem("")
        self.comboBox_selection.addItem("")
        self.comboBox_selection.setObjectName(u"comboBox_selection")
        self.comboBox_selection.setMinimumSize(QSize(0, 26))
        self.comboBox_selection.setMaximumSize(QSize(16777215, 26))
        self.comboBox_selection.setFont(font1)

        self.gridLayout_6.addWidget(self.comboBox_selection, 1, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 10000000))
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_element_options = QFrame(self.tab_setup)
        self.frame_element_options.setObjectName(u"frame_element_options")
        self.frame_element_options.setMaximumSize(QSize(16777215, 160))
        self.frame_element_options.setFrameShape(QFrame.NoFrame)
        self.frame_element_options.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_element_options)
        self.gridLayout_7.setSpacing(8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.label_element_type = QLabel(self.frame_element_options)
        self.label_element_type.setObjectName(u"label_element_type")
        self.label_element_type.setMinimumSize(QSize(80, 26))
        self.label_element_type.setMaximumSize(QSize(120, 26))
        self.label_element_type.setFont(font1)
        self.label_element_type.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_element_type, 0, 1, 1, 1)

        self.label_wall_formulation = QLabel(self.frame_element_options)
        self.label_wall_formulation.setObjectName(u"label_wall_formulation")
        self.label_wall_formulation.setMinimumSize(QSize(80, 26))
        self.label_wall_formulation.setMaximumSize(QSize(120, 26))
        self.label_wall_formulation.setFont(font1)
        self.label_wall_formulation.setFrameShape(QFrame.NoFrame)
        self.label_wall_formulation.setFrameShadow(QFrame.Sunken)
        self.label_wall_formulation.setMidLineWidth(0)
        self.label_wall_formulation.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_wall_formulation, 3, 1, 1, 1)

        self.comboBox_wall_formulation = QComboBox(self.frame_element_options)
        self.comboBox_wall_formulation.addItem("")
        self.comboBox_wall_formulation.addItem("")
        self.comboBox_wall_formulation.addItem("")
        self.comboBox_wall_formulation.setObjectName(u"comboBox_wall_formulation")
        self.comboBox_wall_formulation.setMinimumSize(QSize(80, 26))
        self.comboBox_wall_formulation.setMaximumSize(QSize(90, 26))
        self.comboBox_wall_formulation.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_wall_formulation, 3, 2, 1, 1)

        self.label_force_offset = QLabel(self.frame_element_options)
        self.label_force_offset.setObjectName(u"label_force_offset")
        self.label_force_offset.setMinimumSize(QSize(80, 26))
        self.label_force_offset.setMaximumSize(QSize(120, 26))
        self.label_force_offset.setFont(font1)
        self.label_force_offset.setFrameShape(QFrame.NoFrame)
        self.label_force_offset.setFrameShadow(QFrame.Sunken)
        self.label_force_offset.setMidLineWidth(0)
        self.label_force_offset.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_force_offset, 2, 1, 1, 1)

        self.comboBox_capped_end = QComboBox(self.frame_element_options)
        self.comboBox_capped_end.addItem("")
        self.comboBox_capped_end.addItem("")
        self.comboBox_capped_end.setObjectName(u"comboBox_capped_end")
        self.comboBox_capped_end.setMinimumSize(QSize(80, 26))
        self.comboBox_capped_end.setMaximumSize(QSize(90, 26))
        self.comboBox_capped_end.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_capped_end, 1, 2, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_element_options)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(80, 26))
        self.comboBox_element_type.setMaximumSize(QSize(90, 26))
        self.comboBox_element_type.setFont(font1)
        self.comboBox_element_type.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_element_type.setAutoFillBackground(False)
        self.comboBox_element_type.setStyleSheet(u"")
        self.comboBox_element_type.setMaxCount(500)
        self.comboBox_element_type.setInsertPolicy(QComboBox.InsertAtBottom)
        self.comboBox_element_type.setDuplicatesEnabled(False)

        self.gridLayout_7.addWidget(self.comboBox_element_type, 0, 2, 1, 1)

        self.comboBox_force_offset = QComboBox(self.frame_element_options)
        self.comboBox_force_offset.addItem("")
        self.comboBox_force_offset.addItem("")
        self.comboBox_force_offset.setObjectName(u"comboBox_force_offset")
        self.comboBox_force_offset.setMinimumSize(QSize(80, 26))
        self.comboBox_force_offset.setMaximumSize(QSize(90, 26))
        self.comboBox_force_offset.setFont(font1)

        self.gridLayout_7.addWidget(self.comboBox_force_offset, 2, 2, 1, 1)

        self.label_capped_end = QLabel(self.frame_element_options)
        self.label_capped_end.setObjectName(u"label_capped_end")
        self.label_capped_end.setMinimumSize(QSize(80, 26))
        self.label_capped_end.setMaximumSize(QSize(120, 26))
        self.label_capped_end.setFont(font1)
        self.label_capped_end.setFrameShape(QFrame.NoFrame)
        self.label_capped_end.setFrameShadow(QFrame.Sunken)
        self.label_capped_end.setMidLineWidth(0)
        self.label_capped_end.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_capped_end, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_element_options, 0, 0, 1, 1)

        self.frame_button = QFrame(self.tab_setup)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(16777215, 48))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_button)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_button)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_button)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_button, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_details = QWidget()
        self.tab_details.setObjectName(u"tab_details")
        self.gridLayout_10 = QGridLayout(self.tab_details)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(8, 8, 8, 4)
        self.treeWidget_element_type = QTreeWidget(self.tab_details)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_element_type.setObjectName(u"treeWidget_element_type")
        self.treeWidget_element_type.setMinimumSize(QSize(0, 0))
        self.treeWidget_element_type.setMaximumSize(QSize(1000, 1000))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        self.treeWidget_element_type.setFont(font3)
        self.treeWidget_element_type.setAlternatingRowColors(True)
        self.treeWidget_element_type.setIndentation(0)

        self.gridLayout_10.addWidget(self.treeWidget_element_type, 0, 0, 1, 1)

        self.frame = QFrame(self.tab_details)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_details, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_selection, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.comboBox_element_type)
        QWidget.setTabOrder(self.comboBox_element_type, self.comboBox_capped_end)
        QWidget.setTabOrder(self.comboBox_capped_end, self.comboBox_force_offset)
        QWidget.setTabOrder(self.comboBox_force_offset, self.comboBox_wall_formulation)
        QWidget.setTabOrder(self.comboBox_wall_formulation, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.treeWidget_element_type)
        QWidget.setTabOrder(self.treeWidget_element_type, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_wall_formulation.setCurrentIndex(0)
        self.comboBox_capped_end.setCurrentIndex(1)
        self.comboBox_element_type.setCurrentIndex(0)
        self.comboBox_force_offset.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Structural element type setup", None))
        self.lineEdit_selected_id.setText("")
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        self.label_attribute_to.setText(QCoreApplication.translate("Dialog", u"Attribute to:", None))
        self.comboBox_selection.setItemText(0, QCoreApplication.translate("Dialog", u" All lines", None))
        self.comboBox_selection.setItemText(1, QCoreApplication.translate("Dialog", u" Selected lines", None))

        self.label_element_type.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_wall_formulation.setText(QCoreApplication.translate("Dialog", u"Wall formulation:", None))
        self.comboBox_wall_formulation.setItemText(0, QCoreApplication.translate("Dialog", u" Thin", None))
        self.comboBox_wall_formulation.setItemText(1, QCoreApplication.translate("Dialog", u" Thick", None))
        self.comboBox_wall_formulation.setItemText(2, QCoreApplication.translate("Dialog", u" None", None))

        self.label_force_offset.setText(QCoreApplication.translate("Dialog", u"Force offset:", None))
        self.comboBox_capped_end.setItemText(0, QCoreApplication.translate("Dialog", u" Disabled", None))
        self.comboBox_capped_end.setItemText(1, QCoreApplication.translate("Dialog", u" Enabled", None))

        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"  Pipe 1", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"  Beam 1", None))

#if QT_CONFIG(tooltip)
        self.comboBox_element_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">Choose an element type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_element_type.setCurrentText(QCoreApplication.translate("Dialog", u"  Pipe 1", None))
        self.comboBox_force_offset.setItemText(0, QCoreApplication.translate("Dialog", u" Disabled", None))
        self.comboBox_force_offset.setItemText(1, QCoreApplication.translate("Dialog", u" Enabled", None))

        self.label_capped_end.setText(QCoreApplication.translate("Dialog", u"Capped end:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_element_type.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Lines", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Element type", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_details), QCoreApplication.translate("Dialog", u"Details", None))
    # retranslateUi



class StructuralElementTypeInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_selection: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - label_selected_id: QLabel
                                        - label_attribute_to: QLabel
                                        - comboBox_selection: QComboBox
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_element_options: QFrame
                                                - (Layout): QGridLayout
                                                        - label_element_type: QLabel
                                                        - label_wall_formulation: QLabel
                                                        - comboBox_wall_formulation: QComboBox
                                                        - label_force_offset: QLabel
                                                        - comboBox_capped_end: QComboBox
                                                        - comboBox_element_type: QComboBox
                                                        - comboBox_force_offset: QComboBox
                                                        - label_capped_end: QLabel
                                            - frame_button: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
                                - tab_details: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_element_type: QTreeWidget
                                            - frame: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
