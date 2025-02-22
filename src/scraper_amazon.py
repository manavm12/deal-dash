import requests
from bs4 import BeautifulSoup

def scrape_amazon_sg(search_query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    search_query = search_query.replace(' ', '+')
    url = f"https://www.amazon.sg/s?k={search_query}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve Amazon data: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    results = soup.find_all('div', {'data-component-type': 's-search-result'})[:5]
    for item in results:
        try:

            name_tag = item.h2
            name = name_tag.text.strip() if name_tag else "Product name not found"

            link_tag = item.find('a', class_='a-link-normal', href=True)
            link = "https://www.amazon.sg" + link_tag['href'] if link_tag else "Link not available"

            price_whole = item.find('span', class_='a-price-whole')
            price_fraction = item.find('span', class_='a-price-fraction')
            if price_whole and price_fraction:
                price = f"SGD {price_whole.text}{price_fraction.text}"
            else:
                price = "Price not available"

            delivery = item.find('span', class_='a-color-base a-text-bold')
            delivery_time = delivery.text.strip() if delivery else "Delivery info not available"

            image_tag = item.find('img', class_='s-image')
            image_url = image_tag['src'] if image_tag else "Image not available"

            deal_tag = item.find('div', class_='a-row a-size-base a-color-secondary')
            deal_info = deal_tag.get_text(strip=True) if deal_tag else "No deal"


            products.append({
                'name': name,
                'price': price,
                'link': link,
                'delivery_time': delivery_time,
                'image_url': image_url,
                'deal_info': deal_info
            })

        except Exception as e:
            print(f"Error extracting product data: {e}")
            continue

    return products

if __name__ == "__main__":
    query = input("Enter a product to search on Amazon SG: ")
    results = scrape_amazon_sg(query)
    for idx, product in enumerate(results, 1):
        print(f"\nProduct {idx}:")
        print(f"Name: {product['name']}")
        print(f"Price: {product['price']}")
        print(f"Link: {product['link']}")
        print(f"Delivery Time: {product['delivery_time']}")
        print(f"Image URL: {product['image_url']}")
        print(f"Deal Info: {product['deal_info']}")
