from hal import hal_usonic as usonic
import time
import variables as g

#assume diameter of a drink can is 6cm and length of vending machine is 80cm and max drinks inside one row at once is 10

def remaining_stock():
    distance = usonic.get_distance()
    time.sleep(5)
    # Calculate stock based on distance
    if distance < 6:    # Very close = full stock
        stock = 10
    elif distance > 60:  # Very far = empty
        stock = 0
    else:                # Intermediate distance
        stock = int(10 * (1 - (distance - 6)/54))
        g.stock = stock

    if g.stock < 5:
        g.send_email(receiver_email='terencetngkc2007@gmail.com',
        subject='Extra drink dispensed',
        body_text='Extra drink dispensed')
    
def main():
    usonic.init()  
    

if __name__ == "__main__":
    main()