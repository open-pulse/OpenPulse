# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_stresses_for_harmonic_analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 260)
        Form.setMinimumSize(QSize(300, 260))
        Form.setMaximumSize(QSize(16777215, 280))
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(1, 4, 1, 4)
        self.frame_title = QFrame(Form)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 48))
        self.frame_title.setMaximumSize(QSize(480, 48))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        font.setBold(True)
        self.frame_title.setFont(font)
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_main = QFrame(Form)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 200))
        self.frame_main.setMaximumSize(QSize(480, 240))
        self.frame_main.setFrameShape(QFrame.Shape.Box)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_main)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 6, 4, 4)
        self.frame_selected_id = QFrame(self.frame_main)
        self.frame_selected_id.setObjectName(u"frame_selected_id")
        self.frame_selected_id.setMinimumSize(QSize(0, 40))
        self.frame_selected_id.setMaximumSize(QSize(600, 40))
        self.frame_selected_id.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selected_id.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_selected_id)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(6)
        self.gridLayout_14.setVerticalSpacing(0)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_8, 0, 0, 1, 1)

        self.lineEdit_element_id = QLineEdit(self.frame_selected_id)
        self.lineEdit_element_id.setObjectName(u"lineEdit_element_id")
        self.lineEdit_element_id.setEnabled(True)
        self.lineEdit_element_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_element_id.setMaximumSize(QSize(80, 28))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(250, 250, 250, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        brush2 = QBrush(QColor(100, 100, 100, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        brush3 = QBrush(QColor(240, 240, 240, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_element_id.setPalette(palette)
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.lineEdit_element_id.setFont(font2)
        self.lineEdit_element_id.setStyleSheet(u"")
        self.lineEdit_element_id.setFrame(True)
        self.lineEdit_element_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_element_id.setReadOnly(False)

        self.gridLayout_14.addWidget(self.lineEdit_element_id, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_selected_id)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(90, 28))
        self.label_3.setMaximumSize(QSize(100, 28))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_3, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_selected_id, 0, 0, 1, 1)

        self.frame_buttons = QFrame(self.frame_main)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 40))
        self.frame_buttons.setMaximumSize(QSize(16777215, 40))
        self.frame_buttons.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_buttons)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(4)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_data = QPushButton(self.frame_buttons)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(90, 30))
        self.pushButton_plot_data.setMaximumSize(QSize(90, 30))
        self.pushButton_plot_data.setFont(font2)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_buttons, 3, 0, 1, 1)

        self.frame = QFrame(self.frame_main)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.comboBox_stress_type = QComboBox(self.frame)
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.addItem("")
        self.comboBox_stress_type.setObjectName(u"comboBox_stress_type")
        self.comboBox_stress_type.setMinimumSize(QSize(170, 26))
        self.comboBox_stress_type.setMaximumSize(QSize(170, 26))
        font3 = QFont()
        font3.setPointSize(10)
        self.comboBox_stress_type.setFont(font3)

        self.gridLayout_6.addWidget(self.comboBox_stress_type, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 26))
        self.label_2.setMaximumSize(QSize(70, 26))
        self.label_2.setFont(font3)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_main)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 32))
        self.frame_2.setMaximumSize(QSize(16777215, 32))
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkBox_damping_effect = QCheckBox(self.frame_2)
        self.checkBox_damping_effect.setObjectName(u"checkBox_damping_effect")
        self.checkBox_damping_effect.setMinimumSize(QSize(170, 26))
        self.checkBox_damping_effect.setMaximumSize(QSize(170, 26))
        self.checkBox_damping_effect.setFont(font2)
        self.checkBox_damping_effect.setChecked(False)

        self.gridLayout_4.addWidget(self.checkBox_damping_effect, 0, 2, 1, 1)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(70, 26))
        self.frame_3.setMaximumSize(QSize(70, 26))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.frame_3, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 3, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_main, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_element_id, self.checkBox_damping_effect)
        QWidget.setTabOrder(self.checkBox_damping_effect, self.comboBox_stress_type)
        QWidget.setTabOrder(self.comboBox_stress_type, self.pushButton_plot_data)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot the stress frequency response", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_element_id.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEdit_element_id.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_element_id.setText("")
        self.lineEdit_element_id.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Element ID:", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
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
        self.label_2.setText(QCoreApplication.translate("Form", u"Stress type:", None))
        self.checkBox_damping_effect.setText(QCoreApplication.translate("Form", u"Damping effect", None))
    # retranslateUi



class GetStressesForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_selected_id: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_element_id: QLineEdit
                                        - label_3: QLabel
                            - frame_buttons: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - comboBox_stress_type: QComboBox
                                        - label_2: QLabel
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_damping_effect: QCheckBox
                                        - frame_3: QFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
