import time
from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from hal import hal_moisture_sensor as moistSens
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
import F1_main_menu as f1
import F4_Monitoring_Temp_Conditions as f4
import F5_Dispensing_Drink as f5
import F6_admin_access as f6
import F8_burglar_detection as f8
import F9_Monitoring_Liquid_Leakage as f9
from picamera2 import Picamera2, Preview
import variables as g  # contains global variables,drink_database and lcd pre-initialised
import LCD_Usage as display


def main():
    dc.init()
    buzzer.init()
    led.init()
    temp_humid.init()
    moistSens.init()
    ir_sensor.init()
    servo.init()
    keypad.init(g.key_pressed)

    lcd_print_thread = Thread(target=display.lcd_print, daemon=True)
    lcd_print_thread.start()
    keypad_thread = Thread(target=keypad.get_key,
                           daemon=True)  # constantly gets key
    keypad_thread.start()
    inactivity_thread = Thread(target=f1.inactivity_check, daemon=True)
    inactivity_thread.start()
    f4.main()
    f8_main_thread = Thread(target=f8.main)
    f8_main_thread.start()
    f9.main()
    main_menu_thread = Thread(target=keypad_press_lcd_display)
    main_menu_thread.start()
    f1.homescreen()
    f4threads = False
    f9threads = False
    while True:
        if not f4threads and g.temp >= 10:
            f4.temp_Monitor()
            ledBlink_thread = Thread(target=f4.ledBlink)
            ledBlink_thread.start()
            f4threads = True
        elif not f9threads and g.moist:
            f9.monitor_leak()
            ledBlinkLeak_thread = Thread(target=f4.ledBlinkLeak, daemon=True)
            ledBlinkLeak_thread.start()
            f9threads = True
        else:
            time.sleep(0.1)


def keypad_press_lcd_display():
    g.waiting_for_payment = False
    g.storeSelection = []
    while True:
        key = g.shared_keypad_queue.get()  # gets key from queue
        keyvalue = str(key)  # convert key int to key string

        if key == "*":  # clear lcd when * is pressed and reset key array
            g.lcd_queue.put("clear")
            f1.homescreen()
            g.storeSelection = []
            g.waiting_for_payment = False
            continue

        if g.waiting_for_payment:
            if key == 1:
                g.lcd_queue.put("clear")
                g.lcd_queue.put(("card", 1))
                time.sleep(5)
                # put card payment here
                f5.dispensing_drink(selection)
                f1.homescreen()
                g.waiting_for_payment = False

            elif key == 2:
                g.lcd_queue.put("clear")
                g.lcd_queue.put(("qr code", 1))
                time.sleep(5)
                # put qr code payment here
                f5.dispensing_drink(selection)
                f1.homescreen()
                g.waiting_for_payment = False

            continue

        if len(g.storeSelection) > 5:  # entered number is greater than admin code
            g.lcd_queue.put("clear")
            g.lcd_queue.put(("Invalid number,", 1))
            g.lcd_queue.put(("please retry", 2))
            time.sleep(5)
            g.lcd_queue.put("clear")
            g.storeSelection = []

        elif key == "#":
            # turn storeSelection array into int variable
            selection = int("".join(g.storeSelection))
            if selection == 12345:
                f6.main()
                g.shared_keypad_queue.put("*")
            elif selection in g.drink_database:  # drink number exists
                drink = g.drink_database[selection]

                if drink["stock"] > 0:  # drink has stock
                    g.lcd_queue.put("clear")
                    g.lcd_queue.put((drink["name"]+" "+drink["price"], 1))
                    g.lcd_queue.put(("1=Card 2=QR Code", 2))
                    g.waiting_for_payment = True
                    g.storeSelection = []

                else:  # drink no stock
                    g.lcd_queue.put(("Drink out", 1))
                    g.lcd_queue.put(("of stock", 2))
                    time.sleep(5)
                    g.lcd_queue.put()
                    g.storeSelection = []

            else:  # drink number doesnt exist
                g.lcd_queue.put(("Invalid, Please", 1))
                g.lcd_queue.put(("try again", 2))
                time.sleep(5)
                g.lcd_queue.put("clear")
                g.storeSelection = []

        else:
            if len(g.storeSelection) < 6:
                g.lcd_queue.put("clear")
                # stores most recent key press into array
                g.storeSelection.append(keyvalue)
                # displays key on lcd (cummulative)
                g.lcd_queue.put(("".join(g.storeSelection), 1))


if __name__ == "__main__":
    main()
