import sensor
import pyb
import ustruct
import image


def init_camera():
    sensor.reset()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time=2000)
    sensor.set_contrast(3)
    sensor.set_gainceiling(16)


pyb.usb_mode('VCP+MSC')
usb = pyb.USB_VCP()
led = pyb.LED(3)
face_cascade = image.HaarCascade("frontalface", stages=25)

while not usb.isconnected():
    led.on()
    pyb.delay(750)
    led.off()
    pyb.delay(750)

led = pyb.LED(2)
init_camera()

while usb.isconnected():
    led.on()
    img = sensor.snapshot()
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    if objects:
        led.off()
        pyb.delay(750)
        led.on()
        img_compress = img.compress()
        usb.send(ustruct.pack("<L", img.size()))
        usb.send(img)

led.off()
