# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acoustic_model_info.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(600, 680)
        dialog.setMinimumSize(QSize(600, 680))
        dialog.setMaximumSize(QSize(600, 680))
        self.gridLayout_4 = QGridLayout(dialog)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 42))
        self.frame_3.setMaximumSize(QSize(16777215, 42))
        self.frame_3.setFrameShape(QFrame.Box)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.frame_3)
        self.label_12.setObjectName(u"label_12")
        font = QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setFrameShape(QFrame.NoFrame)
        self.label_12.setTextFormat(Qt.AutoText)
        self.label_12.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_3, 0, 0, 1, 1)

        self.frame_2 = QFrame(dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(310, 510))
        self.frame_2.setMaximumSize(QSize(1000, 580))
        self.frame_2.setFrameShape(QFrame.Box)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.treeWidget_specific_impedance = QTreeWidget(self.frame_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_specific_impedance.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_specific_impedance.setObjectName(u"treeWidget_specific_impedance")
        self.treeWidget_specific_impedance.setMinimumSize(QSize(280, 130))
        self.treeWidget_specific_impedance.setMaximumSize(QSize(280, 130))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        self.treeWidget_specific_impedance.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_specific_impedance, 5, 0, 1, 1)

        self.treeWidget_acoustic_pressure = QTreeWidget(self.frame_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_acoustic_pressure.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_acoustic_pressure.setObjectName(u"treeWidget_acoustic_pressure")
        self.treeWidget_acoustic_pressure.setMinimumSize(QSize(280, 130))
        self.treeWidget_acoustic_pressure.setMaximumSize(QSize(280, 130))
        self.treeWidget_acoustic_pressure.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_acoustic_pressure, 1, 0, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 30))
        self.label_11.setMaximumSize(QSize(16777215, 30))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_11.setFont(font2)
        self.label_11.setFrameShape(QFrame.Box)
        self.label_11.setFrameShadow(QFrame.Raised)
        self.label_11.setTextFormat(Qt.AutoText)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.treeWidget_volume_velocity = QTreeWidget(self.frame_2)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_volume_velocity.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_volume_velocity.setObjectName(u"treeWidget_volume_velocity")
        self.treeWidget_volume_velocity.setMinimumSize(QSize(280, 130))
        self.treeWidget_volume_velocity.setMaximumSize(QSize(280, 130))
        self.treeWidget_volume_velocity.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_volume_velocity, 3, 0, 1, 1)

        self.label_17 = QLabel(self.frame_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 30))
        self.label_17.setMaximumSize(QSize(16777215, 30))
        self.label_17.setFont(font2)
        self.label_17.setFrameShape(QFrame.Box)
        self.label_17.setFrameShadow(QFrame.Raised)
        self.label_17.setTextFormat(Qt.AutoText)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_17, 4, 0, 1, 1)

        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(0, 30))
        self.label_10.setMaximumSize(QSize(16777215, 30))
        self.label_10.setFont(font2)
        self.label_10.setFrameShape(QFrame.Box)
        self.label_10.setFrameShadow(QFrame.Raised)
        self.label_10.setTextFormat(Qt.AutoText)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 30))
        self.label_9.setMaximumSize(QSize(16777215, 30))
        self.label_9.setFont(font2)
        self.label_9.setFrameShape(QFrame.Box)
        self.label_9.setFrameShadow(QFrame.Raised)
        self.label_9.setTextFormat(Qt.AutoText)
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.treeWidget_radiation_impedance = QTreeWidget(self.frame_2)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem3.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_radiation_impedance.setHeaderItem(__qtreewidgetitem3)
        self.treeWidget_radiation_impedance.setObjectName(u"treeWidget_radiation_impedance")
        self.treeWidget_radiation_impedance.setMinimumSize(QSize(280, 130))
        self.treeWidget_radiation_impedance.setMaximumSize(QSize(280, 130))
        self.treeWidget_radiation_impedance.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_radiation_impedance, 1, 1, 1, 1)

        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 30))
        self.label_15.setMaximumSize(QSize(16777215, 30))
        self.label_15.setFont(font2)
        self.label_15.setFrameShape(QFrame.Box)
        self.label_15.setFrameShadow(QFrame.Raised)
        self.label_15.setTextFormat(Qt.AutoText)
        self.label_15.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_15, 2, 1, 1, 1)

        self.treeWidget_perforated_plate = QTreeWidget(self.frame_2)
        __qtreewidgetitem4 = QTreeWidgetItem()
        __qtreewidgetitem4.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem4.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_perforated_plate.setHeaderItem(__qtreewidgetitem4)
        self.treeWidget_perforated_plate.setObjectName(u"treeWidget_perforated_plate")
        self.treeWidget_perforated_plate.setMinimumSize(QSize(280, 130))
        self.treeWidget_perforated_plate.setMaximumSize(QSize(280, 130))
        self.treeWidget_perforated_plate.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_perforated_plate, 3, 1, 1, 1)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 30))
        self.label_16.setMaximumSize(QSize(16777215, 30))
        self.label_16.setFont(font2)
        self.label_16.setFrameShape(QFrame.Box)
        self.label_16.setFrameShadow(QFrame.Raised)
        self.label_16.setTextFormat(Qt.AutoText)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_16, 4, 1, 1, 1)

        self.treeWidget_element_length_correction = QTreeWidget(self.frame_2)
        __qtreewidgetitem5 = QTreeWidgetItem()
        __qtreewidgetitem5.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem5.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget_element_length_correction.setHeaderItem(__qtreewidgetitem5)
        self.treeWidget_element_length_correction.setObjectName(u"treeWidget_element_length_correction")
        self.treeWidget_element_length_correction.setMinimumSize(QSize(280, 130))
        self.treeWidget_element_length_correction.setMaximumSize(QSize(280, 130))
        self.treeWidget_element_length_correction.setFont(font1)

        self.gridLayout.addWidget(self.treeWidget_element_length_correction, 5, 1, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_4 = QFrame(dialog)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 80))
        self.frame_4.setMaximumSize(QSize(16777215, 80))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_number_elements = QLineEdit(self.frame_4)
        self.lineEdit_number_elements.setObjectName(u"lineEdit_number_elements")
        self.lineEdit_number_elements.setEnabled(False)
        self.lineEdit_number_elements.setMinimumSize(QSize(80, 26))
        self.lineEdit_number_elements.setMaximumSize(QSize(80, 26))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(250, 250, 250, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
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
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_number_elements.setPalette(palette)
        self.lineEdit_number_elements.setFont(font2)
        self.lineEdit_number_elements.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}background-color: rgb(255, 255, 255);")
        self.lineEdit_number_elements.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_number_elements, 1, 2, 1, 1)

        self.label_13 = QLabel(self.frame_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 26))
        self.label_13.setMaximumSize(QSize(200, 26))
        self.label_13.setFont(font2)
        self.label_13.setFrameShape(QFrame.NoFrame)
        self.label_13.setTextFormat(Qt.AutoText)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 0, 1, 1, 1)

        self.label_14 = QLabel(self.frame_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 26))
        self.label_14.setMaximumSize(QSize(200, 26))
        self.label_14.setFont(font2)
        self.label_14.setFrameShape(QFrame.NoFrame)
        self.label_14.setTextFormat(Qt.AutoText)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_14, 1, 1, 1, 1)

        self.lineEdit_number_nodes = QLineEdit(self.frame_4)
        self.lineEdit_number_nodes.setObjectName(u"lineEdit_number_nodes")
        self.lineEdit_number_nodes.setEnabled(False)
        self.lineEdit_number_nodes.setMinimumSize(QSize(80, 26))
        self.lineEdit_number_nodes.setMaximumSize(QSize(80, 26))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_number_nodes.setPalette(palette1)
        self.lineEdit_number_nodes.setFont(font2)
        self.lineEdit_number_nodes.setStyleSheet(u"QLineEdit{color: rgb(0, 0, 0); background-color: rgb(250, 250, 250)}\n"
"QLineEdit:disabled{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}background-color: rgb(255, 255, 255);")
        self.lineEdit_number_nodes.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_number_nodes, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_4, 2, 0, 1, 1)

        QWidget.setTabOrder(self.treeWidget_acoustic_pressure, self.treeWidget_radiation_impedance)
        QWidget.setTabOrder(self.treeWidget_radiation_impedance, self.treeWidget_volume_velocity)
        QWidget.setTabOrder(self.treeWidget_volume_velocity, self.treeWidget_perforated_plate)
        QWidget.setTabOrder(self.treeWidget_perforated_plate, self.treeWidget_specific_impedance)
        QWidget.setTabOrder(self.treeWidget_specific_impedance, self.treeWidget_element_length_correction)
        QWidget.setTabOrder(self.treeWidget_element_length_correction, self.lineEdit_number_nodes)
        QWidget.setTabOrder(self.lineEdit_number_nodes, self.lineEdit_number_elements)

        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Acoustic Model Information", None))
        self.label_12.setText(QCoreApplication.translate("dialog", u"Acoustic model information", None))
        ___qtreewidgetitem = self.treeWidget_specific_impedance.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("dialog", u"Values", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("dialog", u"Nodes", None));
        ___qtreewidgetitem1 = self.treeWidget_acoustic_pressure.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("dialog", u"Values", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("dialog", u"Nodes", None));
        self.label_11.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Volume velocity:</p></body></html>", None))
        ___qtreewidgetitem2 = self.treeWidget_volume_velocity.headerItem()
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("dialog", u"Values", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("dialog", u"Nodes", None));
        self.label_17.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Specific impedance:</p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Acoustic pressure:</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Radiation impedance:</p></body></html>", None))
        ___qtreewidgetitem3 = self.treeWidget_radiation_impedance.headerItem()
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("dialog", u"Type", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("dialog", u"Nodes", None));
        self.label_15.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Perforated plate:</p></body></html>", None))
        ___qtreewidgetitem4 = self.treeWidget_perforated_plate.headerItem()
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("dialog", u"PP parameteres", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("dialog", u"Elements", None));
        self.label_16.setText(QCoreApplication.translate("dialog", u"<html><head/><body><p align=\"center\">Elements with length correction:</p></body></html>", None))
        ___qtreewidgetitem5 = self.treeWidget_element_length_correction.headerItem()
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("dialog", u"Type", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("dialog", u"Elements", None));
        self.label_13.setText(QCoreApplication.translate("dialog", u"Number of nodes:", None))
        self.label_14.setText(QCoreApplication.translate("dialog", u"Number of elements:", None))
    # retranslateUi



class AcousticModelInfo_UI(QDialog, Ui_dialog):
    """
    Component Hierarchy:
    - dialog: QDialog
        - (Layout): QGridLayout
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_12: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - treeWidget_specific_impedance: QTreeWidget
                            - treeWidget_acoustic_pressure: QTreeWidget
                            - label_11: QLabel
                            - treeWidget_volume_velocity: QTreeWidget
                            - label_17: QLabel
                            - label_10: QLabel
                            - label_9: QLabel
                            - treeWidget_radiation_impedance: QTreeWidget
                            - label_15: QLabel
                            - treeWidget_perforated_plate: QTreeWidget
                            - label_16: QLabel
                            - treeWidget_element_length_correction: QTreeWidget
                - frame_4: QFrame
                    - (Layout): QGridLayout
                            - lineEdit_number_elements: QLineEdit
                            - label_13: QLabel
                            - label_14: QLabel
                            - lineEdit_number_nodes: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
