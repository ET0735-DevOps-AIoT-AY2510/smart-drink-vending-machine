import time
from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid

import F1_main_menu as f1
import F4_Monitoring_Temp_Conditions as f4
import F5_Dispensing_Drink as f5

import variables as g #contains global variables, and lcd pre-initialised
from get_drink_by_id import get_drink


def main():
    dc.init()
    led.init()
    temp_humid.init()
    keypad.init(f1.key_pressed)

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
    g.storeSelection=[]
    while True:
        key=g.shared_keypad_queue.get() #gets key from queue
        keyvalue= str(key) #convert key int to key string

        if key == "*": #clear lcd when * is pressed and reset key array
            g.LCD.lcd_clear()
            f1.homescreen()
            g.storeSelection=[]
            g.waiting_for_payment=False
            continue

        if g.waiting_for_payment:
            if key == 1:
                g.LCD.lcd_clear()
                g.LCD.lcd_display_string("card", 1)
                time.sleep(5)
                #put card payment here
                f5.dispensing_drink(selection)
                f1.homescreen()
                g.waiting_for_payment = False

            elif key == 2:
                g.LCD.lcd_clear()
                g.LCD.lcd_display_string("qr code", 1)
                time.sleep(5)
                #put qr code payment here
                f5.dispensing_drink(selection)
                f1.homescreen()
                g.waiting_for_payment = False

            continue

        if len(g.storeSelection)>5: #entered number is greater than admin code
            g.LCD.lcd_clear()
            g.LCD.lcd_display_string("Invalid number,",1)
            g.LCD.lcd_display_string("please retry",2)
            time.sleep(5)
            g.LCD.lcd_clear()
            g.storeSelection=[]

        elif key == "#": 
            selection=int("".join(g.storeSelection)) #turn storeSelection array into int variable
            drink = get_drink(selection)
            if drink: #drink number exists
                if drink["stock_quantity"]>0: #drink has stock
                    g.LCD.lcd_clear()
                    g.LCD.lcd_display_string(f"{drink['name']} ${drink['price']:.2f}",1)
                    g.LCD.lcd_display_string("1=Card 2=QR Code",2)
                    g.waiting_for_payment = True

                else: #drink no stock
                    g.LCD.lcd_display_string("Drink out",1)
                    g.LCD.lcd_display_string("of stock",2)
                    time.sleep(5)
                    g.LCD.lcd_clear()
                    g.storeSelection=[]

            else: #drink number doesnt exist
                g.LCD.lcd_display_string("Invalid, Please",1)
                g.LCD.lcd_display_string("try again",2)
                time.sleep(5)
                g.LCD.lcd_clear()
                g.storeSelection=[]

            g.storeSelection=[]   #clears array cuz im lazy to check if i forgot to clear when necessary
            
        else:
            if len(g.storeSelection) < 6:
                g.LCD.lcd_clear()
                g.storeSelection.append(keyvalue) #stores most recent key press into array
                g.LCD.lcd_display_string("".join(g.storeSelection),1) #displays key on lcd (cummulative)

if __name__ == "__main__":
    main()