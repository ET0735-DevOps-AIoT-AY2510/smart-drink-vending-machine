import time
from hal import hal_dc_motor as dc
import variables as g


def main():
    dc.init()

    dispensing_drink(1)

def dispensing_drink(drinkNum):
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string("Payment made,", 1)
    g.LCD.lcd_display_string("dispensing drink", 2)
    dc.set_motor_speed(50)
    time.sleep(2)
    dc.set_motor_speed(0)
    g.drink_database[drinkNum]["stock"] -= 1

if __name__ == "__main__":
    main()
