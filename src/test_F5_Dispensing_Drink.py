import F5_Dispensing_Drink as f5

def test_dispensing_drink():
    expected_drink_stock = 2
    drinkNum = 2
    f5.dispensing_drink(drinkNum)
    
    assert expected_drink_stock == f5.g.drink_database[drinkNum]["stock"]


