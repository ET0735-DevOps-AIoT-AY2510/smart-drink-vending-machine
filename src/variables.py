from hal import hal_lcd as LCD
import queue
import time

drink_database = {
    1: {"name" : "Coke", "price" : "1.50", "stock" : 4},
    6: {"name" : "Sprite", "price" : "1.50", "stock" : 3},
    13: {"name" : "Lemon Tea", "price" : "1.70", "stock" : 1}
}

storeSelection=[]

temp = 0

check10 = 0
check20 = 0

purchaseCheck = 0

LCD = LCD.lcd()

shared_keypad_queue = queue.Queue()
last_key_time = time.time()

drink = {22: {"name" : "Default", "price" : "NIL", "stock" : 10}}

waiting_for_payment = False

email_address = 'devopsgroup2project@gmail.com'
email_password = 'imks ngdl jfte ksey'