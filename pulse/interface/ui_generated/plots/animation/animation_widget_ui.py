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
        Form.resize(333, 177)
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
        self.frame_slider = QFrame(self.frame)
        self.frame_slider.setObjectName(u"frame_slider")
        self.frame_slider.setMinimumSize(QSize(0, 30))
        self.frame_slider.setMaximumSize(QSize(16777215, 30))
        self.frame_slider.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_slider.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_slider)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 0, 4, 0)
        self.frame_phase_label = QFrame(self.frame_slider)
        self.frame_phase_label.setObjectName(u"frame_phase_label")
        self.frame_phase_label.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_phase_label.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_phase_label)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.label_2 = QLabel(self.frame_phase_label)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_phase_label, 0, 0, 1, 1)

        self.phase_slider = QSlider(self.frame_slider)
        self.phase_slider.setObjectName(u"phase_slider")
        self.phase_slider.setMaximum(360)
        self.phase_slider.setOrientation(Qt.Orientation.Horizontal)
        self.phase_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.gridLayout_4.addWidget(self.phase_slider, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame_slider, 1, 0, 1, 1)

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
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_animate.setFont(font1)
        self.pushButton_animate.setStyleSheet(u"")
        self.pushButton_animate.setIconSize(QSize(16, 16))
        self.pushButton_animate.setCheckable(True)

        self.gridLayout_9.addWidget(self.pushButton_animate, 0, 1, 1, 1)

        self.pushButton_export = QPushButton(self.frame_8)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setMinimumSize(QSize(100, 28))
        self.pushButton_export.setMaximumSize(QSize(120, 28))
        self.pushButton_export.setFont(font1)
        self.pushButton_export.setStyleSheet(u"")
        self.pushButton_export.setIconSize(QSize(16, 16))

        self.gridLayout_9.addWidget(self.pushButton_export, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_8, 2, 0, 1, 1)

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
        self.label_frames.setFont(font1)
        self.label_frames.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_frames, 0, 1, 1, 1)

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
        self.spinBox_cycles.setFont(font)
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


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.phase_slider, self.pushButton_export)
        QWidget.setTabOrder(self.pushButton_export, self.pushButton_animate)

        self.retranslateUi(Form)

        self.pushButton_animate.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Phase:", None))
        self.pushButton_animate.setText(QCoreApplication.translate("Form", u"Animate", None))
        self.pushButton_export.setText(QCoreApplication.translate("Form", u" Export video", None))
        self.label_frames.setText(QCoreApplication.translate("Form", u"Frames/cycle:", None))
        self.spinBox_frames.setPrefix("")
        self.label_cycles.setText(QCoreApplication.translate("Form", u"Cycles:", None))
        self.spinBox_cycles.setPrefix("")
    # retranslateUi



class AnimationWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_slider: QFrame
                                - (Layout): QGridLayout
                                        - frame_phase_label: QFrame
                                            - (Layout): QGridLayout
                                                    - label_2: QLabel
                                        - phase_slider: QSlider
                            - frame_8: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_animate: QPushButton
                                        - pushButton_export: QPushButton
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_frames: QLabel
                                        - spinBox_frames: QSpinBox
                                        - label_cycles: QLabel
                                        - spinBox_cycles: QSpinBox
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
