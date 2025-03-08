import requests
import time
import os

# AOP+ API URL and Token
API_URL = "https://api.aopplus.com/v1/products"
API_KEY = "API@CJ4086585@CJ:eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyMzgxMSIsInR5cGUiOiJBQ0NFU1NfVE9LRU4iLCJzdWIiOiJicUxvYnFRMGxtTm55UXB4UFdMWnlqYTMzeXF5L2RiTXkxZFdqcW9DWm9kRXlQVVQvR2ZxN2l0VHJjbUhhL1g4cE42QmRybUI3VWNuaXRaZkZrNHNuOWxnZVNFbEY1VXJzTnpjK1A4enlMc0FkZzJJaklBTmpNS0lQbWR1dTkvNWRNbUI2NjhIUFl1S3RaSndSMUNlMkJCNVdRMXpWMEI4YmJ6UUlHUnNJRExjeTl4YWY1ZjU0OHc5K1VRTm1yL0Qwa1NkMkE4VThkUEhuWE10eDNlWVZRK1NIa3dReG52R1NSeUU2dmFhR09sNE40MllKQlBKR2tDRGQyK0VJRXBhN3orRGVVdFJiZXFQcFlKQnR0TWJDR0VFWDdET3lITy9mZm1QZldjWGJjcitqTG5DMjdqd3ZyQUVHenNGYnlkZSIsImlhdCI6MTc0MTI2MzQwNH0.doVaSAWwCe4Wm3dR5NCM5WXBKFDtqMR2y3E4TcilYao"

# Set a maximum runtime limit (in seconds). For example, 5 hours (5 * 60 * 60 = 18000 seconds)
TIME_LIMIT = 5 * 60 * 60  # 5 hours
start_time = time.time()

# Function to fetch products from AOP+ API
def fetch_products(page=1):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "page": page,
        "limit": 50  # Fetch 50 products per page
    }
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching products: {response.status_code}")
        return []

    products = response.json().get("data", [])
    return products

# Function to fetch product IDs from each page
def fetch_product_ids():
    page = 1
    all_product_ids = []

    while True:
        # Check if the script has exceeded the time limit
        if time.time() - start_time > TIME_LIMIT:
            print("Time limit exceeded. Stopping the script.")
            break
        
        print(f"Fetching products from page {page}...")
        products = fetch_products(page)
        
        if not products:
            print("No more products found. Exiting.")
            break
        
        # Extract product IDs from the products
        product_ids = [product.get("id") for product in products]
        print(f"Product IDs on page {page}: {product_ids}")
        
        # Save product IDs to a list (all_product_ids will collect all)
        all_product_ids.extend(product_ids)
        
        # Move to the next page
        page += 1
        time.sleep(15)  # 15-second break before fetching the next page

    # Return the list of all product IDs
    return all_product_ids

# Function to save product IDs to an artifact file
def save_product_ids(product_ids):
    file_path = "/github/workspace/product_ids.txt"
    
    # Check if the file already exists to append data (to avoid overwriting)
    if os.path.exists(file_path):
        with open(file_path, "a") as f:
            for product_id in product_ids:
                f.write(f"{product_id}\n")
    else:
        # If the file does not exist, create and write data
        with open(file_path, "w") as f:
            for product_id in product_ids:
                f.write(f"{product_id}\n")

# Main function to start fetching product IDs
def main():
    product_ids = fetch_product_ids()
    save_product_ids(product_ids)
    print(f"Total {len(product_ids)} product IDs fetched and saved.")

if __name__ == "__main__":
    main()
