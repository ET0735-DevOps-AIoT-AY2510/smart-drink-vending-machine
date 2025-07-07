import variables as g
import time
from threading import Thread


def main():
    textGet_thread = Thread(target = textGet, daemon = True)
    textGet_thread.start()
    lcd_print_thread = Thread(target = lcd_print, daemon = True)
    lcd_print_thread.start()

    lcd_print("queue",1)
    lcd_print("hi",2)
    time.sleep(3)
    lcd_print("clear",0)

def textGet():
    while True:
        g.text = g.lcd_queue.get()

def textCheckGet():
    while True:
        time.sleep(0.1)
        g.textCheck=g.lcd_queue.get()

def lcd_print(message, line):
    while True:
        while g.text!=g.textCheck:
            g.lcd_queue.put(message)
            time.sleep(0.1)

        if g.text.strip().lower() == "clear":
            g.LCD.lcd_clear()
        else:
            g.LCD.lcd_display_string(message, line)

if __name__ == "__main__":
    main()
