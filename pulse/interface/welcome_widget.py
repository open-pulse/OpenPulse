
from PySide6.QtCore import QSize, Qt, Signal, QByteArray
from PySide6.QtGui import QFont, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QBoxLayout
from fileboxes import Filebox

from pulse import app, EXAMPLES_DIR, ICON_DIR

import numpy as np
import io
from PIL import Image, ImageDraw, ImageFont

from functools import partial
from pathlib import Path
from PIL import Image


class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = app().main_window
        self.widget_layout = QVBoxLayout(self)
        self.setLayout(self.widget_layout)
        self.setup_image(self.widget_layout)
        self.setup_labels(self.widget_layout)
        self.create_recents_setup()
        self.update_recent_projects()
        self.setup_example_projects(self.widget_layout)

    def setup_image(self, layout):
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(str(ICON_DIR / "logos/openpulse_logo.png")).scaled(350, 350, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        # font = QFont()
        # font.setFamily("Bauhaus 93")
        # image_label.setFont(font)
        # image_label.setText("<html><head/><body><p><span style=\" font-size:72pt; color:#0055ff;\">O</span><span style=\" font-size:72pt; color:#c8c8c8;\">pen</span><span style=\" font-size:72pt; color:#0055ff;\">P</span><span style=\" font-size:72pt; color:#c8c8c8;\">ulse</span></p></body></html>")
        image_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(image_label)
        layout.addStretch()

    def setup_labels(self, layout):
        labels_layout = QHBoxLayout()

        new_item = WelcomeItem("New", QIcon(str(ICON_DIR / "common/new_file.png")))
        new_item.clicked.connect(self.new_project)

        open_item = WelcomeItem("Open", QIcon(str(ICON_DIR / "common/import.png")))
        open_item.clicked.connect(self.open_project)

        labels_layout.addWidget(new_item)
        labels_layout.addWidget(open_item)
        labels_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(labels_layout)
        layout.addStretch()

    def update_recent_projects(self):
        if not self.recents_layout.isEmpty():
            self.remove_all_recent_widgets()
            
        number_of_recent = 5
        recent_paths = app().config.get_recent_files()
        recent_paths = recent_paths[-number_of_recent:]

        for path in recent_paths:
            path = Path(path)
            if not path.exists():
                app().config.remove_path_from_config_file(path)
                continue
            
            thumbnail = None
            icon = None

            with Filebox(path, override=False) as fb:
                if "thumbnail.png" in fb:
                    thumbnail = fb.read("thumbnail.png")

            if thumbnail is not None:
                bytes = io.BytesIO()
                thumbnail.save(bytes, format="PNG")
                bytes_data = bytes.getvalue()
                image = QImage.fromData(QByteArray(bytes_data))
                icon = QIcon(QPixmap.fromImage(image))

            handler = partial(self.main_window.open_project, path)
            item = WelcomeItem(path.stem, icon, False)
            item.setToolTip(str(path))
            item.clicked.connect(handler)
            self.recents_layout.addWidget(item)

        for _ in range(number_of_recent - len(recent_paths)):
            self.recents_layout.addWidget(WelcomeItem())
        
    def create_recents_setup(self):
        self.recent_label = QLabel("Recent Projects", self)
        self.recent_label.setAlignment(Qt.AlignCenter)
        self.widget_layout.addWidget(self.recent_label)

        self.recents_layout = QHBoxLayout()
        self.recents_layout.setAlignment(Qt.AlignCenter)
        self.widget_layout.addLayout(self.recents_layout)
        self.widget_layout.addStretch()

    def setup_example_projects(self, layout: QBoxLayout):
        example_label = QLabel("Example Projects", self)
        example_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_label)

        examples_layout = QHBoxLayout()
        examples_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(examples_layout)
        layout.addStretch()

        # Finds every file that end with ".vibra" in the examples
        # dir and use only the last N of them to show.
        number_of_examples = 5
        example_paths = (EXAMPLES_DIR / "openpulse_files/").glob("*.pulse")
        example_paths = list(example_paths)[:number_of_examples]

        for path in example_paths:
            path = Path(path)
            thumbnail = None
            icon = None

            with Filebox(path, override=False) as fb:
                if "thumbnail.png" in fb:
                    thumbnail = fb.read("thumbnail.png")

            if thumbnail is not None:
                bytes = io.BytesIO()
                thumbnail.save(bytes, format="PNG")
                bytes_data = bytes.getvalue()
                image = QImage.fromData(QByteArray(bytes_data))
                icon = QIcon(QPixmap.fromImage(image))

            handler = partial(self.main_window.open_project, path)
            item = WelcomeItem(path.stem, icon, False)
            item.setToolTip(str(path))
            item.clicked.connect(handler)
            examples_layout.addWidget(item)

        # Complete the remaining with empty items
        # for _ in range(number_of_examples - len(example_paths)):
        #     examples_layout.addWidget(WelcomeItem())
    
    def remove_all_recent_widgets(self):
        widgets = [self.recents_layout.itemAt(item_index).widget() 
                   for item_index in range(self.recents_layout.count())]

        for widget in widgets:
           widget.setParent(None)

    def new_project(self):
        self.main_window.new_project()

    def open_project(self):
        self.main_window.open_project_dialog()


class WelcomeItem(QWidget):
    clicked = Signal()

    def __init__(self, text="", icon=None, should_paint=False):
        super().__init__()

        button = QPushButton(self)
        button.clicked.connect(self.clicked.emit)
        button.setFixedSize(QSize(90, 90))
        button.setIconSize(QSize(80, 80))
        button.should_paint = should_paint 

        if icon is not None:
            button.setIcon(icon)

        font = ImageFont.load_default()
        item_text = self.shorten_text(text, 76, font)                  
                                    
        label = QLabel(item_text)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
    
    def shorten_text(self, text: str, max_width: int, font):
        draw = ImageDraw.Draw(Image.new("RGB", (1,1)))

        if draw.textlength(text, font) <= max_width:
            return text
    
        for i in range(len(text), 0, -1):
            subtext = text[:i] + "..."

            if draw.textlength(subtext, font) <= max_width:
                return subtext


    
