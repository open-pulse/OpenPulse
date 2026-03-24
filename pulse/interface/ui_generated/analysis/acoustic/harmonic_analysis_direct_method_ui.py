# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_direct_method.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

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
        Dialog.setMaximumSize(QSize(360, 320))
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
        self.frame_title.setMinimumSize(QSize(0, 60))
        self.frame_title.setMaximumSize(QSize(400, 60))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 24))
        self.label_title.setMaximumSize(QSize(16777215, 24))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)

        self.label_subtitle = QLabel(self.frame_title)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setMinimumSize(QSize(0, 24))
        self.label_subtitle.setMaximumSize(QSize(16777215, 24))
        self.label_subtitle.setFont(font)
        self.label_subtitle.setTextFormat(Qt.AutoText)
        self.label_subtitle.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_subtitle, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 0))
        self.frame_main.setMaximumSize(QSize(400, 260))
        font1 = QFont()
        font1.setPointSize(2)
        self.frame_main.setFont(font1)
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_main)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(2)
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 8, 4, 4)
        self.tabWidget = QTabWidget(self.frame_main)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(360, 16777215))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.tabWidget.setFont(font2)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_5 = QGridLayout(self.tab_setup)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_fmin = QLineEdit(self.tab_setup)
        self.lineEdit_fmin.setObjectName(u"lineEdit_fmin")
        self.lineEdit_fmin.setMinimumSize(QSize(120, 28))
        self.lineEdit_fmin.setMaximumSize(QSize(120, 28))
        font3 = QFont()
        font3.setPointSize(10)
        self.lineEdit_fmin.setFont(font3)
        self.lineEdit_fmin.setStyleSheet(u"")
        self.lineEdit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fmin, 0, 2, 1, 1)

        self.label_23 = QLabel(self.tab_setup)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMinimumSize(QSize(80, 28))
        self.label_23.setMaximumSize(QSize(80, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setItalic(False)
        self.label_23.setFont(font4)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_24 = QLabel(self.tab_setup)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(60, 28))
        self.label_24.setMaximumSize(QSize(60, 28))
        self.label_24.setFont(font4)
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

        self.label_22 = QLabel(self.tab_setup)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setMinimumSize(QSize(80, 28))
        self.label_22.setMaximumSize(QSize(80, 28))
        self.label_22.setFont(font4)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_22, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.lineEdit_fstep = QLineEdit(self.tab_setup)
        self.lineEdit_fstep.setObjectName(u"lineEdit_fstep")
        self.lineEdit_fstep.setMinimumSize(QSize(120, 28))
        self.lineEdit_fstep.setMaximumSize(QSize(120, 28))
        self.lineEdit_fstep.setFont(font3)
        self.lineEdit_fstep.setStyleSheet(u"")
        self.lineEdit_fstep.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_fstep, 2, 2, 1, 1)

        self.label_26 = QLabel(self.tab_setup)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(60, 28))
        self.label_26.setMaximumSize(QSize(60, 28))
        self.label_26.setFont(font4)
        self.label_26.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_26, 2, 3, 1, 1)

        self.label_25 = QLabel(self.tab_setup)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(60, 28))
        self.label_25.setMaximumSize(QSize(60, 28))
        self.label_25.setFont(font4)
        self.label_25.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_25, 1, 3, 1, 1)

        self.label_21 = QLabel(self.tab_setup)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMinimumSize(QSize(80, 28))
        self.label_21.setMaximumSize(QSize(80, 28))
        self.label_21.setFont(font4)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.tabWidget.addTab(self.tab_setup, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.frame_main)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_buttons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(12)
        self.gridLayout_3.setVerticalSpacing(2)
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.run_analysis_button = QPushButton(self.frame_buttons)
        self.run_analysis_button.setObjectName(u"run_analysis_button")
        self.run_analysis_button.setMinimumSize(QSize(100, 30))
        self.run_analysis_button.setMaximumSize(QSize(100, 30))
        self.run_analysis_button.setFont(font2)
        self.run_analysis_button.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.run_analysis_button, 0, 1, 1, 1)

        self.enter_setup_button = QPushButton(self.frame_buttons)
        self.enter_setup_button.setObjectName(u"enter_setup_button")
        self.enter_setup_button.setMinimumSize(QSize(100, 30))
        self.enter_setup_button.setMaximumSize(QSize(100, 30))
        self.enter_setup_button.setFont(font2)
        self.enter_setup_button.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.enter_setup_button, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_buttons, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget, self.lineEdit_fmin)
        QWidget.setTabOrder(self.lineEdit_fmin, self.lineEdit_fmax)
        QWidget.setTabOrder(self.lineEdit_fmax, self.lineEdit_fstep)
        QWidget.setTabOrder(self.lineEdit_fstep, self.enter_setup_button)
        QWidget.setTabOrder(self.enter_setup_button, self.run_analysis_button)

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Acoustic harmonic analysis", None))
        self.label_subtitle.setText(QCoreApplication.translate("Dialog", u"Direct method", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Freq. max:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Freq. min:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u" Freq. step:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Frequency setup", None))
        self.run_analysis_button.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
        self.enter_setup_button.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
    # retranslateUi



class HarmonicAnalysisDirectMethod_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                            - label_subtitle: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - tabWidget: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - lineEdit_fmin: QLineEdit
                                            - label_23: QLabel
                                            - label_24: QLabel
                                            - lineEdit_fmax: QLineEdit
                                            - label_22: QLabel
                                            - lineEdit_fstep: QLineEdit
                                            - label_26: QLabel
                                            - label_25: QLabel
                                            - label_21: QLabel
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - run_analysis_button: QPushButton
                                        - enter_setup_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
