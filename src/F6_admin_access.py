from threading import Thread
import time
from hal import hal_servo as servo
from hal import hal_led as led
from hal import hal_ir_sensor as ir_sensor
import variables as g
from hal import hal_adc as adc


def main(ir_pytest=None, ir_sensor_state=None):
    timeUntilWarning = 10
    min_time = 15
    max_time = 20 * 60  # 1200 seconds (20 minutes)
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

    # In a real scenario, 10 seconds will be changed to 3minutes and 15 seconds
    while time.time() - g.elapsed <= (timeUntilWarning+5) and not get_ir_state():
        if (timeUntilWarning != min_time + (adc.get_adc_value(1) / 1023) * (max_time - min_time) and not g.stillthere_event.is_set()):
            timeUntilWarning = min_time + \
                (adc.get_adc_value(1) / 1023) * (max_time - min_time)
            g.elapsed = time.time()

        # In a real scenario, 5 seconds will be changed to 3minutes
        if (time.time() - g.elapsed >= timeUntilWarning):
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
        elif (time.time() - g.elapsed <= timeUntilWarning):
            remaining = timeUntilWarning - (time.time() - g.elapsed)
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            g.lcd_queue.put((f"{minutes:02d}m {seconds:02d}s", 2))
        time.sleep(1)
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


def unlock_door(security_thread):
    g.stillthere_event.clear()
    servo.set_servo_position(90)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Door Unlocked", 1))
    time.sleep(3)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(("Warning in:", 1))
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
