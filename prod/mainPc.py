import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
import time
import threading
import cv2

from camera.services import ImageReceiver


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main screen PyQt 6')
        self.setStyleSheet("background-color: black;")

        self.layout = QVBoxLayout(self)

        self.label = QLabel('Screen 0', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: white;")
        font = self.label.font()
        font.setPointSize(36)
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        self.is_show_ad = False

        self.image_receiver = ImageReceiver()
        self.image_receiver_thread = threading.Thread(target=self.image_receiver.receive_images)
        self.image_receiver_thread.start()

        self.operation_thread = threading.Thread(target=self.perform_operation)
        self.operation_thread.daemon = True
        self.operation_thread.start()

    def perform_operation(self):
        while True:
            if not self.image_receiver.image_queue.empty():
                image_data = self.image_receiver.image_queue.get()
                if not self.is_show_ad:
                    print("Starting operation...")
                    time.sleep(10)
                    print("Operation completed.")
                    self.image_receiver.image_queue.task_done()
                else:
                    self.image_receiver.image_queue.task_done()
            else:
                time.sleep(1)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
