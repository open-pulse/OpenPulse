# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inertial_load_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(340, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(340, 300))
        Dialog.setMaximumSize(QSize(340, 300))
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_main = QFrame(Dialog)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(0, 200))
        self.frame_main.setMaximumSize(QSize(16777215, 16777215))
        self.frame_main.setFrameShape(QFrame.Box)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_main)
        self.gridLayout_8.setSpacing(2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.frame_gravity_model_setup = QFrame(self.frame_main)
        self.frame_gravity_model_setup.setObjectName(u"frame_gravity_model_setup")
        self.frame_gravity_model_setup.setMinimumSize(QSize(0, 40))
        self.frame_gravity_model_setup.setMaximumSize(QSize(360, 50))
        self.frame_gravity_model_setup.setFrameShape(QFrame.NoFrame)
        self.frame_gravity_model_setup.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_gravity_model_setup)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_7, 0, 0, 1, 1)

        self.checkBox_stiffening_effect = QCheckBox(self.frame_gravity_model_setup)
        self.checkBox_stiffening_effect.setObjectName(u"checkBox_stiffening_effect")
        self.checkBox_stiffening_effect.setMinimumSize(QSize(0, 26))
        self.checkBox_stiffening_effect.setMaximumSize(QSize(16777215, 26))
        font = QFont()
        font.setPointSize(10)
        self.checkBox_stiffening_effect.setFont(font)
        self.checkBox_stiffening_effect.setChecked(True)

        self.gridLayout_7.addWidget(self.checkBox_stiffening_effect, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)


        self.gridLayout_8.addWidget(self.frame_gravity_model_setup, 0, 0, 1, 1)

        self.frame_x_direction = QFrame(self.frame_main)
        self.frame_x_direction.setObjectName(u"frame_x_direction")
        self.frame_x_direction.setMinimumSize(QSize(0, 40))
        self.frame_x_direction.setMaximumSize(QSize(360, 50))
        self.frame_x_direction.setFrameShape(QFrame.NoFrame)
        self.frame_x_direction.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_x_direction)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(2)
        self.gridLayout_6.setContentsMargins(2, 0, 2, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label = QLabel(self.frame_x_direction)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 28))
        self.label.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.label.setFont(font1)

        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)

        self.label_13 = QLabel(self.frame_x_direction)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 28))
        self.label_13.setMaximumSize(QSize(52, 28))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_13, 0, 3, 1, 1)

        self.lineEdit_acceleration_x_axis = QLineEdit(self.frame_x_direction)
        self.lineEdit_acceleration_x_axis.setObjectName(u"lineEdit_acceleration_x_axis")
        self.lineEdit_acceleration_x_axis.setMinimumSize(QSize(90, 28))
        self.lineEdit_acceleration_x_axis.setMaximumSize(QSize(90, 28))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_acceleration_x_axis.setFont(font3)
        self.lineEdit_acceleration_x_axis.setStyleSheet(u"")
        self.lineEdit_acceleration_x_axis.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_acceleration_x_axis, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.gridLayout_8.addWidget(self.frame_x_direction, 1, 0, 1, 1)

        self.frame_y_direction = QFrame(self.frame_main)
        self.frame_y_direction.setObjectName(u"frame_y_direction")
        self.frame_y_direction.setMinimumSize(QSize(0, 40))
        self.frame_y_direction.setMaximumSize(QSize(360, 50))
        self.frame_y_direction.setFrameShape(QFrame.NoFrame)
        self.frame_y_direction.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_y_direction)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(2)
        self.gridLayout_5.setContentsMargins(2, 0, 2, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.label_14 = QLabel(self.frame_y_direction)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 28))
        self.label_14.setMaximumSize(QSize(52, 28))
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.label_14, 0, 3, 1, 1)

        self.lineEdit_acceleration_y_axis = QLineEdit(self.frame_y_direction)
        self.lineEdit_acceleration_y_axis.setObjectName(u"lineEdit_acceleration_y_axis")
        self.lineEdit_acceleration_y_axis.setMinimumSize(QSize(90, 28))
        self.lineEdit_acceleration_y_axis.setMaximumSize(QSize(90, 28))
        self.lineEdit_acceleration_y_axis.setFont(font3)
        self.lineEdit_acceleration_y_axis.setStyleSheet(u"")
        self.lineEdit_acceleration_y_axis.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_acceleration_y_axis, 0, 2, 1, 1)

        self.label_2 = QLabel(self.frame_y_direction)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 28))
        self.label_2.setMaximumSize(QSize(16777215, 28))
        self.label_2.setFont(font1)

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.gridLayout_8.addWidget(self.frame_y_direction, 2, 0, 1, 1)

        self.frame_z_direction = QFrame(self.frame_main)
        self.frame_z_direction.setObjectName(u"frame_z_direction")
        self.frame_z_direction.setMinimumSize(QSize(0, 40))
        self.frame_z_direction.setMaximumSize(QSize(360, 50))
        self.frame_z_direction.setFrameShape(QFrame.NoFrame)
        self.frame_z_direction.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_z_direction)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(2)
        self.gridLayout_4.setContentsMargins(2, 0, 2, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.label_unit_3 = QLabel(self.frame_z_direction)
        self.label_unit_3.setObjectName(u"label_unit_3")
        self.label_unit_3.setMinimumSize(QSize(0, 28))
        self.label_unit_3.setMaximumSize(QSize(52, 28))
        self.label_unit_3.setFont(font2)
        self.label_unit_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_unit_3, 0, 3, 1, 1)

        self.label_3 = QLabel(self.frame_z_direction)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(16777215, 28))
        self.label_3.setFont(font1)

        self.gridLayout_4.addWidget(self.label_3, 0, 1, 1, 1)

        self.lineEdit_acceleration_z_axis = QLineEdit(self.frame_z_direction)
        self.lineEdit_acceleration_z_axis.setObjectName(u"lineEdit_acceleration_z_axis")
        self.lineEdit_acceleration_z_axis.setMinimumSize(QSize(90, 28))
        self.lineEdit_acceleration_z_axis.setMaximumSize(QSize(90, 28))
        self.lineEdit_acceleration_z_axis.setFont(font3)
        self.lineEdit_acceleration_z_axis.setStyleSheet(u"")
        self.lineEdit_acceleration_z_axis.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_acceleration_z_axis, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_z_direction, 3, 0, 1, 1)

        self.frame_button = QFrame(self.frame_main)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setMinimumSize(QSize(0, 0))
        self.frame_button.setMaximumSize(QSize(16777215, 48))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.frame_button.setFont(font4)
        self.frame_button.setFrameShape(QFrame.NoFrame)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_button)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_button)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font3)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_button)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font3)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_button, 4, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_main, 1, 0, 1, 1)

        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFont(font4)
        self.frame_title.setStyleSheet(u"")
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.frame_title.setLineWidth(1)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(0, 40))
        self.label_title.setMaximumSize(QSize(16777215, 40))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(11)
        font5.setBold(False)
        font5.setItalic(False)
        self.label_title.setFont(font5)
        self.label_title.setTextFormat(Qt.AutoText)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        QWidget.setTabOrder(self.checkBox_stiffening_effect, self.lineEdit_acceleration_x_axis)
        QWidget.setTabOrder(self.lineEdit_acceleration_x_axis, self.lineEdit_acceleration_y_axis)
        QWidget.setTabOrder(self.lineEdit_acceleration_y_axis, self.lineEdit_acceleration_z_axis)
        QWidget.setTabOrder(self.lineEdit_acceleration_z_axis, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)

        self.retranslateUi(Dialog)

        self.pushButton_attribute.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Set inertial load", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(tooltip)
        self.checkBox_stiffening_effect.setToolTip(QCoreApplication.translate("Dialog", u"Enable stiffness matrix updating in modal and harmonic analysis.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_stiffening_effect.setText(QCoreApplication.translate("Dialog", u"Enable stiffening effect", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"x-axis acceleration:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"[m/s\u00b2]", None))
        self.lineEdit_acceleration_x_axis.setText("")
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[m/s\u00b2]", None))
        self.lineEdit_acceleration_y_axis.setText(QCoreApplication.translate("Dialog", u"-9.80665", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"y-axis acceleration:", None))
        self.label_unit_3.setText(QCoreApplication.translate("Dialog", u"[m/s\u00b2]", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"z-axis acceleration:", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"Set inertial load", None))
    # retranslateUi



class InertialLoadInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_main: QFrame
                    - (Layout): QGridLayout
                            - frame_gravity_model_setup: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_stiffening_effect: QCheckBox
                            - frame_x_direction: QFrame
                                - (Layout): QGridLayout
                                        - label: QLabel
                                        - label_13: QLabel
                                        - lineEdit_acceleration_x_axis: QLineEdit
                            - frame_y_direction: QFrame
                                - (Layout): QGridLayout
                                        - label_14: QLabel
                                        - lineEdit_acceleration_y_axis: QLineEdit
                                        - label_2: QLabel
                            - frame_z_direction: QFrame
                                - (Layout): QGridLayout
                                        - label_unit_3: QLabel
                                        - label_3: QLabel
                                        - lineEdit_acceleration_z_axis: QLineEdit
                            - frame_button: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_attribute: QPushButton
                                        - pushButton_exit: QPushButton
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label_title: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
