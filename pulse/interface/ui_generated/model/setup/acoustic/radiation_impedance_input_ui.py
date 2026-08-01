# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radiation_impedance_input.ui'
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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(420, 360)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(420, 360))
        Dialog.setMaximumSize(QSize(420, 360))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_7 = QGridLayout(Dialog)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(420, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame_title)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_title.setFont(font1)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(420, 480))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_selection_id = QFrame(self.frame_main)
        self.frame_selection_id.setObjectName(u"frame_selection_id")
        self.frame_selection_id.setMinimumSize(QSize(360, 40))
        self.frame_selection_id.setMaximumSize(QSize(380, 40))
        self.frame_selection_id.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selection_id.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_selection_id)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_node_ids = QLineEdit(self.frame_selection_id)
        self.lineEdit_node_ids.setObjectName(u"lineEdit_node_ids")
        self.lineEdit_node_ids.setMinimumSize(QSize(160, 26))
        self.lineEdit_node_ids.setMaximumSize(QSize(160, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_node_ids.setFont(font2)
        self.lineEdit_node_ids.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_node_ids.setStyleSheet(u"")
        self.lineEdit_node_ids.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_node_ids, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_selection_id)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 26))
        self.label_2.setMaximumSize(QSize(100, 26))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_selection_id, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(360, 0))
        self.tabWidget_main.setMaximumSize(QSize(380, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.tabWidget_main.setFont(font3)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_12 = QGridLayout(self.tab_setup)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(8)
        self.gridLayout_12.setVerticalSpacing(4)
        self.gridLayout_12.setContentsMargins(8, 8, 8, 8)
        self.frame_8 = QFrame(self.tab_setup)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 60))
        self.frame_8.setMaximumSize(QSize(400, 160))
        self.frame_8.setFont(font)
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_8)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(70, 0))
        self.frame.setMaximumSize(QSize(70, 16777215))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame, 0, 3, 1, 1)

        self.label_18 = QLabel(self.frame_8)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(80, 30))
        self.label_18.setMaximumSize(QSize(80, 30))
        self.label_18.setFont(font2)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_18, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.comboBox_radiation_impedance_type = QComboBox(self.frame_8)
        self.comboBox_radiation_impedance_type.addItem("")
        self.comboBox_radiation_impedance_type.addItem("")
        self.comboBox_radiation_impedance_type.addItem("")
        self.comboBox_radiation_impedance_type.setObjectName(u"comboBox_radiation_impedance_type")
        self.comboBox_radiation_impedance_type.setMinimumSize(QSize(100, 26))
        self.comboBox_radiation_impedance_type.setMaximumSize(QSize(16777215, 26))
        self.comboBox_radiation_impedance_type.setFont(font3)

        self.gridLayout.addWidget(self.comboBox_radiation_impedance_type, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_setup)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(8)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 8)
        self.pushButton_exit = QPushButton(self.frame_2)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_attribute = QPushButton(self.frame_2)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_attribute, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.frame_2, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_9 = QGridLayout(self.tab_remove)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(8)
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(8, 8, 8, 8)
        self.frame_buttons_remove = QFrame(self.tab_remove)
        self.frame_buttons_remove.setObjectName(u"frame_buttons_remove")
        self.frame_buttons_remove.setMinimumSize(QSize(320, 48))
        self.frame_buttons_remove.setMaximumSize(QSize(600, 48))
        self.frame_buttons_remove.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons_remove.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_buttons_remove)
        self.gridLayout_8.setSpacing(8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(8, 8, 8, 8)
        self.pushButton_reset = QPushButton(self.frame_buttons_remove)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_buttons_remove)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_8.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.frame_buttons_remove, 1, 0, 1, 1)

        self.treeWidget_nodal_info = QTreeWidget(self.tab_remove)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(320, 0))
        self.treeWidget_nodal_info.setMaximumSize(QSize(600, 200))
        self.treeWidget_nodal_info.setFont(font2)
        self.treeWidget_nodal_info.setIndentation(1)
        self.treeWidget_nodal_info.setHeaderHidden(False)
        self.treeWidget_nodal_info.header().setHighlightSections(False)
        self.treeWidget_nodal_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_nodal_info.header().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.treeWidget_nodal_info, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.comboBox_radiation_impedance_type)
        QWidget.setTabOrder(self.comboBox_radiation_impedance_type, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set radiation impedance", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Radiation impedance setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Node ID:", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Impedance:", None))
        self.comboBox_radiation_impedance_type.setItemText(0, QCoreApplication.translate("Dialog", u"Anechoic", None))
        self.comboBox_radiation_impedance_type.setItemText(1, QCoreApplication.translate("Dialog", u"Flanged", None))
        self.comboBox_radiation_impedance_type.setItemText(2, QCoreApplication.translate("Dialog", u"Unflanged", None))

#if QT_CONFIG(tooltip)
        self.comboBox_radiation_impedance_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select the radiation impedance type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Impedance type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_nodal_info.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class RadiationImpedanceInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_selection_id: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_node_ids: QLineEdit
                                        - label_2: QLabel
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - frame: QFrame
                                                        - label_18: QLabel
                                                        - comboBox_radiation_impedance_type: QComboBox
                                            - frame_2: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_exit: QPushButton
                                                        - pushButton_attribute: QPushButton
                                - tab_remove: QWidget
                                    - (Layout): QGridLayout
                                            - frame_buttons_remove: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - treeWidget_nodal_info: QTreeWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
