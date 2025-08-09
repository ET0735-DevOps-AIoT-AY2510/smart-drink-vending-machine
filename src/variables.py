import sys
from get_drink_by_id import get_all_emails
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from hal import hal_moisture_sensor as moistSens
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from hal import hal_usonic as us
from threading import Thread, Event
import time
import queue
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (4056, 3040)},
    lores={"size": (320, 240)},
    display="lores"
)
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

escape = False
qr_declined = True
card_declined = True
selection = 0

f6_test_flag_1 = None
f6_test_flag_2 = None
f6_test_flag_3 = None
f8_test_flag_1 = None
f8_test_flag_2 = None

stillthere = True
LCD = LCD.lcd()
elapsed = time.time()
security_prompt = True
stillthere_event = Event()
BurglarState = False  # False means F8 is active

storeSelection = []

temp = 0
moist = False

out_of_order = False

check10 = 0
check20 = 0

purchaseCheck = 0
emailCheckLeak = 0

shared_keypad_queue = queue.Queue()
lcd_queue = queue.Queue()

last_key_time = time.time()

waiting_for_payment = False

sender_email = 'devopsgroup2project@gmail.com'
sender_password = 'imks ngdl jfte ksey'

card_data_string = 0
stock = 0


def ledBlink():
    while not BurglarState:
        if waiting_for_payment == 0:
            led.set_output(24, 1)
            time.sleep(0.2)
            led.set_output(24, 0)
            time.sleep(0.2)
        else:
            time.sleep(0.1)
            print(2)


def stillthere_func():
    while stillthere_event.is_set():  # run while event is set
        if 'pytest' not in sys.modules:
            buzzer.beep(0.5, 1, 1)
        else:
            time.sleep(1)


def key_pressed(key):  # puts key into queue
    global last_key_time, stillthere
    if (time.time() - elapsed >= 5) and BurglarState and out_of_order:
        stillthere = True
    elif not BurglarState and not stillthere_event.is_set():
        last_key_time = time.time()
        shared_keypad_queue.put(key)


def send_email(subject, body_text, image_path=None):
    for receiver_email in get_all_emails():
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        if image_path:  # Image provided
            image_cid = make_msgid()[1:-1]

            # Add plain and HTML versions
            msg.set_content(body_text)
            msg.add_alternative(f"""\
            <html>
                <body>
                    <p>{body_text}</p>
                    <img src="cid:{image_cid}" alt="Image">
                </body>
            </html>
            """, subtype='html')

            # Attach the image to the HTML part
            with open(image_path, 'rb') as img:
                img_data = img.read()
                img_type = Path(image_path).suffix.replace('.', '')
                msg.get_payload()[1].add_related(
                    img_data, maintype='image', subtype=img_type, cid=f"<{image_cid}>")
        else:  # No image
            msg.set_content(body_text)

        # Send email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            print("Email sent.")
        except Exception as e:
            print(f"Failed to send email: {e}")


dc.init()
buzzer.init()
led.init()
temp_humid.init()
moistSens.init()
ir_sensor.init()
servo.init()
keypad.init(key_pressed)
us.init()
