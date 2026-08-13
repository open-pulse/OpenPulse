# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_nodal_results_field_for_harmonic_analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(355, 554)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 343, 597))
        self.gridLayout_6 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(0, 6, 0, 0)
        self.frame_title = QFrame(self.scrollAreaWidgetContents)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, -1, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 0))
        self.label_title.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.Shape.NoFrame)
        self.label_title.setFrameShadow(QFrame.Shadow.Raised)
        self.label_title.setTextFormat(Qt.TextFormat.AutoText)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(self.scrollAreaWidgetContents)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setSizeIncrement(QSize(400, 0))
        self.frame_main.setBaseSize(QSize(400, 0))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_main)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(4)
        self.gridLayout_5.setVerticalSpacing(6)
        self.gridLayout_5.setContentsMargins(4, 6, 4, 6)
        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 120))
        self.frame.setMaximumSize(QSize(16777215, 180))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 6, 0, 4)
        self.comboBox_color_scale = QComboBox(self.frame)
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.setObjectName(u"comboBox_color_scale")
        self.comboBox_color_scale.setMinimumSize(QSize(176, 26))
        self.comboBox_color_scale.setMaximumSize(QSize(200, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox_color_scale.setFont(font1)

        self.gridLayout_13.addWidget(self.comboBox_color_scale, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 26))
        self.label_2.setMaximumSize(QSize(90, 26))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_2, 1, 1, 1, 1)

        self.frame_7 = QFrame(self.frame)
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
        self.comboBox_colormaps.setFont(font1)

        self.gridLayout_14.addWidget(self.comboBox_colormaps, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.frame_7, 0, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_12, 0, 3, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(90, 26))
        self.label_6.setMaximumSize(QSize(90, 26))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_6, 0, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.slider_transparency = QSlider(self.frame)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(200, 16777215))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_13.addWidget(self.slider_transparency, 2, 2, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 26))
        self.label_3.setMaximumSize(QSize(90, 26))
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_3, 2, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame, 4, 0, 1, 1)

        self.frame_treeWidget = QFrame(self.frame_main)
        self.frame_treeWidget.setObjectName(u"frame_treeWidget")
        self.frame_treeWidget.setMaximumSize(QSize(16777215, 240))
        self.frame_treeWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_treeWidget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.treeWidget_frequencies = QTreeWidget(self.frame_treeWidget)
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Frequency [Hz]")
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font3)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font2)
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(260, 180))
        self.treeWidget_frequencies.setMaximumSize(QSize(260, 415))
        self.treeWidget_frequencies.setFont(font3)
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_treeWidget, 3, 0, 1, 1)

        self.frame_frequency = QFrame(self.frame_main)
        self.frame_frequency.setObjectName(u"frame_frequency")
        self.frame_frequency.setMinimumSize(QSize(0, 40))
        self.frame_frequency.setMaximumSize(QSize(16777215, 40))
        self.frame_frequency.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_frequency.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_frequency)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.lineEdit_selected_frequency = QLineEdit(self.frame_frequency)
        self.lineEdit_selected_frequency.setObjectName(u"lineEdit_selected_frequency")
        self.lineEdit_selected_frequency.setEnabled(False)
        self.lineEdit_selected_frequency.setMinimumSize(QSize(120, 28))
        self.lineEdit_selected_frequency.setMaximumSize(QSize(120, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        font4.setItalic(False)
        self.lineEdit_selected_frequency.setFont(font4)
        self.lineEdit_selected_frequency.setStyleSheet(u"")
        self.lineEdit_selected_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_frequency, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_4 = QLabel(self.frame_frequency)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(10)
        font5.setBold(False)
        self.label_4.setFont(font5)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_frequency, 2, 0, 1, 1)


        self.gridLayout_6.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_6.addWidget(self.frame_animation, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_frequency, self.treeWidget_frequencies)
        QWidget.setTabOrder(self.treeWidget_frequencies, self.comboBox_colormaps)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot displacement field", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Select the frequency to be plotted", None))
        self.comboBox_color_scale.setItemText(0, QCoreApplication.translate("Form", u"Animation (absolute)", None))
        self.comboBox_color_scale.setItemText(1, QCoreApplication.translate("Form", u"Animation (Ux)", None))
        self.comboBox_color_scale.setItemText(2, QCoreApplication.translate("Form", u"Animation (Uy)", None))
        self.comboBox_color_scale.setItemText(3, QCoreApplication.translate("Form", u"Animation (Uz)", None))
        self.comboBox_color_scale.setItemText(4, QCoreApplication.translate("Form", u"Absolute (resultant)", None))
        self.comboBox_color_scale.setItemText(5, QCoreApplication.translate("Form", u"Absolute (Ux)", None))
        self.comboBox_color_scale.setItemText(6, QCoreApplication.translate("Form", u"Absolute (Uy)", None))
        self.comboBox_color_scale.setItemText(7, QCoreApplication.translate("Form", u"Absolute (Uz)", None))
        self.comboBox_color_scale.setItemText(8, QCoreApplication.translate("Form", u"Real - Ux", None))
        self.comboBox_color_scale.setItemText(9, QCoreApplication.translate("Form", u"Real - Uy", None))
        self.comboBox_color_scale.setItemText(10, QCoreApplication.translate("Form", u"Real - Uz", None))
        self.comboBox_color_scale.setItemText(11, QCoreApplication.translate("Form", u"Imaginary - Ux", None))
        self.comboBox_color_scale.setItemText(12, QCoreApplication.translate("Form", u"Imaginary - Uy", None))
        self.comboBox_color_scale.setItemText(13, QCoreApplication.translate("Form", u"Imaginary - Uz", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"Color scaling:", None))
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
        self.label_3.setText(QCoreApplication.translate("Form", u"Transparency:", None))
        ___qtreewidgetitem = self.treeWidget_frequencies.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Index", None))
        self.lineEdit_selected_frequency.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Frequency:", None))
    # retranslateUi



class PlotNodalResultsFieldForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame_title: QFrame
                                    - (Layout): QGridLayout
                                            - label_title: QLabel
                                - frame_main: QFrame
                                    - (Layout): QGridLayout
                                            - frame: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_color_scale: QComboBox
                                                        - label_2: QLabel
                                                        - frame_7: QFrame
                                                            - (Layout): QGridLayout
                                                                    - comboBox_colormaps: QComboBox
                                                        - label_6: QLabel
                                                        - slider_transparency: QSlider
                                                        - label_3: QLabel
                                            - frame_treeWidget: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_frequencies: QTreeWidget
                                            - frame_frequency: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_frequency: QLineEdit
                                                        - label_4: QLabel
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
