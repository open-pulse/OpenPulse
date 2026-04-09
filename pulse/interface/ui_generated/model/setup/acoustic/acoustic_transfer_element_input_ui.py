# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_transfer_element_input.ui'
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
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(400, 360)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(400, 280))
        Dialog.setMaximumSize(QSize(400, 360))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(520, 48))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(520, 460))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        font1 = QFont()
        font1.setPointSize(10)
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout = QGridLayout(self.tab_setup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_9 = QFrame(self.tab_setup)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(260, 52))
        self.frame_9.setMaximumSize(QSize(16777215, 52))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(4)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(0, 4, 0, 0)
        self.pushButton_search = QPushButton(self.frame_9)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_search.sizePolicy().hasHeightForWidth())
        self.pushButton_search.setSizePolicy(sizePolicy1)
        self.pushButton_search.setMinimumSize(QSize(40, 30))
        self.pushButton_search.setMaximumSize(QSize(40, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_search.setFont(font2)
        self.pushButton_search.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setIconSize(QSize(20, 20))

        self.gridLayout_5.addWidget(self.pushButton_search, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.lineEdit_spreadsheet_path = QLineEdit(self.frame_9)
        self.lineEdit_spreadsheet_path.setObjectName(u"lineEdit_spreadsheet_path")
        self.lineEdit_spreadsheet_path.setEnabled(False)
        self.lineEdit_spreadsheet_path.setMinimumSize(QSize(280, 30))
        self.lineEdit_spreadsheet_path.setMaximumSize(QSize(280, 30))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        self.lineEdit_spreadsheet_path.setFont(font3)
        self.lineEdit_spreadsheet_path.setStyleSheet(u"")
        self.lineEdit_spreadsheet_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_spreadsheet_path, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_9, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.tab_setup)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 52))
        self.frame_5.setMaximumSize(QSize(16777215, 180))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.comboBox_data_type = QComboBox(self.frame_5)
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.addItem("")
        self.comboBox_data_type.setObjectName(u"comboBox_data_type")
        self.comboBox_data_type.setMinimumSize(QSize(120, 30))
        self.comboBox_data_type.setMaximumSize(QSize(150, 30))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.comboBox_data_type.setFont(font4)
        self.comboBox_data_type.setStyleSheet(u"")

        self.gridLayout_6.addWidget(self.comboBox_data_type, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 30))
        self.label_2.setMaximumSize(QSize(120, 30))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)

        self.label_15 = QLabel(self.frame_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(100, 30))
        self.label_15.setMaximumSize(QSize(120, 30))
        self.label_15.setFont(font2)
        self.label_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_15, 2, 1, 1, 1)

        self.pushButton_invert_selection = QPushButton(self.frame_5)
        self.pushButton_invert_selection.setObjectName(u"pushButton_invert_selection")
        self.pushButton_invert_selection.setMinimumSize(QSize(40, 30))
        self.pushButton_invert_selection.setMaximumSize(QSize(40, 30))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(True)
        font5.setItalic(False)
        self.pushButton_invert_selection.setFont(font5)
        self.pushButton_invert_selection.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/common/swap_horizontal_arrows.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_invert_selection.setIcon(icon1)
        self.pushButton_invert_selection.setIconSize(QSize(20, 20))
        self.pushButton_invert_selection.setFlat(False)

        self.gridLayout_6.addWidget(self.pushButton_invert_selection, 2, 3, 1, 1)

        self.lineEdit_input_node_id = QLineEdit(self.frame_5)
        self.lineEdit_input_node_id.setObjectName(u"lineEdit_input_node_id")
        self.lineEdit_input_node_id.setMinimumSize(QSize(120, 30))
        self.lineEdit_input_node_id.setMaximumSize(QSize(150, 30))
        self.lineEdit_input_node_id.setFont(font4)
        self.lineEdit_input_node_id.setStyleSheet(u"")
        self.lineEdit_input_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_input_node_id, 2, 2, 1, 1)

        self.frame_6 = QFrame(self.frame_5)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(40, 30))
        self.frame_6.setMaximumSize(QSize(40, 30))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_6.addWidget(self.frame_6, 0, 3, 1, 1)

        self.lineEdit_output_node_id = QLineEdit(self.frame_5)
        self.lineEdit_output_node_id.setObjectName(u"lineEdit_output_node_id")
        self.lineEdit_output_node_id.setMinimumSize(QSize(120, 30))
        self.lineEdit_output_node_id.setMaximumSize(QSize(150, 30))
        self.lineEdit_output_node_id.setFont(font1)
        self.lineEdit_output_node_id.setStyleSheet(u"")
        self.lineEdit_output_node_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_output_node_id, 3, 2, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(100, 30))
        self.label_10.setMaximumSize(QSize(120, 30))
        self.label_10.setFont(font2)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_10, 3, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_setup)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_47 = QGridLayout(self.frame_3)
        self.gridLayout_47.setSpacing(4)
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_3)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 30))
        self.pushButton_attribute.setMaximumSize(QSize(100, 30))
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setFlat(False)

        self.gridLayout_47.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_7 = QGridLayout(self.tab_remove)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.frame_selection_id = QFrame(self.tab_remove)
        self.frame_selection_id.setObjectName(u"frame_selection_id")
        self.frame_selection_id.setMinimumSize(QSize(360, 40))
        self.frame_selection_id.setMaximumSize(QSize(380, 40))
        self.frame_selection_id.setFrameShape(QFrame.NoFrame)
        self.frame_selection_id.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_selection_id)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(8)
        self.gridLayout_8.setVerticalSpacing(2)
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.frame_selection_id)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(160, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(160, 26))
        self.lineEdit_selected_id.setFont(font2)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_selection_id)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(80, 26))
        self.label_3.setMaximumSize(QSize(100, 26))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_7.addWidget(self.frame_selection_id, 0, 0, 1, 1)

        self.treeWidget_nodal_info = QTreeWidget(self.tab_remove)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_nodal_info.setObjectName(u"treeWidget_nodal_info")
        self.treeWidget_nodal_info.setMinimumSize(QSize(320, 0))
        self.treeWidget_nodal_info.setMaximumSize(QSize(600, 200))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setItalic(False)
        self.treeWidget_nodal_info.setFont(font6)
        self.treeWidget_nodal_info.setIndentation(1)
        self.treeWidget_nodal_info.setHeaderHidden(False)
        self.treeWidget_nodal_info.header().setHighlightSections(False)
        self.treeWidget_nodal_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_nodal_info.header().setStretchLastSection(True)

        self.gridLayout_7.addWidget(self.treeWidget_nodal_info, 1, 0, 1, 1)

        self.frame_buttons_remove = QFrame(self.tab_remove)
        self.frame_buttons_remove.setObjectName(u"frame_buttons_remove")
        self.frame_buttons_remove.setMinimumSize(QSize(320, 48))
        self.frame_buttons_remove.setMaximumSize(QSize(1000, 48))
        self.frame_buttons_remove.setFrameShape(QFrame.NoFrame)
        self.frame_buttons_remove.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_buttons_remove)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.pushButton_reset = QPushButton(self.frame_buttons_remove)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 30))
        self.pushButton_reset.setMaximumSize(QSize(100, 30))
        self.pushButton_reset.setFont(font2)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_reset, 0, 0, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_buttons_remove)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 30))
        self.pushButton_remove.setMaximumSize(QSize(100, 30))
        self.pushButton_remove.setFont(font2)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_9.addWidget(self.pushButton_remove, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_buttons_remove, 2, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_3.addWidget(self.tabWidget_main, 2, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.comboBox_data_type.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Plot frequency response", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Acoustic transfer element setup", None))
