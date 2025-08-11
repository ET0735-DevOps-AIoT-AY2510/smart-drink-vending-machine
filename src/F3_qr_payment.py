from base64 import decode
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import variables as g
from hal import hal_buzzer as buzzer
import queue
import cv2
from pyzbar.pyzbar import decode
from get_drink_by_id import get_drink


def show_qr_display(drinkNum):
    drink = get_drink(drinkNum)
    g.lcd_queue.put("clear")
    g.lcd_queue.put(
        (f"{drink['name']} ${drink['price']:.2f}", 1))
    g.lcd_queue.put(("Show QR Code", 2))


def camera_input():
    for i in range(3):
        try:
            if g.shared_keypad_queue.get(block=False) == "*":
                g.shared_keypad_queue.put("*")
                g.escape = True
                break
        except queue.Empty:
            pass
        g.picam2.capture_file("successfulpayment.jpg")
        image_path = 'successfulpayment.jpg'
        img = cv2.imread(image_path)

        try:
            if img is None:  # For debugging
                print(f"Image not found: {image_path}")
            else:
                img = resize_for_speed(img, max_dim=800)
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
            code_data = None
        if code_data == "Payment Success":
            g.lcd_queue.put("clear")
            g.lcd_queue.put(("Payment Success", 1))
            g.qr_declined = False
            buzzer.beep(0.5, 0, 1)
            time.sleep(1)
            break
        elif code_data != None:
            g.lcd_queue.put("clear")
            buzzer.beep(1, 1, 1)
            g.lcd_queue.put(("Invalid Code", 1))
            g.lcd_queue.put(("please try again", 2))
            time.sleep(3)
            break
        g.last_key_time = time.time()
    else:
        g.lcd_queue.put("clear")
        buzzer.beep(1, 1, 1)
        g.lcd_queue.put(("Nth detected,", 1))
        g.lcd_queue.put(("please try again", 2))
        time.sleep(3)
        g.last_key_time = time.time()


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
    camera_input()
