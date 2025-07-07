from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from picamera2 import Picamera2, Preview
import time
from threading import Thread, Event
import F6_admin_access as admin
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
import variables as g


def main():
    while True:
        if not g.BurglarState and not ir_sensor.get_ir_sensor_state():
            '''security_thread = Thread(target=g.stillthere_func, daemon=True)
            security_thread.start()'''
            locking_thread = Thread(target=forcedlock, daemon=True)
            locking_thread.start()
            g.stillthere_event.set()
            camerafeature()
            g.send_email(
                receiver_email='terencetngkc2007@gmail.com',
                subject='Image of Burglar',
                body_text='Burglar Detected.',
                image_path='idk.jpg'
            )
        while not g.BurglarState and not ir_sensor.get_ir_sensor_state():
            idk = 5  # So that it does not keep sending emails
        if not g.BurglarState and ir_sensor.get_ir_sensor_state():
            g.stillthere_event.clear()
            g.led.set_output(1, 0)


def forcedlock():
    servo.init()
    while True:
        if g.stillthere_event.is_set():
            servo.set_servo_position(0)


def camerafeature():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920,
                                                                     1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("idk.jpg")
    picam2.stop_preview()
    picam2.close()


if __name__ == '__main__':
    main()
