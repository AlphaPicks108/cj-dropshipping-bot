import requests
import time
import os

# Get Printful Access Key from GitHub Secrets
api_token = os.getenv('PRINTFUL_API_TOKEN')

# Printful API URL for Store Products
BASE_URL = "https://api.printful.com/store/products"

# Headers with Access Key
HEADERS = {
    "Authorization": api_token,  # Directly pass the key (No "Bearer" needed)
    "Content-Type": "application/json"
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

# Function to save product IDs (append to file)
def save_product_ids(product_ids):
    with open('product_ids.txt', 'a') as f:
        for product_id in product_ids:
            f.write(f"{product_id}\n")

# Main function
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
