import time
import variables as g
import F6_admin_access as f6


def test_unlock_door(monkeypatch):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = True
    g.security_prompt = True
    g.waiting_for_payment = True
    g.elapsed = time.time()
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: False)
    f6.main(ir_pytest=False)  # Simulate that ir is not covered
    # Check if these conditions are correct when door unlocks, then checks if admin is there, then lastly closes door
    assert g.f6_test_flag_1 is True and g.f6_test_flag_2 is True and g.f6_test_flag_3 is True
    g.elapsed = time.time()+6


def test_security_check(monkeypatch):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = False
    g.security_prompt = False
    g.waiting_for_payment = True
    g.elapsed = time.time()-6
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: False)
    f6.main(ir_pytest=False)  # Simulate that ir is not covered
    # Check if these conditions are correct when only checking if admin is there,snd the closing of door
    assert g.f6_test_flag_1 is False and g.f6_test_flag_2 is True and g.f6_test_flag_3 is True


def test_timeout(monkeypatch):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = True
    g.security_prompt = True
    g.waiting_for_payment = True
    monkeypatch.setattr("hal.hal_ir_sensor.get_ir_sensor_state", lambda: False)
    g.elapsed = time.time()-11
    f6.main(ir_pytest=False)
    # Check if these conditions are correct when only closing door
    assert g.f6_test_flag_1 is False and g.f6_test_flag_2 is False and g.f6_test_flag_3 is True
