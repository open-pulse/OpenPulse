# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_input_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(620, 340)
        Form.setMaximumSize(QSize(16777215, 360))
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 48))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.pushButton_attribute = QPushButton(self.frame_3)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(120, 32))
        self.pushButton_attribute.setMaximumSize(QSize(120, 32))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_3)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(120, 32))
        self.pushButton_exit.setMaximumSize(QSize(120, 32))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.tableWidget_material_data = QTableWidget(self.frame_2)
        if (self.tableWidget_material_data.rowCount() < 7):
            self.tableWidget_material_data.setRowCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_material_data.setVerticalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget_material_data.setObjectName(u"tableWidget_material_data")
        self.tableWidget_material_data.horizontalHeader().setVisible(False)
        self.tableWidget_material_data.verticalHeader().setVisible(True)
        self.tableWidget_material_data.verticalHeader().setCascadingSectionResizes(True)

        self.gridLayout_2.addWidget(self.tableWidget_material_data, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 0))
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_remove_column = QPushButton(self.frame_6)
        self.pushButton_remove_column.setObjectName(u"pushButton_remove_column")
        self.pushButton_remove_column.setMinimumSize(QSize(26, 26))
        self.pushButton_remove_column.setMaximumSize(QSize(26, 26))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_remove_column.setFont(font1)
        self.pushButton_remove_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_remove_column, 0, 3, 1, 1)

        self.pushButton_add_column = QPushButton(self.frame_6)
        self.pushButton_add_column.setObjectName(u"pushButton_add_column")
        self.pushButton_add_column.setMinimumSize(QSize(26, 26))
        self.pushButton_add_column.setMaximumSize(QSize(26, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_add_column.setFont(font2)
        self.pushButton_add_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_add_column, 0, 2, 1, 1)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_reset_library = QPushButton(self.frame_7)
        self.pushButton_reset_library.setObjectName(u"pushButton_reset_library")
        self.pushButton_reset_library.setMinimumSize(QSize(60, 26))
        self.pushButton_reset_library.setMaximumSize(QSize(60, 26))
        self.pushButton_reset_library.setFont(font)
        self.pushButton_reset_library.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_reset_library, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_7, 0, 0, 1, 1)

        self.pushButton_duplicate = QPushButton(self.frame_6)
        self.pushButton_duplicate.setObjectName(u"pushButton_duplicate")
        self.pushButton_duplicate.setMinimumSize(QSize(28, 28))
        self.pushButton_duplicate.setMaximumSize(QSize(28, 28))
        self.pushButton_duplicate.setFont(font1)
        self.pushButton_duplicate.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/mpltoolbar/copy_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_duplicate.setIcon(icon)
        self.pushButton_duplicate.setIconSize(QSize(18, 18))

        self.gridLayout_5.addWidget(self.pushButton_duplicate, 0, 4, 1, 1)


        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_reset_library, self.pushButton_add_column)
        QWidget.setTabOrder(self.pushButton_add_column, self.pushButton_remove_column)
        QWidget.setTabOrder(self.pushButton_remove_column, self.tableWidget_material_data)
        QWidget.setTabOrder(self.tableWidget_material_data, self.pushButton_attribute)

        self.retranslateUi(Form)

        self.pushButton_attribute.setDefault(True)
        self.pushButton_exit.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.pushButton_attribute.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Confirm material attribution</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_attribute.setText(QCoreApplication.translate("Form", u"Attribute", None))
#if QT_CONFIG(tooltip)
        self.pushButton_exit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Confirm material attribution</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exit.setText(QCoreApplication.translate("Form", u"Exit", None))
        ___qtablewidgetitem = self.tableWidget_material_data.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None))
        ___qtablewidgetitem1 = self.tableWidget_material_data.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Identifier", None))
        ___qtablewidgetitem2 = self.tableWidget_material_data.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Density [kg/m\u00b3]", None))
        ___qtablewidgetitem3 = self.tableWidget_material_data.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Elasticity modulus [GPa]", None))
        ___qtablewidgetitem4 = self.tableWidget_material_data.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Poisson ratio", None))
        ___qtablewidgetitem5 = self.tableWidget_material_data.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Thermal expansion coefficient [1/K]", None))
        ___qtablewidgetitem6 = self.tableWidget_material_data.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Color", None))
#if QT_CONFIG(tooltip)
        self.pushButton_remove_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Remove selected row</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove_column.setText(QCoreApplication.translate("Form", u"-", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Add row</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_column.setText(QCoreApplication.translate("Form", u"+", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_library.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Reset to default material library</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_library.setText(QCoreApplication.translate("Form", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_duplicate.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Duplicate the selected fluid</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_duplicate.setText("")
    # retranslateUi



class MaterialInputWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - pushButton_attribute: QPushButton
                            - pushButton_exit: QPushButton
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - tableWidget_material_data: QTableWidget
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_remove_column: QPushButton
                                        - pushButton_add_column: QPushButton
                                        - frame_7: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_reset_library: QPushButton
                                        - pushButton_duplicate: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
