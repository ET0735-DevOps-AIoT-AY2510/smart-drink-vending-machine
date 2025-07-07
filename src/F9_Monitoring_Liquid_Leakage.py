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

    monitor_leak_thread = Thread(target=monitor_leak, daemon=True)
    monitor_leak_thread.start()
    ledBlinkLeak_thread = Thread(target=ledBlinkLeak, daemon=True)
    ledBlinkLeak_thread.start()
    humid_check_thread = Thread(target=getMoist)
    humid_check_thread.start()


def getMoist():  # constantly detect moisture
    while True:
        g.moist = moistSens.read_sensor()
        time.sleep(5)


def ledBlinkLeak():  # blink if moisture is detected and user isnt interacting
    while True:
        while g.waiting_for_payment == 0:
            if g.moist:
                led.set_output(24, 10)
                time.sleep(0.2)
                led.set_output(24, 0)
                time.sleep(0.2)


def monitor_leak():  # send email if moisture detected, display out of order
    emailCheck = 0
    while True:
        if g.moist and emailCheck == 0:
            g.send_email(
                receiver_email='nathanchew2007@gmail.com',
                subject='Liquid Leakage',
                body_text='Liquid Leakage detected in Vending Machine'
            )
            emailCheck == 1

        if (g.waiting_for_payment == 0 and not g.out_of_order) and g.moist == True:
            g.LCD.lcd_clear()
            g.LCD.lcd_display_string("Machine out", 1)
            g.LCD.lcd_display_string("of order", 2)
            g.out_of_order = True

        elif g.waiting_for_payment == 1:
            g.out_of_order = False


if __name__ == "__main__":
    main()
