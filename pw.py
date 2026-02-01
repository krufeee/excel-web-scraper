from asyncio import timeout
from playwright.sync_api import sync_playwright



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
                print('Рекламата е затворена')

            except:
                print("Рекламата не се появи.")



            # 3. Залъгваме страницата за да се хванем API
            page.get_by_role("link", name="Продукти от брошурата").click(timeout=5000)
            print('Зареждаме промоционалните продукти')


            with page.expect_response(
                    lambda r: "products/search" in r.url and r.status == 200
            ) as resp_info:
                page.get_by_role("link", name="2", exact=True).click()
                page.wait_for_timeout(2000)
                print('Сменяме страниците')
                page.get_by_role("link", name="1", exact=True).click()
                page.wait_for_timeout(2000)
                print('Връщаме се в началната страница')

            response = resp_info.value
            data = response.json()


            products = data["products"]
            print(type(products))
            print(len(products))
            print(products[0])

            print(products[0]['code'])
            print(products[0]['name'])
            print(products[0]['price']['value'])
            print(products[0]['url'])
            print(products[0]['categories'][0]['name'])

            dict_keys = (['baseOptions', 'bfStockAndPrice', 'blackFridayHeroProduct', 'categories', 'code', 'deliveryCosts',
                       'description', 'ean', 'expressDelivery', 'hideSticker', 'imagePanelComponents', 'images',
                       'infoPriceOffline', 'leasingEligible', 'leasingPromotion', 'markNew', 'name',
                       'noInterestLeasingPeriod', 'numberOfReviews', 'onlineExclusive', 'onlineOnly',
                       'pickUpFromCustomerStoreLabel', 'pickUpFromOnlineWarehouseLabel', 'pickUpTodayLabel',
                       'potentialPromotions', 'price', 'purchasable', 'showBuyButton', 'showOldPrice', 'showPcd',
                       'showPromoPriceCounter', 'showSavingsAsPercent', 'soldIndividually', 'soldOut', 'stock', 'url',
                       'variantsAllValuesMap'])



        except Exception as e:
            print(f" Възникна грешка: {e}")

        print("\nЗатваряне след 5 секунди...")
        page.wait_for_timeout(5000)
        browser.close()



if __name__ == "__main__":
    run()