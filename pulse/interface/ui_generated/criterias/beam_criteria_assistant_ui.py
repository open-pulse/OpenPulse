# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beam_criteria_assistant.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(500, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 600))
        Dialog.setMaximumSize(QSize(600, 600))
        Dialog.setFocusPolicy(Qt.StrongFocus)
        Dialog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.top_frame = QFrame(Dialog)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setMinimumSize(QSize(0, 48))
        self.top_frame.setMaximumSize(QSize(600, 48))
        font = QFont()
        font.setPointSize(11)
        self.top_frame.setFont(font)
        self.top_frame.setFrameShape(QFrame.Box)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.top_frame.setLineWidth(1)
        self.gridLayout_3 = QGridLayout(self.top_frame)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.top_frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(380, 30))
        self.label.setMaximumSize(QSize(1000, 40))
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.top_frame, 0, 0, 1, 1)

        self.bottom_frame = QFrame(Dialog)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setMinimumSize(QSize(0, 0))
        self.bottom_frame.setMaximumSize(QSize(600, 600))
        self.bottom_frame.setFrameShape(QFrame.Box)
        self.bottom_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.bottom_frame)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(self.bottom_frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 26))
        self.label_4.setMaximumSize(QSize(16777215, 26))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_4.setFont(font1)

        self.gridLayout_4.addWidget(self.label_4, 0, 3, 1, 1)

        self.lineEdit_beam_criteria = QLineEdit(self.frame_2)
        self.lineEdit_beam_criteria.setObjectName(u"lineEdit_beam_criteria")
        self.lineEdit_beam_criteria.setMinimumSize(QSize(80, 26))
        self.lineEdit_beam_criteria.setMaximumSize(QSize(80, 26))
        self.lineEdit_beam_criteria.setFont(font1)
        self.lineEdit_beam_criteria.setFocusPolicy(Qt.ClickFocus)
        self.lineEdit_beam_criteria.setStyleSheet(u"")
        self.lineEdit_beam_criteria.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_beam_criteria, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 26))
        self.label_2.setMaximumSize(QSize(16777215, 26))
        self.label_2.setFont(font1)

        self.gridLayout_4.addWidget(self.label_2, 1, 3, 1, 1)

        self.lineEdit_section_id = QLineEdit(self.frame_2)
        self.lineEdit_section_id.setObjectName(u"lineEdit_section_id")
        self.lineEdit_section_id.setEnabled(False)
        self.lineEdit_section_id.setMinimumSize(QSize(80, 26))
        self.lineEdit_section_id.setMaximumSize(QSize(80, 26))
        self.lineEdit_section_id.setFont(font1)
        self.lineEdit_section_id.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_section_id.setStyleSheet(u"")
        self.lineEdit_section_id.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.lineEdit_section_id, 1, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(40, 28))
        self.frame_6.setMaximumSize(QSize(40, 28))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.gridLayout_4.addWidget(self.frame_6, 0, 2, 1, 1)

        self.pushButton_more_info = QPushButton(self.frame_2)
        self.pushButton_more_info.setObjectName(u"pushButton_more_info")
        self.pushButton_more_info.setMinimumSize(QSize(40, 26))
        self.pushButton_more_info.setMaximumSize(QSize(40, 26))
        self.pushButton_more_info.setFont(font1)
        self.pushButton_more_info.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/help.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_more_info.setIcon(icon)
        self.pushButton_more_info.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.pushButton_more_info, 0, 5, 1, 1)


        self.gridLayout_8.addWidget(self.frame_2, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.bottom_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.treeWidget_sections_parameters_by_lines = QTreeWidget(self.frame_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_sections_parameters_by_lines.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_sections_parameters_by_lines.setObjectName(u"treeWidget_sections_parameters_by_lines")
        self.treeWidget_sections_parameters_by_lines.setMinimumSize(QSize(0, 100))
        self.treeWidget_sections_parameters_by_lines.setMaximumSize(QSize(550, 350))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(8)
        self.treeWidget_sections_parameters_by_lines.setFont(font2)
        self.treeWidget_sections_parameters_by_lines.setAlternatingRowColors(True)
        self.treeWidget_sections_parameters_by_lines.setIndentation(1)
        self.treeWidget_sections_parameters_by_lines.setHeaderHidden(False)
        self.treeWidget_sections_parameters_by_lines.header().setHighlightSections(False)
        self.treeWidget_sections_parameters_by_lines.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_sections_parameters_by_lines.header().setStretchLastSection(True)

        self.gridLayout_5.addWidget(self.treeWidget_sections_parameters_by_lines, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.bottom_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(9, 4, 9, 4)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 32))
        self.label_3.setMaximumSize(QSize(16777215, 32))
        self.label_3.setFont(font1)
        self.label_3.setFrameShape(QFrame.Box)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_4, 2, 0, 1, 1)

        self.frame_5 = QFrame(self.bottom_frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.treeWidget_non_beam_segments = QTreeWidget(self.frame_5)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(3, Qt.AlignCenter)
        __qtreewidgetitem1.setTextAlignment(2, Qt.AlignCenter)
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_non_beam_segments.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_non_beam_segments.setObjectName(u"treeWidget_non_beam_segments")
        self.treeWidget_non_beam_segments.setMinimumSize(QSize(0, 100))
        self.treeWidget_non_beam_segments.setMaximumSize(QSize(550, 350))
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(8)
        font3.setKerning(False)
        self.treeWidget_non_beam_segments.setFont(font3)
        self.treeWidget_non_beam_segments.setAlternatingRowColors(True)
        self.treeWidget_non_beam_segments.setIndentation(1)
        self.treeWidget_non_beam_segments.setHeaderHidden(False)
        self.treeWidget_non_beam_segments.header().setHighlightSections(False)
        self.treeWidget_non_beam_segments.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_non_beam_segments.header().setStretchLastSection(True)

        self.gridLayout_7.addWidget(self.treeWidget_non_beam_segments, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_5, 3, 0, 1, 1)


        self.gridLayout.addWidget(self.bottom_frame, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_exit = QPushButton(self.frame)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 30))
        self.pushButton_exit.setMaximumSize(QSize(100, 30))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_2.addWidget(self.pushButton_exit, 0, 0, 1, 1)

        self.pushButton_check_criteria = QPushButton(self.frame)
        self.pushButton_check_criteria.setObjectName(u"pushButton_check_criteria")
        self.pushButton_check_criteria.setMinimumSize(QSize(100, 30))
        self.pushButton_check_criteria.setMaximumSize(QSize(100, 30))
        self.pushButton_check_criteria.setFont(font1)
        self.pushButton_check_criteria.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.pushButton_check_criteria, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_beam_criteria, self.lineEdit_section_id)
        QWidget.setTabOrder(self.lineEdit_section_id, self.treeWidget_sections_parameters_by_lines)
        QWidget.setTabOrder(self.treeWidget_sections_parameters_by_lines, self.treeWidget_non_beam_segments)
        QWidget.setTabOrder(self.treeWidget_non_beam_segments, self.pushButton_more_info)
        QWidget.setTabOrder(self.pushButton_more_info, self.pushButton_check_criteria)

        self.retranslateUi(Dialog)

        self.pushButton_check_criteria.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Beam theory validity check", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("Dialog", u"Beam theory validity check assistant", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Ratio L/d:", None))
        self.lineEdit_beam_criteria.setText(QCoreApplication.translate("Dialog", u"10", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Section id:", None))
        self.lineEdit_section_id.setText("")
        self.pushButton_more_info.setText("")
        ___qtreewidgetitem = self.treeWidget_sections_parameters_by_lines.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Section parameters", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Element type", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Section ID", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_sections_parameters_by_lines.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Model section information</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Branches out-of the beam theory validity", None))
        ___qtreewidgetitem1 = self.treeWidget_non_beam_segments.headerItem()
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Dialog", u"Ratio L/d", None))
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Dialog", u"Group lines", None))
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"Section ID", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"Group ID", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_non_beam_segments.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Segments whose the L/d ratios are lower than user-defined value</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.pushButton_check_criteria.setText(QCoreApplication.translate("Dialog", u"Check criteria", None))
    # retranslateUi



class BeamCriteriaAssistant_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - top_frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
                - bottom_frame: QFrame
                    - (Layout): QGridLayout
                            - frame_2: QFrame
                                - (Layout): QGridLayout
                                        - label_4: QLabel
                                        - lineEdit_beam_criteria: QLineEdit
                                        - label_2: QLabel
                                        - lineEdit_section_id: QLineEdit
                                        - frame_6: QFrame
                                        - pushButton_more_info: QPushButton
                            - frame_3: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_sections_parameters_by_lines: QTreeWidget
                            - frame_4: QFrame
                                - (Layout): QGridLayout
                                        - label_3: QLabel
                            - frame_5: QFrame
                                - (Layout): QGridLayout
                                        - treeWidget_non_beam_segments: QTreeWidget
                - frame: QFrame
                    - (Layout): QGridLayout
                            - pushButton_exit: QPushButton
                            - pushButton_check_criteria: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
