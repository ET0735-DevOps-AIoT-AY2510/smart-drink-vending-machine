import time
import queue
from threading import Thread
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad

shared_keypad_queue = queue.Queue()

drink_database = {
    1: {"name" : "Coke", "price" : "1.50", "stock" : 4},
    6: {"name" : "Sprite", "price" : "1.50", "stock" : 3},
    13: {"name" : "Lemon Tea", "price" : "1.70", "stock" : 1}
}


def main():
    keypad.init(key_pressed)
    LCD=LCD.lcd()


    keypad_thread = Thread(target=keypad.get_key) #constantly gets key
    keypad_thread.start()

    homescreen()
    keypad_press_lcd_display()

def key_pressed(key): #puts key into queue
    global last_key_time
    last_key_time=time.time()
    shared_keypad_queue.put(key)

def homescreen():
    LCD.lcd_clear()
    LCD.lcd_display_string("Welcome, please", 1)
    LCD.lcd_display_string("select a drink", 2)
    
def keypad_press_lcd_display():
    LCD.lcd_clear()
    storeSelection=[]
    while True:
        key=shared_keypad_queue.get() #gets key from queue
        keyvalue= str(key) #convert key int to key string

        if len(storeSelection)>5: #entered number is greater than admin code
            LCD.lcd_clear()
            LCD.lcd_display_string("Invalid number,",1)
            LCD.lcd_display_string("please retry",2)
            time.sleep(3)
            LCD.lcd_clear()
            storeSelection=[]
        elif time.time()- last_key_time > 30:
            homescreen()
            storeSelection=[]

        elif key == "*": #clear lcd when * is pressed and reset key array
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

                else: #drink no stock
                    LCD.lcd_display_string("Drink out",1)
                    LCD.lcd_display_string("of stock",2)
                    time.sleep(3)
                    LCD.lcd_clear()
                    storeSelection=[]

            else: #drink number doesnt exist
                LCD.lcd_display_string("Invalid, Please",1)
                LCD.lcd_display_string("try again",2)
                time.sleep(3)
                LCD.lcd_clear()
                storeSelection=[]

            storeSelection=[]   #clears array cuz im lazy to check if i forgot to clear when necessary
            
        else:
            storeSelection.append(keyvalue) #stores most recent key press into array
            LCD.lcd_display_string("".join(storeSelection),1) #displays key on lcd (cummulative)
            
            
if __name__ == "__main__":
    main()
