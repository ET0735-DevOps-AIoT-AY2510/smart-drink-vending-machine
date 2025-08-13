from PIL import Image
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
import time
from threading import Thread
import variables as g


SHAKE_THRESHOLD = 0.15


def main(pytest=None, ir_sensor_state=None):
    last_x, last_y, last_z = g.accelerometer.get_3_axis_adjusted()
    if ir_sensor_state is None:
        get_ir_state = ir_sensor.get_ir_sensor_state
    elif callable(ir_sensor_state):
        get_ir_state = ir_sensor_state
    else:
        def get_ir_state(): return ir_sensor_state
    while pytest is None or pytest == 1:

        x, y, z = g.accelerometer.get_3_axis_adjusted()
        delta_x = abs(x - last_x)
        delta_y = abs(y - last_y)
        delta_z = abs(z - last_z)
        if not g.BurglarState and (not get_ir_state() or delta_x > SHAKE_THRESHOLD or delta_y > SHAKE_THRESHOLD or delta_z > SHAKE_THRESHOLD):
            g.stillthere_event.set()
            security_thread = Thread(target=g.stillthere_func)
            security_thread.start()
            camera_thread = Thread(target=camerafeature)
            if pytest is None:
                camera_thread.start()

            while (not g.BurglarState and (not get_ir_state() or delta_x > SHAKE_THRESHOLD or delta_y > SHAKE_THRESHOLD or delta_z > SHAKE_THRESHOLD) and (pytest is None or pytest == 1)) or camera_thread.is_alive():
                current_time = time.time()
                if time.time() - current_time > 2:
                    last_x, last_y, last_z = x, y, z
                # So that it does not keep sending emails and continuously locks the door
                servo.set_servo_position(0)
                time.sleep(0.1)
                x, y, z = g.accelerometer.get_3_axis_adjusted()
                delta_x = abs(x - last_x)
                delta_y = abs(y - last_y)
                delta_z = abs(z - last_z)
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
