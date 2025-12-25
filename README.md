# E-commerce Price Tracker

## Overview

E-commerce Price Tracker is a utility application that allows users to track the price of products on e-commerce websites.  
When the price of a tracked product falls below a desired value, users are notified (e.g., via email or log) so they can make a purchase at the best price.

The goal of this project is to automate price monitoring for online shoppers and help them save money by alerting them to price drops.



## Features

- Track real-time prices of products from popular e-commerce platforms
- Store tracked product details with desired price thresholds
- Fetch product price periodically (scheduled or manual)
- Notify user when current price is less than or equal to desired price
- Support for multiple e-commerce websites (e.g., Amazon, Flipkart)


## Technology Stack

- Python
- Web scraping with BeautifulSoup/requests
- Scheduler (cron/loop-based)
- Email Notification (SMTP) or console logs
- SQLite or local database


## Usage
Configure tracked products

Add products you want to track in the database or file (depending on your app’s setup).
Each entry should include:
- Product name
- Product URL
- Desired price


## How it Works (Behind The Scenes)

- The price tracker fetches the product page using HTTP requests.
- The webpage is parsed using BeautifulSoup to extract the latest price.
- The extracted price is compared with the user’s desired price.
- When the price meets the target condition, the app sends a notification.
