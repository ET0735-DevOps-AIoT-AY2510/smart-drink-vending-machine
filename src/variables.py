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
text = "hi"
textCheck = "bye"

last_key_time = time.time()

drink = {22: {"name": "Default", "price": "NIL", "stock": 10}}

waiting_for_payment = False

sender_email = 'devopsgroup2project@gmail.com'
sender_password = 'imks ngdl jfte ksey'


def stillthere_func():
    while True:  # Always running, react to event state inside
        if stillthere_event.is_set():  # Correct: run while event is set
            buzzer.beep(0.5, 0.05, 0)
            led.set_output(1, 1)
            time.sleep(0.05)
            led.set_output(1, 0)
            time.sleep(0.05)


def key_pressed(key):  # puts key into queue
    global last_key_time, stillthere
    if out_of_order == False:
        last_key_time = time.time()
        shared_keypad_queue.put(key)
    elif (time.time() - elapsed >= 5) and BurglarState:
        stillthere = True


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
