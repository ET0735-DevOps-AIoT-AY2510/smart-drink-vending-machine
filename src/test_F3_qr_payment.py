import pytest
import time
import queue
from unittest.mock import MagicMock, patch
import numpy as np

import F3_qr_payment as f3  # Import your main code module
import variables as g       # Global state shared between components


# This fixture automatically runs before every test
@pytest.fixture(autouse=True)
def setup_globals(monkeypatch):
    # Reset global state for each test
    g.escape = False
    g.qr_declined = True
    g.last_key_time = time.time()
    g.shared_keypad_queue = queue.Queue()
    g.lcd_queue = queue.Queue()

    # Mock LCD output, buzzer, and camera so real hardware is not required
    monkeypatch.setattr(g.lcd_queue, "put", MagicMock())
    monkeypatch.setattr(f3.buzzer, "beep", MagicMock())
    monkeypatch.setattr(g, "picam2", MagicMock())
    monkeypatch.setattr(g.picam2, "capture_file", MagicMock())


# Test QR code recognition logic with 3 scenarios using parameterisation
@pytest.mark.parametrize("code_data, expected_declined", [
    ("Payment Success", False),  # Should be accepted
    ("Invalid Code", True),      # Should be declined
    (None, True)                 # No QR detected, should be declined
])
def test_camera_input_qr_recognition(monkeypatch, code_data, expected_declined):
    # Create dummy image data (100x100 black image)
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    monkeypatch.setattr(f3.cv2, "imread", lambda path: dummy_image)

    # Mock all OpenCV operations to simulate image processing
    monkeypatch.setattr(f3.cv2, "cvtColor", lambda img, code: img)
    monkeypatch.setattr(f3.cv2, "GaussianBlur", lambda img, ksize, sigma: img)
    monkeypatch.setattr(f3.cv2, "Canny", lambda img, low,
                        high: np.zeros((100, 100), dtype=np.uint8))
    monkeypatch.setattr(f3.cv2, "findContours", lambda img, mode, method: (
        [np.array([[0, 0], [0, 1], [1, 1], [1, 0]])], None))
    monkeypatch.setattr(f3.cv2, "minAreaRect",
                        lambda cnt: ((50, 50), (100, 100), 0))
    monkeypatch.setattr(f3.cv2, "getRotationMatrix2D",
                        lambda center, angle, scale: np.eye(2, 3))
    monkeypatch.setattr(f3.cv2, "warpAffine", lambda img,
                        matrix, dsize, flags=None: img)
    monkeypatch.setattr(f3.cv2, "createCLAHE", lambda **
                        kwargs: MagicMock(apply=lambda img: img))
    monkeypatch.setattr(f3.cv2, "resize", lambda img,
                        size, interpolation=None: img)

    # Simulate decoding of a QR code using dummy data
    class DummyDecoded:
        def __init__(self, data):
            self.type = "QRCODE"
            self.data = data.encode() if data else b""
            self.rect = (0, 0, 100, 100)

    # Return dummy decoded QR object or empty list
    decoded_list = [DummyDecoded(code_data)] if code_data else []

    # Patch align_and_decode to return our mocked decoded QR data
    monkeypatch.setattr(f3, "align_and_decode",
                        MagicMock(return_value=decoded_list))

    # Clear keypad queue to avoid interference
    with g.shared_keypad_queue.mutex:
        g.shared_keypad_queue.queue.clear()

    # Run function under test
    f3.camera_input()

    # Check if the system correctly updated qr_declined flag
    assert g.qr_declined == expected_declined


def test_return_button_pressed():
    g.escape = False
    # Simulate user pressing the "*" button
    g.shared_keypad_queue.put("*")
    f3.camera_input()
    # Check that variables are correct when * is pressed
    assert g.escape is True
