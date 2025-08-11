from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import bcrypt
import os
import barcode
from barcode.writer import ImageWriter
from get_drink_by_id import get_actual_drink, get_drink_id_from_barcode, get_admin_barcode, get_all_emails
import variables as g

app = Flask(__name__, static_folder='static', template_folder='templates')
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

ALLOWED_ROUTES = ['homepage', 'login', 'admin_login', 'signup', 'static']


@app.before_request
def redirect_unauthenticated_users():
    if request.endpoint not in ALLOWED_ROUTES and 'user_id' not in session:
        return redirect(url_for('login'))


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
        user = conn.execute(
            'SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
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
        admin = conn.execute(
            'SELECT * FROM Admins WHERE username = ?', (username,)).fetchone()
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

    admin_barcode_data = get_admin_barcode()
    # Generate barcode image
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(admin_barcode_data, writer=ImageWriter())
    ean.save(os.path.join(BARCODES_DIR, f'{admin_barcode_data}'))
    print(
        f"Saving barcode to: {os.path.join(BARCODES_DIR, f'{admin_barcode_data}.png')}")

    conn = get_db_connection()

    all_drinks_data = conn.execute('SELECT drink_id FROM Drinks').fetchall()
    drinks_for_admin = []
    for row in all_drinks_data:
        drink_id = row['drink_id']
        actual_drink = get_actual_drink(drink_id)
        if actual_drink:
            drinks_for_admin.append(actual_drink)

    conn.close()

    return render_template('admin_dashboard.html', barcode_number=admin_barcode_data, drinks=drinks_for_admin, emails=get_all_emails())


@app.route('/update_stock', methods=['POST'])
def update_stock():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    drink_id = request.form['drink_id']
    change = request.form['change']

    conn = get_db_connection()
    try:
        if change == 'increase':
            conn.execute(
                'UPDATE Drinks SET stock_quantity = stock_quantity + 1 WHERE drink_id = ?', (drink_id,))
        elif change == 'decrease':
            conn.execute(
                'UPDATE Drinks SET stock_quantity = stock_quantity - 1 WHERE drink_id = ? AND stock_quantity > 0', (drink_id,))
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
            conn.execute(
                'INSERT INTO Users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
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

    all_drinks_data = conn.execute('SELECT drink_id FROM Drinks').fetchall()
    drinks_with_actual_stock = []
    for row in all_drinks_data:
        drink_id = row['drink_id']
        actual_drink = get_actual_drink(drink_id)
        if actual_drink:
            drinks_with_actual_stock.append(actual_drink)

    # Get username from session
    username = None
    if 'user_id' in session:
        user_id = session['user_id']
        user = conn.execute(
            'SELECT username FROM Users WHERE user_id = ?', (user_id,)).fetchone()
        if user:
            username = user['username']

    conn.close()
    return render_template('drink-page.html', drinks=drinks_with_actual_stock, username=username)


@app.route('/payment/<int:drink_id>')
def payment(drink_id):
    drink = get_actual_drink(drink_id)
    if drink:
        return render_template('payment.html', drink=drink)
    else:
        return redirect(url_for('drink_page'))  # Redirect if drink not found


@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    drink_id = request.form['drink_id']
    user_id = session['user_id']

    conn = get_db_connection()
    drink = conn.execute(
        'SELECT * FROM Drinks WHERE drink_id = ?', (drink_id,)).fetchone()

    if drink and (drink['stock_quantity'] - drink['reserved_stock']) > 0:
        # Simulate payment success and generate barcode
        import random
        collection_barcode = ''.join(random.choices(
            '0123456789', k=8))  # Simple 8-digit barcode

        # Generate barcode image
        EAN = barcode.get_barcode_class('code128')
        # Pass options to ImageWriter for better clarity
        options = {
            'module_width': 0.3,  # Increase module width for thicker bars
            'module_height': 15,  # Set a fixed height for the bars
            'write_text': True,   # Ensure the barcode number is written below
            'font_size': 10,      # Adjust font size for readability
            'text_distance': 5,   # Distance between barcode and text
            'quiet_zone': 6       # Add more quiet zone around the barcode
        }
        writer = ImageWriter()
        ean = EAN(collection_barcode, writer=writer)
        ean.save(os.path.join(BARCODES_DIR, collection_barcode), options=options)

        try:
            conn.execute(
                'UPDATE Drinks SET reserved_stock = reserved_stock + 1 WHERE drink_id = ?', (drink_id,))
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
    drink = None
    if barcode:
        drink_id = get_drink_id_from_barcode(barcode)
        if drink_id:
            drink = get_actual_drink(drink_id)

    return render_template('collection.html', barcode=barcode, drink=drink, out_of_order=g.out_of_order)


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
        # Get drink_id from the order
        order = conn.execute(
            'SELECT drink_id FROM Orders WHERE order_id = ?', (order_id,)).fetchone()
        if order:
            drink_id = order['drink_id']
            # Decrease stock_quantity and reserved_stock
            conn.execute(
                'UPDATE Drinks SET stock_quantity = stock_quantity - 1, reserved_stock = reserved_stock - 1 WHERE drink_id = ?', (drink_id,))
            # Update order status
            conn.execute('UPDATE Orders SET order_status = ? WHERE order_id = ? AND user_id = ?',
                         ('collected', order_id, session['user_id']))
            conn.commit()
            conn.close()
            return redirect(url_for('inbox'))
        else:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('homepage'))


@app.route('/manage_emails', methods=['GET', 'POST'])
def manage_emails():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    emails = get_all_emails()
    return render_template('manage_emails.html', emails=emails)


@app.route('/add_email', methods=['POST'])
def add_email():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    email_address = request.form['email_address']
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO Emails (email_address) VALUES (?)', (email_address,))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle case where email already exists
        pass
    finally:
        conn.close()
    return redirect(url_for('manage_emails'))


@app.route('/delete_email/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM Emails WHERE email_id = ?', (email_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('manage_emails'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
