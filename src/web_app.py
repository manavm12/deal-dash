import streamlit as st
from product_recommendation import recommend_products

st.set_page_config(
    page_title="Deal Dash Product Recommendations",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 1.5em;
            font-weight: 600;
            color: #444444;
            margin-top: 30px;
        }
        .product-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .product-name {
            font-size: 1.5em;  /* Increased size */
            font-weight: 600;
            color: #333333;
        }
        .price {
            font-size: 2em;
            font-weight: bold;
            color: #1f77b4;
        }
        .platform {
            font-size: 1.8em;
            font-weight: 600;
            color: #228B22;
        }
        .buy-button {
            background-color: transparent;
            color: #FF5722;
            padding: 10px 20px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: bold;
            border: 2px solid #FF5722;
            display: inline-block;
            transition: background-color 0.3s, color 0.3s;
        }
        .buy-button:hover {
            background-color: #FF5722;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">Deal Dash Product Recommendations</div>', unsafe_allow_html=True)
st.write("Get the best product recommendations from **Amazon**, **eBay**, and **Lazada** based on price, relevance, and ranking.")

# Search Bar
query = st.text_input("🔍 Enter a product to search:")

# Trigger recommendation when the button is clicked
if st.button("Search"):
    recommended_products = recommend_products(query)

    if recommended_products:
        # Display Top Recommendations
        st.markdown('<div class="subheader">🏆 Top Product Recommendations</div>', unsafe_allow_html=True)

        for idx, product in enumerate(recommended_products, 1):
            with st.container():
                st.markdown(f"""
                    <div class="product-card">
                        <div style="display: flex; align-items: center;">
                            <div style="flex: 1;">
                                <img src="{product.image_url}" width="150" style="border-radius: 10px;">
                            </div>
                            <div style="flex: 3; padding-left: 20px;">
                                <p class="product-name"><a href="{product.link}" target="_blank">{product.name}</a></p>
                                <p class="platform">Platform: {product.platform}</p>
                                <p class="price">Price: ${product.price}</p>
                            </div>
                            <div style="flex: 2;">
                                <h4>Final Score: {product.final_score:.2f}</h4>
                                <progress value="{product.final_score}" max="1" style="width: 100%;"></progress>
                            </div>
                            <div style="flex: 1; text-align: center;">
                                <a class="buy-button" href="{product.link}" target="_blank">🛒 Buy Now</a>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    else:
        st.error("❌ No products found. Please try again with a different search term.")
