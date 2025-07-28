from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_file
from datetime import timedelta, datetime
from reportlab.pdfgen import canvas
import sqlite3
import os
import io

app = Flask(__name__)
app.secret_key = 'freshkart_super_secure_key_2025'
app.permanent_session_lifetime = timedelta(days=30)
DATABASE = os.path.join('db', 'freshkart.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()

# ------------------------ PUBLIC ROUTES ------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')

        cur = get_db().cursor()
        cur.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

        if user and password == user[1]:  # Replace with hashed check in prod
            session['user_id'] = user[0]
            session.permanent = True if remember else False
            flash("Login successful", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = get_db().cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            flash("Email already registered", "warning")
            return redirect(url_for('register'))

        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        get_db().commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cur = get_db().cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user:
            session['reset_email'] = email
            return redirect(url_for('reset_password'))
        else:
            flash("Email not found", "danger")
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        flash("Invalid access to reset page", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        email = session['reset_email']
        cur = get_db().cursor()
        cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
        get_db().commit()
        session.pop('reset_email', None)
        flash("Password reset successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html')

# ------------------------ PRODUCT AND CART ROUTES ------------------------

@app.route('/products')
def products():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM products")
    raw_products = cur.fetchall()

    # Safely parse
    products = []
    for product in raw_products:
        stock = int(product[5]) if product[5] else 0
        price = float(product[4]) if product[4] else 0.0
        discount = int(product[6]) if product[6] else 0
        discounted_price = price - (price * discount / 100)

        products.append({
            "id": product[0],
            "name": product[1],
            "image": product[2],
            "description": product[3],
            "price": price,
            "stock": stock,
            "discount": discount,
            "brand": product[7],
            "category": product[8],
            "discounted_price": round(discounted_price, 2)
        })

    return render_template("products.html", products=products)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    session['cart'] = cart
    flash("Item added to cart", "success")
    return redirect(url_for('products'))

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        session['cart'] = cart
        flash("Item removed from cart", "info")
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
    total = 0.0

    for product in products:
        pid = str(product[0])
        qty = cart.get(pid, 0)

        price = float(product[4]) if product[4] else 0.0
        discount = int(product[6]) if product[6] else 0
        discounted_price = price - (price * discount / 100)
        subtotal = qty * discounted_price
        total += subtotal

        cart_items.append({
            "id": product[0],
            "name": product[1],
            "image": product[2],
            "qty": qty,
            "discounted_price": round(discounted_price, 2),
            "subtotal": round(subtotal, 2)
        })

    return render_template("cart.html", cart_items=cart_items, total=round(total, 2))



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        return redirect(url_for('generate_invoice', name=name, address=address, email=email))

    # Rebuild cart for preview
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
    total = 0.0

    for product in products:
        pid = str(product[0])
        qty = cart.get(pid, 0)
        price = float(product[4])
        discount = float(product[6]) if product[6] else 0.0
        discounted_price = price - (price * discount / 100)
        subtotal = qty * discounted_price
        total += subtotal
        cart_items.append((product, qty, round(subtotal, 2), round(discounted_price, 2)))

    return render_template('checkout.html', cart_items=cart_items, total=round(total, 2))


@app.route('/generate-invoice')
def generate_invoice():
    name = request.args.get('name')
    address = request.args.get('address')
    email = request.args.get('email')

    cart = session.get('cart', {})
    product_ids = list(cart.keys())
    cur = get_db().cursor()

    if not product_ids:
        flash("Cart is empty.", "warning")
        return redirect(url_for('products'))

    placeholders = ','.join('?' for _ in product_ids)
    cur.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", product_ids)
    products = cur.fetchall()

    cart_items = []
    total = 0.0
    for product in products:
        product_id = str(product[0])
        qty = cart[product_id]
        price = product[4]
        discount = product[6] or 0
        discounted_price = price - (price * discount / 100)
        subtotal = qty * discounted_price
        total += subtotal
        cart_items.append((product[1], qty, discounted_price, subtotal))

    invoice_path = f"static/invoices/invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)

    p = canvas.Canvas(invoice_path)
    p.setTitle("FreshKart Invoice")
    p.drawString(50, 800, f"Invoice for {name}")
    p.drawString(50, 785, f"Address: {address}")
    p.drawString(50, 770, f"Email: {email}")
    p.drawString(50, 750, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 720
    p.drawString(50, y, "Item")
    p.drawString(250, y, "Qty")
    p.drawString(300, y, "Unit Price")
    p.drawString(400, y, "Subtotal")
    y -= 20

    for item, qty, unit_price, subtotal in cart_items:
        p.drawString(50, y, item)
        p.drawString(250, y, str(qty))
        p.drawString(300, y, f"₹{unit_price:.2f}")
        p.drawString(400, y, f"₹{subtotal:.2f}")
        y -= 20

    y -= 10
    p.drawString(300, y, "Total:")
    p.drawString(400, y, f"₹{total:.2f}")
    p.showPage()
    p.save()

    session['cart'] = {}
    flash("Order placed successfully!", "success")

    return redirect(url_for('order_confirmation', invoice=invoice_path, name=name))

@app.route('/order-confirmation')
def order_confirmation():
    invoice = request.args.get('invoice')
    name = request.args.get('name')
    return render_template('order_confirmation.html', invoice=invoice, name=name)

if __name__ == '__main__':
    app.run(debug=True)
