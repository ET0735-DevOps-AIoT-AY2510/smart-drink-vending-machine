import F2_card_payment as f2
import variables as g


def test_rfid_input_Card_Accepted():
    g.card_declined = None
    f2.rfid_input(tester=1)

    assert g.card_declined == False

    g.card_declined = None
    g.card_data_string = 0


def test_rfid_input_Card_Declined():
    g.card_declined = None
    f2.rfid_input(tester=0)

    assert g.card_declined == True

    g.card_declined = None
    g.card_data_string = 0
