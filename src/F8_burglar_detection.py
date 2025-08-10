from PIL import Image
import os
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


def main(pytest=None, ir_sensor_state=None):
    if ir_sensor_state is None:
        get_ir_state = ir_sensor.get_ir_sensor_state
    elif callable(ir_sensor_state):
        get_ir_state = ir_sensor_state
    else:
        def get_ir_state(): return ir_sensor_state
    while pytest is None or pytest == 1:
        if not g.BurglarState and not get_ir_state():
            g.stillthere_event.set()
            security_thread = Thread(target=g.stillthere_func)
            security_thread.start()
            camera_thread = Thread(target=camerafeature)
            if pytest is None:
                camera_thread.start()

            while (not g.BurglarState and not get_ir_state() and (pytest is None or pytest == 1)) or camera_thread.is_alive():
                # So that it does not keep sending emails and continuously locks the door
                servo.set_servo_position(0)
                time.sleep(0.1)
                g.f8_test_flag_1 = True
                if pytest is not None:
                    pytest += 1
                    time.sleep(3)
        try:
            if not g.BurglarState and get_ir_state() and security_thread.is_alive():
                g.f8_test_flag_2 = True
                if not camera_thread.is_alive():
                    g.stillthere_event.clear()
                    security_thread.join()
                    g.f8_test_flag_2 = True
        except NameError:
            # security_thread does not exist yet
            pass
        time.sleep(1)
        if pytest is not None:
            pytest += 1


def camerafeature():
    original_path = "burglar_original.jpg"
    resized_path = "burglar.jpg"

    g.picam2.capture_file(original_path)

    # Resize and compress the captured image
    resize_and_compress_image(original_path, resized_path)

    g.send_email(
        subject='Image of Burglar',
        body_text='Burglar Detected.',
        image_path=resized_path
    )


def resize_and_compress_image(input_path, output_path, max_size=(800, 600), quality=70):
    """Resize and compress the image to reduce file size."""
    with Image.open(input_path) as img:
        img.thumbnail(max_size)  # Resize while maintaining aspect ratio
        img.save(output_path, format='JPEG', quality=quality, optimize=True)


if __name__ == '__main__':
    main()
