
from flask import Flask, render_template, request, redirect, session, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'freshkart_super_secure_key_2025'
DATABASE = os.path.join('db', 'freshkart.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template('products.html', products=products)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    session['cart'] = cart
    return redirect(url_for('products'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    product_ids = list(cart.keys())
    cur = get_db().cursor()

    if product_ids:
        placeholders = ','.join('?' for _ in product_ids)
        cur.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", product_ids)
        products = cur.fetchall()
    else:
        products = []

    cart_items = []
    total = 0
    for product in products:
        qty = cart[str(product[0])]
        subtotal = qty * product[4]
        total += subtotal
        cart_items.append((product, qty, subtotal))

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        cur = get_db().cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            get_db().commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username or email already exists"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = get_db().cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            return "Invalid email or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

