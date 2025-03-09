import requests
import time
import os
import sys

# ✅ Printrove API URLs
AUTH_URL = "https://api.printrove.com/api/external/token"
PRODUCTS_URL = "https://api.printrove.com/api/external/products"

# ✅ Get login credentials from GitHub Secrets
EMAIL = os.getenv('PRINTROVE_EMAIL')
PASSWORD = os.getenv('PRINTROVE_PASSWORD')

# ✅ Function to get authentication token
def get_auth_token():
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(AUTH_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("access_token")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to get authentication token - {e}")
        sys.exit(1)

# ✅ Function to fetch product IDs
def fetch_product_ids(token, page=1, per_page=20):
    product_ids = []
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "page": str(page),
        "per_page": str(per_page)
    }

    try:
        response = requests.get(PRODUCTS_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        products = data.get("result", [])
        for product in products:
            product_ids.append(product.get("id"))

        return product_ids

    except requests.exceptions.HTTPError as e:
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
        print(f"❌ ERROR: {response.status_code} - {error_message}")
        return []

# ✅ Function to save product IDs
def save_product_ids(product_ids):
    with open('product_ids.txt', 'a') as f:
        for product_id in product_ids:
            f.write(f"{product_id}\n")

# ✅ Main function
def main():
    print("🔄 Getting authentication token...")
    token = get_auth_token()
    
    page = 1
    per_page = 20  # ✅ Printrove only allows max 20 per page

    while True:
        print(f"🔄 Fetching products (Page {page})...")
        product_ids = fetch_product_ids(token, page, per_page)

        if not product_ids:
            print("✅ No more products found. Exiting...")
            break

        save_product_ids(product_ids)
        print(f"✅ Saved {len(product_ids)} product IDs.")

        page += 1  # ✅ Move to next page
        time.sleep(15)  # ✅ Avoid rate limiting

if __name__ == "__main__":
    main()
