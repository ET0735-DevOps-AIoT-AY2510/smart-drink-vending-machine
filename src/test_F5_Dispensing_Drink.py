import F5_Dispensing_Drink as f5
import variables as g
from get_drink_by_id import get_drink
from unittest.mock import patch

@patch('F5_Dispensing_Drink.dc')
def test_dispensing_drink(mock_dc):
    drinkNum = 1
    initial_stock = get_drink(drinkNum)["stock_quantity"]
    expected_drink_stock = initial_stock - 1

    f5.dispensing_drink(drinkNum)
    final_drink_stock = get_drink(drinkNum)["stock_quantity"]

    assert expected_drink_stock == final_drink_stock
