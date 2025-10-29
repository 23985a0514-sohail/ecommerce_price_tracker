from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.flipkart_scraper import scrape_flipkart
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running"}), 200


@app.route("/track", methods=["POST"])
def track():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)  # 🔍 Debugging
        product_name = data.get("product")

        if not product_name:
            return jsonify({"error": "No product name provided"}), 400

        flipkart_data = scrape_flipkart(product_name)
        print("Scraped data:", flipkart_data)  # 🔍 Debugging

        return jsonify({"flipkart": flipkart_data})
    except Exception as e:
        print("Error:", str(e))  # 🔍 Log error in Render console
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
