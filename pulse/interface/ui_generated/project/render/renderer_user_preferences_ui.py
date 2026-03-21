# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'renderer_user_preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(480, 520)
        Dialog.setMinimumSize(QSize(480, 520))
        Dialog.setMaximumSize(QSize(480, 520))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(600, 42))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_10 = QGridLayout(self.frame_title)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 28))
        self.label_title.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(11)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.NoFrame)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(600, 500))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(240, 120))
        self.frame_6.setMaximumSize(QSize(16777215, 80))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_6)
        self.gridLayout_14.setSpacing(4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 4, 4, 4)
        self.checkBox_OpenPulse_logo = QCheckBox(self.frame_6)
        self.checkBox_OpenPulse_logo.setObjectName(u"checkBox_OpenPulse_logo")
        self.checkBox_OpenPulse_logo.setMinimumSize(QSize(160, 26))
        self.checkBox_OpenPulse_logo.setMaximumSize(QSize(180, 26))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.checkBox_OpenPulse_logo.setFont(font1)
        self.checkBox_OpenPulse_logo.setChecked(True)

        self.gridLayout_14.addWidget(self.checkBox_OpenPulse_logo, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.checkBox_reference_scale = QCheckBox(self.frame_6)
        self.checkBox_reference_scale.setObjectName(u"checkBox_reference_scale")
        self.checkBox_reference_scale.setMinimumSize(QSize(160, 26))
        self.checkBox_reference_scale.setMaximumSize(QSize(180, 26))
        self.checkBox_reference_scale.setFont(font1)
        self.checkBox_reference_scale.setChecked(True)

        self.gridLayout_14.addWidget(self.checkBox_reference_scale, 1, 1, 1, 1)

        self.checkBox_compatibility_mode = QCheckBox(self.frame_6)
        self.checkBox_compatibility_mode.setObjectName(u"checkBox_compatibility_mode")
        self.checkBox_compatibility_mode.setEnabled(True)
        self.checkBox_compatibility_mode.setMinimumSize(QSize(160, 26))
        self.checkBox_compatibility_mode.setMaximumSize(QSize(180, 26))
        self.checkBox_compatibility_mode.setFont(font1)
        self.checkBox_compatibility_mode.setChecked(False)

        self.gridLayout_14.addWidget(self.checkBox_compatibility_mode, 2, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_6, 0, 0, 1, 1, Qt.AlignTop)

        self.frame_background_color_2 = QFrame(self.frame)
        self.frame_background_color_2.setObjectName(u"frame_background_color_2")
        self.frame_background_color_2.setMinimumSize(QSize(320, 280))
        self.frame_background_color_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_background_color_2.setFrameShape(QFrame.NoFrame)
        self.frame_background_color_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_background_color_2)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setHorizontalSpacing(8)
        self.gridLayout_20.setVerticalSpacing(4)
        self.gridLayout_20.setContentsMargins(4, 4, 4, 4)
        self.pushButton_tubes_color = QPushButton(self.frame_background_color_2)
        self.pushButton_tubes_color.setObjectName(u"pushButton_tubes_color")
        self.pushButton_tubes_color.setMinimumSize(QSize(90, 26))
        self.pushButton_tubes_color.setMaximumSize(QSize(90, 26))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(8)
        self.pushButton_tubes_color.setFont(font2)
        self.pushButton_tubes_color.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.pushButton_tubes_color, 7, 3, 1, 1)

        self.label_3 = QLabel(self.frame_background_color_2)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setPointSize(8)
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_3, 8, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.pushButton_lines_color = QPushButton(self.frame_background_color_2)
        self.pushButton_lines_color.setObjectName(u"pushButton_lines_color")
        self.pushButton_lines_color.setMinimumSize(QSize(90, 26))
        self.pushButton_lines_color.setMaximumSize(QSize(90, 26))
        self.pushButton_lines_color.setFont(font3)
        self.pushButton_lines_color.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.pushButton_lines_color, 6, 3, 1, 1)

        self.lineEdit_renderer_background_color_1 = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_background_color_1.setObjectName(u"lineEdit_renderer_background_color_1")
        self.lineEdit_renderer_background_color_1.setEnabled(False)
        self.lineEdit_renderer_background_color_1.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_background_color_1.setMaximumSize(QSize(90, 26))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setItalic(False)
        self.lineEdit_renderer_background_color_1.setFont(font4)
        self.lineEdit_renderer_background_color_1.setStyleSheet(u"")
        self.lineEdit_renderer_background_color_1.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_background_color_1, 1, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.lineEdit_renderer_font_size = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_font_size.setObjectName(u"lineEdit_renderer_font_size")
        self.lineEdit_renderer_font_size.setEnabled(True)
        self.lineEdit_renderer_font_size.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_font_size.setMaximumSize(QSize(90, 26))
        self.lineEdit_renderer_font_size.setFont(font3)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_font_size, 8, 2, 1, 1)

        self.label_2 = QLabel(self.frame_background_color_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(160)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(160, 32))
        self.label_2.setMaximumSize(QSize(160, 32))
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_2, 8, 1, 1, 1)

        self.label = QLabel(self.frame_background_color_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(170, 32))
        self.label.setMaximumSize(QSize(170, 32))
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label.setWordWrap(False)

        self.gridLayout_20.addWidget(self.label, 2, 1, 1, 1)

        self.label_10 = QLabel(self.frame_background_color_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(170, 32))
        self.label_10.setMaximumSize(QSize(170, 32))
        self.label_10.setFont(font3)
        self.label_10.setFrameShape(QFrame.NoFrame)
        self.label_10.setFrameShadow(QFrame.Raised)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_10, 1, 1, 1, 1)

        self.lineEdit_renderer_font_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_font_color.setObjectName(u"lineEdit_renderer_font_color")
        self.lineEdit_renderer_font_color.setEnabled(False)
        self.lineEdit_renderer_font_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_font_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_renderer_font_color.setFont(font4)
        self.lineEdit_renderer_font_color.setStyleSheet(u"")
        self.lineEdit_renderer_font_color.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_font_color, 4, 2, 1, 1)

        self.pushButton_renderer_font_color = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_font_color.setObjectName(u"pushButton_renderer_font_color")
        self.pushButton_renderer_font_color.setMinimumSize(QSize(90, 26))
        self.pushButton_renderer_font_color.setMaximumSize(QSize(90, 26))
        self.pushButton_renderer_font_color.setFont(font3)
        self.pushButton_renderer_font_color.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.pushButton_renderer_font_color, 4, 3, 1, 1)

        self.pushButton_renderer_background_color_2 = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_background_color_2.setObjectName(u"pushButton_renderer_background_color_2")
        self.pushButton_renderer_background_color_2.setMinimumSize(QSize(90, 26))
        self.pushButton_renderer_background_color_2.setMaximumSize(QSize(90, 26))
        self.pushButton_renderer_background_color_2.setFont(font3)

        self.gridLayout_20.addWidget(self.pushButton_renderer_background_color_2, 2, 3, 1, 1)

        self.lineEdit_nodes_points_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_nodes_points_color.setObjectName(u"lineEdit_nodes_points_color")
        self.lineEdit_nodes_points_color.setEnabled(False)
        self.lineEdit_nodes_points_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_nodes_points_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_nodes_points_color.setFont(font4)
        self.lineEdit_nodes_points_color.setStyleSheet(u"")
        self.lineEdit_nodes_points_color.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.lineEdit_nodes_points_color, 5, 2, 1, 1)

        self.lineEdit_tubes_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_tubes_color.setObjectName(u"lineEdit_tubes_color")
        self.lineEdit_tubes_color.setEnabled(False)
        self.lineEdit_tubes_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_tubes_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_tubes_color.setFont(font4)
        self.lineEdit_tubes_color.setStyleSheet(u"")
        self.lineEdit_tubes_color.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.lineEdit_tubes_color, 7, 2, 1, 1)

        self.lineEdit_renderer_background_color_2 = QLineEdit(self.frame_background_color_2)
        self.lineEdit_renderer_background_color_2.setObjectName(u"lineEdit_renderer_background_color_2")
        self.lineEdit_renderer_background_color_2.setEnabled(False)
        self.lineEdit_renderer_background_color_2.setMinimumSize(QSize(90, 26))
        self.lineEdit_renderer_background_color_2.setMaximumSize(QSize(90, 26))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        font5.setPointSize(11)
        self.lineEdit_renderer_background_color_2.setFont(font5)

        self.gridLayout_20.addWidget(self.lineEdit_renderer_background_color_2, 2, 2, 1, 1)

        self.lineEdit_lines_color = QLineEdit(self.frame_background_color_2)
        self.lineEdit_lines_color.setObjectName(u"lineEdit_lines_color")
        self.lineEdit_lines_color.setEnabled(False)
        self.lineEdit_lines_color.setMinimumSize(QSize(90, 26))
        self.lineEdit_lines_color.setMaximumSize(QSize(90, 26))
        self.lineEdit_lines_color.setFont(font4)
        self.lineEdit_lines_color.setStyleSheet(u"")
        self.lineEdit_lines_color.setAlignment(Qt.AlignCenter)

        self.gridLayout_20.addWidget(self.lineEdit_lines_color, 6, 2, 1, 1)

        self.pushButton_renderer_background_color_1 = QPushButton(self.frame_background_color_2)
        self.pushButton_renderer_background_color_1.setObjectName(u"pushButton_renderer_background_color_1")
        self.pushButton_renderer_background_color_1.setMinimumSize(QSize(90, 26))
        self.pushButton_renderer_background_color_1.setMaximumSize(QSize(90, 26))
        self.pushButton_renderer_background_color_1.setFont(font3)
        self.pushButton_renderer_background_color_1.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.pushButton_renderer_background_color_1, 1, 3, 1, 1)

        self.label_8 = QLabel(self.frame_background_color_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(160, 32))
        self.label_8.setMaximumSize(QSize(160, 32))
        self.label_8.setFont(font3)
        self.label_8.setFrameShape(QFrame.NoFrame)
        self.label_8.setFrameShadow(QFrame.Raised)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_8, 7, 1, 1, 1)

        self.pushButton_nodes_points_color = QPushButton(self.frame_background_color_2)
        self.pushButton_nodes_points_color.setObjectName(u"pushButton_nodes_points_color")
        self.pushButton_nodes_points_color.setMinimumSize(QSize(90, 26))
        self.pushButton_nodes_points_color.setMaximumSize(QSize(90, 26))
        self.pushButton_nodes_points_color.setFont(font3)
        self.pushButton_nodes_points_color.setStyleSheet(u"")

        self.gridLayout_20.addWidget(self.pushButton_nodes_points_color, 5, 3, 1, 1)

        self.label_7 = QLabel(self.frame_background_color_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(160, 32))
        self.label_7.setMaximumSize(QSize(160, 32))
        self.label_7.setFont(font3)
        self.label_7.setFrameShape(QFrame.NoFrame)
        self.label_7.setFrameShadow(QFrame.Raised)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_7, 6, 1, 1, 1)

        self.label_12 = QLabel(self.frame_background_color_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(160, 32))
        self.label_12.setMaximumSize(QSize(160, 32))
        self.label_12.setFont(font3)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setFrameShadow(QFrame.Raised)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_12, 4, 1, 1, 1)

        self.label_6 = QLabel(self.frame_background_color_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(160, 32))
        self.label_6.setMaximumSize(QSize(160, 32))
        self.label_6.setFont(font3)
        self.label_6.setFrameShape(QFrame.NoFrame)
        self.label_6.setFrameShadow(QFrame.Raised)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_20.addWidget(self.label_6, 5, 1, 1, 1)


        self.gridLayout_3.addWidget(self.frame_background_color_2, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 48))
        self.frame_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_buttons)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.pushButton_apply_settings = QPushButton(self.frame_buttons)
        self.pushButton_apply_settings.setObjectName(u"pushButton_apply_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_apply_settings.sizePolicy().hasHeightForWidth())
        self.pushButton_apply_settings.setSizePolicy(sizePolicy1)
        self.pushButton_apply_settings.setMinimumSize(QSize(140, 30))
        self.pushButton_apply_settings.setMaximumSize(QSize(140, 30))
        self.pushButton_apply_settings.setFont(font3)

        self.gridLayout.addWidget(self.pushButton_apply_settings, 0, 2, 1, 1)

        self.pushButton_update_settings = QPushButton(self.frame_buttons)
        self.pushButton_update_settings.setObjectName(u"pushButton_update_settings")
        self.pushButton_update_settings.setMinimumSize(QSize(140, 30))
        self.pushButton_update_settings.setMaximumSize(QSize(140, 30))
        self.pushButton_update_settings.setFont(font3)
        self.pushButton_update_settings.setStyleSheet(u"")
        self.pushButton_update_settings.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_update_settings, 0, 3, 1, 1)

        self.pushButton_reset_to_default = QPushButton(self.frame_buttons)
        self.pushButton_reset_to_default.setObjectName(u"pushButton_reset_to_default")
        self.pushButton_reset_to_default.setMinimumSize(QSize(140, 30))
        self.pushButton_reset_to_default.setMaximumSize(QSize(140, 30))
        self.pushButton_reset_to_default.setFont(font3)
        self.pushButton_reset_to_default.setStyleSheet(u"")
        self.pushButton_reset_to_default.setAutoDefault(False)

        self.gridLayout.addWidget(self.pushButton_reset_to_default, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.checkBox_OpenPulse_logo, self.checkBox_reference_scale)
        QWidget.setTabOrder(self.checkBox_reference_scale, self.lineEdit_renderer_background_color_1)
        QWidget.setTabOrder(self.lineEdit_renderer_background_color_1, self.pushButton_renderer_background_color_1)
        QWidget.setTabOrder(self.pushButton_renderer_background_color_1, self.lineEdit_renderer_font_color)
        QWidget.setTabOrder(self.lineEdit_renderer_font_color, self.pushButton_renderer_font_color)
        QWidget.setTabOrder(self.pushButton_renderer_font_color, self.lineEdit_nodes_points_color)
        QWidget.setTabOrder(self.lineEdit_nodes_points_color, self.pushButton_nodes_points_color)
        QWidget.setTabOrder(self.pushButton_nodes_points_color, self.lineEdit_lines_color)
        QWidget.setTabOrder(self.lineEdit_lines_color, self.pushButton_lines_color)
        QWidget.setTabOrder(self.pushButton_lines_color, self.lineEdit_tubes_color)
        QWidget.setTabOrder(self.lineEdit_tubes_color, self.pushButton_tubes_color)
        QWidget.setTabOrder(self.pushButton_tubes_color, self.pushButton_reset_to_default)
        QWidget.setTabOrder(self.pushButton_reset_to_default, self.pushButton_update_settings)

        self.retranslateUi(Dialog)

        self.pushButton_update_settings.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Interface visibility settings", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"User interface visibility settings", None))
        self.checkBox_OpenPulse_logo.setText(QCoreApplication.translate("Dialog", u"Show OpenPulse logo", None))
        self.checkBox_reference_scale.setText(QCoreApplication.translate("Dialog", u"Show reference scale", None))
