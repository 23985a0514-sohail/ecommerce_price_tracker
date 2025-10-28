import sqlite3

def init_db():
    conn = sqlite3.connect("data/prices.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT,
                    product TEXT,
                    price REAL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def insert_price(site, product, price):
    conn = sqlite3.connect("data/prices.db")
    c = conn.cursor()
    c.execute("INSERT INTO prices (site, product, price) VALUES (?, ?, ?)", (site, product, price))
    conn.commit()
    conn.close()
