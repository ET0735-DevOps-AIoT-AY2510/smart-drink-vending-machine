import time
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from threading import Thread
import smtplib
from email.message import EmailMessage
import variables as g


def main():
    temp_check_thread = Thread(target=tempGet, daemon=True)
    temp_check_thread.start()
    temp_Monitor_thread = Thread(target=temp_Monitor, daemon=True)
    temp_Monitor_thread.start()
    ledBlink_thread = Thread(target=ledBlink)
    ledBlink_thread.start()


def tempGet():  # constantly gets temp through thread in main
    while True:
        g.temp = 5


def ledBlink():
    while True:
        if g.temp >= 20 and g.waiting_for_payment == 0:
            led.set_output(24, 10)
            time.sleep(0.2)
            led.set_output(24, 0)
            time.sleep(0.2)


def temp_Monitor():
    while True:
        if g.temp >= 20 and g.check20 == 0:  # emails staff, blinks led at 2 Hz
            g.send_email(
                receiver_email='nathanchew2007@gmail.com',
                subject='Irregular Temperature in Vending Machine',
                body_text='Temperature is above 20 degrees celsius, Machine is Disabled'
            )

            g.check20 = 1
            g.check10 = 1

        elif g.temp >= 10 and g.check10 == 0:  # only emails staff
            g.send_email(
                receiver_email='nathanchew2007@gmail.com',
                subject='Irregular Temperature in Vending Machine',
                body_text='Temperature is above 10 degrees celsius'
            )

            g.check10 = 1

        if g.temp < 10:
            g.check10 = 0

        elif g.temp < 20:
            g.check20 = 0

        if (g.waiting_for_payment == 0 and not g.out_of_order) and g.temp >= 20:
            g.LCD.lcd_clear()
            g.LCD.lcd_display_string("Machine out", 1)
            g.LCD.lcd_display_string("of order", 2)
            g.out_of_order = True


if __name__ == "__main__":
    main()
