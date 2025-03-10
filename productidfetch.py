import requests
import time
import os
import sys

# ✅ Printrove API URLs
AUTH_URL = "https://api.printrove.com/api/external/token"
PRODUCT_CATALOG_URL = "https://api.printrove.com/api/external/product-catalog"  # ✅ Corrected endpoint

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
        
        if not response.text:
            print("❌ ERROR: Empty response from authentication API.")
            sys.exit(1)

        data = response.json()
        token = data.get("access_token")

        if not token:
            print(f"❌ ERROR: Authentication failed. API Response: {data}")
            sys.exit(1)

        print("✅ Authentication successful!")
        return token

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to get authentication token - {e}")
        sys.exit(1)

# ✅ Function to fetch available products from Printrove
def fetch_product_catalog(token):
    product_ids = []
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(PRODUCT_CATALOG_URL, headers=headers)
        response.raise_for_status()

        if not response.text:
            print("❌ ERROR: Empty response from product catalog API.")
            sys.exit(1)

        data = response.json()
        print(f"📢 API Response:", data)  # ✅ Print full response for debugging

        products = data.get("result", [])
        if not products:
            print("❌ ERROR: Printrove API returned an empty product catalog.")
            sys.exit(1)

        for product in products:
            product_ids.append(product.get("id"))

        return product_ids

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP ERROR {response.status_code}: {response.text}")
        sys.exit(1)

    except requests.exceptions.JSONDecodeError:
        print(f"❌ ERROR: Printrove API returned a non-JSON response. Raw output:\n{response.text}")
        sys.exit(1)

# ✅ Function to save product IDs
def save_product_ids(product_ids):
    with open('product_ids.txt', 'w') as f:  # ✅ Overwrite to avoid duplicates
        for product_id in product_ids:
            f.write(f"{product_id}\n")

# ✅ Main function
def main():
    print("🔄 Getting authentication token...")
    token = get_auth_token()
    
    print(f"🔄 Fetching all available products from Printrove...")
    product_ids = fetch_product_catalog(token)

    save_product_ids(product_ids)
    print(f"✅ Saved {len(product_ids)} product IDs.")

if __name__ == "__main__":
    main()
