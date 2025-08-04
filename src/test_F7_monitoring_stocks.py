import F7_monitoring_stocks as f7
import variables as g


def test_remaining_stock_Jammed():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 less than us stock
    g.drink_database[drinkNum]["stock"] -= 1

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and g.drink_database[drinkNum]["stock"] < g.stock


def test_remaining_stock_Extra_Drink():
    g.out_of_order = False
    drinkNum = 1
    # Make database stock 1 more than us stock
    g.drink_database[drinkNum]["stock"] += 2

    f7.remaining_stock(drinkNum, tester=1)

    assert g.out_of_order == True and g.drink_database[drinkNum]["stock"] > g.stock


def test_remaining_stock_Low_Stock():
    drinkNum = 1
    # Make database stock equal to 4, which is less than 5
    g.drink_database[drinkNum]["stock"] -= 1
    drinkNum = 1

    result = f7.remaining_stock(drinkNum, tester=1)

    assert result == 1
