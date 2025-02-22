import requests
from bs4 import BeautifulSoup
import random
import time

def scrape_ebay_simple(search_query):
    # Format search query for the URL
    search_query = search_query.replace(' ', '+')
    url = f"https://www.ebay.com.sg/sch/i.html?_nkw={search_query}&_sacat=0&_from=R40&_trksid=m570.l1313"

    # Set realistic browser headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    # Add random delay to mimic human behavior
    time.sleep(random.uniform(2, 5))

    # Make an HTTP GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code {response.status_code}")
        return []

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store scraped products
    products = []

    # Find product containers
    product_elements = soup.find_all("li", class_="s-item")[:10]  # Get top 10 products

    if not product_elements:
        print("No products found.")
        return []

    for product in product_elements:
        try:
            # Extract product name
            name_tag = product.find("h3", class_="s-item__title")
            name = name_tag.text.strip() if name_tag else "No name found"

            # Extract product price
            price_tag = product.find("span", class_="s-item__price")
            price = price_tag.text.strip() if price_tag else "No price found"

            # Extract product link
            link_tag = product.find("a", class_="s-item__link")
            link = link_tag["href"] if link_tag else "No link found"

            # Extract product image
            image_tag = product.find("img")
            if image_tag and image_tag.get("src"):
                image_url = image_tag["src"]
            else:
                image_url = "No image found"
            image_url = image_tag["src"] if image_tag else "No image found"

            # Append product details
            products.append({
                'name': name,
                'price': price,
                'link': link,
                'image_url': image_url
            })

        except Exception as e:
            print(f"Error extracting product data: {e}")
            continue

    return products

# Test the scraper
if __name__ == "__main__":
    query = input("Enter a product to search on eBay SG: ")
    results = scrape_ebay_simple(query)
    if results:
        for idx, product in enumerate(results, 1):
            print(f"\nProduct {idx}:")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"Link: {product['link']}")
            print(f"Image URL: {product['image_url']}")
    else:
        print("No products found or there was an error scraping data.")
