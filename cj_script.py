import requests
import time
import sys
import os
import json

# Set API endpoint
url = 'https://developers.cjdropshipping.com/api2.0/v1/product/list'

# Get API token from GitHub Secrets
API_TOKEN = os.getenv("CJ_API_TOKEN")

# Check if API token is available
if not API_TOKEN:
    print("❌ ERROR: API token is missing! Add it in GitHub Secrets.")
    sys.exit(1)

# File to store fetched product IDs
FETCHED_PRODUCTS_FILE = "fetched_products.txt"

# Create a session
session = requests.Session()
session.headers.update({
    'CJ-Access-Token': API_TOKEN,
    'Content-Type': 'application/json',
})

# Load previously fetched product IDs
def load_fetched_products():
    if not os.path.exists(FETCHED_PRODUCTS_FILE):
        return set()
    with open(FETCHED_PRODUCTS_FILE, "r") as file:
        return set(file.read().splitlines())

# Save new fetched product IDs
def save_fetched_products(product_ids):
    with open(FETCHED_PRODUCTS_FILE, "a") as file:
        for product_id in product_ids:
            file.write(product_id + "\n")

# Countdown timer function (Now 10 seconds)
def countdown_timer(seconds, message):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ {message} ({remaining}s remaining) ")
        sys.stdout.flush()
        time.sleep(1)
    print("\n🚀 Proceeding...")

# Function to fetch new products only with backoff handling
def fetch_new_products():
    all_products = []
    fetched_products = load_fetched_products()
    page = 1
    page_size = 100  # ✅ Fetches 100 products per page
    max_retries = 5  # ✅ Maximum retry attempts for 429 errors
    retry_delay = 60  # ✅ Start with 60 seconds backoff

    while True:
        print(f"\n🔄 Fetching Page {page}...", flush=True)

        params = {'page': page, 'pageSize': page_size}  

        try:
            response = session.get(url, headers=session.headers, params=params, timeout=60)  
            response.raise_for_status()  
        except requests.exceptions.Timeout:
            print("\n⏳ API timeout! Retrying in 5 minutes...", flush=True)
            countdown_timer(300, "Waiting 5 minutes due to timeout")  
            continue
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:  # ✅ Handle rate limit errors
                print("\n❌ ERROR 429: Too Many Requests. Waiting before retrying...", flush=True)
                countdown_timer(retry_delay, f"Waiting {retry_delay} seconds due to API rate limit")  
                retry_delay *= 2  # ✅ Double wait time for next failure
                continue
            print(f"\n❌ ERROR: {e}. Retrying in 5 minutes...", flush=True)
            countdown_timer(300, "Waiting 5 minutes before retrying")  
            continue

        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('list', [])

            if not products:
                print("\n✅ No more products found. Stopping...", flush=True)
                break  

            new_products = []
            new_product_ids = []

            # Filter new products
            for product in products:
                product_id = product.get('productSku', 'N/A')
                if product_id not in fetched_products:
                    new_products.append(product)
                    new_product_ids.append(product_id)

            if new_products:
                all_products.extend(new_products)
                save_fetched_products(new_product_ids)
                print(f"✅ Fetched {len(new_products)} new products from Page {page}", flush=True)

            page += 1  
            countdown_timer(10, "Waiting before next page request")  # ✅ Now 10s wait time

        elif response.status_code == 401:
            print("\n❌ ERROR: Invalid API token or session expired.", flush=True)
            print("🔄 Retrying in 1 hour...", flush=True)
            countdown_timer(3600, "Retrying after 1 hour")  
            continue  

        else:
            print(f"\n❌ ERROR: Status Code {response.status_code}, Details: {response.text}", flush=True)
            break  

    return all_products  

# Run the function
products = fetch_new_products()

# Show final results
if products:
    print(f"\n✅ Total new products fetched: {len(products)}\n", flush=True)
else:
    print("\n⚠ No new products were fetched. Please check your API token and rate limits.", flush=True)
