from threading import Thread, Event
import time
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_ir_sensor as ir_sensor
from hal import hal_keypad as keypad
import variables as g


def main(ir_pytest=None, ir_sensor_state=None):
    if ir_pytest is None:
        g.out_of_order = True
        g.BurglarState = True
        g.stillthere = True
        g.security_prompt = True
        g.waiting_for_payment = True  # So that the other LED functions are disabled
        time.sleep(3)

    security_thread = Thread(target=g.stillthere_func)
    if ir_pytest is None:
        g.elapsed = time.time()

    get_ir_state = ir_sensor.get_ir_sensor_state if ir_sensor_state is None else lambda: ir_sensor_state

    while time.time() - g.elapsed <= 10 and not get_ir_state():
        if (time.time() - g.elapsed >= 5):
            if not g.security_prompt:
                g.stillthere_event.set()
                if ir_pytest is None:
                    security_thread = Thread(target=g.stillthere_func)
                    security_thread.start()
            security_check()
            g.security_prompt = True
            g.f6_test_flag_2 = True
        elif g.security_prompt and g.stillthere:
            unlock_door(security_thread)
            g.security_prompt = False
            g.f6_test_flag_1 = True
    timeout()
    g.last_key_time = time.time()
    g.BurglarState = False
    g.out_of_order = False
    g.waiting_for_payment = False
    g.emailCheckLeak = 0
    g.check10 = 0
    g.check20 = 0
    g.f6_test_flag_3 = True
    if security_thread.is_alive():
        security_thread.join()


'''def key_pressed(key):
    if (time.time() - g.elapsed >= 5):
        g.stillthere = True'''


def unlock_door(security_thread):
    g.stillthere_event.clear()
    servo.set_servo_position(90)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Door Unlocked", 1))
    g.stillthere = False
    if security_thread.is_alive():
        security_thread.join()


def security_check():
    if g.stillthere:
        g.elapsed = time.time()
    if not g.security_prompt:
        g.lcd_queue.put("clear")
        g.lcd_queue.put(("Still there?", 1))


def timeout():
    g.stillthere_event.clear()
    servo.set_servo_position(0)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Locking Door", 1))
    led.set_output(1, 0)
    time.sleep(3)


if __name__ == '__main__':
    main()
