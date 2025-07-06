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
sender_email = 'devopsgroup2project@gmail.com'
sender_password = 'imks ngdl jfte ksey'


def main():
    ir_sensor.init()
    while True:
        if not g.BurglarState and not ir_sensor.get_ir_sensor_state():
            security_thread = Thread(target=admin.stillthere_func, daemon=True)
            security_thread.start()
            locking_thread = Thread(target=forcedlock, daemon=True)
            locking_thread.start()
            g.stillthere_event.set()
            camerafeature()
            send_email_with_image(
                receiver_email='terencetngkc2007@gmail.com',
                subject='Image of Burglar',
                body_text='Burglar Detected.',
                image_path='test.jpg'
            )
        while not g.BurglarState and not ir_sensor.get_ir_sensor_state():
            True  # So that it does not keep sending emails
        if not g.BurglarState and ir_sensor.get_ir_sensor_state():
            g.stillthere_event.clear()
            admin.led.set_output(1, 0)


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
    picam2.capture_file("test.jpg")
    picam2.stop_preview()
    picam2.close()


def send_email_with_image(receiver_email, subject, body_text, image_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create a unique Content-ID for the image
    image_cid = make_msgid()[1:-1]  # remove angle brackets

    # Email body with HTML that refers to the image Content-ID
    msg.set_content(body_text)
    msg.add_alternative(f"""\
    <html>
        <body>
            <p>{body_text}</p>
            <img src="cid:{image_cid}" alt="Image">
        </body>
    </html>
    """, subtype='html')

    # Read and attach the image
    with open(image_path, 'rb') as img:
        img_data = img.read()
        img_type = Path(image_path).suffix.replace('.', '')
        msg.get_payload()[1].add_related(
            img_data, maintype='image', subtype=img_type, cid=f"<{image_cid}>")

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email sent with image.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == '__main__':
    main()
