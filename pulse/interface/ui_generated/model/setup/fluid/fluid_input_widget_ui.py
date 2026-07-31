# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fluid_input_widget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(696, 472)
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
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
        self.tableWidget_fluid_data = QTableWidget(self.frame_2)
        if (self.tableWidget_fluid_data.rowCount() < 14):
            self.tableWidget_fluid_data.setRowCount(14)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(12, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_fluid_data.setVerticalHeaderItem(13, __qtablewidgetitem13)
        self.tableWidget_fluid_data.setObjectName(u"tableWidget_fluid_data")
        self.tableWidget_fluid_data.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        self.tableWidget_fluid_data.setColumnCount(0)
        self.tableWidget_fluid_data.horizontalHeader().setVisible(False)
        self.tableWidget_fluid_data.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_fluid_data.verticalHeader().setVisible(True)
        self.tableWidget_fluid_data.verticalHeader().setCascadingSectionResizes(True)

        self.gridLayout_2.addWidget(self.tableWidget_fluid_data, 1, 0, 1, 1)

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
        self.pushButton_reset_library.setMinimumSize(QSize(60, 28))
        self.pushButton_reset_library.setMaximumSize(QSize(60, 28))
        self.pushButton_reset_library.setFont(font)
        self.pushButton_reset_library.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_reset_library, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.frame_7, 0, 0, 1, 1)

        self.pushButton_refprop = QPushButton(self.frame_6)
        self.pushButton_refprop.setObjectName(u"pushButton_refprop")
        self.pushButton_refprop.setMinimumSize(QSize(80, 28))
        self.pushButton_refprop.setMaximumSize(QSize(80, 28))
        self.pushButton_refprop.setFont(font)
        self.pushButton_refprop.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_refprop, 0, 2, 1, 1)

        self.pushButton_remove_column = QPushButton(self.frame_6)
        self.pushButton_remove_column.setObjectName(u"pushButton_remove_column")
        self.pushButton_remove_column.setMinimumSize(QSize(28, 28))
        self.pushButton_remove_column.setMaximumSize(QSize(28, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_remove_column.setFont(font1)
        self.pushButton_remove_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_remove_column, 0, 4, 1, 1)

        self.pushButton_add_column = QPushButton(self.frame_6)
        self.pushButton_add_column.setObjectName(u"pushButton_add_column")
        self.pushButton_add_column.setMinimumSize(QSize(28, 28))
        self.pushButton_add_column.setMaximumSize(QSize(28, 28))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(True)
        font2.setItalic(False)
        self.pushButton_add_column.setFont(font2)
        self.pushButton_add_column.setStyleSheet(u"")

        self.gridLayout_5.addWidget(self.pushButton_add_column, 0, 3, 1, 1)

        self.pushButton_duplicate = QPushButton(self.frame_6)
        self.pushButton_duplicate.setObjectName(u"pushButton_duplicate")
        self.pushButton_duplicate.setMinimumSize(QSize(28, 28))
        self.pushButton_duplicate.setMaximumSize(QSize(28, 28))
        self.pushButton_duplicate.setFont(font1)
        self.pushButton_duplicate.setStyleSheet(u"")
        icon = Icon(u":/icons/common/copy_icon.png")
        self.pushButton_duplicate.setIcon(icon)
        self.pushButton_duplicate.setIconSize(QSize(18, 18))

        self.gridLayout_5.addWidget(self.pushButton_duplicate, 0, 5, 1, 1)


        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pushButton_reset_library, self.pushButton_refprop)
        QWidget.setTabOrder(self.pushButton_refprop, self.pushButton_add_column)
        QWidget.setTabOrder(self.pushButton_add_column, self.pushButton_remove_column)
        QWidget.setTabOrder(self.pushButton_remove_column, self.tableWidget_fluid_data)
        QWidget.setTabOrder(self.tableWidget_fluid_data, self.pushButton_attribute)

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
        ___qtablewidgetitem = self.tableWidget_fluid_data.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None))
        ___qtablewidgetitem1 = self.tableWidget_fluid_data.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Identifier", None))
        ___qtablewidgetitem2 = self.tableWidget_fluid_data.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Temperature [K]", None))
        ___qtablewidgetitem3 = self.tableWidget_fluid_data.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Pressure [Pa]", None))
        ___qtablewidgetitem4 = self.tableWidget_fluid_data.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Density [kg/m\u00b3]", None))
        ___qtablewidgetitem5 = self.tableWidget_fluid_data.verticalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Speed of sound [m/s]", None))
        ___qtablewidgetitem6 = self.tableWidget_fluid_data.verticalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Isentropic exponent", None))
        ___qtablewidgetitem7 = self.tableWidget_fluid_data.verticalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"Thermal conductivity [W/mK]", None))
        ___qtablewidgetitem8 = self.tableWidget_fluid_data.verticalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"Specific heat Cp [J/kgK]", None))
        ___qtablewidgetitem9 = self.tableWidget_fluid_data.verticalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"Dynamic viscosity [Ns/m\u00b2]", None))
        ___qtablewidgetitem10 = self.tableWidget_fluid_data.verticalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"Adiabatic bulk modulus [Pa]", None))
        ___qtablewidgetitem11 = self.tableWidget_fluid_data.verticalHeaderItem(11)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Form", u"Vapor pressure [Pa]", None))
        ___qtablewidgetitem12 = self.tableWidget_fluid_data.verticalHeaderItem(12)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Form", u"Molar mass [kg/kmol]", None))
        ___qtablewidgetitem13 = self.tableWidget_fluid_data.verticalHeaderItem(13)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Form", u"Color", None))
#if QT_CONFIG(tooltip)
        self.pushButton_reset_library.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Reset to default material library</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset_library.setText(QCoreApplication.translate("Form", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_refprop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Press to open the REFPROP interface</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_refprop.setText(QCoreApplication.translate("Form", u"Refprop", None))
#if QT_CONFIG(tooltip)
        self.pushButton_remove_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Remove selected row</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_remove_column.setText(QCoreApplication.translate("Form", u"-", None))
#if QT_CONFIG(tooltip)
        self.pushButton_add_column.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:400;\">Add row</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_add_column.setText(QCoreApplication.translate("Form", u"+", None))
#if QT_CONFIG(tooltip)
        self.pushButton_duplicate.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Duplicate the selected fluid</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_duplicate.setText("")
    # retranslateUi



class FluidInputWidget_UI(QWidget, Ui_Form):
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
                            - tableWidget_fluid_data: QTableWidget
                            - frame_6: QFrame
                                - (Layout): QGridLayout
                                        - frame_7: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_reset_library: QPushButton
                                        - pushButton_refprop: QPushButton
                                        - pushButton_remove_column: QPushButton
                                        - pushButton_add_column: QPushButton
                                        - pushButton_duplicate: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
