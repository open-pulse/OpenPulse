# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_group_information.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 360)
        Dialog.setMinimumSize(QSize(400, 240))
        Dialog.setMaximumSize(QSize(600, 500))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(16777215, 16777215))
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, -1, 4, -1)
        self.frame_selection = QFrame(self.frame_main)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setMinimumSize(QSize(0, 36))
        self.frame_selection.setFrameShape(QFrame.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_selection)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, -1, 4)
        self.lineEdit_selected_id = QLineEdit(self.frame_selection)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setEnabled(True)
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 26))
        self.lineEdit_selected_id.setMaximumSize(QSize(240, 26))
        font = QFont()
        font.setPointSize(10)
        self.lineEdit_selected_id.setFont(font)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_id, 0, 2, 1, 1)

        self.label_selected_id = QLabel(self.frame_selection)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(80, 0))
        self.label_selected_id.setMaximumSize(QSize(100, 16777215))
        self.label_selected_id.setFont(font)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_selected_id, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.frame_main)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setFrameShape(QFrame.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, -1, 4)
        self.treeWidget_group_info = QTreeWidget(self.frame_treeWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_group_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_group_info.setObjectName(u"treeWidget_group_info")
        self.treeWidget_group_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_group_info.setMaximumSize(QSize(600, 1000))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        self.treeWidget_group_info.setFont(font1)
        self.treeWidget_group_info.setTextElideMode(Qt.ElideRight)
        self.treeWidget_group_info.setIndentation(0)
        self.treeWidget_group_info.setUniformRowHeights(False)
        self.treeWidget_group_info.setAnimated(False)
        self.treeWidget_group_info.setAllColumnsShowFocus(False)
        self.treeWidget_group_info.setHeaderHidden(False)
        self.treeWidget_group_info.setColumnCount(2)
        self.treeWidget_group_info.header().setVisible(True)

        self.gridLayout_5.addWidget(self.treeWidget_group_info, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_treeWidget, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font2 = QFont()
        font2.setPointSize(11)
        self.label_title.setFont(font2)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 52))
        self.frame_buttons.setMaximumSize(QSize(16777215, 52))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_buttons)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(10)
        self.gridLayout_6.setContentsMargins(10, 0, 10, 0)
        self.pushButton_remove = QPushButton(self.frame_buttons)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remove.sizePolicy().hasHeightForWidth())
        self.pushButton_remove.setSizePolicy(sizePolicy)
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setSizeIncrement(QSize(0, 1))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_remove.setFont(font3)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_remove, 0, 1, 1, 1)

        self.pushButton_close = QPushButton(self.frame_buttons)
        self.pushButton_close.setObjectName(u"pushButton_close")
        sizePolicy.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy)
        self.pushButton_close.setMinimumSize(QSize(100, 28))
        self.pushButton_close.setMaximumSize(QSize(100, 28))
        self.pushButton_close.setSizeIncrement(QSize(0, 1))
        self.pushButton_close.setFont(font3)
        self.pushButton_close.setStyleSheet(u"")
        self.pushButton_close.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_close, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.treeWidget_group_info, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.pushButton_close)

        self.retranslateUi(Dialog)

        self.pushButton_close.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.lineEdit_selected_id.setText("")
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected ID:", None))
        ___qtreewidgetitem = self.treeWidget_group_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Elements", None));
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Information of selected group", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi



class GetGroupInformation_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_selection: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - label_selected_id: QLabel
                            - frame_treeWidget: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_group_info: QTreeWidget
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_remove: QPushButton
                            - pushButton_close: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
