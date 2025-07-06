from hal import hal_moisture_sensor as moistSens
from hal import hal_led as led
import time
from threading import Thread
import smtplib
from email.message import EmailMessage
import variables as g

def main():
    led.init()
    moistSens.init()

    humid_check_thread = Thread(target = getMoist, daemon = True)
    humid_check_thread.start()
    ledBlinkLeak_thread = Thread(target = ledBlinkLeak, daemon = True)
    ledBlinkLeak_thread.start()
    monitor_leak_thread = Thread(target = monitor_leak)
    monitor_leak_thread.start()

def getMoist(): #constantly detect moisture
    while True:
        g.moist = moistSens.read_sensor()
        time.sleep(5)

def ledBlinkLeak(): #blink if moisture is detected and user isnt interacting
    while g.waiting_for_payment == 0:
        if g.moist:
            led.set_output(24,10)
            time.sleep(0.2)
            led.set_output(24,0)
            time.sleep(0.2)

def monitor_leak(): #send email if moisture detected, display out of order
    if g.moist:
        msg = EmailMessage()
        msg['Subject'] = 'Liquid Leakage'
        msg['From'] = g.email_address
        msg['To'] = 'nathanchew2007@gmail.com'
        msg.set_content('Liquid Leakage detected in Vending Machine')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(g.email_address, g.email_password)
            smtp.send_message(msg)

    if (g.waiting_for_payment == 0 and not g.out_of_order) and g.moist == True:
        g.LCD.lcd_clear()
        g.LCD.lcd_display_string("Machine out", 1)
        g.LCD.lcd_display_string("of order", 2)
        g.out_of_order = True

    elif g.waiting_for_payment == 1:
        g.out_of_order = False


