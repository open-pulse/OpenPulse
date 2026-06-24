# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_loading_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_loading_window(object):
    def setupUi(self, loading_window):
        if not loading_window.objectName():
            loading_window.setObjectName(u"loading_window")
        loading_window.setWindowModality(Qt.ApplicationModal)
        loading_window.resize(377, 145)
        self.verticalLayout = QVBoxLayout(loading_window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.progress_label = QLabel(loading_window)
        self.progress_label.setObjectName(u"progress_label")
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar(loading_window)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(10)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout.addWidget(self.progress_bar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(loading_window)

        QMetaObject.connectSlotsByName(loading_window)
    # setupUi

    def retranslateUi(self, loading_window):
        loading_window.setWindowTitle(QCoreApplication.translate("loading_window", u"Loading Window", None))
        self.progress_label.setText(QCoreApplication.translate("loading_window", u"Loading ...", None))
    # retranslateUi



class NewLoadingWindow_UI(QWidget, Ui_loading_window):
    """
    Component Hierarchy:
    - loading_window: QWidget
        - (Layout): QVBoxLayout
                - progress_label: QLabel
                - progress_bar: QProgressBar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
