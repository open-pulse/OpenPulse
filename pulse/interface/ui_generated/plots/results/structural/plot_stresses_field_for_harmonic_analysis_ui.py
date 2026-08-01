# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_stresses_field_for_harmonic_analysis.ui'
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
        Form.resize(339, 586)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 327, 678))
        self.gridLayout_11 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(6)
        self.gridLayout_11.setVerticalSpacing(4)
        self.gridLayout_11.setContentsMargins(0, 4, 0, -1)
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
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 200))
        self.frame_3.setMaximumSize(QSize(16777215, 220))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setVerticalSpacing(6)
        self.gridLayout_9.setContentsMargins(0, 10, 0, 10)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 1, 3, 1, 1)

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
        self.comboBox_colormaps.setMaximumSize(QSize(240, 26))
        font = QFont()
        font.setPointSize(10)
        self.comboBox_colormaps.setFont(font)

        self.gridLayout_9.addWidget(self.comboBox_colormaps, 3, 2, 1, 1)

        self.label_8 = QLabel(self.frame_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(92, 26))
        self.label_8.setMaximumSize(QSize(92, 26))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_8, 2, 1, 1, 1)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(92, 26))
        self.label_3.setMaximumSize(QSize(92, 26))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_3, 5, 1, 1, 1)

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
        self.comboBox_stress_type.setMaximumSize(QSize(240, 26))
        self.comboBox_stress_type.setFont(font)

        self.gridLayout_9.addWidget(self.comboBox_stress_type, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.comboBox_color_scale = QComboBox(self.frame_3)
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.addItem("")
        self.comboBox_color_scale.setObjectName(u"comboBox_color_scale")
        self.comboBox_color_scale.setMinimumSize(QSize(176, 26))
        self.comboBox_color_scale.setMaximumSize(QSize(240, 26))
        self.comboBox_color_scale.setFont(font)

        self.gridLayout_9.addWidget(self.comboBox_color_scale, 4, 2, 1, 1)

        self.comboBox_damping_effect = QComboBox(self.frame_3)
        self.comboBox_damping_effect.addItem("")
        self.comboBox_damping_effect.addItem("")
        self.comboBox_damping_effect.setObjectName(u"comboBox_damping_effect")
        self.comboBox_damping_effect.setMinimumSize(QSize(176, 26))
        self.comboBox_damping_effect.setMaximumSize(QSize(240, 26))
        self.comboBox_damping_effect.setFont(font)

        self.gridLayout_9.addWidget(self.comboBox_damping_effect, 2, 2, 1, 1)

        self.slider_transparency = QSlider(self.frame_3)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(240, 16777215))
        self.slider_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_9.addWidget(self.slider_transparency, 5, 2, 1, 1)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(92, 26))
        self.label_2.setMaximumSize(QSize(92, 26))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_2, 4, 1, 1, 1)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(92, 26))
        self.label_5.setMaximumSize(QSize(92, 26))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(92, 26))
        self.label_6.setMaximumSize(QSize(92, 26))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_6, 3, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_3, 3, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 220))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.treeWidget_frequencies = QTreeWidget(self.frame_4)
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(9)
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Frequency [Hz]")
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font2)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font1)
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(259, 180))
        self.treeWidget_frequencies.setMaximumSize(QSize(260, 415))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.treeWidget_frequencies.setFont(font3)
        self.treeWidget_frequencies.setStyleSheet(u"")
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 2, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 40))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_selected_frequency = QLineEdit(self.frame_5)
        self.lineEdit_selected_frequency.setObjectName(u"lineEdit_selected_frequency")
        self.lineEdit_selected_frequency.setEnabled(False)
        self.lineEdit_selected_frequency.setMinimumSize(QSize(120, 28))
        self.lineEdit_selected_frequency.setMaximumSize(QSize(120, 28))
        self.lineEdit_selected_frequency.setFont(font3)
        self.lineEdit_selected_frequency.setStyleSheet(u"")
        self.lineEdit_selected_frequency.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_selected_frequency, 0, 2, 1, 1)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_4.setFont(font4)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 0, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 28))
        self.label_7.setMaximumSize(QSize(16777215, 28))
        self.label_7.setFont(font4)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 1, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 42))
        self.frame.setMaximumSize(QSize(16777215, 42))
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
        self.label.setMaximumSize(QSize(16777215, 32))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label.setFont(font5)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_animation = QFrame(self.scrollAreaWidgetContents)
        self.frame_animation.setObjectName(u"frame_animation")
        self.frame_animation.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_animation.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_11.addWidget(self.frame_animation, 3, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 1, 1, 1)

        QWidget.setTabOrder(self.lineEdit_selected_frequency, self.treeWidget_frequencies)
        QWidget.setTabOrder(self.treeWidget_frequencies, self.comboBox_stress_type)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
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

        self.label_8.setText(QCoreApplication.translate("Form", u"Damping effect:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Transparency:", None))
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
        self.comboBox_color_scale.setItemText(0, QCoreApplication.translate("Form", u"Animation (absolute)", None))
        self.comboBox_color_scale.setItemText(1, QCoreApplication.translate("Form", u"Animation (non absolute)", None))
        self.comboBox_color_scale.setItemText(2, QCoreApplication.translate("Form", u"Absolute values", None))
        self.comboBox_color_scale.setItemText(3, QCoreApplication.translate("Form", u"Real values", None))
        self.comboBox_color_scale.setItemText(4, QCoreApplication.translate("Form", u"Imaginary values", None))

        self.comboBox_damping_effect.setItemText(0, QCoreApplication.translate("Form", u"Excluded", None))
        self.comboBox_damping_effect.setItemText(1, QCoreApplication.translate("Form", u"Included", None))

#if QT_CONFIG(tooltip)
        self.comboBox_damping_effect.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the stress type to get the frequency response</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Form", u"Color scaling:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Stress type:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
        ___qtreewidgetitem = self.treeWidget_frequencies.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Index", None))
        self.lineEdit_selected_frequency.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Frequency:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"[Hz]", None))
        self.label.setText(QCoreApplication.translate("Form", u"Stress field plot setup", None))
    # retranslateUi



class PlotStressesFieldForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame_2: QFrame
                                    - (Layout): QGridLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - comboBox_colormaps: QComboBox
                                                        - label_8: QLabel
                                                        - label_3: QLabel
                                                        - comboBox_stress_type: QComboBox
                                                        - comboBox_color_scale: QComboBox
                                                        - comboBox_damping_effect: QComboBox
                                                        - slider_transparency: QSlider
                                                        - label_2: QLabel
                                                        - label_5: QLabel
                                                        - label_6: QLabel
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_frequencies: QTreeWidget
                                            - frame_5: QFrame
                                                - (Layout): QGridLayout
                                                        - lineEdit_selected_frequency: QLineEdit
                                                        - label_4: QLabel
                                                        - label_7: QLabel
                                - frame: QFrame
                                    - (Layout): QGridLayout
                                            - label: QLabel
                                - frame_animation: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
