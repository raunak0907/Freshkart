import sqlite3
conn = sqlite3.connect('db/freshkart.db')
cur = conn.cursor()

# Drop & recreate table
cur.execute('DROP TABLE IF EXISTS products')
cur.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    description TEXT,
    price REAL NOT NULL,
    category TEXT,
    stock INTEGER DEFAULT 0,
    discount INTEGER DEFAULT 0,
    brand TEXT
)
''')

# Insert data
products = [
    ('Fresh Apples', 'https://i.imgur.com/eTmWoAN.png', 'Crisp and juicy apples from Himachal', 120, 'Fruits', 100, 10, 'Himachal Farms'),
    ('Organic Bananas', 'https://i.imgur.com/9z1bKVe.jpg', 'Rich in potassium and fibre', 80, 'Fruits', 80, 5, 'Nature’s Basket'),
    ('Desi Potatoes', 'https://i.imgur.com/o8cd5bC.jpg', 'Farm-fresh potatoes for daily use', 60, 'Vegetables', 120, 0, 'Local Farmer'),
    ('Amul Milk 1L', 'https://i.imgur.com/xZ4yKyU.png', 'Full cream packaged milk', 56, 'Dairy', 150, 8, 'Amul'),
    ('Mother Dairy Paneer', 'https://i.imgur.com/U6aYoGJ.jpg', 'Soft & creamy 200g paneer', 95, 'Dairy', 90, 5, 'Mother Dairy'),
    ('Fortune Mustard Oil', 'https://i.imgur.com/SlxijHa.jpg', 'Pure cold-pressed mustard oil - 1L', 140, 'Staples', 60, 15, 'Fortune'),
    ('Aashirvaad Atta 5kg', 'https://i.imgur.com/MczFZGK.jpg', '100% whole wheat flour', 280, 'Staples', 70, 10, 'Aashirvaad'),
    ('Tata Salt 1kg', 'https://i.imgur.com/f8kDBoH.jpg', 'Iodized salt for daily cooking', 22, 'Staples', 200, 0, 'Tata'),
    ('Maggi 2-Min Noodles', 'https://i.imgur.com/jJjKnDl.jpg', 'Pack of 4 instant noodles', 52, 'Snacks', 180, 12, 'Nestlé'),
    ('Parle-G Biscuits', 'https://i.imgur.com/IYK6A7K.jpg', 'Family pack of classic glucose biscuits', 40, 'Snacks', 220, 0, 'Parle'),
    ('Surf Excel Quick Wash 1kg', 'https://i.imgur.com/MqDHDsp.jpg', 'Effective stain removal detergent', 210, 'Home Care', 75, 20, 'HUL'),
    ('Tropicana Orange Juice', 'https://i.imgur.com/JYPhDAS.jpg', '1L fresh orange juice', 110, 'Beverages', 60, 10, 'Tropicana'),
    ('Red Onions 1kg', 'https://i.imgur.com/EyZzvV6.jpg', 'Fresh pungent onions from Nashik', 48, 'Vegetables', 130, 0, 'Local Farmer'),
    ('Tomatoes 1kg', 'https://i.imgur.com/KZuSdcg.jpg', 'Ripe, red tomatoes for everyday cooking', 35, 'Vegetables', 115, 0, 'Local Farmer'),
    ('Britannia Cheese Slices', 'https://i.imgur.com/VpHPWMT.jpg', '12 slices of creamy cheese', 95, 'Dairy', 85, 5, 'Britannia')
]

cur.executemany('''
    INSERT INTO products (name, image, description, price, category, stock, discount, brand)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', products)

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
