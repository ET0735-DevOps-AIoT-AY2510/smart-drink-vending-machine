
import sqlite3

def clear_database():
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()

    try:
        c.execute('DELETE FROM Orders')
        c.execute('DELETE FROM Users')
        c.execute('DELETE FROM Drinks')
        conn.commit()
        print("All data cleared from Users, Drinks, and Orders tables.")
    except Exception as e:
        print(f"Error clearing database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    clear_database()
