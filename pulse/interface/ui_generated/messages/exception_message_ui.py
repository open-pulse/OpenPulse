# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exception_message.ui'
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
    QLabel, QPushButton, QSizePolicy, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        Dialog.resize(701, 240)
        Dialog.setMinimumSize(QSize(500, 240))
        Dialog.setMaximumSize(QSize(900, 600))
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.title_label = QLabel(self.frame_title)
        self.title_label.setObjectName(u"title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setMaximumSize(QSize(16777215, 50))
        self.title_label.setBaseSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.title_label, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_title)

        self.frame_short_message = QFrame(Dialog)
        self.frame_short_message.setObjectName(u"frame_short_message")
        self.frame_short_message.setMinimumSize(QSize(0, 40))
        font1 = QFont()
        font1.setPointSize(9)
        self.frame_short_message.setFont(font1)
        self.frame_short_message.setFrameShape(QFrame.Shape.Box)
        self.frame_short_message.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.frame_short_message)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.error_message = QLabel(self.frame_short_message)
        self.error_message.setObjectName(u"error_message")
        sizePolicy.setHeightForWidth(self.error_message.sizePolicy().hasHeightForWidth())
        self.error_message.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(10)
        self.error_message.setFont(font2)
        self.error_message.setTextFormat(Qt.TextFormat.PlainText)
        self.error_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_message.setWordWrap(True)
        self.error_message.setMargin(10)

        self.verticalLayout_2.addWidget(self.error_message)


        self.verticalLayout.addWidget(self.frame_short_message)

        self.stack_trace_text_browser = QTextBrowser(Dialog)
        self.stack_trace_text_browser.setObjectName(u"stack_trace_text_browser")
        self.stack_trace_text_browser.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stack_trace_text_browser.sizePolicy().hasHeightForWidth())
        self.stack_trace_text_browser.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setFamilies([u"Courier"])
        font3.setPointSize(10)
        font3.setKerning(True)
        self.stack_trace_text_browser.setFont(font3)
        self.stack_trace_text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.stack_trace_text_browser.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self.verticalLayout.addWidget(self.stack_trace_text_browser)

        self.frame_button = QFrame(Dialog)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 40))
        self.frame_button.setMaximumSize(QSize(16777215, 40))
        self.frame_button.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_button)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.ok_button = QPushButton(self.frame_button)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setMinimumSize(QSize(145, 0))
        self.ok_button.setMaximumSize(QSize(145, 16777215))
        self.ok_button.setBaseSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.ok_button, 0, 3, 1, 1)

        self.copy_log_button = QPushButton(self.frame_button)
        self.copy_log_button.setObjectName(u"copy_log_button")
        self.copy_log_button.setMinimumSize(QSize(145, 0))
        self.copy_log_button.setMaximumSize(QSize(145, 16777215))

        self.gridLayout_2.addWidget(self.copy_log_button, 0, 1, 1, 1)

        self.copy_stacktrace_button = QPushButton(self.frame_button)
        self.copy_stacktrace_button.setObjectName(u"copy_stacktrace_button")
        self.copy_stacktrace_button.setMinimumSize(QSize(145, 0))
        self.copy_stacktrace_button.setMaximumSize(QSize(145, 16777215))
        self.copy_stacktrace_button.setFont(font)

        self.gridLayout_2.addWidget(self.copy_stacktrace_button, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frame_button)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.error_message.setText(QCoreApplication.translate("Dialog", u"Short message explaining the error", None))
        self.stack_trace_text_browser.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Courier'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cascadia Code'; font-size:9pt;\">Stack trace containing only the last few calls</span></p></body></html>", None))
        self.ok_button.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.copy_log_button.setText(QCoreApplication.translate("Dialog", u"Copy Logs", None))
        self.copy_stacktrace_button.setText(QCoreApplication.translate("Dialog", u"Copy Stacktrace", None))
    # retranslateUi



class ExceptionMessage_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QVBoxLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - title_label: QLabel
                - frame_short_message: QFrame
                    - (Layout): QVBoxLayout
                            - error_message: QLabel
                - stack_trace_text_browser: QTextBrowser
                - frame_button: QFrame
                    - (Layout): QGridLayout
                            - ok_button: QPushButton
                            - copy_log_button: QPushButton
                            - copy_stacktrace_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
