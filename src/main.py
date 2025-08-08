from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import bcrypt
import os
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key' # Replace with a strong secret key

# Ensure the barcodes directory exists
BARCODES_DIR = os.path.join(app.root_path, 'static', 'barcodes')
os.makedirs(BARCODES_DIR, exist_ok=True)

#  helper function to get db connection
def get_db_connection():
    conn = sqlite3.connect('vending_machine.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user['password_hash']):
            session['user_id'] = user['user_id']
            session['is_admin'] = False
            return redirect(url_for('drink_page'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM Admins WHERE username = ?', (username,)).fetchone()
        conn.close()

        if admin and bcrypt.checkpw(password, admin['password_hash']):
            session['user_id'] = admin['admin_id']
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid Admin username or password', is_admin_login=True)
    return render_template('login.html', is_admin_login=True)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    admin_barcode_data = '12345'
    # Generate barcode image
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(admin_barcode_data, writer=ImageWriter())
    ean.save(os.path.join(BARCODES_DIR, f'{admin_barcode_data}.png'))

    conn = get_db_connection()
    drinks = conn.execute('SELECT * FROM Drinks').fetchall()
    conn.close()

    return render_template('admin_dashboard.html', barcode_number=admin_barcode_data, drinks=drinks)

@app.route('/update_stock', methods=['POST'])
def update_stock():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    drink_id = request.form['drink_id']
    change = request.form['change']

    conn = get_db_connection()
    try:
        if change == 'increase':
            conn.execute('UPDATE Drinks SET stock_quantity = stock_quantity + 1 WHERE drink_id = ?', (drink_id,))
        elif change == 'decrease':
            conn.execute('UPDATE Drinks SET stock_quantity = stock_quantity - 1 WHERE drink_id = ? AND stock_quantity > 0', (drink_id,))
        conn.commit()
    except Exception as e:
        print(f"Error updating stock: {e}")
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error='Username already exists')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/drinks')
def drink_page():
    conn = get_db_connection()
    drinks = conn.execute('SELECT * FROM Drinks').fetchall()
    conn.close()
    return render_template('drink-page.html', drinks=drinks)

@app.route('/payment/<int:drink_id>')
def payment(drink_id):
    conn = get_db_connection()
    drink = conn.execute('SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,)).fetchone()
    conn.close()
    if drink:
        return render_template('payment.html', drink=drink)
    else:
        return redirect(url_for('drink_page')) # Redirect if drink not found

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    drink_id = request.form['drink_id']
    user_id = session['user_id']

    conn = get_db_connection()
    drink = conn.execute('SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,)).fetchone()

    if drink and drink['stock_quantity'] > 0:
        # Simulate payment success and generate barcode
        import random
        collection_barcode = ''.join(random.choices('0123456789', k=8)) # Simple 8-digit barcode
        
        # Generate barcode image
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(collection_barcode, writer=ImageWriter())
        ean.save(os.path.join(BARCODES_DIR, f'{collection_barcode}.png'))

        try:
            conn.execute('UPDATE Drinks SET stock_quantity = stock_quantity - 1 WHERE drink_id = ?', (drink_id,))
            conn.execute('INSERT INTO Orders (user_id, drink_id, order_status, collection_barcode) VALUES (?, ?, ?, ?)', 
                         (user_id, drink_id, 'paid', collection_barcode))
            conn.commit()
            conn.close()
            return redirect(url_for('collection_page', barcode=collection_barcode))
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Drink not available or out of stock'}), 400

@app.route('/collection_page')
def collection_page():
    barcode = request.args.get('barcode')
    return render_template('collection.html', barcode=barcode)

@app.route('/inbox')
def inbox():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    uncollected_orders = conn.execute('''
        SELECT o.order_id, d.name, d.image_url, o.collection_barcode
        FROM Orders o
        JOIN Drinks d ON o.drink_id = d.drink_id
        WHERE o.user_id = ? AND o.order_status = ?
    ''', (user_id, 'paid')).fetchall()
    conn.close()
    return render_template('inbox.html', orders=uncollected_orders)

@app.route('/collect_drink/<int:order_id>', methods=['POST'])
def collect_drink(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        conn.execute('UPDATE Orders SET order_status = ? WHERE order_id = ? AND user_id = ?', 
                     ('collected', order_id, session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('inbox'))
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)