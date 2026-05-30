# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_element_type_input.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 400)
        Dialog.setMinimumSize(QSize(440, 400))
        Dialog.setMaximumSize(QSize(500, 400))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_title)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.frame_selection = QFrame(self.frame_main)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setMinimumSize(QSize(0, 76))
        self.frame_selection.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_selection)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(7)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.frame_selection)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(True)
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(240, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.lineEdit_selected_id.setFont(font1)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_selection)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(100, 26))
        self.label_selected_id.setMaximumSize(QSize(100, 26))
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id, 1, 1, 1, 1)

        self.label_attribute_to = QLabel(self.frame_selection)
        self.label_attribute_to.setObjectName(u"label_attribute_to")
        self.label_attribute_to.setMinimumSize(QSize(100, 26))
        self.label_attribute_to.setMaximumSize(QSize(100, 26))
        self.label_attribute_to.setFont(font1)
        self.label_attribute_to.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_attribute_to, 0, 1, 1, 1)

        self.comboBox_selection = QComboBox(self.frame_selection)
        self.comboBox_selection.addItem("")
        self.comboBox_selection.addItem("")
        self.comboBox_selection.setObjectName(u"comboBox_selection")
        self.comboBox_selection.setMinimumSize(QSize(0, 26))
        self.comboBox_selection.setMaximumSize(QSize(16777215, 26))
        self.comboBox_selection.setFont(font1)

        self.gridLayout_6.addWidget(self.comboBox_selection, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 1, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(16777215, 10000000))
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_button = QFrame(self.tab_setup)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(16777215, 48))
        self.frame_button.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Shadow.Raised)
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


        self.gridLayout_5.addWidget(self.frame_button, 2, 0, 1, 1)

        self.stackedWidget_main = QStackedWidget(self.tab_setup)
        self.stackedWidget_main.setObjectName(u"stackedWidget_main")
        self.stackedWidget_main.setMinimumSize(QSize(0, 48))
        self.stackedWidget_main.setMaximumSize(QSize(16777215, 80))
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.gridLayout_7 = QGridLayout(self.page_1)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(6)
        self.label_proportional_damping = QLabel(self.page_1)
        self.label_proportional_damping.setObjectName(u"label_proportional_damping")
        self.label_proportional_damping.setMinimumSize(QSize(150, 26))
        self.label_proportional_damping.setMaximumSize(QSize(150, 26))
        self.label_proportional_damping.setFont(font1)
        self.label_proportional_damping.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_proportional_damping, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.lineEdit_proportional_damping = QLineEdit(self.page_1)
        self.lineEdit_proportional_damping.setObjectName(u"lineEdit_proportional_damping")
        self.lineEdit_proportional_damping.setMinimumSize(QSize(160, 26))
        self.lineEdit_proportional_damping.setMaximumSize(QSize(180, 26))
        self.lineEdit_proportional_damping.setFont(font1)
        self.lineEdit_proportional_damping.setStyleSheet(u"")
        self.lineEdit_proportional_damping.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_proportional_damping, 0, 2, 1, 1)

        self.label_volume_rate_unit_3 = QLabel(self.page_1)
        self.label_volume_rate_unit_3.setObjectName(u"label_volume_rate_unit_3")
        self.label_volume_rate_unit_3.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_volume_rate_unit_3.sizePolicy().hasHeightForWidth())
        self.label_volume_rate_unit_3.setSizePolicy(sizePolicy)
        self.label_volume_rate_unit_3.setMinimumSize(QSize(45, 26))
        self.label_volume_rate_unit_3.setMaximumSize(QSize(45, 26))
        self.label_volume_rate_unit_3.setFont(font1)
        self.label_volume_rate_unit_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_volume_rate_unit_3, 0, 3, 1, 1)

        self.stackedWidget_main.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_11 = QGridLayout(self.page_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(20)
        self.gridLayout_11.setContentsMargins(-1, 4, -1, -1)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)

        self.label_volumetric_flow_rate_unit = QLabel(self.page_2)
        self.label_volumetric_flow_rate_unit.setObjectName(u"label_volumetric_flow_rate_unit")
        self.label_volumetric_flow_rate_unit.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_volumetric_flow_rate_unit.sizePolicy().hasHeightForWidth())
        self.label_volumetric_flow_rate_unit.setSizePolicy(sizePolicy)
        self.label_volumetric_flow_rate_unit.setMinimumSize(QSize(45, 26))
        self.label_volumetric_flow_rate_unit.setMaximumSize(QSize(45, 26))
        self.label_volumetric_flow_rate_unit.setFont(font1)
        self.label_volumetric_flow_rate_unit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_volumetric_flow_rate_unit, 0, 3, 1, 1)

        self.lineEdit_volumetric_flow_rate = QLineEdit(self.page_2)
        self.lineEdit_volumetric_flow_rate.setObjectName(u"lineEdit_volumetric_flow_rate")
        self.lineEdit_volumetric_flow_rate.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_volumetric_flow_rate.sizePolicy().hasHeightForWidth())
        self.lineEdit_volumetric_flow_rate.setSizePolicy(sizePolicy1)
        self.lineEdit_volumetric_flow_rate.setMinimumSize(QSize(160, 26))
        self.lineEdit_volumetric_flow_rate.setMaximumSize(QSize(180, 26))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(250, 250, 250, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(100, 100, 100, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        brush3 = QBrush(QColor(240, 240, 240, 0))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_volumetric_flow_rate.setPalette(palette)
        self.lineEdit_volumetric_flow_rate.setFont(font1)
        self.lineEdit_volumetric_flow_rate.setStyleSheet(u"")
        self.lineEdit_volumetric_flow_rate.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_volumetric_flow_rate, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.label_volumetric_flow_rate = QLabel(self.page_2)
        self.label_volumetric_flow_rate.setObjectName(u"label_volumetric_flow_rate")
        self.label_volumetric_flow_rate.setMinimumSize(QSize(150, 0))
        self.label_volumetric_flow_rate.setMaximumSize(QSize(150, 16777215))
        self.label_volumetric_flow_rate.setFont(font1)
        self.label_volumetric_flow_rate.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_volumetric_flow_rate, 0, 1, 1, 1)

        self.pushButton_get_volumetric_flow_rate = QPushButton(self.page_2)
        self.pushButton_get_volumetric_flow_rate.setObjectName(u"pushButton_get_volumetric_flow_rate")
        self.pushButton_get_volumetric_flow_rate.setMinimumSize(QSize(80, 28))
        self.pushButton_get_volumetric_flow_rate.setMaximumSize(QSize(180, 28))
        self.pushButton_get_volumetric_flow_rate.setFont(font2)
        self.pushButton_get_volumetric_flow_rate.setStyleSheet(u"")
        self.pushButton_get_volumetric_flow_rate.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_get_volumetric_flow_rate, 1, 2, 1, 1)

        self.label_get_flow_rate_from = QLabel(self.page_2)
        self.label_get_flow_rate_from.setObjectName(u"label_get_flow_rate_from")
        self.label_get_flow_rate_from.setMinimumSize(QSize(150, 0))
        self.label_get_flow_rate_from.setMaximumSize(QSize(150, 16777215))
        self.label_get_flow_rate_from.setFont(font1)
        self.label_get_flow_rate_from.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_get_flow_rate_from, 1, 1, 1, 1)

        self.stackedWidget_main.addWidget(self.page_2)

        self.gridLayout_5.addWidget(self.stackedWidget_main, 1, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_setup)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_11, 0, 0, 1, 1)

        self.comboBox_element_type = QComboBox(self.frame_2)
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.addItem("")
        self.comboBox_element_type.setObjectName(u"comboBox_element_type")
        self.comboBox_element_type.setMinimumSize(QSize(160, 26))
        self.comboBox_element_type.setMaximumSize(QSize(160, 26))
        self.comboBox_element_type.setFont(font1)
        self.comboBox_element_type.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox_element_type.setAutoFillBackground(False)
        self.comboBox_element_type.setStyleSheet(u"")
        self.comboBox_element_type.setMaxCount(500)
        self.comboBox_element_type.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.comboBox_element_type.setDuplicatesEnabled(False)

        self.gridLayout_13.addWidget(self.comboBox_element_type, 0, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

        self.label_element_type = QLabel(self.frame_2)
        self.label_element_type.setObjectName(u"label_element_type")
        self.label_element_type.setMinimumSize(QSize(150, 26))
        self.label_element_type.setMaximumSize(QSize(150, 26))
        self.label_element_type.setFont(font1)
        self.label_element_type.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_element_type, 0, 1, 1, 1)

        self.label_volume_rate_unit_2 = QLabel(self.frame_2)
        self.label_volume_rate_unit_2.setObjectName(u"label_volume_rate_unit_2")
        self.label_volume_rate_unit_2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_volume_rate_unit_2.sizePolicy().hasHeightForWidth())
        self.label_volume_rate_unit_2.setSizePolicy(sizePolicy)
        self.label_volume_rate_unit_2.setMinimumSize(QSize(45, 26))
        self.label_volume_rate_unit_2.setMaximumSize(QSize(45, 26))
        self.label_volume_rate_unit_2.setFont(font1)
        self.label_volume_rate_unit_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_volume_rate_unit_2, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_2, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_details = QWidget()
        self.tab_details.setObjectName(u"tab_details")
        self.gridLayout_10 = QGridLayout(self.tab_details)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.treeWidget_element_type = QTreeWidget(self.tab_details)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_element_type.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_element_type.setObjectName(u"treeWidget_element_type")
        self.treeWidget_element_type.setMinimumSize(QSize(0, 0))
        self.treeWidget_element_type.setMaximumSize(QSize(1000, 1000))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        self.treeWidget_element_type.setFont(font3)
        self.treeWidget_element_type.setAlternatingRowColors(True)
        self.treeWidget_element_type.setIndentation(0)

        self.gridLayout_10.addWidget(self.treeWidget_element_type, 0, 0, 1, 1)

        self.frame = QFrame(self.tab_details)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
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
        QWidget.setTabOrder(self.tabWidget_main, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.treeWidget_element_type)
        QWidget.setTabOrder(self.treeWidget_element_type, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)
        self.stackedWidget_main.setCurrentIndex(1)
        self.pushButton_get_volumetric_flow_rate.setDefault(False)
        self.comboBox_element_type.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Acoustic element type setup", None))
        self.lineEdit_selected_id.setText("")
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        self.label_attribute_to.setText(QCoreApplication.translate("Dialog", u"Attribute to:", None))
        self.comboBox_selection.setItemText(0, QCoreApplication.translate("Dialog", u" All lines", None))
        self.comboBox_selection.setItemText(1, QCoreApplication.translate("Dialog", u" Selected lines", None))

        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_proportional_damping.setText(QCoreApplication.translate("Dialog", u"Proportional damping:", None))
        self.label_volume_rate_unit_3.setText("")
        self.label_volumetric_flow_rate_unit.setText(QCoreApplication.translate("Dialog", u"[m\u00b3/s]", None))
        self.lineEdit_volumetric_flow_rate.setText("")
        self.label_volumetric_flow_rate.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate:", None))
        self.pushButton_get_volumetric_flow_rate.setText(QCoreApplication.translate("Dialog", u"Pump", None))
        self.label_get_flow_rate_from.setText(QCoreApplication.translate("Dialog", u"Get flow rate from:", None))
        self.comboBox_element_type.setItemText(0, QCoreApplication.translate("Dialog", u"Undamped", None))
        self.comboBox_element_type.setItemText(1, QCoreApplication.translate("Dialog", u"Proportional", None))
        self.comboBox_element_type.setItemText(2, QCoreApplication.translate("Dialog", u"Wide-duct", None))
        self.comboBox_element_type.setItemText(3, QCoreApplication.translate("Dialog", u"LRF fluid equivalent", None))
        self.comboBox_element_type.setItemText(4, QCoreApplication.translate("Dialog", u"LRF full", None))
        self.comboBox_element_type.setItemText(5, QCoreApplication.translate("Dialog", u"Damped (for liquids)", None))
        self.comboBox_element_type.setItemText(6, QCoreApplication.translate("Dialog", u"Undamped mean flow", None))
        self.comboBox_element_type.setItemText(7, QCoreApplication.translate("Dialog", u"Peters", None))
        self.comboBox_element_type.setItemText(8, QCoreApplication.translate("Dialog", u"Howe", None))

