import requests
import time
import os

# Get Printful API Token from GitHub Secrets
api_token = os.getenv('PRINTFUL_API_TOKEN')

# Ensure the token is retrieved
if not api_token:
    print("Error: PRINTFUL_API_TOKEN is missing. Set it in GitHub Secrets.")
    exit(1)

# Printful API URL for Store Products
BASE_URL = "https://api.printful.com/store/products"

# ✅ Correct Headers for Bearer Authentication
HEADERS = {
    "Authorization": f"Bearer {api_token}",  # ✅ Use Bearer token format
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
        response.raise_for_status()  # Raise an error for 401, 403, etc.

        data = response.json()
        products = data.get('result', [])

        for product in products:
            product_ids.append(product.get('id'))

        return product_ids

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error: Unauthorized. Check if PRINTFUL_API_TOKEN is correct and in Bearer format.")
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
