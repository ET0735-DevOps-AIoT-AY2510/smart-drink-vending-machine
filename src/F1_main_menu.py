import time
from threading import Thread
from hal import hal_keypad as keypad
import variables as g



def main():
    keypad.init(key_pressed)

    keypad_thread = Thread(target=keypad.get_key, daemon=True) #constantly gets key
    keypad_thread.start()
    inactivity_thread=Thread(target=inactivity_check, daemon=True)
    inactivity_thread.start()

    homescreen()
    keypad_press_lcd_display()

def key_pressed(key): #puts key into queue
    g.last_key_time=time.time()
    g.shared_keypad_queue.put(key)
    

def inactivity_check():
    while True:
        if time.time() - g.last_key_time > 30:
            homescreen()
            g.last_key_time = time.time() #reset to avoid repeated homescreen calls
        time.sleep(1) #prevent lag?

def homescreen():
    g.LCD.lcd_clear()
    g.storeSelection=[]
    g.LCD.lcd_display_string("Welcome, please", 1)
    g.LCD.lcd_display_string("select a drink", 2)
    
def keypad_press_lcd_display():
    g.waiting_for_payment = False
    g.storeSelection=[]
    while True:
        key=g.shared_keypad_queue.get() #gets key from queue
        keyvalue= str(key) #convert key int to key string

        if key == "*": #clear lcd when * is pressed and reset key array
            g.LCD.lcd_clear()
            homescreen()
            g.storeSelection=[]
            g.waiting_for_payment=False
            continue

        if g.waiting_for_payment:
            if key == 1:
                g.LCD.lcd_clear()
                g.LCD.lcd_display_string("card", 1)
                time.sleep(5)
                #put card payment here
                homescreen()
                g.waiting_for_payment = False

            elif key == 2:
                g.LCD.lcd_clear()
                g.LCD.lcd_display_string("qr code", 1)
                time.sleep(5)
                #put qr code payment here
                homescreen()
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

            if selection in g.drink_database: #drink number exists
                g.drink = g.drink_database[selection] 

                if g.drink["stock"]>0: #drink has stock
                    g.LCD.lcd_clear()
                    g.LCD.lcd_display_string(g.drink["name"]+" "+g.drink["price"],1)
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
