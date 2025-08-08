import sqlite3

def get_drink(drink_id):
    """Fetches a drink from the database by its ID."""
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,))
    drink = c.fetchone()
    
    conn.close()
    
    return drink

def get_all_drink_ids():
    """Fetches all drink IDs from the database."""
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    
    c.execute('SELECT drink_id FROM Drinks')
    drink_ids = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return drink_ids

if __name__ == '__main__':
    print("--- All Drink IDs ---")
    all_ids = get_all_drink_ids()
    if all_ids:
        for drink_id in all_ids:
            print(f"  ID: {drink_id}")
    else:
        print("No drinks found in the database.")

    print("\n--- Get Drink by ID ---")
    drink_id_to_find = 2  # Example: Change this ID to search for a different drink
    drink_info = get_drink(drink_id_to_find)
    
    if drink_info:
        print(f"--- Drink Information for ID: {drink_info['drink_id']} ---")
        print(f"  Name: {drink_info['name']}")
        print(f"  Price: ${drink_info['price']:.2f}")
        print(f"  Stock: {drink_info['stock_quantity']}")
        print(f"  Image URL: {drink_info['image_url']}")
    else:
        print(f"No drink found with ID: {drink_id_to_find}")
