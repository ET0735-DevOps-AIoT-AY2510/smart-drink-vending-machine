import sqlite3

def update_stock(drink_id, new_stock):
    """Updates the stock of a drink in the database."""
    conn = sqlite3.connect('vending_machine.db')
    c = conn.cursor()
    
    c.execute('UPDATE Drinks SET stock_quantity = ? WHERE drink_id = ?', (new_stock, drink_id))
    
    conn.commit()
    conn.close()