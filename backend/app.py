# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
from scraper.flipkart_scraper import scrape_flipkart
from apscheduler.schedulers.background import BackgroundScheduler
from performance_monitor import timing_decorator, get_performance_stats
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize caching and compression for performance
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 3600})
compress = Compress(app)

DB_PATH = "tracker.db"

# 🔹 Get full price history for a product
@app.route("/history/<product>", methods=["GET"])
@cache.cached(timeout=600, query_string=True)  # Cache for 10 minutes
@timing_decorator("/history/<product>")
def get_history(product):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT name, price, timestamp 
        FROM prices 
        WHERE product = ? 
        ORDER BY timestamp ASC
    """, (product,))
    rows = c.fetchall()
    conn.close()

    data = [
        {"name": r[0], "price": r[1], "timestamp": r[2]}
        for r in rows
    ]
    return jsonify(data)


# 🔹 Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            name TEXT,
            price TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()


# 🔹 Helper to insert scraped data
def save_to_db(product, results):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in results:
        c.execute(
            "INSERT INTO prices (product, name, price, timestamp) VALUES (?, ?, ?, ?)",
            (product, item.get("name"), item.get("price"), datetime.now())
        )
    conn.commit()
    conn.close()


# 🔹 Manual tracking endpoint
@app.route("/track", methods=["POST"])
@timing_decorator("/track")
def track():
    try:
        data = request.get_json(force=True)
        product_name = data.get("product")

        if not product_name:
            return jsonify({"error": "No product name provided"}), 400

        # Check cache first
        cache_key = f"scrape_{product_name}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print(f"[CACHE HIT] Using cached data for {product_name}")
            flipkart_data = cached_data
        else:
            print(f"[CACHE MISS] Scraping fresh data for {product_name}")
            flipkart_data = scrape_flipkart(product_name)
            cache.set(cache_key, flipkart_data, timeout=3600)  # Cache for 1 hour
        
        save_to_db(product_name, flipkart_data)
        return jsonify({"flipkart": flipkart_data})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


# 🔹 Get latest tracked products
@app.route("/latest", methods=["GET"])
@cache.cached(timeout=300)  # Cache for 5 minutes
@timing_decorator("/latest")
def get_latest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT product, name, price, timestamp 
        FROM prices 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    rows = c.fetchall()
    conn.close()

    data = [
        {"product": r[0], "name": r[1], "price": r[2], "timestamp": r[3]}
        for r in rows
    ]
    return jsonify(data)


# 🔹 Scheduled auto tracker
def scheduled_scrape():
    try:
        print("[CRON] Running scheduled scrape...")
        products = ["iphone", "laptop", "headphones"]
        for product in products:
            data = scrape_flipkart(product)
            save_to_db(product, data)
        print("[CRON] Scrape completed successfully.")
    except Exception as e:
        print("[CRON ERROR]", e)


# 🔹 Background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_scrape, "interval", hours=6)  # runs every 6 hours
scheduler.start()


# 🔹 Performance stats endpoint
@app.route("/performance", methods=["GET"])
def performance_stats():
    return jsonify(get_performance_stats())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
