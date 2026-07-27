# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_cross_section.ui'
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
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(620, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(620, 640))
        Dialog.setMaximumSize(QSize(620, 660))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_33 = QGridLayout(Dialog)
        self.gridLayout_33.setSpacing(4)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(4, 4, 4, 4)
        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(1000, 48))
        self.top_frame.setFrameShape(QFrame.Box)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout = QGridLayout(self.top_frame)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)


        self.gridLayout_33.addWidget(self.top_frame, 0, 0, 1, 1)

        self.bottom_frame = QFrame(Dialog)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setMinimumSize(QSize(0, 0))
        self.bottom_frame.setMaximumSize(QSize(1000, 1000))
        self.bottom_frame.setFrameShape(QFrame.Box)
        self.bottom_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_29 = QGridLayout(self.bottom_frame)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridLayout_29.setHorizontalSpacing(4)
        self.gridLayout_29.setVerticalSpacing(0)
        self.gridLayout_29.setContentsMargins(4, 4, 4, 4)
        self.main_frame = QFrame(self.bottom_frame)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setMinimumSize(QSize(0, 0))
        self.main_frame.setMaximumSize(QSize(1000, 1000))
        font1 = QFont()
        font1.setPointSize(10)
        self.main_frame.setFont(font1)
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_28 = QGridLayout(self.main_frame)
        self.gridLayout_28.setSpacing(2)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setContentsMargins(2, 0, 2, 2)

        self.gridLayout_29.addWidget(self.main_frame, 1, 0, 1, 1)

        self.selection_frame = QFrame(self.bottom_frame)
        self.selection_frame.setObjectName(u"selection_frame")
        self.selection_frame.setMinimumSize(QSize(0, 80))
        self.selection_frame.setMaximumSize(QSize(16777215, 80))
        self.selection_frame.setFrameShape(QFrame.NoFrame)
        self.selection_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_26 = QGridLayout(self.selection_frame)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setHorizontalSpacing(6)
        self.gridLayout_26.setVerticalSpacing(2)
        self.gridLayout_26.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_selected_id = QLineEdit(self.selection_frame)
        self.lineEdit_selected_id.setObjectName(u"lineEdit_selected_id")
        self.lineEdit_selected_id.setMinimumSize(QSize(0, 28))
        self.lineEdit_selected_id.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setKerning(False)
        self.lineEdit_selected_id.setFont(font2)
        self.lineEdit_selected_id.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_selected_id.setStyleSheet(u"")
        self.lineEdit_selected_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_26.addWidget(self.lineEdit_selected_id, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.comboBox_attribution_type = QComboBox(self.selection_frame)
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.addItem("")
        self.comboBox_attribution_type.setObjectName(u"comboBox_attribution_type")
        self.comboBox_attribution_type.setMinimumSize(QSize(0, 28))
        self.comboBox_attribution_type.setMaximumSize(QSize(16777215, 28))
        self.comboBox_attribution_type.setFont(font1)

        self.gridLayout_26.addWidget(self.comboBox_attribution_type, 0, 2, 1, 1)

        self.frame_26 = QFrame(self.selection_frame)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMinimumSize(QSize(120, 26))
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_26)
        self.gridLayout_27.setSpacing(0)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer, 1, 0, 1, 1)


        self.gridLayout_26.addWidget(self.frame_26, 1, 0, 1, 1)

        self.label_attribute = QLabel(self.selection_frame)
        self.label_attribute.setObjectName(u"label_attribute")
        self.label_attribute.setMinimumSize(QSize(120, 28))
        self.label_attribute.setMaximumSize(QSize(120, 28))
        self.label_attribute.setFont(font1)
        self.label_attribute.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_attribute, 0, 1, 1, 1)

        self.label_selected_id = QLabel(self.selection_frame)
        self.label_selected_id.setObjectName(u"label_selected_id")
        self.label_selected_id.setMinimumSize(QSize(120, 28))
        self.label_selected_id.setMaximumSize(QSize(120, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_selected_id.setFont(font3)
        self.label_selected_id.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_26.addWidget(self.label_selected_id, 1, 1, 1, 1)


        self.gridLayout_29.addWidget(self.selection_frame, 0, 0, 1, 1)


        self.gridLayout_33.addWidget(self.bottom_frame, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set: cross-section", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Set cross-section configuration", None))
        self.comboBox_attribution_type.setItemText(0, QCoreApplication.translate("Dialog", u" All lines", None))
        self.comboBox_attribution_type.setItemText(1, QCoreApplication.translate("Dialog", u" Selected lines", None))

        self.label_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute to:", None))
        self.label_selected_id.setText(QCoreApplication.translate("Dialog", u"Selected lines:", None))
    # retranslateUi



class SetCrossSection_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - bottom_frame: QFrame
                    - (Layout): QGridLayout
                            - main_frame: QFrame
                                - (Layout): QGridLayout
                            - selection_frame: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_selected_id: QLineEdit
                                        - comboBox_attribution_type: QComboBox
                                        - frame_26: QFrame
                                            - (Layout): QGridLayout
                                        - label_attribute: QLabel
                                        - label_selected_id: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
