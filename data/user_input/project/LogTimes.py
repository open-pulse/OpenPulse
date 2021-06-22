from PyQt5.QtWidgets import QLineEdit, QDialog, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic

class LogTimes(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Analysis/runAnalysisInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.project = project

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        self.label_message.setWordWrap(True)
        self.config_title_font()
        self.config_message_font()
        self.run()
        # self.show()
        self.exec_()

    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:black")

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        # font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("color:blue")
    
    def run(self):

        text = "Solution finished!\n\n"
        # text += "Time to check all entries: {} [s]\n".format(round(self.project.time_to_checking_entries, 6))
        text += "Time to load/create the project: {} [s]\n".format(round(self.project.time_to_load_or_create_project, 6))
        text += "Time to process cross-sections: {} [s]\n".format(round(self.project.time_to_process_cross_sections, 6))
        text += "Time elapsed in pre-processing: {} [s]\n".format(round(self.project.time_to_preprocess_model, 6))
        text += "Time to solve the model: {} [s]\n".format(round(self.project.time_to_solve_model, 6))
        text += "Time elapsed in post-processing: {} [s]\n\n".format(round(self.project.time_to_postprocess, 6))
        text += "Total time elapsed: {} [s]\n\n\n".format(round(self.project.total_time, 6))

        text += "Press ESC to continue..."
        self.label_message.setText(text)
        # self.label_message.setText(f"<font color='blue'>{text}<>")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()