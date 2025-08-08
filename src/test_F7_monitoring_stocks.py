import F7_monitoring_stocks as f7
import variables as g
from get_drink_by_id import get_drink
from update_drink_stock import update_stock


def test_remaining_stock_Jammed():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 less than us stock
    drink = get_drink(drinkNum)
    update_stock(drinkNum, drink['stock_quantity'] - 1)

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and get_drink(drinkNum)['stock_quantity'] < g.stock


def test_remaining_stock_Extra_Drink():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 more than us stock
    drink = get_drink(drinkNum)
    update_stock(drinkNum, drink['stock_quantity'] + 2)

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and get_drink(drinkNum)['stock_quantity'] > g.stock


def test_remaining_stock_Low_Stock():
    drinkNum = 1
    # Make database stock equal to 4, which is less than 5
    update_stock(drinkNum, 4)

    result = f7.remaining_stock(drinkNum, tester=1)

    assert result == 1
