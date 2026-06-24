# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_stresses_field_for_static_analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(356, 333)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 4, 0, 4)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 356, 325))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(0, 6, 0, -1)
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 160))
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(4)
        self.gridLayout_10.setVerticalSpacing(6)
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 160))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(0, 6, 0, 6)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)

        self.comboBox_stress_type = QComboBox(self.frame_3)
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.setObjectName(u"comboBox_stress_type")
        self.comboBox_stress_type.setMinimumSize(QSize(176, 26))
        self.comboBox_stress_type.setMaximumSize(QSize(200, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_stress_type.setFont(font1)

        self.gridLayout_9.addWidget(self.comboBox_stress_type, 0, 2, 1, 1)

        self.comboBox_colormaps = QComboBox(self.frame_3)
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.addItem("")
        self.comboBox_colormaps.setObjectName(u"comboBox_colormaps")
        self.comboBox_colormaps.setMinimumSize(QSize(176, 26))
        self.comboBox_colormaps.setMaximumSize(QSize(200, 26))
        self.comboBox_colormaps.setFont(font1)

        self.gridLayout_9.addWidget(self.comboBox_colormaps, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 26))
        self.label_3.setMaximumSize(QSize(90, 26))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_3, 1, 1, 1, 1)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(86, 26))
        self.label_2.setMaximumSize(QSize(86, 26))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(86, 26))
        self.label_5.setMaximumSize(QSize(86, 26))
        self.label_5.setFont(font1)

        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)

        self.comboBox_color_scale = QComboBox(self.frame_3)
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.setObjectName(u"comboBox_color_scale")
        self.comboBox_color_scale.setMinimumSize(QSize(176, 26))
        self.comboBox_color_scale.setMaximumSize(QSize(200, 26))
        self.comboBox_color_scale.setFont(font1)

        self.gridLayout_9.addWidget(self.comboBox_color_scale, 2, 2, 1, 1)

        self.slider_transparency = QSlider(self.frame_3)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(200, 16777215))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_9.addWidget(self.slider_transparency, 3, 2, 1, 1)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(90, 26))
        self.label_4.setMaximumSize(QSize(90, 26))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_4, 3, 1, 1, 1)


        self.gridLayout_10.addWidget(self.frame_3, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setMinimumSize(QSize(0, 60))
        self.frame_animation.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Stress field plot setup", None))
        self.comboBox_stress_type.setItemText(0, QCoreApplication.translate("Form", u" Normal axial", None))
        self.comboBox_stress_type.setItemText(1, QCoreApplication.translate("Form", u" Normal bending y", None))
        self.comboBox_stress_type.setItemText(2, QCoreApplication.translate("Form", u" Normal bending z", None))
        self.comboBox_stress_type.setItemText(3, QCoreApplication.translate("Form", u" Hoop", None))
        self.comboBox_stress_type.setItemText(4, QCoreApplication.translate("Form", u" Torsional shear", None))
        self.comboBox_stress_type.setItemText(5, QCoreApplication.translate("Form", u" Transversal shear xy", None))
        self.comboBox_stress_type.setItemText(6, QCoreApplication.translate("Form", u" Transversal shear xz", None))

#if QT_CONFIG(tooltip)
        self.comboBox_stress_type.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the stress type to get the frequency response</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_colormaps.setItemText(0, QCoreApplication.translate("Form", u" Jet scale", None))
        self.comboBox_colormaps.setItemText(1, QCoreApplication.translate("Form", u" Viridis scale", None))
        self.comboBox_colormaps.setItemText(2, QCoreApplication.translate("Form", u" Inferno scale", None))
        self.comboBox_colormaps.setItemText(3, QCoreApplication.translate("Form", u" Magma scale", None))
        self.comboBox_colormaps.setItemText(4, QCoreApplication.translate("Form", u" Plasma scale", None))
        self.comboBox_colormaps.setItemText(5, QCoreApplication.translate("Form", u"BWR diverging scale", None))
        self.comboBox_colormaps.setItemText(6, QCoreApplication.translate("Form", u"PiYG diverging scale", None))
        self.comboBox_colormaps.setItemText(7, QCoreApplication.translate("Form", u"PRGn diverging scale", None))
        self.comboBox_colormaps.setItemText(8, QCoreApplication.translate("Form", u"BrBG diverging scale", None))
        self.comboBox_colormaps.setItemText(9, QCoreApplication.translate("Form", u"PuOr diverging scale", None))
        self.comboBox_colormaps.setItemText(10, QCoreApplication.translate("Form", u" Grayscale", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Color scaling:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Stress type:", None))
        self.comboBox_color_scale.setItemText(0, QCoreApplication.translate("Form", u"Animation (absolute)", None))
        self.comboBox_color_scale.setItemText(1, QCoreApplication.translate("Form", u"Animation (non absolute)", None))
        self.comboBox_color_scale.setItemText(2, QCoreApplication.translate("Form", u"Absolute values", None))
        self.comboBox_color_scale.setItemText(3, QCoreApplication.translate("Form", u"Real values", None))
        self.comboBox_color_scale.setItemText(4, QCoreApplication.translate("Form", u"Imaginary values", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Transparency:", None))
    # retranslateUi



class PlotStressesFieldForStaticAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame: QFrame
                                    - (Layout): QGridLayout
                                            - label_title: QLabel
                                - frame_2: QFrame
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_stress_type: QComboBox
                                                        - comboBox_colormaps: QComboBox
                                                        - label_3: QLabel
                                                        - label_2: QLabel
                                                        - label_5: QLabel
                                                        - comboBox_color_scale: QComboBox
                                                        - slider_transparency: QSlider
                                                        - label_4: QLabel
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