#if QT_CONFIG(tooltip)
        self.pushButton_search.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select the spreadsheet fle to import the acoustic transfer element data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_search.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_spreadsheet_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select the spreadsheet fle to import the acoustic transfer element data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_data_type.setItemText(0, QCoreApplication.translate("Dialog", u" Transfer functions", None))
        self.comboBox_data_type.setItemText(1, QCoreApplication.translate("Dialog", u" Admittance matrix", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Data type:", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Input node ID:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:400;\">Press to invert the selected IDs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert_selection.setText("")
        self.lineEdit_input_node_id.setText("")
        self.lineEdit_output_node_id.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Output node ID:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Output Node ID", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Input Node ID", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"ID", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_nodal_info.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
    # retranslateUi



class AcousticTransferElementInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_9: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_search: QPushButton
                                                        - lineEdit_spreadsheet_path: QLineEdit
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_data_type: QComboBox
                                                        - label_2: QLabel
                                                        - label_15: QLabel
                                                        - pushButton_invert_selection: QPushButton
                                                        - lineEdit_input_node_id: QLineEdit
                                                        - frame_6: QFrame
                                                        - lineEdit_output_node_id: QLineEdit
                                                        - label_10: QLabel
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
                                - tab_remove: QWidget
                                    - (Layout): QGridLayout
                                            - frame_selection_id: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_id: QLineEdit
                                                        - label_3: QLabel
                                            - treeWidget_nodal_info: QTreeWidget
                                            - frame_buttons_remove: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
