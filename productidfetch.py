import requests
import time
import os
import sys  # ✅ Needed to exit on fatal errors

# Get Printful API Token from GitHub Secrets
api_token = os.getenv('PRINTFUL_API_TOKEN')

# Ensure the token is retrieved
if not api_token:
    print("❌ ERROR: PRINTFUL_API_TOKEN is missing. Set it in GitHub Secrets.")
    sys.exit(1)  # ✅ Stop execution if no token

# Printful API URL for Store Products
BASE_URL = "https://api.printful.com/store/products"

# ✅ Correct Headers for Bearer Authentication
HEADERS = {
    "Authorization": f"Bearer {api_token}",
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
        response.raise_for_status()  # Raise error for 400, 401, etc.

        data = response.json()
        products = data.get('result', [])

        for product in products:
            product_ids.append(product.get('id'))

        return product_ids

    except requests.exceptions.HTTPError as e:
        # ✅ Capture the exact API error from Printful
        try:
            error_response = response.json()
            error_code = error_response.get('code', 'Unknown Code')
            error_message = error_response.get('error', {}).get('message', 'No message provided')
        except Exception:
            error_code = response.status_code
            error_message = "Invalid API response format"

        print(f"❌ ERROR {error_code}: {error_message}")  # ✅ Logs exact issue in GitHub Actions
        sys.exit(1)  # ✅ Stop execution if API request fails

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
        print(f"🔄 Fetching products with offset {offset}...")
        product_ids = fetch_product_ids(offset, limit)

        if not product_ids:
            print("✅ No more products found. Exiting...")
            break

        save_product_ids(product_ids)
        print(f"✅ Saved {len(product_ids)} product IDs.")

        offset += limit  # Move to next batch
        time.sleep(15)  # Avoid rate limiting

if __name__ == "__main__":
    main()
