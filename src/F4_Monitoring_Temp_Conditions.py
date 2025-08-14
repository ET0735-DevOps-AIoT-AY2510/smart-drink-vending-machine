import time
from threading import Thread
import variables as g
from hal import hal_temp_humidity_sensor as temp_humid


def main():
    temp_check_thread = Thread(target=tempGet, daemon=True)
    temp_check_thread.start()


def tempGet():  # constantly gets temp through thread in main
    while True:
        time.sleep(1)
        g.temp, _ = temp_humid.read_temp_humidity()


def temp_Monitor():

    if g.temp > 20 and g.check20 == 0:  # emails staff, blinks led at 2 Hz
        g.send_email(
            subject='Irregular Temperature in Vending Machine',
            body_text='Temperature is above 20 degrees celsius, Machine is Disabled'
        )

        g.check20 = 1
        g.check10 = 1

    elif g.temp > 10 and g.check10 == 0:  # only emails staff
        g.send_email(
            subject='Irregular Temperature in Vending Machine',
            body_text='Temperature is above 10 degrees celsius'
        )

        g.check10 = 1
    while g.waiting_for_payment and g.check20:
        time.sleep(1)
    if (g.waiting_for_payment == 0 and not g.out_of_order) and g.check20:
        g.storeSelection = []
        g.lcd_queue.put("clear")
        g.lcd_queue.put(("Machine out", 1))
        g.lcd_queue.put(("of order", 2))
        g.out_of_order = True


if __name__ == "__main__":
    main()
