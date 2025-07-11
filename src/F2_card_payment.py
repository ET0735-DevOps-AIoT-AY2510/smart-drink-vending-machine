import time
from threading import Thread
from hal import hal_rfid_reader as rfid_reader
from hal import hal_buzzer as buzzer
import variables as g
reader = rfid_reader.init()


def main():
    rfid_input_thread = Thread(target=rfid_input, daemon=True)
    rfid_input_thread.start()


def tap_card_lcd_display(drinkNum):
    g.lcd_queue.put("clear")
    g.lcd_queue.put(
        (f"{g.drink_database[drinkNum]['name']} ${g.drink_database[drinkNum]['price']}", 1))
    g.lcd_queue.put(("Please tap card", 2))


def rfid_input():
    card_data_string = 0
    while time.time() - g.last_key_time <= 29:
        card_data = reader.read_id_no_block()
        if card_data:
            card_data_string = str(card_data)
            break

    if card_data_string != 0:  # check if card was tapped
        g.last_key_time = time.time()  # update time to when card is tapped

        accepted_card_data = ["437194800967", "765343767958"]  # card id
        print(card_data_string)
        if card_data_string in accepted_card_data:  # accepted card
            g.card_declined = False
            g.lcd_queue.put("clear")
            buzzer.beep(0.05, 0.5, 1)
            g.lcd_queue.put(("Payment Success", 1))
            card_data_string = 0
            time.sleep(1)
        else:
            g.card_declined = True
            g.lcd_queue.put("clear")  # declined card
            buzzer.beep(0.5, 1, 1)
            g.lcd_queue.put(("Card declined,", 1))
            g.lcd_queue.put(("please try again", 2))
            card_data_string = 0
            time.sleep(1)
    time.sleep(1)


if __name__ == "__main__":
    main()
