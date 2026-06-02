# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_acoustic_pressure_field_for_harmonic_analysis.ui'
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
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(358, 499)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 4, 1, 4)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 344, 500))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, -1, 0, -1)
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, -1, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setSizeIncrement(QSize(400, 0))
        self.frame_2.setBaseSize(QSize(400, 0))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 40))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(176, 0))
        self.frame_7.setMaximumSize(QSize(176, 16777215))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_7)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.comboBox_colormaps = QComboBox(self.frame_7)
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
        self.comboBox_colormaps.setMinimumSize(QSize(120, 26))
        self.comboBox_colormaps.setMaximumSize(QSize(200, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_colormaps.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_colormaps, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame_7, 0, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_12, 0, 3, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(90, 26))
        self.label_6.setMaximumSize(QSize(90, 26))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_6, 0, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 2, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(6)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_color_scalling = QLabel(self.frame_3)
        self.label_color_scalling.setObjectName(u"label_color_scalling")
        self.label_color_scalling.setMinimumSize(QSize(90, 26))
        self.label_color_scalling.setMaximumSize(QSize(90, 26))
        self.label_color_scalling.setFont(font1)
        self.label_color_scalling.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_color_scalling, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

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

        self.gridLayout_9.addWidget(self.comboBox_color_scale, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 4, 0, 1, 1)

        self.frame_button = QFrame(self.frame_2)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 40))
        self.frame_button.setMaximumSize(QSize(16777215, 40))
        self.frame_button.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_button)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot = QPushButton(self.frame_button)
        self.pushButton_plot.setObjectName(u"pushButton_plot")
        self.pushButton_plot.setMinimumSize(QSize(160, 30))
        self.pushButton_plot.setMaximumSize(QSize(160, 30))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.pushButton_plot.setFont(font2)
        self.pushButton_plot.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.pushButton_plot, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_button, 5, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.frame_2)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.treeWidget_frequencies = QTreeWidget(self.frame_treeWidget)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Frequency [Hz]")
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font2)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font3)
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(260, 180))
        self.treeWidget_frequencies.setMaximumSize(QSize(260, 420))
        self.treeWidget_frequencies.setFont(font2)
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_treeWidget, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 40))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_5)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 26))
        self.label_3.setMaximumSize(QSize(90, 26))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_8.addWidget(self.label_3, 0, 1, 1, 1)

        self.slider_transparency = QSlider(self.frame_5)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(200, 16777215))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_8.addWidget(self.slider_transparency, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 3, 0, 1, 1)

        self.frame_selector = QFrame(self.frame_2)
        self.frame_selector.setObjectName(u"frame_selector")
        self.frame_selector.setMinimumSize(QSize(0, 40))
        self.frame_selector.setMaximumSize(QSize(16777215, 40))
        self.frame_selector.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selector.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_selector)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.lineEdit_selected_frequency = QLineEdit(self.frame_selector)
        self.lineEdit_selected_frequency.setObjectName(u"lineEdit_selected_frequency")
        self.lineEdit_selected_frequency.setEnabled(False)
        self.lineEdit_selected_frequency.setMinimumSize(QSize(80, 28))
        self.lineEdit_selected_frequency.setMaximumSize(QSize(80, 28))
        self.lineEdit_selected_frequency.setFont(font2)
        self.lineEdit_selected_frequency.setStyleSheet(u"")
        self.lineEdit_selected_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_frequency, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frame_selector)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frame_selector)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 28))
        self.label_5.setMaximumSize(QSize(16777215, 28))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_5, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_selector, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_frequency, self.treeWidget_frequencies)
        QWidget.setTabOrder(self.treeWidget_frequencies, self.comboBox_colormaps)
        QWidget.setTabOrder(self.comboBox_colormaps, self.slider_transparency)
        QWidget.setTabOrder(self.slider_transparency, self.comboBox_color_scale)
        QWidget.setTabOrder(self.comboBox_color_scale, self.pushButton_plot)

        self.retranslateUi(Form)

        self.pushButton_plot.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot pressure field", None))
        self.label.setText(QCoreApplication.translate("Form", u"Select the frequency to be plotted", None))
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

        self.label_6.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
        self.label_color_scalling.setText(QCoreApplication.translate("Form", u"Color scaling:", None))
        self.comboBox_color_scale.setItemText(0, QCoreApplication.translate("Form", u"Animation (absolute)", None))
        self.comboBox_color_scale.setItemText(1, QCoreApplication.translate("Form", u"Animation (non absolute)", None))
        self.comboBox_color_scale.setItemText(2, QCoreApplication.translate("Form", u"Absolute values", None))
        self.comboBox_color_scale.setItemText(3, QCoreApplication.translate("Form", u"Real values", None))
        self.comboBox_color_scale.setItemText(4, QCoreApplication.translate("Form", u"Imaginary values", None))

        self.pushButton_plot.setText(QCoreApplication.translate("Form", u"Plot pressure field", None))
        ___qtreewidgetitem = self.treeWidget_frequencies.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Index", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Transparency:", None))
        self.lineEdit_selected_frequency.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Frequency:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"[Hz]", None))
    # retranslateUi



class PlotAcousticPressureFieldForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame: QFrame
                                    - (Layout): QGridLayout
                                            - label: QLabel
                                - frame_2: QFrame
                                    - (Layout): QGridLayout
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - frame_7: QFrame
                                                            - (Layout): QGridLayout
                                                                    - comboBox_colormaps: QComboBox
                                                        - label_6: QLabel
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_color_scalling: QLabel
                                                        - comboBox_color_scale: QComboBox
                                            - frame_button: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_plot: QPushButton
                                            - frame_treeWidget: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_frequencies: QTreeWidget
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - label_3: QLabel
                                                        - slider_transparency: QSlider
                                            - frame_selector: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_frequency: QLineEdit
                                                        - label_4: QLabel
                                                        - label_5: QLabel
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
