import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.resize(300, 170)
        message = "Aquieudeveriaescreverumamensagemconsideravelementelongaparatestaraestruturadepularlinhasautomáticas."
                        

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.document().setHtml("""
<table width="100%">
    <tr>
        <td><img height="500" src="icons/info1.png"/></td>
        <td style="vertical-align: middle;">Here is some text.</td>
    </tr>
</table>
""")
        self.textBrowser.setText(message)
        self.textBrowser.setAlignment(Qt.AlignCenter)
        self.layout = QGridLayout()
        self.layout.addWidget(self.textBrowser)
        self.setLayout(self.layout)

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())