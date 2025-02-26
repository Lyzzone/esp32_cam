import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class VideoCaptureWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ESP32-CAM Video Stream")
        self.setGeometry(100, 100, 240, 350)  # Set window size to 240x240

        # Create a label to display video frames (resize to fit 240x240)
        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 240, 240)  # Fit video label to 240x240

        # Create buttons to start/stop recording
        self.record_button = QPushButton("Start Recording", self)
        self.record_button.setGeometry(10, 250, 220, 40)  # Adjust button size and position
        self.record_button.clicked.connect(self.toggle_recording)
        
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setGeometry(10, 300, 220, 40)  # Adjust button size and position
        self.exit_button.clicked.connect(self.close)

        # Initialize video capture and recording status
        self.cap = cv2.VideoCapture("http://192.168.3.27:5000/video_feed")
        if not self.cap.isOpened():
            print("无法打开视频流")
            sys.exit()
        
        self.is_recording = False
        self.out = None
        self.frame_rate = 20.0  # 每秒帧数
        self.video_filename = "output_video.avi"

        # Set up a timer to fetch frames periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // int(self.frame_rate))

    def update_frame(self):
        # Read a frame from the ESP32-CAM stream
        ret, frame = self.cap.read()
        if not ret:
            print("无法读取帧")
            self.timer.stop()
            return

        # Resize the frame to 240x240 to match screen resolution
        frame_resized = cv2.resize(frame, (240, 240))
        
        # Convert the resized frame to RGB (Qt expects RGB format)
        rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Display the frame in the QLabel
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

        # Save the frame if recording
        if self.is_recording:
            self.out.write(frame_resized)

    def toggle_recording(self):
        # Toggle the recording status
        if not self.is_recording:
            self.is_recording = True
            self.out = cv2.VideoWriter(self.video_filename, cv2.VideoWriter_fourcc(*'XVID'), self.frame_rate, 
                                       (240, 240))  # Save video in 240x240 resolution
            self.record_button.setText("Stop Recording")
            print("开始录制视频")
        else:
            self.is_recording = False
            self.out.release()
            self.record_button.setText("Start Recording")
            print("停止录制视频")

    def closeEvent(self, event):
        # Release resources when closing the application
        if self.is_recording:
            self.out.release()
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCaptureWindow()
    window.show()
    sys.exit(app.exec_())
