import F5_Dispensing_Drink as f5
import variables as g


def test_dispensing_drink():
    drinkNum = 6
    initial_stock = f5.g.drink_database[drinkNum]["stock"]
    expected_drink_stock = initial_stock - 1

    f5.dispensing_drink(drinkNum)
    final_drink_stock = f5.g.drink_database[drinkNum]["stock"]

    assert expected_drink_stock == final_drink_stock
