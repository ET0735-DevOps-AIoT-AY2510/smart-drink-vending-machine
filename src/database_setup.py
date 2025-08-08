
import sqlite3
import bcrypt

def setup_database():
    conn = sqlite3.connect('vending_machine.db')
    print(f"Database connected/created at: vending_machine.db")
    c = conn.cursor()

    # Drop tables if they exist to ensure a clean start
    c.execute('DROP TABLE IF EXISTS Orders')
    c.execute('DROP TABLE IF EXISTS Drinks')
    c.execute('DROP TABLE IF EXISTS Users')
    c.execute('DROP TABLE IF EXISTS Admins')

    # Create Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Admins table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add Admin user
    admin_username = 'Admin'
    admin_password = 'test1'.encode('utf-8')
    hashed_admin_password = bcrypt.hashpw(admin_password, bcrypt.gensalt())
    c.execute('INSERT OR IGNORE INTO Admins (username, password_hash) VALUES (?, ?)', (admin_username, hashed_admin_password))

    # Create Drinks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Drinks (
            drink_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT,
            stock_quantity INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Create Orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            drink_id INTEGER NOT NULL,
            order_status TEXT NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            collection_barcode TEXT UNIQUE,
            FOREIGN KEY(user_id) REFERENCES Users(user_id),
            FOREIGN KEY(drink_id) REFERENCES Drinks(drink_id)
        )
    ''')

    # Populate Drinks table with initial data
    drinks = [
        ('Coke', 1.30, 'images/coke.png', 24),
        ('Sprite', 1.50, 'images/sprite.png', 18),
        ('Lemon Tea', 1.10, 'images/lemon_tea.png', 30),
        ('Water', 1.00, 'images/water.png', 40)
    ]

    c.executemany('INSERT INTO Drinks (name, price, image_url, stock_quantity) VALUES (?,?,?,?)', drinks)


    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database and tables created successfully.")
