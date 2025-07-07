from hal import hal_lcd as LCD
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


shared_keypad_queue = queue.Queue()
last_key_time = time.time()

drink = {22: {"name": "Default", "price": "NIL", "stock": 10}}

waiting_for_payment = False

sender_email = 'devopsgroup2project@gmail.com'
sender_password = 'imks ngdl jfte ksey'
msg = EmailMessage()


def send_email(receiver_email, subject, body_text, image_path=None):
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
