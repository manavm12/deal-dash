from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_lazada_sg(search_query):

    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    search_query = search_query.replace(' ', '%20')
    url = f"https://www.lazada.sg/catalog/?q={search_query}"

    driver.get(url)
    time.sleep(5)  

    products = []

    try:

        product_elements = driver.find_elements(By.CLASS_NAME, "Bm3ON")[:5]  

        if not product_elements:
            print("No products found.")
            return []

        for product in product_elements:
            try:
                name = product.find_element(By.CLASS_NAME, "RfADt").text.strip()

                price = product.find_element(By.CLASS_NAME, "ooOxS").text.strip()

                link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

                image_url = product.find_element(By.TAG_NAME, "img").get_attribute("src")

                products.append({
                    'name': name,
                    'price': price,
                    'link': link,
                    'image_url': image_url,
                })

            except Exception as e:
                print(f"Error extracting product data: {e}")
                continue

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

    return products


if __name__ == "__main__":
    query = input("Enter a product to search on Lazada SG: ")
    results = scrape_lazada_sg(query)
    if results:
        for idx, product in enumerate(results, 1):
            print(f"\nProduct {idx}:")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"Link: {product['link']}")
            print(f"Image URL: {product['image_url']}")
    else:
        print("No products found or there was an error scraping data.")
