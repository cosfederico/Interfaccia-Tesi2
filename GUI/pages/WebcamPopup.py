from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import os
import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer

class WebcamPopup(QDialog):
    
    def __init__(self, parent, cap, action=None):
        super().__init__()
                
        self.parent_window = parent
        self.action = action
        
        self.cap = cap
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        loadUi("GUI/qtdesigner/WebcamPopup.ui", self)
        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.setContentsMargins(20,20,20,20)
        self.setWindowTitle("Calibrazione Webcam")
        self.setWindowIcon(QIcon(os.path.join('GUI', 'icons','webcam.png')))
        
        self.update_frame()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1e3/self.fps))  # Update every 30 ms
            
    def ok_button_clicked(self):
        if self.action is not None:
            self.action()
        self.close()
        
    def update_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # Convert to QImage
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Display the image on the label
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))