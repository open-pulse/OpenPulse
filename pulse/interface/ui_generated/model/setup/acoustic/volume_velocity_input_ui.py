# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'volume_velocity_input.ui'
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
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(460, 360)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(460, 360))
        Dialog.setMaximumSize(QSize(460, 360))
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
        self.frame_title.setMaximumSize(QSize(16777215, 48))
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
        self.frame_main.setMaximumSize(QSize(16777215, 480))
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
        self.tabWidget_main.setMaximumSize(QSize(440, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.tabWidget_main.setFont(font3)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_12 = QGridLayout(self.tab_setup)
        self.gridLayout_12.setSpacing(2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(8, 8, 8, 4)
        self.tabWidget_inputs = QTabWidget(self.tab_setup)
        self.tabWidget_inputs.setObjectName(u"tabWidget_inputs")
        self.tabWidget_inputs.setFont(font3)
        self.tab_constant = QWidget()
        self.tab_constant.setObjectName(u"tab_constant")
        self.gridLayout_15 = QGridLayout(self.tab_constant)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.lineEdit_real_value = QLineEdit(self.tab_constant)
        self.lineEdit_real_value.setObjectName(u"lineEdit_real_value")
        self.lineEdit_real_value.setMinimumSize(QSize(80, 30))
        self.lineEdit_real_value.setMaximumSize(QSize(80, 30))
        self.lineEdit_real_value.setFont(font2)
        self.lineEdit_real_value.setStyleSheet(u"")
        self.lineEdit_real_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_real_value, 2, 2, 1, 1)

        self.label_4 = QLabel(self.tab_constant)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(80, 26))
        self.label_4.setMaximumSize(QSize(80, 26))
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_20 = QLabel(self.tab_constant)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(80, 26))
        self.label_20.setMaximumSize(QSize(80, 26))
        self.label_20.setFont(font2)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_20, 1, 3, 1, 1)

        self.label_18 = QLabel(self.tab_constant)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setMinimumSize(QSize(120, 30))
        self.label_18.setMaximumSize(QSize(120, 30))
        self.label_18.setFont(font2)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_18, 2, 1, 1, 1)

        self.lineEdit_imag_value = QLineEdit(self.tab_constant)
        self.lineEdit_imag_value.setObjectName(u"lineEdit_imag_value")
        self.lineEdit_imag_value.setMinimumSize(QSize(80, 30))
        self.lineEdit_imag_value.setMaximumSize(QSize(80, 30))
        self.lineEdit_imag_value.setFont(font2)
        self.lineEdit_imag_value.setStyleSheet(u"")
        self.lineEdit_imag_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_imag_value, 2, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_8, 2, 5, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_7, 2, 0, 1, 1)

        self.label_21 = QLabel(self.tab_constant)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(0, 30))
        self.label_21.setMaximumSize(QSize(100, 30))
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_21, 2, 4, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer, 3, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer_2, 0, 2, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_constant, "")
        self.tab_values = QWidget()
        self.tab_values.setObjectName(u"tab_values")
        self.gridLayout = QGridLayout(self.tab_values)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(self.tab_values)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.pushButton_search = QPushButton(self.frame)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_search.sizePolicy().hasHeightForWidth())
        self.pushButton_search.setSizePolicy(sizePolicy1)
        self.pushButton_search.setMinimumSize(QSize(62, 26))
        self.pushButton_search.setMaximumSize(QSize(62, 26))
        self.pushButton_search.setFont(font2)
        self.pushButton_search.setStyleSheet(u"")
        self.pushButton_search.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.pushButton_search, 0, 2, 1, 1)

        self.lineEdit_table_path = QLineEdit(self.frame)
        self.lineEdit_table_path.setObjectName(u"lineEdit_table_path")
        self.lineEdit_table_path.setEnabled(True)
        self.lineEdit_table_path.setMinimumSize(QSize(280, 26))
        self.lineEdit_table_path.setMaximumSize(QSize(280, 26))
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(False)
        self.lineEdit_table_path.setFont(font4)
        self.lineEdit_table_path.setStyleSheet(u"")
        self.lineEdit_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_table_path.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.lineEdit_table_path, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_values, "")

        self.gridLayout_12.addWidget(self.tabWidget_inputs, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.tab_setup)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 48))
        self.frame_7.setMaximumSize(QSize(16777215, 80))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_7)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_7)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font2)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_7)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_7, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_9 = QGridLayout(self.tab_remove)
        self.gridLayout_9.setSpacing(2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(8, 8, 8, 4)
        self.frame_buttons_remove = QFrame(self.tab_remove)
        self.frame_buttons_remove.setObjectName(u"frame_buttons_remove")
        self.frame_buttons_remove.setMinimumSize(QSize(320, 48))
        self.frame_buttons_remove.setMaximumSize(QSize(1000, 48))
        self.frame_buttons_remove.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons_remove.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_buttons_remove)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(4)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
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

        QWidget.setTabOrder(self.tabWidget_main, self.tabWidget_inputs)
        QWidget.setTabOrder(self.tabWidget_inputs, self.lineEdit_real_value)
        QWidget.setTabOrder(self.lineEdit_real_value, self.lineEdit_imag_value)
        QWidget.setTabOrder(self.lineEdit_imag_value, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.lineEdit_table_path)
        QWidget.setTabOrder(self.lineEdit_table_path, self.pushButton_search)
        QWidget.setTabOrder(self.pushButton_search, self.treeWidget_nodal_info)
        QWidget.setTabOrder(self.treeWidget_nodal_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_inputs.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)
        self.pushButton_reset.setDefault(False)
        self.pushButton_remove.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Prescribe an acoustic pressure", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Volume velocity setup", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Node ID:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Volume velocity:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[m\u00b3/s]", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_constant), QCoreApplication.translate("Dialog", u"Constant values", None))
        self.pushButton_search.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_values), QCoreApplication.translate("Dialog", u"Load table", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        ___qtreewidgetitem = self.treeWidget_nodal_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Assignment type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Nodes", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_nodal_info.setToolTip(QCoreApplication.translate("Dialog", u"Select a face to remove the previously attributed boundary condition.", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"List", None))
    # retranslateUi



class VolumeVelocityInput_UI(QDialog, Ui_Dialog):
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
                                            - tabWidget_inputs: QTabWidget
                                                - tab_constant: QWidget
                                                    - (Layout): QGridLayout
                                                            - lineEdit_real_value: QLineEdit
                                                            - label_4: QLabel
                                                            - label_20: QLabel
                                                            - label_18: QLabel
                                                            - lineEdit_imag_value: QLineEdit
                                                            - label_21: QLabel
                                                - tab_values: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame: QFrame
                                                                - (Layout): QGridLayout
                                                                        - pushButton_search: QPushButton
                                                                        - lineEdit_table_path: QLineEdit
                                            - frame_7: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
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
