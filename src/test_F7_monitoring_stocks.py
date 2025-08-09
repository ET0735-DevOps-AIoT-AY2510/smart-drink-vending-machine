import F7_monitoring_stocks as f7
import variables as g
from get_drink_by_id import get_drink
from update_drink_stock import set_stock_quantity


def test_remaining_stock_Jammed():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 less than us stock
    drink = get_drink(drinkNum)
    set_stock_quantity(drinkNum, 3)

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and get_drink(
        drinkNum)['stock_quantity'] < g.stock


def test_remaining_stock_Extra_Drink():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 more than us stock
    drink = get_drink(drinkNum)
    set_stock_quantity(drinkNum, 5)

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and get_drink(
        drinkNum)['stock_quantity'] > g.stock


def test_remaining_stock_Low_Stock():
    drinkNum = 1
    # Make database stock equal to 4, which is less than 5
    set_stock_quantity(drinkNum, 4)

    result = f7.remaining_stock(drinkNum, tester=1)

    assert result == 1
