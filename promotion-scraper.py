
from playwright.sync_api import sync_playwright
import pandas as pd


def run():
    with sync_playwright() as p:
        # Starting chromium browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Opening website...")


        try:
# ------------------------------------FUNCTIONS LOBBY--------------------------------------------------
            # Function for extracting products from current page
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


            # Function for extracting product details for current product
            def extract_product_data(current_product):
                return {
                    "name": current_product.get("name"),
                    "price": float(current_product.get("price", {}).get("value")),
                    "link": "https://www.technopolis.bg" + current_product.get("url", ""),

                }
            # Function for exporting extracted products details in excel sheet
            def export_to_excel(list_of_products, period):
                df = pd.DataFrame(list_of_products)
                df.to_excel(f"Technopolis promotion {period}.xlsx", index=False)
                print('Exported to excel...')
#------------------------------------------------------------------------------------------------------

            # Чакаме само зареждане на DOM, за да не увисва на реклами
            page.goto("https://www.technopolis.bg/bg/Promo/c/Promotions",
                      wait_until="domcontentloaded",
                      timeout=60000)

            # Кликване на бисквитките (ако се появят)
            selector = "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
            # try:
            #     page.wait_for_selector()
            try:
                page.wait_for_selector(selector, timeout=5000)
                page.click(selector)
                print("Accepted cookies.")
            except:
                print("Cookies are accepted already.")

            page.wait_for_timeout(2000)

            # Кликване на технополис приложението (ако се появи)
            selector = ".modal-container"
            button = ".modal-close"
            try:
                page.wait_for_selector(selector, timeout=2000)
                print("Ad popup.")
                page.wait_for_timeout(2000)
                page.wait_for_selector(button, timeout=2000)
                page.wait_for_timeout(2000)
                page.click(button)
                page.wait_for_timeout(2000)
                print('Ad closed.')

            except:
                print("Ad did not showed up.")

            page.wait_for_timeout(2000)

            # Избираме само промоционалните продукти
            page.get_by_role("link", name="Продукти от брошурата").click(timeout=5000)
            print('Loading promotional products...')

            pagination = get_page_number_return_data(1)["pagination"]
            number_of_pages = pagination["totalPages"]
            number_of_products = pagination["totalResults"]
            print(f'Found {number_of_pages} pages.')
            print(f'Found {number_of_products} products.')

            clean_products = []

            for current_page in range(1,number_of_pages + 1):
                    current_data = get_page_number_return_data(current_page)
                    products = current_data["products"]
                    print(f'Extracting {current_page}.')

                    for product in products:
                        extracted = extract_product_data(product)
                        clean_products.append(extracted)

                    print(f'Extracted {len(clean_products)} products.')


            print(f'Removing duplicating products.')
            # convert the list into a set to remove duplicates
            unique_products = list({frozenset(p.items()) for p in clean_products})

            # Convert back to dictionaries
            unique_products = [dict(p) for p in unique_products]

            promotion_period_element = page.query_selector('.content-title')
            promotion_period = promotion_period_element.inner_text()
            print(f'Extracted {len(clean_products)} unique products.')

            export_to_excel(unique_products, promotion_period.split()[0])


        except Exception as e:
            print(f"Error: {e}.")

        print("\nClosing after 5 seconds...")
        page.wait_for_timeout(5000)
        browser.close()



if __name__ == "__main__":
    run()







