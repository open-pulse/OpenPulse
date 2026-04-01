# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modal_analysis_setup_input.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(300, 220)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(300, 220))
        Dialog.setMaximumSize(QSize(300, 220))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u"../../../../../../../OpenPulse/Downloads/load - Copia.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(16777215, 48))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        self.frame_title.setFont(font)
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
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


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_main)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_modes = QFrame(self.frame_main)
        self.frame_modes.setObjectName(u"frame_modes")
        self.frame_modes.setMinimumSize(QSize(0, 40))
        self.frame_modes.setMaximumSize(QSize(16777215, 40))
        self.frame_modes.setFrameShape(QFrame.NoFrame)
        self.frame_modes.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_modes)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.label_modes = QLabel(self.frame_modes)
        self.label_modes.setObjectName(u"label_modes")
        self.label_modes.setMinimumSize(QSize(60, 28))
        self.label_modes.setMaximumSize(QSize(60, 28))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_modes.setFont(font2)
        self.label_modes.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_modes, 0, 1, 1, 1)

        self.lineEdit_number_modes = QLineEdit(self.frame_modes)
        self.lineEdit_number_modes.setObjectName(u"lineEdit_number_modes")
        self.lineEdit_number_modes.setMinimumSize(QSize(80, 28))
        self.lineEdit_number_modes.setMaximumSize(QSize(80, 28))
        self.lineEdit_number_modes.setFont(font2)
        self.lineEdit_number_modes.setStyleSheet(u"")
        self.lineEdit_number_modes.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_number_modes, 0, 2, 1, 1)

        self.label_spacing = QLabel(self.frame_modes)
        self.label_spacing.setObjectName(u"label_spacing")
        self.label_spacing.setMinimumSize(QSize(60, 28))
        self.label_spacing.setMaximumSize(QSize(60, 28))
        self.label_spacing.setFont(font2)
        self.label_spacing.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_spacing, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_modes, 0, 0, 1, 1)

        self.frame_sigma = QFrame(self.frame_main)
        self.frame_sigma.setObjectName(u"frame_sigma")
        self.frame_sigma.setMinimumSize(QSize(0, 40))
        self.frame_sigma.setMaximumSize(QSize(16777215, 40))
        self.frame_sigma.setFrameShape(QFrame.NoFrame)
        self.frame_sigma.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_sigma)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_sigma_unit = QLabel(self.frame_sigma)
        self.label_sigma_unit.setObjectName(u"label_sigma_unit")
        self.label_sigma_unit.setMinimumSize(QSize(60, 28))
        self.label_sigma_unit.setMaximumSize(QSize(60, 28))
        self.label_sigma_unit.setFont(font2)
        self.label_sigma_unit.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_sigma_unit, 0, 3, 1, 1)

        self.label_sigma = QLabel(self.frame_sigma)
        self.label_sigma.setObjectName(u"label_sigma")
        self.label_sigma.setMinimumSize(QSize(60, 28))
        self.label_sigma.setMaximumSize(QSize(60, 28))
        self.label_sigma.setFont(font2)
        self.label_sigma.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_sigma, 0, 1, 1, 1)

        self.lineEdit_sigma_factor = QLineEdit(self.frame_sigma)
        self.lineEdit_sigma_factor.setObjectName(u"lineEdit_sigma_factor")
        self.lineEdit_sigma_factor.setMinimumSize(QSize(80, 28))
        self.lineEdit_sigma_factor.setMaximumSize(QSize(80, 28))
        self.lineEdit_sigma_factor.setFont(font2)
        self.lineEdit_sigma_factor.setStyleSheet(u"")
        self.lineEdit_sigma_factor.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_sigma_factor, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.gridLayout_3.addWidget(self.frame_sigma, 1, 0, 1, 1)

        self.frame_button = QFrame(self.frame_main)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 40))
        self.frame_button.setMaximumSize(QSize(16777215, 40))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_button)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_run_analysis = QPushButton(self.frame_button)
        self.pushButton_run_analysis.setObjectName(u"pushButton_run_analysis")
        self.pushButton_run_analysis.setMinimumSize(QSize(100, 28))
        self.pushButton_run_analysis.setMaximumSize(QSize(100, 28))
        self.pushButton_run_analysis.setFont(font2)
        self.pushButton_run_analysis.setStyleSheet(u"")
        self.pushButton_run_analysis.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_run_analysis, 0, 1, 1, 1)

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
        self.pushButton_enter_setup.setAutoDefault(False)

        self.gridLayout_11.addWidget(self.pushButton_enter_setup, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_button, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Modal analysis setup", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Structural modal analysis setup", None))
        self.label_modes.setText(QCoreApplication.translate("Dialog", u"Modes:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_number_modes.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Number of modes to find in acoustic modal analysis</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_number_modes.setText(QCoreApplication.translate("Dialog", u"40", None))
        self.label_spacing.setText("")
        self.label_sigma_unit.setText(QCoreApplication.translate("Dialog", u"[Hz]", None))
        self.label_sigma.setText(QCoreApplication.translate("Dialog", u"Sigma:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_sigma_factor.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>This parameter allows to find eigenvalues near 'Sigma' value using shift-invert mode.</p><p>&gt; See scipy.sparse.linalg.eigs for more details.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_sigma_factor.setText(QCoreApplication.translate("Dialog", u"1e-2", None))
        self.pushButton_run_analysis.setText(QCoreApplication.translate("Dialog", u"Run analysis", None))
        self.pushButton_enter_setup.setText(QCoreApplication.translate("Dialog", u"Enter setup", None))
    # retranslateUi



class ModalAnalysisSetupInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_modes: QFrame
                                - (Layout): QGridLayout
                                        - label_modes: QLabel
                                        - lineEdit_number_modes: QLineEdit
                                        - label_spacing: QLabel
                            - frame_sigma: QFrame
                                - (Layout): QGridLayout
                                        - label_sigma_unit: QLabel
                                        - label_sigma: QLabel
                                        - lineEdit_sigma_factor: QLineEdit
                            - frame_button: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_run_analysis: QPushButton
                                        - pushButton_enter_setup: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
