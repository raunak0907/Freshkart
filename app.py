from flask import Flask, render_template, g, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Replace with a secure value
DATABASE = os.path.join('db', 'freshkart.db')

# ---------- Database Connection ---------- #
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

# ---------- Routes ---------- #

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template('products.html', products=products)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('products'))

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        session['cart'] = cart
    return redirect(url_for('view_cart'))

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
        pid = str(product[0])
        qty = cart[pid]
        subtotal = product[4] * qty
        total += subtotal
        cart_items.append((product, qty, subtotal))

    return render_template('cart.html', cart_items=cart_items, total=total)

# ---------- Main ---------- #
if __name__ == '__main__':
    app.run(debug=True)
