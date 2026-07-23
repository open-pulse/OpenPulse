# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'static_analysis.ui'
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
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(320, 280)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(320, 280))
        Dialog.setMaximumSize(QSize(320, 280))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        self.frame_title.setFont(font)
        self.frame_title.setStyleSheet(u"")
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 32))
        self.label_title.setMaximumSize(QSize(16777215, 32))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setKerning(False)
        self.label_title.setFont(font1)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_button = QFrame(Dialog)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(16777215, 48))
        self.frame_button.setFont(font)
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_button)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.pushButton_run_analysis = QPushButton(self.frame_button)
        self.pushButton_run_analysis.setObjectName(u"pushButton_run_analysis")
        self.pushButton_run_analysis.setMinimumSize(QSize(100, 28))
        self.pushButton_run_analysis.setMaximumSize(QSize(100, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        self.pushButton_run_analysis.setFont(font2)
        self.pushButton_run_analysis.setStyleSheet(u"")
        self.pushButton_run_analysis.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_run_analysis, 0, 1, 1, 1)

        self.pushButton_enter_setup = QPushButton(self.frame_button)
        self.pushButton_enter_setup.setObjectName(u"pushButton_enter_setup")
        self.pushButton_enter_setup.setMinimumSize(QSize(100, 28))
        self.pushButton_enter_setup.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.pushButton_enter_setup.setFont(font3)
        self.pushButton_enter_setup.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_enter_setup, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_button, 2, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame)
        self.gridLayout_8.setSpacing(2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.checkBox_self_weight_load = QCheckBox(self.frame)
        self.checkBox_self_weight_load.setObjectName(u"checkBox_self_weight_load")
        self.checkBox_self_weight_load.setMinimumSize(QSize(180, 26))
        self.checkBox_self_weight_load.setMaximumSize(QSize(180, 26))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setKerning(False)
        self.checkBox_self_weight_load.setFont(font4)
        self.checkBox_self_weight_load.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_self_weight_load, 0, 1, 1, 1)

        self.checkBox_distributed_element = QCheckBox(self.frame)
        self.checkBox_distributed_element.setObjectName(u"checkBox_distributed_element")
        self.checkBox_distributed_element.setMinimumSize(QSize(180, 26))
        self.checkBox_distributed_element.setMaximumSize(QSize(180, 26))
        self.checkBox_distributed_element.setFont(font4)
        self.checkBox_distributed_element.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_distributed_element, 3, 1, 1, 1)

        self.checkBox_internal_pressure_load = QCheckBox(self.frame)
        self.checkBox_internal_pressure_load.setObjectName(u"checkBox_internal_pressure_load")
        self.checkBox_internal_pressure_load.setMinimumSize(QSize(180, 26))
        self.checkBox_internal_pressure_load.setMaximumSize(QSize(180, 26))
        self.checkBox_internal_pressure_load.setFont(font4)
        self.checkBox_internal_pressure_load.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_internal_pressure_load, 1, 1, 1, 1)

        self.checkBox_external_nodal_loads = QCheckBox(self.frame)
        self.checkBox_external_nodal_loads.setObjectName(u"checkBox_external_nodal_loads")
        self.checkBox_external_nodal_loads.setMinimumSize(QSize(180, 26))
        self.checkBox_external_nodal_loads.setMaximumSize(QSize(180, 26))
        self.checkBox_external_nodal_loads.setFont(font4)
        self.checkBox_external_nodal_loads.setChecked(True)

        self.gridLayout_8.addWidget(self.checkBox_external_nodal_loads, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        QWidget.setTabOrder(self.checkBox_self_weight_load, self.checkBox_internal_pressure_load)
        QWidget.setTabOrder(self.checkBox_internal_pressure_load, self.checkBox_external_nodal_loads)
        QWidget.setTabOrder(self.checkBox_external_nodal_loads, self.checkBox_distributed_element)
        QWidget.setTabOrder(self.checkBox_distributed_element, self.pushButton_run_analysis)

        self.retranslateUi(Dialog)

        self.pushButton_run_analysis.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Static Analysis Setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Static analysis setup", None))
        self.pushButton_run_analysis.setText(QCoreApplication.translate("Dialog", u"Run Analysis", None))
        self.pushButton_enter_setup.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
        self.checkBox_self_weight_load.setText(QCoreApplication.translate("Dialog", u"Self weight load", None))
        self.checkBox_distributed_element.setText(QCoreApplication.translate("Dialog", u"Distributed element load", None))
        self.checkBox_internal_pressure_load.setText(QCoreApplication.translate("Dialog", u"Internal pressure load", None))
        self.checkBox_external_nodal_loads.setText(QCoreApplication.translate("Dialog", u"External nodal loads", None))
    # retranslateUi



class StaticAnalysis_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_button: QFrame
                    - (Layout): QGridLayout
                            - pushButton_run_analysis: QPushButton
                            - pushButton_enter_setup: QPushButton
                - frame: QFrame
                    - (Layout): QGridLayout
                            - checkBox_self_weight_load: QCheckBox
                            - checkBox_distributed_element: QCheckBox
                            - checkBox_internal_pressure_load: QCheckBox
                            - checkBox_external_nodal_loads: QCheckBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
