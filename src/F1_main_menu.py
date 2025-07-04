import time
import queue
from threading import Thread
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

shared_keypad_queue = queue.Queue()
global last_key_time
last_key_time=time.time()

drink_database = {
    1: {"name" : "Coke", "price" : "1.50", "stock" : 4},
    6: {"name" : "Sprite", "price" : "1.50", "stock" : 3},
    13: {"name" : "Lemon Tea", "price" : "1.70", "stock" : 1}
}


def main():
    keypad.init(key_pressed)
    global LCD
    LCD=LCD.lcd()


    keypad_thread = Thread(target=keypad.get_key, daemon=True) #constantly gets key
    keypad_thread.start()
    inactivity_thread=Thread(target=inactivity_check, daemon=True)
    inactivity_thread.start()

    homescreen()
    keypad_press_lcd_display()

def key_pressed(key): #puts key into queue
    global last_key_time
    last_key_time=time.time()
    shared_keypad_queue.put(key)
    

def inactivity_check():
    global last_key_time
    while True:
        if time.time() - last_key_time > 30:
            homescreen()
            last_key_time = time.time() #reset to avoid repeated homescreen calls
        time.sleep(1) #prevent lag?

def homescreen():
    LCD.lcd_clear()
    LCD.lcd_display_string("Welcome, please", 1)
    LCD.lcd_display_string("select a drink", 2)
    
def keypad_press_lcd_display():
    waiting_for_payment = False
    storeSelection=[]
    while True:
        key=shared_keypad_queue.get() #gets key from queue
        keyvalue= str(key) #convert key int to key string

        if key == "*": #clear lcd when * is pressed and reset key array
            LCD.lcd_clear()
            homescreen()
            storeSelection=[]
            waiting_for_payment=False
            continue

        if waiting_for_payment:
            if key == 1:
                LCD.lcd_clear()
                LCD.lcd_display_string("card", 1)
                time.sleep(5)
                #put card payment here
                homescreen()
                waiting_for_payment = False

            elif key == 2:
                LCD.lcd_clear()
                LCD.lcd_display_string("qr code", 1)
                time.sleep(5)
                #put qr code payment here
                homescreen()
                waiting_for_payment = False

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

            if selection in drink_database: #drink number exists
                drink = drink_database[selection] 

                if drink["stock"]>0: #drink has stock
                    LCD.lcd_clear()
                    LCD.lcd_display_string(drink["name"]+" "+drink["price"],1)
                    LCD.lcd_display_string("1=Card 2=QR Code",2)
                    waiting_for_payment = True

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
            
            
if __name__ == "__main__":
    main()
