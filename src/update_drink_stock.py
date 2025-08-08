
import sqlite3

def update_drink_stock(drink_id, new_stock_quantity):
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    
    try:
        c.execute('UPDATE Drinks SET stock_quantity = ? WHERE drink_id = ?', (new_stock_quantity, drink_id))
        conn.commit()
        if c.rowcount > 0:
            print(f"Stock for drink_id {drink_id} updated to {new_stock_quantity}.")
        else:
            print(f"No drink found with drink_id {drink_id}.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        try:
            drink_id = int(sys.argv[1])
            new_stock_quantity = int(sys.argv[2])
            update_drink_stock(drink_id, new_stock_quantity)
        except ValueError:
            print("Error: drink_id and new_stock_quantity must be integers.")
    else:
        print("Usage: python update_drink_stock.py <drink_id> <new_stock_quantity>")
