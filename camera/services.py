import queue
import struct
import threading
import time
import serial

ser = serial.Serial('COM4', 115200)


class ImageReceiver:
    def __init__(self):
        self.stop_event = threading.Event()
        self.image_queue = queue.Queue()
        self.last_image_time = None

    def receive_images(self):
        while not self.stop_event.is_set():
            try:
                size_data = ser.read(4)
                if len(size_data) == 4:
                    size = struct.unpack("<L", size_data)[0]
                    image_data = ser.read(size)
                    if len(image_data) == size:
                        self.image_queue.put(image_data)
                        self.last_image_time = time.time()
                        print(image_data)
                    else:
                        print("Ошибка при чтении изображения")
                else:
                    print("Ошибка при чтении размера изображения")
            except Exception as e:
                print(f"Ошибка приема изображения: {str(e)}")

    def stop(self):
        self.stop_event.set()

