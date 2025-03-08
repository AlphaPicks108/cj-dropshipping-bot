import requests
import time
import os

# Fetch API key from GitHub secret
api_key = os.getenv('PRINTROVE_API_KEY')

# Printrove API URL (adjust the URL as per Printrove API documentation)
BASE_URL = "https://api.printrove.com/v1/products"  # Example URL, replace with the actual endpoint

# Function to fetch product IDs
def fetch_product_ids(page):
    product_ids = []
    params = {
        'page': page,
        'api_key': api_key  # Ensure the API key is passed in the request
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        products = data.get('products', [])

        for product in products:
            product_ids.append(product.get('id'))

        return product_ids

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save product IDs to file (appending to existing file)
def save_product_ids(product_ids):
    with open('product_ids.txt', 'a') as f:
        for product_id in product_ids:
            f.write(f"{product_id}\n")

# Main function to run the script and fetch product IDs from all pages
def main():
    page = 1
    while True:
        print(f"Fetching data for page {page}...")
        product_ids = fetch_product_ids(page)
        
        if not product_ids:
            print("No more products found. Exiting...")
            break
        
        save_product_ids(product_ids)
        print(f"Saved {len(product_ids)} product IDs from page {page}.")

        page += 1
        time.sleep(15)  # Wait for 15 seconds before fetching next page

if __name__ == "__main__":
    main()
