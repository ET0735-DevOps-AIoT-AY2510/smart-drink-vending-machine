import time
from threading import Thread
from hal import hal_keypad as keypad
from hal import hal_dc_motor as dc
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp_humid
from hal import hal_moisture_sensor as moistSens
from hal import hal_ir_sensor as ir_sensor
from hal import hal_servo as servo
from hal import hal_buzzer as buzzer
from hal import hal_usonic as us
import F1_main_menu as f1
import F2_card_payment as f2
import F4_Monitoring_Temp_Conditions as f4
import F5_Dispensing_Drink as f5
import F6_admin_access as f6
import F7_monitoring_stocks as f7
import F8_burglar_detection as f8
import F9_Monitoring_Liquid_Leakage as f9
from picamera2 import Picamera2, Preview
import variables as g  # contains global variables, and lcd pre-initialised
from get_drink_by_id import get_drink
import LCD_Usage as display
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


def main():
    dc.init()
    buzzer.init()
    led.init()
    temp_humid.init()
    moistSens.init()
    ir_sensor.init()
    servo.init()
    keypad.init(g.key_pressed)
    us.init()

    lcd_print_thread = Thread(target=display.lcd_print, daemon=True)
    lcd_print_thread.start()
    keypad_thread = Thread(target=keypad.get_key,
                           daemon=True)  # constantly gets key
    keypad_thread.start()
    inactivity_thread = Thread(target=f1.inactivity_check, daemon=True)
    inactivity_thread.start()
    f4.main()
    f8_main_thread = Thread(target=f8.main)
    # f8_main_thread.start()
    f9.main()
    main_menu_thread = Thread(target=keypad_press_lcd_display)
    main_menu_thread.start()
    f1.homescreen()
    while True:
        if not g.check10 and g.temp >= 10:
            f4.temp_Monitor()
        elif not g.check20 and g.temp >= 20:
            ledBlink_thread = Thread(target=g.ledBlink, daemon=True)
            ledBlink_thread.start()
            f4.temp_Monitor()
        elif not g.emailCheckLeak and g.moist:
            ledBlink_thread = Thread(target=g.ledBlink, daemon=True)
            ledBlink_thread.start()
            f9.monitor_leak()
        else:
            time.sleep(1)


