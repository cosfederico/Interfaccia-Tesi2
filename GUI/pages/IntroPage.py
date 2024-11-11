from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi

import os

class IntroPage(QWidget):
    
    readyClicked = pyqtSignal()
    exitClicked = pyqtSignal()
    
    def __init__(self, parent, title, text, button_text="Avanti", bottom_text="", warning_text="", error_text=""):
        super().__init__()
        self.parent_window = parent
        self.title_str = title
        self.text_str = text
        self.error_text_str = error_text
        self.warning_text_str = warning_text
        self.button_text = button_text
        
        loadUi("GUI/qtdesigner/IntroPage.ui", self)
        self.setContentsMargins(200,50,200,10)
        
        self.title.setText(self.title_str)
        self.text.setText(self.text_str)
        self.text.setWordWrap(True)
        self.bottom_text.setText(bottom_text)
        self.bottom_text.setWordWrap(True)
        self.warning_text.setText(self.warning_text_str)
        self.warning_text.setWordWrap(True)
        self.ready_button.setText(self.button_text)
        self.error_text.setText("")
        
        self.warning_icon.setPixmap(QPixmap.fromImage(QImage(os.path.join('GUI', 'icons', 'warning.png'))).scaledToWidth(self.warning_frame.geometry().width()))
        
        self.checkbox.toggled.connect(self.checkbox_toggled)
        self.ready_button.clicked.connect(self.ready_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)
        
    def checkbox_toggled(self):
        if self.sender().isChecked():
            self.error_text.setText("")
        
    def ready_button_clicked(self):
        if not self.checkbox.isChecked():
            self.error_text.setText(self.error_text_str)
            return
        
        self.readyClicked.emit()
        self.parent_window.next_page()
        self.parent_window.participant.add_answer(self.checkbox.text(), "Si")
        
    def exit_button_clicked(self):
        self.exitClicked.emit()