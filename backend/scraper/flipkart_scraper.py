# flipkart_scraper.py
import sys
sys.stdout.reconfigure(encoding='utf-8')  # ensure UTF-8 output (safe for most terminals)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os

def scrape_flipkart(product_name):
    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")   # run without window
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    try:
        # search URL
        query = product_name.replace(" ", "+")
        url = f"https://www.flipkart.com/search?q={query}"
        print(f"[INFO] Fetching URL: {url}")

        driver.get(url)
        time.sleep(5)  # allow page to load

       
        soup = BeautifulSoup(driver.page_source, "html.parser")

        
        product_blocks = soup.select("div._75nlfW, div._1AtVbE")

        results = []
        for block in product_blocks:
            name = block.select_one("a.IRpwTa, a.s1Q9rs, div.KzDlHZ, ._4rR01T")
            price = block.select_one("div._30jeq3, div.Nx9bqj")
            if name and price:
                results.append({
                    "name": name.text.strip(),
                    "price": price.text.replace("₹", "").replace(",", "").strip()
                })

        print(f"[INFO] Found {len(results)} products from Flipkart.")
        return results

    except Exception as e:
        print("[ERROR] While scraping Flipkart:", e)
        return []

    finally:
        driver.quit()