#if QT_CONFIG(tooltip)
        self.comboBox_element_type.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">Choose an element type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_element_type.setCurrentText(QCoreApplication.translate("Dialog", u"Undamped", None))
        self.label_element_type.setText(QCoreApplication.translate("Dialog", u"Element type:", None))
        self.label_volume_rate_unit_2.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_element_type.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Lines", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Element type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Group", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_details), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class AcousticElementTypeInput_UI(QDialog, Ui_Dialog):
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
                                            - frame_button: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
                                            - stackedWidget_main: QStackedWidget
                                                - page_1: QWidget
                                                    - (Layout): QGridLayout
                                                            - label_proportional_damping: QLabel
                                                            - lineEdit_proportional_damping: QLineEdit
                                                            - label_volume_rate_unit_3: QLabel
                                                - page_2: QWidget
                                                    - (Layout): QGridLayout
                                                            - label_volumetric_flow_rate_unit: QLabel
                                                            - lineEdit_volumetric_flow_rate: QLineEdit
                                                            - label_volumetric_flow_rate: QLabel
                                                            - pushButton_get_volumetric_flow_rate: QPushButton
                                                            - label_get_flow_rate_from: QLabel
                                            - frame_2: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_element_type: QComboBox
                                                        - label_element_type: QLabel
                                                        - label_volume_rate_unit_2: QLabel
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
