import time
from threading import Thread
from hal import hal_rfid_reader as rfid_reader
from hal import hal_buzzer as buzzer
import variables as g
import queue
from get_drink_by_id import get_drink
reader = rfid_reader.init()


def main():
    rfid_input_thread = Thread(target=rfid_input, daemon=True)
    rfid_input_thread.start()


def tap_card_lcd_display(drinkNum):
    drink = get_drink(drinkNum)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(
        (f"{drink['name']} ${drink['price']:.2f}", 1))
    g.lcd_queue.put(("Please tap card", 2))


def rfid_input(tester=None):
    if tester is None:
        while time.time() - g.last_key_time <= 14.5:
            try:
                if g.shared_keypad_queue.get(block=False) == "*":
                    g.shared_keypad_queue.put("*")
                    break
            except queue.Empty:
                pass
            card_data = reader.read_id_no_block()
            if card_data:
                g.card_data_string = str(card_data)
                break
    elif tester == 1:
        g.card_data_string = "765343767958"
    elif tester == 0:
        g.card_data_string = "1"

    if g.card_data_string != 0:  # check if card was tapped
        g.last_key_time = time.time()  # update time to when card is tapped

        accepted_card_data = ["765343767958"]  # card id
        print(g.card_data_string)
        if g.card_data_string in accepted_card_data:  # accepted card
            g.card_declined = False
            g.lcd_queue.put("clear")
            g.lcd_queue.put(("Payment Success", 1))
            if tester is None:
                buzzer.beep(0.5, 0, 1)
            time.sleep(1)
        else:
            g.card_declined = True
            g.lcd_queue.put("clear")  # declined card
            if tester is None:
                buzzer.beep(1, 1, 1)
            g.lcd_queue.put(("Card declined,", 1))
            g.lcd_queue.put(("please try again", 2))
            time.sleep(1)


if __name__ == "__main__":
    main()
