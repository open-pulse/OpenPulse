# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'standard_cross_section_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(660, 600)
        Dialog.setMinimumSize(QSize(660, 550))
        Dialog.setMaximumSize(QSize(660, 600))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QSize(0, 52))
        self.frame.setMaximumSize(QSize(16777215, 52))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_confirm_selection = QPushButton(self.frame)
        self.pushButton_confirm_selection.setObjectName(u"pushButton_confirm_selection")
        self.pushButton_confirm_selection.setEnabled(True)
        self.pushButton_confirm_selection.setMinimumSize(QSize(120, 32))
        self.pushButton_confirm_selection.setMaximumSize(QSize(120, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_confirm_selection.setFont(font)
        self.pushButton_confirm_selection.setStyleSheet(u"")
        self.pushButton_confirm_selection.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_confirm_selection, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setEnabled(True)
        self.pushButton_exit.setMinimumSize(QSize(120, 32))
        self.pushButton_exit.setMaximumSize(QSize(120, 32))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

        self.frame1 = QFrame(Dialog)
        self.frame1.setObjectName(u"frame1")
        self.frame1.setFrameShape(QFrame.Shape.Box)
        self.frame1.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame1)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame1)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_section_data = QTreeWidget(self.frame_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        self.treeWidget_section_data.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_section_data.setObjectName(u"treeWidget_section_data")
        self.treeWidget_section_data.setMinimumSize(QSize(500, 0))
        self.treeWidget_section_data.setMaximumSize(QSize(620, 420))
        self.treeWidget_section_data.setIndentation(0)

        self.gridLayout_6.addWidget(self.treeWidget_section_data, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.frame1)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 7, 1, 1)

        self.comboBox_units = QComboBox(self.frame_3)
        self.comboBox_units.addItem("")
        self.comboBox_units.addItem("")
        self.comboBox_units.setObjectName(u"comboBox_units")
        self.comboBox_units.setMinimumSize(QSize(0, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_units.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_units, 1, 12, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.comboBox_pipe_material = QComboBox(self.frame_3)
        self.comboBox_pipe_material.addItem("")
        self.comboBox_pipe_material.addItem("")
        self.comboBox_pipe_material.setObjectName(u"comboBox_pipe_material")
        self.comboBox_pipe_material.setMinimumSize(QSize(0, 28))
        self.comboBox_pipe_material.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_pipe_material, 1, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 1, 13, 1, 1)

        self.label_pipe_material = QLabel(self.frame_3)
        self.label_pipe_material.setObjectName(u"label_pipe_material")
        self.label_pipe_material.setFont(font1)
        self.label_pipe_material.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_pipe_material, 1, 1, 1, 1)

        self.comboBox_nps_filter = QComboBox(self.frame_3)
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.addItem("")
        self.comboBox_nps_filter.setObjectName(u"comboBox_nps_filter")
        self.comboBox_nps_filter.setMinimumSize(QSize(120, 28))
        self.comboBox_nps_filter.setFont(font1)

        self.gridLayout_4.addWidget(self.comboBox_nps_filter, 1, 6, 1, 1)

        self.checkBox_nps_filter = QCheckBox(self.frame_3)
        self.checkBox_nps_filter.setObjectName(u"checkBox_nps_filter")
        self.checkBox_nps_filter.setMinimumSize(QSize(18, 0))
        self.checkBox_nps_filter.setFont(font1)
        self.checkBox_nps_filter.setChecked(False)

        self.gridLayout_4.addWidget(self.checkBox_nps_filter, 1, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.label_units = QLabel(self.frame_3)
        self.label_units.setObjectName(u"label_units")
        self.label_units.setFont(font1)
        self.label_units.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_units, 1, 8, 1, 1)

        self.label_pipe_material_2 = QLabel(self.frame_3)
        self.label_pipe_material_2.setObjectName(u"label_pipe_material_2")
        self.label_pipe_material_2.setFont(font1)
        self.label_pipe_material_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_pipe_material_2, 1, 5, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame1, 1, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_2)
        self.label_title.setObjectName(u"label_title")
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(11)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_title.setFont(font2)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_units, self.treeWidget_section_data)
        QWidget.setTabOrder(self.treeWidget_section_data, self.pushButton_confirm_selection)

        self.retranslateUi(Dialog)

        self.pushButton_confirm_selection.setDefault(True)
        self.pushButton_exit.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Standardized cross-sections", None))
        self.pushButton_confirm_selection.setText(QCoreApplication.translate("Dialog", u"Load section", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.comboBox_units.setItemText(0, QCoreApplication.translate("Dialog", u"inches", None))
        self.comboBox_units.setItemText(1, QCoreApplication.translate("Dialog", u"millimeters", None))

        self.comboBox_pipe_material.setItemText(0, QCoreApplication.translate("Dialog", u"Carbon steel", None))
        self.comboBox_pipe_material.setItemText(1, QCoreApplication.translate("Dialog", u"Stainless steel", None))

        self.label_pipe_material.setText(QCoreApplication.translate("Dialog", u"Pipe material:", None))
        self.comboBox_nps_filter.setItemText(0, QCoreApplication.translate("Dialog", u"0.125 (1/8)", None))
        self.comboBox_nps_filter.setItemText(1, QCoreApplication.translate("Dialog", u"0.25 (1/4)", None))
        self.comboBox_nps_filter.setItemText(2, QCoreApplication.translate("Dialog", u"0.5 (1/2)", None))
        self.comboBox_nps_filter.setItemText(3, QCoreApplication.translate("Dialog", u"0.75 (3/4)", None))
        self.comboBox_nps_filter.setItemText(4, QCoreApplication.translate("Dialog", u"1", None))
        self.comboBox_nps_filter.setItemText(5, QCoreApplication.translate("Dialog", u"1.25 (1+1/4)", None))
        self.comboBox_nps_filter.setItemText(6, QCoreApplication.translate("Dialog", u"1.5 (1+1/2)", None))
        self.comboBox_nps_filter.setItemText(7, QCoreApplication.translate("Dialog", u"2", None))
        self.comboBox_nps_filter.setItemText(8, QCoreApplication.translate("Dialog", u"2.5 (2+1/2)", None))
        self.comboBox_nps_filter.setItemText(9, QCoreApplication.translate("Dialog", u"3", None))
        self.comboBox_nps_filter.setItemText(10, QCoreApplication.translate("Dialog", u"3.5 (3+1/2)", None))
        self.comboBox_nps_filter.setItemText(11, QCoreApplication.translate("Dialog", u"4", None))
        self.comboBox_nps_filter.setItemText(12, QCoreApplication.translate("Dialog", u"5", None))
        self.comboBox_nps_filter.setItemText(13, QCoreApplication.translate("Dialog", u"6", None))
        self.comboBox_nps_filter.setItemText(14, QCoreApplication.translate("Dialog", u"8", None))
        self.comboBox_nps_filter.setItemText(15, QCoreApplication.translate("Dialog", u"10", None))
        self.comboBox_nps_filter.setItemText(16, QCoreApplication.translate("Dialog", u"12", None))
        self.comboBox_nps_filter.setItemText(17, QCoreApplication.translate("Dialog", u"14", None))
        self.comboBox_nps_filter.setItemText(18, QCoreApplication.translate("Dialog", u"16", None))
        self.comboBox_nps_filter.setItemText(19, QCoreApplication.translate("Dialog", u"18", None))
        self.comboBox_nps_filter.setItemText(20, QCoreApplication.translate("Dialog", u"20", None))
        self.comboBox_nps_filter.setItemText(21, QCoreApplication.translate("Dialog", u"22", None))
        self.comboBox_nps_filter.setItemText(22, QCoreApplication.translate("Dialog", u"24", None))
        self.comboBox_nps_filter.setItemText(23, QCoreApplication.translate("Dialog", u"26", None))
        self.comboBox_nps_filter.setItemText(24, QCoreApplication.translate("Dialog", u"28", None))
        self.comboBox_nps_filter.setItemText(25, QCoreApplication.translate("Dialog", u"30", None))
        self.comboBox_nps_filter.setItemText(26, QCoreApplication.translate("Dialog", u"32", None))
        self.comboBox_nps_filter.setItemText(27, QCoreApplication.translate("Dialog", u"34", None))
        self.comboBox_nps_filter.setItemText(28, QCoreApplication.translate("Dialog", u"36", None))
        self.comboBox_nps_filter.setItemText(29, QCoreApplication.translate("Dialog", u"38", None))
        self.comboBox_nps_filter.setItemText(30, QCoreApplication.translate("Dialog", u"40", None))
        self.comboBox_nps_filter.setItemText(31, QCoreApplication.translate("Dialog", u"42", None))
        self.comboBox_nps_filter.setItemText(32, QCoreApplication.translate("Dialog", u"44", None))
        self.comboBox_nps_filter.setItemText(33, QCoreApplication.translate("Dialog", u"46", None))
        self.comboBox_nps_filter.setItemText(34, QCoreApplication.translate("Dialog", u"48", None))
        self.comboBox_nps_filter.setItemText(35, QCoreApplication.translate("Dialog", u"52", None))
        self.comboBox_nps_filter.setItemText(36, QCoreApplication.translate("Dialog", u"56", None))
        self.comboBox_nps_filter.setItemText(37, QCoreApplication.translate("Dialog", u"60", None))
        self.comboBox_nps_filter.setItemText(38, QCoreApplication.translate("Dialog", u"64", None))
        self.comboBox_nps_filter.setItemText(39, QCoreApplication.translate("Dialog", u"68", None))
        self.comboBox_nps_filter.setItemText(40, QCoreApplication.translate("Dialog", u"72", None))
        self.comboBox_nps_filter.setItemText(41, QCoreApplication.translate("Dialog", u"76", None))
        self.comboBox_nps_filter.setItemText(42, QCoreApplication.translate("Dialog", u"80", None))

        self.checkBox_nps_filter.setText("")
        self.label_units.setText(QCoreApplication.translate("Dialog", u"Units:", None))
        self.label_pipe_material_2.setText(QCoreApplication.translate("Dialog", u"NPS filter:", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Select a standardized cross-section", None))
    # retranslateUi



class StandardCrossSectionInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm_selection: QPushButton
                            - pushButton_exit: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_section_data: QTreeWidget
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_units: QComboBox
                                        - comboBox_pipe_material: QComboBox
                                        - label_pipe_material: QLabel
                                        - comboBox_nps_filter: QComboBox
                                        - checkBox_nps_filter: QCheckBox
                                        - label_units: QLabel
                                        - label_pipe_material_2: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
