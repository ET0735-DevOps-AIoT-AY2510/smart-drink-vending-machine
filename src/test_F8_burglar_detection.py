import threading
import variables as g
import F8_burglar_detection as f8
import time


def test_door_was_pried_open(monkeypatch):
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    g.BurglarState = False
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: False)
    f8.main(pytest=1)
    assert g.f8_test_flag_1 is True and g.f8_test_flag_2 is False


def test_door_is_closed(monkeypatch):
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: True)
    f8.main(pytest=1)
    # Door was not opened at all
    assert g.f8_test_flag_1 is False and g.f8_test_flag_2 is False


def test_door_was_pried_opened_then_closed(monkeypatch):
    g.f8_test_flag_1 = False
    g.f8_test_flag_2 = False
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: False)
    t = threading.Thread(target=f8.main, args=(1,))
    t.start()
    time.sleep(1)
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: True)
    t.join()
    assert g.f8_test_flag_1 is True and g.f8_test_flag_2 is True
