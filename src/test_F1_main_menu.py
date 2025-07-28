import F1_main_menu as f1
import queue 
def test_inactivity_check_trigger():
   f1.g.last_key_time = f1.time.time() - 20
   f1.g.BurglarState = False
   f1.g.waiting_for_payment = True
   
   f1.inactivity_check()
   
   assert f1.g.waiting_for_payment == False

def test_inactivity_check_no_trigger():
   f1.g.last_key_time = f1.time.time() - 5
   f1.g.BurglarState = False
   f1.g.waiting_for_payment = True
   
   f1.inactivity_check()
   
   assert f1.g.waiting_for_payment == True

def test_homescreen_normal():
   f1.g.out_of_order = False
   f1.g.storeSelection = [3,5,7]

   f1.homescreen()

   assert f1.g.storeSelection == []

def test_homescreen_OutOfOrder():
   f1.g.out_of_order = True
   f1.g.storeSelection = [7,8,9]

   f1.homescreen()

   assert f1.g.storeSelection == []

def test_keypad_press_lcd_display_Return_Button():
   f1.g.waiting_for_payment = True
   f1.g.storeSelection = [7,8,9]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put("#")

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == False

def test_keypad_press_lcd_display_Card_select():
   f1.g.waiting_for_payment = True
   f1.g.storeSelection = [7,8,9]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put(1)

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == False

   
def test_keypad_press_lcd_display_QRcode_select():
   f1.g.waiting_for_payment = True
   f1.g.storeSelection = [7,8,9]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put(1)

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == False

def test_keypad_press_lcd_display_Drink_Available():
   f1.g.waiting_for_payment = False
   f1.g.storeSelection = [1,3]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put("#")

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == True

def test_keypad_press_lcd_display_Drink_Unavailable():
   f1.g.waiting_for_payment = False
   f1.g.storeSelection = [1,9]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put("#")

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == False

def test_keypad_press_lcd_display_No_Such_Drink():
   f1.g.waiting_for_payment = False
   f1.g.storeSelection = [1,5,4]
   f1.g.shared_keypad_queue = queue.Queue()
   f1.g.shared_keypad_queue.put("#")

   f1.keypad_press_lcd_display()

   assert f1.g.storeSelection == [] and f1.g.waiting_for_payment == False


   