#if QT_CONFIG(tooltip)
        self.checkBox_compatibility_mode.setToolTip(QCoreApplication.translate("Dialog", u"If the points are not being shown in your renderers, try this option.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_compatibility_mode.setText(QCoreApplication.translate("Dialog", u"Compatibility mode", None))
        self.pushButton_tubes_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"pt", None))
        self.pushButton_lines_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Renderer font size", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Renderer background color 2:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Renderer background color 1:", None))
        self.pushButton_renderer_font_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_renderer_background_color_2.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.pushButton_renderer_background_color_1.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Tubes color:", None))
        self.pushButton_nodes_points_color.setText(QCoreApplication.translate("Dialog", u"Pick color", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Lines color:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Renderer font color:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Nodes/Points color:", None))
        self.pushButton_apply_settings.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.pushButton_update_settings.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pushButton_reset_to_default.setText(QCoreApplication.translate("Dialog", u"Reset", None))
    # retranslateUi



class RendererUserPreferences_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_OpenPulse_logo: QCheckBox
                                        - checkBox_reference_scale: QCheckBox
                                        - checkBox_compatibility_mode: QCheckBox
                            - frame_background_color_2: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_tubes_color: QPushButton
                                        - label_3: QLabel
                                        - pushButton_lines_color: QPushButton
                                        - lineEdit_renderer_background_color_1: QLineEdit
                                        - lineEdit_renderer_font_size: QLineEdit
                                        - label_2: QLabel
                                        - label: QLabel
                                        - label_10: QLabel
                                        - lineEdit_renderer_font_color: QLineEdit
                                        - pushButton_renderer_font_color: QPushButton
                                        - pushButton_renderer_background_color_2: QPushButton
                                        - lineEdit_nodes_points_color: QLineEdit
                                        - lineEdit_tubes_color: QLineEdit
                                        - lineEdit_renderer_background_color_2: QLineEdit
                                        - lineEdit_lines_color: QLineEdit
                                        - pushButton_renderer_background_color_1: QPushButton
                                        - label_8: QLabel
                                        - pushButton_nodes_points_color: QPushButton
                                        - label_7: QLabel
                                        - label_12: QLabel
                                        - label_6: QLabel
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply_settings: QPushButton
                            - pushButton_update_settings: QPushButton
                            - pushButton_reset_to_default: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
