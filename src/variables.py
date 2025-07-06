from hal import hal_lcd as LCD
from threading import Thread, Event
import time
stillthere = True
LCD = LCD.lcd()
elapsed = time.time()
security_prompt = True
stillthere_event = Event()
BurglarState = False
