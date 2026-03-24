# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connecting_flanges_input.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(756, 605)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(1600, 48))
        self.top_frame.setFrameShape(QFrame.Box)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.top_frame)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        self.main_frame = QFrame(Dialog)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1600, 1600))
        self.main_frame.setFrameShape(QFrame.Box)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.main_frame)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.selection_frame = QFrame(self.main_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 100))
        self.selection_frame.setMaximumSize(QSize(16777215, 140))
        self.selection_frame.setFrameShape(QFrame.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_30 = QGridLayout(self.selection_frame)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setHorizontalSpacing(6)
        self.gridLayout_30.setVerticalSpacing(4)
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(90, 28))
        self.label_selected_id.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label_selected_id.setFont(font1)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_30.addWidget(self.label_selected_id, 1, 1, 1, 1)

        self.label_attribute_to = QLabel(self.selection_frame)
        self.label_attribute_to.setObjectName(u"label_attribute_to")
        self.label_attribute_to.setMinimumSize(QSize(90, 28))
        self.label_attribute_to.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_attribute_to.setFont(font2)
        self.label_attribute_to.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_30.addWidget(self.label_attribute_to, 0, 1, 1, 1)

        self.comboBox_selection_type = QComboBox(self.selection_frame)
        self.comboBox_selection_type.addItem("")
        self.comboBox_selection_type.addItem("")
        self.comboBox_selection_type.addItem("")
        self.comboBox_selection_type.setObjectName(u"comboBox_selection_type")
        self.comboBox_selection_type.setMinimumSize(QSize(132, 28))
        self.comboBox_selection_type.setMaximumSize(QSize(132, 28))
        self.comboBox_selection_type.setFont(font2)

        self.gridLayout_30.addWidget(self.comboBox_selection_type, 0, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_7, 1, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(132, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(132, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setKerning(False)
        self.lineEdit_selected_id.setFont(font3)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_30.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.selection_frame, 0, 1, 2, 1)

        self.frame_tabWidgets = QFrame(self.main_frame)
        self.frame_tabWidgets.setObjectName(u"frame_tabWidgets")
        self.frame_tabWidgets.setMinimumSize(QSize(400, 300))
        self.frame_tabWidgets.setFrameShape(QFrame.NoFrame)
        self.frame_tabWidgets.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_tabWidgets)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 4, 8, 4)
        self.tabWidget_inputs = QTabWidget(self.frame_tabWidgets)
        self.tabWidget_inputs.setObjectName(u"tabWidget_inputs")
        self.tabWidget_inputs.setEnabled(True)
        self.tabWidget_inputs.setMinimumSize(QSize(440, 300))
        self.tabWidget_inputs.setMaximumSize(QSize(440, 300))
        self.tabWidget_inputs.setFont(font2)
        self.tabWidget_inputs.setTabShape(QTabWidget.Rounded)
        self.tabWidget_inputs.setDocumentMode(False)
        self.tabWidget_inputs.setTabsClosable(False)
        self.tabWidget_inputs.setMovable(False)
        self.tabWidget_inputs.setTabBarAutoHide(False)
        self.tab_lines = QWidget()
        self.tab_lines.setObjectName(u"tab_lines")
        self.tab_lines.setEnabled(True)
        self.gridLayout_2 = QGridLayout(self.tab_lines)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.tab_lines)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_selected_id_13 = QLabel(self.frame_6)
        self.label_selected_id_13.setObjectName(u"label_selected_id_13")
        self.label_selected_id_13.setEnabled(True)
        self.label_selected_id_13.setMinimumSize(QSize(120, 26))
        self.label_selected_id_13.setMaximumSize(QSize(180, 26))
        self.label_selected_id_13.setFont(font2)
        self.label_selected_id_13.setMouseTracking(True)
        self.label_selected_id_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selected_id_13, 4, 1, 1, 1)

        self.lineEdit_last_node = QLineEdit(self.frame_6)
        self.lineEdit_last_node.setObjectName(u"lineEdit_last_node")
        self.lineEdit_last_node.setEnabled(False)
        self.lineEdit_last_node.setMinimumSize(QSize(110, 26))
        self.lineEdit_last_node.setMaximumSize(QSize(110, 26))
        self.lineEdit_last_node.setSizeIncrement(QSize(0, 26))
        self.lineEdit_last_node.setFont(font2)
        self.lineEdit_last_node.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_last_node.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_last_node.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_last_node, 1, 2, 1, 1)

        self.lineEdit_element_size_line = QLineEdit(self.frame_6)
        self.lineEdit_element_size_line.setObjectName(u"lineEdit_element_size_line")
        self.lineEdit_element_size_line.setEnabled(False)
        self.lineEdit_element_size_line.setMinimumSize(QSize(110, 26))
        self.lineEdit_element_size_line.setMaximumSize(QSize(110, 26))
        self.lineEdit_element_size_line.setSizeIncrement(QSize(0, 26))
        self.lineEdit_element_size_line.setFont(font2)
        self.lineEdit_element_size_line.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_element_size_line.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_element_size_line.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_element_size_line, 4, 2, 1, 1)

        self.label_110 = QLabel(self.frame_6)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setEnabled(True)
        self.label_110.setMinimumSize(QSize(40, 30))
        self.label_110.setMaximumSize(QSize(40, 30))
        self.label_110.setFont(font2)
        self.label_110.setMouseTracking(True)
        self.label_110.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_110, 4, 3, 1, 1)

        self.label_selected_id_9 = QLabel(self.frame_6)
        self.label_selected_id_9.setObjectName(u"label_selected_id_9")
        self.label_selected_id_9.setEnabled(True)
        self.label_selected_id_9.setMinimumSize(QSize(120, 26))
        self.label_selected_id_9.setMaximumSize(QSize(180, 26))
        self.label_selected_id_9.setFont(font2)
        self.label_selected_id_9.setMouseTracking(True)
        self.label_selected_id_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selected_id_9, 5, 1, 1, 1)

        self.label_first_node_3 = QLabel(self.frame_6)
        self.label_first_node_3.setObjectName(u"label_first_node_3")
        self.label_first_node_3.setEnabled(True)
        self.label_first_node_3.setMinimumSize(QSize(120, 26))
        self.label_first_node_3.setMaximumSize(QSize(180, 26))
        self.label_first_node_3.setFont(font2)
        self.label_first_node_3.setMouseTracking(True)
        self.label_first_node_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_first_node_3, 2, 1, 1, 1)

        self.lineEdit_first_node = QLineEdit(self.frame_6)
        self.lineEdit_first_node.setObjectName(u"lineEdit_first_node")
        self.lineEdit_first_node.setEnabled(False)
        self.lineEdit_first_node.setMinimumSize(QSize(110, 26))
        self.lineEdit_first_node.setMaximumSize(QSize(110, 26))
        self.lineEdit_first_node.setSizeIncrement(QSize(0, 26))
        self.lineEdit_first_node.setFont(font2)
        self.lineEdit_first_node.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_first_node.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_first_node.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_first_node, 0, 2, 1, 1)

        self.label_number_elements = QLabel(self.frame_6)
        self.label_number_elements.setObjectName(u"label_number_elements")
        self.label_number_elements.setEnabled(True)
        self.label_number_elements.setMinimumSize(QSize(120, 26))
        self.label_number_elements.setMaximumSize(QSize(180, 26))
        self.label_number_elements.setFont(font2)
        self.label_number_elements.setMouseTracking(True)
        self.label_number_elements.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_number_elements, 3, 1, 1, 1)

        self.lineEdit_flange_length_line = QLineEdit(self.frame_6)
        self.lineEdit_flange_length_line.setObjectName(u"lineEdit_flange_length_line")
        self.lineEdit_flange_length_line.setEnabled(False)
        self.lineEdit_flange_length_line.setMinimumSize(QSize(110, 26))
        self.lineEdit_flange_length_line.setMaximumSize(QSize(110, 26))
        self.lineEdit_flange_length_line.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_length_line.setFont(font2)
        self.lineEdit_flange_length_line.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_flange_length_line.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_flange_length_line.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_flange_length_line, 5, 2, 1, 1)

        self.comboBox_ending_setup = QComboBox(self.frame_6)
        self.comboBox_ending_setup.addItem("")
        self.comboBox_ending_setup.addItem("")
        self.comboBox_ending_setup.addItem("")
        self.comboBox_ending_setup.setObjectName(u"comboBox_ending_setup")
        self.comboBox_ending_setup.setMinimumSize(QSize(110, 26))
        self.comboBox_ending_setup.setMaximumSize(QSize(110, 26))
        self.comboBox_ending_setup.setFont(font2)

        self.gridLayout_8.addWidget(self.comboBox_ending_setup, 2, 2, 1, 1)

        self.label_first_node = QLabel(self.frame_6)
        self.label_first_node.setObjectName(u"label_first_node")
        self.label_first_node.setEnabled(True)
        self.label_first_node.setMinimumSize(QSize(120, 26))
        self.label_first_node.setMaximumSize(QSize(180, 26))
        self.label_first_node.setFont(font2)
        self.label_first_node.setMouseTracking(True)
        self.label_first_node.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_first_node, 0, 1, 1, 1)

        self.label_first_node_2 = QLabel(self.frame_6)
        self.label_first_node_2.setObjectName(u"label_first_node_2")
        self.label_first_node_2.setEnabled(True)
        self.label_first_node_2.setMinimumSize(QSize(120, 26))
        self.label_first_node_2.setMaximumSize(QSize(180, 26))
        self.label_first_node_2.setFont(font2)
        self.label_first_node_2.setMouseTracking(True)
        self.label_first_node_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_first_node_2, 1, 1, 1, 1)

        self.spinBox_number_elements_line = QSpinBox(self.frame_6)
        self.spinBox_number_elements_line.setObjectName(u"spinBox_number_elements_line")
        self.spinBox_number_elements_line.setMinimumSize(QSize(110, 26))
        self.spinBox_number_elements_line.setMaximumSize(QSize(110, 26))
        self.spinBox_number_elements_line.setFont(font2)
        self.spinBox_number_elements_line.setAlignment(Qt.AlignCenter)
        self.spinBox_number_elements_line.setMinimum(1)
        self.spinBox_number_elements_line.setValue(2)

        self.gridLayout_8.addWidget(self.spinBox_number_elements_line, 3, 2, 1, 1)

        self.lineEdit_outer_diameter_line = QLineEdit(self.frame_6)
        self.lineEdit_outer_diameter_line.setObjectName(u"lineEdit_outer_diameter_line")
        self.lineEdit_outer_diameter_line.setEnabled(True)
        self.lineEdit_outer_diameter_line.setMinimumSize(QSize(110, 26))
        self.lineEdit_outer_diameter_line.setMaximumSize(QSize(110, 26))
        self.lineEdit_outer_diameter_line.setSizeIncrement(QSize(0, 26))
        self.lineEdit_outer_diameter_line.setFont(font2)
        self.lineEdit_outer_diameter_line.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_outer_diameter_line.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_outer_diameter_line.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_outer_diameter_line, 6, 2, 1, 1)

        self.label_selected_id_14 = QLabel(self.frame_6)
        self.label_selected_id_14.setObjectName(u"label_selected_id_14")
        self.label_selected_id_14.setEnabled(True)
        self.label_selected_id_14.setMinimumSize(QSize(120, 26))
        self.label_selected_id_14.setMaximumSize(QSize(180, 26))
        self.label_selected_id_14.setFont(font2)
        self.label_selected_id_14.setMouseTracking(True)
        self.label_selected_id_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_selected_id_14, 6, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_3, 4, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 4, 4, 1, 1)

        self.label_111 = QLabel(self.frame_6)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setEnabled(True)
        self.label_111.setMinimumSize(QSize(40, 30))
        self.label_111.setMaximumSize(QSize(40, 30))
        self.label_111.setFont(font2)
        self.label_111.setMouseTracking(True)
        self.label_111.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_111, 5, 3, 1, 1)

        self.label_112 = QLabel(self.frame_6)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(40, 30))
        self.label_112.setMaximumSize(QSize(40, 30))
        self.label_112.setFont(font2)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_112, 6, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_6, 4, 0, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_lines, "")
        self.tab_nodes = QWidget()
        self.tab_nodes.setObjectName(u"tab_nodes")
        self.gridLayout_13 = QGridLayout(self.tab_nodes)
        self.gridLayout_13.setSpacing(4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(4, 4, 4, 4)
        self.frame_7 = QFrame(self.tab_nodes)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_7)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_selected_id_10 = QLabel(self.frame_7)
        self.label_selected_id_10.setObjectName(u"label_selected_id_10")
        self.label_selected_id_10.setEnabled(True)
        self.label_selected_id_10.setMinimumSize(QSize(120, 26))
        self.label_selected_id_10.setMaximumSize(QSize(180, 26))
        self.label_selected_id_10.setFont(font2)
        self.label_selected_id_10.setMouseTracking(True)
        self.label_selected_id_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_selected_id_10, 0, 1, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 1, 0, 1, 1)

        self.spinBox_number_elements_node = QSpinBox(self.frame_7)
        self.spinBox_number_elements_node.setObjectName(u"spinBox_number_elements_node")
        self.spinBox_number_elements_node.setMinimumSize(QSize(100, 30))
        self.spinBox_number_elements_node.setMaximumSize(QSize(100, 30))
        self.spinBox_number_elements_node.setFont(font2)
        self.spinBox_number_elements_node.setAlignment(Qt.AlignCenter)
        self.spinBox_number_elements_node.setMinimum(1)
        self.spinBox_number_elements_node.setValue(2)

        self.gridLayout_14.addWidget(self.spinBox_number_elements_node, 0, 2, 1, 1)

        self.label_selected_id_12 = QLabel(self.frame_7)
        self.label_selected_id_12.setObjectName(u"label_selected_id_12")
        self.label_selected_id_12.setEnabled(True)
        self.label_selected_id_12.setMinimumSize(QSize(120, 30))
        self.label_selected_id_12.setMaximumSize(QSize(180, 30))
        self.label_selected_id_12.setFont(font2)
        self.label_selected_id_12.setMouseTracking(True)
        self.label_selected_id_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_selected_id_12, 2, 1, 1, 1)

        self.label_selected_id_11 = QLabel(self.frame_7)
        self.label_selected_id_11.setObjectName(u"label_selected_id_11")
        self.label_selected_id_11.setEnabled(True)
        self.label_selected_id_11.setMinimumSize(QSize(120, 30))
        self.label_selected_id_11.setMaximumSize(QSize(180, 30))
        self.label_selected_id_11.setFont(font2)
        self.label_selected_id_11.setMouseTracking(True)
        self.label_selected_id_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_selected_id_11, 1, 1, 1, 1)

        self.lineEdit_element_size_node = QLineEdit(self.frame_7)
        self.lineEdit_element_size_node.setObjectName(u"lineEdit_element_size_node")
        self.lineEdit_element_size_node.setEnabled(False)
        self.lineEdit_element_size_node.setMinimumSize(QSize(100, 30))
        self.lineEdit_element_size_node.setMaximumSize(QSize(100, 30))
        self.lineEdit_element_size_node.setSizeIncrement(QSize(0, 26))
        self.lineEdit_element_size_node.setFont(font2)
        self.lineEdit_element_size_node.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_element_size_node.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_element_size_node.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_element_size_node, 1, 2, 1, 1)

        self.label_selected_id_7 = QLabel(self.frame_7)
        self.label_selected_id_7.setObjectName(u"label_selected_id_7")
        self.label_selected_id_7.setEnabled(True)
        self.label_selected_id_7.setMinimumSize(QSize(120, 30))
        self.label_selected_id_7.setMaximumSize(QSize(180, 30))
        self.label_selected_id_7.setFont(font2)
        self.label_selected_id_7.setMouseTracking(True)
        self.label_selected_id_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_selected_id_7, 3, 1, 1, 1)

        self.lineEdit_outer_diameter_node = QLineEdit(self.frame_7)
        self.lineEdit_outer_diameter_node.setObjectName(u"lineEdit_outer_diameter_node")
        self.lineEdit_outer_diameter_node.setEnabled(True)
        self.lineEdit_outer_diameter_node.setMinimumSize(QSize(100, 30))
        self.lineEdit_outer_diameter_node.setMaximumSize(QSize(100, 30))
        self.lineEdit_outer_diameter_node.setSizeIncrement(QSize(0, 26))
        self.lineEdit_outer_diameter_node.setFont(font2)
        self.lineEdit_outer_diameter_node.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_outer_diameter_node.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_outer_diameter_node.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_outer_diameter_node, 3, 2, 1, 1)

        self.lineEdit_flange_length_node = QLineEdit(self.frame_7)
        self.lineEdit_flange_length_node.setObjectName(u"lineEdit_flange_length_node")
        self.lineEdit_flange_length_node.setEnabled(False)
        self.lineEdit_flange_length_node.setMinimumSize(QSize(100, 30))
        self.lineEdit_flange_length_node.setMaximumSize(QSize(100, 30))
        self.lineEdit_flange_length_node.setSizeIncrement(QSize(0, 26))
        self.lineEdit_flange_length_node.setFont(font2)
        self.lineEdit_flange_length_node.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_flange_length_node.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_flange_length_node.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.lineEdit_flange_length_node, 2, 2, 1, 1)

        self.label_115 = QLabel(self.frame_7)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setEnabled(True)
        self.label_115.setMinimumSize(QSize(40, 30))
        self.label_115.setMaximumSize(QSize(40, 30))
        self.label_115.setFont(font2)
        self.label_115.setMouseTracking(True)
        self.label_115.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_115, 3, 3, 1, 1)

        self.label_113 = QLabel(self.frame_7)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setEnabled(True)
        self.label_113.setMinimumSize(QSize(40, 30))
        self.label_113.setMaximumSize(QSize(40, 30))
        self.label_113.setFont(font2)
        self.label_113.setMouseTracking(True)
        self.label_113.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_113, 1, 3, 1, 1)

        self.label_114 = QLabel(self.frame_7)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setEnabled(True)
        self.label_114.setMinimumSize(QSize(40, 30))
        self.label_114.setMaximumSize(QSize(40, 30))
        self.label_114.setFont(font2)
        self.label_114.setMouseTracking(True)
        self.label_114.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_114, 2, 3, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_12, 1, 4, 1, 1)


        self.gridLayout_13.addWidget(self.frame_7, 1, 5, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_nodes, "")
        self.tab_elements = QWidget()
        self.tab_elements.setObjectName(u"tab_elements")
        self.gridLayout_12 = QGridLayout(self.tab_elements)
        self.gridLayout_12.setSpacing(4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.frame_5 = QFrame(self.tab_elements)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.treeWidget_flange_by_elements = QTreeWidget(self.frame_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font2);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font2);
        self.treeWidget_flange_by_elements.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_flange_by_elements.setObjectName(u"treeWidget_flange_by_elements")
        self.treeWidget_flange_by_elements.setMinimumSize(QSize(320, 140))
        self.treeWidget_flange_by_elements.setMaximumSize(QSize(320, 140))

        self.gridLayout_11.addWidget(self.treeWidget_flange_by_elements, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_2 = QFrame(self.tab_elements)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 52))
        self.frame_2.setMaximumSize(QSize(16777215, 52))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(6)
        self.gridLayout_10.setVerticalSpacing(4)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.label_unit_outer_diameter_element = QLabel(self.frame_2)
        self.label_unit_outer_diameter_element.setObjectName(u"label_unit_outer_diameter_element")
        self.label_unit_outer_diameter_element.setEnabled(True)
        self.label_unit_outer_diameter_element.setMinimumSize(QSize(40, 30))
        self.label_unit_outer_diameter_element.setMaximumSize(QSize(40, 30))
        self.label_unit_outer_diameter_element.setFont(font2)
        self.label_unit_outer_diameter_element.setMouseTracking(True)
        self.label_unit_outer_diameter_element.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_unit_outer_diameter_element, 0, 3, 1, 1)

        self.label_outer_diameter_element = QLabel(self.frame_2)
        self.label_outer_diameter_element.setObjectName(u"label_outer_diameter_element")
        self.label_outer_diameter_element.setEnabled(True)
        self.label_outer_diameter_element.setMinimumSize(QSize(120, 30))
        self.label_outer_diameter_element.setMaximumSize(QSize(120, 30))
        self.label_outer_diameter_element.setFont(font2)
        self.label_outer_diameter_element.setMouseTracking(True)
        self.label_outer_diameter_element.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_outer_diameter_element, 0, 1, 1, 1)

        self.lineEdit_outer_diameter_element = QLineEdit(self.frame_2)
        self.lineEdit_outer_diameter_element.setObjectName(u"lineEdit_outer_diameter_element")
        self.lineEdit_outer_diameter_element.setEnabled(True)
        self.lineEdit_outer_diameter_element.setMinimumSize(QSize(100, 30))
        self.lineEdit_outer_diameter_element.setMaximumSize(QSize(100, 30))
        self.lineEdit_outer_diameter_element.setSizeIncrement(QSize(0, 26))
        self.lineEdit_outer_diameter_element.setFont(font2)
        self.lineEdit_outer_diameter_element.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_outer_diameter_element.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_outer_diameter_element.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_outer_diameter_element, 0, 2, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)


        self.gridLayout_12.addWidget(self.frame_2, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_elements, "")
        self.tab_section_parameters = QWidget()
        self.tab_section_parameters.setObjectName(u"tab_section_parameters")
        self.gridLayout_9 = QGridLayout(self.tab_section_parameters)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.tab_section_parameters)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.lineEdit_inner_diameter = QLineEdit(self.frame_8)
        self.lineEdit_inner_diameter.setObjectName(u"lineEdit_inner_diameter")
        self.lineEdit_inner_diameter.setEnabled(True)
        self.lineEdit_inner_diameter.setMinimumSize(QSize(100, 30))
        self.lineEdit_inner_diameter.setMaximumSize(QSize(100, 30))
        self.lineEdit_inner_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_inner_diameter.setFont(font2)
        self.lineEdit_inner_diameter.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_inner_diameter.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_inner_diameter.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_inner_diameter, 1, 2, 1, 1)

        self.label_offset_y = QLabel(self.frame_8)
        self.label_offset_y.setObjectName(u"label_offset_y")
        self.label_offset_y.setEnabled(True)
        self.label_offset_y.setMinimumSize(QSize(120, 30))
        self.label_offset_y.setMaximumSize(QSize(140, 30))
        self.label_offset_y.setFont(font2)
        self.label_offset_y.setMouseTracking(True)
        self.label_offset_y.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_offset_y, 2, 1, 1, 1)

        self.lineEdit_offset_y = QLineEdit(self.frame_8)
        self.lineEdit_offset_y.setObjectName(u"lineEdit_offset_y")
        self.lineEdit_offset_y.setEnabled(True)
        self.lineEdit_offset_y.setMinimumSize(QSize(100, 30))
        self.lineEdit_offset_y.setMaximumSize(QSize(100, 30))
        self.lineEdit_offset_y.setSizeIncrement(QSize(0, 26))
        self.lineEdit_offset_y.setFont(font2)
        self.lineEdit_offset_y.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_offset_y.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_offset_y.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_offset_y, 2, 2, 1, 1)

        self.label_offset_z = QLabel(self.frame_8)
        self.label_offset_z.setObjectName(u"label_offset_z")
        self.label_offset_z.setEnabled(True)
        self.label_offset_z.setMinimumSize(QSize(120, 30))
        self.label_offset_z.setMaximumSize(QSize(140, 30))
        self.label_offset_z.setFont(font2)
        self.label_offset_z.setMouseTracking(True)
        self.label_offset_z.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_offset_z, 3, 1, 1, 1)

        self.lineEdit_offset_z = QLineEdit(self.frame_8)
        self.lineEdit_offset_z.setObjectName(u"lineEdit_offset_z")
        self.lineEdit_offset_z.setEnabled(True)
        self.lineEdit_offset_z.setMinimumSize(QSize(100, 30))
        self.lineEdit_offset_z.setMaximumSize(QSize(100, 30))
        self.lineEdit_offset_z.setSizeIncrement(QSize(0, 26))
        self.lineEdit_offset_z.setFont(font2)
        self.lineEdit_offset_z.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_offset_z.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_offset_z.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_offset_z, 3, 2, 1, 1)

        self.label_130 = QLabel(self.frame_8)
        self.label_130.setObjectName(u"label_130")
        self.label_130.setEnabled(True)
        self.label_130.setMinimumSize(QSize(40, 30))
        self.label_130.setMaximumSize(QSize(100, 30))
        self.label_130.setFont(font2)
        self.label_130.setMouseTracking(True)
        self.label_130.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_130, 2, 3, 1, 1)

        self.label_129 = QLabel(self.frame_8)
        self.label_129.setObjectName(u"label_129")
        self.label_129.setEnabled(True)
        self.label_129.setMinimumSize(QSize(40, 30))
        self.label_129.setMaximumSize(QSize(100, 30))
        self.label_129.setFont(font2)
        self.label_129.setMouseTracking(True)
        self.label_129.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_129, 1, 3, 1, 1)

        self.label_132 = QLabel(self.frame_8)
        self.label_132.setObjectName(u"label_132")
        self.label_132.setEnabled(True)
        self.label_132.setMinimumSize(QSize(40, 30))
        self.label_132.setMaximumSize(QSize(100, 30))
        self.label_132.setFont(font2)
        self.label_132.setMouseTracking(True)
        self.label_132.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_132, 3, 3, 1, 1)

        self.label_inner_diameter = QLabel(self.frame_8)
        self.label_inner_diameter.setObjectName(u"label_inner_diameter")
        self.label_inner_diameter.setEnabled(True)
        self.label_inner_diameter.setMinimumSize(QSize(120, 30))
        self.label_inner_diameter.setMaximumSize(QSize(140, 30))
        self.label_inner_diameter.setFont(font2)
        self.label_inner_diameter.setMouseTracking(True)
        self.label_inner_diameter.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_inner_diameter, 1, 1, 1, 1)

        self.label_128 = QLabel(self.frame_8)
        self.label_128.setObjectName(u"label_128")
        self.label_128.setEnabled(True)
        self.label_128.setMinimumSize(QSize(40, 30))
        self.label_128.setMaximumSize(QSize(100, 30))
        self.label_128.setFont(font2)
        self.label_128.setMouseTracking(True)
        self.label_128.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_128, 0, 3, 1, 1)

        self.label_outer_diameter = QLabel(self.frame_8)
        self.label_outer_diameter.setObjectName(u"label_outer_diameter")
        self.label_outer_diameter.setEnabled(True)
        self.label_outer_diameter.setMinimumSize(QSize(120, 30))
        self.label_outer_diameter.setMaximumSize(QSize(140, 30))
        self.label_outer_diameter.setFont(font2)
        self.label_outer_diameter.setMouseTracking(True)
        self.label_outer_diameter.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_outer_diameter, 0, 1, 1, 1)

        self.lineEdit_outer_diameter = QLineEdit(self.frame_8)
        self.lineEdit_outer_diameter.setObjectName(u"lineEdit_outer_diameter")
        self.lineEdit_outer_diameter.setEnabled(True)
        self.lineEdit_outer_diameter.setMinimumSize(QSize(100, 30))
        self.lineEdit_outer_diameter.setMaximumSize(QSize(100, 30))
        self.lineEdit_outer_diameter.setSizeIncrement(QSize(0, 26))
        self.lineEdit_outer_diameter.setFont(font2)
        self.lineEdit_outer_diameter.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_outer_diameter.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_outer_diameter.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_outer_diameter, 0, 2, 1, 1)

        self.lineEdit_insulation_thickness = QLineEdit(self.frame_8)
        self.lineEdit_insulation_thickness.setObjectName(u"lineEdit_insulation_thickness")
        self.lineEdit_insulation_thickness.setEnabled(True)
        self.lineEdit_insulation_thickness.setMinimumSize(QSize(100, 30))
        self.lineEdit_insulation_thickness.setMaximumSize(QSize(100, 30))
        self.lineEdit_insulation_thickness.setSizeIncrement(QSize(0, 26))
        self.lineEdit_insulation_thickness.setFont(font2)
        self.lineEdit_insulation_thickness.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_insulation_thickness.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_insulation_thickness.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_insulation_thickness, 4, 2, 1, 1)

        self.label_133 = QLabel(self.frame_8)
        self.label_133.setObjectName(u"label_133")
        self.label_133.setEnabled(True)
        self.label_133.setMinimumSize(QSize(40, 30))
        self.label_133.setMaximumSize(QSize(100, 30))
        self.label_133.setFont(font2)
        self.label_133.setMouseTracking(True)
        self.label_133.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_133, 4, 3, 1, 1)

        self.label_131 = QLabel(self.frame_8)
        self.label_131.setObjectName(u"label_131")
        self.label_131.setEnabled(True)
        self.label_131.setMinimumSize(QSize(70, 30))
        self.label_131.setMaximumSize(QSize(100, 30))
        self.label_131.setFont(font2)
        self.label_131.setMouseTracking(True)
        self.label_131.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_131, 5, 3, 1, 1)

        self.lineEdit_insulation_density = QLineEdit(self.frame_8)
        self.lineEdit_insulation_density.setObjectName(u"lineEdit_insulation_density")
        self.lineEdit_insulation_density.setEnabled(True)
        self.lineEdit_insulation_density.setMinimumSize(QSize(100, 30))
        self.lineEdit_insulation_density.setMaximumSize(QSize(100, 30))
        self.lineEdit_insulation_density.setSizeIncrement(QSize(0, 26))
        self.lineEdit_insulation_density.setFont(font2)
        self.lineEdit_insulation_density.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_insulation_density.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_insulation_density.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_insulation_density, 5, 2, 1, 1)

        self.label_insulation_density = QLabel(self.frame_8)
        self.label_insulation_density.setObjectName(u"label_insulation_density")
        self.label_insulation_density.setEnabled(True)
        self.label_insulation_density.setMinimumSize(QSize(120, 30))
        self.label_insulation_density.setMaximumSize(QSize(140, 30))
        self.label_insulation_density.setFont(font2)
        self.label_insulation_density.setMouseTracking(True)
        self.label_insulation_density.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_insulation_density, 5, 1, 1, 1)

        self.label_insulationthickness = QLabel(self.frame_8)
        self.label_insulationthickness.setObjectName(u"label_insulationthickness")
        self.label_insulationthickness.setEnabled(True)
        self.label_insulationthickness.setMinimumSize(QSize(120, 30))
        self.label_insulationthickness.setMaximumSize(QSize(140, 30))
        self.label_insulationthickness.setFont(font2)
        self.label_insulationthickness.setMouseTracking(True)
        self.label_insulationthickness.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_insulationthickness, 4, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)


        self.gridLayout_9.addWidget(self.frame_8, 0, 5, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_section_parameters, "")

        self.gridLayout_4.addWidget(self.tabWidget_inputs, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_tabWidgets, 3, 0, 1, 2)

        self.frame_get_section = QFrame(self.main_frame)
        self.frame_get_section.setObjectName(u"frame_get_section")
        self.frame_get_section.setFrameShape(QFrame.NoFrame)
        self.frame_get_section.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_get_section)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.checkBox_get_cross_section = QCheckBox(self.frame_get_section)
        self.checkBox_get_cross_section.setObjectName(u"checkBox_get_cross_section")
        self.checkBox_get_cross_section.setFont(font2)
        self.checkBox_get_cross_section.setIconSize(QSize(16, 16))
        self.checkBox_get_cross_section.setChecked(True)
        self.checkBox_get_cross_section.setTristate(False)

        self.gridLayout_7.addWidget(self.checkBox_get_cross_section, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_get_section, 2, 0, 1, 2)


        self.gridLayout.addWidget(self.main_frame, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_confirm = QPushButton(self.frame_3)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(100, 28))
        self.pushButton_confirm.setMaximumSize(QSize(100, 28))
        self.pushButton_confirm.setFont(font2)
        self.pushButton_confirm.setStyleSheet(u"QPushButton{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}\n"
"QPushButton:hover{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}\n"
"QPushButton:pressed{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255)}\n"
"QPushButton:disabled{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(150,150, 150); background-color: rgb(220, 220, 220)}")
        self.pushButton_confirm.setAutoDefault(False)
        self.pushButton_confirm.setFlat(False)

        self.gridLayout_3.addWidget(self.pushButton_confirm, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_selection_type, self.checkBox_get_cross_section)
        QWidget.setTabOrder(self.checkBox_get_cross_section, self.tabWidget_inputs)
        QWidget.setTabOrder(self.tabWidget_inputs, self.comboBox_ending_setup)
        QWidget.setTabOrder(self.comboBox_ending_setup, self.spinBox_number_elements_line)
        QWidget.setTabOrder(self.spinBox_number_elements_line, self.pushButton_confirm)
        QWidget.setTabOrder(self.pushButton_confirm, self.spinBox_number_elements_node)
        QWidget.setTabOrder(self.spinBox_number_elements_node, self.treeWidget_flange_by_elements)

        self.retranslateUi(Dialog)

        self.tabWidget_inputs.setCurrentIndex(0)
        self.pushButton_confirm.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Connecting flanges configuration", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected id:", None))
        self.label_attribute_to.setText(QCoreApplication.translate("Dialog", u"Attribute by:", None))
        self.comboBox_selection_type.setItemText(0, QCoreApplication.translate("Dialog", u" Line selection", None))
        self.comboBox_selection_type.setItemText(1, QCoreApplication.translate("Dialog", u" Node selection", None))
        self.comboBox_selection_type.setItemText(2, QCoreApplication.translate("Dialog", u" Elements selection", None))

        self.label_selected_id_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Element size:</p></body></html>", None))
        self.label_110.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_selected_id_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Flange length:</p></body></html>", None))
        self.label_first_node_3.setText(QCoreApplication.translate("Dialog", u"Ending setup:", None))
        self.label_number_elements.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Number of elements:</p></body></html>", None))
        self.comboBox_ending_setup.setItemText(0, QCoreApplication.translate("Dialog", u" Both nodes", None))
        self.comboBox_ending_setup.setItemText(1, QCoreApplication.translate("Dialog", u" First node", None))
        self.comboBox_ending_setup.setItemText(2, QCoreApplication.translate("Dialog", u" Last node", None))

        self.label_first_node.setText(QCoreApplication.translate("Dialog", u"First node:", None))
        self.label_first_node_2.setText(QCoreApplication.translate("Dialog", u"Last node:", None))
        self.label_selected_id_14.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outer diameter:</p></body></html>", None))
        self.label_111.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_112.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_lines), QCoreApplication.translate("Dialog", u"Line selection", None))
        self.label_selected_id_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Number of elements:</p></body></html>", None))
        self.label_selected_id_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Flange length:</p></body></html>", None))
        self.label_selected_id_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Element size:</p></body></html>", None))
        self.label_selected_id_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outer diameter:</p></body></html>", None))
        self.label_115.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_113.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_114.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_nodes), QCoreApplication.translate("Dialog", u"Node selection", None))
        ___qtreewidgetitem = self.treeWidget_flange_by_elements.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Flange length [m]", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Line", None));
        self.label_unit_outer_diameter_element.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_outer_diameter_element.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outer diameter:</p></body></html>", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_elements), QCoreApplication.translate("Dialog", u"Element selection", None))
        self.label_offset_y.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Offset y:</p></body></html>", None))
        self.label_offset_z.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Offset z:</p></body></html>", None))
        self.label_130.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_129.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_132.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_inner_diameter.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Inner diameter:</p></body></html>", None))
        self.label_128.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_outer_diameter.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Outer diameter:</p></body></html>", None))
        self.label_133.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_131.setText(QCoreApplication.translate("Dialog", u"[kg/m\u00b3]", None))
        self.label_insulation_density.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Insulation density:</p></body></html>", None))
        self.label_insulationthickness.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">Insulation thickness:</p></body></html>", None))
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_section_parameters), QCoreApplication.translate("Dialog", u"Section parameters", None))
        self.checkBox_get_cross_section.setText(QCoreApplication.translate("Dialog", u"Get cross-section info from each element", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"Confirm", None))
    # retranslateUi



class ConnectingFlangesInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - main_frame: QFrame
                    - (Layout): QGridLayout
                            - selection_frame: QFrame
                                - (Layout): QGridLayout
                                        - label_selected_id: QLabel
                                        - label_attribute_to: QLabel
                                        - comboBox_selection_type: QComboBox
                                        - lineEdit_selected_id: QLineEdit
                            - frame_tabWidgets: QFrame
                                - (Layout): QGridLayout
                                        - tabWidget_inputs: QTabWidget
                                            - tab_lines: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_6: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_selected_id_13: QLabel
                                                                    - lineEdit_last_node: QLineEdit
                                                                    - lineEdit_element_size_line: QLineEdit
                                                                    - label_110: QLabel
                                                                    - label_selected_id_9: QLabel
                                                                    - label_first_node_3: QLabel
                                                                    - lineEdit_first_node: QLineEdit
                                                                    - label_number_elements: QLabel
                                                                    - lineEdit_flange_length_line: QLineEdit
                                                                    - comboBox_ending_setup: QComboBox
                                                                    - label_first_node: QLabel
                                                                    - label_first_node_2: QLabel
                                                                    - spinBox_number_elements_line: QSpinBox
                                                                    - lineEdit_outer_diameter_line: QLineEdit
                                                                    - label_selected_id_14: QLabel
                                                                    - label_111: QLabel
                                                                    - label_112: QLabel
                                            - tab_nodes: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_7: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_selected_id_10: QLabel
                                                                    - spinBox_number_elements_node: QSpinBox
                                                                    - label_selected_id_12: QLabel
                                                                    - label_selected_id_11: QLabel
                                                                    - lineEdit_element_size_node: QLineEdit
                                                                    - label_selected_id_7: QLabel
                                                                    - lineEdit_outer_diameter_node: QLineEdit
                                                                    - lineEdit_flange_length_node: QLineEdit
                                                                    - label_115: QLabel
                                                                    - label_113: QLabel
                                                                    - label_114: QLabel
                                            - tab_elements: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_5: QFrame
                                                            - (Layout): QGridLayout
                                                                    - treeWidget_flange_by_elements: QTreeWidget
                                                        - frame_2: QFrame
                                                            - (Layout): QGridLayout
                                                                    - label_unit_outer_diameter_element: QLabel
                                                                    - label_outer_diameter_element: QLabel
                                                                    - lineEdit_outer_diameter_element: QLineEdit
                                            - tab_section_parameters: QWidget
                                                - (Layout): QGridLayout
                                                        - frame_8: QFrame
                                                            - (Layout): QGridLayout
                                                                    - lineEdit_inner_diameter: QLineEdit
                                                                    - label_offset_y: QLabel
                                                                    - lineEdit_offset_y: QLineEdit
                                                                    - label_offset_z: QLabel
                                                                    - lineEdit_offset_z: QLineEdit
                                                                    - label_130: QLabel
                                                                    - label_129: QLabel
                                                                    - label_132: QLabel
                                                                    - label_inner_diameter: QLabel
                                                                    - label_128: QLabel
                                                                    - label_outer_diameter: QLabel
                                                                    - lineEdit_outer_diameter: QLineEdit
                                                                    - lineEdit_insulation_thickness: QLineEdit
                                                                    - label_133: QLabel
                                                                    - label_131: QLabel
                                                                    - lineEdit_insulation_density: QLineEdit
                                                                    - label_insulation_density: QLabel
                                                                    - label_insulationthickness: QLabel
                            - frame_get_section: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_get_cross_section: QCheckBox
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_confirm: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
