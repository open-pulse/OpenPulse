# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'section_plane_inputs.ui'
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
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(392, 426)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(36, 0))
        self.label.setMaximumSize(QSize(36, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)

        self.relative_plane_position_x_spinbox = QSpinBox(self.frame_3)
        self.relative_plane_position_x_spinbox.setObjectName(u"relative_plane_position_x_spinbox")
        self.relative_plane_position_x_spinbox.setMinimumSize(QSize(60, 0))
        self.relative_plane_position_x_spinbox.setMaximumSize(QSize(60, 16777215))
        self.relative_plane_position_x_spinbox.setFont(font)
        self.relative_plane_position_x_spinbox.setAlignment(Qt.AlignCenter)
        self.relative_plane_position_x_spinbox.setMaximum(100)
        self.relative_plane_position_x_spinbox.setValue(50)

        self.gridLayout_3.addWidget(self.relative_plane_position_x_spinbox, 1, 2, 1, 1)

        self.relative_plane_position_z_spinbox = QSpinBox(self.frame_3)
        self.relative_plane_position_z_spinbox.setObjectName(u"relative_plane_position_z_spinbox")
        self.relative_plane_position_z_spinbox.setMinimumSize(QSize(60, 0))
        self.relative_plane_position_z_spinbox.setMaximumSize(QSize(60, 16777215))
        self.relative_plane_position_z_spinbox.setFont(font)
        self.relative_plane_position_z_spinbox.setAlignment(Qt.AlignCenter)
        self.relative_plane_position_z_spinbox.setMaximum(100)
        self.relative_plane_position_z_spinbox.setValue(50)

        self.gridLayout_3.addWidget(self.relative_plane_position_z_spinbox, 3, 2, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(36, 0))
        self.label_4.setMaximumSize(QSize(36, 16777215))
        self.label_4.setFont(font)

        self.gridLayout_3.addWidget(self.label_4, 1, 3, 1, 1)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(36, 0))
        self.label_2.setMaximumSize(QSize(36, 16777215))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)

        self.relative_plane_position_y_slider = QSlider(self.frame_3)
        self.relative_plane_position_y_slider.setObjectName(u"relative_plane_position_y_slider")
        self.relative_plane_position_y_slider.setMaximum(100)
        self.relative_plane_position_y_slider.setValue(50)
        self.relative_plane_position_y_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.relative_plane_position_y_slider, 2, 1, 1, 1)

        self.relative_plane_position_x_slider = QSlider(self.frame_3)
        self.relative_plane_position_x_slider.setObjectName(u"relative_plane_position_x_slider")
        self.relative_plane_position_x_slider.setMaximum(100)
        self.relative_plane_position_x_slider.setValue(50)
        self.relative_plane_position_x_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.relative_plane_position_x_slider, 1, 1, 1, 1)

        self.relative_plane_position_y_spinbox = QSpinBox(self.frame_3)
        self.relative_plane_position_y_spinbox.setObjectName(u"relative_plane_position_y_spinbox")
        self.relative_plane_position_y_spinbox.setMinimumSize(QSize(60, 0))
        self.relative_plane_position_y_spinbox.setMaximumSize(QSize(60, 16777215))
        self.relative_plane_position_y_spinbox.setFont(font)
        self.relative_plane_position_y_spinbox.setAlignment(Qt.AlignCenter)
        self.relative_plane_position_y_spinbox.setMaximum(100)
        self.relative_plane_position_y_spinbox.setValue(50)

        self.gridLayout_3.addWidget(self.relative_plane_position_y_spinbox, 2, 2, 1, 1)

        self.label_13 = QLabel(self.frame_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 22))
        self.label_13.setMaximumSize(QSize(16777215, 22))
        self.label_13.setFont(font)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_13, 0, 1, 1, 1)

        self.relative_plane_position_z_slider = QSlider(self.frame_3)
        self.relative_plane_position_z_slider.setObjectName(u"relative_plane_position_z_slider")
        self.relative_plane_position_z_slider.setMaximum(100)
        self.relative_plane_position_z_slider.setValue(50)
        self.relative_plane_position_z_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.relative_plane_position_z_slider, 3, 1, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(36, 0))
        self.label_3.setMaximumSize(QSize(36, 16777215))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(36, 0))
        self.label_5.setMaximumSize(QSize(36, 16777215))
        self.label_5.setFont(font)

        self.gridLayout_3.addWidget(self.label_5, 2, 3, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(36, 0))
        self.label_6.setMaximumSize(QSize(36, 16777215))
        self.label_6.setFont(font)

        self.gridLayout_3.addWidget(self.label_6, 3, 3, 1, 1)


        self.gridLayout_6.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.plane_rotation_z_spinbox = QSpinBox(self.frame_5)
        self.plane_rotation_z_spinbox.setObjectName(u"plane_rotation_z_spinbox")
        self.plane_rotation_z_spinbox.setMinimumSize(QSize(60, 0))
        self.plane_rotation_z_spinbox.setMaximumSize(QSize(60, 16777215))
        self.plane_rotation_z_spinbox.setFont(font)
        self.plane_rotation_z_spinbox.setAlignment(Qt.AlignCenter)
        self.plane_rotation_z_spinbox.setMaximum(360)

        self.gridLayout_5.addWidget(self.plane_rotation_z_spinbox, 3, 2, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(36, 0))
        self.label_8.setMaximumSize(QSize(36, 16777215))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_8, 2, 0, 1, 1)

        self.plane_rotation_z_slider = QSlider(self.frame_5)
        self.plane_rotation_z_slider.setObjectName(u"plane_rotation_z_slider")
        self.plane_rotation_z_slider.setMaximum(360)
        self.plane_rotation_z_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.plane_rotation_z_slider, 3, 1, 1, 1)

        self.plane_rotation_y_slider = QSlider(self.frame_5)
        self.plane_rotation_y_slider.setObjectName(u"plane_rotation_y_slider")
        self.plane_rotation_y_slider.setMaximum(360)
        self.plane_rotation_y_slider.setValue(90)
        self.plane_rotation_y_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.plane_rotation_y_slider, 2, 1, 1, 1)

        self.label_12 = QLabel(self.frame_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(36, 0))
        self.label_12.setMaximumSize(QSize(36, 16777215))
        self.label_12.setFont(font)

        self.gridLayout_5.addWidget(self.label_12, 3, 3, 1, 1)

        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(36, 0))
        self.label_9.setMaximumSize(QSize(36, 16777215))
        self.label_9.setFont(font)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_9, 3, 0, 1, 1)

        self.plane_rotation_x_slider = QSlider(self.frame_5)
        self.plane_rotation_x_slider.setObjectName(u"plane_rotation_x_slider")
        self.plane_rotation_x_slider.setMaximum(360)
        self.plane_rotation_x_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_5.addWidget(self.plane_rotation_x_slider, 1, 1, 1, 1)

        self.label_10 = QLabel(self.frame_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(36, 0))
        self.label_10.setMaximumSize(QSize(36, 16777215))
        self.label_10.setFont(font)

        self.gridLayout_5.addWidget(self.label_10, 1, 3, 1, 1)

        self.label_11 = QLabel(self.frame_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(36, 0))
        self.label_11.setMaximumSize(QSize(36, 16777215))
        self.label_11.setFont(font)

        self.gridLayout_5.addWidget(self.label_11, 2, 3, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(36, 0))
        self.label_7.setMaximumSize(QSize(36, 16777215))
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_14 = QLabel(self.frame_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 22))
        self.label_14.setMaximumSize(QSize(16777215, 22))
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_14, 0, 1, 1, 1)

        self.plane_rotation_x_spinbox = QSpinBox(self.frame_5)
        self.plane_rotation_x_spinbox.setObjectName(u"plane_rotation_x_spinbox")
        self.plane_rotation_x_spinbox.setMinimumSize(QSize(60, 0))
        self.plane_rotation_x_spinbox.setMaximumSize(QSize(60, 16777215))
        self.plane_rotation_x_spinbox.setFont(font)
        self.plane_rotation_x_spinbox.setAlignment(Qt.AlignCenter)
        self.plane_rotation_x_spinbox.setMaximum(360)

        self.gridLayout_5.addWidget(self.plane_rotation_x_spinbox, 1, 2, 1, 1)

        self.plane_rotation_y_spinbox = QSpinBox(self.frame_5)
        self.plane_rotation_y_spinbox.setObjectName(u"plane_rotation_y_spinbox")
        self.plane_rotation_y_spinbox.setMinimumSize(QSize(60, 0))
        self.plane_rotation_y_spinbox.setMaximumSize(QSize(60, 16777215))
        self.plane_rotation_y_spinbox.setFont(font)
        self.plane_rotation_y_spinbox.setAlignment(Qt.AlignCenter)
        self.plane_rotation_y_spinbox.setMaximum(360)
        self.plane_rotation_y_spinbox.setValue(90)

        self.gridLayout_5.addWidget(self.plane_rotation_y_spinbox, 2, 2, 1, 1)


        self.gridLayout_6.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_top_buttons = QFrame(self.frame_4)
        self.frame_top_buttons.setObjectName(u"frame_top_buttons")
        self.frame_top_buttons.setMinimumSize(QSize(0, 48))
        self.frame_top_buttons.setMaximumSize(QSize(16777215, 48))
        self.frame_top_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_top_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_top_buttons)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.pushButton_reset = QPushButton(self.frame_top_buttons)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font)

        self.gridLayout_2.addWidget(self.pushButton_reset, 1, 0, 1, 1)

        self.pushButton_invert = QPushButton(self.frame_top_buttons)
        self.pushButton_invert.setObjectName(u"pushButton_invert")
        self.pushButton_invert.setMinimumSize(QSize(100, 28))
        self.pushButton_invert.setMaximumSize(QSize(100, 28))
        self.pushButton_invert.setFont(font)

        self.gridLayout_2.addWidget(self.pushButton_invert, 1, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame_top_buttons, 3, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 48))
        self.frame_2.setMaximumSize(QSize(16777215, 48))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(11)
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_6 = QFrame(Form)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 48))
        self.frame_6.setMaximumSize(QSize(16777215, 48))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_6)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.pushButton_apply = QPushButton(self.frame_6)
        self.pushButton_apply.setObjectName(u"pushButton_apply")
        self.pushButton_apply.setMinimumSize(QSize(100, 28))
        self.pushButton_apply.setMaximumSize(QSize(100, 28))
        self.pushButton_apply.setFont(font)

        self.gridLayout_7.addWidget(self.pushButton_apply, 1, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_6)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)

        self.gridLayout_7.addWidget(self.pushButton_exit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_6, 2, 0, 1, 1)

        QWidget.setTabOrder(self.relative_plane_position_x_slider, self.relative_plane_position_x_spinbox)
        QWidget.setTabOrder(self.relative_plane_position_x_spinbox, self.relative_plane_position_y_slider)
        QWidget.setTabOrder(self.relative_plane_position_y_slider, self.relative_plane_position_y_spinbox)
        QWidget.setTabOrder(self.relative_plane_position_y_spinbox, self.relative_plane_position_z_slider)
        QWidget.setTabOrder(self.relative_plane_position_z_slider, self.relative_plane_position_z_spinbox)
        QWidget.setTabOrder(self.relative_plane_position_z_spinbox, self.plane_rotation_x_slider)
        QWidget.setTabOrder(self.plane_rotation_x_slider, self.plane_rotation_x_spinbox)
        QWidget.setTabOrder(self.plane_rotation_x_spinbox, self.plane_rotation_y_slider)
        QWidget.setTabOrder(self.plane_rotation_y_slider, self.plane_rotation_y_spinbox)
        QWidget.setTabOrder(self.plane_rotation_y_spinbox, self.plane_rotation_z_slider)
        QWidget.setTabOrder(self.plane_rotation_z_slider, self.plane_rotation_z_spinbox)
        QWidget.setTabOrder(self.plane_rotation_z_spinbox, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_invert)
        QWidget.setTabOrder(self.pushButton_invert, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_apply)

        self.retranslateUi(Form)
        self.relative_plane_position_x_slider.sliderMoved.connect(self.relative_plane_position_x_spinbox.setValue)
        self.relative_plane_position_x_spinbox.valueChanged.connect(self.relative_plane_position_x_slider.setValue)
        self.relative_plane_position_y_slider.valueChanged.connect(self.relative_plane_position_y_spinbox.setValue)
        self.relative_plane_position_y_spinbox.valueChanged.connect(self.relative_plane_position_y_slider.setValue)
        self.relative_plane_position_z_slider.valueChanged.connect(self.relative_plane_position_z_spinbox.setValue)
        self.relative_plane_position_z_spinbox.valueChanged.connect(self.relative_plane_position_z_slider.setValue)
        self.plane_rotation_x_slider.valueChanged.connect(self.plane_rotation_x_spinbox.setValue)
        self.plane_rotation_x_spinbox.valueChanged.connect(self.plane_rotation_x_slider.setValue)
        self.plane_rotation_y_slider.valueChanged.connect(self.plane_rotation_y_spinbox.setValue)
        self.plane_rotation_y_spinbox.valueChanged.connect(self.plane_rotation_y_slider.setValue)
        self.plane_rotation_z_slider.valueChanged.connect(self.plane_rotation_z_spinbox.setValue)
        self.plane_rotation_z_spinbox.valueChanged.connect(self.plane_rotation_z_slider.setValue)

        self.pushButton_apply.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Px:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Py:", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Relative plane position", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Pz:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"[%]", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Ry:", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"[deg]", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Rz:", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"[deg]", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"[deg]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Rx:", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Plane rotation", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Form", u"Reset cut", None))
        self.pushButton_invert.setText(QCoreApplication.translate("Form", u"Invert cut", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Section plane controls", None))
        self.pushButton_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Form", u"Exit", None))
    # retranslateUi



class SectionPlaneInputs_UI(QDialog, Ui_Form):
    """
    Component Hierarchy:
    - Form: QDialog
        - (Layout): QGridLayout
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label: QLabel
                                        - relative_plane_position_x_spinbox: QSpinBox
                                        - relative_plane_position_z_spinbox: QSpinBox
                                        - label_4: QLabel
                                        - label_2: QLabel
                                        - relative_plane_position_y_slider: QSlider
                                        - relative_plane_position_x_slider: QSlider
                                        - relative_plane_position_y_spinbox: QSpinBox
                                        - label_13: QLabel
                                        - relative_plane_position_z_slider: QSlider
                                        - label_3: QLabel
                                        - label_5: QLabel
                                        - label_6: QLabel
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - plane_rotation_z_spinbox: QSpinBox
                                        - label_8: QLabel
                                        - plane_rotation_z_slider: QSlider
                                        - plane_rotation_y_slider: QSlider
                                        - label_12: QLabel
                                        - label_9: QLabel
                                        - plane_rotation_x_slider: QSlider
                                        - label_10: QLabel
                                        - label_11: QLabel
                                        - label_7: QLabel
                                        - label_14: QLabel
                                        - plane_rotation_x_spinbox: QSpinBox
                                        - plane_rotation_y_spinbox: QSpinBox
                            - frame_top_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_reset: QPushButton
                                        - pushButton_invert: QPushButton
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - label_15: QLabel
                - frame_6: QFrame
                    - (Layout): QGridLayout
                            - pushButton_apply: QPushButton
                            - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
