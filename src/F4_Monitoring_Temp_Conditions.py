import time
from hal import hal_lcd as LCD
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from threading import Thread
import smtplib
from email.message import EmailMessage

global temp
temp=0

check10=0
check20=0
purchaseCheck=0

email_address = 'devopsgroup2project@gmail.com'
email_password = 'imks ngdl jfte ksey'

def main():
    led.init()
    temp_humid.init()

    temp_check_thread=Thread(target=tempGet)
    temp_check_thread.start()
    temp_Monitor_thread=Thread(target=temp_Monitor)
    temp_Monitor_thread.start()

def tempGet(): #constantly gets temp through thread in main
    global temp
    while True:
        temp, _ =temp_humid.read_temp_humidity()
        time.sleep(2) #prevent lag?

def temp_Monitor():
    global check10, check20, purchaseCheck
    waiting_for_payment = False
    while True:
        if temp>=10 and check10 == 0: #only emails staff
            msg = email_content(10)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)

            check10=1

        elif temp >= 20 and check20 == 0: #emails staff, blinks led at 2 Hz
            msg = email_content(20)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)

            if purchaseCheck == 0:
                LCD.lcd_clear()
                LCD.lcd_display_string("Machine out", 1)
                LCD.lcd_display_string("of order", 2)
                
                if temp >= 20:
                    led.set_output(24,10)
                    time.sleep(0.5)
                    led.set_output(24,0)
                    time.sleep(0.5)

            else:
                waiting_for_payment = True
                print("placeholder")

            check20 = 1
            check10 = 1

        else:
            waiting_for_payment = False
            check10=0
            check20=0

def email_content(whatMsg): #defining email content
    msg = EmailMessage()
    msg['Subject'] = 'Irregular Temperature in Vending Machine '
    msg['From'] = email_address
    msg['To'] = 'nathanchew2007@gmail.com'

    if whatMsg==20:
        msg.set_content('Temperature is above 20 degrees celsius, Machine is Disabled')

    elif whatMsg==10:
        msg.set_content('Temperature is above 10 degrees celsius')

    return msg

if __name__ == "__main__":
    main()
