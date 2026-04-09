# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_data_to_compare.ui'
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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(540, 580)
        Dialog.setMinimumSize(QSize(540, 580))
        Dialog.setMaximumSize(QSize(540, 580))
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setSizeIncrement(QSize(0, 0))
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(452, 30))
        self.label.setMaximumSize(QSize(452, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_lower = QFrame(Dialog)
        self.frame_lower.setObjectName(u"frame_lower")
        self.frame_lower.setFrameShape(QFrame.Box)
        self.frame_lower.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_lower)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.frame_main = QFrame(self.frame_lower)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_main)
        self.gridLayout_14.setSpacing(8)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(8, 8, 8, 8)
        self.frame_skiprows_reset = QFrame(self.frame_main)
        self.frame_skiprows_reset.setObjectName(u"frame_skiprows_reset")
        self.frame_skiprows_reset.setMaximumSize(QSize(16777215, 40))
        self.frame_skiprows_reset.setFrameShape(QFrame.NoFrame)
        self.frame_skiprows_reset.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_skiprows_reset)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(6)
        self.gridLayout_12.setVerticalSpacing(2)
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.frame_13 = QFrame(self.frame_skiprows_reset)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_13)
        self.gridLayout_6.setSpacing(2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.pushButton_reset_imported_data = QPushButton(self.frame_13)
        self.pushButton_reset_imported_data.setObjectName(u"pushButton_reset_imported_data")
        self.pushButton_reset_imported_data.setMinimumSize(QSize(72, 28))
        self.pushButton_reset_imported_data.setMaximumSize(QSize(72, 28))
        self.pushButton_reset_imported_data.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_reset_imported_data.setFont(font1)
        self.pushButton_reset_imported_data.setStyleSheet(u"")
        self.pushButton_reset_imported_data.setIconSize(QSize(20, 20))

        self.gridLayout_6.addWidget(self.pushButton_reset_imported_data, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.frame_13, 0, 4, 1, 1)

        self.checkBox_skiprows = QCheckBox(self.frame_skiprows_reset)
        self.checkBox_skiprows.setObjectName(u"checkBox_skiprows")
        self.checkBox_skiprows.setMinimumSize(QSize(25, 28))
        self.checkBox_skiprows.setMaximumSize(QSize(25, 28))
        self.checkBox_skiprows.setLayoutDirection(Qt.RightToLeft)
        self.checkBox_skiprows.setTristate(False)

        self.gridLayout_12.addWidget(self.checkBox_skiprows, 0, 1, 1, 1)

        self.label_14 = QLabel(self.frame_skiprows_reset)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(160, 28))
        self.label_14.setMaximumSize(QSize(180, 28))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_14, 0, 2, 1, 1)

        self.spinBox_skiprows = QSpinBox(self.frame_skiprows_reset)
        self.spinBox_skiprows.setObjectName(u"spinBox_skiprows")
        self.spinBox_skiprows.setMinimumSize(QSize(0, 28))
        self.spinBox_skiprows.setMaximumSize(QSize(60, 28))
        font2 = QFont()
        font2.setPointSize(10)
        self.spinBox_skiprows.setFont(font2)
        self.spinBox_skiprows.setAlignment(Qt.AlignCenter)
        self.spinBox_skiprows.setMaximum(10)

        self.gridLayout_12.addWidget(self.spinBox_skiprows, 0, 3, 1, 1)

        self.frame_14 = QFrame(self.frame_skiprows_reset)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)

        self.gridLayout_12.addWidget(self.frame_14, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_skiprows_reset, 1, 0, 1, 1)

        self.frame_spreadsheet_files = QFrame(self.frame_main)
        self.frame_spreadsheet_files.setObjectName(u"frame_spreadsheet_files")
        self.frame_spreadsheet_files.setFrameShape(QFrame.NoFrame)
        self.frame_spreadsheet_files.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_spreadsheet_files)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(2, 2, 2, 2)
        self.treeWidget_import_sheet_files = QTreeWidget(self.frame_spreadsheet_files)
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setFont(2, font3)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font3)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font3)
        self.treeWidget_import_sheet_files.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_import_sheet_files.setObjectName(u"treeWidget_import_sheet_files")
        self.treeWidget_import_sheet_files.setMinimumSize(QSize(410, 40))
        self.treeWidget_import_sheet_files.setMaximumSize(QSize(500, 200))
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(8)
        font4.setItalic(False)
        self.treeWidget_import_sheet_files.setFont(font4)
        self.treeWidget_import_sheet_files.setAlternatingRowColors(True)
        self.treeWidget_import_sheet_files.setIndentation(0)

        self.gridLayout_5.addWidget(self.treeWidget_import_sheet_files, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_spreadsheet_files, 3, 0, 1, 1)

        self.frame_text_files = QFrame(self.frame_main)
        self.frame_text_files.setObjectName(u"frame_text_files")
        self.frame_text_files.setFrameShape(QFrame.NoFrame)
        self.frame_text_files.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_text_files)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.treeWidget_import_text_files = QTreeWidget(self.frame_text_files)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(1, font3)
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(0, font3)
        self.treeWidget_import_text_files.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_import_text_files.setObjectName(u"treeWidget_import_text_files")
        self.treeWidget_import_text_files.setMinimumSize(QSize(410, 40))
        self.treeWidget_import_text_files.setMaximumSize(QSize(500, 200))
        self.treeWidget_import_text_files.setFont(font4)
        self.treeWidget_import_text_files.setAlternatingRowColors(True)
        self.treeWidget_import_text_files.setIndentation(0)

        self.gridLayout.addWidget(self.treeWidget_import_text_files, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_text_files, 2, 0, 1, 1)

        self.frame_get_path = QFrame(self.frame_main)
        self.frame_get_path.setObjectName(u"frame_get_path")
        self.frame_get_path.setMaximumSize(QSize(16777215, 48))
        self.frame_get_path.setFrameShape(QFrame.NoFrame)
        self.frame_get_path.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_get_path)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(6)
        self.gridLayout_11.setVerticalSpacing(2)
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_11 = QLabel(self.frame_get_path)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(48, 30))
        self.label_11.setMaximumSize(QSize(48, 30))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_11, 0, 0, 1, 1)

        self.lineEdit_import_results_path = QLineEdit(self.frame_get_path)
        self.lineEdit_import_results_path.setObjectName(u"lineEdit_import_results_path")
        self.lineEdit_import_results_path.setEnabled(False)
        self.lineEdit_import_results_path.setMinimumSize(QSize(240, 30))
        self.lineEdit_import_results_path.setMaximumSize(QSize(500, 30))
        font5 = QFont()
        font5.setPointSize(8)
        font5.setBold(False)
        font5.setItalic(False)
        self.lineEdit_import_results_path.setFont(font5)
        self.lineEdit_import_results_path.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_import_results_path.setStyleSheet(u"")
        self.lineEdit_import_results_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.lineEdit_import_results_path, 0, 1, 1, 1)

        self.pushButton_search_file_to_import = QPushButton(self.frame_get_path)
        self.pushButton_search_file_to_import.setObjectName(u"pushButton_search_file_to_import")
        self.pushButton_search_file_to_import.setMinimumSize(QSize(40, 30))
        self.pushButton_search_file_to_import.setMaximumSize(QSize(40, 30))
        self.pushButton_search_file_to_import.setSizeIncrement(QSize(0, 0))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(11)
        font6.setBold(True)
        font6.setItalic(False)
        self.pushButton_search_file_to_import.setFont(font6)
        self.pushButton_search_file_to_import.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/import.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_search_file_to_import.setIcon(icon)
        self.pushButton_search_file_to_import.setIconSize(QSize(20, 20))

        self.gridLayout_11.addWidget(self.pushButton_search_file_to_import, 0, 2, 1, 1)

        self.frame_32 = QFrame(self.frame_get_path)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Raised)

        self.gridLayout_11.addWidget(self.frame_32, 0, 3, 1, 1)


        self.gridLayout_14.addWidget(self.frame_get_path, 0, 0, 1, 1)

        self.frame_add_imported_data = QFrame(self.frame_main)
        self.frame_add_imported_data.setObjectName(u"frame_add_imported_data")
        self.frame_add_imported_data.setFrameShape(QFrame.NoFrame)
        self.frame_add_imported_data.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_add_imported_data)
        self.gridLayout_7.setSpacing(2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.pushButton_add_imported_data_to_plot = QPushButton(self.frame_add_imported_data)
        self.pushButton_add_imported_data_to_plot.setObjectName(u"pushButton_add_imported_data_to_plot")
        self.pushButton_add_imported_data_to_plot.setMinimumSize(QSize(180, 30))
        self.pushButton_add_imported_data_to_plot.setMaximumSize(QSize(180, 30))
        self.pushButton_add_imported_data_to_plot.setSizeIncrement(QSize(0, 0))
        self.pushButton_add_imported_data_to_plot.setFont(font1)
        self.pushButton_add_imported_data_to_plot.setStyleSheet(u"")
        self.pushButton_add_imported_data_to_plot.setIconSize(QSize(20, 20))
        self.pushButton_add_imported_data_to_plot.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_add_imported_data_to_plot, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_add_imported_data)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(180, 30))
        self.pushButton_exit.setMaximumSize(QSize(180, 30))
        self.pushButton_exit.setSizeIncrement(QSize(0, 0))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setIconSize(QSize(20, 20))
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_7.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_14.addWidget(self.frame_add_imported_data, 4, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_main, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_lower, 1, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_import_results_path, self.pushButton_search_file_to_import)
        QWidget.setTabOrder(self.pushButton_search_file_to_import, self.checkBox_skiprows)
        QWidget.setTabOrder(self.checkBox_skiprows, self.spinBox_skiprows)
        QWidget.setTabOrder(self.spinBox_skiprows, self.pushButton_reset_imported_data)
        QWidget.setTabOrder(self.pushButton_reset_imported_data, self.treeWidget_import_text_files)
        QWidget.setTabOrder(self.treeWidget_import_text_files, self.treeWidget_import_sheet_files)
        QWidget.setTabOrder(self.treeWidget_import_sheet_files, self.pushButton_add_imported_data_to_plot)

        self.retranslateUi(Dialog)

        self.pushButton_add_imported_data_to_plot.setDefault(True)
        self.pushButton_exit.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Import data to compare", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Import data to compare", None))
        self.pushButton_reset_imported_data.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.checkBox_skiprows.setText("")
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Header rows to skip:", None))
        ___qtreewidgetitem = self.treeWidget_import_sheet_files.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Add to plot", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Sheetname", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Filename", None))
        ___qtreewidgetitem1 = self.treeWidget_import_text_files.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"Add to plot", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Filename", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Path:", None))
        self.pushButton_search_file_to_import.setText("")
        self.pushButton_add_imported_data_to_plot.setText(QCoreApplication.translate("Dialog", u"Add imported data", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi



class ImportDataToCompare_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - frame_lower: QFrame
                    - (Layout): QGridLayout
                            - frame_main: QFrame
                                - (Layout): QGridLayout
                                        - frame_skiprows_reset: QFrame
                                            - (Layout): QGridLayout
                                                    - frame_13: QFrame
                                                        - (Layout): QGridLayout
                                                                - pushButton_reset_imported_data: QPushButton
                                                    - checkBox_skiprows: QCheckBox
                                                    - label_14: QLabel
                                                    - spinBox_skiprows: QSpinBox
                                                    - frame_14: QFrame
                                        - frame_spreadsheet_files: QFrame
                                            - (Layout): QGridLayout
                                                    - treeWidget_import_sheet_files: QTreeWidget
                                        - frame_text_files: QFrame
                                            - (Layout): QGridLayout
                                                    - treeWidget_import_text_files: QTreeWidget
                                        - frame_get_path: QFrame
                                            - (Layout): QGridLayout
                                                    - label_11: QLabel
                                                    - lineEdit_import_results_path: QLineEdit
                                                    - pushButton_search_file_to_import: QPushButton
                                                    - frame_32: QFrame
                                        - frame_add_imported_data: QFrame
                                            - (Layout): QGridLayout
                                                    - pushButton_add_imported_data_to_plot: QPushButton
                                                    - pushButton_exit: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
