# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_setup_input.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(360, 377)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(360, 360))
        Dialog.setMaximumSize(QSize(380, 460))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 60))
        self.frame_title.setMaximumSize(QSize(430, 60))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_main)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(2)
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(4, 6, 4, 4)
        self.tabWidget_main = QTabWidget(self.frame_main)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(360, 188))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.tabWidget_main.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_26 = QLabel(self.tab_setup)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(40, 28))
        self.label_26.setMaximumSize(QSize(40, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_26, 2, 3, 1, 1)

        self.label_25 = QLabel(self.tab_setup)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(40, 28))
        self.label_25.setMaximumSize(QSize(40, 28))
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_25, 1, 3, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.tab_setup)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(170, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(180, 28))
        self.lineEdit_fstep.setFont(font1)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.tab_setup)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(170, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmax.setFont(font1)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_24 = QLabel(self.tab_setup)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(40, 28))
        self.label_24.setMaximumSize(QSize(40, 28))
        self.label_24.setFont(font2)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_24, 0, 3, 1, 1)

        self.label_22 = QLabel(self.tab_setup)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setItalic(False)
        font3.setKerning(False)
        self.label_22.setFont(font3)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_22, 0, 1, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.tab_setup)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(170, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(180, 28))
        self.lineEdit_fmin.setFont(font1)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.label_23 = QLabel(self.tab_setup)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(100, 28))
        self.label_23.setFont(font3)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_21 = QLabel(self.tab_setup)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 28))
        self.label_21.setMaximumSize(QSize(100, 28))
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_damping = QWidget()
        self.tab_damping.setObjectName(u"tab_damping")
        self.gridLayout_4 = QGridLayout(self.tab_damping)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 4, 6, 4)
        self.frame_dampings = QFrame(self.tab_damping)
        self.frame_dampings.setObjectName(u"frame_dampings")
        self.frame_dampings.setFrameShape(QFrame.NoFrame)
        self.frame_dampings.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_dampings)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label_16 = QLabel(self.frame_dampings)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_16, 2, 4, 1, 1)

        self.lineEdit_constant_structural_coefficient = QLineEdit(self.frame_dampings)
        self.lineEdit_constant_structural_coefficient.setObjectName(u"lineEdit_constant_structural_coefficient")
        self.lineEdit_constant_structural_coefficient.setMinimumSize(QSize(80, 26))
        self.lineEdit_constant_structural_coefficient.setMaximumSize(QSize(100, 26))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.lineEdit_constant_structural_coefficient.setFont(font4)
        self.lineEdit_constant_structural_coefficient.setStyleSheet(u"")
        self.lineEdit_constant_structural_coefficient.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_constant_structural_coefficient, 2, 3, 1, 1)

        self.label_9 = QLabel(self.frame_dampings)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(132, 0))
        self.label_9.setFont(font4)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_9, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.lineEdit_stiffness_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_stiffness_multiplier.setObjectName(u"lineEdit_stiffness_multiplier")
        self.lineEdit_stiffness_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_stiffness_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_stiffness_multiplier.setFont(font4)
        self.lineEdit_stiffness_multiplier.setStyleSheet(u"")
        self.lineEdit_stiffness_multiplier.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_stiffness_multiplier, 1, 3, 1, 1)

        self.label_10 = QLabel(self.frame_dampings)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(132, 0))
        self.label_10.setFont(font4)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_10, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frame_dampings)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(20, 26))
        self.label_11.setMaximumSize(QSize(40, 26))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label_11.setFont(font5)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_11, 1, 2, 1, 1)

        self.label_14 = QLabel(self.frame_dampings)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 26))
        self.label_14.setMaximumSize(QSize(16777215, 26))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_14, 1, 4, 1, 1)

        self.lineEdit_mass_multiplier = QLineEdit(self.frame_dampings)
        self.lineEdit_mass_multiplier.setObjectName(u"lineEdit_mass_multiplier")
        self.lineEdit_mass_multiplier.setMinimumSize(QSize(80, 26))
        self.lineEdit_mass_multiplier.setMaximumSize(QSize(100, 26))
        self.lineEdit_mass_multiplier.setFont(font4)
        self.lineEdit_mass_multiplier.setStyleSheet(u"")
        self.lineEdit_mass_multiplier.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_mass_multiplier, 0, 3, 1, 1)

        self.label_12 = QLabel(self.frame_dampings)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(20, 26))
        self.label_12.setMaximumSize(QSize(40, 26))
        self.label_12.setFont(font5)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_12, 0, 2, 1, 1)

        self.label_17 = QLabel(self.frame_dampings)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(132, 0))
        self.label_17.setFont(font4)
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_17.setWordWrap(True)

        self.gridLayout_6.addWidget(self.label_17, 0, 1, 1, 1)

        self.label_15 = QLabel(self.frame_dampings)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 26))
        self.label_15.setMaximumSize(QSize(16777215, 26))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_15, 0, 4, 1, 1)

        self.label_13 = QLabel(self.frame_dampings)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(20, 26))
        self.label_13.setMaximumSize(QSize(40, 26))
        self.label_13.setFont(font5)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.label_13, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.label_12.raise_()
        self.label_16.raise_()
        self.lineEdit_constant_structural_coefficient.raise_()
        self.label_9.raise_()
        self.lineEdit_stiffness_multiplier.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_14.raise_()
        self.lineEdit_mass_multiplier.raise_()
        self.label_17.raise_()
        self.label_15.raise_()
        self.label_13.raise_()

        self.gridLayout_4.addWidget(self.frame_dampings, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_damping, "")

        self.gridLayout_9.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_analysis_type = QFrame(self.frame_main)
        self.frame_analysis_type.setObjectName(u"frame_analysis_type")
        self.frame_analysis_type.setMinimumSize(QSize(0, 72))
        self.frame_analysis_type.setMaximumSize(QSize(1000, 80))
        self.frame_analysis_type.setFrameShape(QFrame.NoFrame)
        self.frame_analysis_type.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_analysis_type)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.comboBox_method = QComboBox(self.frame_analysis_type)
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setMinimumSize(QSize(160, 28))
        self.comboBox_method.setMaximumSize(QSize(160, 28))
        self.comboBox_method.setFont(font1)
        self.comboBox_method.setInsertPolicy(QComboBox.NoInsert)

        self.gridLayout_7.addWidget(self.comboBox_method, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_analysis_type)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 28))
        self.label_3.setMaximumSize(QSize(160, 28))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setBold(False)
        self.label_3.setFont(font6)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_modes_to_expand = QLabel(self.frame_analysis_type)
        self.label_modes_to_expand.setObjectName(u"label_modes_to_expand")
        self.label_modes_to_expand.setMinimumSize(QSize(120, 28))
        self.label_modes_to_expand.setMaximumSize(QSize(160, 28))
        self.label_modes_to_expand.setFont(font1)
        self.label_modes_to_expand.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_modes_to_expand, 1, 1, 1, 1)

        self.lineEdit_modes_to_expand = QLineEdit(self.frame_analysis_type)
        self.lineEdit_modes_to_expand.setObjectName(u"lineEdit_modes_to_expand")
        self.lineEdit_modes_to_expand.setMinimumSize(QSize(160, 28))
        self.lineEdit_modes_to_expand.setMaximumSize(QSize(160, 28))
        self.lineEdit_modes_to_expand.setFont(font1)
        self.lineEdit_modes_to_expand.setStyleSheet(u"")
        self.lineEdit_modes_to_expand.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_modes_to_expand, 1, 2, 1, 1)


        self.gridLayout_9.addWidget(self.frame_analysis_type, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(360, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_enter_setup = QPushButton(self.frame_buttons)
        self.pushButton_enter_setup.setObjectName(u"pushButton_enter_setup")
        self.pushButton_enter_setup.setMinimumSize(QSize(100, 30))
        self.pushButton_enter_setup.setMaximumSize(QSize(100, 30))
        self.pushButton_enter_setup.setFont(font1)
        self.pushButton_enter_setup.setStyleSheet(u"")
        self.pushButton_enter_setup.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_enter_setup, 0, 0, 1, 1)

        self.pushButton_run_analysis = QPushButton(self.frame_buttons)
        self.pushButton_run_analysis.setObjectName(u"pushButton_run_analysis")
        self.pushButton_run_analysis.setMinimumSize(QSize(100, 30))
        self.pushButton_run_analysis.setMaximumSize(QSize(100, 30))
        self.pushButton_run_analysis.setFont(font1)
        self.pushButton_run_analysis.setStyleSheet(u"")
        self.pushButton_run_analysis.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_run_analysis, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.pushButton_enter_setup)
        QWidget.setTabOrder(self.pushButton_enter_setup, self.pushButton_run_analysis)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Frequency Setup", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[--]", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Constant structural damping coefficient", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Stiffness matrix multiplier", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b2:</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b1:</p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Mass matrix multiplier", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[1/s]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\">\u03b7:</p></body></html>", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_damping), QCoreApplication.translate("Dialog", u"Damping setup", None))
        self.comboBox_method.setItemText(0, QCoreApplication.translate("Dialog", u"Direct", None))
        self.comboBox_method.setItemText(1, QCoreApplication.translate("Dialog", u"Mode Superposition", None))

