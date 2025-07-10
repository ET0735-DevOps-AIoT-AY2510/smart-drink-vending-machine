import time
from threading import Thread
import queue
from hal import hal_keypad as keypad
from hal import hal_lcd as LCD
from hal import hal_rfid_reader as rfid_reader
from hal import hal_buzzer as buzzer
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
    g.LCD.lcd_display_string("please tap card", 2)


def rfid_input():
    global last_key_time

    while True:
        card_data = reader.read_id_no_block()
        card_data_string = str(card_data) 

        if card_data_string:  # check if card was tapped
            g.last_key_time = time.time()  # update time to when card is tapped

            accepted_card_data = ["1098490313"]  # placeholder for id

            if card_data_string in accepted_card_data:  # accepted card
                g.LCD.lcd_clear()
                buzzer.beep(0.05, 0.5, 1)
                g.LCD.lcd_display_string("Payment Success", 1)
                time.sleep(5)
            else:
                g.LCD.lcd_clear()  # declined card
                buzzer.beep(0.5, 1, 1)
                g.LCD.lcd_display_string("Card declined,", 1)
                g.LCD.lcd_display_string("please try again", 2)
                time.sleep(5)
                tap_card_lcd_display()
        time.sleep(5)

        return False


if __name__ == "__main__":
    main()
