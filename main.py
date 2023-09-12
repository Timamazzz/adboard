import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import time
import threading
from camera.services import ImageReceiver
import cv2 as cv

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
                if (self.image_receiver.last_image_time - time.time()) >= 0:
                    image_data = self.image_receiver.image_queue.get()
                    if not self.is_show_ad:
                        self.predict_gender(image_data)
                        print("Starting operation...")
                        time.sleep(10)
                        print("Operation completed.")
                        self.image_receiver.image_queue.task_done()
                    else:
                        self.image_receiver.image_queue.task_done()
            else:
                time.sleep(1)

    def predict_gender(self, image_data):
        genderProto = "models/gender_deploy.prototxt"
        genderModel = "models/gender_net.caffemodel"
        genderNet = cv.dnn.readNet(genderModel, genderProto)

        genderList = ['Male', 'Female']

        blob = cv.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]

        return "Gender : {}".format(gender)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
