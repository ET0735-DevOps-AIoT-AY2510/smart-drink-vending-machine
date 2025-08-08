
import sqlite3

def remove_collected_drink(barcode):
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE Orders SET order_status = ? WHERE collection_barcode = ?', ('collected', barcode))
        conn.commit()
        if c.rowcount > 0:
            print(f"Order with barcode {barcode} marked as collected.")
        else:
            print(f"No uncollected order found with barcode {barcode}.")
    except Exception as e:
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
