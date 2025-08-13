from unittest.mock import patch
import threading
import variables as g
import F8_burglar_detection as f8
import time


@patch('variables.accelerometer')
def test_door_was_pried_open(mock_accelerometer):
    mock_accelerometer.get_3_axis_adjusted.return_value = (0, 0, 0)
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    g.BurglarState = False
    f8.main(pytest=1, ir_sensor_state=False)
    assert g.f8_test_flag_1 is True and g.f8_test_flag_2 is False


@patch('variables.accelerometer')
def test_door_is_closed(mock_accelerometer):
    mock_accelerometer.get_3_axis_adjusted.return_value = (0, 0, 0)
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    f8.main(pytest=1, ir_sensor_state=True)
    # Door was not opened at all
    assert g.f8_test_flag_1 is False and g.f8_test_flag_2 is False


@patch('variables.accelerometer')
def test_door_was_pried_opened_then_closed(mock_accelerometer):
    mock_accelerometer.get_3_axis_adjusted.return_value = (0, 0, 0)
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    sensor_state = [False]  # Use a list to make it mutable

    def ir_sensor_state_func():
        return sensor_state[0]

    t = threading.Thread(target=f8.main, args=(1, ir_sensor_state_func))
    t.start()
    time.sleep(1)
    sensor_state[0] = True
    t.join()
    assert g.f8_test_flag_1 is True and g.f8_test_flag_2 is True
