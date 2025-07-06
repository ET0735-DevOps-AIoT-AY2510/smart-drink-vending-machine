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
    g.BurglarState = True
    g.stillthere = True
    g.elapsed = time.time()
    g.security_prompt = True
    servo.init()

    ir_sensor.init()
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key, daemon=True)
    keypad_thread.start()
    security_thread = Thread(target=stillthere_func, daemon=True)
    security_thread.start()
    while time.time() - g.elapsed <= 10 and not ir_sensor.get_ir_sensor_state():
        if (time.time() - g.elapsed >= 5):
            security_check()
            g.security_prompt = True
        elif g.security_prompt and g.stillthere:
            unlock_door()
            g.security_prompt = False
    timeout()
    g.BurglarState = False


def key_pressed(key):
    if (time.time() - g.elapsed >= 5):
        g.stillthere = True


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
    if (not ir_sensor.get_ir_sensor_state()):
        servo.set_servo_position(0)
    g.LCD.lcd_clear()
    g.LCD.lcd_display_string("Locking Door", 1)
    led.set_output(1, 0)
    time.sleep(3)


def stillthere_func():
    buzzer.init()
    led.init()
    while True:  # Always running, react to event state inside
        if g.stillthere_event.is_set():  # Correct: run while event is set
            buzzer.beep(0.5, 0.05, 1)
            led.set_output(1, 1)
            time.sleep(0.05)
            led.set_output(1, 1)
            time.sleep(0.05)


if __name__ == '__main__':
    main()
