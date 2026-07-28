# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'perforated_plate_input.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

from pulse.interface.formatters.icons import Icon

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModality.WindowModal)
        Dialog.resize(480, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(480, 520))
        Dialog.setMaximumSize(QSize(480, 600))
        Dialog.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        icon = Icon(u"../../../../../../../../Olavo/.designer/temp/Downloads/load - Copia.png")
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(391, 395))
        self.frame_2.setMaximumSize(QSize(1000, 1000))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.frame_selection = QFrame(self.frame_2)
        self.frame_selection.setObjectName(u"frame_selection")
        self.frame_selection.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_selection.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame_selection)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_selection = QLabel(self.frame_selection)
        self.label_selection.setObjectName(u"label_selection")
        self.label_selection.setMinimumSize(QSize(0, 26))
        self.label_selection.setMaximumSize(QSize(16777215, 26))
        self.label_selection.setSizeIncrement(QSize(0, 30))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_selection.setFont(font)
        self.label_selection.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_selection, 0, 1, 1, 1)

        self.lineEdit_element_id = QLineEdit(self.frame_selection)
        self.lineEdit_element_id.setObjectName(u"lineEdit_element_id")
        self.lineEdit_element_id.setMinimumSize(QSize(120, 26))
        self.lineEdit_element_id.setMaximumSize(QSize(120, 26))
        self.lineEdit_element_id.setFont(font)
        self.lineEdit_element_id.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineEdit_element_id.setStyleSheet(u"")
        self.lineEdit_element_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_13.addWidget(self.lineEdit_element_id, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer, 0, 4, 1, 1)


        self.gridLayout_14.addWidget(self.frame_selection, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setEnabled(True)
        self.tabWidget_main.setFont(font)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.gridLayout_19 = QGridLayout(self.tab_setup)
        self.gridLayout_19.setSpacing(4)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(4, 4, 4, 4)
        self.tabWidget_setup = QTabWidget(self.tab_setup)
        self.tabWidget_setup.setObjectName(u"tabWidget_setup")
        self.tabWidget_setup.setFont(font)
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.gridLayout_25 = QGridLayout(self.tab_main)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setHorizontalSpacing(4)
        self.gridLayout_25.setVerticalSpacing(0)
        self.gridLayout_25.setContentsMargins(4, 4, 4, 4)
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_25.addItem(self.verticalSpacer_5, 0, 0, 1, 1)

        self.frame_setup_main = QFrame(self.tab_main)
        self.frame_setup_main.setObjectName(u"frame_setup_main")
        self.frame_setup_main.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_setup_main.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_setup_main)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_area_porosity = QLineEdit(self.frame_setup_main)
        self.lineEdit_area_porosity.setObjectName(u"lineEdit_area_porosity")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_area_porosity.sizePolicy().hasHeightForWidth())
        self.lineEdit_area_porosity.setSizePolicy(sizePolicy1)
        self.lineEdit_area_porosity.setMinimumSize(QSize(100, 26))
        self.lineEdit_area_porosity.setMaximumSize(QSize(120, 26))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(250, 250, 250, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
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
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_area_porosity.setPalette(palette)
        self.lineEdit_area_porosity.setFont(font)
        self.lineEdit_area_porosity.setStyleSheet(u"")
        self.lineEdit_area_porosity.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_area_porosity, 4, 2, 1, 1)

        self.lineEdit_discharge_coefficient = QLineEdit(self.frame_setup_main)
        self.lineEdit_discharge_coefficient.setObjectName(u"lineEdit_discharge_coefficient")
        sizePolicy1.setHeightForWidth(self.lineEdit_discharge_coefficient.sizePolicy().hasHeightForWidth())
        self.lineEdit_discharge_coefficient.setSizePolicy(sizePolicy1)
        self.lineEdit_discharge_coefficient.setMinimumSize(QSize(100, 26))
        self.lineEdit_discharge_coefficient.setMaximumSize(QSize(120, 26))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_discharge_coefficient.setPalette(palette1)
        self.lineEdit_discharge_coefficient.setFont(font)
        self.lineEdit_discharge_coefficient.setStyleSheet(u"")
        self.lineEdit_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_discharge_coefficient, 5, 2, 1, 1)

        self.label_hole_diameter = QLabel(self.frame_setup_main)
        self.label_hole_diameter.setObjectName(u"label_hole_diameter")
        sizePolicy.setHeightForWidth(self.label_hole_diameter.sizePolicy().hasHeightForWidth())
        self.label_hole_diameter.setSizePolicy(sizePolicy)
        self.label_hole_diameter.setMinimumSize(QSize(140, 26))
        self.label_hole_diameter.setMaximumSize(QSize(140, 26))
        self.label_hole_diameter.setFont(font)
        self.label_hole_diameter.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_hole_diameter, 2, 1, 1, 1)

        self.label_area_porosity = QLabel(self.frame_setup_main)
        self.label_area_porosity.setObjectName(u"label_area_porosity")
        sizePolicy.setHeightForWidth(self.label_area_porosity.sizePolicy().hasHeightForWidth())
        self.label_area_porosity.setSizePolicy(sizePolicy)
        self.label_area_porosity.setMinimumSize(QSize(140, 26))
        self.label_area_porosity.setMaximumSize(QSize(140, 26))
        self.label_area_porosity.setFont(font)
        self.label_area_porosity.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_area_porosity, 4, 1, 1, 1)

        self.label_plate_thickness = QLabel(self.frame_setup_main)
        self.label_plate_thickness.setObjectName(u"label_plate_thickness")
        sizePolicy.setHeightForWidth(self.label_plate_thickness.sizePolicy().hasHeightForWidth())
        self.label_plate_thickness.setSizePolicy(sizePolicy)
        self.label_plate_thickness.setMinimumSize(QSize(140, 26))
        self.label_plate_thickness.setMaximumSize(QSize(140, 26))
        self.label_plate_thickness.setFont(font)
        self.label_plate_thickness.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_plate_thickness, 3, 1, 1, 1)

        self.label_discharge = QLabel(self.frame_setup_main)
        self.label_discharge.setObjectName(u"label_discharge")
        sizePolicy.setHeightForWidth(self.label_discharge.sizePolicy().hasHeightForWidth())
        self.label_discharge.setSizePolicy(sizePolicy)
        self.label_discharge.setMinimumSize(QSize(140, 26))
        self.label_discharge.setMaximumSize(QSize(140, 26))
        self.label_discharge.setFont(font)
        self.label_discharge.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_discharge, 5, 1, 1, 1)

        self.lineEdit_hole_diameter = QLineEdit(self.frame_setup_main)
        self.lineEdit_hole_diameter.setObjectName(u"lineEdit_hole_diameter")
        sizePolicy1.setHeightForWidth(self.lineEdit_hole_diameter.sizePolicy().hasHeightForWidth())
        self.lineEdit_hole_diameter.setSizePolicy(sizePolicy1)
        self.lineEdit_hole_diameter.setMinimumSize(QSize(100, 26))
        self.lineEdit_hole_diameter.setMaximumSize(QSize(120, 26))
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_hole_diameter.setPalette(palette2)
        self.lineEdit_hole_diameter.setFont(font)
        self.lineEdit_hole_diameter.setStyleSheet(u"")
        self.lineEdit_hole_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_hole_diameter, 2, 2, 1, 1)

        self.label_14 = QLabel(self.frame_setup_main)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QSize(35, 26))
        self.label_14.setMaximumSize(QSize(35, 26))
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_14, 3, 3, 1, 1)

        self.label_15 = QLabel(self.frame_setup_main)
        self.label_15.setObjectName(u"label_15")
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QSize(35, 26))
        self.label_15.setMaximumSize(QSize(35, 26))
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_15, 4, 3, 1, 1)

        self.label_16 = QLabel(self.frame_setup_main)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QSize(35, 26))
        self.label_16.setMaximumSize(QSize(35, 26))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_16, 5, 3, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_12, 2, 0, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_13, 2, 4, 1, 1)

        self.lineEdit_plate_thickness = QLineEdit(self.frame_setup_main)
        self.lineEdit_plate_thickness.setObjectName(u"lineEdit_plate_thickness")
        sizePolicy1.setHeightForWidth(self.lineEdit_plate_thickness.sizePolicy().hasHeightForWidth())
        self.lineEdit_plate_thickness.setSizePolicy(sizePolicy1)
        self.lineEdit_plate_thickness.setMinimumSize(QSize(100, 26))
        self.lineEdit_plate_thickness.setMaximumSize(QSize(120, 26))
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_plate_thickness.setPalette(palette3)
        self.lineEdit_plate_thickness.setFont(font)
        self.lineEdit_plate_thickness.setStyleSheet(u"")
        self.lineEdit_plate_thickness.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_plate_thickness, 3, 2, 1, 1)

        self.label_17 = QLabel(self.frame_setup_main)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QSize(35, 26))
        self.label_17.setMaximumSize(QSize(35, 26))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_17, 2, 3, 1, 1)

        self.frame_single_hole = QFrame(self.frame_setup_main)
        self.frame_single_hole.setObjectName(u"frame_single_hole")
        self.frame_single_hole.setMinimumSize(QSize(100, 26))
        self.frame_single_hole.setMaximumSize(QSize(120, 26))
        self.frame_single_hole.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_single_hole.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_single_hole)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.checkBox_single_hole = QCheckBox(self.frame_single_hole)
        self.checkBox_single_hole.setObjectName(u"checkBox_single_hole")
        self.checkBox_single_hole.setEnabled(True)
        self.checkBox_single_hole.setMinimumSize(QSize(0, 20))
        self.checkBox_single_hole.setMaximumSize(QSize(16777215, 26))
        self.checkBox_single_hole.setFont(font)
        self.checkBox_single_hole.setChecked(False)

        self.gridLayout_15.addWidget(self.checkBox_single_hole, 0, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_15, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.frame_single_hole, 1, 2, 1, 1)

        self.comboBox_perforated_plate_model = QComboBox(self.frame_setup_main)
        self.comboBox_perforated_plate_model.addItem("")
        self.comboBox_perforated_plate_model.addItem("")
        self.comboBox_perforated_plate_model.addItem("")
        self.comboBox_perforated_plate_model.setObjectName(u"comboBox_perforated_plate_model")
        self.comboBox_perforated_plate_model.setMinimumSize(QSize(100, 26))
        self.comboBox_perforated_plate_model.setMaximumSize(QSize(120, 26))
        self.comboBox_perforated_plate_model.setFont(font)

        self.gridLayout.addWidget(self.comboBox_perforated_plate_model, 0, 2, 1, 1)

        self.label_HoleDiameter_2 = QLabel(self.frame_setup_main)
        self.label_HoleDiameter_2.setObjectName(u"label_HoleDiameter_2")
        sizePolicy.setHeightForWidth(self.label_HoleDiameter_2.sizePolicy().hasHeightForWidth())
        self.label_HoleDiameter_2.setSizePolicy(sizePolicy)
        self.label_HoleDiameter_2.setMinimumSize(QSize(140, 26))
        self.label_HoleDiameter_2.setMaximumSize(QSize(140, 26))
        self.label_HoleDiameter_2.setFont(font)
        self.label_HoleDiameter_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_HoleDiameter_2, 0, 1, 1, 1)


        self.gridLayout_25.addWidget(self.frame_setup_main, 1, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_25.addItem(self.verticalSpacer_6, 2, 0, 1, 1)

        self.tabWidget_setup.addTab(self.tab_main, "")
        self.tab_advanced = QWidget()
        self.tab_advanced.setObjectName(u"tab_advanced")
        self.gridLayout_18 = QGridLayout(self.tab_advanced)
        self.gridLayout_18.setSpacing(4)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(4, 4, 4, 4)
        self.scrollArea = QScrollArea(self.tab_advanced)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 422, 262))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_14 = QFrame(self.scrollAreaWidgetContents)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMaximumSize(QSize(16777215, 26))
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_14)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setHorizontalSpacing(0)
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_21.addItem(self.horizontalSpacer_6, 0, 1, 1, 1)

        self.checkBox_dimensionless_impedance = QCheckBox(self.frame_14)
        self.checkBox_dimensionless_impedance.setObjectName(u"checkBox_dimensionless_impedance")
        self.checkBox_dimensionless_impedance.setEnabled(True)
        self.checkBox_dimensionless_impedance.setFont(font)
        self.checkBox_dimensionless_impedance.setChecked(False)

        self.gridLayout_21.addWidget(self.checkBox_dimensionless_impedance, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_14, 1, 0, 1, 1)

        self.frame_11 = QFrame(self.scrollAreaWidgetContents)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setStyleSheet(u"")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_11)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setVerticalSpacing(4)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.label_27 = QLabel(self.frame_11)
        self.label_27.setObjectName(u"label_27")
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QSize(20, 26))
        self.label_27.setMaximumSize(QSize(32, 26))
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_27, 1, 4, 1, 1)

        self.lineEdit_nonlin_discharge = QLineEdit(self.frame_11)
        self.lineEdit_nonlin_discharge.setObjectName(u"lineEdit_nonlin_discharge")
        self.lineEdit_nonlin_discharge.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.lineEdit_nonlin_discharge.sizePolicy().hasHeightForWidth())
        self.lineEdit_nonlin_discharge.setSizePolicy(sizePolicy1)
        self.lineEdit_nonlin_discharge.setMinimumSize(QSize(80, 26))
        self.lineEdit_nonlin_discharge.setMaximumSize(QSize(80, 26))
        palette4 = QPalette()
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_nonlin_discharge.setPalette(palette4)
        self.lineEdit_nonlin_discharge.setStyleSheet(u"")
        self.lineEdit_nonlin_discharge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_nonlin_discharge, 0, 3, 1, 1)

        self.lineEdit_correction_factor = QLineEdit(self.frame_11)
        self.lineEdit_correction_factor.setObjectName(u"lineEdit_correction_factor")
        self.lineEdit_correction_factor.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.lineEdit_correction_factor.sizePolicy().hasHeightForWidth())
        self.lineEdit_correction_factor.setSizePolicy(sizePolicy1)
        self.lineEdit_correction_factor.setMinimumSize(QSize(80, 26))
        self.lineEdit_correction_factor.setMaximumSize(QSize(80, 26))
        palette5 = QPalette()
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_correction_factor.setPalette(palette5)
        self.lineEdit_correction_factor.setStyleSheet(u"")
        self.lineEdit_correction_factor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_correction_factor, 1, 3, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_20, 0, 6, 1, 1)

        self.lineEdit_bias_flow_coefficient = QLineEdit(self.frame_11)
        self.lineEdit_bias_flow_coefficient.setObjectName(u"lineEdit_bias_flow_coefficient")
        self.lineEdit_bias_flow_coefficient.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.lineEdit_bias_flow_coefficient.sizePolicy().hasHeightForWidth())
        self.lineEdit_bias_flow_coefficient.setSizePolicy(sizePolicy1)
        self.lineEdit_bias_flow_coefficient.setMinimumSize(QSize(80, 26))
        self.lineEdit_bias_flow_coefficient.setMaximumSize(QSize(80, 26))
        palette6 = QPalette()
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush2)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush3)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush2)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush2)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush3)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush3)
        self.lineEdit_bias_flow_coefficient.setPalette(palette6)
        self.lineEdit_bias_flow_coefficient.setStyleSheet(u"")
        self.lineEdit_bias_flow_coefficient.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.lineEdit_bias_flow_coefficient, 2, 3, 1, 1)

        self.label_21 = QLabel(self.frame_11)
        self.label_21.setObjectName(u"label_21")
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QSize(20, 26))
        self.label_21.setMaximumSize(QSize(32, 26))
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_21, 0, 4, 1, 1)

        self.label_28 = QLabel(self.frame_11)
        self.label_28.setObjectName(u"label_28")
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QSize(20, 26))
        self.label_28.setMaximumSize(QSize(32, 26))
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_28, 2, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.checkBox_nonlinear_discharge_coefficient = QCheckBox(self.frame_11)
        self.checkBox_nonlinear_discharge_coefficient.setObjectName(u"checkBox_nonlinear_discharge_coefficient")

        self.gridLayout_5.addWidget(self.checkBox_nonlinear_discharge_coefficient, 0, 5, 1, 1)

        self.checkBox_bias_flow_coefficient = QCheckBox(self.frame_11)
        self.checkBox_bias_flow_coefficient.setObjectName(u"checkBox_bias_flow_coefficient")

        self.gridLayout_5.addWidget(self.checkBox_bias_flow_coefficient, 2, 5, 1, 1)

        self.label_bias_flow_coefficient = QLabel(self.frame_11)
        self.label_bias_flow_coefficient.setObjectName(u"label_bias_flow_coefficient")
        self.label_bias_flow_coefficient.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_bias_flow_coefficient, 2, 2, 1, 1)

        self.label_correction_factor = QLabel(self.frame_11)
        self.label_correction_factor.setObjectName(u"label_correction_factor")
        self.label_correction_factor.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_correction_factor.sizePolicy().hasHeightForWidth())
        self.label_correction_factor.setSizePolicy(sizePolicy)
        self.label_correction_factor.setMinimumSize(QSize(200, 26))
        self.label_correction_factor.setMaximumSize(QSize(200, 26))
        self.label_correction_factor.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_correction_factor, 1, 2, 1, 1)

        self.label_non_linear_discharge_coefficient = QLabel(self.frame_11)
        self.label_non_linear_discharge_coefficient.setObjectName(u"label_non_linear_discharge_coefficient")
        self.label_non_linear_discharge_coefficient.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.label_non_linear_discharge_coefficient, 0, 2, 1, 1)


        self.gridLayout_3.addWidget(self.frame_11, 0, 0, 1, 1)

        self.tabWidget_dimensionless = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_dimensionless.setObjectName(u"tabWidget_dimensionless")
        self.tabWidget_dimensionless.setEnabled(True)
        self.tabWidget_dimensionless.setMaximumSize(QSize(16777215, 120))
        self.tabWidget_dimensionless.setFont(font)
        self.tab_single_value = QWidget()
        self.tab_single_value.setObjectName(u"tab_single_value")
        self.gridLayout_9 = QGridLayout(self.tab_single_value)
        self.gridLayout_9.setSpacing(4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(4, 4, 4, 4)
        self.label_12 = QLabel(self.tab_single_value)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(68, 26))
        self.label_12.setMaximumSize(QSize(68, 26))
        self.label_12.setFrameShape(QFrame.Shape.NoFrame)
        self.label_12.setFrameShadow(QFrame.Shadow.Raised)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_12, 1, 2, 1, 1)

        self.label_10 = QLabel(self.tab_single_value)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(68, 26))
        self.label_10.setMaximumSize(QSize(68, 26))
        self.label_10.setFrameShape(QFrame.Shape.NoFrame)
        self.label_10.setFrameShadow(QFrame.Shadow.Raised)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.label_10, 1, 3, 1, 1)

        self.label_dimensionless_impedance = QLabel(self.tab_single_value)
        self.label_dimensionless_impedance.setObjectName(u"label_dimensionless_impedance")
        self.label_dimensionless_impedance.setEnabled(True)
        self.label_dimensionless_impedance.setMinimumSize(QSize(160, 26))
        self.label_dimensionless_impedance.setMaximumSize(QSize(160, 26))
        self.label_dimensionless_impedance.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_dimensionless_impedance, 2, 1, 1, 1)

        self.lineEdit_impedance_imag = QLineEdit(self.tab_single_value)
        self.lineEdit_impedance_imag.setObjectName(u"lineEdit_impedance_imag")
        self.lineEdit_impedance_imag.setMinimumSize(QSize(68, 26))
        self.lineEdit_impedance_imag.setMaximumSize(QSize(68, 26))
        self.lineEdit_impedance_imag.setStyleSheet(u"")
        self.lineEdit_impedance_imag.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_impedance_imag, 2, 3, 1, 1)

        self.lineEdit_impedance_real = QLineEdit(self.tab_single_value)
        self.lineEdit_impedance_real.setObjectName(u"lineEdit_impedance_real")
        self.lineEdit_impedance_real.setMinimumSize(QSize(68, 26))
        self.lineEdit_impedance_real.setMaximumSize(QSize(68, 26))
        self.lineEdit_impedance_real.setStyleSheet(u"")
        self.lineEdit_impedance_real.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_9.addWidget(self.lineEdit_impedance_real, 2, 2, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_7, 2, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer, 3, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_2, 0, 2, 1, 1)

        self.tabWidget_dimensionless.addTab(self.tab_single_value, "")
        self.tab_table_of_values = QWidget()
        self.tab_table_of_values.setObjectName(u"tab_table_of_values")
        self.gridLayout_22 = QGridLayout(self.tab_table_of_values)
        self.gridLayout_22.setSpacing(4)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(4, 4, 4, 4)
        self.frame_skip = QFrame(self.tab_table_of_values)
        self.frame_skip.setObjectName(u"frame_skip")
        self.frame_skip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_skip.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_23 = QGridLayout(self.frame_skip)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setHorizontalSpacing(8)
        self.gridLayout_23.setContentsMargins(4, 4, 4, 4)
        self.label_rows_to_skip = QLabel(self.frame_skip)
        self.label_rows_to_skip.setObjectName(u"label_rows_to_skip")
        self.label_rows_to_skip.setMinimumSize(QSize(132, 26))
        self.label_rows_to_skip.setMaximumSize(QSize(132, 26))
        self.label_rows_to_skip.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_23.addWidget(self.label_rows_to_skip, 0, 1, 1, 1)

        self.spinBox_skip_rows = QSpinBox(self.frame_skip)
        self.spinBox_skip_rows.setObjectName(u"spinBox_skip_rows")
        self.spinBox_skip_rows.setMinimumSize(QSize(60, 26))
        self.spinBox_skip_rows.setMaximumSize(QSize(60, 26))
        self.spinBox_skip_rows.setStyleSheet(u"")
        self.spinBox_skip_rows.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_skip_rows.setMaximum(10)

        self.gridLayout_23.addWidget(self.spinBox_skip_rows, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_19, 0, 3, 1, 1)


        self.gridLayout_22.addWidget(self.frame_skip, 2, 0, 1, 2)

        self.frame_17 = QFrame(self.tab_table_of_values)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_31 = QGridLayout(self.frame_17)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setHorizontalSpacing(6)
        self.gridLayout_31.setVerticalSpacing(4)
        self.gridLayout_31.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_load_table_path = QLineEdit(self.frame_17)
        self.lineEdit_load_table_path.setObjectName(u"lineEdit_load_table_path")
        self.lineEdit_load_table_path.setEnabled(False)
        self.lineEdit_load_table_path.setMinimumSize(QSize(300, 26))
        self.lineEdit_load_table_path.setMaximumSize(QSize(300, 26))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(True)
        self.lineEdit_load_table_path.setFont(font1)
        self.lineEdit_load_table_path.setStyleSheet(u"")
        self.lineEdit_load_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_31.addWidget(self.lineEdit_load_table_path, 0, 1, 1, 1)

        self.pushButton_load_table = QPushButton(self.frame_17)
        self.pushButton_load_table.setObjectName(u"pushButton_load_table")
        self.pushButton_load_table.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_load_table.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table.setSizePolicy(sizePolicy2)
        self.pushButton_load_table.setMinimumSize(QSize(65, 26))
        self.pushButton_load_table.setMaximumSize(QSize(65, 26))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setKerning(False)
        self.pushButton_load_table.setFont(font2)
        self.pushButton_load_table.setStyleSheet(u"")

        self.gridLayout_31.addWidget(self.pushButton_load_table, 0, 2, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_16, 0, 0, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_17, 0, 3, 1, 1)


        self.gridLayout_22.addWidget(self.frame_17, 1, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_22.addItem(self.verticalSpacer_3, 0, 0, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_22.addItem(self.verticalSpacer_4, 3, 0, 1, 2)

        self.tabWidget_dimensionless.addTab(self.tab_table_of_values, "")

        self.gridLayout_3.addWidget(self.tabWidget_dimensionless, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_18.addWidget(self.scrollArea, 2, 1, 1, 1)

        self.tabWidget_setup.addTab(self.tab_advanced, "")

        self.gridLayout_19.addWidget(self.tabWidget_setup, 0, 0, 1, 1)

        self.frame_15 = QFrame(self.tab_setup)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(0, 48))
        self.frame_15.setMaximumSize(QSize(16777215, 48))
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_20 = QGridLayout(self.frame_15)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.pushButton_attribute = QPushButton(self.frame_15)
        self.pushButton_attribute.setObjectName(u"pushButton_attribute")
        self.pushButton_attribute.setMinimumSize(QSize(100, 28))
        self.pushButton_attribute.setMaximumSize(QSize(100, 28))
        self.pushButton_attribute.setFont(font)
        self.pushButton_attribute.setStyleSheet(u"")
        self.pushButton_attribute.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_attribute, 0, 1, 1, 1)

        self.pushButton_exit = QPushButton(self.frame_15)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setMinimumSize(QSize(100, 28))
        self.pushButton_exit.setMaximumSize(QSize(100, 28))
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet(u"")
        self.pushButton_exit.setAutoDefault(False)

        self.gridLayout_20.addWidget(self.pushButton_exit, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.frame_15, 1, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_setup, "")
        self.tab_remove = QWidget()
        self.tab_remove.setObjectName(u"tab_remove")
        self.gridLayout_30 = QGridLayout(self.tab_remove)
        self.gridLayout_30.setSpacing(4)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(4, 4, 4, 4)
        self.frame_22 = QFrame(self.tab_remove)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_29 = QGridLayout(self.frame_22)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.treeWidget_elements_info = QTreeWidget(self.frame_22)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_elements_info.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_elements_info.setObjectName(u"treeWidget_elements_info")
        self.treeWidget_elements_info.setMinimumSize(QSize(0, 0))
        self.treeWidget_elements_info.setMaximumSize(QSize(360, 500))
        self.treeWidget_elements_info.setIndentation(1)
        self.treeWidget_elements_info.setHeaderHidden(False)
        self.treeWidget_elements_info.header().setHighlightSections(False)
        self.treeWidget_elements_info.header().setProperty(u"showSortIndicator", False)
        self.treeWidget_elements_info.header().setStretchLastSection(True)

        self.gridLayout_29.addWidget(self.treeWidget_elements_info, 1, 0, 1, 1)


        self.gridLayout_30.addWidget(self.frame_22, 2, 0, 1, 1)

        self.frame_19 = QFrame(self.tab_remove)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_26 = QGridLayout(self.frame_19)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.pushButton_reset = QPushButton(self.frame_19)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(100, 28))
        self.pushButton_reset.setMaximumSize(QSize(100, 28))
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setStyleSheet(u"")
        self.pushButton_reset.setAutoDefault(False)
        self.pushButton_reset.setFlat(False)

        self.gridLayout_26.addWidget(self.pushButton_reset, 0, 1, 1, 1)

        self.pushButton_remove = QPushButton(self.frame_19)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMinimumSize(QSize(100, 28))
        self.pushButton_remove.setMaximumSize(QSize(100, 28))
        self.pushButton_remove.setFont(font)
        self.pushButton_remove.setStyleSheet(u"")
        self.pushButton_remove.setAutoDefault(False)

        self.gridLayout_26.addWidget(self.pushButton_remove, 0, 2, 1, 1)


        self.gridLayout_30.addWidget(self.frame_19, 4, 0, 1, 1)

        self.frame_3 = QFrame(self.tab_remove)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 48))
        self.frame_3.setMaximumSize(QSize(16777215, 160))
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_3)
        self.gridLayout_7.setSpacing(4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(4, 4, 4, 4)
        self.pushButton_plot_absorption_coefficient = QPushButton(self.frame_3)
        self.pushButton_plot_absorption_coefficient.setObjectName(u"pushButton_plot_absorption_coefficient")
        self.pushButton_plot_absorption_coefficient.setMinimumSize(QSize(140, 28))
        self.pushButton_plot_absorption_coefficient.setMaximumSize(QSize(140, 28))
        self.pushButton_plot_absorption_coefficient.setFont(font)
        self.pushButton_plot_absorption_coefficient.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton_plot_absorption_coefficient, 0, 1, 1, 1)

        self.pushButton_plot_impedance = QPushButton(self.frame_3)
        self.pushButton_plot_impedance.setObjectName(u"pushButton_plot_impedance")
        self.pushButton_plot_impedance.setMinimumSize(QSize(140, 28))
        self.pushButton_plot_impedance.setMaximumSize(QSize(140, 28))
        self.pushButton_plot_impedance.setFont(font)
        self.pushButton_plot_impedance.setStyleSheet(u"")

        self.gridLayout_7.addWidget(self.pushButton_plot_impedance, 0, 0, 1, 1)


        self.gridLayout_30.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_20 = QFrame(self.tab_remove)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMaximumSize(QSize(16777215, 40))
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_27 = QGridLayout(self.frame_20)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridLayout_27.setContentsMargins(6, 0, 0, 0)
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_14, 0, 2, 1, 1)

        self.checkBox_remove_valve_structural_effects = QCheckBox(self.frame_20)
        self.checkBox_remove_valve_structural_effects.setObjectName(u"checkBox_remove_valve_structural_effects")
        self.checkBox_remove_valve_structural_effects.setMinimumSize(QSize(220, 30))
        self.checkBox_remove_valve_structural_effects.setMaximumSize(QSize(280, 30))
        self.checkBox_remove_valve_structural_effects.setFont(font)
        self.checkBox_remove_valve_structural_effects.setChecked(True)

        self.gridLayout_27.addWidget(self.checkBox_remove_valve_structural_effects, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)


        self.gridLayout_30.addWidget(self.frame_20, 3, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_remove, "")

        self.gridLayout_14.addWidget(self.tabWidget_main, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 48))
        self.frame.setMaximumSize(QSize(16777215, 48))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.label.setFont(font3)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget_main, self.tabWidget_setup)
        QWidget.setTabOrder(self.tabWidget_setup, self.comboBox_perforated_plate_model)
        QWidget.setTabOrder(self.comboBox_perforated_plate_model, self.checkBox_single_hole)
        QWidget.setTabOrder(self.checkBox_single_hole, self.lineEdit_hole_diameter)
        QWidget.setTabOrder(self.lineEdit_hole_diameter, self.lineEdit_plate_thickness)
        QWidget.setTabOrder(self.lineEdit_plate_thickness, self.lineEdit_area_porosity)
        QWidget.setTabOrder(self.lineEdit_area_porosity, self.lineEdit_discharge_coefficient)
        QWidget.setTabOrder(self.lineEdit_discharge_coefficient, self.pushButton_exit)
        QWidget.setTabOrder(self.pushButton_exit, self.pushButton_attribute)
        QWidget.setTabOrder(self.pushButton_attribute, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.lineEdit_nonlin_discharge)
        QWidget.setTabOrder(self.lineEdit_nonlin_discharge, self.checkBox_nonlinear_discharge_coefficient)
        QWidget.setTabOrder(self.checkBox_nonlinear_discharge_coefficient, self.lineEdit_correction_factor)
        QWidget.setTabOrder(self.lineEdit_correction_factor, self.lineEdit_bias_flow_coefficient)
        QWidget.setTabOrder(self.lineEdit_bias_flow_coefficient, self.checkBox_bias_flow_coefficient)
        QWidget.setTabOrder(self.checkBox_bias_flow_coefficient, self.checkBox_dimensionless_impedance)
        QWidget.setTabOrder(self.checkBox_dimensionless_impedance, self.tabWidget_dimensionless)
        QWidget.setTabOrder(self.tabWidget_dimensionless, self.lineEdit_impedance_real)
        QWidget.setTabOrder(self.lineEdit_impedance_real, self.lineEdit_impedance_imag)
        QWidget.setTabOrder(self.lineEdit_impedance_imag, self.lineEdit_load_table_path)
        QWidget.setTabOrder(self.lineEdit_load_table_path, self.pushButton_load_table)
        QWidget.setTabOrder(self.pushButton_load_table, self.spinBox_skip_rows)
        QWidget.setTabOrder(self.spinBox_skip_rows, self.checkBox_remove_valve_structural_effects)
        QWidget.setTabOrder(self.checkBox_remove_valve_structural_effects, self.treeWidget_elements_info)
        QWidget.setTabOrder(self.treeWidget_elements_info, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.pushButton_remove)

        self.retranslateUi(Dialog)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_setup.setCurrentIndex(0)
        self.tabWidget_dimensionless.setCurrentIndex(0)
        self.pushButton_attribute.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add: perforated plate", None))
