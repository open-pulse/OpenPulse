# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'save_project_data_selector.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(340, 260)
        Dialog.setMinimumSize(QSize(340, 260))
        Dialog.setMaximumSize(QSize(340, 260))
        font = QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.checkBox_solution_data = QCheckBox(self.frame_2)
        self.checkBox_solution_data.setObjectName(u"checkBox_solution_data")
        self.checkBox_solution_data.setMinimumSize(QSize(0, 28))
        self.checkBox_solution_data.setMaximumSize(QSize(260, 28))
        self.checkBox_solution_data.setFont(font)
        self.checkBox_solution_data.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_solution_data, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.checkBox_mesh_data = QCheckBox(self.frame_2)
        self.checkBox_mesh_data.setObjectName(u"checkBox_mesh_data")
        self.checkBox_mesh_data.setMinimumSize(QSize(0, 28))
        self.checkBox_mesh_data.setMaximumSize(QSize(260, 28))
        self.checkBox_mesh_data.setFont(font)
        self.checkBox_mesh_data.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_mesh_data, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 2, 0, 1, 1)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 60))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(6)
        self.gridLayout_6.setVerticalSpacing(4)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 28))
        self.label_2.setMaximumSize(QSize(16777215, 28))
        self.label_2.setFont(font)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 28))
        self.label_3.setMaximumSize(QSize(16777215, 28))
        self.label_3.setFont(font)

        self.gridLayout_6.addWidget(self.label_3, 0, 3, 1, 1)

        self.lineEdit_required_memory = QLineEdit(self.frame_5)
        self.lineEdit_required_memory.setObjectName(u"lineEdit_required_memory")
        self.lineEdit_required_memory.setMinimumSize(QSize(100, 28))
        self.lineEdit_required_memory.setMaximumSize(QSize(100, 28))
        self.lineEdit_required_memory.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.lineEdit_required_memory, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.gridLayout_4.addWidget(self.frame_5, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 40))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 26))
        self.label.setMaximumSize(QSize(16777215, 32))
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_4 = QFrame(Dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.frame_4.setMaximumSize(QSize(16777215, 48))
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.pushButton_proceed = QPushButton(self.frame_4)
        self.pushButton_proceed.setObjectName(u"pushButton_proceed")
        self.pushButton_proceed.setMinimumSize(QSize(110, 30))
        self.pushButton_proceed.setMaximumSize(QSize(110, 30))
        self.pushButton_proceed.setFont(font)
        self.pushButton_proceed.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_proceed, 0, 1, 1, 1)

        self.pushButton_cancel = QPushButton(self.frame_4)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(110, 30))
        self.pushButton_cancel.setMaximumSize(QSize(110, 30))
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setAutoDefault(False)

        self.gridLayout_5.addWidget(self.pushButton_cancel, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_4, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_required_memory, self.checkBox_mesh_data)
        QWidget.setTabOrder(self.checkBox_mesh_data, self.checkBox_solution_data)
        QWidget.setTabOrder(self.checkBox_solution_data, self.pushButton_proceed)

        self.retranslateUi(Dialog)

        self.pushButton_proceed.setDefault(False)
        self.pushButton_cancel.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Project data to save", None))
#if QT_CONFIG(tooltip)
        self.checkBox_solution_data.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Save the solution data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_solution_data.setText(QCoreApplication.translate("Dialog", u"Solution data", None))
#if QT_CONFIG(tooltip)
        self.checkBox_mesh_data.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Save the mesh data</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mesh_data.setText(QCoreApplication.translate("Dialog", u"Mesh data", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Required memory:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"[MB]", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Project data to save", None))
        self.pushButton_proceed.setText(QCoreApplication.translate("Dialog", u"Proceed", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi



class SaveProjectDataSelector_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - checkBox_solution_data: QCheckBox
                                        - checkBox_mesh_data: QCheckBox
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - label_3: QLabel
                                        - lineEdit_required_memory: QLineEdit
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - pushButton_proceed: QPushButton
                            - pushButton_cancel: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
