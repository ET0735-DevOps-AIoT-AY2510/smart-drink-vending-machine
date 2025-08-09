import sys
from unittest.mock import MagicMock

# Mock RPi.GPIO
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()

# Mock smbus
sys.modules['smbus'] = MagicMock()

# Mock spidev
sys.modules['spi'] = MagicMock()

# Mock picamera2
sys.modules['picamera2'] = MagicMock()
sys.modules['picamera2.Picamera2'] = MagicMock()
sys.modules['picamera2.Preview'] = MagicMock()

# Mock cv2
sys.modules['cv2'] = MagicMock()

# Mock PIL
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

# Mock pyzbar
sys.modules['pyzbar'] = MagicMock()
sys.modules['pyzbar.pyzbar'] = MagicMock()