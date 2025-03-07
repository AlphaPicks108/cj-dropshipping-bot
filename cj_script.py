import requests
import time
import sys
import os  # Import os to use GitHub Secrets

# Set the correct API endpoint
url = 'https://developers.cjdropshipping.com/api2.0/v1/product/list'

# Get API token from GitHub Secrets
API_TOKEN = os.getenv("CJ_API_TOKEN")

# Check if API token is available
if not API_TOKEN:
    print("❌ ERROR: API token is missing! Add it in GitHub Secrets.")
    sys.exit(1)

# Create a session
session = requests.Session()
session.headers.update({
    'CJ-Access-Token': API_TOKEN,
    'Content-Type': 'application/json',
})

# Countdown timer function (10 seconds)
def countdown_timer(seconds, message):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ {message} ({remaining}s remaining) ")
        sys.stdout.flush()
        time.sleep(1)
    print("\n🚀 Proceeding...")

# Function to fetch all products
def fetch_all_products():
    all_products = []
    page = 1
    page_size = 100  # ✅ Fixed pageSize to fetch 100 products per page

    while True:
        print(f"\n🔄 Fetching Page {page}...", end="", flush=True)

        params = {'page': page, 'pageSize': page_size}  # ✅ Correct parameter

        try:
            response = session.get(url, headers=session.headers, params=params, timeout=60)  
            response.raise_for_status()  
        except requests.exceptions.Timeout:
            print("\n⏳ API timeout! Retrying in 5 minutes...", flush=True)
            countdown_timer(300, "Waiting 5 minutes due to timeout")  
            continue
        except requests.exceptions.RequestException as e:
            print(f"\n❌ ERROR: {e}. Retrying in 5 minutes...", flush=True)
            countdown_timer(300, "Waiting 5 minutes before retrying")  
            continue

        if response.status_code == 200:
            data = response.json()

            # Debugging: Print raw response for verification
            print(f"\n🟢 RAW RESPONSE: {data}")

            products = data.get('data', {}).get('list', [])

            if not products:
                print("\n✅ No more products found. Stopping...", flush=True)
                break  

            all_products.extend(products)
            print(f"✅ Successfully fetched {len(products)} products from Page {page}", flush=True)

            # Display fetched products
            for index, product in enumerate(products, start=1):
                print(f"""
                📌 **Product {index}**  
                - **Name:** {product.get('productNameEn', 'N/A')}
                - **SKU:** {product.get('productSku', 'N/A')}
                - **Price:** ${product.get('sellPrice', 'N/A')}
                - **Category:** {product.get('categoryName', 'N/A')}
                - **Image URL:** {product.get('productImage', 'N/A')}
                """)

            page += 1  
            countdown_timer(10, "Waiting before next page request")  # ✅ Changed to 10s

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
products = fetch_all_products()

# Show final results
if products:
    print(f"\n✅ Total products fetched: {len(products)}\n", flush=True)
else:
    print("\n⚠ No products were fetched. Please check your API token and rate limits.", flush=True)
