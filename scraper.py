import requests
from bs4 import BeautifulSoup
import pandas as pd



def get_promotion_period(soup):
    print(soup.prettify())
    promotion_period = soup.find('h1', class_='content-title').text.split()[0]
    return promotion_period

def clean_price(raw_price):
    return float(
        raw_price
        .replace("лв.", "")
        .replace(" ", "")
        .replace(",", ".")
    )

def get_number_of_pages(soup):
    end_btn = soup.select_one('cx-pagination a.end')
    if not end_btn:
        return 1
    return int(end_btn['href'].split('=')[1])


def extract_products(product_card):
    try:
        product_name = product_card.find('a', class_='product-box__title-link')['title']
        name = product_name.split(',')[0]
        product_link = product_card.find('a', class_='product-box__title-link')['href']
        full_link = ''
        if product_link.startswith('/'):
            full_link = f'https://www.technopolis.bg{product_link}'
        else:
            full_link = product_link
        product_price = product_card.find('span', class_='product-box__price-value').text
        product_price = clean_price(product_price)

        return{ 'name': name,
                'link': full_link,
                'price': product_price
            }

    except AttributeError:
        return{}

def clean_products_entities(products):
    unique_products = {p["link"]: p for p in products}.values()
    products = list(unique_products)
    products = sorted(products, key=lambda x: x["price"])
    print(f'Scraped {len(products)} unique products')
    return products

def export_to_excel(products, promotion_period):
    df = pd.DataFrame(products)
    df.to_excel(f"Technopolis promotion - {promotion_period}.xlsx", index=False)
    print('Exported to excel')

def scrape_promotions():
    target_url = f'https://www.technopolis.bg/bg/c/Promotions'
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products_list = []
    promotion_period = get_promotion_period(soup)
    number_of_product_pages = get_number_of_pages(soup)

    for page in range(number_of_product_pages):
        target_url = f'https://www.technopolis.bg/bg/c/Promotions?currentPage={page}'
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_card = soup.find_all('te-product-box')
        for product in product_card:
            extracted_product = extract_products(product)
            if extracted_product:
                products_list.append(extracted_product)
            else:
                continue

        print(f"Scraped page {page}/{number_of_product_pages}, total products: {len(products_list)}")
    products_list = clean_products_entities(products_list)
    export_to_excel(products_list, promotion_period)

scrape_promotions()