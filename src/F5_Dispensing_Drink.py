import time
from hal import hal_lcd as LCD
from hal import hal_dc_motor as dc

import F1_main_menu as f1



def main():
    global LCD
    LCD=LCD.lcd()
    dc.init()

    dispensing_drink()

def dispensing_drink():
    LCD.lcd_clear()
    LCD.lcd_display_string("Payment made,", 1)
    LCD.lcd_display_string("dispensing drink", 2)
    dc.set_motor_speed(50)
    time.sleep(2)
    dc.set_motor_speed(0)
    selected_drink=f1.drink
    selected_drink["stock"] -= 1

if __name__ == "__main__":
    main()
