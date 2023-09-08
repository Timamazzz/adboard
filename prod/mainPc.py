import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
import time
import threading

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

        self.timer_label = QLabel('Time: 0 sec', self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.timer_label)

        self.start_time = time.time()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.image_receiver = ImageReceiver()
        self.image_receiver_thread = threading.Thread(target=self.image_receiver.receive_images)
        self.image_receiver_thread.start()

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.setText(f'Time: {elapsed_time} sec')


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
