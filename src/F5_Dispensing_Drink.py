import time
from hal import hal_dc_motor as dc
import variables as g
import F7_monitoring_stocks as f7


def main():
    dc.init()

    dispensing_drink(1)


def dispensing_drink(drinkNum):
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Payment made,", 1))
    g.lcd_queue.put(("dispensing drink", 2))
    dc.set_motor_speed(50)
    time.sleep(2)
    dc.set_motor_speed(0)
    g.drink_database[drinkNum]["stock"] -= 1

    if g.drink_database[drinkNum]["stock"] > f7.stock:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
        subject='Vending Machine Jammed',
        body_text='Vending Machine Jammed')
    elif g.drink_database[drinkNum]["stock"] < f7.stock:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
        subject='Extra drink dispensed',
        body_text='Extra drink dispensed')

    g.drink_database[drinkNum]["stock"] = g.stock


if __name__ == "__main__":
    main()
