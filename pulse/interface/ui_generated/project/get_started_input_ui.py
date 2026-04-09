# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_started_input.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(650, 424)
        Form.setMinimumSize(QSize(650, 424))
        Form.setMaximumSize(QSize(650, 424))
        Form.setSizeIncrement(QSize(0, 0))
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMaximumSize(QSize(16777215, 80))
        self.frame_title.setFrameShape(QFrame.NoFrame)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_openpulse = QLabel(self.frame_title)
        self.label_openpulse.setObjectName(u"label_openpulse")
        self.label_openpulse.setMinimumSize(QSize(0, 40))
        self.label_openpulse.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"Bauhaus 93"])
        font.setPointSize(26)
        font.setBold(True)
        self.label_openpulse.setFont(font)
        self.label_openpulse.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_openpulse, 0, 0, 1, 1)

        self.label_description = QLabel(self.frame_title)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setMinimumSize(QSize(0, 25))
        self.label_description.setMaximumSize(QSize(16777215, 25))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_description.setFont(font1)
        self.label_description.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_description, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.widget_main = QWidget(Form)
        self.widget_main.setObjectName(u"widget_main")
        self.gridLayout_5 = QGridLayout(self.widget_main)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.frame_2 = QFrame(self.widget_main)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(406, 0))
        self.frame_2.setMaximumSize(QSize(406, 16777215))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.recents_label = QLabel(self.frame_2)
        self.recents_label.setObjectName(u"recents_label")
        self.recents_label.setMinimumSize(QSize(0, 30))
        self.recents_label.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(False)
        self.recents_label.setFont(font2)
        self.recents_label.setAutoFillBackground(True)
        self.recents_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.recents_label, 0, 0, 1, 1)

        self.project_path_label_1 = QLabel(self.frame_2)
        self.project_path_label_1.setObjectName(u"project_path_label_1")
        self.project_path_label_1.setMinimumSize(QSize(320, 52))
        self.project_path_label_1.setMaximumSize(QSize(320, 52))
        self.project_path_label_1.setStyleSheet(u"")
        self.project_path_label_1.setFrameShape(QFrame.Box)
        self.project_path_label_1.setScaledContents(True)
        self.project_path_label_1.setAlignment(Qt.AlignCenter)
        self.project_path_label_1.setWordWrap(True)
        self.project_path_label_1.setMargin(6)
        self.project_path_label_1.setIndent(0)

        self.gridLayout_4.addWidget(self.project_path_label_1, 1, 0, 1, 1)

        self.project_button_1 = QPushButton(self.frame_2)
        self.project_button_1.setObjectName(u"project_button_1")
        self.project_button_1.setMinimumSize(QSize(80, 52))
        self.project_button_1.setMaximumSize(QSize(80, 52))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.project_button_1.setFont(font3)
        self.project_button_1.setLayoutDirection(Qt.LeftToRight)
        self.project_button_1.setAutoFillBackground(False)
        self.project_button_1.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/002-analysis.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.project_button_1.setIcon(icon)
        self.project_button_1.setAutoDefault(False)
        self.project_button_1.setFlat(False)

        self.gridLayout_4.addWidget(self.project_button_1, 1, 1, 1, 1)

        self.project_path_label_2 = QLabel(self.frame_2)
        self.project_path_label_2.setObjectName(u"project_path_label_2")
        self.project_path_label_2.setMinimumSize(QSize(320, 52))
        self.project_path_label_2.setMaximumSize(QSize(320, 52))
        self.project_path_label_2.setStyleSheet(u"")
        self.project_path_label_2.setFrameShape(QFrame.Box)
        self.project_path_label_2.setScaledContents(True)
        self.project_path_label_2.setAlignment(Qt.AlignCenter)
        self.project_path_label_2.setWordWrap(True)
        self.project_path_label_2.setMargin(6)
        self.project_path_label_2.setIndent(0)

        self.gridLayout_4.addWidget(self.project_path_label_2, 2, 0, 1, 1)

        self.project_path_label_3 = QLabel(self.frame_2)
        self.project_path_label_3.setObjectName(u"project_path_label_3")
        self.project_path_label_3.setMinimumSize(QSize(320, 52))
        self.project_path_label_3.setMaximumSize(QSize(320, 52))
        self.project_path_label_3.setFrameShape(QFrame.Box)
        self.project_path_label_3.setScaledContents(True)
        self.project_path_label_3.setAlignment(Qt.AlignCenter)
        self.project_path_label_3.setWordWrap(True)
        self.project_path_label_3.setMargin(6)
        self.project_path_label_3.setIndent(0)

        self.gridLayout_4.addWidget(self.project_path_label_3, 3, 0, 1, 1)

        self.project_button_2 = QPushButton(self.frame_2)
        self.project_button_2.setObjectName(u"project_button_2")
        self.project_button_2.setMinimumSize(QSize(80, 52))
        self.project_button_2.setMaximumSize(QSize(80, 52))
        self.project_button_2.setFont(font3)
        self.project_button_2.setLayoutDirection(Qt.LeftToRight)
        self.project_button_2.setAutoFillBackground(False)
        self.project_button_2.setStyleSheet(u"")
        self.project_button_2.setIcon(icon)
        self.project_button_2.setAutoDefault(False)
        self.project_button_2.setFlat(False)

        self.gridLayout_4.addWidget(self.project_button_2, 2, 1, 1, 1)

        self.project_path_label_5 = QLabel(self.frame_2)
        self.project_path_label_5.setObjectName(u"project_path_label_5")
        self.project_path_label_5.setMinimumSize(QSize(320, 52))
        self.project_path_label_5.setMaximumSize(QSize(320, 52))
        self.project_path_label_5.setFrameShape(QFrame.Box)
        self.project_path_label_5.setScaledContents(True)
        self.project_path_label_5.setAlignment(Qt.AlignCenter)
        self.project_path_label_5.setWordWrap(True)
        self.project_path_label_5.setMargin(6)
        self.project_path_label_5.setIndent(0)

        self.gridLayout_4.addWidget(self.project_path_label_5, 5, 0, 1, 1)

        self.project_button_3 = QPushButton(self.frame_2)
        self.project_button_3.setObjectName(u"project_button_3")
        self.project_button_3.setMinimumSize(QSize(80, 52))
        self.project_button_3.setMaximumSize(QSize(80, 52))
        self.project_button_3.setFont(font3)
        self.project_button_3.setLayoutDirection(Qt.LeftToRight)
        self.project_button_3.setAutoFillBackground(False)
        self.project_button_3.setStyleSheet(u"")
        self.project_button_3.setIcon(icon)
        self.project_button_3.setAutoDefault(False)
        self.project_button_3.setFlat(False)

        self.gridLayout_4.addWidget(self.project_button_3, 3, 1, 1, 1)

        self.project_button_4 = QPushButton(self.frame_2)
        self.project_button_4.setObjectName(u"project_button_4")
        self.project_button_4.setMinimumSize(QSize(80, 52))
        self.project_button_4.setMaximumSize(QSize(80, 52))
        self.project_button_4.setFont(font3)
        self.project_button_4.setLayoutDirection(Qt.LeftToRight)
        self.project_button_4.setAutoFillBackground(False)
        self.project_button_4.setStyleSheet(u"")
        self.project_button_4.setIcon(icon)
        self.project_button_4.setAutoDefault(False)
        self.project_button_4.setFlat(False)

        self.gridLayout_4.addWidget(self.project_button_4, 4, 1, 1, 1)

        self.project_path_label_4 = QLabel(self.frame_2)
        self.project_path_label_4.setObjectName(u"project_path_label_4")
        self.project_path_label_4.setMinimumSize(QSize(320, 52))
        self.project_path_label_4.setMaximumSize(QSize(320, 52))
        self.project_path_label_4.setFrameShape(QFrame.Box)
        self.project_path_label_4.setScaledContents(True)
        self.project_path_label_4.setAlignment(Qt.AlignCenter)
        self.project_path_label_4.setWordWrap(True)
        self.project_path_label_4.setMargin(6)
        self.project_path_label_4.setIndent(0)

        self.gridLayout_4.addWidget(self.project_path_label_4, 4, 0, 1, 1)

        self.project_button_5 = QPushButton(self.frame_2)
        self.project_button_5.setObjectName(u"project_button_5")
        self.project_button_5.setMinimumSize(QSize(80, 52))
        self.project_button_5.setMaximumSize(QSize(80, 52))
        self.project_button_5.setFont(font3)
        self.project_button_5.setLayoutDirection(Qt.LeftToRight)
        self.project_button_5.setAutoFillBackground(False)
        self.project_button_5.setStyleSheet(u"")
        self.project_button_5.setIcon(icon)
        self.project_button_5.setAutoDefault(False)
        self.project_button_5.setFlat(False)

        self.gridLayout_4.addWidget(self.project_button_5, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 6, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame = QFrame(self.widget_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(218, 0))
        self.frame.setMaximumSize(QSize(218, 16777215))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 0, 6, 0)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setMaximumSize(QSize(16777215, 30))
        self.label_4.setFont(font1)
        self.label_4.setAutoFillBackground(True)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.create_button = QPushButton(self.frame)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setMinimumSize(QSize(190, 52))
        self.create_button.setMaximumSize(QSize(190, 52))
        self.create_button.setFont(font3)
        self.create_button.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/common/new_file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.create_button.setIcon(icon1)
        self.create_button.setIconSize(QSize(30, 32))

        self.gridLayout.addWidget(self.create_button, 1, 0, 1, 1)

        self.load_button = QPushButton(self.frame)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setMinimumSize(QSize(190, 52))
        self.load_button.setMaximumSize(QSize(190, 52))
        self.load_button.setFont(font3)
        self.load_button.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/common/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.load_button.setIcon(icon2)
        self.load_button.setIconSize(QSize(30, 32))

        self.gridLayout.addWidget(self.load_button, 2, 0, 1, 1)

        self.reset_list_projects_button = QPushButton(self.frame)
        self.reset_list_projects_button.setObjectName(u"reset_list_projects_button")
        self.reset_list_projects_button.setMinimumSize(QSize(190, 52))
        self.reset_list_projects_button.setMaximumSize(QSize(190, 52))
        self.reset_list_projects_button.setFont(font3)
        self.reset_list_projects_button.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/common/reset-image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.reset_list_projects_button.setIcon(icon3)
        self.reset_list_projects_button.setIconSize(QSize(30, 32))

        self.gridLayout.addWidget(self.reset_list_projects_button, 3, 0, 1, 1)

        self.about_button = QPushButton(self.frame)
        self.about_button.setObjectName(u"about_button")
        self.about_button.setMinimumSize(QSize(190, 52))
        self.about_button.setMaximumSize(QSize(190, 52))
        self.about_button.setFont(font3)
        self.about_button.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/pulse/pulse_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.about_button.setIcon(icon4)
        self.about_button.setIconSize(QSize(30, 32))

        self.gridLayout.addWidget(self.about_button, 4, 0, 1, 1)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 52))
        self.frame_3.setMaximumSize(QSize(16777215, 52))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_3, 5, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 6, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.widget_main, 2, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 3, 0, 1, 1)

        QWidget.setTabOrder(self.project_button_1, self.project_button_2)
        QWidget.setTabOrder(self.project_button_2, self.project_button_3)
        QWidget.setTabOrder(self.project_button_3, self.project_button_4)
        QWidget.setTabOrder(self.project_button_4, self.project_button_5)
        QWidget.setTabOrder(self.project_button_5, self.create_button)
        QWidget.setTabOrder(self.create_button, self.load_button)
        QWidget.setTabOrder(self.load_button, self.reset_list_projects_button)
        QWidget.setTabOrder(self.reset_list_projects_button, self.about_button)

        self.retranslateUi(Form)

        self.project_button_1.setDefault(False)
        self.project_button_2.setDefault(False)
        self.project_button_3.setDefault(False)
        self.project_button_4.setDefault(False)
        self.project_button_5.setDefault(False)
        self.create_button.setDefault(False)
        self.load_button.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"OpenPulse - Get Started", None))
        self.label_openpulse.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" color:#0055ff;\">O</span>pen<span style=\" color:#0055ff;\">P</span>ulse</p></body></html>", None))
        self.label_description.setText(QCoreApplication.translate("Form", u"Open Source Software for Pulsation Analysis of Pipeline Systems", None))
        self.recents_label.setText(QCoreApplication.translate("Form", u"Recents Projects", None))
        self.project_path_label_1.setText(QCoreApplication.translate("Form", u"Project path 1", None))
        self.project_path_label_1.setProperty(u"status", QCoreApplication.translate("Form", u"project-path", None))
        self.project_button_1.setText(QCoreApplication.translate("Form", u"Load \n"
"project", None))
        self.project_path_label_2.setText(QCoreApplication.translate("Form", u"Project path 2", None))
        self.project_path_label_2.setProperty(u"status", QCoreApplication.translate("Form", u"project-path", None))
        self.project_path_label_3.setText(QCoreApplication.translate("Form", u"Project path 3", None))
        self.project_path_label_3.setProperty(u"status", QCoreApplication.translate("Form", u"project-path", None))
        self.project_button_2.setText(QCoreApplication.translate("Form", u"Load\n"
"Project", None))
        self.project_path_label_5.setText(QCoreApplication.translate("Form", u"Project path 5", None))
        self.project_path_label_5.setProperty(u"status", QCoreApplication.translate("Form", u"project-path", None))
        self.project_button_3.setText(QCoreApplication.translate("Form", u"Load\n"
"Project", None))
        self.project_button_4.setText(QCoreApplication.translate("Form", u"Load\n"
"Project", None))
        self.project_path_label_4.setText(QCoreApplication.translate("Form", u"Project path 4", None))
        self.project_path_label_4.setProperty(u"status", QCoreApplication.translate("Form", u"project-path", None))
        self.project_button_5.setText(QCoreApplication.translate("Form", u"Load\n"
"Project", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Get Started", None))
        self.create_button.setText(QCoreApplication.translate("Form", u"New Project", None))
        self.load_button.setText(QCoreApplication.translate("Form", u"Open Project", None))
        self.reset_list_projects_button.setText(QCoreApplication.translate("Form", u"Reset list of Projects", None))
        self.about_button.setText(QCoreApplication.translate("Form", u"About Open Pulse", None))
    # retranslateUi



class GetStartedInput_UI(QDialog, Ui_Form):
    """
    Component Hierarchy:
    - Form: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_openpulse: QLabel
                            - label_description: QLabel
                - widget_main: QWidget
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - recents_label: QLabel
                                        - project_path_label_1: QLabel
                                        - project_button_1: QPushButton
                                        - project_path_label_2: QLabel
                                        - project_path_label_3: QLabel
                                        - project_button_2: QPushButton
                                        - project_path_label_5: QLabel
                                        - project_button_3: QPushButton
                                        - project_button_4: QPushButton
                                        - project_path_label_4: QLabel
                                        - project_button_5: QPushButton
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - label_4: QLabel
                                        - create_button: QPushButton
                                        - load_button: QPushButton
                                        - reset_list_projects_button: QPushButton
                                        - about_button: QPushButton
                                        - frame_3: QFrame
                - line: Line
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
