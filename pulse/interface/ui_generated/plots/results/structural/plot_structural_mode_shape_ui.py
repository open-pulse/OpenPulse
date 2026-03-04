# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_structural_mode_shape.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(330, 499)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, 10, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 32))
        self.label_title.setMaximumSize(QSize(16777215, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_title.setFont(font)
        self.label_title.setFrameShape(QFrame.NoFrame)
        self.label_title.setFrameShadow(QFrame.Raised)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_frequencies = QFrame(Form)
        self.frame_frequencies.setObjectName(u"frame_frequencies")
        self.frame_frequencies.setSizeIncrement(QSize(400, 0))
        self.frame_frequencies.setBaseSize(QSize(400, 0))
        self.frame_frequencies.setFrameShape(QFrame.Box)
        self.frame_frequencies.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_frequencies)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.frame_button = QFrame(self.frame_frequencies)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 40))
        self.frame_button.setMaximumSize(QSize(16777215, 40))
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_button)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot = QPushButton(self.frame_button)
        self.pushButton_plot.setObjectName(u"pushButton_plot")
        self.pushButton_plot.setMinimumSize(QSize(160, 30))
        self.pushButton_plot.setMaximumSize(QSize(160, 30))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_plot.setFont(font1)
        self.pushButton_plot.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton_plot, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_button, 5, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_frequencies)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 40))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_natural_frequency = QLineEdit(self.frame_5)
        self.lineEdit_natural_frequency.setObjectName(u"lineEdit_natural_frequency")
        self.lineEdit_natural_frequency.setEnabled(False)
        self.lineEdit_natural_frequency.setMinimumSize(QSize(80, 28))
        self.lineEdit_natural_frequency.setMaximumSize(QSize(80, 28))
        self.lineEdit_natural_frequency.setFont(font1)
        self.lineEdit_natural_frequency.setStyleSheet(u"")
        self.lineEdit_natural_frequency.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_natural_frequency, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 28))
        self.label_4.setMaximumSize(QSize(16777215, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_4.setFont(font2)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 28))
        self.label_7.setMaximumSize(QSize(16777215, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        self.label_7.setFont(font3)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 3, 1, 1)


        self.gridLayout_5.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_scalling2 = QFrame(self.frame_frequencies)
        self.frame_scalling2.setObjectName(u"frame_scalling2")
        self.frame_scalling2.setMinimumSize(QSize(0, 40))
        self.frame_scalling2.setMaximumSize(QSize(16777215, 40))
        self.frame_scalling2.setFrameShape(QFrame.NoFrame)
        self.frame_scalling2.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_scalling2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.comboBox_color_scale = QComboBox(self.frame_scalling2)
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
        font4 = QFont()
        font4.setPointSize(10)
        self.comboBox_color_scale.setFont(font4)

        self.gridLayout_9.addWidget(self.comboBox_color_scale, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_scalling2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(90, 26))
        self.label_2.setMaximumSize(QSize(90, 26))
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_scalling2, 4, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_frequencies)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(10, 2, 10, 2)
        self.treeWidget_frequencies = QTreeWidget(self.frame_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(1, u"Natural frequency [Hz]");
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font1);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font1);
        self.treeWidget_frequencies.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_frequencies.setObjectName(u"treeWidget_frequencies")
        self.treeWidget_frequencies.setMinimumSize(QSize(260, 0))
        self.treeWidget_frequencies.setMaximumSize(QSize(600, 600))
        self.treeWidget_frequencies.setFont(font1)
        self.treeWidget_frequencies.setStyleSheet(u"")
        self.treeWidget_frequencies.setAlternatingRowColors(True)
        self.treeWidget_frequencies.setIndentation(0)

        self.gridLayout_3.addWidget(self.treeWidget_frequencies, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_4, 1, 0, 1, 1)

        self.frame = QFrame(self.frame_frequencies)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_13, 0, 0, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_12, 0, 4, 1, 1)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(90, 26))
        self.label_6.setMaximumSize(QSize(90, 26))
        self.label_6.setFont(font4)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_6, 0, 1, 1, 1)

        self.comboBox_colormaps = QComboBox(self.frame)
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
        self.comboBox_colormaps.setFont(font4)

        self.gridLayout_13.addWidget(self.comboBox_colormaps, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame, 2, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_frequencies)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 40))
        self.frame_6.setMaximumSize(QSize(16777215, 40))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(90, 26))
        self.label_5.setMaximumSize(QSize(90, 26))
        self.label_5.setFont(font4)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_5, 0, 1, 1, 1)

        self.slider_transparency = QSlider(self.frame_6)
        self.slider_transparency.setObjectName(u"slider_transparency")
        self.slider_transparency.setMinimumSize(QSize(176, 0))
        self.slider_transparency.setMaximumSize(QSize(200, 16777215))
        self.slider_transparency.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.slider_transparency, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_8, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_6, 3, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_frequencies, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_natural_frequency, self.treeWidget_frequencies)
        QWidget.setTabOrder(self.treeWidget_frequencies, self.comboBox_colormaps)
        QWidget.setTabOrder(self.comboBox_colormaps, self.slider_transparency)
        QWidget.setTabOrder(self.slider_transparency, self.comboBox_color_scale)
        QWidget.setTabOrder(self.comboBox_color_scale, self.pushButton_plot)

        self.retranslateUi(Form)

        self.pushButton_plot.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Plot structural mode shape", None))
        self.label_title.setText(QCoreApplication.translate("Form", u"Plot the structural mode shape", None))
        self.pushButton_plot.setText(QCoreApplication.translate("Form", u"Plot the mode shape", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Natural frequency:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"[Hz]", None))
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
        ___qtreewidgetitem = self.treeWidget_frequencies.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Mode", None));
#if QT_CONFIG(tooltip)
        self.treeWidget_frequencies.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the mode shape to be plotted</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Form", u"Colormaps:", None))
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

        self.label_5.setText(QCoreApplication.translate("Form", u"Transparency:", None))
    # retranslateUi



class PlotStructuralModeShape_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
                - frame_frequencies: QFrame
                    - (Layout): QGridLayout
                            - frame_button: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot: QPushButton
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_natural_frequency: QLineEdit
                                        - label_4: QLabel
                                        - label_7: QLabel
                            - frame_scalling2: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_color_scale: QComboBox
                                        - label_2: QLabel
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_frequencies: QTreeWidget
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - label_6: QLabel
                                        - comboBox_colormaps: QComboBox
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - label_5: QLabel
                                        - slider_transparency: QSlider
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
