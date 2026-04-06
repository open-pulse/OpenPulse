# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'expansion_joint_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(406, 449)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_7 = QSpacerItem(20, 21, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_7)

        self.frame_top_inputs = QFrame(Form)
        self.frame_top_inputs.setObjectName(u"frame_top_inputs")
        self.frame_top_inputs.setMinimumSize(QSize(0, 0))
        self.frame_top_inputs.setMaximumSize(QSize(451, 574))
        self.frame_top_inputs.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_top_inputs.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_top_inputs)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setHorizontalSpacing(8)
        self.gridLayout_12.setVerticalSpacing(6)
        self.gridLayout_12.setContentsMargins(4, 4, 4, 4)
        self.lineEdit_joint_mass = QLineEdit(self.frame_top_inputs)
        self.lineEdit_joint_mass.setObjectName(u"lineEdit_joint_mass")
        self.lineEdit_joint_mass.setEnabled(True)
        self.lineEdit_joint_mass.setMinimumSize(QSize(120, 26))
        self.lineEdit_joint_mass.setMaximumSize(QSize(120, 26))
        self.lineEdit_joint_mass.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.lineEdit_joint_mass.setFont(font)
        self.lineEdit_joint_mass.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_joint_mass.setStyleSheet(u"")
        self.lineEdit_joint_mass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_joint_mass, 1, 1, 1, 1)

        self.label_axial_lock_criteria = QLabel(self.frame_top_inputs)
        self.label_axial_lock_criteria.setObjectName(u"label_axial_lock_criteria")
        self.label_axial_lock_criteria.setEnabled(True)
        self.label_axial_lock_criteria.setMinimumSize(QSize(148, 26))
        self.label_axial_lock_criteria.setMaximumSize(QSize(148, 26))
        self.label_axial_lock_criteria.setFont(font)
        self.label_axial_lock_criteria.setMouseTracking(True)
        self.label_axial_lock_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_axial_lock_criteria, 2, 0, 1, 1)

        self.label_111 = QLabel(self.frame_top_inputs)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setEnabled(True)
        self.label_111.setMinimumSize(QSize(80, 26))
        self.label_111.setMaximumSize(QSize(100, 26))
        self.label_111.setFont(font)
        self.label_111.setMouseTracking(True)
        self.label_111.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_111, 1, 2, 1, 1)

        self.label_102 = QLabel(self.frame_top_inputs)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setEnabled(True)
        self.label_102.setMinimumSize(QSize(148, 26))
        self.label_102.setMaximumSize(QSize(148, 26))
        self.label_102.setFont(font)
        self.label_102.setMouseTracking(True)
        self.label_102.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_102, 1, 0, 1, 1)

        self.comboBox_axial_stop_rod = QComboBox(self.frame_top_inputs)
        self.comboBox_axial_stop_rod.addItem("")
        self.comboBox_axial_stop_rod.addItem("")
        self.comboBox_axial_stop_rod.setObjectName(u"comboBox_axial_stop_rod")
        self.comboBox_axial_stop_rod.setMinimumSize(QSize(120, 26))
        self.comboBox_axial_stop_rod.setMaximumSize(QSize(120, 26))
        self.comboBox_axial_stop_rod.setFont(font)

        self.gridLayout_12.addWidget(self.comboBox_axial_stop_rod, 3, 1, 1, 1)

        self.lineEdit_axial_locking_criteria = QLineEdit(self.frame_top_inputs)
        self.lineEdit_axial_locking_criteria.setObjectName(u"lineEdit_axial_locking_criteria")
        self.lineEdit_axial_locking_criteria.setEnabled(True)
        self.lineEdit_axial_locking_criteria.setMinimumSize(QSize(120, 26))
        self.lineEdit_axial_locking_criteria.setMaximumSize(QSize(120, 26))
        self.lineEdit_axial_locking_criteria.setSizeIncrement(QSize(0, 26))
        self.lineEdit_axial_locking_criteria.setFont(font)
        self.lineEdit_axial_locking_criteria.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_axial_locking_criteria.setStyleSheet(u"")
        self.lineEdit_axial_locking_criteria.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_axial_locking_criteria, 2, 1, 1, 1)

        self.label_109 = QLabel(self.frame_top_inputs)
        self.label_109.setObjectName(u"label_109")
        self.label_109.setEnabled(True)
        self.label_109.setMinimumSize(QSize(148, 26))
        self.label_109.setMaximumSize(QSize(148, 26))
        self.label_109.setFont(font)
        self.label_109.setMouseTracking(True)
        self.label_109.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.label_109, 3, 0, 1, 1)

        self.lineEdit_effective_diameter = QLineEdit(self.frame_top_inputs)
        self.lineEdit_effective_diameter.setObjectName(u"lineEdit_effective_diameter")
        self.lineEdit_effective_diameter.setEnabled(True)
        self.lineEdit_effective_diameter.setMinimumSize(QSize(120, 26))
        self.lineEdit_effective_diameter.setMaximumSize(QSize(120, 26))
        self.lineEdit_effective_diameter.setSizeIncrement(QSize(0, 0))
        self.lineEdit_effective_diameter.setFont(font)
        self.lineEdit_effective_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_effective_diameter.setStyleSheet(u"")
        self.lineEdit_effective_diameter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_12.addWidget(self.lineEdit_effective_diameter, 0, 1, 1, 1)

        self.label_107 = QLabel(self.frame_top_inputs)
        self.label_107.setObjectName(u"label_107")
        self.label_107.setEnabled(True)
        self.label_107.setMinimumSize(QSize(80, 26))
        self.label_107.setMaximumSize(QSize(100, 26))
        self.label_107.setFont(font)
        self.label_107.setMouseTracking(True)
        self.label_107.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_107, 0, 2, 1, 1)

        self.label_103 = QLabel(self.frame_top_inputs)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setEnabled(True)
        self.label_103.setMinimumSize(QSize(148, 26))
        self.label_103.setMaximumSize(QSize(148, 26))
        self.label_103.setFont(font)
        self.label_103.setMouseTracking(True)
        self.label_103.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_103, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_top_inputs)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.frame_bottom_inputs = QFrame(Form)
        self.frame_bottom_inputs.setObjectName(u"frame_bottom_inputs")
        self.frame_bottom_inputs.setMaximumSize(QSize(16777215, 200))
        self.frame_bottom_inputs.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_bottom_inputs.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_bottom_inputs)
        self.gridLayout_14.setSpacing(4)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(4, 0, 4, 0)
        self.tabWidget_inputs = QTabWidget(self.frame_bottom_inputs)
        self.tabWidget_inputs.setObjectName(u"tabWidget_inputs")
        self.tabWidget_inputs.setMinimumSize(QSize(380, 0))
        self.tabWidget_inputs.setMaximumSize(QSize(16777215, 180))
        self.tabWidget_inputs.setSizeIncrement(QSize(0, 0))
        self.tab_constant_values = QWidget()
        self.tab_constant_values.setObjectName(u"tab_constant_values")
        self.gridLayout_15 = QGridLayout(self.tab_constant_values)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(4, 6, 4, 6)
        self.label_116 = QLabel(self.tab_constant_values)
        self.label_116.setObjectName(u"label_116")
        self.label_116.setEnabled(True)
        self.label_116.setMinimumSize(QSize(40, 26))
        self.label_116.setMaximumSize(QSize(40, 26))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_116.setFont(font1)
        self.label_116.setMouseTracking(True)
        self.label_116.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_116, 1, 0, 1, 1)

        self.lineEdit_Kyz = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kyz.setObjectName(u"lineEdit_Kyz")
        self.lineEdit_Kyz.setEnabled(True)
        self.lineEdit_Kyz.setMinimumSize(QSize(0, 0))
        self.lineEdit_Kyz.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_Kyz.setFont(font)
        self.lineEdit_Kyz.setStyleSheet(u"")
        self.lineEdit_Kyz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_Kyz, 1, 1, 1, 1)

        self.lineEdit_Kx = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kx.setObjectName(u"lineEdit_Kx")
        self.lineEdit_Kx.setEnabled(True)
        self.lineEdit_Kx.setMinimumSize(QSize(0, 0))
        self.lineEdit_Kx.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_Kx.setFont(font)
        self.lineEdit_Kx.setStyleSheet(u"")
        self.lineEdit_Kx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_Kx, 0, 1, 1, 1)

        self.lineEdit_Kryz = QLineEdit(self.tab_constant_values)
        self.lineEdit_Kryz.setObjectName(u"lineEdit_Kryz")
        self.lineEdit_Kryz.setEnabled(True)
        self.lineEdit_Kryz.setMinimumSize(QSize(0, 0))
        self.lineEdit_Kryz.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_Kryz.setFont(font)
        self.lineEdit_Kryz.setStyleSheet(u"")
        self.lineEdit_Kryz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_Kryz, 3, 1, 1, 1)

        self.label_16 = QLabel(self.tab_constant_values)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setMinimumSize(QSize(0, 0))
        self.label_16.setMaximumSize(QSize(16777215, 16777215))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_16, 0, 2, 1, 1)

        self.label_93 = QLabel(self.tab_constant_values)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setEnabled(True)
        self.label_93.setMinimumSize(QSize(0, 0))
        self.label_93.setMaximumSize(QSize(40, 26))
        self.label_93.setFont(font1)
        self.label_93.setMouseTracking(True)
        self.label_93.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_93, 2, 0, 1, 1)

        self.label_112 = QLabel(self.tab_constant_values)
        self.label_112.setObjectName(u"label_112")
        self.label_112.setEnabled(True)
        self.label_112.setMinimumSize(QSize(0, 0))
        self.label_112.setMaximumSize(QSize(40, 26))
        self.label_112.setFont(font1)
        self.label_112.setMouseTracking(True)
        self.label_112.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_112, 3, 0, 1, 1)

        self.label_114 = QLabel(self.tab_constant_values)
        self.label_114.setObjectName(u"label_114")
        self.label_114.setMinimumSize(QSize(0, 0))
        self.label_114.setMaximumSize(QSize(16777215, 16777215))
        self.label_114.setFont(font)
        self.label_114.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_114, 3, 2, 1, 1)

        self.label_115 = QLabel(self.tab_constant_values)
        self.label_115.setObjectName(u"label_115")
        self.label_115.setEnabled(True)
        self.label_115.setMinimumSize(QSize(0, 0))
        self.label_115.setMaximumSize(QSize(40, 26))
        self.label_115.setFont(font1)
        self.label_115.setMouseTracking(True)
        self.label_115.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.label_115, 0, 0, 1, 1)

        self.label_17 = QLabel(self.tab_constant_values)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setMinimumSize(QSize(0, 0))
        self.label_17.setMaximumSize(QSize(16777215, 16777215))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_17, 1, 2, 1, 1)

        self.label_113 = QLabel(self.tab_constant_values)
        self.label_113.setObjectName(u"label_113")
        self.label_113.setMinimumSize(QSize(0, 0))
        self.label_113.setMaximumSize(QSize(16777215, 16777215))
        self.label_113.setFont(font)
        self.label_113.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_15.addWidget(self.label_113, 2, 2, 1, 1)

        self.lineEdit_Krx = QLineEdit(self.tab_constant_values)
        self.lineEdit_Krx.setObjectName(u"lineEdit_Krx")
        self.lineEdit_Krx.setEnabled(True)
        self.lineEdit_Krx.setMinimumSize(QSize(0, 0))
        self.lineEdit_Krx.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_Krx.setFont(font)
        self.lineEdit_Krx.setStyleSheet(u"")
        self.lineEdit_Krx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_15.addWidget(self.lineEdit_Krx, 2, 1, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_constant_values, "")
        self.tab_table_values = QWidget()
        self.tab_table_values.setObjectName(u"tab_table_values")
        self.gridLayout_16 = QGridLayout(self.tab_table_values)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(4, 6, 4, 6)
        self.pushButton_load_table_Kryz = QPushButton(self.tab_table_values)
        self.pushButton_load_table_Kryz.setObjectName(u"pushButton_load_table_Kryz")
        self.pushButton_load_table_Kryz.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kryz.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kryz.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kryz.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Kryz.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_load_table_Kryz.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/common/new_file.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_load_table_Kryz.setIcon(icon)
        self.pushButton_load_table_Kryz.setIconSize(QSize(20, 20))

        self.gridLayout_16.addWidget(self.pushButton_load_table_Kryz, 4, 2, 1, 1)

        self.label_117 = QLabel(self.tab_table_values)
        self.label_117.setObjectName(u"label_117")
        self.label_117.setEnabled(True)
        self.label_117.setMinimumSize(QSize(0, 0))
        self.label_117.setMaximumSize(QSize(40, 26))
        self.label_117.setFont(font1)
        self.label_117.setMouseTracking(True)
        self.label_117.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_117, 0, 0, 1, 1)

        self.pushButton_load_table_Krx = QPushButton(self.tab_table_values)
        self.pushButton_load_table_Krx.setObjectName(u"pushButton_load_table_Krx")
        self.pushButton_load_table_Krx.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Krx.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Krx.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Krx.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Krx.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_load_table_Krx.setStyleSheet(u"")
        self.pushButton_load_table_Krx.setIcon(icon)
        self.pushButton_load_table_Krx.setIconSize(QSize(20, 20))

        self.gridLayout_16.addWidget(self.pushButton_load_table_Krx, 3, 2, 1, 1)

        self.lineEdit_Kx_table_path = QLineEdit(self.tab_table_values)
        self.lineEdit_Kx_table_path.setObjectName(u"lineEdit_Kx_table_path")
        self.lineEdit_Kx_table_path.setEnabled(False)
        self.lineEdit_Kx_table_path.setMinimumSize(QSize(0, 26))
        self.lineEdit_Kx_table_path.setMaximumSize(QSize(16777215, 26))
        self.lineEdit_Kx_table_path.setSizeIncrement(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setKerning(True)
        self.lineEdit_Kx_table_path.setFont(font2)
        self.lineEdit_Kx_table_path.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_Kx_table_path.setStyleSheet(u"")
        self.lineEdit_Kx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_Kx_table_path, 0, 1, 1, 1)

        self.pushButton_load_table_Kx = QPushButton(self.tab_table_values)
        self.pushButton_load_table_Kx.setObjectName(u"pushButton_load_table_Kx")
        self.pushButton_load_table_Kx.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kx.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kx.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kx.setMinimumSize(QSize(40, 0))
        self.pushButton_load_table_Kx.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_load_table_Kx.setStyleSheet(u"")
        self.pushButton_load_table_Kx.setIcon(icon)
        self.pushButton_load_table_Kx.setIconSize(QSize(20, 20))

        self.gridLayout_16.addWidget(self.pushButton_load_table_Kx, 0, 2, 1, 1)

        self.lineEdit_Krx_table_path = QLineEdit(self.tab_table_values)
        self.lineEdit_Krx_table_path.setObjectName(u"lineEdit_Krx_table_path")
        self.lineEdit_Krx_table_path.setEnabled(False)
        self.lineEdit_Krx_table_path.setMinimumSize(QSize(0, 26))
        self.lineEdit_Krx_table_path.setMaximumSize(QSize(16777215, 26))
        self.lineEdit_Krx_table_path.setSizeIncrement(QSize(0, 0))
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        self.lineEdit_Krx_table_path.setFont(font3)
        self.lineEdit_Krx_table_path.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_Krx_table_path.setStyleSheet(u"")
        self.lineEdit_Krx_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_Krx_table_path, 3, 1, 1, 1)

        self.label_120 = QLabel(self.tab_table_values)
        self.label_120.setObjectName(u"label_120")
        self.label_120.setEnabled(True)
        self.label_120.setMinimumSize(QSize(0, 0))
        self.label_120.setMaximumSize(QSize(40, 26))
        self.label_120.setFont(font1)
        self.label_120.setMouseTracking(True)
        self.label_120.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_120, 4, 0, 1, 1)

        self.lineEdit_Kryz_table_path = QLineEdit(self.tab_table_values)
        self.lineEdit_Kryz_table_path.setObjectName(u"lineEdit_Kryz_table_path")
        self.lineEdit_Kryz_table_path.setEnabled(False)
        self.lineEdit_Kryz_table_path.setMinimumSize(QSize(0, 26))
        self.lineEdit_Kryz_table_path.setMaximumSize(QSize(16777215, 26))
        self.lineEdit_Kryz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kryz_table_path.setFont(font3)
        self.lineEdit_Kryz_table_path.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_Kryz_table_path.setStyleSheet(u"")
        self.lineEdit_Kryz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_Kryz_table_path, 4, 1, 1, 1)

        self.label_119 = QLabel(self.tab_table_values)
        self.label_119.setObjectName(u"label_119")
        self.label_119.setEnabled(True)
        self.label_119.setMinimumSize(QSize(0, 0))
        self.label_119.setMaximumSize(QSize(40, 26))
        self.label_119.setFont(font1)
        self.label_119.setMouseTracking(True)
        self.label_119.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_119, 3, 0, 1, 1)

        self.lineEdit_Kyz_table_path = QLineEdit(self.tab_table_values)
        self.lineEdit_Kyz_table_path.setObjectName(u"lineEdit_Kyz_table_path")
        self.lineEdit_Kyz_table_path.setEnabled(False)
        self.lineEdit_Kyz_table_path.setMinimumSize(QSize(0, 26))
        self.lineEdit_Kyz_table_path.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_Kyz_table_path.setSizeIncrement(QSize(0, 0))
        self.lineEdit_Kyz_table_path.setFont(font3)
        self.lineEdit_Kyz_table_path.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_Kyz_table_path.setStyleSheet(u"")
        self.lineEdit_Kyz_table_path.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.lineEdit_Kyz_table_path, 2, 1, 1, 1)

        self.label_118 = QLabel(self.tab_table_values)
        self.label_118.setObjectName(u"label_118")
        self.label_118.setEnabled(True)
        self.label_118.setMinimumSize(QSize(0, 0))
        self.label_118.setMaximumSize(QSize(40, 26))
        self.label_118.setFont(font1)
        self.label_118.setMouseTracking(True)
        self.label_118.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_16.addWidget(self.label_118, 2, 0, 1, 1)

        self.pushButton_load_table_Kyz = QPushButton(self.tab_table_values)
        self.pushButton_load_table_Kyz.setObjectName(u"pushButton_load_table_Kyz")
        self.pushButton_load_table_Kyz.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_load_table_Kyz.sizePolicy().hasHeightForWidth())
        self.pushButton_load_table_Kyz.setSizePolicy(sizePolicy)
        self.pushButton_load_table_Kyz.setMinimumSize(QSize(40, 26))
        self.pushButton_load_table_Kyz.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_load_table_Kyz.setStyleSheet(u"")
        self.pushButton_load_table_Kyz.setIcon(icon)
        self.pushButton_load_table_Kyz.setIconSize(QSize(20, 20))

        self.gridLayout_16.addWidget(self.pushButton_load_table_Kyz, 2, 2, 1, 1)

        self.tabWidget_inputs.addTab(self.tab_table_values, "")

        self.gridLayout_14.addWidget(self.tabWidget_inputs, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_bottom_inputs)

        self.verticalSpacer_8 = QSpacerItem(20, 21, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_8)

        QWidget.setTabOrder(self.lineEdit_effective_diameter, self.lineEdit_joint_mass)
        QWidget.setTabOrder(self.lineEdit_joint_mass, self.lineEdit_axial_locking_criteria)
        QWidget.setTabOrder(self.lineEdit_axial_locking_criteria, self.comboBox_axial_stop_rod)
        QWidget.setTabOrder(self.comboBox_axial_stop_rod, self.tabWidget_inputs)
        QWidget.setTabOrder(self.tabWidget_inputs, self.lineEdit_Kx)
        QWidget.setTabOrder(self.lineEdit_Kx, self.lineEdit_Kyz)
        QWidget.setTabOrder(self.lineEdit_Kyz, self.lineEdit_Krx)
        QWidget.setTabOrder(self.lineEdit_Krx, self.lineEdit_Kryz)
        QWidget.setTabOrder(self.lineEdit_Kryz, self.lineEdit_Kx_table_path)
        QWidget.setTabOrder(self.lineEdit_Kx_table_path, self.pushButton_load_table_Kx)
        QWidget.setTabOrder(self.pushButton_load_table_Kx, self.lineEdit_Krx_table_path)
        QWidget.setTabOrder(self.lineEdit_Krx_table_path, self.pushButton_load_table_Krx)
        QWidget.setTabOrder(self.pushButton_load_table_Krx, self.lineEdit_Kryz_table_path)
        QWidget.setTabOrder(self.lineEdit_Kryz_table_path, self.pushButton_load_table_Kryz)

        self.retranslateUi(Form)

        self.comboBox_axial_stop_rod.setCurrentIndex(1)
        self.tabWidget_inputs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"OpenPulse", None))
        self.lineEdit_joint_mass.setText("")
        self.label_axial_lock_criteria.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">Axial locking criteria \u03b5:</span></p></body></html>", None))
        self.label_111.setText(QCoreApplication.translate("Form", u"[kg]", None))
        self.label_102.setText(QCoreApplication.translate("Form", u"Joint mass:", None))
        self.comboBox_axial_stop_rod.setItemText(0, QCoreApplication.translate("Form", u" Not included", None))
        self.comboBox_axial_stop_rod.setItemText(1, QCoreApplication.translate("Form", u" Included", None))

        self.lineEdit_axial_locking_criteria.setText("")
        self.label_109.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">Axial stop rods:</p></body></html>", None))
        self.lineEdit_effective_diameter.setText("")
        self.label_107.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_103.setText(QCoreApplication.translate("Form", u"Effective diameter:", None))
        self.label_116.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">yz</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.lineEdit_Kyz.setText("")
        self.lineEdit_Kx.setText("")
        self.lineEdit_Kryz.setText("")
        self.label_16.setText(QCoreApplication.translate("Form", u"[N/m]", None))
        self.label_93.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">rx</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_112.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">ryz</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_114.setText(QCoreApplication.translate("Form", u"[N.m/rad]", None))
        self.label_115.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">x</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"[N/m]", None))
        self.label_113.setText(QCoreApplication.translate("Form", u"[N.m/rad]", None))
        self.lineEdit_Krx.setText("")
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_constant_values), QCoreApplication.translate("Form", u"Constant values", None))
        self.pushButton_load_table_Kryz.setText("")
        self.label_117.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\"><span style=\" font-weight:400; font-style:normal;\">k</span><span style=\" font-weight:400; font-style:normal; vertical-align:sub;\">x</span><span style=\" font-weight:400; font-style:normal;\">:</span></p></body></html>", None))
        self.pushButton_load_table_Krx.setText("")
        self.pushButton_load_table_Kx.setText("")
        self.label_120.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">ryz</span>:</p></body></html>", None))
        self.label_119.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">rx</span>:</p></body></html>", None))
        self.label_118.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"right\">k<span style=\" vertical-align:sub;\">yz</span>:</p></body></html>", None))
        self.pushButton_load_table_Kyz.setText("")
        self.tabWidget_inputs.setTabText(self.tabWidget_inputs.indexOf(self.tab_table_values), QCoreApplication.translate("Form", u"Table of values", None))
    # retranslateUi



