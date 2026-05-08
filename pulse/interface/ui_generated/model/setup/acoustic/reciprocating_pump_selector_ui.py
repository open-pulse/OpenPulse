# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reciprocating_pump_selector.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(479, 399)
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

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_selection = QFrame(self.frame)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setMinimumSize(QSize(0, 90))
        self.frame_selection.setFrameShape(QFrame.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_selection)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(7)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.label_selected_id = QLabel(self.frame_selection)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(100, 26))
        self.label_selected_id.setMaximumSize(QSize(160, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.frame_selection)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(True)
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(240, 26))
        self.lineEdit_selected_id.setFont(font1)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_volume_rate_unit = QLabel(self.frame_selection)
        self.label_volume_rate_unit.setObjectName(u"label_volume_rate_unit")
        self.label_volume_rate_unit.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_volume_rate_unit.sizePolicy().hasHeightForWidth())
        self.label_volume_rate_unit.setSizePolicy(sizePolicy)
        self.label_volume_rate_unit.setMinimumSize(QSize(45, 26))
        self.label_volume_rate_unit.setMaximumSize(QSize(45, 26))
        self.label_volume_rate_unit.setFont(font1)
        self.label_volume_rate_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_volume_rate_unit, 2, 3, 1, 1)

        self.lineEdit_volumetric_flow_rate = QLineEdit(self.frame_selection)
        self.lineEdit_volumetric_flow_rate.setObjectName(u"lineEdit_volumetric_flow_rate")
        self.lineEdit_volumetric_flow_rate.setEnabled(True)
        self.lineEdit_volumetric_flow_rate.setMinimumSize(QSize(0, 26))
        self.lineEdit_volumetric_flow_rate.setMaximumSize(QSize(240, 26))
        self.lineEdit_volumetric_flow_rate.setFont(font1)
        self.lineEdit_volumetric_flow_rate.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_volumetric_flow_rate.setStyleSheet(u"")
        self.lineEdit_volumetric_flow_rate.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_volumetric_flow_rate, 2, 2, 1, 1)

        self.label_selected_id_2 = QLabel(self.frame_selection)
        self.label_selected_id_2.setObjectName(u"label_selected_id_2")
        self.label_selected_id_2.setMinimumSize(QSize(100, 26))
        self.label_selected_id_2.setMaximumSize(QSize(160, 26))
        self.label_selected_id_2.setFont(font1)
        self.label_selected_id_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id_2, 2, 1, 1, 1)

        self.label_selected_id_3 = QLabel(self.frame_selection)
        self.label_selected_id_3.setObjectName(u"label_selected_id_3")
        self.label_selected_id_3.setMinimumSize(QSize(100, 26))
        self.label_selected_id_3.setMaximumSize(QSize(160, 26))
        self.label_selected_id_3.setFont(font1)
        self.label_selected_id_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_selected_id_3, 1, 1, 1, 1)

        self.lineEdit_connection_type = QLineEdit(self.frame_selection)
        self.lineEdit_connection_type.setObjectName(u"lineEdit_connection_type")
        self.lineEdit_connection_type.setEnabled(True)
        self.lineEdit_connection_type.setMinimumSize(QSize(0, 26))
        self.lineEdit_connection_type.setMaximumSize(QSize(240, 26))
        self.lineEdit_connection_type.setFont(font1)
        self.lineEdit_connection_type.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_connection_type.setStyleSheet(u"")
        self.lineEdit_connection_type.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_connection_type, 1, 2, 1, 1)

        self.pushButton_reset_selection = QPushButton(self.frame_selection)
        self.pushButton_reset_selection.setObjectName(u"pushButton_reset_selection")
        icon = QIcon()
        icon.addFile(u":/icons/common/broom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_reset_selection.setIcon(icon)

        self.gridLayout_6.addWidget(self.pushButton_reset_selection, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.treeWidget_reciprocating_machine_data = QTreeWidget(self.frame)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_reciprocating_machine_data.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_reciprocating_machine_data.setObjectName(u"treeWidget_reciprocating_machine_data")
        self.treeWidget_reciprocating_machine_data.setMinimumSize(QSize(0, 0))
        self.treeWidget_reciprocating_machine_data.setMaximumSize(QSize(1000, 1000))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        self.treeWidget_reciprocating_machine_data.setFont(font2)
        self.treeWidget_reciprocating_machine_data.setAlternatingRowColors(True)
        self.treeWidget_reciprocating_machine_data.setIndentation(0)

        self.gridLayout_4.addWidget(self.treeWidget_reciprocating_machine_data, 1, 0, 1, 1)

        self.frame_button = QFrame(self.frame)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(16777215, 48))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_button)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_select = QPushButton(self.frame_button)
        self.pushButton_select.setObjectName(u"pushButton_select")
        self.pushButton_select.setMinimumSize(QSize(100, 28))
        self.pushButton_select.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_select.setFont(font3)
        self.pushButton_select.setStyleSheet(u"")
        self.pushButton_select.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_select, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_button)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_button, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.pushButton_select.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Select the reciprocating machine", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Node ID:", None))
        self.lineEdit_selected_id.setText("")
        self.label_volume_rate_unit.setText(QCoreApplication.translate("Dialog", u"[m\u00b3/s]", None))
        self.lineEdit_volumetric_flow_rate.setText("")
        self.label_selected_id_2.setText(QCoreApplication.translate("Dialog", u"Volumetric flow rate:", None))
        self.label_selected_id_3.setText(QCoreApplication.translate("Dialog", u"Connection type:", None))
        self.lineEdit_connection_type.setText("")
        self.pushButton_reset_selection.setText("")
        ___qtreewidgetitem = self.treeWidget_reciprocating_machine_data.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Volumetric flow rate [m\u00b3/s]", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Connection type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Node ID", None))
        self.pushButton_select.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class ReciprocatingPumpSelector_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_selection: QFrame
                                - (Layout): QGridLayout
                                        - label_selected_id: QLabel
                                        - lineEdit_selected_id: QLineEdit
                                        - label_volume_rate_unit: QLabel
                                        - lineEdit_volumetric_flow_rate: QLineEdit
                                        - label_selected_id_2: QLabel
                                        - label_selected_id_3: QLabel
                                        - lineEdit_connection_type: QLineEdit
                                        - pushButton_reset_selection: QPushButton
                            - treeWidget_reciprocating_machine_data: QTreeWidget
                            - frame_button: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_select: QPushButton
                                        - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
