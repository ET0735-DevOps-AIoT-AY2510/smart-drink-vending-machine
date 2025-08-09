import sqlite3

def verify_database_content():
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row # To access columns by name
    c = conn.cursor()
    
    print("\n--- Users Table ---")
    try:
        c.execute('SELECT user_id, username, password_hash, created_at FROM Users')
        users = c.fetchall()
        if not users:
            print("Users table is empty.")
        else:
            for user in users:
                print(f"  ID: {user['user_id']}, Username: {user['username']}, Password Hash: {user['password_hash']}, Created At: {user['created_at']}")
    except sqlite3.OperationalError as e:
        print(f"Error accessing Users table: {e}")

    print("\n--- Admins Table ---")
    try:
        c.execute('SELECT admin_id, username, password_hash, created_at FROM Admins')
        admins = c.fetchall()
        if not admins:
            print("Admins table is empty.")
        else:
            for admin in admins:
                print(f"  ID: {admin['admin_id']}, Username: {admin['username']}, Password Hash: {admin['password_hash']}, Created At: {admin['created_at']}")
    except sqlite3.OperationalError as e:
        print(f"Error accessing Admins table: {e}")

    print("\n--- Drinks Table ---")
    try:
        c.execute('SELECT drink_id, name, price, image_url, stock_quantity, reserved_stock FROM Drinks')
        drinks = c.fetchall()
        if not drinks:
            print("Drinks table is empty.")
        else:
            for drink in drinks:
                print(f"  ID: {drink['drink_id']}, Name: {drink['name']}, Price: {drink['price']:.2f}, Image: {drink['image_url']}, Stock: {drink['stock_quantity']}, Reserved: {drink['reserved_stock']}")
    except sqlite3.OperationalError as e:
        print(f"Error accessing Drinks table: {e}")

    print("\n--- Orders Table ---")
    try:
        c.execute('SELECT order_id, user_id, drink_id, order_status, order_date, collection_barcode FROM Orders')
        orders = c.fetchall()
        if not orders:
            print("Orders table is empty.")
        else:
            for order in orders:
                print(f"  Order ID: {order['order_id']}, User ID: {order['user_id']}, Drink ID: {order['drink_id']}, Status: {order['order_status']}, Date: {order['order_date']}, Barcode: {order['collection_barcode']}")
    except sqlite3.OperationalError as e:
        print(f"Error accessing Orders table: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    verify_database_content()