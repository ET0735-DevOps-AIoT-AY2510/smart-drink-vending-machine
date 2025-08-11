from hal import hal_moisture_sensor as moistSens
import time
from threading import Thread
import variables as g


def main():
    humid_check_thread = Thread(target=getMoist, daemon=True)
    humid_check_thread.start()


def getMoist():  # constantly detect moisture
    while True:
        g.moist = moistSens.read_sensor()
        time.sleep(5)


def monitor_leak():  # send email if moisture detected, display out of order
    if g.moist and g.emailCheckLeak == 0:
        g.send_email(
            subject='Liquid Leakage',
            body_text='Liquid Leakage detected in Vending Machine'
        )
        g.emailCheckLeak = 1
    while g.waiting_for_payment and g.emailCheckLeak:
        time.sleep(1)
    if (g.waiting_for_payment == 0 and not g.out_of_order) and g.emailCheckLeak == True:
        g.storeSelection = []
        g.lcd_queue.put("clear")
        g.lcd_queue.put(("Machine out", 1))
        g.lcd_queue.put(("of order", 2))
        g.out_of_order = True


if __name__ == "__main__":
    main()
