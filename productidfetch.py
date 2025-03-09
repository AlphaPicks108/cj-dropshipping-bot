import requests
import time
import os

# Fetch API key from GitHub secrets
api_key = os.getenv('PRINTFUL_API_KEY')

# Base URL for Printful API
BASE_URL = "https://api.printful.com/products"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {api_key}"
}

# Function to fetch product IDs
def fetch_product_ids(offset=0, limit=50):
    product_ids = []
    params = {
        "offset": offset,
        "limit": limit
    }

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()
        products = data.get('result', [])

        for product in products:
            product_ids.append(product.get('id'))

        return product_ids

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save product IDs (append to existing file)
def save_product_ids(product_ids):
    with open('product_ids.txt', 'a') as f:
        for product_id in product_ids:
            f.write(f"{product_id}\n")

# Main function to fetch and save product IDs
def main():
    offset = 0
    limit = 50

    while True:
        print(f"Fetching products with offset {offset}...")
        product_ids = fetch_product_ids(offset, limit)

        if not product_ids:
            print("No more products found. Exiting...")
            break

        save_product_ids(product_ids)
        print(f"Saved {len(product_ids)} product IDs.")

        offset += limit  # Move to next batch
        time.sleep(15)  # Avoid rate limiting

if __name__ == "__main__":
    main()
