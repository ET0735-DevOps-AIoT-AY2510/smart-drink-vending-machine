from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from picamera2 import Picamera2, Preview
import time
from threading import Thread, Event
import F6_admin_access as admin


def main():
    ir_sensor.init()
    servo.init()
    print(admin.disable_burglar)
    if not admin.disable_burglar and not ir_sensor.get_ir_sensor_state():
        security_thread = Thread(target=admin.ledandbuzzer)
        security_thread.daemon = True
        security_thread.start()
        admin.ledandbuzzer_event.set()
        camerafeature()

    while not admin.disable_burglar and not ir_sensor.get_ir_sensor_state():
        servo.set_servo_position(0)

    if not admin.disable_burglar:
        admin.led.set_output(1, 0)


def camerafeature():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920,
                                                                     1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")
    picam2.stop_preview()
    picam2.close()


if __name__ == '__main__':
    main()
