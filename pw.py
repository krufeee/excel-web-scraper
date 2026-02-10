
from playwright.sync_api import sync_playwright
import pandas as pd


def run():
    with sync_playwright() as p:
        # Стартираме браузъра
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Отваряне на Technopolis (бърз режим)...")


        try:
            # Чакаме само зареждане на DOM, за да не увисва на реклами
            page.goto("https://www.technopolis.bg/bg/Promo/c/Promotions",
                      wait_until="domcontentloaded",
                      timeout=60000)

            # 1. Кликване на бисквитките (ако се появят)
            selector = "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"

            try:
                page.wait_for_selector(selector, timeout=5000)
                page.click(selector)
                print("Бисквитките са приети.")
            except:
                print("Прозорецът за бисквитки не се появи (може би вече е приет).")

            page.wait_for_timeout(2000)

            # 2. Кликване на технополис приложението (ако се появи)
            selector = ".modal-container"
            button = ".modal-close"
            try:
                page.wait_for_selector(selector, timeout=2000)
                print("Рекламата се появи.")
                page.wait_for_timeout(2000)

                page.wait_for_selector(button, timeout=2000)
                page.wait_for_timeout(2000)
                page.click(button)
                page.wait_for_timeout(2000)
                print('Рекламата е затворена.')

            except:
                print("Рекламата не се появи.")



            # Избираме само промоционалните продукти
            page.get_by_role("link", name="Продукти от брошурата").click(timeout=5000)
            print('Зареждаме промоционалните продукти.')

            # 3. Залъгваме страницата за да се хванем API
            def get_page_number_return_data(curr_p):
                data=''
                if   curr_p == 1:
                    with page.expect_response(
                            lambda r: "products/search" in r.url and r.status == 200
                    ) as resp_info:
                        page.get_by_role("link", name="2", exact=True).click()
                        page.wait_for_timeout(2000)
                        page.get_by_role("link", name="1", exact=True).click()
                        page.wait_for_timeout(2000)
                        response = resp_info.value
                        data = response.json()
                else:
                    with page.expect_response(lambda r: "products/search" in r.url and r.status == 200
                    ) as resp_info:
                        page.wait_for_timeout(2000)
                        page.get_by_role("link", name=f"{curr_p}", exact=True).click()
                        response = resp_info.value
                        data = response.json()

                return data


            pagination = get_page_number_return_data(1)["pagination"]

            number_of_pages = pagination["totalPages"]
            number_of_products = pagination["totalResults"]


            print(f'Намерени {number_of_pages} страници.')
            print(f'Очакван брой на продуктите - {number_of_products}.')



            # Извличаме нужната информация за продукта
            def extract_product_data(current_product):
                return {
                    "name": current_product.get("name"),
                    "price": float(current_product.get("price", {}).get("value")),
                    "link": "https://www.technopolis.bg" + current_product.get("url", ""),

                }
            clean_products = []

            for current_page in range(1,number_of_pages + 1):
                    current_data = get_page_number_return_data(current_page)
                    products = current_data["products"]
                    print(f'Извличане на страница {current_page}.')

                    for product in products:
                        extracted = extract_product_data(product)
                        clean_products.append(extracted)

                    print(f'Извлечени {len(clean_products)} продукта.')

            def export_to_excel(list_of_products):
                df = pd.DataFrame(list_of_products)
                df.to_excel(f"Technopolis promotion.xlsx", index=False)
                print('Експортиране в Excel файл.')

            export_to_excel(clean_products)


        except Exception as e:
            print(f"Възникна грешка: {e}.")

        print("\nЗатваряне след 5 секунди...")
        page.wait_for_timeout(5000)
        browser.close()



if __name__ == "__main__":
    run()