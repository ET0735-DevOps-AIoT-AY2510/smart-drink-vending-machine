import time
from hal import hal_dc_motor as dc
import variables as g
import F7_monitoring_stocks as f7
from get_drink_by_id import get_drink
from update_drink_stock import update_stock


def main():
    dc.init()

    dispensing_drink(1)


def dispensing_drink(drinkNum):
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Payment Success,", 1))
    g.lcd_queue.put(("dispensing drink", 2))
    dc.set_motor_speed(50)
    time.sleep(2)
    dc.set_motor_speed(0)
    drink = get_drink(drinkNum)
    update_stock(drinkNum, drink['stock_quantity'] - 1)


if __name__ == "__main__":
    main()
