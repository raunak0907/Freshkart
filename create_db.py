import sqlite3
import os

DB_PATH = os.path.join('db', 'freshkart.db')
os.makedirs('db', exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop old tables if needed (optional safety for rebuild)
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("DROP TABLE IF EXISTS products")

# Create products table
cur.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    discount INTEGER DEFAULT 0,
    brand TEXT,
    category TEXT
)
''')

# Create users table
cur.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert 30 product records
products = [
    # Fruits
    ("Bananas", "https://i.imgur.com/0umadnY.jpg", "Fresh organic bananas", 50, 100, 10, "FreshKart", "Fruits"),
    ("Apples", "https://i.imgur.com/eTmWoAN.png", "Crisp red apples", 120, 80, 5, "Himalayan Fresh", "Fruits"),
    ("Oranges", "https://i.imgur.com/8zQHrAh.png", "Juicy Nagpur oranges", 90, 70, 0, "FarmVille", "Fruits"),
    ("Pineapple", "https://i.imgur.com/rJwj1ss.png", "Tropical golden pineapple", 60, 50, 10, "FruitNest", "Fruits"),
    ("Papaya", "https://i.imgur.com/xAuhNV3.png", "Healthy ripe papaya", 45, 60, 0, "HealthFarm", "Fruits"),
    
    # Vegetables
    ("Tomatoes", "https://i.imgur.com/4i5nNMG.png", "Red cooking tomatoes", 30, 150, 5, "GreenKart", "Vegetables"),
    ("Potatoes", "https://i.imgur.com/tHG3mZG.png", "Starchy Indian potatoes", 25, 200, 0, "GreenKart", "Vegetables"),
    ("Onions", "https://i.imgur.com/yz3O3bP.png", "Fresh red onions", 35, 180, 0, "GreenKart", "Vegetables"),
    ("Cabbage", "https://i.imgur.com/KV6e94L.png", "Green leafy cabbage", 40, 100, 10, "GreenKart", "Vegetables"),
    ("Carrots", "https://i.imgur.com/U7x7qUO.png", "Orange baby carrots", 50, 90, 5, "GreenKart", "Vegetables"),

    # Dairy
    ("Amul Milk 1L", "https://i.imgur.com/milk.png", "Full cream milk", 60, 120, 0, "Amul", "Dairy"),
    ("Mother Dairy Curd", "https://i.imgur.com/dairy.png", "Fresh thick curd", 55, 100, 5, "Mother Dairy", "Dairy"),
    ("Paneer 200g", "https://i.imgur.com/qFZ1p6B.png", "Soft paneer cubes", 90, 80, 10, "Gowardhan", "Dairy"),

    # Snacks
    ("Maggie Noodles", "https://i.imgur.com/maggie.png", "2-min tasty noodles", 95, 120, 5, "Nestle", "Snacks"),
    ("Lays Chips", "https://i.imgur.com/lays.png", "Classic salted chips", 20, 300, 0, "PepsiCo", "Snacks"),
    ("Kurkure Masala", "https://i.imgur.com/kurkure.png", "Spicy crunchy snack", 25, 250, 5, "PepsiCo", "Snacks"),

    # Beverages
    ("Pepsi 1.25L", "https://i.imgur.com/pepsi.png", "Chilled cola drink", 45, 200, 0, "PepsiCo", "Beverages"),
    ("Real Orange Juice", "https://i.imgur.com/realjuice.png", "100% orange juice", 110, 70, 10, "Dabur", "Beverages"),
    ("Bru Coffee", "https://i.imgur.com/bru.png", "Instant strong coffee", 145, 40, 15, "Nestle", "Beverages"),

    # Grocery
    ("Tata Salt", "https://i.imgur.com/salt.png", "Iodized cooking salt", 28, 100, 0, "Tata", "Groceries"),
    ("Aashirvaad Atta 5kg", "https://i.imgur.com/atta.png", "High-fiber wheat flour", 265, 60, 10, "ITC", "Groceries"),
    ("Basmati Rice 1kg", "https://i.imgur.com/rice.png", "Aromatic long grain rice", 105, 90, 0, "IndiaGate", "Groceries"),

    # Personal Care
    ("Dove Shampoo", "https://i.imgur.com/shampoo.png", "Silky smooth shampoo", 220, 60, 10, "Dove", "Personal Care"),
    ("Colgate Toothpaste", "https://i.imgur.com/toothpaste.png", "Minty freshness toothpaste", 55, 140, 5, "Colgate", "Personal Care"),
    ("Dettol Soap Pack", "https://i.imgur.com/dettol.png", "Antibacterial soap", 75, 200, 15, "Dettol", "Personal Care"),

    # Household
    ("Surf Excel", "https://i.imgur.com/laundry.png", "Laundry detergent", 210, 80, 15, "Surf Excel", "Household"),
    ("Vim Dishwash", "https://i.imgur.com/vim.png", "Powerful grease cleaner", 45, 100, 5, "Vim", "Household"),
    ("Lizol Floor Cleaner", "https://i.imgur.com/lizol.png", "Antibac floor cleaner", 175, 90, 10, "Lizol", "Household"),

    # Spreads & Condiments
    ("Kissan Jam", "https://i.imgur.com/jam.png", "Mixed fruit jam", 85, 60, 10, "Kissan", "Spreads"),
    ("Nutella 350g", "https://i.imgur.com/nutella.png", "Hazelnut chocolate spread", 250, 50, 20, "Ferrero", "Spreads"),
    ("MDH Masala", "https://i.imgur.com/masala.png", "Mixed Indian spices", 65, 100, 0, "MDH", "Condiments")
]

cur.executemany('''
    INSERT INTO products (name, image, description, price, stock, discount, brand, category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', products)

conn.commit()
conn.close()

print("✅ freshkart.db created with 30 products and user table initialized.")
