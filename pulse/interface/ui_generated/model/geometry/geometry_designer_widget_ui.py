# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geometry_designer_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(648, 846)
        Form.setMinimumSize(QSize(0, 0))
        self.select_all_action = QAction(Form)
        self.select_all_action.setObjectName(u"select_all_action")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(420, 0))
        self.scrollArea.setFrameShape(QFrame.Shape.Box)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 642, 794))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.create_structure_frame = QFrame(self.scrollAreaWidgetContents)
        self.create_structure_frame.setObjectName(u"create_structure_frame")
        self.create_structure_frame.setFrameShape(QFrame.Shape.Box)
        self.create_structure_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_6 = QGridLayout(self.create_structure_frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.remove_attach_add_frame = QFrame(self.create_structure_frame)
        self.remove_attach_add_frame.setObjectName(u"remove_attach_add_frame")
        self.remove_attach_add_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.remove_attach_add_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.remove_attach_add_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.delete_button = QPushButton(self.remove_attach_add_frame)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(72, 26))
        self.delete_button.setMaximumSize(QSize(72, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.delete_button.setFont(font)

        self.horizontalLayout.addWidget(self.delete_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.attach_button = QPushButton(self.remove_attach_add_frame)
        self.attach_button.setObjectName(u"attach_button")
        self.attach_button.setMinimumSize(QSize(72, 26))
        self.attach_button.setMaximumSize(QSize(72, 16777215))
        self.attach_button.setFont(font)

        self.horizontalLayout.addWidget(self.attach_button)

        self.add_button = QPushButton(self.remove_attach_add_frame)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setMinimumSize(QSize(72, 26))
        self.add_button.setMaximumSize(QSize(72, 16777215))
        self.add_button.setFont(font)

        self.horizontalLayout.addWidget(self.add_button)


        self.gridLayout_6.addWidget(self.remove_attach_add_frame, 2, 0, 1, 1)

        self.frame_bending_options = QFrame(self.create_structure_frame)
        self.frame_bending_options.setObjectName(u"frame_bending_options")
        self.frame_bending_options.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_bending_options.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_bending_options)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 2, 0, 1, 1)

        self.bending_radius_line_edit = QLineEdit(self.frame_bending_options)
        self.bending_radius_line_edit.setObjectName(u"bending_radius_line_edit")
        self.bending_radius_line_edit.setMinimumSize(QSize(160, 26))
        self.bending_radius_line_edit.setMaximumSize(QSize(160, 26))
        self.bending_radius_line_edit.setFont(font)
        self.bending_radius_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.bending_radius_line_edit.setClearButtonEnabled(True)

        self.gridLayout_5.addWidget(self.bending_radius_line_edit, 2, 2, 1, 1)

        self.bending_type_label = QLabel(self.frame_bending_options)
        self.bending_type_label.setObjectName(u"bending_type_label")
        self.bending_type_label.setMinimumSize(QSize(120, 26))
        self.bending_type_label.setMaximumSize(QSize(120, 26))
        self.bending_type_label.setFont(font)
        self.bending_type_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.bending_type_label, 1, 1, 1, 1)

        self.bending_options_combobox = QComboBox(self.frame_bending_options)
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.addItem("")
        self.bending_options_combobox.setObjectName(u"bending_options_combobox")
        self.bending_options_combobox.setMinimumSize(QSize(160, 26))
        self.bending_options_combobox.setMaximumSize(QSize(160, 26))
        self.bending_options_combobox.setFont(font)

        self.gridLayout_5.addWidget(self.bending_options_combobox, 1, 2, 1, 1)

        self.bending_radius_label = QLabel(self.frame_bending_options)
        self.bending_radius_label.setObjectName(u"bending_radius_label")
        self.bending_radius_label.setMinimumSize(QSize(120, 26))
        self.bending_radius_label.setMaximumSize(QSize(120, 26))
        self.bending_radius_label.setFont(font)
        self.bending_radius_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_5.addWidget(self.bending_radius_label, 2, 1, 1, 1)

        self.bending_radius_unity_label = QLabel(self.frame_bending_options)
        self.bending_radius_unity_label.setObjectName(u"bending_radius_unity_label")
        self.bending_radius_unity_label.setMinimumSize(QSize(50, 0))
        self.bending_radius_unity_label.setMaximumSize(QSize(50, 16777215))
        self.bending_radius_unity_label.setFont(font)

        self.gridLayout_5.addWidget(self.bending_radius_unity_label, 2, 3, 1, 1)

        self.bending_options_label = QLabel(self.frame_bending_options)
        self.bending_options_label.setObjectName(u"bending_options_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.bending_options_label.setFont(font1)
        self.bending_options_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.bending_options_label, 0, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_8, 2, 4, 1, 1)


        self.gridLayout_6.addWidget(self.frame_bending_options, 0, 0, 1, 1)

        self.frame_bounding_box_sizes = QFrame(self.create_structure_frame)
        self.frame_bounding_box_sizes.setObjectName(u"frame_bounding_box_sizes")
        self.frame_bounding_box_sizes.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_bounding_box_sizes.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.frame_bounding_box_sizes)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.unity_y_label = QLabel(self.frame_bounding_box_sizes)
        self.unity_y_label.setObjectName(u"unity_y_label")
        self.unity_y_label.setMinimumSize(QSize(50, 0))
        self.unity_y_label.setMaximumSize(QSize(50, 16777215))
        self.unity_y_label.setFont(font)

        self.gridLayout_10.addWidget(self.unity_y_label, 3, 3, 1, 1)

        self.y_line_edit = QLineEdit(self.frame_bounding_box_sizes)
        self.y_line_edit.setObjectName(u"y_line_edit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_line_edit.sizePolicy().hasHeightForWidth())
        self.y_line_edit.setSizePolicy(sizePolicy)
        self.y_line_edit.setMinimumSize(QSize(160, 26))
        self.y_line_edit.setMaximumSize(QSize(160, 26))
        self.y_line_edit.setFont(font)
        self.y_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.y_line_edit.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.y_line_edit, 3, 2, 1, 1)

        self.x_line_edit = QLineEdit(self.frame_bounding_box_sizes)
        self.x_line_edit.setObjectName(u"x_line_edit")
        sizePolicy.setHeightForWidth(self.x_line_edit.sizePolicy().hasHeightForWidth())
        self.x_line_edit.setSizePolicy(sizePolicy)
        self.x_line_edit.setMinimumSize(QSize(160, 26))
        self.x_line_edit.setMaximumSize(QSize(160, 26))
        self.x_line_edit.setFont(font)
        self.x_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.x_line_edit.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.x_line_edit, 2, 2, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_15, 1, 5, 1, 1)

        self.dx_label = QLabel(self.frame_bounding_box_sizes)
        self.dx_label.setObjectName(u"dx_label")
        self.dx_label.setMinimumSize(QSize(120, 26))
        self.dx_label.setMaximumSize(QSize(120, 26))
        self.dx_label.setFont(font)
        self.dx_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.dx_label, 2, 1, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_14, 1, 0, 1, 1)

        self.sizes_coords_label = QLabel(self.frame_bounding_box_sizes)
        self.sizes_coords_label.setObjectName(u"sizes_coords_label")
        self.sizes_coords_label.setFont(font1)
        self.sizes_coords_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_10.addWidget(self.sizes_coords_label, 0, 2, 1, 1)

        self.length_x_label = QLabel(self.frame_bounding_box_sizes)
        self.length_x_label.setObjectName(u"length_x_label")
        self.length_x_label.setMinimumSize(QSize(50, 0))
        self.length_x_label.setMaximumSize(QSize(50, 16777215))
        self.length_x_label.setFont(font)

        self.gridLayout_10.addWidget(self.length_x_label, 1, 3, 1, 1)

        self.unity_x_label = QLabel(self.frame_bounding_box_sizes)
        self.unity_x_label.setObjectName(u"unity_x_label")
        self.unity_x_label.setMinimumSize(QSize(50, 0))
        self.unity_x_label.setMaximumSize(QSize(50, 16777215))
        self.unity_x_label.setFont(font)

        self.gridLayout_10.addWidget(self.unity_x_label, 2, 3, 1, 1)

        self.invert_y_sign = QPushButton(self.frame_bounding_box_sizes)
        self.invert_y_sign.setObjectName(u"invert_y_sign")
        sizePolicy.setHeightForWidth(self.invert_y_sign.sizePolicy().hasHeightForWidth())
        self.invert_y_sign.setSizePolicy(sizePolicy)
        self.invert_y_sign.setMaximumSize(QSize(40, 16777215))
        self.invert_y_sign.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.invert_y_sign, 3, 5, 1, 1)

        self.unity_z_label = QLabel(self.frame_bounding_box_sizes)
        self.unity_z_label.setObjectName(u"unity_z_label")
        self.unity_z_label.setMinimumSize(QSize(50, 0))
        self.unity_z_label.setMaximumSize(QSize(50, 16777215))
        self.unity_z_label.setFont(font)

        self.gridLayout_10.addWidget(self.unity_z_label, 4, 3, 1, 1)

        self.invert_z_sign = QPushButton(self.frame_bounding_box_sizes)
        self.invert_z_sign.setObjectName(u"invert_z_sign")
        sizePolicy.setHeightForWidth(self.invert_z_sign.sizePolicy().hasHeightForWidth())
        self.invert_z_sign.setSizePolicy(sizePolicy)
        self.invert_z_sign.setMaximumSize(QSize(40, 16777215))
        self.invert_z_sign.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.invert_z_sign, 4, 5, 1, 1)

        self.dy_label = QLabel(self.frame_bounding_box_sizes)
        self.dy_label.setObjectName(u"dy_label")
        self.dy_label.setMinimumSize(QSize(120, 26))
        self.dy_label.setMaximumSize(QSize(120, 26))
        self.dy_label.setFont(font)
        self.dy_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.dy_label, 3, 1, 1, 1)

        self.dx_label_2 = QLabel(self.frame_bounding_box_sizes)
        self.dx_label_2.setObjectName(u"dx_label_2")
        self.dx_label_2.setMinimumSize(QSize(120, 26))
        self.dx_label_2.setMaximumSize(QSize(120, 26))
        self.dx_label_2.setFont(font)
        self.dx_label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.dx_label_2, 1, 1, 1, 1)

        self.z_line_edit = QLineEdit(self.frame_bounding_box_sizes)
        self.z_line_edit.setObjectName(u"z_line_edit")
        sizePolicy.setHeightForWidth(self.z_line_edit.sizePolicy().hasHeightForWidth())
        self.z_line_edit.setSizePolicy(sizePolicy)
        self.z_line_edit.setMinimumSize(QSize(160, 26))
        self.z_line_edit.setMaximumSize(QSize(160, 26))
        self.z_line_edit.setFont(font)
        self.z_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.z_line_edit.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.z_line_edit, 4, 2, 1, 1)

        self.dz_label = QLabel(self.frame_bounding_box_sizes)
        self.dz_label.setObjectName(u"dz_label")
        self.dz_label.setMinimumSize(QSize(120, 26))
        self.dz_label.setMaximumSize(QSize(120, 26))
        self.dz_label.setFont(font)
        self.dz_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_10.addWidget(self.dz_label, 4, 1, 1, 1)

        self.length_line_edit = QLineEdit(self.frame_bounding_box_sizes)
        self.length_line_edit.setObjectName(u"length_line_edit")
        sizePolicy.setHeightForWidth(self.length_line_edit.sizePolicy().hasHeightForWidth())
        self.length_line_edit.setSizePolicy(sizePolicy)
        self.length_line_edit.setMinimumSize(QSize(160, 26))
        self.length_line_edit.setMaximumSize(QSize(160, 26))
        self.length_line_edit.setFont(font)
        self.length_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.length_line_edit.setClearButtonEnabled(True)

        self.gridLayout_10.addWidget(self.length_line_edit, 1, 2, 1, 1)

        self.invert_x_sign = QPushButton(self.frame_bounding_box_sizes)
        self.invert_x_sign.setObjectName(u"invert_x_sign")
        sizePolicy.setHeightForWidth(self.invert_x_sign.sizePolicy().hasHeightForWidth())
        self.invert_x_sign.setSizePolicy(sizePolicy)
        self.invert_x_sign.setMaximumSize(QSize(40, 16777215))
        self.invert_x_sign.setAutoDefault(False)

        self.gridLayout_10.addWidget(self.invert_x_sign, 2, 5, 1, 1)


        self.gridLayout_6.addWidget(self.frame_bounding_box_sizes, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.create_structure_frame, 1, 0, 1, 1)

        self.frame_division_options = QFrame(self.scrollAreaWidgetContents)
        self.frame_division_options.setObjectName(u"frame_division_options")
        self.frame_division_options.setFrameShape(QFrame.Shape.Box)
        self.frame_division_options.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_3 = QGridLayout(self.frame_division_options)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.frame_5 = QFrame(self.frame_division_options)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_3.addWidget(self.frame_5, 3, 2, 1, 1)

        self.frame_3 = QFrame(self.frame_division_options)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_11 = QGridLayout(self.frame_3)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 26))
        self.label_4.setMaximumSize(QSize(120, 26))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_4, 1, 1, 1, 1)

        self.division_combobox = QComboBox(self.frame_3)
        self.division_combobox.addItem("")
        self.division_combobox.addItem("")
        self.division_combobox.addItem("")
        self.division_combobox.setObjectName(u"division_combobox")
        sizePolicy.setHeightForWidth(self.division_combobox.sizePolicy().hasHeightForWidth())
        self.division_combobox.setSizePolicy(sizePolicy)
        self.division_combobox.setMinimumSize(QSize(160, 26))
        self.division_combobox.setMaximumSize(QSize(160, 26))
        self.division_combobox.setFont(font)

        self.gridLayout_11.addWidget(self.division_combobox, 1, 2, 1, 1)

        self.general_options_label_3 = QLabel(self.frame_3)
        self.general_options_label_3.setObjectName(u"general_options_label_3")
        self.general_options_label_3.setFont(font1)
        self.general_options_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_11.addWidget(self.general_options_label_3, 0, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_9, 1, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_10, 1, 4, 1, 1)

        self.unity_x_label_2 = QLabel(self.frame_3)
        self.unity_x_label_2.setObjectName(u"unity_x_label_2")
        self.unity_x_label_2.setMinimumSize(QSize(50, 0))
        self.unity_x_label_2.setMaximumSize(QSize(50, 16777215))
        self.unity_x_label_2.setFont(font)

        self.gridLayout_11.addWidget(self.unity_x_label_2, 1, 3, 1, 1)


        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 3)

        self.options_stack_widget = QStackedWidget(self.frame_division_options)
        self.options_stack_widget.setObjectName(u"options_stack_widget")
        sizePolicy1.setHeightForWidth(self.options_stack_widget.sizePolicy().hasHeightForWidth())
        self.options_stack_widget.setSizePolicy(sizePolicy1)
        self.options_stack_widget.setMinimumSize(QSize(0, 0))
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.horizontalLayout_4 = QHBoxLayout(self.page_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.position_slider_label = QLabel(self.page_9)
        self.position_slider_label.setObjectName(u"position_slider_label")
        self.position_slider_label.setMinimumSize(QSize(72, 0))
        self.position_slider_label.setFont(font)
        self.position_slider_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.position_slider_label)

        self.position_slider = QSlider(self.page_9)
        self.position_slider.setObjectName(u"position_slider")
        self.position_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.position_slider)

        self.position_spinbox = QSpinBox(self.page_9)
        self.position_spinbox.setObjectName(u"position_spinbox")
        self.position_spinbox.setMinimumSize(QSize(0, 26))
        self.position_spinbox.setSizeIncrement(QSize(0, 0))
        self.position_spinbox.setFont(font)
        self.position_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.position_spinbox.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.position_spinbox)

        self.options_stack_widget.addWidget(self.page_9)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.horizontalLayout_6 = QHBoxLayout(self.page_10)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.division_slider_label = QLabel(self.page_10)
        self.division_slider_label.setObjectName(u"division_slider_label")
        self.division_slider_label.setMinimumSize(QSize(72, 0))
        self.division_slider_label.setFont(font)
        self.division_slider_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.division_slider_label)

        self.division_slider = QSlider(self.page_10)
        self.division_slider.setObjectName(u"division_slider")
        self.division_slider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.division_slider)

        self.division_amount_spinbox = QSpinBox(self.page_10)
        self.division_amount_spinbox.setObjectName(u"division_amount_spinbox")
        self.division_amount_spinbox.setMinimumSize(QSize(0, 26))
        self.division_amount_spinbox.setFont(font)
        self.division_amount_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.division_amount_spinbox.setMinimum(1)

        self.horizontalLayout_6.addWidget(self.division_amount_spinbox)

        self.options_stack_widget.addWidget(self.page_10)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout = QGridLayout(self.page_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_18, 2, 4, 1, 1)

        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.selected_point_combo_box = QComboBox(self.page_2)
        self.selected_point_combo_box.addItem("")
        self.selected_point_combo_box.addItem("")
        self.selected_point_combo_box.setObjectName(u"selected_point_combo_box")
        sizePolicy.setHeightForWidth(self.selected_point_combo_box.sizePolicy().hasHeightForWidth())
        self.selected_point_combo_box.setSizePolicy(sizePolicy)
        self.selected_point_combo_box.setMinimumSize(QSize(160, 26))
        self.selected_point_combo_box.setMaximumSize(QSize(160, 26))
        self.selected_point_combo_box.setFont(font)

        self.gridLayout.addWidget(self.selected_point_combo_box, 0, 2, 1, 1)

        self.label_6 = QLabel(self.page_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)

        self.distance_axis_combo_box = QComboBox(self.page_2)
        self.distance_axis_combo_box.addItem("")
        self.distance_axis_combo_box.addItem("")
        self.distance_axis_combo_box.addItem("")
        self.distance_axis_combo_box.addItem("")
        self.distance_axis_combo_box.setObjectName(u"distance_axis_combo_box")
        sizePolicy.setHeightForWidth(self.distance_axis_combo_box.sizePolicy().hasHeightForWidth())
        self.distance_axis_combo_box.setSizePolicy(sizePolicy)
        self.distance_axis_combo_box.setMinimumSize(QSize(160, 26))
        self.distance_axis_combo_box.setMaximumSize(QSize(160, 26))
        self.distance_axis_combo_box.setFont(font)

        self.gridLayout.addWidget(self.distance_axis_combo_box, 1, 2, 1, 1)

        self.unity_division_dx_label_2 = QLabel(self.page_2)
        self.unity_division_dx_label_2.setObjectName(u"unity_division_dx_label_2")
        self.unity_division_dx_label_2.setMinimumSize(QSize(50, 0))
        self.unity_division_dx_label_2.setFont(font)

        self.gridLayout.addWidget(self.unity_division_dx_label_2, 2, 3, 1, 1)

        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)

        self.distance_value_line_edit = QLineEdit(self.page_2)
        self.distance_value_line_edit.setObjectName(u"distance_value_line_edit")
        sizePolicy.setHeightForWidth(self.distance_value_line_edit.sizePolicy().hasHeightForWidth())
        self.distance_value_line_edit.setSizePolicy(sizePolicy)
        self.distance_value_line_edit.setMinimumSize(QSize(160, 26))
        self.distance_value_line_edit.setMaximumSize(QSize(160, 26))
        self.distance_value_line_edit.setFont(font)
        self.distance_value_line_edit.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.distance_value_line_edit, 2, 2, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_19, 2, 0, 1, 1)

        self.options_stack_widget.addWidget(self.page_2)

        self.gridLayout_3.addWidget(self.options_stack_widget, 1, 0, 1, 3)

        self.frame_4 = QFrame(self.frame_division_options)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.apply_division_button = QPushButton(self.frame_4)
        self.apply_division_button.setObjectName(u"apply_division_button")
        self.apply_division_button.setMinimumSize(QSize(72, 26))
        self.apply_division_button.setMaximumSize(QSize(72, 16777215))
        self.apply_division_button.setFont(font)

        self.gridLayout_7.addWidget(self.apply_division_button, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.cancel_division_button = QPushButton(self.frame_4)
        self.cancel_division_button.setObjectName(u"cancel_division_button")
        self.cancel_division_button.setMinimumSize(QSize(72, 26))
        self.cancel_division_button.setMaximumSize(QSize(72, 16777215))
        self.cancel_division_button.setFont(font)

        self.gridLayout_7.addWidget(self.cancel_division_button, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame_4, 2, 0, 1, 3)


        self.gridLayout_4.addWidget(self.frame_division_options, 7, 0, 1, 1)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_8 = QGridLayout(self.frame_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(2, 2, 2, 2)
        self.frame_general_options = QFrame(self.frame_2)
        self.frame_general_options.setObjectName(u"frame_general_options")
        self.frame_general_options.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_general_options.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_general_options)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.unit_label = QLabel(self.frame_general_options)
        self.unit_label.setObjectName(u"unit_label")
        self.unit_label.setMinimumSize(QSize(120, 26))
        self.unit_label.setMaximumSize(QSize(120, 26))
        self.unit_label.setFont(font)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.unit_label, 1, 1, 1, 1)

        self.set_material_button = QPushButton(self.frame_general_options)
        self.set_material_button.setObjectName(u"set_material_button")
        self.set_material_button.setMinimumSize(QSize(160, 26))
        self.set_material_button.setMaximumSize(QSize(160, 26))
        self.set_material_button.setFont(font)

        self.gridLayout_2.addWidget(self.set_material_button, 6, 2, 1, 1)

        self.structure_type_label_2 = QLabel(self.frame_general_options)
        self.structure_type_label_2.setObjectName(u"structure_type_label_2")
        self.structure_type_label_2.setMinimumSize(QSize(120, 26))
        self.structure_type_label_2.setMaximumSize(QSize(120, 26))
        self.structure_type_label_2.setFont(font)
        self.structure_type_label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.structure_type_label_2, 5, 1, 1, 1)

        self.configure_button = QPushButton(self.frame_general_options)
        self.configure_button.setObjectName(u"configure_button")
        self.configure_button.setMinimumSize(QSize(160, 26))
        self.configure_button.setMaximumSize(QSize(160, 26))
        self.configure_button.setFont(font)

        self.gridLayout_2.addWidget(self.configure_button, 5, 2, 1, 1)

        self.bending_radius_unity_label_2 = QLabel(self.frame_general_options)
        self.bending_radius_unity_label_2.setObjectName(u"bending_radius_unity_label_2")
        self.bending_radius_unity_label_2.setMinimumSize(QSize(50, 0))
        self.bending_radius_unity_label_2.setMaximumSize(QSize(50, 16777215))
        self.bending_radius_unity_label_2.setFont(font)

        self.gridLayout_2.addWidget(self.bending_radius_unity_label_2, 1, 3, 1, 1)

        self.structure_type_label = QLabel(self.frame_general_options)
        self.structure_type_label.setObjectName(u"structure_type_label")
        self.structure_type_label.setMinimumSize(QSize(120, 26))
        self.structure_type_label.setMaximumSize(QSize(120, 26))
        self.structure_type_label.setFont(font)
        self.structure_type_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.structure_type_label, 4, 1, 1, 1)

        self.structure_type_label_3 = QLabel(self.frame_general_options)
        self.structure_type_label_3.setObjectName(u"structure_type_label_3")
        self.structure_type_label_3.setMinimumSize(QSize(120, 26))
        self.structure_type_label_3.setMaximumSize(QSize(120, 26))
        self.structure_type_label_3.setFont(font)
        self.structure_type_label_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.structure_type_label_3, 6, 1, 1, 1)

        self.unit_combobox = QComboBox(self.frame_general_options)
        self.unit_combobox.addItem("")
        self.unit_combobox.addItem("")
        self.unit_combobox.addItem("")
        self.unit_combobox.setObjectName(u"unit_combobox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.unit_combobox.sizePolicy().hasHeightForWidth())
        self.unit_combobox.setSizePolicy(sizePolicy2)
        self.unit_combobox.setMinimumSize(QSize(160, 26))
        self.unit_combobox.setMaximumSize(QSize(160, 26))
        self.unit_combobox.setFont(font)

        self.gridLayout_2.addWidget(self.unit_combobox, 1, 2, 1, 1)

        self.general_options_label = QLabel(self.frame_general_options)
        self.general_options_label.setObjectName(u"general_options_label")
        self.general_options_label.setFont(font1)
        self.general_options_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.general_options_label, 0, 2, 1, 1)

        self.structure_combobox = QComboBox(self.frame_general_options)
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.addItem("")
        self.structure_combobox.setObjectName(u"structure_combobox")
        sizePolicy2.setHeightForWidth(self.structure_combobox.sizePolicy().hasHeightForWidth())
        self.structure_combobox.setSizePolicy(sizePolicy2)
        self.structure_combobox.setMinimumSize(QSize(160, 26))
        self.structure_combobox.setMaximumSize(QSize(160, 26))
        self.structure_combobox.setFont(font)

        self.gridLayout_2.addWidget(self.structure_combobox, 4, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)


        self.gridLayout_8.addWidget(self.frame_general_options, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 8, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cancel_button = QPushButton(self.frame)
        self.cancel_button.setObjectName(u"cancel_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy3)
        self.cancel_button.setMinimumSize(QSize(72, 26))
        self.cancel_button.setMaximumSize(QSize(72, 16777215))
        self.cancel_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.cancel_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.finalize_button = QPushButton(self.frame)
        self.finalize_button.setObjectName(u"finalize_button")
        sizePolicy3.setHeightForWidth(self.finalize_button.sizePolicy().hasHeightForWidth())
        self.finalize_button.setSizePolicy(sizePolicy3)
        self.finalize_button.setMinimumSize(QSize(72, 26))
        self.finalize_button.setMaximumSize(QSize(72, 16777215))
        self.finalize_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.finalize_button)


        self.verticalLayout_2.addWidget(self.frame)

        QWidget.setTabOrder(self.unit_combobox, self.structure_combobox)
        QWidget.setTabOrder(self.structure_combobox, self.configure_button)
        QWidget.setTabOrder(self.configure_button, self.set_material_button)
        QWidget.setTabOrder(self.set_material_button, self.bending_options_combobox)
        QWidget.setTabOrder(self.bending_options_combobox, self.bending_radius_line_edit)
        QWidget.setTabOrder(self.bending_radius_line_edit, self.length_line_edit)
        QWidget.setTabOrder(self.length_line_edit, self.x_line_edit)
        QWidget.setTabOrder(self.x_line_edit, self.y_line_edit)
        QWidget.setTabOrder(self.y_line_edit, self.z_line_edit)
        QWidget.setTabOrder(self.z_line_edit, self.delete_button)
        QWidget.setTabOrder(self.delete_button, self.attach_button)
        QWidget.setTabOrder(self.attach_button, self.add_button)
        QWidget.setTabOrder(self.add_button, self.division_combobox)
        QWidget.setTabOrder(self.division_combobox, self.selected_point_combo_box)
        QWidget.setTabOrder(self.selected_point_combo_box, self.distance_axis_combo_box)
        QWidget.setTabOrder(self.distance_axis_combo_box, self.distance_value_line_edit)
        QWidget.setTabOrder(self.distance_value_line_edit, self.cancel_division_button)
        QWidget.setTabOrder(self.cancel_division_button, self.apply_division_button)
        QWidget.setTabOrder(self.apply_division_button, self.cancel_button)
        QWidget.setTabOrder(self.cancel_button, self.finalize_button)
        QWidget.setTabOrder(self.finalize_button, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.position_spinbox)
        QWidget.setTabOrder(self.position_spinbox, self.division_slider)
        QWidget.setTabOrder(self.division_slider, self.position_slider)
        QWidget.setTabOrder(self.position_slider, self.division_amount_spinbox)

        self.retranslateUi(Form)

        self.options_stack_widget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.select_all_action.setText(QCoreApplication.translate("Form", u"Select All", None))
#if QT_CONFIG(shortcut)
        self.select_all_action.setShortcut(QCoreApplication.translate("Form", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.delete_button.setText(QCoreApplication.translate("Form", u"Delete", None))
#if QT_CONFIG(shortcut)
        self.delete_button.setShortcut(QCoreApplication.translate("Form", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.attach_button.setText(QCoreApplication.translate("Form", u"Attach", None))
        self.add_button.setText(QCoreApplication.translate("Form", u"Add", None))
#if QT_CONFIG(shortcut)
        self.add_button.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.bending_type_label.setText(QCoreApplication.translate("Form", u"Bending type:", None))
        self.bending_options_combobox.setItemText(0, QCoreApplication.translate("Form", u"Long Radius", None))
        self.bending_options_combobox.setItemText(1, QCoreApplication.translate("Form", u"Short Radius", None))
        self.bending_options_combobox.setItemText(2, QCoreApplication.translate("Form", u"User-Defined", None))
        self.bending_options_combobox.setItemText(3, QCoreApplication.translate("Form", u"Disabled", None))

        self.bending_radius_label.setText(QCoreApplication.translate("Form", u"Bending radius:", None))
        self.bending_radius_unity_label.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.bending_options_label.setText(QCoreApplication.translate("Form", u"Bending Options", None))
        self.unity_y_label.setText(QCoreApplication.translate("Form", u"[m]", None))
#if QT_CONFIG(tooltip)
        self.y_line_edit.setToolTip(QCoreApplication.translate("Form", u"Defines the structure segment length component along the global Y-axis.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.x_line_edit.setToolTip(QCoreApplication.translate("Form", u"Defines the structure segment length component along the global X-axis.", None))
#endif // QT_CONFIG(tooltip)
        self.dx_label.setText(QCoreApplication.translate("Form", u"Length \u0394X:", None))
        self.sizes_coords_label.setText(QCoreApplication.translate("Form", u"Bounding Box Sizes", None))
        self.length_x_label.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.unity_x_label.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.invert_y_sign.setText(QCoreApplication.translate("Form", u"+/-", None))
        self.unity_z_label.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.invert_z_sign.setText(QCoreApplication.translate("Form", u"+/-", None))
        self.dy_label.setText(QCoreApplication.translate("Form", u"Length \u0394Y:", None))
        self.dx_label_2.setText(QCoreApplication.translate("Form", u"Total length:", None))
#if QT_CONFIG(tooltip)
        self.z_line_edit.setToolTip(QCoreApplication.translate("Form", u"Defines the structure segment length component along the global Z-axis.", None))
#endif // QT_CONFIG(tooltip)
        self.dz_label.setText(QCoreApplication.translate("Form", u"Length \u0394Z:", None))
#if QT_CONFIG(tooltip)
        self.length_line_edit.setToolTip(QCoreApplication.translate("Form", u"Sets the structure segment length along its current trajectory.\n"
"(Active at endpoints only).", None))
#endif // QT_CONFIG(tooltip)
        self.invert_x_sign.setText(QCoreApplication.translate("Form", u"+/-", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Division type:", None))
        self.division_combobox.setItemText(0, QCoreApplication.translate("Form", u"Single Division", None))
        self.division_combobox.setItemText(1, QCoreApplication.translate("Form", u"Multiple Division", None))
        self.division_combobox.setItemText(2, QCoreApplication.translate("Form", u"Distance from Point", None))

        self.general_options_label_3.setText(QCoreApplication.translate("Form", u"Division Options", None))
        self.unity_x_label_2.setText("")
        self.position_slider_label.setText(QCoreApplication.translate("Form", u"Postion [%]:", None))
        self.division_slider_label.setText(QCoreApplication.translate("Form", u"Divisions:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Selected point:", None))
        self.selected_point_combo_box.setItemText(0, QCoreApplication.translate("Form", u"Start point", None))
        self.selected_point_combo_box.setItemText(1, QCoreApplication.translate("Form", u"End point", None))

        self.label_6.setText(QCoreApplication.translate("Form", u"Direction:", None))
        self.distance_axis_combo_box.setItemText(0, QCoreApplication.translate("Form", u" X-axis", None))
        self.distance_axis_combo_box.setItemText(1, QCoreApplication.translate("Form", u" Y-axis", None))
        self.distance_axis_combo_box.setItemText(2, QCoreApplication.translate("Form", u" Z-axis", None))
        self.distance_axis_combo_box.setItemText(3, QCoreApplication.translate("Form", u" Along the line", None))

        self.unity_division_dx_label_2.setText(QCoreApplication.translate("Form", u"[m]", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Distance:", None))
        self.distance_value_line_edit.setText("")
        self.apply_division_button.setText(QCoreApplication.translate("Form", u"Divide", None))
        self.cancel_division_button.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.unit_label.setText(QCoreApplication.translate("Form", u"Unit length:", None))
        self.set_material_button.setText(QCoreApplication.translate("Form", u"Set material", None))
        self.structure_type_label_2.setText(QCoreApplication.translate("Form", u"Structure settings:", None))
        self.configure_button.setText(QCoreApplication.translate("Form", u"Configure", None))
        self.bending_radius_unity_label_2.setText("")
        self.structure_type_label.setText(QCoreApplication.translate("Form", u"Structure type:", None))
        self.structure_type_label_3.setText(QCoreApplication.translate("Form", u"Structure material:", None))
        self.unit_combobox.setItemText(0, QCoreApplication.translate("Form", u"Meter", None))
        self.unit_combobox.setItemText(1, QCoreApplication.translate("Form", u"Millimeter", None))
        self.unit_combobox.setItemText(2, QCoreApplication.translate("Form", u"Inch", None))

        self.general_options_label.setText(QCoreApplication.translate("Form", u"General Options", None))
        self.structure_combobox.setItemText(0, QCoreApplication.translate("Form", u"Pipe", None))
        self.structure_combobox.setItemText(1, QCoreApplication.translate("Form", u"Flange", None))
        self.structure_combobox.setItemText(2, QCoreApplication.translate("Form", u"Reducer", None))
        self.structure_combobox.setItemText(3, QCoreApplication.translate("Form", u"Circular Beam", None))
        self.structure_combobox.setItemText(4, QCoreApplication.translate("Form", u"Rectangular Beam", None))
        self.structure_combobox.setItemText(5, QCoreApplication.translate("Form", u"I-Beam", None))
        self.structure_combobox.setItemText(6, QCoreApplication.translate("Form", u"T-Beam", None))
        self.structure_combobox.setItemText(7, QCoreApplication.translate("Form", u"C-Beam", None))
        self.structure_combobox.setItemText(8, QCoreApplication.translate("Form", u"Expansion Joint", None))
        self.structure_combobox.setItemText(9, QCoreApplication.translate("Form", u"Valve", None))
        self.structure_combobox.setItemText(10, QCoreApplication.translate("Form", u"Point", None))
        self.structure_combobox.setItemText(11, QCoreApplication.translate("Form", u"Rigid Element", None))

        self.cancel_button.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.finalize_button.setText(QCoreApplication.translate("Form", u"Finalize", None))
#if QT_CONFIG(shortcut)
        self.finalize_button.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.finalize_button.setProperty(u"status", QCoreApplication.translate("Form", u"main", None))
    # retranslateUi



class GeometryDesignerWidget_UI(QDialog, Ui_Form):
    """
    Component Hierarchy:
    - Form: QDialog
        - (Layout): QVBoxLayout
                - scrollArea: QScrollArea
                    - scrollAreaWidgetContents: QWidget
                        - (Layout): QGridLayout
                                - create_structure_frame: QFrame
                                    - (Layout): QGridLayout
                                            - remove_attach_add_frame: QFrame
                                                - (Layout): QHBoxLayout
                                                        - delete_button: QPushButton
                                                        - attach_button: QPushButton
                                                        - add_button: QPushButton
                                            - frame_bending_options: QFrame
                                                - (Layout): QGridLayout
                                                        - bending_radius_line_edit: QLineEdit
                                                        - bending_type_label: QLabel
                                                        - bending_options_combobox: QComboBox
                                                        - bending_radius_label: QLabel
                                                        - bending_radius_unity_label: QLabel
                                                        - bending_options_label: QLabel
                                            - frame_bounding_box_sizes: QFrame
                                                - (Layout): QGridLayout
                                                        - unity_y_label: QLabel
                                                        - y_line_edit: QLineEdit
                                                        - x_line_edit: QLineEdit
                                                        - dx_label: QLabel
                                                        - sizes_coords_label: QLabel
                                                        - length_x_label: QLabel
                                                        - unity_x_label: QLabel
                                                        - invert_y_sign: QPushButton
                                                        - unity_z_label: QLabel
                                                        - invert_z_sign: QPushButton
                                                        - dy_label: QLabel
                                                        - dx_label_2: QLabel
                                                        - z_line_edit: QLineEdit
                                                        - dz_label: QLabel
                                                        - length_line_edit: QLineEdit
                                                        - invert_x_sign: QPushButton
                                - frame_division_options: QFrame
                                    - (Layout): QGridLayout
                                            - frame_5: QFrame
                                                - (Layout): QHBoxLayout
                                            - frame_3: QFrame
                                                - (Layout): QGridLayout
                                                        - label_4: QLabel
                                                        - division_combobox: QComboBox
                                                        - general_options_label_3: QLabel
                                                        - unity_x_label_2: QLabel
                                            - options_stack_widget: QStackedWidget
                                                - page_9: QWidget
                                                    - (Layout): QHBoxLayout
                                                            - position_slider_label: QLabel
                                                            - position_slider: QSlider
                                                            - position_spinbox: QSpinBox
                                                - page_10: QWidget
                                                    - (Layout): QHBoxLayout
                                                            - division_slider_label: QLabel
                                                            - division_slider: QSlider
                                                            - division_amount_spinbox: QSpinBox
                                                - page_2: QWidget
                                                    - (Layout): QGridLayout
                                                            - label_3: QLabel
                                                            - selected_point_combo_box: QComboBox
                                                            - label_6: QLabel
                                                            - distance_axis_combo_box: QComboBox
                                                            - unity_division_dx_label_2: QLabel
                                                            - label_5: QLabel
                                                            - distance_value_line_edit: QLineEdit
                                            - frame_4: QFrame
                                                - (Layout): QGridLayout
                                                        - apply_division_button: QPushButton
                                                        - cancel_division_button: QPushButton
                                - frame_2: QFrame
                                    - (Layout): QGridLayout
                                            - frame_general_options: QFrame
                                                - (Layout): QGridLayout
                                                        - unit_label: QLabel
                                                        - set_material_button: QPushButton
                                                        - structure_type_label_2: QLabel
                                                        - configure_button: QPushButton
                                                        - bending_radius_unity_label_2: QLabel
                                                        - structure_type_label: QLabel
                                                        - structure_type_label_3: QLabel
                                                        - unit_combobox: QComboBox
                                                        - general_options_label: QLabel
                                                        - structure_combobox: QComboBox
                - frame: QFrame
                    - (Layout): QHBoxLayout
                            - cancel_button: QPushButton
                            - finalize_button: QPushButton
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
