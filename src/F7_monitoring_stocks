import time
from hal import hal_usonic as usonic

#define a function called distance below:
def get_distance():
    distance = usonic.get_distance()
    return distance

#assume diameter of a drink can is 6cm and length of vending machine is 80cm and max drinks inside one row at once is 10

def remaining_stock():
    # distance = get_distance()  # Get current ultrasonic reading
    distance = get_distance()
    # Calculate stock based on distance
    if distance < 6:    # Very close = full stock
        stock = 10
    elif distance > 60:  # Very far = empty
        stock = 0
    else:                # Intermediate distance
        stock = int(10 * (1 - (distance - 6)/54))
    
    return stock

def alert_staff(stock):
    #get stock value 
    
    if stock < 5:
      # Email staff
      print("email")


def main():
    usonic.init()  
    while True:  
        distance = get_distance()
        stock = remaining_stock()
        print(f"Distance: {distance:.2f} cm, Stock remaining: {stock}")
        
        alert_staff(stock)
        
        time.sleep(1) 



if __name__ == "__main__":
    main()