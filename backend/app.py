from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.flipkart_scraper import scrape_flipkart
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/track", methods=["POST"])
def track():
    data = request.get_json()
    product_name = data.get("product")
    if not product_name:
        return jsonify({"error": "No product name provided"}), 400

    flipkart_data = scrape_flipkart(product_name)
    return jsonify({"flipkart": flipkart_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))