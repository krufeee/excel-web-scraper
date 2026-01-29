
import pandas as pd
import requests
from bs4 import BeautifulSoup


current_page = 0

target_url = 'https://www.technopolis.bg/bg/c/Promotions'
response = requests.get(target_url)
soup = BeautifulSoup(response.text, 'html.parser')

promotion_period = soup.find('h1', class_='content-title').text.split()[0]
number_of_product_pages = end_button = soup.select_one('cx-pagination a.end')['href'].split('=')[1]
number_of_product_pages = int(number_of_product_pages)



products_list = []

for page in range (1,number_of_product_pages + 1):
    target_url = f'https://www.technopolis.bg/bg/c/Promotions?currentPage={current_page}'
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_card = soup.find_all('te-product-box')


    for product in product_card:
        try:
            product_name = product.find('a', class_='product-box__title-link')['title']
            name = product_name.split(',')[0]
            product_link = product.find('a', class_='product-box__title-link')['href']
            full_link = ''
            if product_link.startswith('/'):
                full_link = f'https://www.technopolis.bg{product_link}'
            else:
                full_link = product_link
            product_price = product.find('span', class_='product-box__price-value').text

            products_list.append({
                'name': name,
                'link': full_link,
                'price': float(product_price)
            })

        except AttributeError:
            continue
    current_page += 1
    print(f"Scraped page {page}/{number_of_product_pages}, total products: {len(products_list)}")


unique_products = {p["link"]: p for p in products_list}.values()
products = list(unique_products)
products = sorted(products, key=lambda x: x["price"])

print(f'Scraped {len(products)} unique products')



df = pd.DataFrame(products)
df.to_excel(f"Technopolis promotion - {promotion_period}.xlsx", index=False)