class ExpansionJointWidget_UI(QWidget, Ui_Form):
    """
    Component Hierarchy:
    - Form: QWidget
        - (Layout): QVBoxLayout
                - frame_top_inputs: QFrame
                    - (Layout): QGridLayout
                            - lineEdit_joint_mass: QLineEdit
                            - label_axial_lock_criteria: QLabel
                            - label_111: QLabel
                            - label_102: QLabel
                            - comboBox_axial_stop_rod: QComboBox
                            - lineEdit_axial_locking_criteria: QLineEdit
                            - label_109: QLabel
                            - lineEdit_effective_diameter: QLineEdit
                            - label_107: QLabel
                            - label_103: QLabel
                - frame_bottom_inputs: QFrame
                    - (Layout): QGridLayout
                            - tabWidget_inputs: QTabWidget
                                - tab_constant_values: QWidget
                                    - (Layout): QGridLayout
                                            - label_116: QLabel
                                            - lineEdit_Kyz: QLineEdit
                                            - lineEdit_Kx: QLineEdit
                                            - lineEdit_Kryz: QLineEdit
                                            - label_16: QLabel
                                            - label_93: QLabel
                                            - label_112: QLabel
                                            - label_114: QLabel
                                            - label_115: QLabel
                                            - label_17: QLabel
                                            - label_113: QLabel
                                            - lineEdit_Krx: QLineEdit
                                - tab_table_values: QWidget
                                    - (Layout): QGridLayout
                                            - pushButton_load_table_Kryz: QPushButton
                                            - label_117: QLabel
                                            - pushButton_load_table_Krx: QPushButton
                                            - lineEdit_Kx_table_path: QLineEdit
                                            - pushButton_load_table_Kx: QPushButton
                                            - lineEdit_Krx_table_path: QLineEdit
                                            - label_120: QLabel
                                            - lineEdit_Kryz_table_path: QLineEdit
                                            - label_119: QLabel
                                            - lineEdit_Kyz_table_path: QLineEdit
                                            - label_118: QLabel
                                            - pushButton_load_table_Kyz: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
