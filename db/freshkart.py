import sqlite3

conn = sqlite3.connect('db/freshkart.db')
c = conn.cursor()

c.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    image_url TEXT,
    description TEXT,
    price REAL,
    stock INTEGER
)
''')

conn.commit()
conn.close()