#if QT_CONFIG(whatsthis)
        Dialog.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label_selection.setText(QCoreApplication.translate("Dialog", u"Element IDs:", None))
        self.lineEdit_element_id.setText("")
        self.lineEdit_area_porosity.setText("")
        self.lineEdit_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_hole_diameter.setText(QCoreApplication.translate("Dialog", u"Hole diameter:", None))
        self.label_area_porosity.setText(QCoreApplication.translate("Dialog", u"Area porosity:", None))
        self.label_plate_thickness.setText(QCoreApplication.translate("Dialog", u"Plate thickness:", None))
        self.label_discharge.setText(QCoreApplication.translate("Dialog", u"Discharge coefficient:", None))
        self.lineEdit_hole_diameter.setText("")
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.lineEdit_plate_thickness.setText("")
        self.label_17.setText(QCoreApplication.translate("Dialog", u"[m]", None))
        self.checkBox_single_hole.setText(QCoreApplication.translate("Dialog", u"Single hole", None))
        self.comboBox_perforated_plate_model.setItemText(0, QCoreApplication.translate("Dialog", u" OpenPulse", None))
        self.comboBox_perforated_plate_model.setItemText(1, QCoreApplication.translate("Dialog", u" Melling", None))
        self.comboBox_perforated_plate_model.setItemText(2, QCoreApplication.translate("Dialog", u" Common pipe", None))

        self.label_HoleDiameter_2.setText(QCoreApplication.translate("Dialog", u"Perforate plate model:", None))
        self.tabWidget_setup.setTabText(self.tabWidget_setup.indexOf(self.tab_main), QCoreApplication.translate("Dialog", u"Main", None))
        self.checkBox_dimensionless_impedance.setText(QCoreApplication.translate("Dialog", u"Add dimensionless impedance", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.lineEdit_nonlin_discharge.setText(QCoreApplication.translate("Dialog", u"0.76", None))
        self.lineEdit_correction_factor.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.lineEdit_bias_flow_coefficient.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"[-]", None))
        self.checkBox_nonlinear_discharge_coefficient.setText("")
        self.checkBox_bias_flow_coefficient.setText("")
        self.label_bias_flow_coefficient.setText(QCoreApplication.translate("Dialog", u"Bias flow coefficient:", None))
        self.label_correction_factor.setText(QCoreApplication.translate("Dialog", u"Correction factor:", None))
        self.label_non_linear_discharge_coefficient.setText(QCoreApplication.translate("Dialog", u"Nonlinear discharge coefficient:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Real", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Imaginary", None))
        self.label_dimensionless_impedance.setText(QCoreApplication.translate("Dialog", u"Dimensionless impedance:", None))
        self.lineEdit_impedance_imag.setText("")
        self.lineEdit_impedance_real.setText("")
        self.tabWidget_dimensionless.setTabText(self.tabWidget_dimensionless.indexOf(self.tab_single_value), QCoreApplication.translate("Dialog", u"Single value", None))
        self.label_rows_to_skip.setText(QCoreApplication.translate("Dialog", u"Header rows to skip:", None))
        self.lineEdit_load_table_path.setText("")
        self.pushButton_load_table.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.tabWidget_dimensionless.setTabText(self.tabWidget_dimensionless.indexOf(self.tab_table_of_values), QCoreApplication.translate("Dialog", u"Import table", None))
        self.tabWidget_setup.setTabText(self.tabWidget_setup.indexOf(self.tab_advanced), QCoreApplication.translate("Dialog", u"Advanced", None))
        self.pushButton_attribute.setText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_setup), QCoreApplication.translate("Dialog", u"Setup", None))
        ___qtreewidgetitem = self.treeWidget_elements_info.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Perforated plate parameters", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"Element", None))
