import time
from threading import Thread
import queue
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
from hal import hal_rfid_reader as rfid_reader
import variables as g
reader = rfid_reader.init()


def main():
    # start threads
    Thread(target=rfid_input).start()  # start RFID checking


def homescreen():
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string("Welcome, please", 1)
    g.LCD.lcd_display_string("select a drink", 2)


def tap_card_lcd_display():
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string(
        f"{g.drink_database[1]['name']} ${g.drink_database[1]['price']}", 1)
    g.LCD.lcd_display_string("Please tap card", 2)


def rfid_input():
    global last_key_time

    while True:
        card_data = reader.read_id_no_block()
        card_data = str(id) 

        if card_data:  # check if card was tapped
            g.last_key_time = time.time()  # update time to when card is tapped

            accepted_card_data = ["1098490313"]  # placeholder for id

            if card_data in accepted_card_data:  # accepted card
                g.LCD.lcd_clear()
                g.LCD.lcd_display_string("Payment Success", 1)
                time.sleep(5)
            else:
                g.LCD.lcd_clear()  # declined card
                g.LCD.lcd_display_string("Card declined,", 1)
                g.LCD.lcd_display_string("please try again", 2)
                time.sleep(5)
                tap_card_lcd_display()
        time.sleep(5)

        return False


if __name__ == "__main__":
    main()
