import time
from hal import hal_lcd as LCD
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from threading import Thread
import smtplib
from email.message import EmailMessage
import variables as g


def main():
    led.init()
    temp_humid.init()

    temp_check_thread=Thread(target=tempGet, daemon = True)
    temp_check_thread.start()
    temp_Monitor_thread=Thread(target=temp_Monitor, daemon = True)
    temp_Monitor_thread.start()
    ledBlink_thread=Thread(target=ledBlink)
    ledBlink_thread.start()

def tempGet(): #constantly gets temp through thread in main
    while True:
        g.temp, _ =temp_humid.read_temp_humidity()
        time.sleep(5) #prevent lag?

def ledBlink():
    while g.purchaseCheck == 0:
        if g.temp >= 20:
            led.set_output(24,10)
            time.sleep(0.2)
            led.set_output(24,0)
            time.sleep(0.2)

def temp_Monitor():
    g.waiting_for_payment = False
    out_of_order = False
    while True:
        if g.temp >= 20 and g.check20 == 0: #emails staff, blinks led at 2 Hz
            msg = email_content(20)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(g.email_address, g.email_password)
                smtp.send_message(msg)


            g.check20 = 1
            g.check10 = 1
        
        elif g.temp>=10 and g.check10 == 0: #only emails staff
            msg = email_content(10)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(g.email_address, g.email_password)
                smtp.send_message(msg)

            g.check10=1

        if g.temp<10:
            g.check10=0

        elif g.temp<20:
            g.waiting_for_payment = False
            g.check20=0

        if (g.purchaseCheck == 0 and not out_of_order) and g.temp>=20:
                LCD.lcd_clear()
                LCD.lcd_display_string("Machine out", 1)
                LCD.lcd_display_string("of order", 2)
                out_of_order = True
                g.waiting_for_payment = True

        elif g.purchaseCheck == 1:
            out_of_order = False


def email_content(whatMsg): #defining email content
    msg = EmailMessage()
    msg['Subject'] = 'Irregular Temperature in Vending Machine '
    msg['From'] = g.email_address
    msg['To'] = 'nathanchew2007@gmail.com'

    if whatMsg==20:
        msg.set_content('Temperature is above 20 degrees celsius, Machine is Disabled')

    elif whatMsg==10:
        msg.set_content('Temperature is above 10 degrees celsius')

    return msg

if __name__ == "__main__":
    main()
