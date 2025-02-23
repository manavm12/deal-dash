import re

def clean_price(input_price):
    match = re.search(r'[\d,.]+', input_price)
    if match:
        return float(match.group().replace(',', ''))
    return 0.0

