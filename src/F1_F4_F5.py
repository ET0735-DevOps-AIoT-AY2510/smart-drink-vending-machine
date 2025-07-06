import time
from threading import Thread
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid

import F1_main_menu as f1
import F4_Monitoring_Temp_Conditions as f4
import F5_Dispensing_Drink as f5

import variables as g


def main():
    dc.init()
    led.init()
    temp_humid.init()

    temp_check_thread=Thread(target=f4.tempGet, daemon = True)
    temp_check_thread.start()
    temp_Monitor_thread=Thread(target=f4.temp_Monitor, daemon = True)
    temp_Monitor_thread.start()
    ledBlink_thread=Thread(target=f4.ledBlink, daemon = True)
    ledBlink_thread.start()
    keypad_thread = Thread(target=keypad.get_key, daemon=True) #constantly gets key
    keypad_thread.start()
    inactivity_thread=Thread(target=f1.inactivity_check, daemon=True)
    inactivity_thread.start()

    f1.homescreen()
    keypad_press_lcd_display()

    


def keypad_press_lcd_display():
    g.waiting_for_payment = False
    storeSelection=[]
    while True:
        key=g.shared_keypad_queue.get() #gets key from queue
        keyvalue= str(key) #convert key int to key string

        if key == "*": #clear lcd when * is pressed and reset key array
            LCD.lcd_clear()
            f1.homescreen()
            storeSelection=[]
            g.waiting_for_payment=False
            continue

        if g.waiting_for_payment:
            if key == 1:
                LCD.lcd_clear()
                LCD.lcd_display_string("card", 1)
                time.sleep(5)
                #put card payment here
                f5.dispensing_drink()
                f1.homescreen()
                g.waiting_for_payment = False

            elif key == 2:
                LCD.lcd_clear()
                LCD.lcd_display_string("qr code", 1)
                time.sleep(5)
                #put qr code payment here
                f5.dispensing_drink()
                f1.homescreen()
                g.waiting_for_payment = False

            continue

        if len(storeSelection)>5: #entered number is greater than admin code
            LCD.lcd_clear()
            LCD.lcd_display_string("Invalid number,",1)
            LCD.lcd_display_string("please retry",2)
            time.sleep(5)
            LCD.lcd_clear()
            storeSelection=[]

        elif key == "#": 
            selection=int("".join(storeSelection)) #turn storeSelection array into int variable

            if selection in f1.drink_database: #drink number exists
                g.drink = f1.drink_database[selection] 

                if g.drink["stock"]>0: #drink has stock
                    LCD.lcd_clear()
                    LCD.lcd_display_string(g.drink["name"]+" "+g.drink["price"],1)
                    LCD.lcd_display_string("1=Card 2=QR Code",2)
                    g.waiting_for_payment = True

                else: #drink no stock
                    LCD.lcd_display_string("Drink out",1)
                    LCD.lcd_display_string("of stock",2)
                    time.sleep(5)
                    LCD.lcd_clear()
                    storeSelection=[]

            else: #drink number doesnt exist
                LCD.lcd_display_string("Invalid, Please",1)
                LCD.lcd_display_string("try again",2)
                time.sleep(5)
                LCD.lcd_clear()
                storeSelection=[]

            storeSelection=[]   #clears array cuz im lazy to check if i forgot to clear when necessary
            
        else:
            if len(storeSelection) < 6:
                LCD.lcd_clear()
                storeSelection.append(keyvalue) #stores most recent key press into array
                LCD.lcd_display_string("".join(storeSelection),1) #displays key on lcd (cummulative)
            