import F4_Monitoring_Temp_Conditions as f4
import variables as g

'''def test_tempGet():
    f4.g.temp=0
    
    f4.tempGet(tester=1)

    assert f4.g.temp>0'''

def test_temp_Monitor_email20():
    f4.g.temp=21
    f4.g.check20=0
    f4.g.check10=0

    f4.temp_Monitor()

    assert f4.g.check20 == 1 and f4.g.check10 == 1

def test_temp_Monitor_email10():
    f4.g.temp=15
    f4.g.check20=0
    f4.g.check10=0

    f4.temp_Monitor()

    assert f4.g.check20 == 0 and f4.g.check10 == 1

def test_temp_Monitor_OutOfOrder():
    f4.g.waiting_for_payment = False
    f4.g.out_of_order = False
    f4.g.check20 = True

    f4.temp_Monitor()

    assert f4.g.out_of_order == True
