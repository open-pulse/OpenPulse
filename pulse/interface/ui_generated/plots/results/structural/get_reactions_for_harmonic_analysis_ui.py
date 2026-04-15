# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_reactions_for_harmonic_analysis.ui'
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
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(354, 594)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 4, 1, 4)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(300, 42))
        self.frame.setMaximumSize(QSize(600, 42))
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(1)
        self.gridLayout_11 = QGridLayout(self.frame)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.label_10.setFont(font)
        self.label_10.setFrameShape(QFrame.Shape.NoFrame)
        self.label_10.setFrameShadow(QFrame.Shadow.Raised)
        self.label_10.setTextFormat(Qt.TextFormat.AutoText)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.label_10, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 360))
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_2)
        self.gridLayout_15.setSpacing(2)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(2, 4, 2, 2)
        self.frame_16 = QFrame(self.frame_2)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 40))
        self.frame_16.setMaximumSize(QSize(400, 40))
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_16)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(6)
        self.gridLayout_14.setVerticalSpacing(0)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_16)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 28))
        self.label_2.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_2, 0, 1, 1, 1)

        self.lineEdit_node_id = QLineEdit(self.frame_16)
        self.lineEdit_node_id.setObjectName(u"lineEdit_node_id")
        self.lineEdit_node_id.setEnabled(False)
        self.lineEdit_node_id.setMinimumSize(QSize(80, 28))
        self.lineEdit_node_id.setMaximumSize(QSize(80, 28))
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
        self.lineEdit_node_id.setPalette(palette)
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setKerning(False)
        self.lineEdit_node_id.setFont(font2)
        self.lineEdit_node_id.setStyleSheet(u"")
        self.lineEdit_node_id.setFrame(True)
        self.lineEdit_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_node_id.setReadOnly(False)

        self.gridLayout_14.addWidget(self.lineEdit_node_id, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)


        self.gridLayout_15.addWidget(self.frame_16, 0, 0, 1, 1)

        self.tabWidget_main = QTabWidget(self.frame_2)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMaximumSize(QSize(400, 16777215))
        self.tabWidget_main.setFont(font1)
        self.tab_constrained_dofs = QWidget()
        self.tab_constrained_dofs.setObjectName(u"tab_constrained_dofs")
        self.gridLayout_16 = QGridLayout(self.tab_constrained_dofs)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.treeWidget_reactions_at_constrained_dofs = QTreeWidget(self.tab_constrained_dofs)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font2)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font2)
        self.treeWidget_reactions_at_constrained_dofs.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_reactions_at_constrained_dofs.setObjectName(u"treeWidget_reactions_at_constrained_dofs")
        self.treeWidget_reactions_at_constrained_dofs.setMinimumSize(QSize(282, 0))
        self.treeWidget_reactions_at_constrained_dofs.setMaximumSize(QSize(282, 170))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.treeWidget_reactions_at_constrained_dofs.setFont(font3)
        self.treeWidget_reactions_at_constrained_dofs.setIndentation(0)

        self.gridLayout_16.addWidget(self.treeWidget_reactions_at_constrained_dofs, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constrained_dofs, "")
        self.tab_external_springs_dampers = QWidget()
        self.tab_external_springs_dampers.setObjectName(u"tab_external_springs_dampers")
        self.gridLayout_17 = QGridLayout(self.tab_external_springs_dampers)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.tabWidget_springs_dampers = QTabWidget(self.tab_external_springs_dampers)
        self.tabWidget_springs_dampers.setObjectName(u"tabWidget_springs_dampers")
        self.tabWidget_springs_dampers.setFont(font1)
        self.tab_reactions_at_springs = QWidget()
        self.tab_reactions_at_springs.setObjectName(u"tab_reactions_at_springs")
        self.gridLayout_18 = QGridLayout(self.tab_reactions_at_springs)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.treeWidget_reactions_at_springs = QTreeWidget(self.tab_reactions_at_springs)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(1, font2)
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(0, font2)
        self.treeWidget_reactions_at_springs.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_reactions_at_springs.setObjectName(u"treeWidget_reactions_at_springs")
        self.treeWidget_reactions_at_springs.setMinimumSize(QSize(282, 150))
        self.treeWidget_reactions_at_springs.setMaximumSize(QSize(282, 150))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setItalic(False)
        self.treeWidget_reactions_at_springs.setFont(font4)
        self.treeWidget_reactions_at_springs.setIndentation(0)

        self.gridLayout_18.addWidget(self.treeWidget_reactions_at_springs, 0, 0, 1, 1)

        self.tabWidget_springs_dampers.addTab(self.tab_reactions_at_springs, "")
        self.tab_reactions_at_dampers = QWidget()
        self.tab_reactions_at_dampers.setObjectName(u"tab_reactions_at_dampers")
        self.gridLayout_19 = QGridLayout(self.tab_reactions_at_dampers)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.treeWidget_reactions_at_dampers = QTreeWidget(self.tab_reactions_at_dampers)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem2.setFont(1, font2)
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem2.setFont(0, font2)
        self.treeWidget_reactions_at_dampers.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_reactions_at_dampers.setObjectName(u"treeWidget_reactions_at_dampers")
        self.treeWidget_reactions_at_dampers.setMinimumSize(QSize(282, 150))
        self.treeWidget_reactions_at_dampers.setMaximumSize(QSize(282, 150))
        self.treeWidget_reactions_at_dampers.setFont(font4)
        self.treeWidget_reactions_at_dampers.setIndentation(0)

        self.gridLayout_19.addWidget(self.treeWidget_reactions_at_dampers, 0, 0, 1, 1)

        self.tabWidget_springs_dampers.addTab(self.tab_reactions_at_dampers, "")

        self.gridLayout_17.addWidget(self.tabWidget_springs_dampers, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_external_springs_dampers, "")

        self.gridLayout_15.addWidget(self.tabWidget_main, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(300, 42))
        self.frame_3.setMaximumSize(QSize(600, 42))
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3.setLineWidth(1)
        self.gridLayout_12 = QGridLayout(self.frame_3)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(2, 2, 2, 2)
        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 30))
        self.label_11.setMaximumSize(QSize(16777215, 30))
        self.label_11.setFont(font)
        self.label_11.setFrameShape(QFrame.Shape.NoFrame)
        self.label_11.setFrameShadow(QFrame.Shadow.Raised)
        self.label_11.setTextFormat(Qt.TextFormat.AutoText)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_11, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_3, 2, 0, 1, 1)

        self.frame_15 = QFrame(Form)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(16777215, 300))
        self.frame_15.setFrameShape(QFrame.Shape.Box)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_21 = QGridLayout(self.frame_15)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setHorizontalSpacing(4)
        self.gridLayout_21.setVerticalSpacing(2)
        self.gridLayout_21.setContentsMargins(4, 4, 4, 4)
        self.frame_9 = QFrame(self.frame_15)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 120))
        self.frame_9.setMaximumSize(QSize(16777215, 140))
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_9)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(2)
        self.gridLayout_7.setVerticalSpacing(4)
        self.gridLayout_7.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.frame_9)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(200, 140))
        self.frame_5.setFrameShape(QFrame.Shape.Box)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.radioButton_Fy = QRadioButton(self.frame_5)
        self.radioButton_Fy.setObjectName(u"radioButton_Fy")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_Fy.sizePolicy().hasHeightForWidth())
        self.radioButton_Fy.setSizePolicy(sizePolicy)
        self.radioButton_Fy.setMaximumSize(QSize(85, 16777215))
        self.radioButton_Fy.setFont(font1)
        self.radioButton_Fy.setCheckable(True)
        self.radioButton_Fy.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_Fy, 1, 1, 1, 1)

        self.radioButton_Fx = QRadioButton(self.frame_5)
        self.radioButton_Fx.setObjectName(u"radioButton_Fx")
        sizePolicy.setHeightForWidth(self.radioButton_Fx.sizePolicy().hasHeightForWidth())
        self.radioButton_Fx.setSizePolicy(sizePolicy)
        self.radioButton_Fx.setMaximumSize(QSize(85, 16777215))
        self.radioButton_Fx.setFont(font2)
        self.radioButton_Fx.setChecked(True)

        self.gridLayout.addWidget(self.radioButton_Fx, 0, 1, 1, 1)

        self.radioButton_My = QRadioButton(self.frame_5)
        self.radioButton_My.setObjectName(u"radioButton_My")
        sizePolicy.setHeightForWidth(self.radioButton_My.sizePolicy().hasHeightForWidth())
        self.radioButton_My.setSizePolicy(sizePolicy)
        self.radioButton_My.setMaximumSize(QSize(85, 16777215))
        self.radioButton_My.setFont(font1)
        self.radioButton_My.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_My, 1, 3, 1, 1)

        self.radioButton_Mz = QRadioButton(self.frame_5)
        self.radioButton_Mz.setObjectName(u"radioButton_Mz")
        sizePolicy.setHeightForWidth(self.radioButton_Mz.sizePolicy().hasHeightForWidth())
        self.radioButton_Mz.setSizePolicy(sizePolicy)
        self.radioButton_Mz.setMaximumSize(QSize(85, 16777215))
        self.radioButton_Mz.setFont(font1)
        self.radioButton_Mz.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_Mz, 2, 3, 1, 1)

        self.radioButton_Mx = QRadioButton(self.frame_5)
        self.radioButton_Mx.setObjectName(u"radioButton_Mx")
        sizePolicy.setHeightForWidth(self.radioButton_Mx.sizePolicy().hasHeightForWidth())
        self.radioButton_Mx.setSizePolicy(sizePolicy)
        self.radioButton_Mx.setMaximumSize(QSize(85, 16777215))
        self.radioButton_Mx.setFont(font1)
        self.radioButton_Mx.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_Mx, 0, 3, 1, 1)

        self.radioButton_Fz = QRadioButton(self.frame_5)
        self.radioButton_Fz.setObjectName(u"radioButton_Fz")
        sizePolicy.setHeightForWidth(self.radioButton_Fz.sizePolicy().hasHeightForWidth())
        self.radioButton_Fz.setSizePolicy(sizePolicy)
        self.radioButton_Fz.setMaximumSize(QSize(85, 16777215))
        self.radioButton_Fz.setFont(font1)
        self.radioButton_Fz.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_Fz, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 1, 4, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 2, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_10, 2, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_11, 2, 4, 1, 1)


        self.gridLayout_7.addWidget(self.frame_5, 1, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(0, 32))
        self.frame_10.setMaximumSize(QSize(200, 32))
        self.frame_10.setFrameShape(QFrame.Shape.Box)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_10)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_10)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(80, 25))
        self.label_3.setMaximumSize(QSize(237, 25))
        font5 = QFont()
        font5.setPointSize(11)
        font5.setBold(False)
        self.label_3.setFont(font5)
        self.label_3.setFrameShape(QFrame.Shape.NoFrame)
        self.label_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_3.setTextFormat(Qt.TextFormat.AutoText)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(False)
        self.label_3.setIndent(0)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_10, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_9, 0, 0, 1, 1)

        self.frame_12 = QFrame(self.frame_15)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 40))
        self.frame_12.setMaximumSize(QSize(16777215, 40))
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_12)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(4)
        self.gridLayout_9.setVerticalSpacing(0)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_plot_data = QPushButton(self.frame_12)
        self.pushButton_plot_data.setObjectName(u"pushButton_plot_data")
        self.pushButton_plot_data.setMinimumSize(QSize(100, 30))
        self.pushButton_plot_data.setMaximumSize(QSize(100, 30))
        self.pushButton_plot_data.setFont(font1)
        self.pushButton_plot_data.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.pushButton_plot_data, 0, 0, 1, 1)


        self.gridLayout_21.addWidget(self.frame_12, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_15, 3, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_id, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.treeWidget_reactions_at_constrained_dofs)
        QWidget.setTabOrder(self.treeWidget_reactions_at_constrained_dofs, self.tabWidget_springs_dampers)
        QWidget.setTabOrder(self.tabWidget_springs_dampers, self.treeWidget_reactions_at_springs)
        QWidget.setTabOrder(self.treeWidget_reactions_at_springs, self.treeWidget_reactions_at_dampers)
        QWidget.setTabOrder(self.treeWidget_reactions_at_dampers, self.radioButton_Fx)
        QWidget.setTabOrder(self.radioButton_Fx, self.radioButton_Mx)
        QWidget.setTabOrder(self.radioButton_Mx, self.radioButton_Fy)
        QWidget.setTabOrder(self.radioButton_Fy, self.radioButton_My)
        QWidget.setTabOrder(self.radioButton_My, self.radioButton_Fz)
        QWidget.setTabOrder(self.radioButton_Fz, self.radioButton_Mz)
        QWidget.setTabOrder(self.radioButton_Mz, self.pushButton_plot_data)

        self.retranslateUi(Form)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_springs_dampers.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Select the node to get reactions", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Node ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_node_id.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEdit_node_id.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_node_id.setText("")
        self.lineEdit_node_id.setPlaceholderText("")
        ___qtreewidgetitem = self.treeWidget_reactions_at_constrained_dofs.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Reactions", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Nodes", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_constrained_dofs), QCoreApplication.translate("Form", u"Constrained DOFs", None))
        ___qtreewidgetitem1 = self.treeWidget_reactions_at_springs.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Form", u"Reactions", None))
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Form", u"Nodes", None))
        self.tabWidget_springs_dampers.setTabText(self.tabWidget_springs_dampers.indexOf(self.tab_reactions_at_springs), QCoreApplication.translate("Form", u"Reactions at springs", None))
        ___qtreewidgetitem2 = self.treeWidget_reactions_at_dampers.headerItem()
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Form", u"Reactions", None))
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Form", u"Nodes", None))
        self.tabWidget_springs_dampers.setTabText(self.tabWidget_springs_dampers.indexOf(self.tab_reactions_at_dampers), QCoreApplication.translate("Form", u"Reactions at dampers", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_external_springs_dampers), QCoreApplication.translate("Form", u"External elements", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Plot the reactions at selected node", None))
        self.radioButton_Fy.setText(QCoreApplication.translate("Form", u"Fy", None))
        self.radioButton_Fx.setText(QCoreApplication.translate("Form", u"Fx", None))
        self.radioButton_My.setText(QCoreApplication.translate("Form", u"My", None))
        self.radioButton_Mz.setText(QCoreApplication.translate("Form", u"Mz", None))
        self.radioButton_Mx.setText(QCoreApplication.translate("Form", u"Mx", None))
        self.radioButton_Fz.setText(QCoreApplication.translate("Form", u"Fz", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Load to get response", None))
        self.pushButton_plot_data.setText(QCoreApplication.translate("Form", u"Plot data", None))
    # retranslateUi



class GetReactionsForHarmonicAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - frame: QFrame
                    - (Layout): QGridLayout
                            - label_10: QLabel
                - frame_2: QFrame
                    - (Layout): QGridLayout
                            - frame_16: QFrame
                                - (Layout): QGridLayout
                                        - label_2: QLabel
                                        - lineEdit_node_id: QLineEdit
                            - tabWidget_main: QTabWidget
                                - tab_constrained_dofs: QWidget
                                    - (Layout): QGridLayout
                                            - treeWidget_reactions_at_constrained_dofs: QTreeWidget
                                - tab_external_springs_dampers: QWidget
                                    - (Layout): QGridLayout
                                            - tabWidget_springs_dampers: QTabWidget
                                                - tab_reactions_at_springs: QWidget
                                                    - (Layout): QGridLayout
                                                            - treeWidget_reactions_at_springs: QTreeWidget
                                                - tab_reactions_at_dampers: QWidget
                                                    - (Layout): QGridLayout
                                                            - treeWidget_reactions_at_dampers: QTreeWidget
                - frame_3: QFrame
                    - (Layout): QGridLayout
                            - label_11: QLabel
                - frame_15: QFrame
                    - (Layout): QGridLayout
                            - frame_9: QFrame
                                - (Layout): QGridLayout
                                        - frame_5: QFrame
                                            - (Layout): QGridLayout
                                                    - radioButton_Fy: QRadioButton
                                                    - radioButton_Fx: QRadioButton
                                                    - radioButton_My: QRadioButton
                                                    - radioButton_Mz: QRadioButton
                                                    - radioButton_Mx: QRadioButton
                                                    - radioButton_Fz: QRadioButton
                                        - frame_10: QFrame
                                            - (Layout): QGridLayout
                                                    - label_3: QLabel
                            - frame_12: QFrame
                                - (Layout): QGridLayout
                                        - pushButton_plot_data: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
