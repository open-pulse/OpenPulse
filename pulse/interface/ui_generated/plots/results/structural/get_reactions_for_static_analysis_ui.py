# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_reactions_for_static_analysis.ui'
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
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(356, 536)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 0))
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(1, 4, 1, 4)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 342, 550))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, -1, 0, -1)
        self.frame_treeWidgets = QFrame(self.scrollAreaWidgetContents)
        self.frame_treeWidgets.setObjectName(u"frame_treeWidgets")
        self.frame_treeWidgets.setMinimumSize(QSize(0, 260))
        self.frame_treeWidgets.setMaximumSize(QSize(16777215, 260))
        self.frame_treeWidgets.setFrameShape(QFrame.Shape.Box)
        self.frame_treeWidgets.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_treeWidgets)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 4, 0, 4)
        self.tabWidget_main = QTabWidget(self.frame_treeWidgets)
        self.tabWidget_main.setObjectName(u"tabWidget_main")
        self.tabWidget_main.setMinimumSize(QSize(0, 0))
        self.tabWidget_main.setMaximumSize(QSize(400, 16777215))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.tabWidget_main.setFont(font)
        self.tab_constrained_dofs = QWidget()
        self.tab_constrained_dofs.setObjectName(u"tab_constrained_dofs")
        self.gridLayout_6 = QGridLayout(self.tab_constrained_dofs)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.treeWidget_reactions_at_constrained_dofs = QTreeWidget(self.tab_constrained_dofs)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem.setFont(1, font)
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem.setFont(0, font)
        self.treeWidget_reactions_at_constrained_dofs.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_reactions_at_constrained_dofs.setObjectName(u"treeWidget_reactions_at_constrained_dofs")
        self.treeWidget_reactions_at_constrained_dofs.setMinimumSize(QSize(280, 0))
        self.treeWidget_reactions_at_constrained_dofs.setMaximumSize(QSize(320, 170))
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setItalic(False)
        self.treeWidget_reactions_at_constrained_dofs.setFont(font1)
        self.treeWidget_reactions_at_constrained_dofs.setIndentation(0)

        self.gridLayout_6.addWidget(self.treeWidget_reactions_at_constrained_dofs, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_constrained_dofs, "")
        self.tab_external_springs_dampers = QWidget()
        self.tab_external_springs_dampers.setObjectName(u"tab_external_springs_dampers")
        self.gridLayout_7 = QGridLayout(self.tab_external_springs_dampers)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget_springs_dampers = QTabWidget(self.tab_external_springs_dampers)
        self.tabWidget_springs_dampers.setObjectName(u"tabWidget_springs_dampers")
        self.tabWidget_springs_dampers.setFont(font)
        self.tab_reactions_at_springs = QWidget()
        self.tab_reactions_at_springs.setObjectName(u"tab_reactions_at_springs")
        self.gridLayout_8 = QGridLayout(self.tab_reactions_at_springs)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.treeWidget_reactions_at_springs = QTreeWidget(self.tab_reactions_at_springs)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(1, font)
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem1.setFont(0, font)
        self.treeWidget_reactions_at_springs.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_reactions_at_springs.setObjectName(u"treeWidget_reactions_at_springs")
        self.treeWidget_reactions_at_springs.setMinimumSize(QSize(280, 0))
        self.treeWidget_reactions_at_springs.setMaximumSize(QSize(320, 150))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(True)
        self.treeWidget_reactions_at_springs.setFont(font2)
        self.treeWidget_reactions_at_springs.setIndentation(0)

        self.gridLayout_8.addWidget(self.treeWidget_reactions_at_springs, 0, 0, 1, 1)

        self.tabWidget_springs_dampers.addTab(self.tab_reactions_at_springs, "")
        self.tab_reactions_at_dampers = QWidget()
        self.tab_reactions_at_dampers.setObjectName(u"tab_reactions_at_dampers")
        self.gridLayout_9 = QGridLayout(self.tab_reactions_at_dampers)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.treeWidget_reactions_at_dampers = QTreeWidget(self.tab_reactions_at_dampers)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter)
        __qtreewidgetitem2.setFont(1, font)
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter)
        __qtreewidgetitem2.setFont(0, font)
        self.treeWidget_reactions_at_dampers.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_reactions_at_dampers.setObjectName(u"treeWidget_reactions_at_dampers")
        self.treeWidget_reactions_at_dampers.setMinimumSize(QSize(280, 0))
        self.treeWidget_reactions_at_dampers.setMaximumSize(QSize(320, 150))
        self.treeWidget_reactions_at_dampers.setFont(font1)
        self.treeWidget_reactions_at_dampers.setIndentation(0)

        self.gridLayout_9.addWidget(self.treeWidget_reactions_at_dampers, 0, 0, 1, 1)

        self.tabWidget_springs_dampers.addTab(self.tab_reactions_at_dampers, "")

        self.gridLayout_7.addWidget(self.tabWidget_springs_dampers, 0, 0, 1, 1)

        self.tabWidget_main.addTab(self.tab_external_springs_dampers, "")

        self.gridLayout_4.addWidget(self.tabWidget_main, 1, 0, 1, 1)

        self.frame_16 = QFrame(self.frame_treeWidgets)
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
        self.label_15 = QLabel(self.frame_16)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(0, 28))
        self.label_15.setMaximumSize(QSize(16777215, 28))
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_14.addWidget(self.label_15, 0, 1, 1, 1)

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
        font3 = QFont()
        font3.setFamilies([u"MS Shell Dlg 2"])
        font3.setPointSize(11)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_node_id.setFont(font3)
        self.lineEdit_node_id.setStyleSheet(u"")
        self.lineEdit_node_id.setFrame(True)
        self.lineEdit_node_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_node_id.setReadOnly(False)

        self.gridLayout_14.addWidget(self.lineEdit_node_id, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButton_reset = QPushButton(self.frame_16)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setMinimumSize(QSize(52, 26))
        self.pushButton_reset.setMaximumSize(QSize(52, 26))
        font4 = QFont()
        font4.setPointSize(9)
        self.pushButton_reset.setFont(font4)
        self.pushButton_reset.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.pushButton_reset, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.frame_16, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_treeWidgets, 1, 0, 1, 1)

        self.frame_title = QFrame(self.scrollAreaWidgetContents)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setMinimumSize(QSize(0, 40))
        self.frame_title.setMaximumSize(QSize(16777215, 40))
        self.frame_title.setFrameShape(QFrame.Shape.Box)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_title)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_title)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(300, 32))
        self.label.setMaximumSize(QSize(300, 32))
        font5 = QFont()
        font5.setPointSize(11)
        font5.setBold(False)
        self.label.setFont(font5)
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setFrameShadow(QFrame.Shadow.Raised)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.frame_title, 0, 0, 1, 1)

        self.frame_responses = QFrame(self.scrollAreaWidgetContents)
        self.frame_responses.setObjectName(u"frame_responses")
        self.frame_responses.setMinimumSize(QSize(0, 220))
        self.frame_responses.setMaximumSize(QSize(16777215, 16777215))
        self.frame_responses.setFrameShape(QFrame.Shape.Box)
        self.frame_responses.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_responses)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_reaction_mz = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_mz.setObjectName(u"lineEdit_reaction_mz")
        self.lineEdit_reaction_mz.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_mz.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_mz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_mz.setBaseSize(QSize(0, 0))
        font6 = QFont()
        font6.setPointSize(10)
        self.lineEdit_reaction_mz.setFont(font6)
        self.lineEdit_reaction_mz.setStyleSheet(u"")
        self.lineEdit_reaction_mz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_mz, 5, 2, 1, 1)

        self.label_9 = QLabel(self.frame_responses)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(52, 28))
        self.label_9.setMaximumSize(QSize(52, 28))
        font7 = QFont()
        font7.setPointSize(10)
        font7.setBold(False)
        self.label_9.setFont(font7)
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_9, 1, 3, 1, 1)

        self.lineEdit_reaction_fz = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_fz.setObjectName(u"lineEdit_reaction_fz")
        self.lineEdit_reaction_fz.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_fz.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_fz.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_fz.setBaseSize(QSize(0, 0))
        self.lineEdit_reaction_fz.setFont(font6)
        self.lineEdit_reaction_fz.setStyleSheet(u"")
        self.lineEdit_reaction_fz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_fz, 2, 2, 1, 1)

        self.lineEdit_reaction_fx = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_fx.setObjectName(u"lineEdit_reaction_fx")
        self.lineEdit_reaction_fx.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_fx.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_fx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_fx.setBaseSize(QSize(0, 0))
        self.lineEdit_reaction_fx.setFont(font6)
        self.lineEdit_reaction_fx.setStyleSheet(u"")
        self.lineEdit_reaction_fx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_fx, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame_responses)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(72, 28))
        self.label_3.setMaximumSize(QSize(72, 28))
        self.label_3.setFont(font7)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)

        self.lineEdit_reaction_mx = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_mx.setObjectName(u"lineEdit_reaction_mx")
        self.lineEdit_reaction_mx.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_mx.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_mx.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_mx.setBaseSize(QSize(0, 0))
        self.lineEdit_reaction_mx.setFont(font6)
        self.lineEdit_reaction_mx.setStyleSheet(u"")
        self.lineEdit_reaction_mx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_mx, 3, 2, 1, 1)

        self.label_13 = QLabel(self.frame_responses)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(52, 28))
        self.label_13.setMaximumSize(QSize(52, 28))
        self.label_13.setFont(font7)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_13, 5, 3, 1, 1)

        self.label_6 = QLabel(self.frame_responses)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(72, 28))
        self.label_6.setMaximumSize(QSize(72, 28))
        self.label_6.setFont(font7)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_6, 4, 1, 1, 1)

        self.label_10 = QLabel(self.frame_responses)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(52, 28))
        self.label_10.setMaximumSize(QSize(52, 28))
        self.label_10.setFont(font7)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 2, 3, 1, 1)

        self.frame_5 = QFrame(self.frame_responses)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.frame_5, 0, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_responses)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_6)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.frame_6, 0, 4, 1, 1)

        self.label_2 = QLabel(self.frame_responses)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(72, 28))
        self.label_2.setMaximumSize(QSize(72, 28))
        self.label_2.setFont(font7)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_8 = QLabel(self.frame_responses)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(52, 28))
        self.label_8.setMaximumSize(QSize(52, 28))
        self.label_8.setFont(font7)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 0, 3, 1, 1)

        self.label_12 = QLabel(self.frame_responses)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(52, 28))
        self.label_12.setMaximumSize(QSize(52, 28))
        self.label_12.setFont(font7)
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_12, 4, 3, 1, 1)

        self.label_11 = QLabel(self.frame_responses)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(52, 28))
        self.label_11.setMaximumSize(QSize(52, 28))
        self.label_11.setFont(font7)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_11, 3, 3, 1, 1)

        self.label_7 = QLabel(self.frame_responses)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(72, 28))
        self.label_7.setMaximumSize(QSize(72, 28))
        self.label_7.setFont(font7)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_7, 5, 1, 1, 1)

        self.lineEdit_reaction_my = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_my.setObjectName(u"lineEdit_reaction_my")
        self.lineEdit_reaction_my.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_my.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_my.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_my.setBaseSize(QSize(0, 0))
        self.lineEdit_reaction_my.setFont(font6)
        self.lineEdit_reaction_my.setStyleSheet(u"")
        self.lineEdit_reaction_my.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_my, 4, 2, 1, 1)

        self.label_4 = QLabel(self.frame_responses)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(72, 28))
        self.label_4.setMaximumSize(QSize(72, 28))
        self.label_4.setFont(font7)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_4, 2, 1, 1, 1)

        self.label_5 = QLabel(self.frame_responses)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(72, 28))
        self.label_5.setMaximumSize(QSize(72, 28))
        self.label_5.setFont(font7)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 3, 1, 1, 1)

        self.lineEdit_reaction_fy = QLineEdit(self.frame_responses)
        self.lineEdit_reaction_fy.setObjectName(u"lineEdit_reaction_fy")
        self.lineEdit_reaction_fy.setMinimumSize(QSize(120, 28))
        self.lineEdit_reaction_fy.setMaximumSize(QSize(120, 28))
        self.lineEdit_reaction_fy.setSizeIncrement(QSize(0, 0))
        self.lineEdit_reaction_fy.setBaseSize(QSize(0, 0))
        self.lineEdit_reaction_fy.setFont(font6)
        self.lineEdit_reaction_fy.setStyleSheet(u"")
        self.lineEdit_reaction_fy.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_reaction_fy, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.frame_responses, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineEdit_node_id, self.pushButton_reset)
        QWidget.setTabOrder(self.pushButton_reset, self.tabWidget_main)
        QWidget.setTabOrder(self.tabWidget_main, self.treeWidget_reactions_at_constrained_dofs)
        QWidget.setTabOrder(self.treeWidget_reactions_at_constrained_dofs, self.tabWidget_springs_dampers)
        QWidget.setTabOrder(self.tabWidget_springs_dampers, self.treeWidget_reactions_at_springs)
        QWidget.setTabOrder(self.treeWidget_reactions_at_springs, self.treeWidget_reactions_at_dampers)
        QWidget.setTabOrder(self.treeWidget_reactions_at_dampers, self.lineEdit_reaction_fx)
        QWidget.setTabOrder(self.lineEdit_reaction_fx, self.lineEdit_reaction_fy)
        QWidget.setTabOrder(self.lineEdit_reaction_fy, self.lineEdit_reaction_fz)
        QWidget.setTabOrder(self.lineEdit_reaction_fz, self.lineEdit_reaction_mx)
        QWidget.setTabOrder(self.lineEdit_reaction_mx, self.lineEdit_reaction_my)
        QWidget.setTabOrder(self.lineEdit_reaction_my, self.lineEdit_reaction_mz)

        self.retranslateUi(Form)

        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_springs_dampers.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
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
        self.label_15.setText(QCoreApplication.translate("Form", u"Node ID:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_node_id.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.lineEdit_node_id.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.lineEdit_node_id.setText("")
        self.lineEdit_node_id.setPlaceholderText("")
        self.pushButton_reset.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label.setText(QCoreApplication.translate("Form", u"Static reactions", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_mz.setToolTip(QCoreApplication.translate("Form", u"Moment Mz reaction", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("Form", u" [N]", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_fz.setToolTip(QCoreApplication.translate("Form", u"Force Fz reaction", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_fx.setToolTip(QCoreApplication.translate("Form", u"Force Fx reaction", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Form", u"Fy: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_mx.setToolTip(QCoreApplication.translate("Form", u"Moment Mx reaction", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("Form", u" [N.m]", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"My: ", None))
        self.label_10.setText(QCoreApplication.translate("Form", u" [N]", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Fx: ", None))
        self.label_8.setText(QCoreApplication.translate("Form", u" [N]", None))
        self.label_12.setText(QCoreApplication.translate("Form", u" [N.m]", None))
        self.label_11.setText(QCoreApplication.translate("Form", u" [N.m]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Mz: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_my.setToolTip(QCoreApplication.translate("Form", u"Moment My reaction", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Form", u"Fz: ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Mx: ", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_reaction_fy.setToolTip(QCoreApplication.translate("Form", u"Force Fy reaction", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi



class GetReactionsForStaticAnalysis_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QGridLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - frame_treeWidgets: QFrame
                                    - (Layout): QGridLayout
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
                                            - frame_16: QFrame
                                                - (Layout): QGridLayout
                                                        - label_15: QLabel
                                                        - lineEdit_node_id: QLineEdit
                                                        - pushButton_reset: QPushButton
                                - frame_title: QFrame
                                    - (Layout): QGridLayout
                                            - label: QLabel
                                - frame_responses: QFrame
                                    - (Layout): QGridLayout
                                            - lineEdit_reaction_mz: QLineEdit
                                            - label_9: QLabel
                                            - lineEdit_reaction_fz: QLineEdit
                                            - lineEdit_reaction_fx: QLineEdit
                                            - label_3: QLabel
                                            - lineEdit_reaction_mx: QLineEdit
                                            - label_13: QLabel
                                            - label_6: QLabel
                                            - label_10: QLabel
                                            - frame_5: QFrame
                                            - frame_6: QFrame
                                                - (Layout): QGridLayout
                                            - label_2: QLabel
                                            - label_8: QLabel
                                            - label_12: QLabel
                                            - label_11: QLabel
                                            - label_7: QLabel
                                            - lineEdit_reaction_my: QLineEdit
                                            - label_4: QLabel
                                            - label_5: QLabel
                                            - lineEdit_reaction_fy: QLineEdit
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
