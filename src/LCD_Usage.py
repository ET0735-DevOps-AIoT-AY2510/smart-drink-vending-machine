import variables as g
import time
from threading import Thread


def main():
    lcd_print_thread = Thread(target=lcd_print, daemon=True)
    lcd_print_thread.start()

    g.lcd_queue.put("queue", 1)
    g.lcd_queue.put("hi", 2)
    time.sleep(3)
    g.lcd_queue.put("clear")


def lcd_print():
    while True:
        text = g.lcd_queue.get()
        if text.strip().lower() == "clear":
            g.LCD.lcd_clear()
        else:
            g.LCD.lcd_display_string(*text)


if __name__ == "__main__":
    main()
