from hal import hal_usonic as us
import time
import variables as g

# assume diameter of a drink can is 6cm and length of vending machine is 80cm and max drinks inside one row at once is 10


def remaining_stock(drinkNum, tester=None):
    if tester is not None:  # for pytest
        distance = 38.4
    else:
        distance = us.get_distance()
    time.sleep(1)
    # Calculate stock based on distance
    if distance < 6:    # Very close = full stock
        g.stock = 10
    elif distance > 60:  # Very far = empty
        g.stock = 0
    else:                # Intermediate distance
        g.stock = int(10 * (1 - (distance - 6)/54))

    if g.drink_database[drinkNum]["stock"] < g.stock:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
                     subject='Vending Machine Jammed',
                     body_text=f'Vending Machine Jammed for {g.drink_database[drinkNum]["name"]}')
        g.lcd_queue.put("clear")
        g.lcd_queue.put(("Dispense failed", 1))
        g.lcd_queue.put(("contact 12345", 2))
        time.sleep(5)
        g.out_of_order = True

    elif g.drink_database[drinkNum]["stock"] > g.stock:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
                     subject='Extra drink dispensed',
                     body_text=f'Extra drink dispensed for {g.drink_database[drinkNum]["name"]}')
        g.out_of_order = True
    if tester is None:
        g.drink_database[drinkNum]["stock"] = g.stock

    if g.drink_database[drinkNum]["stock"] < 5:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
                     subject='Drink is low in stock',
                     body_text=f'{g.drink_database[drinkNum]["name"]} currently has {g.drink_database[drinkNum]["stock"]} left')
        if tester is not None:
            return 1


def main():
    us.init()


if __name__ == "__main__":
    main()
