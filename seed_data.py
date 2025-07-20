import sqlite3

conn = sqlite3.connect('db/freshkart.db')
c = conn.cursor()

sample_products = [
    ("Organic Apples", "https://via.placeholder.com/300", "Fresh organic apples from Himachal", 120.00, 50),
    ("Brown Bread", "https://via.placeholder.com/300", "Whole wheat brown bread (400g)", 45.00, 30),
    ("Almonds 250g", "https://via.placeholder.com/300", "Premium quality almonds", 190.00, 20),
    ("Full Cream Milk", "https://via.placeholder.com/300", "Amul full cream milk 1L", 60.00, 100),
    ("Aashirvaad Atta", "https://via.placeholder.com/300", "Wheat flour 5kg pack", 260.00, 40)
]

c.executemany('''
INSERT INTO products (name, image_url, description, price, stock)
VALUES (?, ?, ?, ?, ?)
''', sample_products)

conn.commit()
conn.close()

print("✅ Sample products inserted into the database.")
