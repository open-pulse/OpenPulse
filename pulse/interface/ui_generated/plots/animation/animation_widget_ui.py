# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animation_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(366, 222)
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
        self.gridLayout.setContentsMargins(4, 6, 4, 6)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 80))
        self.frame_2.setMaximumSize(QSize(16777215, 80))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.spinBox_cycles = QSpinBox(self.frame_2)
        self.spinBox_cycles.setObjectName(u"spinBox_cycles")
        self.spinBox_cycles.setMinimumSize(QSize(70, 28))
        self.spinBox_cycles.setMaximumSize(QSize(70, 28))
        font = QFont()
        font.setPointSize(10)
        self.spinBox_cycles.setFont(font)
        self.spinBox_cycles.setStyleSheet(u"")
        self.spinBox_cycles.setWrapping(False)
        self.spinBox_cycles.setFrame(True)
        self.spinBox_cycles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_cycles.setMinimum(0)
        self.spinBox_cycles.setMaximum(20)
        self.spinBox_cycles.setSingleStep(1)
        self.spinBox_cycles.setValue(5)

        self.gridLayout_3.addWidget(self.spinBox_cycles, 1, 2, 1, 1)

        self.pushButton_animation_loop = QPushButton(self.frame_2)
        self.pushButton_animation_loop.setObjectName(u"pushButton_animation_loop")
        self.pushButton_animation_loop.setMinimumSize(QSize(40, 28))
        self.pushButton_animation_loop.setMaximumSize(QSize(16777215, 28))
        icon = QIcon()
        icon.addFile(u":/icons/common/infinite_symbol.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_animation_loop.setIcon(icon)
        self.pushButton_animation_loop.setIconSize(QSize(22, 22))
        self.pushButton_animation_loop.setCheckable(False)

        self.gridLayout_3.addWidget(self.pushButton_animation_loop, 1, 3, 1, 1)

        self.spinBox_frames = QSpinBox(self.frame_2)
        self.spinBox_frames.setObjectName(u"spinBox_frames")
        self.spinBox_frames.setMinimumSize(QSize(70, 28))
        self.spinBox_frames.setMaximumSize(QSize(70, 28))
        self.spinBox_frames.setFont(font)
        self.spinBox_frames.setStyleSheet(u"")
        self.spinBox_frames.setWrapping(False)
        self.spinBox_frames.setFrame(True)
        self.spinBox_frames.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_frames.setMinimum(20)
        self.spinBox_frames.setMaximum(120)
        self.spinBox_frames.setSingleStep(10)
        self.spinBox_frames.setValue(40)

        self.gridLayout_3.addWidget(self.spinBox_frames, 0, 2, 1, 1)

        self.label_frames = QLabel(self.frame_2)
        self.label_frames.setObjectName(u"label_frames")
        self.label_frames.setMinimumSize(QSize(0, 28))
        self.label_frames.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_frames.setFont(font1)
        self.label_frames.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_frames, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.label_animation_cycles = QLabel(self.frame_2)
        self.label_animation_cycles.setObjectName(u"label_animation_cycles")
        self.label_animation_cycles.setMinimumSize(QSize(0, 28))
        self.label_animation_cycles.setMaximumSize(QSize(16777215, 28))
        self.label_animation_cycles.setFont(font)
        self.label_animation_cycles.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_animation_cycles, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 40))
        self.frame_8.setMaximumSize(QSize(16777215, 48))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_8)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_animate = QPushButton(self.frame_8)
        self.pushButton_animate.setObjectName(u"pushButton_animate")
        self.pushButton_animate.setMinimumSize(QSize(100, 28))
        self.pushButton_animate.setMaximumSize(QSize(130, 30))
        self.pushButton_animate.setFont(font1)
        self.pushButton_animate.setStyleSheet(u"")
        self.pushButton_animate.setIconSize(QSize(16, 16))
        self.pushButton_animate.setCheckable(True)

        self.gridLayout_9.addWidget(self.pushButton_animate, 0, 1, 1, 1)

        self.pushButton_export_video = QPushButton(self.frame_8)
        self.pushButton_export_video.setObjectName(u"pushButton_export_video")
        self.pushButton_export_video.setMinimumSize(QSize(100, 28))
        self.pushButton_export_video.setMaximumSize(QSize(130, 30))
        self.pushButton_export_video.setFont(font1)
        self.pushButton_export_video.setStyleSheet(u"")
        self.pushButton_export_video.setIconSize(QSize(16, 16))

        self.gridLayout_9.addWidget(self.pushButton_export_video, 0, 0, 1, 1)


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

        QWidget.setTabOrder(self.pushButton_export_video, self.pushButton_animate)

        self.retranslateUi(Form)

        self.pushButton_animate.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.spinBox_cycles.setPrefix("")
#if QT_CONFIG(tooltip)
        self.pushButton_animation_loop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Loop the animation</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_animation_loop.setText("")
        self.spinBox_frames.setPrefix("")
        self.label_frames.setText(QCoreApplication.translate("Form", u"Frames / cycle:", None))
        self.label_animation_cycles.setText(QCoreApplication.translate("Form", u"Animation cycles:", None))
        self.pushButton_animate.setText(QCoreApplication.translate("Form", u"Animate", None))
        self.pushButton_export_video.setText(QCoreApplication.translate("Form", u" Export video", None))
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
                                        - spinBox_cycles: QSpinBox
                                        - pushButton_animation_loop: QPushButton
                                        - spinBox_frames: QSpinBox
                                        - label_frames: QLabel
                                        - label_animation_cycles: QLabel
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_animate: QPushButton
                                        - pushButton_export_video: QPushButton
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
