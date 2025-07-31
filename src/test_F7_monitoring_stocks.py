import F7_monitoring_stocks as f7
from hal import hal_usonic as us
import variables as g

def test_remaining_stock_Jammed():
    us.init()
    g.out_of_order=False
    drinkNum = 1
    g.drink_database[drinkNum]["stock"]-=1

    f7.remaining_stock(drinkNum,tester=1)

    assert g.out_of_order==True and g.drink_database[drinkNum]["stock"] < g.stock

def test_remaining_stock_Extra_Drink():
    us.init()
    g.out_of_order=False
    drinkNum = 1
    g.drink_database[drinkNum]["stock"]+=1

    f7.remaining_stock(drinkNum,tester=1)

    assert g.out_of_order==True and g.drink_database[drinkNum]["stock"] > g.stock

def test_remaining_stock_Low_Stock():
    us.init()
    drinkNum = 1

    result=f7.remaining_stock(drinkNum,tester=1)

    assert result == 1