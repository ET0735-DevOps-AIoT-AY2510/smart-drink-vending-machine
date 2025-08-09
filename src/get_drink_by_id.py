import sqlite3
import time
import random

admin_barcode = None
barcode_generation_time = 0

def get_admin_barcode():
    global admin_barcode, barcode_generation_time
    current_time = time.time()
    if current_time - barcode_generation_time > 30:
        admin_barcode = ''.join(random.choices('0123456789', k=10))
        barcode_generation_time = current_time
    return admin_barcode

def get_drink(drink_id):
    """Fetches a drink from the database by its ID."""
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,))
    drink = c.fetchone()
    
    conn.close()
    
    return drink

def get_actual_drink(drink_id):
    """Fetches a drink from the database by its ID and calculates actual stock."""
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,))
    drink = c.fetchone()

    conn.close()

    if drink:
        # Convert to a mutable dictionary
        drink_dict = dict(drink)
        drink_dict['actual_stock'] = drink_dict['stock_quantity'] - drink_dict['reserved_stock']
        return drink_dict
    return None

def get_all_drink_ids():
    """Fetches all drink IDs from the database."""
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    
    c.execute('SELECT drink_id FROM Drinks')
    drink_ids = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return drink_ids

def get_reserved_drink_barcodes():
    """Fetches a list of collection barcodes for drinks with 'paid' status."""
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT collection_barcode FROM Orders WHERE order_status = ?', ('paid',))
    barcodes = [row['collection_barcode'] for row in c.fetchall()]

    conn.close()
    return barcodes

def get_drink_id_from_barcode(barcode):
    """Fetches the drink_id associated with a given collection barcode."""
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT drink_id FROM Orders WHERE collection_barcode = ?', (barcode,))
    result = c.fetchone()

    conn.close()
    if result:
        return result['drink_id']
    return None

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

    print("\n--- Get Actual Drink by ID ---")
    actual_drink_info = get_actual_drink(drink_id_to_find)
    if actual_drink_info:
        print(f"--- Actual Drink Information for ID: {actual_drink_info['drink_id']} ---")
        print(f"  Name: {actual_drink_info['name']}")
        print(f"  Price: ${actual_drink_info['price']:.2f}")
        print(f"  Stock: {actual_drink_info['stock_quantity']}")
        print(f"  Reserved Stock: {actual_drink_info['reserved_stock']}")
        print(f"  Actual Stock: {actual_drink_info['actual_stock']}")
        print(f"  Image URL: {actual_drink_info['image_url']}")
    else:
        print(f"No actual drink info found with ID: {drink_id_to_find}")

    print("\n--- Reserved Drink Barcodes ---")
    reserved_barcodes = get_reserved_drink_barcodes()
    if reserved_barcodes:
        for barcode_val in reserved_barcodes:
            print(f"  Barcode: {barcode_val}")

            # Test the new function
            drink_id_from_barcode = get_drink_id_from_barcode(barcode_val)
            if drink_id_from_barcode is not None:
                print(f"    -> Drink ID for this barcode: {drink_id_from_barcode}")
            else:
                print(f"    -> Could not find drink ID for barcode: {barcode_val}")
    else:
        print("No reserved drinks found.")

