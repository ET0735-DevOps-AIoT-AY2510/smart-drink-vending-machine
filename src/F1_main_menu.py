import time
from threading import Thread
from hal import hal_keypad as keypad
import variables as g
import F6_admin_access as f6
from get_drink_by_id import get_drink, get_all_drink_ids


def main():
    keypad.init(g.key_pressed)

    keypad_thread = Thread(target=keypad.get_key,
                           daemon=True)  # constantly gets key
    keypad_thread.start()
    inactivity_thread = Thread(target=inactivity_check, daemon=True)
    inactivity_thread.start()

    homescreen()
    keypad_press_lcd_display()


def inactivity_check(tester=None):
    while True:
        if time.time() - g.last_key_time > 15 and g.BurglarState == False:
            homescreen()
            g.last_key_time = time.time()
            g.waiting_for_payment = False  # reset to avoid repeated homescreen calls
        time.sleep(1)  # prevent lag?
        if tester is not None:
            break


def homescreen():
    if g.out_of_order:
        g.lcd_queue.put("clear")
        g.storeSelection = []
        g.lcd_queue.put(("Machine out", 1))
        g.lcd_queue.put(("of order", 2))
    else:
        g.lcd_queue.put("clear")
        g.storeSelection = []
        g.lcd_queue.put(("Welcome, please", 1))
        g.lcd_queue.put(("select a drink", 2))


def keypad_press_lcd_display(tester=None):
    while True and (tester == None or tester == 1):
        if tester is not None:
            tester = 2

        key = g.shared_keypad_queue.get()  # gets key from queue
        keyvalue = str(key)  # convert key int to key string

        if key == "*":  # clear lcd when * is pressed and reset key array
            g.lcd_queue.put("clear")
            homescreen()
            g.storeSelection = []
            g.waiting_for_payment = False
            continue

        if g.waiting_for_payment:
            if key == 1:
                g.lcd_queue.put("clear")
                g.lcd_queue.put(("card", 1))
                time.sleep(5)
                # put card payment here
                homescreen()
                g.waiting_for_payment = False

            elif key == 2:
                g.lcd_queue.put("clear")
                g.lcd_queue.put(("qr code", 1))
                time.sleep(5)
                # put qr code payment here
                homescreen()
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
            elif g.selection in get_all_drink_ids():
                drink = get_drink(selection)
                if drink:  # drink number exists
                    if drink["stock_quantity"] > 0:  # drink has stock
                        g.lcd_queue.put("clear")
                        g.lcd_queue.put(
                            (f"{drink['name']} ${drink['price']:.2f}", 1))
                        g.lcd_queue.put(("1=Card 2=QR Code", 2))
                        g.waiting_for_payment = True
                        g.storeSelection = []

                else:  # drink no stock
                    g.lcd_queue.put(("Drink out", 1))
                    g.lcd_queue.put(("of stock", 2))
                    time.sleep(5)
                    g.lcd_queue.put("clear")
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
