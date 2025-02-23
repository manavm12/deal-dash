from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scraper_amazon import scrape_amazon_sg
from scraper_ebay import scrape_ebay_sg
from scraper_lazada import scrape_lazada_sg
import statistics
import numpy as np

products = []
rank1_products = []
rank2_products = []
rank3_products = []

def fetch_products(query):
    global rank1_products,rank2_products,rank3_products,products
    amazon_products = scrape_amazon_sg(query)
    lazada_products = scrape_lazada_sg(query)
    ebay_products = scrape_ebay_sg(query)

    products = amazon_products + lazada_products + ebay_products

    for product in products:
        match product.rank:
            case 1:
                rank1_products.append(product)
            case 2:
                rank2_products.append(product)
            case 3:
                rank3_products.append(product)
    return 0

def calculate_ideal_price(rank1_products, rank2_products, rank3_products):
    rank1_prices = []
    rank2_prices = []
    rank3_prices = []

    for product in rank1_products:
        rank1_prices.append({"price": product.price, "done": False})
    
    for product in rank2_products:
        rank2_prices.append({"price": product.price, "done": False})

    for product in rank3_products:
        rank3_prices.append({"price": product.price, "done": False})

    final_price_list = rank1_prices[:]

    def compute_stats(price_list):
        prices = [item["price"] for item in price_list]
        mean_val = statistics.mean(prices)
        sd_val = statistics.stdev(prices) if len(prices) > 1 else 0
        return mean_val, sd_val

    final_mean, final_sd = compute_stats(final_price_list)
    final_variation = final_sd / final_mean if final_mean != 0 else 0

    while final_variation > 0.25:
        index = furthest_item(final_price_list, final_mean)
        
        if index < len(rank2_prices) and not rank2_prices[index]['done']:
            final_price_list[index]["price"] = rank2_prices[index]["price"]
            rank2_prices[index]['done'] = True
        elif index < len(rank3_prices) and not rank3_prices[index]['done']:
            final_price_list[index]["price"] = rank3_prices[index]["price"]
            rank3_prices[index]['done'] = True
        else:
            final_price_list.pop(index)
        
        if not final_price_list:
            break

        final_mean, final_sd = compute_stats(final_price_list)
        final_variation = final_sd / final_mean if final_mean != 0 else 0
    
    print(final_price_list)
    return final_mean

def compute_price_score(products, ideal_price):
    valid_prices = [product.price for product in products if 0.5 * ideal_price < product.price < 1.5 * ideal_price]
    
    if not valid_prices:
        return  

    max_deviation = max(abs(ideal_price - price) for price in valid_prices)

    if max_deviation == 0:
        k = 1 
    else:
        k = (0.5 * ideal_price) / max_deviation

    for product in products:
        if 0.5 * ideal_price <= product.price <= 1.5 * ideal_price:
            score = 0.5 + k * ((ideal_price - product.price) / ideal_price)
            product.price_score = max(0, min(1, score))
        else:
            product.price_score = 0

    print(f"Max Deviation: {max_deviation}")
    print(k)

def furthest_item(price_list, mean):
    furthest_index = 0
    max_distance = 0
    for i in range(len(price_list)):
        price = price_list[i]["price"]
        distance = abs(mean - price)
        if distance > max_distance:
            furthest_index = i
            max_distance = distance
    return furthest_index

def compute_similarity_score(products, query):
    corpus = [query.lower()] + [product.name.lower() for product in products]  
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()

    query_vector = vectors[0].reshape(1, -1)
    product_vectors = vectors[1:]
    similarities = cosine_similarity(query_vector, product_vectors)[0]

    for product, similarity in zip(products, similarities):
        product.similarity_score = similarity

def compute_rank_score(products):
    for product in products:
        product.rank_score = 1 / product.rank  

def compute_final_score(products):
    for product in products:
        product.final_score = (
            0.4 * product.price_score +
            0.3 * product.similarity_score +
            0.3 * product.rank_score
        )
        

def print_products(products):
     for idx, product in enumerate(products, 1):
            print(f"\nProduct {idx}:")
            print(f"Platform: {product.platform}")
            print(f"Name: {product.name}")
            print(f"Price: {product.price}")
            print(f"Link: {product.link}")
            print(f"Price Score: {product.price_score}")
            print(f"Semantic Score: {product.similarity_score}")
            print(f"Rank Score: {product.rank_score}")
            print(f"Final Score: {product.final_score}")


def recommend_products(query):
    fetch_products(query)
    ideal_price = calculate_ideal_price(rank1_products, rank2_products, rank3_products)

    compute_price_score(products, ideal_price)
    compute_rank_score(products)
    compute_similarity_score(products, query)
    compute_final_score(products)

    products.sort(key=lambda product: product.final_score, reverse=True)

    print_products(products)

if __name__ == "__main__":
    query = input("Enter a product to search: ")
    recommend_products(query)

