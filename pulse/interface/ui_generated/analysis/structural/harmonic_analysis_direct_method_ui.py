# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_direct_method.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(360, 320)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(360, 320))
        Dialog.setMaximumSize(QSize(360, 327))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(300, 60))
        self.frame_3.setMaximumSize(QSize(430, 60))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_3)
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

        self.label_subtitle = QLabel(self.frame_3)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setFont(font)
        self.label_subtitle.setTextFormat(Qt.AutoText)
        self.label_subtitle.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_subtitle, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(2)
        self.gridLayout_9.setVerticalSpacing(4)
        self.gridLayout_9.setContentsMargins(4, 8, 4, 4)
        self.tabWidget = QTabWidget(self.frame_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tabWidget.setMaximumSize(QSize(360, 16777215))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setKerning(False)
        self.tabWidget.setFont(font1)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_21 = QLabel(self.tab_setup)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 28))
        self.label_21.setMaximumSize(QSize(80, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setItalic(False)
        self.label_21.setFont(font2)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 2, 1, 1, 1)

        self.label_26 = QLabel(self.tab_setup)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 28))
        self.label_26.setMaximumSize(QSize(60, 28))
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_26, 2, 3, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.tab_setup)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(120, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(120, 28))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_fstep.setFont(font3)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.label_22 = QLabel(self.tab_setup)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(80, 28))
        self.label_22.setFont(font2)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_22, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_fmin = QLineEdit(self.tab_setup)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(120, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(120, 28))
        self.lineEdit_fmin.setFont(font3)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.label_24 = QLabel(self.tab_setup)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(60, 28))
        self.label_24.setMaximumSize(QSize(60, 28))
        self.label_24.setFont(font2)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_24, 0, 3, 1, 1)

        self.lineEdit_fmax = QLineEdit(self.tab_setup)
        self.lineEdit_fmax.setObjectName(u"lineEdit_fmax")
        self.lineEdit_fmax.setMinimumSize(QSize(120, 28))
        self.lineEdit_fmax.setMaximumSize(QSize(120, 28))
        self.lineEdit_fmax.setFont(font3)
        self.lineEdit_fmax.setStyleSheet(u"")
        self.lineEdit_fmax.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fmax, 1, 2, 1, 1)

        self.label_23 = QLabel(self.tab_setup)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(80, 28))
        self.label_23.setFont(font2)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_25 = QLabel(self.tab_setup)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 28))
        self.label_25.setMaximumSize(QSize(60, 28))
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_25, 1, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.tabWidget.addTab(self.tab_setup, "")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_15 = QLabel(self.widget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 26))
        self.label_15.setMaximumSize(QSize(16777215, 26))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.label_15.setFont(font4)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_15, 0, 0, 1, 1)

        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 26))
        self.label_14.setMaximumSize(QSize(16777215, 26))
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_14, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_12, 0, 4, 1, 1)

        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(40, 26))
        self.label_10.setMaximumSize(QSize(40, 26))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label_10.setFont(font5)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(40, 26))
        self.label_11.setMaximumSize(QSize(40, 26))
        self.label_11.setFont(font5)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.label_11, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_15, 0, 2, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font3)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_8)


        self.gridLayout_4.addLayout(self.verticalLayout_5, 0, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.lineEdit_ah = QLineEdit(self.widget)
        self.lineEdit_ah.setObjectName(u"lineEdit_ah")
        self.lineEdit_ah.setMinimumSize(QSize(100, 26))
        self.lineEdit_ah.setMaximumSize(QSize(100, 26))
        self.lineEdit_ah.setFont(font3)
        self.lineEdit_ah.setStyleSheet(u"")
        self.lineEdit_ah.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_ah, 0, 0, 1, 1)

        self.lineEdit_bh = QLineEdit(self.widget)
        self.lineEdit_bh.setObjectName(u"lineEdit_bh")
        self.lineEdit_bh.setMinimumSize(QSize(100, 26))
        self.lineEdit_bh.setMaximumSize(QSize(100, 26))
        self.lineEdit_bh.setFont(font3)
        self.lineEdit_bh.setStyleSheet(u"")
        self.lineEdit_bh.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_bh, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_10, 1, 3, 1, 1)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(40, 26))
        self.label_13.setMaximumSize(QSize(40, 26))
        self.label_13.setFont(font5)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(40, 26))
        self.label_12.setMaximumSize(QSize(40, 26))
        self.label_12.setFont(font5)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.label_12, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_14, 1, 2, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font3)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_9)


        self.gridLayout_4.addLayout(self.verticalLayout_6, 1, 1, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.lineEdit_av = QLineEdit(self.widget)
        self.lineEdit_av.setObjectName(u"lineEdit_av")
        self.lineEdit_av.setMinimumSize(QSize(100, 26))
        self.lineEdit_av.setMaximumSize(QSize(100, 26))
        self.lineEdit_av.setFont(font3)
        self.lineEdit_av.setStyleSheet(u"")
        self.lineEdit_av.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_av, 0, 0, 1, 1)

        self.lineEdit_bv = QLineEdit(self.widget)
        self.lineEdit_bv.setObjectName(u"lineEdit_bv")
        self.lineEdit_bv.setMinimumSize(QSize(100, 26))
        self.lineEdit_bv.setMaximumSize(QSize(100, 26))
        self.lineEdit_bv.setFont(font3)
        self.lineEdit_bv.setStyleSheet(u"")
        self.lineEdit_bv.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_bv, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_11, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_16 = QLabel(self.widget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 26))
        self.label_16.setMaximumSize(QSize(16777215, 26))
        self.label_16.setFont(font4)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_17 = QLabel(self.widget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 26))
        self.label_17.setMaximumSize(QSize(16777215, 26))
        self.label_17.setFont(font4)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.label_17, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_13, 1, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.widget, "")

        self.gridLayout_9.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(360, 48))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.run_analysis_button = QPushButton(self.frame)
        self.run_analysis_button.setObjectName(u"run_analysis_button")
        self.run_analysis_button.setMinimumSize(QSize(100, 28))
        self.run_analysis_button.setMaximumSize(QSize(100, 28))
        self.run_analysis_button.setFont(font4)
        self.run_analysis_button.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.run_analysis_button, 0, 1, 1, 1)

        self.enter_setup_button = QPushButton(self.frame)
        self.enter_setup_button.setObjectName(u"enter_setup_button")
        self.enter_setup_button.setMinimumSize(QSize(100, 28))
        self.enter_setup_button.setMaximumSize(QSize(100, 28))
        self.enter_setup_button.setFont(font4)
        self.enter_setup_button.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.enter_setup_button, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.frame, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.enter_setup_button)
        QWidget.setTabOrder(self.enter_setup_button, self.run_analysis_button)
        QWidget.setTabOrder(self.run_analysis_button, self.lineEdit_av)
        QWidget.setTabOrder(self.lineEdit_av, self.lineEdit_bv)
        QWidget.setTabOrder(self.lineEdit_bv, self.lineEdit_ah)
        QWidget.setTabOrder(self.lineEdit_ah, self.lineEdit_bh)

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Harmonic analysis - Structural", None))
        self.label_subtitle.setText(QCoreApplication.translate("Dialog", u"Direct method", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Freq. step:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Frequency Setup", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[1/s]", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[s]", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">\u03b1</span><span style=\" font-size:10pt; vertical-align:sub;\">v</span><span style=\" font-size:10pt;\">:</span></p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">\u03b2</span><span style=\" font-size:10pt; vertical-align:sub;\">v</span><span style=\" font-size:10pt;\">:</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Proportional\n"
"viscous", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">\u03b1</span><span style=\" font-size:10pt; vertical-align:sub;\">h</span><span style=\" font-size:10pt;\">:</span></p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">\u03b2</span><span style=\" font-size:10pt; vertical-align:sub;\">h</span><span style=\" font-size:10pt;\">:</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Proportional\n"
"hysteretic", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[1/s\u00b2]", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QCoreApplication.translate("Dialog", u"Structural damping", None))
        self.run_analysis_button.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
        self.enter_setup_button.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
    # retranslateUi



class HarmonicAnalysisDirectMethod_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                            - label_subtitle: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tabWidget: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - label_21: QLabel
                                            - label_26: QLabel
                                            - lineEdit_fstep: QLineEdit
                                            - label_22: QLabel
                                            - lineEdit_fmin: QLineEdit
                                            - label_24: QLabel
                                            - lineEdit_fmax: QLineEdit
                                            - label_23: QLabel
                                            - label_25: QLabel
                                - widget: QWidget
                                    - (Layout): QGridLayout
                                            - (Layout): QGridLayout
                                                    - label_15: QLabel
                                                    - label_14: QLabel
                                            - (Layout): QGridLayout
                                                    - label_10: QLabel
                                                    - label_11: QLabel
                                            - (Layout): QVBoxLayout
                                                    - label_8: QLabel
                                            - (Layout): QGridLayout
                                                    - lineEdit_ah: QLineEdit
                                                    - lineEdit_bh: QLineEdit
                                            - (Layout): QGridLayout
                                                    - label_13: QLabel
                                                    - label_12: QLabel
                                            - (Layout): QVBoxLayout
                                                    - label_9: QLabel
                                            - (Layout): QGridLayout
                                                    - lineEdit_av: QLineEdit
                                                    - lineEdit_bv: QLineEdit
                                            - (Layout): QGridLayout
                                                    - label_16: QLabel
                                                    - label_17: QLabel
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - run_analysis_button: QPushButton
                                        - enter_setup_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
