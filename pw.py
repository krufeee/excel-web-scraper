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



            # 2. Кликване на технополис приложението (ако се появи)
            selector = ".modal-container"
            button = ".modal-close"

            try:
                page.wait_for_selector(selector, timeout=5000)
                print("✅ Рекламата се появи.")

            except:
                print("Рекламата не се появи.")

            try:
                page.wait_for_selector(button, timeout=5000)
                page.click(button)
                print('Рекламата е затворена')
            except:
                print('Не се появи реклама')


            # 2. Улавяне на API заявката
            print("⏳ Очакване на продуктите...")


        except Exception as e:
            print(f"❌ Възникна грешка: {e}")

        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    run()