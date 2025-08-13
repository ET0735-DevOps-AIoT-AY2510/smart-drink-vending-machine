import F6_admin_access as f6
import variables as g
import time
import sys
from unittest.mock import patch, MagicMock

sys.modules['spidev'] = MagicMock()


@patch('hal.hal_accelerometer.init', return_value=MagicMock())
def test_unlock_door(mock_accel_init):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = True
    g.security_prompt = True
    g.waiting_for_payment = True
    g.elapsed = time.time()
    # Simulate that ir is not covered
    with patch('F6_admin_access.adc.get_adc_value', return_value=0):
        f6.main(ir_pytest=False, ir_sensor_state=False)
    # Check if these conditions are correct when door unlocks, then checks if admin is there, then lastly closes door
    assert g.f6_test_flag_1 is True and g.f6_test_flag_2 is True and g.f6_test_flag_3 is True
    g.elapsed = time.time()+6


@patch('hal.hal_accelerometer.init', return_value=MagicMock())
def test_security_check(mock_accel_init):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = False
    g.security_prompt = False
    g.waiting_for_payment = True
    g.elapsed = time.time()-6
    # Simulate that ir is not covered
    with patch('F6_admin_access.adc.get_adc_value', return_value=0):
        f6.main(ir_pytest=False, ir_sensor_state=False)
    # Check if these conditions are correct when only checking if admin is there,snd the closing of door
    assert g.f6_test_flag_1 is False and g.f6_test_flag_2 is True and g.f6_test_flag_3 is True


@patch('hal.hal_accelerometer.init', return_value=MagicMock())
def test_timeout(mock_accel_init):
    g.f6_test_flag_1 = False
    g.f6_test_flag_2 = False
    g.f6_test_flag_3 = False
    g.out_of_order = True
    g.BurglarState = True
    g.stillthere = True
    g.security_prompt = True
    g.waiting_for_payment = True
    g.elapsed = time.time()-16
    with patch('F6_admin_access.adc.get_adc_value', return_value=0):
        f6.main(ir_pytest=False, ir_sensor_state=False)
    # Check if these conditions are correct when only closing door
    assert g.f6_test_flag_1 is False and g.f6_test_flag_2 is False and g.f6_test_flag_3 is True
