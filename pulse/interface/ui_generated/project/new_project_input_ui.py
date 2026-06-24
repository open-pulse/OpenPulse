# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_project_input.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 360)
        Dialog.setMinimumSize(QSize(500, 360))
        Dialog.setMaximumSize(QSize(500, 360))
        Dialog.setStyleSheet(u"")
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame_title = QFrame(Dialog)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 42))
        self.frame_title.setMaximumSize(QSize(16777215, 42))
        self.frame_title.setFrameShape(QFrame.Box)
        self.frame_title.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_title)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_center = QFrame(Dialog)
        self.frame_center.setObjectName(u"frame_center")
        self.frame_center.setMinimumSize(QSize(0, 0))
        self.frame_center.setMaximumSize(QSize(600, 360))
        self.frame_center.setFrameShape(QFrame.Box)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.frame_center.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame_center)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setVerticalSpacing(4)
        self.gridLayout_4.setContentsMargins(4, 6, 4, 6)
        self.frame_6 = QFrame(self.frame_center)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(252, 40))
        self.frame_6.setMaximumSize(QSize(16777215, 40))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.lineEdit_element_size = QLineEdit(self.frame_6)
        self.lineEdit_element_size.setObjectName(u"lineEdit_element_size")
        self.lineEdit_element_size.setEnabled(True)
        self.lineEdit_element_size.setMinimumSize(QSize(100, 28))
        self.lineEdit_element_size.setMaximumSize(QSize(100, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.lineEdit_element_size.setFont(font1)
        self.lineEdit_element_size.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_element_size.setStyleSheet(u"")
        self.lineEdit_element_size.setInputMethodHints(Qt.ImhNone)
        self.lineEdit_element_size.setMaxLength(20)
        self.lineEdit_element_size.setFrame(True)
        self.lineEdit_element_size.setCursorPosition(4)
        self.lineEdit_element_size.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.lineEdit_element_size, 0, 2, 1, 1)

        self.label_element_size = QLabel(self.frame_6)
        self.label_element_size.setObjectName(u"label_element_size")
        self.label_element_size.setMinimumSize(QSize(160, 28))
        self.label_element_size.setMaximumSize(QSize(160, 28))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_element_size.setFont(font2)
        self.label_element_size.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_element_size, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_3, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_6, 3, 0, 1, 1)

        self.frame = QFrame(self.frame_center)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(252, 40))
        self.frame.setMaximumSize(QSize(16777215, 40))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 0, 3, 1, 1)

        self.label_geometry_tolerance = QLabel(self.frame)
        self.label_geometry_tolerance.setObjectName(u"label_geometry_tolerance")
        self.label_geometry_tolerance.setMinimumSize(QSize(160, 28))
        self.label_geometry_tolerance.setMaximumSize(QSize(160, 28))
        self.label_geometry_tolerance.setFont(font2)
        self.label_geometry_tolerance.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_geometry_tolerance, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.lineEdit_geometry_tolerance = QLineEdit(self.frame)
        self.lineEdit_geometry_tolerance.setObjectName(u"lineEdit_geometry_tolerance")
        self.lineEdit_geometry_tolerance.setEnabled(True)
        self.lineEdit_geometry_tolerance.setMinimumSize(QSize(100, 28))
        self.lineEdit_geometry_tolerance.setMaximumSize(QSize(100, 28))
        self.lineEdit_geometry_tolerance.setFont(font1)
        self.lineEdit_geometry_tolerance.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_geometry_tolerance.setStyleSheet(u"")
        self.lineEdit_geometry_tolerance.setInputMethodHints(Qt.ImhNone)
        self.lineEdit_geometry_tolerance.setMaxLength(20)
        self.lineEdit_geometry_tolerance.setFrame(True)
        self.lineEdit_geometry_tolerance.setCursorPosition(4)
        self.lineEdit_geometry_tolerance.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_geometry_tolerance, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame, 4, 0, 1, 1)

        self.frame_3 = QFrame(self.frame_center)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(252, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 40))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setVerticalSpacing(4)
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.label_geometry_file = QLabel(self.frame_3)
        self.label_geometry_file.setObjectName(u"label_geometry_file")
        self.label_geometry_file.setMinimumSize(QSize(120, 28))
        self.label_geometry_file.setMaximumSize(QSize(120, 28))
        self.label_geometry_file.setFont(font2)
        self.label_geometry_file.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_geometry_file, 0, 0, 1, 1)

        self.lineEdit_geometry_path = QLineEdit(self.frame_3)
        self.lineEdit_geometry_path.setObjectName(u"lineEdit_geometry_path")
        self.lineEdit_geometry_path.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_geometry_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_geometry_path.setSizePolicy(sizePolicy)
        self.lineEdit_geometry_path.setMinimumSize(QSize(260, 28))
        self.lineEdit_geometry_path.setMaximumSize(QSize(260, 28))
        self.lineEdit_geometry_path.setSizeIncrement(QSize(0, 1))
        self.lineEdit_geometry_path.setFont(font1)
        self.lineEdit_geometry_path.setStyleSheet(u"")
        self.lineEdit_geometry_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.lineEdit_geometry_path, 0, 1, 1, 1)

        self.pushButton_import_geometry = QPushButton(self.frame_3)
        self.pushButton_import_geometry.setObjectName(u"pushButton_import_geometry")
        self.pushButton_import_geometry.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_import_geometry.sizePolicy().hasHeightForWidth())
        self.pushButton_import_geometry.setSizePolicy(sizePolicy)
        self.pushButton_import_geometry.setMinimumSize(QSize(80, 28))
        self.pushButton_import_geometry.setMaximumSize(QSize(80, 28))
        self.pushButton_import_geometry.setSizeIncrement(QSize(0, 1))
        self.pushButton_import_geometry.setFont(font2)
        self.pushButton_import_geometry.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/020-search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_import_geometry.setIcon(icon)
        self.pushButton_import_geometry.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_import_geometry, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_center)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(252, 40))
        self.frame_5.setMaximumSize(QSize(16777215, 40))
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.label_length_unit = QLabel(self.frame_5)
        self.label_length_unit.setObjectName(u"label_length_unit")
        self.label_length_unit.setMinimumSize(QSize(160, 28))
        self.label_length_unit.setMaximumSize(QSize(160, 28))
        self.label_length_unit.setFont(font2)
        self.label_length_unit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_length_unit, 0, 1, 1, 1)

        self.comboBox_length_unit = QComboBox(self.frame_5)
        self.comboBox_length_unit.addItem("")
        self.comboBox_length_unit.addItem("")
        self.comboBox_length_unit.addItem("")
        self.comboBox_length_unit.setObjectName(u"comboBox_length_unit")
        self.comboBox_length_unit.setMinimumSize(QSize(100, 28))
        self.comboBox_length_unit.setMaximumSize(QSize(100, 28))
        font3 = QFont()
        font3.setPointSize(9)
        self.comboBox_length_unit.setFont(font3)
        self.comboBox_length_unit.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.comboBox_length_unit, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(89, 19, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_2 = QFrame(self.frame_center)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(252, 40))
        self.frame_2.setMaximumSize(QSize(16777215, 40))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(4)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_project_name_2 = QLabel(self.frame_2)
        self.label_project_name_2.setObjectName(u"label_project_name_2")
        self.label_project_name_2.setMinimumSize(QSize(120, 28))
        self.label_project_name_2.setMaximumSize(QSize(120, 28))
        self.label_project_name_2.setFont(font2)
        self.label_project_name_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_project_name_2, 0, 0, 1, 1)

        self.comboBox_start_project = QComboBox(self.frame_2)
        self.comboBox_start_project.addItem("")
        self.comboBox_start_project.addItem("")
        self.comboBox_start_project.setObjectName(u"comboBox_start_project")
        self.comboBox_start_project.setMinimumSize(QSize(260, 28))
        self.comboBox_start_project.setMaximumSize(QSize(260, 28))
        self.comboBox_start_project.setFont(font3)
        self.comboBox_start_project.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.comboBox_start_project, 0, 1, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(80, 28))
        self.frame_4.setMaximumSize(QSize(80, 28))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout_5.addWidget(self.frame_4, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_center, 1, 0, 1, 1)

        self.frame_buttons = QFrame(Dialog)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 52))
        self.frame_buttons.setMaximumSize(QSize(16777215, 52))
        self.frame_buttons.setFrameShape(QFrame.NoFrame)
        self.frame_buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_buttons)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(10)
        self.gridLayout_6.setContentsMargins(10, 0, 10, 0)
        self.pushButton_start_project = QPushButton(self.frame_buttons)
        self.pushButton_start_project.setObjectName(u"pushButton_start_project")
        sizePolicy.setHeightForWidth(self.pushButton_start_project.sizePolicy().hasHeightForWidth())
        self.pushButton_start_project.setSizePolicy(sizePolicy)
        self.pushButton_start_project.setMinimumSize(QSize(80, 30))
        self.pushButton_start_project.setMaximumSize(QSize(80, 30))
        self.pushButton_start_project.setSizeIncrement(QSize(0, 1))
        self.pushButton_start_project.setFont(font2)
        self.pushButton_start_project.setStyleSheet(u"")
        self.pushButton_start_project.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_start_project, 0, 1, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_buttons)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setMinimumSize(QSize(80, 30))
        self.pushButton_cancel.setMaximumSize(QSize(80, 30))
        self.pushButton_cancel.setSizeIncrement(QSize(0, 1))
        self.pushButton_cancel.setFont(font2)
        self.pushButton_cancel.setStyleSheet(u"")
        self.pushButton_cancel.setAutoDefault(False)

        self.gridLayout_6.addWidget(self.pushButton_cancel, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_buttons, 2, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_start_project, self.lineEdit_geometry_path)
        QWidget.setTabOrder(self.lineEdit_geometry_path, self.pushButton_import_geometry)
        QWidget.setTabOrder(self.pushButton_import_geometry, self.comboBox_length_unit)
        QWidget.setTabOrder(self.comboBox_length_unit, self.lineEdit_element_size)
        QWidget.setTabOrder(self.lineEdit_element_size, self.lineEdit_geometry_tolerance)
        QWidget.setTabOrder(self.lineEdit_geometry_tolerance, self.pushButton_start_project)
        QWidget.setTabOrder(self.pushButton_start_project, self.pushButton_cancel)

        self.retranslateUi(Dialog)

        self.comboBox_start_project.setCurrentIndex(1)
        self.pushButton_start_project.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"OpenPulse", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"New project settings", None))
        self.lineEdit_element_size.setText(QCoreApplication.translate("Dialog", u"0.01", None))
        self.lineEdit_element_size.setPlaceholderText(QCoreApplication.translate("Dialog", u"< Insert a value >", None))
        self.label_element_size.setText(QCoreApplication.translate("Dialog", u"Element size [m]:", None))
        self.label_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"Geometry tolerance [m]:", None))
        self.lineEdit_geometry_tolerance.setText(QCoreApplication.translate("Dialog", u"1e-6", None))
        self.lineEdit_geometry_tolerance.setPlaceholderText(QCoreApplication.translate("Dialog", u"< Insert a value >", None))
        self.label_geometry_file.setText(QCoreApplication.translate("Dialog", u"Geometry file:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_geometry_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Geometry file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_import_geometry.setText(QCoreApplication.translate("Dialog", u"Import", None))
        self.label_length_unit.setText(QCoreApplication.translate("Dialog", u"Length unit:", None))
        self.comboBox_length_unit.setItemText(0, QCoreApplication.translate("Dialog", u" meter", None))
        self.comboBox_length_unit.setItemText(1, QCoreApplication.translate("Dialog", u" millimeter", None))
        self.comboBox_length_unit.setItemText(2, QCoreApplication.translate("Dialog", u" inch", None))

        self.label_project_name_2.setText(QCoreApplication.translate("Dialog", u"Geometry options:", None))
        self.comboBox_start_project.setItemText(0, QCoreApplication.translate("Dialog", u"   Start a project with geometry file", None))
        self.comboBox_start_project.setItemText(1, QCoreApplication.translate("Dialog", u"   Start a project without geometry", None))

        self.pushButton_start_project.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class NewProjectInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_title: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_center: QFrame
                    - (Layout): QGridLayout
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - lineEdit_element_size: QLineEdit
                                        - label_element_size: QLabel
                            - frame: QFrame
                                - (Layout): QGridLayout
                                        - label_geometry_tolerance: QLabel
                                        - lineEdit_geometry_tolerance: QLineEdit
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - label_geometry_file: QLabel
                                        - lineEdit_geometry_path: QLineEdit
                                        - pushButton_import_geometry: QPushButton
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - label_length_unit: QLabel
                                        - comboBox_length_unit: QComboBox
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_project_name_2: QLabel
                                        - comboBox_start_project: QComboBox
                                        - frame_4: QFrame
                - frame_buttons: QFrame
                    - (Layout): QGridLayout
                            - pushButton_start_project: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
