
import sqlite3

def dispense_drink(barcode):
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    
    try:
        # Check if the barcode exists and the order is 'paid'
        c.execute('SELECT order_id FROM Orders WHERE collection_barcode = ? AND order_status = ?', (barcode, 'paid'))
        order = c.fetchone()

        if order:
            order_id = order[0]
            # Update the order status to 'collected'
            c.execute('UPDATE Orders SET order_status = ? WHERE order_id = ?', ('collected', order_id))
            conn.commit()
            print("dispensing")
        else:
            print("wrong code")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        barcode_to_check = sys.argv[1]
        dispense_drink(barcode_to_check)
    else:
        print("Usage: python dispense_drink.py <barcode>")