def keypad_press_lcd_display():
    g.waiting_for_payment = False
    g.storeSelection = []
    while True:
        key = g.shared_keypad_queue.get()  # gets key from queue
        keyvalue = str(key)  # convert key int to key string

        if key == "*":  # clear lcd when * is pressed and reset key array
            f1.homescreen()
            g.storeSelection = []
            g.waiting_for_payment = False
            continue

        if g.waiting_for_payment:
            if key == 1:
                f2.tap_card_lcd_display(g.selection)
                f2.rfid_input()
                if g.card_data_string != 0:
                    if g.card_declined == False:
                        f5.dispensing_drink(g.selection)
                        f7.remaining_stock(g.selection)
                        f1.homescreen()
                        g.card_data_string = 0
                        g.waiting_for_payment = False
                        g.card_declined = True
                    else:
                        drink = get_drink(g.selection)
                        g.lcd_queue.put("clear")
                        g.lcd_queue.put(
                            (f"{drink['name']} ${drink['price']:.2f}", 1))
                        g.lcd_queue.put(("1=Card 2=QR Code", 2))
                        g.card_data_string = 0
                    time.sleep(1)

            elif key == 2:
                g.lcd_queue.put("clear")
                g.lcd_queue.put(("qr code", 1))
                time.sleep(5)
                # put qr code payment here
                f5.dispensing_drink(g.selection)
                f7.remaining_stock(g.selection)
                g.waiting_for_payment = False
                time.sleep(1)

            continue

        if len(g.storeSelection) > 5:  # entered number is greater than admin code
            g.lcd_queue.put("clear")
            g.lcd_queue.put(("Invalid number,", 1))
            g.lcd_queue.put(("please retry", 2))
            time.sleep(5)
            g.lcd_queue.put("clear")
            g.storeSelection = []

        elif key == "#":
            # turn storeSelection array into int variable
            if g.storeSelection:
                g.selection = int("".join(g.storeSelection))
                if g.selection == 12345:
                    f6.main()
                    g.shared_keypad_queue.put("*")
                elif g.out_of_order:
                    g.lcd_queue.put("clear")
                    g.lcd_queue.put(("Drink Purchase", 1))
                    g.lcd_queue.put(("is suspended", 2))
                    time.sleep(5)
                    g.lcd_queue.put("clear")
                    g.storeSelection = []
                    g.lcd_queue.put(("Machine out", 1))
                    g.lcd_queue.put(("of order", 2))
                else:
                    drink = get_drink(g.selection)
                    if drink:  # drink number exists
                        if drink["stock_quantity"] > 0:  # drink has stock
                            g.lcd_queue.put("clear")
                            g.lcd_queue.put(
                                (f"{drink['name']} ${drink['price']:.2f}", 1))
                            g.lcd_queue.put(("1=Card 2=QR Code", 2))
                            g.waiting_for_payment = True
                            g.storeSelection = []

                    else:  # drink no stock
                        g.lcd_queue.put("clear")
                        g.lcd_queue.put(("Drink out", 1))
                        g.lcd_queue.put(("of stock", 2))
                        time.sleep(5)
                        g.lcd_queue.put("clear")
                        g.storeSelection = []

                else:  # drink number doesnt exist
                    g.lcd_queue.put("clear")
                    g.lcd_queue.put(("Invalid, Please", 1))
                    g.lcd_queue.put(("try again", 2))
                    time.sleep(5)
                    g.lcd_queue.put("clear")
                    g.storeSelection = []
            else:
                g.picam2.capture_file("barcodeforadmin.jpg")
                image_path = 'barcodeforadmin.jpg'
                img = cv2.imread(image_path)

                try:
                    if img is None:
                        print(f"Image not found: {image_path}")
                    else:
                        img = resize_for_speed(img, max_dim=640)
                        decoded_objects = align_and_decode(img)
                except Exception as e:
                    print(f"Error in thread: {e}")
                    decoded_objects = []

                code_data_list = []

                if decoded_objects:
                    print(f"Found {len(decoded_objects)} code(s):\n")
                    for obj in decoded_objects:
                        code_type = obj.type
                        code_data = obj.data.decode('utf-8')
                        code_data_list.append({
                            'type': code_type,
                            'data': code_data,
                            'position': obj.rect
                        })

                        print(f"Type: {code_type}")
                        print(f"Data: {code_data}")
                        print(f"Bounding Box: {obj.rect}\n")
                else:
                    print("No barcode or QR code found.")

        else:
            if len(g.storeSelection) < 6:
                g.lcd_queue.put("clear")
                # stores most recent key press into array
                g.storeSelection.append(keyvalue)
                # displays key on lcd (cummulative)
                g.lcd_queue.put(("".join(g.storeSelection), 1))


def resize_for_speed(img, max_dim=800):
    h, w = img.shape[:2]
    scale = max_dim / max(h, w) if max(h, w) > max_dim else 1.0
    if scale < 1.0:
        img = cv2.resize(img, (int(w * scale), int(h * scale)),
                         interpolation=cv2.INTER_AREA)
    return img

# Decode wrapper


def decode_image(img):
    return decode(img)

# Rotation utility


def rotate_image(image, angle):
    if angle % 90 == 0:
        if angle == 0:
            return image
        elif angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        (h, w) = image.shape[:2]
        centre = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(centre, angle, 1.0)
        return cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_NEAREST)

# Parallel orientation check


def try_all_orientations_parallel(image):
    base_angles = [0, 90, 180, 270]
    extra_angles = [45, 135]
    angles = base_angles + extra_angles
    flips = [None, 1]  # No flip, horizontal flip

    tasks = []
    for flip_code in flips:
        flipped = image if flip_code is None else cv2.flip(image, flip_code)
        for angle in angles:
            tasks.append((flipped, angle))

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(decode_image, rotate_image(
            img, angle)): (img, angle) for img, angle in tasks}

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    for f in futures:
                        if not f.done():
                            f.cancel()
                    return result
            except Exception:
                pass

    return []

# Alignment + Preprocessing + Decoding


def align_and_decode(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(blurred, 50, 200)
    contours, _ = cv2.findContours(
        edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No contours found")
        return []

    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[-1]
    if angle < -45:
        angle += 90

    (h, w) = img.shape[:2]
    centre = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(centre, angle, 1.0)
    aligned = cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_LINEAR)

    aligned_gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_img = clahe.apply(aligned_gray)

    return try_all_orientations_parallel(contrast_img)


if __name__ == "__main__":
    main()
