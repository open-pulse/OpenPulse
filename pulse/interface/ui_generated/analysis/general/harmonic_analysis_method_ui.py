# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'harmonic_analysis_method.ui'
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
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(320, 220)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(320, 220))
        Dialog.setMaximumSize(QSize(320, 220))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName(u"label_title")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_title.setFont(font1)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_analysis = QFrame(self.frame_2)
        self.frame_analysis.setObjectName(u"frame_analysis")
        self.frame_analysis.setMinimumSize(QSize(0, 48))
        self.frame_analysis.setMaximumSize(QSize(1000, 48))
        self.frame_analysis.setFrameShape(QFrame.NoFrame)
        self.frame_analysis.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_analysis)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label_method = QLabel(self.frame_analysis)
        self.label_method.setObjectName(u"label_method")
        self.label_method.setMinimumSize(QSize(0, 30))
        self.label_method.setMaximumSize(QSize(180, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_method.setFont(font2)
        self.label_method.setFrameShape(QFrame.NoFrame)
        self.label_method.setFrameShadow(QFrame.Plain)
        self.label_method.setTextFormat(Qt.AutoText)
        self.label_method.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_method, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_analysis, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 48))
        self.frame_4.setMaximumSize(QSize(1000, 48))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.comboBox_method = QComboBox(self.frame_4)
        self.comboBox_method.addItem("")
        self.comboBox_method.addItem("")
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setMinimumSize(QSize(160, 28))
        self.comboBox_method.setMaximumSize(QSize(160, 28))
        self.comboBox_method.setFont(font2)
        self.comboBox_method.setInsertPolicy(QComboBox.NoInsert)

        self.gridLayout_5.addWidget(self.comboBox_method, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(52, 28))
        self.label_2.setMaximumSize(QSize(52, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(48, 0))
        self.frame_6.setMaximumSize(QSize(48, 16777215))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_5.addWidget(self.frame_6, 0, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_button = QFrame(self.frame_2)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 48))
        self.frame_button.setMaximumSize(QSize(1000, 48))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_button)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pushButton_proceed = QPushButton(self.frame_button)
        self.pushButton_proceed.setObjectName(u"pushButton_proceed")
        self.pushButton_proceed.setMinimumSize(QSize(100, 30))
        self.pushButton_proceed.setMaximumSize(QSize(100, 30))
        self.pushButton_proceed.setFont(font2)
        self.pushButton_proceed.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_proceed, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_button)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font2)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_4.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_button, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Harmonic analysis: method selection", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Harmonic Analysis Method Selector", None))
        self.label_method.setText(QCoreApplication.translate("Dialog", u"Select the Analysis Method", None))
        self.comboBox_method.setItemText(0, QCoreApplication.translate("Dialog", u" Direct", None))
        self.comboBox_method.setItemText(1, QCoreApplication.translate("Dialog", u"Mode Superposition", None))

#if QT_CONFIG(tooltip)
        self.comboBox_method.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Select the analysis method</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Method:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_proceed.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Go to the analysis setup</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_proceed.setText(QCoreApplication.translate("Dialog", u"Proceed", None))
#if QT_CONFIG(tooltip)
        self.pushButton_exit.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Go to the analysis setup</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class HarmonicAnalysisMethod_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_analysis: QFrame
                                - (Layout): QGridLayout
                                        - label_method: QLabel
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_method: QComboBox
                                        - label_2: QLabel
                                        - frame_6: QFrame
                            - frame_button: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_proceed: QPushButton
                                        - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
