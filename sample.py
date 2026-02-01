from playwright.sync_api import sync_playwright




def run():
    with sync_playwright() as p:
        # Стартираме браузъра
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🚀 Отваряне на Technopolis (бърз режим)...")

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
                print("✅ Бисквитките са приети.")
            except:
                print("ℹ️ Прозорецът за бисквитки не се появи (може би вече е приет).")

            # 2. Улавяне на API заявката
            print("⏳ Очакване на продуктите...")

            # Тук чакаме специфичната заявка
            with page.expect_response(lambda response: "products/search" in response.url,
                                      timeout=30000) as response_info:
                # Скролваме леко надолу, за да сме сигурни, че тригърваме зареждането
                page.mouse.wheel(0, 500)

                response = response_info.value
                data = response.json()

                products = data.get('products', [])
                if products:
                    print(f"\n📦 Успех! Намерени {len(products)} продукта:")
                    for p in products:
                        print(f" - {p.get('name')} | {p.get('price', {}).get('formattedValue')}")
                else:
                    print("⚠️ Списъкът с продукти е празен.")

        except Exception as e:
            print(f"❌ Възникна грешка: {e}")

        print("\nЗатваряне след 5 секунди...")
        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    run()