#if QT_CONFIG(tooltip)
        self.treeWidget_elements_info.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select a group to remove the perforated plate or press double-click to get detailed information.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.pushButton_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.pushButton_remove.setProperty(u"status", QCoreApplication.translate("Dialog", u"danger", None))
        self.pushButton_plot_absorption_coefficient.setText(QCoreApplication.translate("Dialog", u"Plot absorption coef.", None))
        self.pushButton_plot_impedance.setText(QCoreApplication.translate("Dialog", u"Plot impedance", None))
        self.checkBox_remove_valve_structural_effects.setText(QCoreApplication.translate("Dialog", u"Remove valve strucutral effects", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_remove), QCoreApplication.translate("Dialog", u"Remove", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Perforated plate setup", None))
    # retranslateUi



class PerforatedPlateInput_UI(QDialog, Ui_Dialog):
    """
    Component Hierarchy:
    - Dialog: QDialog
        - (Layout): QGridLayout
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_selection: QFrame
                                - (Layout): QGridLayout
                                        - label_selection: QLabel
                                        - lineEdit_element_id: QLineEdit
                            - tabWidget_main: QTabWidget
                                - tab_setup: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_setup: QTabWidget
                                                - tab_main: QWidget
                                                    - (Layout): QGridLayout
                                                            - frame_setup_main: QFrame
                                                                - (Layout): QGridLayout
                                                                        - lineEdit_area_porosity: QLineEdit
                                                                        - lineEdit_discharge_coefficient: QLineEdit
                                                                        - label_hole_diameter: QLabel
                                                                        - label_area_porosity: QLabel
                                                                        - label_plate_thickness: QLabel
                                                                        - label_discharge: QLabel
                                                                        - lineEdit_hole_diameter: QLineEdit
                                                                        - label_14: QLabel
                                                                        - label_15: QLabel
                                                                        - label_16: QLabel
                                                                        - lineEdit_plate_thickness: QLineEdit
                                                                        - label_17: QLabel
                                                                        - frame_single_hole: QFrame
                                                                            - (Layout): QGridLayout
                                                                                    - checkBox_single_hole: QCheckBox
                                                                        - comboBox_perforated_plate_model: QComboBox
                                                                        - label_HoleDiameter_2: QLabel
                                                - tab_advanced: QWidget
                                                    - (Layout): QGridLayout
                                                            - scrollArea: QScrollArea
                                                                - scrollAreaWidgetContents: QWidget
                                                                    - (Layout): QGridLayout
                                                                            - frame_14: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - checkBox_dimensionless_impedance: QCheckBox
                                                                            - frame_11: QFrame
                                                                                - (Layout): QGridLayout
                                                                                        - label_27: QLabel
                                                                                        - lineEdit_nonlin_discharge: QLineEdit
                                                                                        - lineEdit_correction_factor: QLineEdit
                                                                                        - lineEdit_bias_flow_coefficient: QLineEdit
                                                                                        - label_21: QLabel
                                                                                        - label_28: QLabel
                                                                                        - checkBox_nonlinear_discharge_coefficient: QCheckBox
                                                                                        - checkBox_bias_flow_coefficient: QCheckBox
                                                                                        - label_bias_flow_coefficient: QLabel
                                                                                        - label_correction_factor: QLabel
                                                                                        - label_non_linear_discharge_coefficient: QLabel
                                                                            - tabWidget_dimensionless: QTabWidget
                                                                                - tab_single_value: QWidget
                                                                                    - (Layout): QGridLayout
                                                                                            - label_12: QLabel
                                                                                            - label_10: QLabel
                                                                                            - label_dimensionless_impedance: QLabel
                                                                                            - lineEdit_impedance_imag: QLineEdit
                                                                                            - lineEdit_impedance_real: QLineEdit
                                                                                - tab_table_of_values: QWidget
                                                                                    - (Layout): QGridLayout
                                                                                            - frame_skip: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - label_rows_to_skip: QLabel
                                                                                                        - spinBox_skip_rows: QSpinBox
                                                                                            - frame_17: QFrame
                                                                                                - (Layout): QGridLayout
                                                                                                        - lineEdit_load_table_path: QLineEdit
                                                                                                        - pushButton_load_table: QPushButton
                                            - frame_15: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_attribute: QPushButton
                                                        - pushButton_exit: QPushButton
                                - tab_remove: QWidget
                                    - (Layout): QGridLayout
                                            - frame_22: QFrame
                                                - (Layout): QGridLayout
                                                        - treeWidget_elements_info: QTreeWidget
                                            - frame_19: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_reset: QPushButton
                                                        - pushButton_remove: QPushButton
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - pushButton_plot_absorption_coefficient: QPushButton
                                                        - pushButton_plot_impedance: QPushButton
                                            - frame_20: QFrame
                                                - (Layout): QGridLayout
                                                        - checkBox_remove_valve_structural_effects: QCheckBox
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label: QLabel
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
