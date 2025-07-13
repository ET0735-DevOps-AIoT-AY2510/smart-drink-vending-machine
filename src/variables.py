from hal import hal_lcd as LCD
from hal import hal_buzzer as buzzer
from hal import hal_led as led
from threading import Thread, Event
import time
import queue
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

card_declined = True
selection = 0

stillthere = True
LCD = LCD.lcd()
elapsed = time.time()
security_prompt = True
stillthere_event = Event()
BurglarState = False

drink_database = {
    1: {"name": "Coke", "price": "1.50", "stock": 4},
    6: {"name": "Sprite", "price": "1.50", "stock": 3},
    13: {"name": "Lemon Tea", "price": "1.70", "stock": 1}
}

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
        buzzer.beep(0.5, 1, 1)


def key_pressed(key):  # puts key into queue
    global last_key_time, stillthere
    if (time.time() - elapsed >= 5) and BurglarState and out_of_order:
        stillthere = True
    elif not BurglarState and not stillthere_event.is_set():
        last_key_time = time.time()
        shared_keypad_queue.put(key)


def send_email(receiver_email, subject, body_text, image_path=None):
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
