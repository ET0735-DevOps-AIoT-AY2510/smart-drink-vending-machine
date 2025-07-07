from threading import Thread, Event
import time
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_ir_sensor as ir_sensor
from hal import hal_keypad as keypad
import variables as g


def main():
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = True
    g.elapsed = time.time()
    g.security_prompt = True
    g.waiting_for_payment = True  # So that the other LED functions are disabled
    time.sleep(10)
    '''keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key, daemon=True)
    keypad_thread.start()
    security_thread = Thread(target=g.stillthere_func, daemon=True)
    security_thread.start()'''
    while time.time() - g.elapsed <= 10 and not ir_sensor.get_ir_sensor_state():
        if (time.time() - g.elapsed >= 5):
            security_check()
            g.security_prompt = True
        elif g.security_prompt and g.stillthere:
            unlock_door()
            g.security_prompt = False
    timeout()
    g.BurglarState = False
    g.out_of_order = False
    g.waiting_for_payment = False
    g.emailCheckLeak = 0
    g.check10 = 0
    g.check20 = 0


'''def key_pressed(key):
    if (time.time() - g.elapsed >= 5):
        g.stillthere = True'''


def unlock_door():
    g.stillthere_event.clear()
    servo.set_servo_position(90)
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string("Door Unlocked", 1)
    g.stillthere = False


def security_check():
    if g.stillthere:
        g.elapsed = time.time()
    if not g.security_prompt:
        g.stillthere_event.set()
        g.LCD.lcd_clear()
        g.LCD.lcd_display_string("Still there?", 1)
        g.LCD.lcd_display_string("Click anything", 2)


def timeout():
    g.stillthere_event.clear()
    servo.set_servo_position(0)
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string("Locking Door", 1)
    led.set_output(1, 0)
    time.sleep(3)


if __name__ == '__main__':
    main()
