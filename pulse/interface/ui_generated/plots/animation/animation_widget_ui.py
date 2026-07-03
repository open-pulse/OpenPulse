# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(333, 211)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 6, 4, 4)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 80))
        self.frame_2.setMaximumSize(QSize(16777215, 80))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_frames = QLabel(self.frame_2)
        self.label_frames.setObjectName(u"label_frames")
        self.label_frames.setMinimumSize(QSize(92, 28))
        self.label_frames.setMaximumSize(QSize(92, 28))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_frames.setFont(font)
        self.label_frames.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_frames, 0, 1, 1, 1)

        self.spinBox_frames = QSpinBox(self.frame_2)
        self.spinBox_frames.setObjectName(u"spinBox_frames")
        self.spinBox_frames.setMinimumSize(QSize(70, 28))
        self.spinBox_frames.setMaximumSize(QSize(70, 28))
        font1 = QFont()
        font1.setPointSize(10)
        self.spinBox_frames.setFont(font1)
        self.spinBox_frames.setStyleSheet(u"")
        self.spinBox_frames.setWrapping(False)
        self.spinBox_frames.setFrame(True)
        self.spinBox_frames.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(120)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)

        self.gridLayout_3.addWidget(self.spinBox_frames, 0, 2, 1, 1)

        self.label_cycles = QLabel(self.frame_2)
        self.label_cycles.setObjectName(u"label_cycles")
        self.label_cycles.setMinimumSize(QSize(92, 28))
        self.label_cycles.setMaximumSize(QSize(92, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_cycles.setFont(font2)
        self.label_cycles.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_cycles, 1, 1, 1, 1)

        self.spinBox_cycles = QSpinBox(self.frame_2)
        self.spinBox_cycles.setObjectName(u"spinBox_cycles")
        self.spinBox_cycles.setMinimumSize(QSize(70, 28))
        self.spinBox_cycles.setMaximumSize(QSize(70, 28))
        self.spinBox_cycles.setFont(font1)
        self.spinBox_cycles.setStyleSheet(u"")
        self.spinBox_cycles.setWrapping(False)
        self.spinBox_cycles.setFrame(True)
        self.spinBox_cycles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_cycles.setMinimum(0)
        self.spinBox_cycles.setMaximum(20)
        self.spinBox_cycles.setSingleStep(1)
        self.spinBox_cycles.setValue(0)

        self.gridLayout_3.addWidget(self.spinBox_cycles, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 40))
        self.frame_8.setMaximumSize(QSize(16777215, 40))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_8)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_animate = QPushButton(self.frame_8)
        self.pushButton_animate.setObjectName(u"pushButton_animate")
        self.pushButton_animate.setMinimumSize(QSize(100, 28))
        self.pushButton_animate.setMaximumSize(QSize(120, 28))
        self.pushButton_animate.setFont(font)
        self.pushButton_animate.setStyleSheet(u"")
        self.pushButton_animate.setIconSize(QSize(16, 16))
        self.pushButton_animate.setCheckable(True)

        self.gridLayout_9.addWidget(self.pushButton_animate, 0, 1, 1, 1)

        self.pushButton_export = QPushButton(self.frame_8)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setMinimumSize(QSize(100, 28))
        self.pushButton_export.setMaximumSize(QSize(120, 28))
        self.pushButton_export.setFont(font)
        self.pushButton_export.setStyleSheet(u"")
        self.pushButton_export.setIconSize(QSize(16, 16))

        self.gridLayout_9.addWidget(self.pushButton_export, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_8, 2, 0, 1, 1)

        self.frame_middle = QFrame(self.frame)
        self.frame_middle.setObjectName(u"frame_middle")
        self.frame_middle.setMaximumSize(QSize(16777215, 16777215))
        self.frame_middle.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_middle.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_middle)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 2, 6, 2)
        self.label_phase_angle = QLabel(self.frame_middle)
        self.label_phase_angle.setObjectName(u"label_phase_angle")
        self.label_phase_angle.setMinimumSize(QSize(60, 26))
        self.label_phase_angle.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_5.addWidget(self.label_phase_angle, 1, 2, 1, 1)

        self.magnification_factor_slider = QSlider(self.frame_middle)
        self.magnification_factor_slider.setObjectName(u"magnification_factor_slider")
        self.magnification_factor_slider.setMinimumSize(QSize(0, 0))
        self.magnification_factor_slider.setMaximum(2)
        self.magnification_factor_slider.setValue(1)
        self.magnification_factor_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_5.addWidget(self.magnification_factor_slider, 2, 1, 1, 1)

        self.label_factor = QLabel(self.frame_middle)
        self.label_factor.setObjectName(u"label_factor")
        self.label_factor.setMinimumSize(QSize(60, 26))
        self.label_factor.setMaximumSize(QSize(16777215, 26))

        self.gridLayout_5.addWidget(self.label_factor, 2, 2, 1, 1)

        self.label_animation_phase = QLabel(self.frame_middle)
        self.label_animation_phase.setObjectName(u"label_animation_phase")
        self.label_animation_phase.setMinimumSize(QSize(0, 26))
        self.label_animation_phase.setMaximumSize(QSize(16777215, 26))
        self.label_animation_phase.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_animation_phase, 1, 0, 1, 1)

        self.phase_slider = QSlider(self.frame_middle)
        self.phase_slider.setObjectName(u"phase_slider")
        self.phase_slider.setMinimumSize(QSize(0, 0))
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_5.addWidget(self.phase_slider, 1, 1, 1, 1)

        self.label_magnification_factor = QLabel(self.frame_middle)
        self.label_magnification_factor.setObjectName(u"label_magnification_factor")
        self.label_magnification_factor.setMinimumSize(QSize(0, 26))
        self.label_magnification_factor.setMaximumSize(QSize(16777215, 26))
        self.label_magnification_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_magnification_factor, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_middle, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_export, self.pushButton_animate)

        self.retranslateUi(Form)

        self.pushButton_animate.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_frames.setText(QCoreApplication.translate("Form", u"Frames/cycle:", None))
        self.spinBox_frames.setPrefix("")
        self.label_cycles.setText(QCoreApplication.translate("Form", u"Cycles:", None))
        self.spinBox_cycles.setPrefix("")
        self.pushButton_animate.setText(QCoreApplication.translate("Form", u"Animate", None))
        self.pushButton_export.setText(QCoreApplication.translate("Form", u" Export video", None))
        self.label_phase_angle.setText(QCoreApplication.translate("Form", u"0\u00ba", None))
        self.label_factor.setText(QCoreApplication.translate("Form", u"1.0x", None))
        self.label_animation_phase.setText(QCoreApplication.translate("Form", u"Phase:", None))
        self.label_magnification_factor.setText(QCoreApplication.translate("Form", u"Magnification:", None))
    # retranslateUi



class AnimationWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_frames: QLabel
                                        - spinBox_frames: QSpinBox
                                        - label_cycles: QLabel
                                        - spinBox_cycles: QSpinBox
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_animate: QPushButton
                                        - pushButton_export: QPushButton
                            - frame_middle: QFrame
                                - (Layout): QGridLayout
                                        - label_phase_angle: QLabel
                                        - magnification_factor_slider: QSlider
                                        - label_factor: QLabel
                                        - label_animation_phase: QLabel
                                        - phase_slider: QSlider
                                        - label_magnification_factor: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
