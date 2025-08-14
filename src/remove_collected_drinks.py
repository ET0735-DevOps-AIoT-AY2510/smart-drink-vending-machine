import sqlite3

def remove_collected_drink(barcode):
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    try:
        # Look for an order with status 'paid'
        c.execute('SELECT drink_id FROM Orders WHERE collection_barcode = ? AND order_status = ?', (barcode, 'paid'))
        result = c.fetchone()

        if result:
            drink_id = result[0]
            c.execute('UPDATE Orders SET order_status = ? WHERE collection_barcode = ?', ('collected', barcode))
            c.execute('UPDATE Drinks SET reserved_stock = reserved_stock - 1 WHERE drink_id = ?', (drink_id,))
            conn.commit()
            if c.rowcount > 0:
                print(f"Order with barcode {barcode} marked as collected and reserved stock decremented.")
            else:
                # This case should ideally not be reached if the first SELECT was successful
                print(f"Could not update order with barcode {barcode}.")
        else:
            # If no 'paid' order is found, check if the barcode exists with a different status
            c.execute('SELECT order_status FROM Orders WHERE collection_barcode = ?', (barcode,))
            status_result = c.fetchone()
            if status_result:
                print(f"Order with barcode {barcode} found, but its status is '{status_result[0]}', not 'paid'.")
            else:
                print(f"No order found with barcode {barcode}.")

    except Exception as e:
        conn.rollback()
        print(f"Error updating order: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        barcode_to_remove = sys.argv[1]
        remove_collected_drink(barcode_to_remove)
    else:
        print("Usage: python remove_collected_drinks.py <barcode>")