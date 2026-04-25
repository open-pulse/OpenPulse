# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stress_stiffening_input.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 460)
        Dialog.setMinimumSize(QSize(480, 460))
        Dialog.setMaximumSize(QSize(480, 460))
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
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_7 = QFrame(Dialog)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 40))
        self.frame_7.setMaximumSize(QSize(16777215, 40))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.pushButton_exit = QPushButton(self.frame_7)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_attribute = QPushButton(self.frame_7)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font1)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_attribute, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_7, 2, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_attribution_options = QFrame(self.frame_2)
        self.frame_attribution_options.setObjectName(u"frame_attribution_options")
        self.frame_attribution_options.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_attribution_options.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_attribution_options)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(7)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_id = QLineEdit(self.frame_attribution_options)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(False)
        self.lineEdit_selected_id.setMinimumSize(QSize(150, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(16777215, 26))
        font2 = QFont()
        font2.setPointSize(10)
        self.lineEdit_selected_id.setFont(font2)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.frame_attribution_options)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(150, 26))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 26))
        self.comboBox_attribution_type.setFont(font2)

        self.gridLayout_6.addWidget(self.comboBox_attribution_type, 0, 2, 1, 1)

        self.label_attribute_to = QLabel(self.frame_attribution_options)
        self.label_attribute_to.setObjectName(u"label_attribute_to")
        self.label_attribute_to.setMinimumSize(QSize(110, 26))
        self.label_attribute_to.setMaximumSize(QSize(110, 26))
        self.label_attribute_to.setFont(font2)
        self.label_attribute_to.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_attribute_to, 0, 1, 1, 1)

        self.label_selected_id = QLabel(self.frame_attribution_options)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(110, 26))
        self.label_selected_id.setMaximumSize(QSize(110, 26))
        self.label_selected_id.setFont(font2)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 1, 5, 1, 1)


        self.gridLayout_7.addWidget(self.frame_attribution_options, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 1000))
        self.tabWidget_main.setFont(font2)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.tab_setup)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 120))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.label_external_pressure_unit = QLabel(self.frame_3)
        self.label_external_pressure_unit.setObjectName(u"label_external_pressure_unit")
        self.label_external_pressure_unit.setMinimumSize(QSize(80, 28))
        self.label_external_pressure_unit.setMaximumSize(QSize(80, 28))
        self.label_external_pressure_unit.setFont(font2)
        self.label_external_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_external_pressure_unit, 1, 3, 1, 1)

        self.lineEdit_internal_pressure = QLineEdit(self.frame_3)
        self.lineEdit_internal_pressure.setObjectName(u"lineEdit_internal_pressure")
        self.lineEdit_internal_pressure.setMinimumSize(QSize(160, 28))
        self.lineEdit_internal_pressure.setMaximumSize(QSize(160, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_internal_pressure.setFont(font3)
        self.lineEdit_internal_pressure.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_internal_pressure.setStyleSheet(u"")
        self.lineEdit_internal_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_internal_pressure, 2, 2, 1, 1)

        self.label_26 = QLabel(self.frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(0, 28))
        self.label_26.setMaximumSize(QSize(16777215, 28))
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_26, 2, 1, 1, 1)

        self.lineEdit_external_pressure = QLineEdit(self.frame_3)
        self.lineEdit_external_pressure.setObjectName(u"lineEdit_external_pressure")
        self.lineEdit_external_pressure.setMinimumSize(QSize(160, 28))
        self.lineEdit_external_pressure.setMaximumSize(QSize(160, 28))
        self.lineEdit_external_pressure.setFont(font3)
        self.lineEdit_external_pressure.setStyleSheet(u"")
        self.lineEdit_external_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_external_pressure, 1, 2, 1, 1)

        self.label_25 = QLabel(self.frame_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(0, 28))
        self.label_25.setMaximumSize(QSize(16777215, 28))
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_25, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 1, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.label_27 = QLabel(self.frame_3)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMinimumSize(QSize(0, 28))
        self.label_27.setMaximumSize(QSize(16777215, 28))
        self.label_27.setFont(font2)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_27, 0, 1, 1, 1)

        self.comboBox_pressure_units = QComboBox(self.frame_3)
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.addItem("")
        self.comboBox_pressure_units.setObjectName(u"comboBox_pressure_units")
        self.comboBox_pressure_units.setMinimumSize(QSize(160, 28))
        self.comboBox_pressure_units.setMaximumSize(QSize(160, 28))
        self.comboBox_pressure_units.setFont(font1)

        self.gridLayout_8.addWidget(self.comboBox_pressure_units, 0, 2, 1, 1)

        self.label_internal_pressure_unit = QLabel(self.frame_3)
        self.label_internal_pressure_unit.setObjectName(u"label_internal_pressure_unit")
        self.label_internal_pressure_unit.setMinimumSize(QSize(80, 28))
        self.label_internal_pressure_unit.setMaximumSize(QSize(80, 28))
        self.label_internal_pressure_unit.setFont(font2)
        self.label_internal_pressure_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_internal_pressure_unit, 2, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 0, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_4 = QGridLayout(self.tab_list)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.treeWidget_lines_info = QTreeWidget(self.tab_list)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_lines_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_lines_info.setObjectName(u"treeWidget_lines_info")
        self.treeWidget_lines_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_lines_info.setMaximumSize(QSize(1000, 1000))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(9)
        self.treeWidget_lines_info.setFont(font4)
        self.treeWidget_lines_info.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.treeWidget_lines_info.setIndentation(0)

        self.gridLayout_4.addWidget(self.treeWidget_lines_info, 0, 1, 1, 1)

        self.frame_buttons = QFrame(self.tab_list)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMaximumSize(QSize(16777215, 80))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_buttons)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_buttons, 1, 1, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_7.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_attribution_type, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_external_pressure)
        QWidget.setTabOrder(self.lineEdit_external_pressure, self.lineEdit_internal_pressure)
        QWidget.setTabOrder(self.lineEdit_internal_pressure, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.treeWidget_lines_info)
        QWidget.setTabOrder(self.treeWidget_lines_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.pushButton_attribute.setDefault(False)
        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_pressure_units.setCurrentIndex(0)
        self.pushButton_remove.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Stress stiffening setup", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.lineEdit_selected_id.setText(QCoreApplication.translate("Dialog", u"All lines", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u"All lines", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))

#if QT_CONFIG(tooltip)
        self.comboBox_attribution_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Enable stress stiffening effects to:</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_attribute_to.setText(QCoreApplication.translate("Dialog", u"Attribute to:", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.label_external_pressure_unit.setText(QCoreApplication.translate("Dialog", u"Pa (a]", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"Internal pressure:", None))
        self.lineEdit_external_pressure.setText("")
        self.label_25.setText(QCoreApplication.translate("Dialog", u"External pressure:", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"Pressure units:", None))
        self.comboBox_pressure_units.setItemText(0, QCoreApplication.translate("Dialog", u"Pa (a)", None))
        self.comboBox_pressure_units.setItemText(1, QCoreApplication.translate("Dialog", u"kPa (a)", None))
        self.comboBox_pressure_units.setItemText(2, QCoreApplication.translate("Dialog", u"atm (a)", None))
        self.comboBox_pressure_units.setItemText(3, QCoreApplication.translate("Dialog", u"bar (a)", None))
        self.comboBox_pressure_units.setItemText(4, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (a)", None))
        self.comboBox_pressure_units.setItemText(5, QCoreApplication.translate("Dialog", u"psi (a)", None))
        self.comboBox_pressure_units.setItemText(6, QCoreApplication.translate("Dialog", u"ksi (a)", None))
        self.comboBox_pressure_units.setItemText(7, QCoreApplication.translate("Dialog", u"Pa (g)", None))
        self.comboBox_pressure_units.setItemText(8, QCoreApplication.translate("Dialog", u"kPa (g)", None))
        self.comboBox_pressure_units.setItemText(9, QCoreApplication.translate("Dialog", u"atm (g)", None))
        self.comboBox_pressure_units.setItemText(10, QCoreApplication.translate("Dialog", u"bar (g)", None))
        self.comboBox_pressure_units.setItemText(11, QCoreApplication.translate("Dialog", u"kgf/cm\u00b2 (g)", None))
        self.comboBox_pressure_units.setItemText(12, QCoreApplication.translate("Dialog", u"psi (g)", None))
        self.comboBox_pressure_units.setItemText(13, QCoreApplication.translate("Dialog", u"ksi (g)", None))

        self.label_internal_pressure_unit.setText(QCoreApplication.translate("Dialog", u"Pa (a)", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_lines_info.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"Pressure units", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Internal pressure", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"External pressure", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Lines", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_lines_info.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:400; font-style:normal;\">Select a group to remove the capped end attributed to lines</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class StressStiffeningInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_7: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_attribute: QPushButton
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_attribution_options: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - comboBox_attribution_type: QComboBox
                                        - label_attribute_to: QLabel
                                        - label_selected_id: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_external_pressure_unit: QLabel
                                                        - lineEdit_internal_pressure: QLineEdit
                                                        - label_26: QLabel
                                                        - lineEdit_external_pressure: QLineEdit
                                                        - label_25: QLabel
                                                        - label_27: QLabel
                                                        - comboBox_pressure_units: QComboBox
                                                        - label_internal_pressure_unit: QLabel
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_lines_info: QTreeWidget
                                            - frame_buttons: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_remove: QPushButton
                                                        - pushButton_reset: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
