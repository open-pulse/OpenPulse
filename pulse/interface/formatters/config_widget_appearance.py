from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QWidget
from PyQt5.QtCore import Qt

from collections import defaultdict

class ConfigWidgetAppearance:
    def __init__(self, parent, **kwargs):
        super().__init__()

        self.parent = parent
        tool_tip = kwargs.get("tool_tip", False)

        self._initialize()

        if isinstance(parent, (QDialog, QWidget)):
            self._update_widgets_appearance()
            if tool_tip:
                self._config_toolTip()

    def _initialize(self):
        self.list_widgets = (QComboBox, 
                             QDoubleSpinBox, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QSlider, 
                             QSpinBox)

    def _config_toolTip(self):
        self.parent.setStyleSheet("""QToolTip{  color: rgb(100, 100, 100); 
                                                background-color: rgb(240, 240, 240)  }""")

    def find_widgets_recursively(self, input_widget):
        widgets = list()
        for widget in input_widget.children():
            if isinstance(widget, self.list_widgets):
                if widget in widgets:
                    continue
                widgets.append(widget)

            else:
                for w in self.find_widgets_recursively(widget):
                    if w in widgets:
                        continue
                    widgets.append(w)

        return widgets

    def _update_widgets_appearance(self):

        data = defaultdict(list)
        for widget in self.parent.children():
            for _widget in self.find_widgets_recursively(widget):

                if isinstance(_widget, QComboBox):
                    _widget.setCursor(Qt.PointingHandCursor)
                    try:
                        if _widget in data["ComboBox"]:
                            continue
                        data["ComboBox"].append(_widget)
                    except:
                        pass

                elif isinstance(_widget, QDoubleSpinBox):
                    _widget.setCursor(Qt.PointingHandCursor)
                    try:
                        if _widget in data["DoubleSpinBox"]:
                            continue
                        data["DoubleSpinBox"].append(_widget)
                    except:
                        pass

                elif isinstance(_widget, QLabel):
                    if "_path" == _widget.objectName()[-5:]:
                        try:
                            if _widget in data["Label"]:
                                continue
                            data["Label"].append(_widget)
                        except:
                            pass

                elif isinstance(_widget, QLineEdit):
                    _widget.setCursor(Qt.IBeamCursor)
                    try:
                        if _widget in data["LineEdit"]:
                            continue
                        data["LineEdit"].append(_widget)
                    except:
                        pass

                elif isinstance(_widget, QPushButton):
                    _widget.setCursor(Qt.PointingHandCursor)
                    try:
                        if _widget in data["PushButton"]:
                            continue
                        data["PushButton"].append(_widget)
                    except:
                        pass

                elif isinstance(_widget, QSlider):
                    _widget.setCursor(Qt.PointingHandCursor)
                    try:
                        if _widget in data["Slider"]:
                            continue
                        data["Slider"].append(_widget)
                    except:
                        pass

                elif isinstance(_widget, QSpinBox):
                    _widget.setCursor(Qt.PointingHandCursor)
                    try:
                        if _widget in data["SpinBox"]:
                            continue
                        data["SpinBox"].append(_widget)
                    except:
                        pass

        styles = self.get_stylesheets()
        for key, _widgets in data.items():
            try:
                for current_widget in _widgets:
                    current_widget.setStyleSheet(styles[key])
            except:
                pass

    def get_ComboBox_stylesheet(self):
        style = """ QComboBox{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}
                    QComboBox:hover{border-radius: 2px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}
                    QComboBox:disabled{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(100, 100, 100); background-color: rgba(220, 220, 220, 50)}
                """
        return style

    def get_DoubleSpinBox_stylesheet(self):
        style = """ QDoubleSpinBox{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}
                    QDoubleSpinBox:hover{border-radius: 2px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}
                    QDoubleSpinBox:disabled{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(100, 100, 100); background-color: rgba(220, 220, 220, 50)}
                """
        return style

    def get_LineEdit_stylesheet(self):
        style = """ QLineEdit{ color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }
                    QLineEdit:disabled{ color: rgb(150,150, 150); background-color: rgba(220, 220, 220, 50) }
                """
        return style

    def get_highlighted_LineEdit_stylesheet(self, color):
        style = """ QLineEdit{ color: rgb(0, 0, 0); background-color: rgb(250, 250, 250) }
                    QLineEdit:disabled{ color: rgb(150,150, 150); background-color: rgba(220, 220, 220, 50) }
                """
        return style

    def get_PushButton_stylesheet(self):
        style = """ QPushButton{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}
                    QPushButton:hover{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}
                    QPushButton:pressed{border-radius: 6px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(174, 213, 255)}
                    QPushButton:disabled{border-radius: 6px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(150,150, 150); background-color: rgba(220, 220, 220, 50)}
                """
        return style

    def get_SpinBox_stylesheet(self):
        style = """ QSpinBox{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgb(240, 240, 240)}
                    QSpinBox:hover{border-radius: 2px; border-color: rgb(0, 170, 255); border-style: ridge; border-width: 2px; color: rgb(0, 0, 0); background-color: rgba(174, 213, 255, 100)}
                    QSpinBox:disabled{border-radius: 2px; border-color: rgb(150, 150, 150); border-style: ridge; border-width: 0px; color: rgb(100, 100, 100); background-color: rgba(220, 220, 220, 50)}
                """
        return style

    def get_Label_stylesheet(self):
        style = """QLabel{border-radius: 4px; border-color: rgb(100, 100, 100); border-style: solid; border-width: 1px; color: rgb(100, 100, 100); background-color: rgb(255, 255, 255)}
                """
        return style

    def get_LCDNumber_stylesheet(self):
        style = """ QLCDNumber{ color: rgb(255, 255, 255); 
                                border-color: rgb(255, 255, 255); 
                                border-style: solid; 
                                border-radius: 8px; 
                                border-width: 2px; 
                                background-color: rgb(0, 0, 0)}"""
        return style

    def get_stylesheets(self):
        styles = dict()
        styles["ComboBox"] = self.get_ComboBox_stylesheet()
        styles["DoubleSpinBox"] = self.get_DoubleSpinBox_stylesheet()
        styles["Label"] = self.get_Label_stylesheet()
        styles["LineEdit"] = self.get_LineEdit_stylesheet()
        styles["PushButton"] = self.get_PushButton_stylesheet()
        styles["SpinBox"] = self.get_SpinBox_stylesheet()
        return styles