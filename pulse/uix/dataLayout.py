from PyQt5 import Qt

#Temp
from os.path import expanduser
from PyQt5.QtWidgets import *

class DataLayout(Qt.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.magic = Qt.QWidget()
        self.layout = Qt.QVBoxLayout()
        self.magic.setLayout(self.layout)

        self.tabWidget = Qt.QTabWidget()
        self.tabWidget.addTab(self.magic, "Data")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.hidden)
        self.addWidget(self.tabWidget)
        self.hidden()

    def hidden(self, index = -1):
        self.tabWidget.setTabText(0, "Data")
        self.tabWidget.hide()

    def show(self):
        self.tabWidget.show()

    def clearLayout(self):
        for i in range(self.layout.count()):
            if (type(self.layout.itemAt(i)) == Qt.QHBoxLayout):
                self.layout.clearLayout(self.layout.itemAt(i))
            else:
                self.layout.itemAt(i).widget().close()

    def add_mesh_input(self):
        self.clearLayout()
        self.show()
        self.tabWidget.setTabText(0, "Generate")
        text = Qt.QLineEdit()
        text.setValidator(Qt.QDoubleValidator(text))

        buttons = Qt.QWidget()
        buttons_layout = Qt.QHBoxLayout()
        buttons.setLayout(buttons_layout)
        cancel_button = Qt.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)

        ok_button = Qt.QPushButton("Mesh")
        ok_button.clicked.connect(lambda: self.ok(text.text()))

        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(ok_button)

        label = Qt.QLabel("Insert min value")

        self.layout.addWidget(label)
        self.layout.addWidget(text)
        self.layout.addWidget(buttons)
        space = Qt.QWidget()
        self.layout.addWidget(space, 100)

    def cancel(self):
        self.hidden()

    def ok(self, text):
        print(text)
        print("ok")