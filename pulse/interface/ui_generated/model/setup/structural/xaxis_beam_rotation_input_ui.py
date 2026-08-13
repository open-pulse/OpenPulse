# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'xaxis_beam_rotation_input.ui'
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
        Dialog.setWindowModality(Qt.WindowModality.NonModal)
        Dialog.resize(380, 440)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(380, 440))
        Dialog.setMaximumSize(QSize(380, 440))
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(40)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(460, 600))
        font = QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(600, 360))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_8 = QFrame(self.tab_setup)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(8)
        self.gridLayout_8.setVerticalSpacing(6)
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 30))
        self.label_5.setMaximumSize(QSize(120, 26))
        self.label_5.setSizeIncrement(QSize(196, 26))
        self.label_5.setFont(font1)
        self.label_5.setTextFormat(Qt.TextFormat.AutoText)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_8 = QLabel(self.frame_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 30))
        self.label_8.setMaximumSize(QSize(120, 26))
        self.label_8.setSizeIncrement(QSize(196, 26))
        self.label_8.setFont(font1)
        self.label_8.setTextFormat(Qt.TextFormat.AutoText)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_8, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame_8)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(80, 30))
        self.label_6.setMaximumSize(QSize(80, 26))
        self.label_6.setSizeIncrement(QSize(0, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setKerning(False)
        self.label_6.setFont(font2)
        self.label_6.setTextFormat(Qt.TextFormat.AutoText)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_6, 0, 3, 1, 1)

        self.lineEdit_increment_angle = QLineEdit(self.frame_8)
        self.lineEdit_increment_angle.setObjectName(u"lineEdit_increment_angle")
        self.lineEdit_increment_angle.setEnabled(True)
        self.lineEdit_increment_angle.setMinimumSize(QSize(100, 30))
        self.lineEdit_increment_angle.setMaximumSize(QSize(100, 26))
        self.lineEdit_increment_angle.setSizeIncrement(QSize(0, 26))
        self.lineEdit_increment_angle.setFont(font1)
        self.lineEdit_increment_angle.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_increment_angle.setStyleSheet(u"")
        self.lineEdit_increment_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_increment_angle, 1, 2, 1, 1)

        self.label_7 = QLabel(self.frame_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(80, 30))
        self.label_7.setMaximumSize(QSize(80, 26))
        self.label_7.setSizeIncrement(QSize(0, 26))
        self.label_7.setFont(font2)
        self.label_7.setTextFormat(Qt.TextFormat.AutoText)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_7, 1, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.lineEdit_actual_angle = QLineEdit(self.frame_8)
        self.lineEdit_actual_angle.setObjectName(u"lineEdit_actual_angle")
        self.lineEdit_actual_angle.setEnabled(False)
        self.lineEdit_actual_angle.setMinimumSize(QSize(100, 30))
        self.lineEdit_actual_angle.setMaximumSize(QSize(100, 26))
        self.lineEdit_actual_angle.setSizeIncrement(QSize(0, 26))
        self.lineEdit_actual_angle.setFont(font1)
        self.lineEdit_actual_angle.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_actual_angle.setStyleSheet(u"")
        self.lineEdit_actual_angle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.lineEdit_actual_angle, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_8, 0, 0, 1, 2)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_list = QWidget()
        self.tab_list.setObjectName(u"tab_list")
        self.gridLayout_3 = QGridLayout(self.tab_list)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_lines_info = QTreeWidget(self.tab_list)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font3)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font3)
        self.treeWidget_lines_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_lines_info.setObjectName(u"treeWidget_lines_info")
        self.treeWidget_lines_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_lines_info.setMaximumSize(QSize(320, 400))
        self.treeWidget_lines_info.setFont(font3)
        self.treeWidget_lines_info.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_lines_info, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.tab_list)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 44))
        self.frame_7.setMaximumSize(QSize(16777215, 48))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_7)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_remove = QPushButton(self.frame_7)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font1)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_7)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font1)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_reset, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_7, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_list, "")

        self.gridLayout.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_attribution_controls = QFrame(self.frame_2)
        self.frame_attribution_controls.setObjectName(u"frame_attribution_controls")
        self.frame_attribution_controls.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_attribution_controls.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_attribution_controls)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(7)
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_id = QLineEdit(self.frame_attribution_controls)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(False)
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(16777215, 26))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setKerning(False)
        self.lineEdit_selected_id.setFont(font4)
        self.lineEdit_selected_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.comboBox_selection = QComboBox(self.frame_attribution_controls)
        self.comboBox_selection.addItem("")
        self.comboBox_selection.addItem("")
        self.comboBox_selection.setObjectName(u"comboBox_selection")
        self.comboBox_selection.setMinimumSize(QSize(0, 26))
        self.comboBox_selection.setMaximumSize(QSize(16777215, 26))
        self.comboBox_selection.setFont(font4)

        self.gridLayout_9.addWidget(self.comboBox_selection, 0, 2, 1, 1)

        self.label_attribute_to = QLabel(self.frame_attribution_controls)
        self.label_attribute_to.setObjectName(u"label_attribute_to")
        self.label_attribute_to.setMinimumSize(QSize(90, 26))
        self.label_attribute_to.setMaximumSize(QSize(100, 26))
        self.label_attribute_to.setFont(font4)
        self.label_attribute_to.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_attribute_to, 0, 1, 1, 1)

        self.label_selected_id = QLabel(self.frame_attribution_controls)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(90, 26))
        self.label_selected_id.setMaximumSize(QSize(100, 26))
        self.label_selected_id.setFont(font4)
        self.label_selected_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_selected_id, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 1, 5, 1, 1)


        self.gridLayout.addWidget(self.frame_attribution_controls, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame_title)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font5 = QFont()
        font5.setPointSize(11)
        self.label_title.setFont(font5)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_title, 0, 0, 2, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_5 = QFrame(Dialog)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 48))
        self.frame_5.setMaximumSize(QSize(16777215, 48))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_5)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_5)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        font6 = QFont()
        font6.setPointSize(10)
        self.pushButton_attribute.setFont(font6)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_5)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font6)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_5, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_selection, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.treeWidget_lines_info)
        QWidget.setTabOrder(self.treeWidget_lines_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.pushButton_remove.setDefault(False)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u" Set: beam x-axis rotation angle", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Actual angle:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Increment angle:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"[degrees]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_increment_angle.setToolTip(QCoreApplication.translate("Dialog", u"Insert an increment value to the rotation angle in degrees.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_increment_angle.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"[degrees]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_actual_angle.setToolTip(QCoreApplication.translate("Dialog", u"Actual value of the rotation angle in degrees.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_actual_angle.setText("")
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_lines_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Angle [deg]", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Lines", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_list), QCoreApplication.translate("Dialog", u"List", None))
        self.lineEdit_selected_id.setText(QCoreApplication.translate("Dialog", u"All lines", None))
        self.comboBox_selection.setItemText(0, QCoreApplication.translate("Dialog", u"All lines", None))
        self.comboBox_selection.setItemText(1, QCoreApplication.translate("Dialog", u"Selected lines", None))

        self.label_attribute_to.setText(QCoreApplication.translate("Dialog", u"Attribute to:", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"X-axis beam rotation setup", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class XaxisBeamRotationInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - frame_8: QFrame
                                                - (Layout): QGridLayout
                                                        - label_5: QLabel
                                                        - label_8: QLabel
                                                        - label_6: QLabel
                                                        - lineEdit_increment_angle: QLineEdit
                                                        - label_7: QLabel
                                                        - lineEdit_actual_angle: QLineEdit
                                - tab_list: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_lines_info: QTreeWidget
                                            - frame_7: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_remove: QPushButton
                                                        - pushButton_reset: QPushButton
                            - frame_attribution_controls: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - comboBox_selection: QComboBox
                                        - label_attribute_to: QLabel
                                        - label_selected_id: QLabel
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_5: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
