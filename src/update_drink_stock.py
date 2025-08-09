import sqlite3
import sys # Import sys for command-line arguments

def set_stock_quantity(drink_id, new_stock_quantity):
    """Updates the stock_quantity of a drink in the database."""
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()

    c.execute('UPDATE Drinks SET stock_quantity = ? WHERE drink_id = ?', (new_stock_quantity, drink_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python src/update_drink_stock.py <drink_id> <new_stock_quantity>")
        sys.exit(1)

    try:
        drink_id = int(sys.argv[1])
        new_stock_quantity = int(sys.argv[2])
    except ValueError:
        print("Error: drink_id and new_stock_quantity must be integers.")
        sys.exit(1)

    print(f"Updating stock_quantity for drink ID {drink_id}...")
    set_stock_quantity(drink_id, new_stock_quantity)
    print("Stock quantity updated.")

    print("\nRun 'python src/verify_db.py' to verify changes.")
