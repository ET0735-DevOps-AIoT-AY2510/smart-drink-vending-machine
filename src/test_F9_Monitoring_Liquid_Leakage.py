import F9_Monitoring_Liquid_Leakage as f9

def test_getMoist():
    f9.g.moist=True

    f9.getMoist()

    assert f9.g.moist == False

def test_monitor_leak_normal():
    f9.g.moist=True
    f9.g.emailCheckLeak=0

    f9.monitor_leak()

    assert f9.g.emailCheckLeak == 1 

def test_monitor_leak_OutOfOrderl():
    f9.g.waiting_for_payment=0
    f9.g.out_of_order=False
    f9.g.emailCheckLeak=True

    f9.monitor_leak()

    assert f9.g.out_of_order == True
    