#if QT_CONFIG(tooltip)
        self.comboBox_method.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Select the analysis method</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Method:", None))
        self.label_modes_to_expand.setText(QCoreApplication.translate("Dialog", u"Modes to expand:", None))
        self.pushButton_enter_setup.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
        self.pushButton_run_analysis.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
    # retranslateUi



class HarmonicAnalysisSetupInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - label_26: QLabel
                                            - label_25: QLabel
                                            - lineEdit_fstep: QLineEdit
                                            - lineEdit_fmax: QLineEdit
                                            - label_24: QLabel
                                            - label_22: QLabel
                                            - lineEdit_fmin: QLineEdit
                                            - label_23: QLabel
                                            - label_21: QLabel
                                - tab_damping: QWidget
                                    - (Layout): QGridLayout
                                            - frame_dampings: QFrame
                                                - (Layout): QGridLayout
                                                        - label_16: QLabel
                                                        - lineEdit_constant_structural_coefficient: QLineEdit
                                                        - label_9: QLabel
                                                        - lineEdit_stiffness_multiplier: QLineEdit
                                                        - label_10: QLabel
                                                        - label_11: QLabel
                                                        - label_14: QLabel
                                                        - lineEdit_mass_multiplier: QLineEdit
                                                        - label_12: QLabel
                                                        - label_17: QLabel
                                                        - label_15: QLabel
                                                        - label_13: QLabel
                            - frame_analysis_type: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_method: QComboBox
                                        - label_3: QLabel
                                        - label_modes_to_expand: QLabel
                                        - lineEdit_modes_to_expand: QLineEdit
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_enter_setup: QPushButton
                            - pushButton_run_analysis: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
