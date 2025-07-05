from threading import Thread, Event
import time
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_ir_sensor as ir_sensor
from hal import hal_keypad as keypad
disable_burglar = False
ledandbuzzer_event = Event()


def main():
    global active, lcd, elapsed, security_prompt, ledandbuzzer_event, disable_burglar
    disable_burglar = True
    active = [1]
    elapsed = time.time()
    security_prompt = True
    servo.init()
    lcd = LCD.lcd()
    ir_sensor.init()
    keypad.init(key_pressed)
    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.daemon = True
    keypad_thread.start()
    security_thread = Thread(target=ledandbuzzer)
    security_thread.start()
    while time.time() - elapsed <= 10 and not ir_sensor.get_ir_sensor_state():
        if (time.time() - elapsed >= 5):
            security_check()
            security_prompt = True
        elif security_prompt and active:
            unlock_door()
            security_prompt = False
    timeout()
    disable_burglar = False


def key_pressed(key):
    if (time.time() - elapsed >= 5):
        active.append(key)


def unlock_door():
    global active
    ledandbuzzer_event.clear()
    servo.set_servo_position(90)
    lcd.lcd_clear()
    lcd.lcd_display_string("Door Unlocked", 1)
    active = []


def security_check():
    global active, lcd, elapsed, security_prompt
    if active:
        elapsed = time.time()
    elif not security_prompt:
        ledandbuzzer_event.set()
        lcd.lcd_clear()
        lcd.lcd_display_string("Still there?", 1)
        lcd.lcd_display_string("Click anything", 2)


def timeout():
    ledandbuzzer_event.clear()
    if (not ir_sensor.get_ir_sensor_state()):
        servo.set_servo_position(0)
    lcd.lcd_clear()
    lcd.lcd_display_string("Locking Door", 1)
    time.sleep(3)


def ledandbuzzer():
    buzzer.init()
    led.init()
    while True:  # Always running, react to event state inside
        if ledandbuzzer_event.is_set():  # Correct: run while event is set
            buzzer.beep(0.5, 0.1, 0)
            led.set_output(1, 1)
            time.sleep(0.1)
            led.set_output(1, 1)
            time.sleep(0.1)
        else:
            led.set_output(1, 0)
            time.sleep(0.1)  # Idle wait if not triggered


if __name__ == '__main__':
    main()
