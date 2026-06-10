# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'b2p_decoupling_rotation_dofs_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(421, 460)
        Dialog.setMinimumSize(QSize(420, 360))
        Dialog.setMaximumSize(QSize(421, 460))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 48))
        self.frame_main.setMaximumSize(QSize(16777215, 16777215))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        font = QFont()
        font.setPointSize(10)
        self.tabWidget_main.setFont(font)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_13 = QGridLayout(self.tab_setup)
        self.gridLayout_13.setSpacing(4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab_setup)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 100))
        self.frame_7.setMaximumSize(QSize(16777215, 120))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_7)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(10, 4, 10, 4)
        self.label_9 = QLabel(self.frame_7)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(300, 30))
        self.label_9.setMaximumSize(QSize(360, 30))
        self.label_9.setFont(font)
        self.label_9.setFrameShape(QFrame.Shape.Box)
        self.label_9.setFrameShadow(QFrame.Shadow.Raised)
        self.label_9.setMidLineWidth(0)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.label_9, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_7)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 52))
        self.frame_2.setMaximumSize(QSize(360, 600))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(8)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.checkBox_rotation_x = QCheckBox(self.frame_2)
        self.checkBox_rotation_x.setObjectName(u"checkBox_rotation_x")
        self.checkBox_rotation_x.setMaximumSize(QSize(104, 16777215))
        self.checkBox_rotation_x.setFont(font)
        self.checkBox_rotation_x.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_rotation_x, 0, 1, 1, 1)

        self.checkBox_rotation_y = QCheckBox(self.frame_2)
        self.checkBox_rotation_y.setObjectName(u"checkBox_rotation_y")
        self.checkBox_rotation_y.setMaximumSize(QSize(104, 16777215))
        self.checkBox_rotation_y.setFont(font)
        self.checkBox_rotation_y.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_rotation_y, 0, 3, 1, 1)

        self.checkBox_rotation_z = QCheckBox(self.frame_2)
        self.checkBox_rotation_z.setObjectName(u"checkBox_rotation_z")
        self.checkBox_rotation_z.setMaximumSize(QSize(104, 16777215))
        self.checkBox_rotation_z.setFont(font)
        self.checkBox_rotation_z.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_rotation_z, 0, 5, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 0, 6, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)


        self.gridLayout_10.addWidget(self.frame_2, 1, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame_7, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_8 = QGridLayout(self.tab_list)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.tab_list)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_3)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_elements_info = QTreeWidget(self.frame_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_elements_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_elements_info.setObjectName(u"treeWidget_elements_info")
        self.treeWidget_elements_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_elements_info.setMaximumSize(QSize(1000, 1000))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(9)
        self.treeWidget_elements_info.setFont(font1)
        self.treeWidget_elements_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.treeWidget_elements_info.setFrameShadow(QFrame.Shadow.Sunken)
        self.treeWidget_elements_info.setIndentation(0)

        self.gridLayout_6.addWidget(self.treeWidget_elements_info, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.tab_list)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 48))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setKerning(False)
        self.frame_4.setFont(font2)
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_4)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset = QPushButton(self.frame_4)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_4)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.frame_4, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_main)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 72))
        self.frame_6.setMaximumSize(QSize(16777215, 72))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(4)
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.label_3 = QLabel(self.frame_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 26))
        self.label_3.setMaximumSize(QSize(16777215, 26))
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.TextFormat.AutoText)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(100, 26))
        self.label_7.setMaximumSize(QSize(16777215, 26))
        self.label_7.setFont(font)
        self.label_7.setTextFormat(Qt.TextFormat.AutoText)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_7, 1, 1, 1, 1)

        self.lineEdit_element_id = QLineEdit(self.frame_6)
        self.lineEdit_element_id.setObjectName(u"lineEdit_element_id")
        self.lineEdit_element_id.setEnabled(False)
        self.lineEdit_element_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_element_id.setMaximumSize(QSize(100, 26))
        self.lineEdit_element_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_element_id.setStyleSheet(u"")
        self.lineEdit_element_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_element_id, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)

        self.lineEdit_tjoint_node_id = QLineEdit(self.frame_6)
        self.lineEdit_tjoint_node_id.setObjectName(u"lineEdit_tjoint_node_id")
        self.lineEdit_tjoint_node_id.setEnabled(False)
        self.lineEdit_tjoint_node_id.setMinimumSize(QSize(100, 26))
        self.lineEdit_tjoint_node_id.setMaximumSize(QSize(100, 26))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(250, 250, 250, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        brush3 = QBrush(QColor(100, 100, 100, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush3)
        brush4 = QBrush(QColor(240, 240, 240, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush4)
        self.lineEdit_tjoint_node_id.setPalette(palette)
        self.lineEdit_tjoint_node_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_tjoint_node_id.setStyleSheet(u"")
        self.lineEdit_tjoint_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_tjoint_node_id.setClearButtonEnabled(False)

        self.gridLayout_11.addWidget(self.lineEdit_tjoint_node_id, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setPointSize(11)
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_8 = QFrame(Dialog)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 48))
        self.frame_8.setMaximumSize(QSize(16777215, 48))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_8)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_8)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_8)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_12.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_8, 2, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.checkBox_rotation_x)
        QWidget.setTabOrder(self.checkBox_rotation_x, self.checkBox_rotation_y)
        QWidget.setTabOrder(self.checkBox_rotation_y, self.checkBox_rotation_z)
        QWidget.setTabOrder(self.checkBox_rotation_z, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_remove.setDefault(False)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"DOFs to decouple", None))
        self.checkBox_rotation_x.setText(QCoreApplication.translate("Dialog", u"Rotation x", None))
        self.checkBox_rotation_y.setText(QCoreApplication.translate("Dialog", u"Rotation y", None))
        self.checkBox_rotation_z.setText(QCoreApplication.translate("Dialog", u"Rotation z", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_elements_info.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Decoupled DOFs", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Node ID", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Element ID", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Element ID:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"T-joint node ID:", None))
        self.lineEdit_element_id.setText("")
        self.lineEdit_tjoint_node_id.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Rotation DOFs decoupling setup", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class B2pDecouplingRotationDofsInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_7: QFrame
                                                - (Layout): QGridLayout
                                                        - label_9: QLabel
                                                        - frame_2: QFrame
                                                            - (Layout): QGridLayout
                                                                    - checkBox_rotation_x: QCheckBox
                                                                    - checkBox_rotation_y: QCheckBox
                                                                    - checkBox_rotation_z: QCheckBox
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_elements_info: QTreeWidget
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - label_3: QLabel
                                        - label_7: QLabel
                                        - lineEdit_element_id: QLineEdit
                                        - lineEdit_tjoint_node_id: QLineEdit
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_8: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
