# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_model_results.ui'
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
    QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 320)
        Dialog.setMinimumSize(QSize(400, 320))
        Dialog.setMaximumSize(QSize(464, 320))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setFrameShape(QFrame.Box)
        self.frame_lower.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_lower)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(6)
        self.gridLayout_3.setContentsMargins(8, 8, 8, 8)
        self.frame_14 = QFrame(self.frame_lower)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 120))
        self.frame_14.setMaximumSize(QSize(16777215, 120))
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_14)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(4, 0, 4, 0)
        self.pushButton_choose_folder_export = QPushButton(self.frame_14)
        self.pushButton_choose_folder_export.setObjectName(u"pushButton_choose_folder_export")
        self.pushButton_choose_folder_export.setMinimumSize(QSize(40, 30))
        self.pushButton_choose_folder_export.setMaximumSize(QSize(40, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        self.pushButton_choose_folder_export.setFont(font)
        self.pushButton_choose_folder_export.setStyleSheet(u"")
        icon = Icon(u":/icons/common/import.png")
        self.pushButton_choose_folder_export.setIcon(icon)
        self.pushButton_choose_folder_export.setIconSize(QSize(20, 20))

        self.gridLayout_15.addWidget(self.pushButton_choose_folder_export, 1, 1, 1, 1)

        self.lineEdit_save_results_path = QLineEdit(self.frame_14)
        self.lineEdit_save_results_path.setObjectName(u"lineEdit_save_results_path")
        self.lineEdit_save_results_path.setEnabled(False)
        self.lineEdit_save_results_path.setMinimumSize(QSize(0, 30))
        self.lineEdit_save_results_path.setMaximumSize(QSize(16777215, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_save_results_path.setFont(font1)
        self.lineEdit_save_results_path.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_save_results_path.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_save_results_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_save_results_path, 1, 0, 1, 1)

        self.lineEdit_file_name = QLineEdit(self.frame_14)
        self.lineEdit_file_name.setObjectName(u"lineEdit_file_name")
        self.lineEdit_file_name.setMinimumSize(QSize(0, 30))
        self.lineEdit_file_name.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_file_name.setFont(font2)
        self.lineEdit_file_name.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_file_name.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}")
        self.lineEdit_file_name.setAlignment(Qt.AlignCenter)
        self.lineEdit_file_name.setClearButtonEnabled(True)

        self.gridLayout_15.addWidget(self.lineEdit_file_name, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_14, 1, 0, 1, 1)

        self.label_data_information = QLabel(self.frame_lower)
        self.label_data_information.setObjectName(u"label_data_information")
        self.label_data_information.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(10)
        self.label_data_information.setFont(font3)
        self.label_data_information.setFrameShape(QFrame.StyledPanel)
        self.label_data_information.setAlignment(Qt.AlignCenter)
        self.label_data_information.setWordWrap(True)
        self.label_data_information.setMargin(2)

        self.gridLayout_3.addWidget(self.label_data_information, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_lower, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setSizeIncrement(QSize(0, 0))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setMaximumSize(QSize(600, 48))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setKerning(False)
        self.label.setFont(font4)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_15 = QFrame(Dialog)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 48))
        self.frame_15.setMaximumSize(QSize(16777215, 48))
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_15)
        self.gridLayout_16.setSpacing(2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(2, 2, 2, 2)
        self.pushButton_export_results = QPushButton(self.frame_15)
        self.pushButton_export_results.setObjectName(u"pushButton_export_results")
        self.pushButton_export_results.setMinimumSize(QSize(120, 30))
        self.pushButton_export_results.setMaximumSize(QSize(120, 30))
        self.pushButton_export_results.setFont(font2)
        self.pushButton_export_results.setStyleSheet(u"")

        self.gridLayout_16.addWidget(self.pushButton_export_results, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_15, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_file_name, self.lineEdit_save_results_path)
        QWidget.setTabOrder(self.lineEdit_save_results_path, self.pushButton_choose_folder_export)
        QWidget.setTabOrder(self.pushButton_choose_folder_export, self.pushButton_export_results)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Export selected model result", None))
#if QT_CONFIG(tooltip)
        self.pushButton_choose_folder_export.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:400;\">Search a folder</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.pushButton_choose_folder_export.setWhatsThis(QCoreApplication.translate("Dialog", u"Choose a folder to export the model results.", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_choose_folder_export.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_save_results_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose a folder to export the selected data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_file_name.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Insert a filename</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_file_name.setText("")
        self.label_data_information.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Export selected model result", None))
        self.pushButton_export_results.setText(QCoreApplication.translate("Dialog", u"Export results", None))
    # retranslateUi



class ExportModelResults_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - frame_14: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_choose_folder_export: QPushButton
                                        - lineEdit_save_results_path: QLineEdit
                                        - lineEdit_file_name: QLineEdit
                            - label_data_information: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_15: QFrame
                    - (Layout): QGridLayout
                            - pushButton_export_results: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
