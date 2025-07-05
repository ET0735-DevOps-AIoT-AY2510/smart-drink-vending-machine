import time
from F1_main_menu import homescreen
from threading import Thread
import queue 
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
from hal import hal_rfid_reader as rfid_reader 


shared_keypad_queue = queue.Queue()
global last_key_time
last_key_time=time.time()

drink_database = {
    1: {"name" : "Coke", "price" : "1.50", "stock" : 4},
    6: {"name" : "Sprite", "price" : "1.50", "stock" : 3},
    13: {"name" : "Lemon Tea", "price" : "1.70", "stock" : 1}
}

global drink

def main():
   def main():
    global LCD, drink, last_key_time

    # initialize hardware
    keypad.init(key_input)
    LCD = LCD.lcd()

    #start threads
    Thread(target=keypad.get_key, daemon=True).start()
    Thread(target=check_inactivity, daemon=True).start()
    Thread(target=rfid_input, daemon=True).start()  #start RFID checking


def tap_card_lcd_display(): 
    LCD.lcd_clear 
    LCD.lcd_display_string(f"{drink['name']} ${drink['price']}", 1)
    LCD.lcd_display_string("Tap card on reader", 2)

def check_inactivity(): 
    global last_key_time
    while True:
        if time.time() - last_key_time > 30: 
            homescreen() 
            return 

def key_input(): 
    global last_key_time
    if not shared_keypad_queue.empty():
        key = shared_keypad_queue.get()
        last_key_time = time.time()

        if key == "*": 
            LCD.lcd_clear()
            LCD.lcd_display_string("Returning to", 1)
            LCD.lcd_display_string("payment options", 2)
            time.sleep(2)
            LCD.lcd_clear()
            LCD.lcd_display_string(f"{drink['name']} ${drink['price']}", 1)
            LCD.lcd_display_string("1=Card 2=QR Code", 2)
            return True 
        
    return False 

def rfid_input():
    global last_key_time
    card_data = rfid_reader.read_rfid_card() 

    if card_data: #check if card was tapped
        last_key_time = time.time() #update time to when card is tapped

        if card_data = 
            LCD.lcd_clear()
            LCD.lcd_display_string("Payment Success", 1)
            time.sleep(2)
            tap_card_lcd_display()
        else:
            LCD.lcd_clear()
            LCD.lcd_display_string("Card declined,", 1)
            LCD.lcd_display_string("please try again", 2)
            time.sleep(3)
            tap_card_lcd_display()
        
    return False

if __name__ == "__main__":
    main()